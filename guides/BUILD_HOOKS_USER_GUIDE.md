# Customize your build with local hooks

Add YAML recipes under `.c2/recipes/hooks/build/` in your project repository to
customize the shared C2 build. You can run tests, supply design research, add prompt
guidance, require specialist reviews, prepare generated files, and publish after
merge. Install only the hooks your project needs.

Use a c2j build with repository-local hooks and value artifacts (`66cbded` or later),
including the corrections in [the runtime compatibility report](BUG_C2J_VALUE_ARTIFACT_COMPATIBILITY.md), and
the shared build recipe containing these hooks. The runtime and recipe versions
used for validation are listed in the [hook validation report](BUILD_HOOKS_VALIDATION.md)
and [value-artifact migration report](VALUE_ARTIFACT_MIGRATION.md).

## Choose your hooks

All paths below are relative to the repository root, including in a monorepo.

| File under `.c2/recipes/hooks/build/` | When it runs | What to use it for |
| --- | --- | --- |
| `configure.yaml` | Once, before framing the request | Prompt additions, named values, specialist requests |
| `before_design.yaml` | Before each framing round, including redesign | Research, alternatives, constraints, reference material |
| `prepare.yaml` | After rebase, before candidate assessment and verification | Formatting or generating files that need review |
| `verify.yaml` | Before successful completion, including unchanged and delegated outcomes | Tests, lint, builds, existing CI workflows |
| `publish.yaml` | After a successful merge | Packages, images, documentation, deployments |

The current shared build uses Adaptive3 and always requests direction approval for
delivery work. Configure hooks may still return `require_design`; setting it to
false does not bypass this checkpoint. See [the process](../ADAPTIVE_BUILD_PROCESS.md).

Prepare may change the managed repository; its changes receive normal assessment
and review. The shared recipe invokes the other hooks with `const: true`, inherited
by nested steps. c2j discards their repository edits while retaining outputs and
artifacts. Publish uses the
exact merged commit even if the branch advances afterward. It does not run for
unchanged, delegated, cancelled, or failed-merge outcomes.

c2j selects hook code using the configured `source_hooks` policy and enforces hook
permissions and source trust. The shared recipe uses `cell://` includes and leaves
that selection to the runtime. A floating branch may advance between read-only
tasks; a changed hash alone is not evidence that a hook edited the repository.

A missing hook produces a `skipped` report. Invalid YAML, malformed results,
permission errors, and timeouts fail the invocation; they do not count as absence.

A verify hook can optionally return a `checks` object keyed by stable requirement
or test IDs, for example `{"tenant-switch":"passed","token-denial":"failed"}`.
Each value is `passed`, `failed`, or `skipped`. Report the overall status as usual.
Adaptive3 records newly passing checks even when the overall result is failed.
Use the same IDs on every retry so repeated results count once.

## Start with verification

There is no automatic `build.sh` discovery. If you already have that script, install
this as `.c2/recipes/hooks/build/verify.yaml` to invoke it explicitly. Replace the
command with your own test entrypoint as needed.

```yaml
id: project-verify
inputs:
  target_directory: ${{ inputs.target_directory }}
sequence:
- id: tests
  op: command_execution
  const: true
  inputs:
    env:
      TARGET: '{{ context.environment.op.worktree_path }}/{{ inputs.target_directory }}'
      OUTBOX: ${{ context.environment.op.outbox }}
    run: |
      cd "$TARGET" || exit 1
      if bash ./build.sh > "$OUTBOX/tests.log" 2>&1; then
        printf passed
      else
        printf failed
      fi
outputs:
  api_version: c2.build-hook/v1
  status: ${{ sequence.tests.outputs.stdout }}
  summary: Repository checks completed; inspect tests.log.
  artifact_refs: "${{ {'tests.log': sequence.tests.artifacts['tests.log']} }}"
```

A semantic `failed` result returns the evidence to implementation for repair.
The shell above translates a test exit status into that result. Verification
also returns to implementation when hook loading, execution, output validation,
or report generation fails. This includes timeouts and denied
capabilities. The build supplies `verification.md` and a structured failure under
`hooks/verify/<round>/failure.json`, preserving the original failure origin.
Invalid hook artifact maps are not rebound to produce this fallback report;
original task logs remain in the job story. Cancellation still stops execution.
Move formatters and generators into prepare when their changes must survive to
later tasks. Verification's temporary repository edits are discarded by c2j.

Verification is optional by default. To require it, set **the build input**
`require_verification: true` when submitting the build. This is not a configure
setting. An absent or explicitly skipped verify hook then returns to implementation
to configure or repair verification. It cannot permit completion. Repair is
followed by fresh rebase, assessment, verification, and normal outcome review;
failed verification clears approval reuse. Failures outside verification retain
their existing propagation, including implementation-agent and publish-hook errors.

For an existing GitHub Actions workflow, use the
[verify-gha example](../examples/build-hooks/verify-gha.yaml) as `verify.yaml`.
It calls c2ops `gha` and maps the workflow result to the hook status. Its local
backend requires Docker and a workflow declaring `workflow_dispatch`.
See the [GitHub Actions guide](ops/OP_GITHUB_ACTIONS.md) for backend selection,
credentials, artifact output, and `gha-many`.

## Add prompt guidance and named values

Install this as `.c2/recipes/hooks/build/configure.yaml`:

```yaml
id: project-configure
sequence: []
outputs:
  api_version: c2.build-hook/v1
  status: passed
  summary: Apply project design and verification guidance.
  artifact_refs: {}
  settings:
    require_design: true
    prompt_additions:
      design: Compare alternatives and explain operational costs.
      test_plan: Include negative authorization and tenant-isolation cases.
      implementation: Preserve the documented public API.
      plan_assessment: Check that the proposal addresses migration risks.
      outcome_assessment: Check failure behavior and rollback assumptions.
    variables:
      release_channel: preview
      compatibility_window_months: 6
    consultations: []
```

The five prompt-addition keys shown above are the supported keys. Guidance is added
to the appropriate phase without replacing workflow instructions, output schemas,
or human approval. `implementation` applies during implementation; assessment
guidance also reaches the configured specialists at that checkpoint.

Adaptive3 frames delivery work and asks for direction approval.
`require_design` remains accepted by the shared configure contract but does not
change that behavior. Design guidance and `before_design.yaml` run during framing.

Omitted settings use defaults: `require_design: false`, empty prompt additions,
empty variables, and no configured consultations. Unknown settings are rejected.
Variables can hold JSON scalars, arrays, and objects. They remain data, including
text resembling shell commands or template expressions. Keep credentials out of
settings and prompt text; use hook permissions instead.

Configuration is captured once for the build. It survives revision, upstream
rebases, and redesign. Editing configure affects a new build.
Other hooks resolve at their checkpoint from the current candidate, including
unpushed changes. Child builds load their own cell's configuration.

### Read named values in a later hook

Later hooks receive a value-backed `settings` artifact containing normalized
`build-settings.json`. The existing 16,000-character settings limit still applies.
Agents also receive it as context. To let a script read it, bind the artifact into
that operation's inbox. This fragment belongs inside a hook:

```yaml
inputs:
  settings: ${{ inputs.settings }}
sequence:
- id: consume_settings
  op: command_execution
  const: true
  artifacts:
    build-settings.json: ${{ inputs.settings }}
  inputs:
    env:
      SETTINGS_FILE: '{{ context.environment.op.inbox }}/build-settings.json'
    run: ./scripts/check-project-policy.sh "$SETTINGS_FILE"
```

The script reads values such as `variables.release_channel` from the JSON file.
Do not evaluate the JSON as shell code. The complete hook must also return the
standard result described below.

## Supply research before design

Use `before_design.yaml` for custom research automation. Export findings through
`artifact_refs`; creating an outbox file alone does not select it as a deliverable.
For example:

```yaml
id: project-design-research
sequence:
- id: research
  op: command_execution
  const: true
  inputs:
    env:
      OUTBOX: ${{ context.environment.op.outbox }}
    run: ./scripts/research-alternatives.sh > "$OUTBOX/alternatives.md"
outputs:
  api_version: c2.build-hook/v1
  status: passed
  summary: Compare the alternatives in the attached research.
  artifact_refs: "${{ {'alternatives.md': sequence.research.artifacts['alternatives.md']} }}"
```

The designer and plan reviewers receive this evidence. A new design round refreshes
it; clarification within the same round does not. Research does not approve the
design or replace the canonical design and test statements. For alternative agent
thinking, a configured advisory consultation can be simpler than a research script.

## Require security or other specialist consultations

Add requests under `settings.consultations` in configure. Each request needs a
unique key, a checkpoint, a role, a concrete request, and a `required` boolean:

```yaml
consultations:
- key: alternatives
  checkpoint: before_design
  role: Independent architect
  request: Propose alternatives and identify assumptions worth challenging.
  required: false
- key: security_plan
  checkpoint: plan_assessment
  role: Security architect
  request: Review trust boundaries, authorization, and proposed negative tests.
  required: true
- key: security_outcome
  checkpoint: outcome_assessment
  role: Security reviewer
  request: Inspect the implemented authorization boundaries and negative tests.
  required: true
```

`before_design` runs after the research hook. `plan_assessment` follows design and
test planning after direction approval. `outcome_assessment` runs after preparation
and before verification. The general candidate assessment also runs when a new
outcome approval is needed.

A required consultation needs both agreement and an explicit passing assessment.
Agreement that problems exist cannot satisfy the gate. Revision findings return
work to the appropriate phase. Advisory findings become evidence the agent must
account for, without adding a pass gate. Execution failures still propagate.

Security, accessibility, performance, and architecture use this same expert API.
Requests inspect the current cell; they do not submit prerequisite implementation
work to another cell. Each revisited checkpoint gets a fresh assessment, so a
completed review is not silently reused for changed work.

## Prepare files and publish deliverables

The [prepare example](../examples/build-hooks/prepare.yaml) runs a project script
that can change tracked files. Make preparation converge: rerunning it on an
already prepared candidate should not introduce unrelated differences. Preparation
runs again after upstream rebases; changed files remain subject to normal review.
A `failed` prepare result returns evidence to implementation.

The [publish example](../examples/build-hooks/publish.yaml) passes `merged_hash` to
an explicit publication script. Publish also receives `target_branch`; checkout
HEAD, `candidate` and `merged_hash` identify the same recorded commit even after
the branch advances. The hook receives selected fields, not a native merge
receipt. The adapter selects that workspace on a containing sequence before
hook pinning and input binding; keep the hook include inside that scope. Putting
`workspace` directly on the cell include can bind `candidate` from the enclosing
job after a restart. Nested jobs must explicitly preserve the immutable source;
this adapter guarantee does not certify a product's nested release handoff.

With ordinary integration (`merge_queue: false`), the build invokes publish after
its successful native merge. Same-job recovery reuses the internal `merge_state`,
bound to the target and accepted Outcome/patch, without merging again. General
`feedback.publication` cannot select publication. Explicit cross-job Integration
recovery may supply it as a producer lookup hint: `merge-receipt.yaml` checks the
successful native task, original human acceptance, patch equivalence, full hash,
target identity and current reachability. Missing or contradictory evidence stops
recovery. Legacy two-field queue receipts and moving refs remain stuck. A failure
preserves the merge; publication does not roll Git or external effects back.

Publisher-only changes use the same merge recipe inline with one contribution;
that merging job performs publication itself. Product-only changes use the grouped
receiver below. Mixed publisher/product changes must be split before either merge
route. See [integration routing](../recipes/adaptive3/README.md).

When inline publication fails, Integration stays stuck and retains the confirmed
merge, original source/base/request/documents/settings and hook diagnostics in its
private `merge_state`. A later Integration validates that state's target and
accepted-patch binding, then retries only the hook at the original full hash,
even after branch advancement or disabling the queue setting. Repeated failure
stays stuck; success or `skipped` completes without another hook call on the next
Integration. Hook adapter errors before invocation also retain the merge.
General feedback and copied queue history cannot authorize this retry. Keep the
original Integration state; a new already-landed submission cannot recover failed
publication. This inline path needs no grouped receiver handle.

With the merge queue enabled, the receiver invokes publish after the final
successful assembled merge. Callers and subset-check children never publish.
The source is the assembled tip; each caller keeps its individual landed hash,
which may be an intermediate commit. Shared verification covers the assembled
tip, not every prefix. A missing or ineligible hook can return `skipped` normally.
An already-landed-only batch returns `no-new-merge`, a null source and a skipped
result; it does not recover or certify an earlier publication.

The receiver supplies the final assembly base, a branch/accepted-ID request,
screened common directory/settings and accepted documents under
`contributions/<Change-Id>/<original-key>`. Artifact bindings transport their bytes.
[Local hook trust and permissions](GUIDE-Local-Recipe-Hooks.md) still control hook
code, secrets and submission; appends cannot combine or grant authority.

A failed grouped receiver hook leaves a failed receiver and successful merge evidence in
its retained native landing and publication tasks, even when final outputs are
absent. Callers retain the completed grouped start item and report stuck. Inspect
that original receiver with `job log`, `job fields` and artifact commands. Discover
a post-merge scope with `job restart-points`, inspect `job restart-context`, then
restart the receiver immediately before publication. Preserve the original source,
base, owner and document references. Do not resubmit or remerge to retry publish.
A continuation has a new job ID; `owner_job` remains the original receiver.

Caller recovery carries the original receiver start item, branch and Change-Id in
`feedback.queue_recovery`. For a restarted publication, supply `repair_job` from
the native restart receipt. The caller reads that exact job and verifies its
retained assembly against the original receiver’s stored bundle and merge. It
then checks its contribution and the published source. A pending, unrelated or
unreadable repair keeps publication open. The receiver owns the publish hook.

Successful receiver generations remain serialized through publish. Failure or
cancellation permits successors; older recovery may therefore run after newer
batches. Repeated or out-of-order receiver publication remains possible on recovery.
Products own branch eligibility, durable release intent, version ordering and
external-effect reconciliation. Cancelling a caller stops its wait, while shared
receiver work remains eligible. Cancelling the receiver before publish prevents
new hook work; cancellation does not undo completed effects.

### Queue receipt and upgrade

Queue contributions, verification policy and receipts use version 2 together.
The grouping namespace ends in `/merge-publish-v2`. Receipt fields are `version`,
`branch`, sorted unique `requested`, per-contribution `results`, and `publication`:

```yaml
publication:
  owner_job: ORIGINAL_RECEIVER_JOB
  source:
    merged_hash: FULL_NATIVE_MERGED_HASH
    target_branch: refs/heads/main
  reason: hook
  result:
    api_version: c2.build-hook/v1
    status: passed
    summary: Published the assembled commit.
    artifact_refs: {}
```

For no new merge, `source` is null, `reason` is `no-new-merge`, and the result is
`skipped`. Callers validate receiver identity, branch, complete result coverage,
full hashes, their Change-Id trailer, reachability and ancestry to the published
source. Rejected callers stay rejected even when accepted peers publish.

Build completion preserves `outputs.merge` as the caller's merge identity,
`outputs.publication` as the shared hook result, and adds `outputs.queue_publication`
for receiver/source/reason/result. Shared hook artifacts are exported under
`outputs.artifact_refs` with `publication/` aliases; JSON references alone do not
hydrate files. Ordinary hook inputs and `c2.build-hook/v1` remain unchanged.

Deploy paired caller/receiver revisions. Drain old queued jobs and unresolved old
publication recovery first: retained jobs keep their captured recipes on restart.
New readers reject v1 receipts and new receivers reject v1 contributions. Separate
grouping namespaces cannot alone prevent old and new external publishers from
both acting. Never fall back to caller publication on incompatibility or denial.

## Hook inputs and results

All hooks receive these inputs:

| Input | Meaning |
| --- | --- |
| `api_version` | `c2.build-hook/v1` |
| `request` | Original build request |
| `target_directory` | Repository-relative task directory; normally `.` |
| `candidate` | Exact commit at hook entry |
| `base` | Integration base for understanding the changes |
| `documents` | Artifact map containing available specifications and evidence |

Hooks after configure also receive `settings`, the configuration artifact. Publish
additionally receives `merged_hash` and `target_branch`. Hooks run from the repository
root; use `target_directory` when your command should run in a component directory.
The [full verify example](../examples/build-hooks/verify.yaml) shows typed input
declarations. Binding only the inputs a hook uses is sufficient; if you declare
an `input_schema`, include all fields supplied by its callsite.

Every hook returns:

```yaml
outputs:
  api_version: c2.build-hook/v1
  status: passed
  summary: Explain what the hook did and where to find evidence.
  artifact_refs: {}
```

`status` must be `passed`, `failed`, or `skipped`. Configure additionally returns
`settings`. Do not add other top-level result fields. `artifact_refs` maps safe
relative names to native artifact references, not strings containing paths. Use
`sequence.<step>.artifacts['filename']` for an outbox file. Names cannot contain
parent traversal, backslashes, or reserved Git-state names.

Reports are exposed as `configuration.md`, `design-context.md`, `preparation.md`,
`verification.md`, and `publication.md`. Exported hook evidence is namespaced under
`hooks/<hook>/<round>/`; specialist findings use `specialists/`. Hook evidence cannot
overwrite the approved specifications or canonical reports.

Results allow up to 64 exported artifact references and 8,192 characters of summary.
Prompt additions allow 8,192 characters per field. The complete normalized settings
must fit within 16,000 characters and may contain at most 40 consultation requests.
Use artifacts for larger evidence and keep configuration compact.

Each operation has its own execution environment. Declare tools through
`execution_needs`; pass evidence through artifacts. Do not rely on tools installed
or temporary files created by a previous operation. Relative recipe includes are
supported, including unpushed local includes. Local selector ops currently require
a fetchable source commit; see the [runtime guide](GUIDE-Local-Recipe-Hooks.md).

## Grant permissions to the hook that needs them

Hook permissions are administered in JobDB, keyed by the exact hook path. Without
grants, a hook has no JobDB capabilities for resolving secrets or submitting jobs.
Local commands without those capabilities need no such grant.

For example, an administrator can grant a publish hook access to a named secret:

```sh
c2j hooks perms add .c2/recipes/hooks/build/publish.yaml \
  --cell my-service --secret PUBLISH_TOKEN --trust-candidate-code
c2j hooks perms get .c2/recipes/hooks/build/publish.yaml --cell my-service
```

Replace `my-service` and `PUBLISH_TOKEN` with your cell and secret. This grants the
capability; the publishing op must still explicitly request the secret through its
supported secret input. It does not automatically become an environment variable.

`--trust-candidate-code` authorizes that capability for candidate hook code.
Alternatively, `--candidate-commit FULL_SHA` restricts it to that exact invocation
candidate. Grant test credentials to verify and publication credentials to publish
as needed. Grants do not transfer to the shared caller or sibling hooks. Add
`--submit-jobs` only for hooks that need child jobs. For embedded runs, administer
permissions in the same embedded JobDB with `--embed`.

Permission changes apply to new jobs. See the
[permission administration reference](GUIDE-Local-Recipe-Hooks.md#permission-administration)
for cell overrides, source trust, removal, and explicit denial.

## Try your configuration

Make the hook files available in the consuming repository's Git candidate. On a
normal local submission, a local commit is a straightforward way to include them;
do not assume an arbitrary untracked working-tree file is part of the job. During
a running build, c2j can load hook edits from its managed unpushed candidate.

Use a disposable project or harmless hook commands for the first run. Submitting
a complete build can reach its normal review, merge, and publish steps.

```sh
c2j self
c2j submit 'Validate the requested project change' \
  --cell /path/to/project \
  --inputs-json '{"require_verification":true}' --run --embed
```

That command uses the shared build selected by c2j. To test a local checkout of the
shared recipe, add `--advanced-recipe-file /path/to/recipes/build.yaml`. Older CLI
versions called this flag `--recipe-file`; check your installed `submit --help`.

For deterministic tests, use runtime-backed integration cases with fixture hook
files. [Verification tests](../recipe-tests/verification.test.yaml) demonstrate
passing, failing, absent, malformed, and timed-out hooks; the
[verification recovery tests](../recipe-tests/verification-recovery.test.yaml)
exercise implementation repair and successful re-verification on both build paths;
the
[integrated hook tests](../recipe-tests/build-hooks-flow.test.yaml) demonstrate both
build paths and security review. Static validation alone does not load late hooks.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Verify is skipped | Is `verify.yaml` at the exact root-relative hook path and present in the candidate? An existing script alone is not discovered. |
| Research never runs | Check the hook path and its invocation diagnostics; Adaptive3 runs `before_design` during framing. |
| Prompt edits have no effect | Configure is captured at startup. Start a new build, and check the phase-specific key. |
| Files generated by a read-only hook disappear | Move generation or formatting into prepare when later tasks need those repository changes. |
| Hook output contract fails | Check the API version, allowed fields, status, and native artifact references. |
| Secret or job submission is denied | Check the exact hook's grants, source trust, JobDB, and secret provider authorization. |
| A custom consultation child requires a snapshot | See the [known c2j clean-pin bug](BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md). Its regression test is temporarily excluded from discovery. |

See the [complete contract](PROPOSAL_BUILD_RECIPE_HOOKS.md) for checkpoint ordering
and detailed limits, and the [example directory](../examples/build-hooks/README.md)
for files to adapt to your project.

## Scoped tool installation authority in Adaptive3

Before scheduling scoped tools, direction and package reviews explain their installation
authority. Private pnpm authorization permits builds for direct, transitive and selected
optional dependencies, mutable transitive resolutions and repeated preparation after failure,
worker changes or cache loss. Keep exact requested references and checks. Changed requests
or installation scope need applicable authority. Questions are not approval; withdrawal,
cancellation and newer human scope take precedence. Unchanged authorized retries need no
second prompt. A legacy pnpm reference/check match alone takes the existing package review.
Baseline recipe, repository, extension and early-hook dependencies use source authority and
applicable standing cell policy; personal job approval does not universally precede setup.

Adaptive3 compares approved additions and unrelated settings against the retained original
baseline before staging, and again before adoption after a successful validation child.
Only a subsequent fresh task prepares the accepted additions. An independently edited
configuration outside this package service is outside that ordering guarantee.

For the separately saved strict-verification candidate, retain `pnpm:pnpm@12.10.1` only on
the verification operation after applicable approval. Do not move it into repository-wide,
recipe-wide, configure or planning dependencies. This correction does not change the runner
pin or establish runtime activation or that candidate's fresh full worker acceptance.

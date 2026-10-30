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
| `configure.yaml` | Once, before choosing light or heavy development | Prompt additions, named values, specialist requests, requiring design |
| `before_design.yaml` | Before each heavy design round, including redesign | Research, alternatives, constraints, reference material |
| `prepare.yaml` | After rebase, before candidate assessment and verification | Formatting or generating files that need review |
| `verify.yaml` | Before successful completion, including unchanged and delegated outcomes | Tests, lint, builds, existing CI workflows |
| `publish.yaml` | After a successful merge | Packages, images, documentation, deployments |

Prepare may change the managed repository; its changes receive normal assessment
and review. The other hooks must preserve the managed candidate. Publish uses the
exact merged commit even if the branch advances afterward. It does not run for
unchanged, delegated, cancelled, or failed-merge outcomes.

A missing hook produces a `skipped` report. Invalid YAML, malformed results,
permission errors, and timeouts fail the invocation; they do not count as absence.

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
The shell above translates a test exit status into that result. An operation
error or timeout propagates as an execution failure instead. Verification must not
change the managed candidate; move formatters and generators into prepare.

Verification is optional by default. To require it, set **the build input**
`require_verification: true` when submitting the build. This is not a configure
setting. An absent or explicitly skipped verify hook then blocks completion.

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
or human approval. `implementation` applies on both development paths; assessment
guidance also reaches the configured specialists at that checkpoint.

`require_design: true` selects heavy development. Adding only design prompt text
or a `before_design.yaml` file does not force a light build to have a design phase.

Omitted settings use defaults: `require_design: false`, empty prompt additions,
empty variables, and no configured consultations. Unknown settings are rejected.
Variables can hold JSON scalars, arrays, and objects. They remain data, including
text resembling shell commands or template expressions. Keep credentials out of
settings and prompt text; use hook permissions instead.

Configuration is captured once for the build. It survives revision, upstream
rebases, and escalation from light to heavy. Editing configure affects a new build.
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
test planning. Either checkpoint forces heavy development. `outcome_assessment`
runs after preparation and before verification on both light and heavy builds.
The heavy path retains its general assessment in addition to these specialists.

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
an explicit publication script. Publish also receives `target_branch`, and its
`candidate` equals `merged_hash`. It preserves the managed repository and uses
ordinary c2j execution and failure handling. The build adds no custom publication
recovery or rollback protocol. A publication failure does not undo the Git merge.

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
[integrated hook tests](../recipe-tests/build-hooks-flow.test.yaml) demonstrate both
build paths and security review. Static validation alone does not load late hooks.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Verify is skipped | Is `verify.yaml` at the exact root-relative hook path and present in the candidate? An existing script alone is not discovered. |
| Research never runs | Light builds have no design round. Set `require_design: true` or configure a design-stage consultation. |
| Prompt edits have no effect | Configure is captured at startup. Start a new build, and check the phase-specific key. |
| Read-only hook changed the candidate | Move tracked-file generation or formatting into prepare. |
| Hook output contract fails | Check the API version, allowed fields, status, and native artifact references. |
| Secret or job submission is denied | Check the exact hook's grants, source trust, JobDB, and secret provider authorization. |
| A custom consultation child requires a snapshot | See the [known c2j clean-pin bug](BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md). Its regression test is temporarily excluded from discovery. |

See the [complete contract](PROPOSAL_BUILD_RECIPE_HOOKS.md) for checkpoint ordering
and detailed limits, and the [example directory](../examples/build-hooks/README.md)
for files to adapt to your project.

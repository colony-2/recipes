# Proposal: local hooks for the build recipe

Status: implemented in the shared build recipes. Acceptance suites live under `recipe-tests/`.
See [validation results and the remaining c2j limitation](BUILD_HOOKS_VALIDATION.md).

## Recommendation

Add five optional repository-local hooks, spanning configuration, design,
implementation, and publication:

| Hook | Repository-relative path | Purpose |
| --- | --- | --- |
| Configure | `.c2/recipes/hooks/build/configure.yaml` | Supply prompt additions, named values, and specialist consultation requests at build startup. |
| Before design | `.c2/recipes/hooks/build/before_design.yaml` | Research alternatives and supply evidence before drafting or revising a design. |
| Prepare | `.c2/recipes/hooks/build/prepare.yaml` | Format files, regenerate checked-in code, or otherwise prepare the candidate for review. |
| Verify | `.c2/recipes/hooks/build/verify.yaml` | Run the repository's tests, lint, build, or existing CI workflows. |
| Publish | `.c2/recipes/hooks/build/publish.yaml` | Publish packages, images, documentation, or other deliverables after merge. |

Invoke each through a late `cell://` include, using the capability described in
[Repository-local recipe hooks](GUIDE-Local-Recipe-Hooks.md). These are ordinary
recipes included in the build job. A hook can compose relative includes and real
ops; it need not start another job. A hook that chooses to delegate must await its
children and aggregate their results before returning.

Replace automatic `build.sh` discovery in one change. A repository may keep that
script and explicitly call it from its verify hook. The shared build recipe will
no longer attach special meaning to the filename.

This fits the recipes cell's purpose: this cell owns hook locations, contracts,
orchestration, and review artifacts. Consuming cells own their hook bodies. c2j
owns hook resolution, pinning, permissions, durability, and retry behavior; c2ops
owns the operations a hook invokes. This proposal adds no runtime mechanisms.

## Current behavior and proposed placement

Both build paths call [the shared verification helper](../recipes/develop/verify.yaml).
It discovers `build.sh` inside `target_directory`, runs it if present, and produces
`verification.md` and an optional `build.log`. Light builds additionally repeat a
`verification_command` supplied by the implementation agent. Missing checks are
reported as skipped and allow the existing review gates to proceed.

The proposed order is:

```text
configure hook
  → classification (configuration may require the heavy path)
  → before_design hook and configured research consultations (heavy)
  → design and test statements (heavy)
  → independent plan assessment and configured specialists (heavy)
  → human plan review (heavy)
  → implementation and prerequisite completion
  → rebase when needed
  → prepare hook
  → refresh candidate inventory
  → independent implementation assessment (heavy) and configured specialists (both)
  → verify hook
  → file accounting / synopsis and human outcome review
  → squash and merge
  → publish hook
```

The hooks do not replace design review, independent assessment, human acceptance,
or the normal dependency lifecycle.

### Configure: values and prompt additions at startup

Run once at entry to `build.yaml`, in the consuming workspace, before classification
and the first agent session. It is read-only with respect to the Git candidate.
This is a recipe step returning explicit outputs, not a way to mutate global CEL
variables or arbitrary parent inputs.

In addition to the common result envelope, configure returns a required `settings`
object with these fields:

| Field | Type / default | Use |
| --- | --- | --- |
| `require_design` | boolean / `false` | Require the heavy path even if classification would select light. Never force light. |
| `prompt_additions` | object / `{}` | Optional strings keyed by `design`, `test_plan`, `implementation`, `plan_assessment`, and `outcome_assessment`. |
| `variables` | JSON object / `{}` | Repository-defined values for later hooks and agent context. |
| `consultations` | array / `[]` | Specialist requests using the contract below. |

For example, configure could return these additional outputs:

```yaml
settings:
  require_design: true
  prompt_additions:
    design: >-
      Compare a managed service with extending the current implementation.
      Explain the operational cost and reversibility of each option.
    test_plan: Include negative cases for cross-tenant access.
    implementation: Preserve the documented public API compatibility guarantees.
  variables:
    deployment_tier: internal
    compatibility_window_months: 6
  consultations:
    - key: security_design
      checkpoint: plan_assessment
      role: Security architect
      request: Review trust boundaries, authorization, and the proposed negative tests.
      required: true
    - key: security_implementation
      checkpoint: outcome_assessment
      role: Security reviewer
      request: Inspect the implemented authorization boundaries and negative tests.
      required: true
```

The configure callsite extends its self-contained output schema with `settings`:
reject unknown settings and prompt-addition keys; validate all declared field types.
Normalize omitted settings fields to the defaults above. Values inside `variables`
may be JSON scalars, arrays, or objects; they are data, never template expressions
to evaluate or shell text to interpolate. Do not place credentials in them.

Publish the normalized settings as `build-settings.json`, and pass that reference
to subsequent hooks as an optional `settings` input of type `artifact`. This uses
the existing artifact transport rather than introducing an untyped recipe object
input. Include it in agent context as repository configuration. The parent can use
the configure step's structured outputs directly for routing and prompt assembly.

Append the relevant prompt addition in a clearly labeled repository-guidance
section of each effective phase prompt. Keep the original request, built-in
instructions, current documents, and human feedback. Do not allow configuration
to replace the agent output schema, approvals, permission policy, or state graph.
`implementation` applies to both light and heavy agents; assessment additions apply
to the corresponding reviewers, including configured specialists. Rebuild prompts
from the normalized settings instead of cumulatively appending text on each turn.

Configuration is a snapshot for this build. Preserve it across phase changes,
revision, upstream chasing, session replacement, and light-to-heavy escalation.
Do not rerun configure inside those loops. A later edit to configure takes effect
in a new build; other hook definitions retain ordinary checkpoint-time resolution.
Child builds load their own cell's configuration rather than inheriting the
parent's prompt additions and specialist requirements automatically.

An absent configure hook supplies empty settings and the common skipped result.
A failed configure result stops the step through ordinary failure handling.
Because even an absent late hook pins the candidate, placing configure at startup
intentionally pins earlier than today's build. Retain the existing later rebase
to catch upstream changes; this is a documented consequence of the placement.

### Before design: research and alternative thinking

Run on entry to each heavy design round, including redesign, before the design
agent drafts the proposal. Supply the original request, current documents,
configuration artifact, and any feedback from the previous round. It may run
research, compare architectures, or compose an alternative proposal. It returns
the common envelope and artifacts; it must not edit the repository or replace
the workflow's canonical `design.md` or test statements.

Make its evidence available to the designer, test planner, and plan reviewers.
The design must explain which alternatives it adopted or rejected and why. A
successful research run is not an approval of the resulting design. A failed
hook stops its step normally; a skipped hook leaves design to proceed with the
available context. Requests to revise a completed design use the existing review
and redesign flow.

Run configured `before_design` consultations after this hook so they can use its
research. Ordinary clarification or a resumed turn in the same design round does
not rerun either checkpoint. A new design round receives the updated evidence.

Light builds have no design phase. A cell that needs this hook for every build
sets `require_design: true`; merely adding a design prompt addition or a
`before_design.yaml` file does not invent a design phase on the light path.
Declaring a design-stage consultation also requires heavy routing, as specified
below, so a configured consultation cannot silently disappear.

### Specialist consultations: reuse the existing expert mechanism

The heavy workflow already has two relevant extension points:

- The agent can request `kind: expert`, with a `role` and `request`, through
  [the coordinator](../recipes/develop/coordinate.yaml). Its expert route includes
  [the consultation kernel](../recipes/kernel/consultation.yaml) directly.
- The `assessment` state in [heavy development](../recipes/develop/develop.yaml)
  uses that same kernel for `plan-assessment` after design and test planning, and
  `outcome-assessment` after implementation. These are explicit gates before
  human review, not merely suggestions in an agent prompt.

Security, accessibility, performance, and architecture are expert roles, not new
consultation kinds. Existing agent-requested expert dialogue remains available.
The addition proposed here is deterministic scheduling from configuration, so a
required security review does not depend on the agent remembering to request it.
The light coordinator currently supports serving-cell consultations rather than
this expert request API; add a configured outcome-specialist checkpoint directly
using the common kernel, without changing light's serving-cell request contract.

Each `settings.consultations` item has these required fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `key` | nonempty string matching `^[a-zA-Z0-9_-]+$` | Unique specialist request identifier within the configuration. |
| `checkpoint` | enum | `before_design`, `plan_assessment`, or `outcome_assessment`. |
| `role` | nonempty string | Specialist assignment, such as security architect. |
| `request` | nonempty string | Concrete question or review scope. |
| `required` | boolean | Require an explicit passing assessment before leaving this checkpoint. |

Reject duplicate keys and unknown fields. These describe experts inspecting the
current cell, not prerequisite work in another cell. Keep serving-cell ownership
negotiation and child-build submission on their existing routes.

Any configured `before_design` or `plan_assessment` consultation requires heavy
routing. `outcome_assessment` applies to either path after prepare and before verify.
At heavy assessment checkpoints, retain the existing general assessment and then
run the configured specialists in declaration order. The general reviewer does
not substitute for a specialist, nor does a specialist replace the general reviewer.

For `required: true`, demand `outcome: agreed` **and** `assessment: pass`. Agreement
on adverse findings is not a pass. `revise` routes back to design for plan findings
and implementation for outcome findings; scope changes still require redesign.
Required `before_design` assessments can evaluate the research brief and constraints;
a revision starts a new design round with those findings. Unresolved consultations
use the kernel's normal direction/error handling rather than silently proceeding.

For `required: false`, preserve the consultation's findings and disposition as
advisory evidence, without turning them into a new pass gate. The designer or
implementer must account for the findings in their deliverable. Execution errors
still propagate normally. Use advisory `before_design` requests for exploratory
thinking and required `plan_assessment` requests for approval of concrete proposals.

Provide the current documents and requester session through the existing internal
kernel API. Preserve returned transcripts, findings, assessment, and session updates
using the same plumbing as existing expert consultations; native sessions remain
outside the public hook API. Associate each result with its checkpoint and document
or candidate revision. New evidence needs a new assessment; do not let the existing
coordinator's completed-thread shortcut reuse a stale result just because the
configured key is unchanged. Use distinct round-qualified internal thread keys.

Rerun outcome specialists after candidate revisions and upstream rebases. Required
specialist failure blocks the normal approval-reuse shortcut. Plan assessments
rerun when design or test statements change. Advisory and required results are
both visible in the corresponding human review artifacts.

### Prepare

Run once per candidate-validation round, after any rebase and before assessment
or verification. Do not run it after every agent turn.

Prepare may change the managed repository. Changes must remain within the
approved scope and appear in the subsequent full-repository inventory and review,
including changes outside `target_directory`. The parent recomputes the inventory;
a hook-provided claim that nothing changed is not sufficient.

Examples include formatting, updating generated source, or refreshing checked-in
API specifications. Preparation should converge: repeating it on an already
prepared candidate should make no further changes.

This is not an environment setup hook. Separate ops do not share a shell or an
installation directory. Declare tools with `execution_needs`, use artifacts for
handoffs, or perform installation and use within the same op.

### Verify

Run against the prepared candidate before outcome review. It is read-only with
respect to the managed Git candidate; logs and reports belong in the outbox.
Formatting fixes belong in prepare. A verification hook that changes the candidate
violates the contract and must not produce accepted verification evidence.

The hook owns the choice of checks. Prefer existing `gha` / `gha-many` workflows
where suitable, or ordinary test commands. Checks must exercise the current
candidate, not merely observe a successful CI run for the target branch. Wait for
checks to finish before returning.

Apply this checkpoint before successful local completion in both build paths,
including `unchanged` and `delegated` outcomes. This closes the current light-path
shortcut that can finish delegated work without local verification. Preserve the
existing human-review rules for those outcomes. If prepare creates local changes,
the outcome must follow the normal local-change review and merge path.

### Publish

Run after the native merge operation succeeds, before the build recipe completes.
Do not run for cancelled, unchanged, or delegated outcomes, or after an unsuccessful
merge attempt. Child builds that merge run their own publish hooks.

Supply the merge operation's exact `merged_hash` and `target_branch`. The hook
definition and consuming workspace must refer to that merged commit, not a later
branch tip. Use c2j's existing workspace selection and pinning, and test this
explicitly with an advancing target branch.

Publish may perform external side effects, such as uploading a package or
deploying documentation. It must not modify the already merged Git candidate.
Version bumps and generated release files that need review belong in prepare.
The consuming cell decides what publishing means and which operations implement it.

Use ordinary c2j execution, error propagation, and retry semantics. Do not add a
recipe-specific publication recovery state machine, merge rollback, or durable
publication ledger. Hook authors should use the merged commit as an idempotency
key where their publishing service supports one; this is not an exactly-once
execution guarantee.

## Hook API v1

Hook paths are fixed at the repository root. `target_directory` is an input to the
hook, not a second discovery location. Monorepos can dispatch to component-specific
recipes using relative includes. No arbitrary hook-path override is proposed.

### Common inputs

Every hook declares the following public inputs. Scalar fields avoid exposing
internal workflow objects or native agent sessions.

| Input | Recipe input type | Meaning |
| --- | --- | --- |
| `api_version` | `string` | Literal `c2.build-hook/v1`. |
| `request` | `string` | Original build request, for context. |
| `target_directory` | `string` | Validated repository-relative task directory; defaults to `.` at the build entrypoint. |
| `candidate` | `string` | Exact commit at hook entry, bound after the late include pins its workspace. |
| `base` | `string` | Build's integration base for understanding the local changes; not necessarily `candidate`'s parent. |
| `documents` | `artifact_map` | Available specifications and evidence, keyed by stable document names. Empty when none exist. |

All hooks after configure additionally accept `settings`, an optional `artifact`
containing normalized `build-settings.json`. Configure itself does not receive
this input. With no configure hook, the parent still supplies the default settings
artifact so subsequent hooks have the same contract.

For prepare and verify, bind `candidate` from `context.git.hash` at the late include
callsite, not from a previously captured flow field. Bind `base` from the execution
base. For publish, use the captured integration base and require that the pinned
candidate equals `merged_hash`.

Publish additionally receives:

| Input | Recipe input type | Meaning |
| --- | --- | --- |
| `merged_hash` | `string` | Exact commit returned by the successful merge. |
| `target_branch` | `string` | Destination branch returned by the successful merge. |

Artifacts can include approved design, test statements, implementation summaries,
and verification reports. The shared wrapper documents the keys it supplies;
hooks must tolerate documents that do not exist in the light workflow. Do not pass
the entire internal `flow`, credentials, or Codex session objects.

An inventory artifact generated before a late include is historical context: the
hook's `candidate` is authoritative. A hook needing an exact diff can inspect its
pinned workspace using `base` and `candidate`. This avoids assuming that an earlier
inventory and a newly pinned hook necessarily describe the same commit.

### Common outputs

Use a small common result envelope for all hooks. Configure additionally returns
the `settings` object described above:

| Output | Type | Meaning |
| --- | --- | --- |
| `api_version` | `string` | Literal `c2.build-hook/v1`. |
| `status` | enum | `passed`, `failed`, or `skipped`. |
| `summary` | nonempty string | Human-readable result, including why work failed or was skipped. |
| `artifact_refs` | object | Map of report/log names to structured c2 artifact references. May be empty. |

`passed` means all applicable work promised by the hook completed successfully.
`failed` means completed work found a semantic problem, such as failing tests or
an inability to prepare the requested files. `skipped` means no applicable work
was performed; it must never be described as a successful test run or publication.
Multi-check hooks aggregate their results: any failing required check prevents
`passed`. Check-level details belong in an attached report rather than a second,
potentially conflicting top-level result API.

For prepare and verify, a `failed` result returns the evidence to implementation
through the existing revision route. A failed publish result fails its enclosing
step using normal recipe failure handling; it does not route back to coding.
Hook execution errors, invalid definitions, denied capabilities, invalid output
contracts, and timeouts propagate as errors. Do not turn them into skipped checks.

An absent hook returns this fallback, with the appropriate hook name:

```yaml
outputs:
  api_version: c2.build-hook/v1
  status: skipped
  summary: No repository verify hook is configured.
  artifact_refs: {}
```

Only ordinary-file absence invokes the fallback. Invalid YAML, a symlink, a failed
lookup, or a malformed result must fail as specified by c2j.

Hook summaries are limited to 8,192 characters and artifact maps to 64 entries.
Normalized settings are limited to 16,000 characters of serialized JSON; exceeding
the limit fails before process launch. Use artifacts for substantial research.
Consultation configuration allows up to 40 specialist requests.

Each callsite supplies a self-contained `expect_outputs` schema. The following is
the common schema; configure adds `settings` to its properties and required list:

```yaml
expect_outputs:
  type: object
  additionalProperties: false
  required: [api_version, status, summary, artifact_refs]
  properties:
    api_version:
      type: string
      enum: [c2.build-hook/v1]
    status:
      type: string
      enum: [passed, failed, skipped]
    summary:
      type: string
      minLength: 1
    artifact_refs:
      type: object
      additionalProperties:
        type: object
```

The wrapper must resolve exported artifact references before presenting them as
evidence. Namespace hook artifacts under `hooks/<hook>/<validation-round>/` when
adding them to the parent document map; do not allow a hook to overwrite approved
specifications or the parent's canonical review documents.

The shared wrappers create configuration and design-context summaries, plus
`preparation.md`, `verification.md`, and `publication.md` as applicable. Each records
the hook path, input candidate, normalized result,
summary, and evidence links. Preparation also records the resulting candidate.
Keep c2j's recorded hook source and policy details in the job story rather than
building a parallel provenance system.

Add one build input, `require_verification`, a boolean defaulting to `false`.
When false, skipped verification remains visible and permits normal review, as
today. When true, only `passed` permits successful completion; absence or an
explicit skip blocks it with an actionable diagnostic. Propagate this input to
both build paths and across light-to-heavy escalation.

This option requires verification for the current build; it does not automatically
configure checks in child cells or establish an independent security policy.

## Example verify hook

This example explicitly opts into an existing script. A cell could instead invoke
its test runner or include its existing CI recipe. All common API inputs are
declared even when this implementation only needs the target directory.

```yaml
id: repository-build-verify
input_schema:
  api_version: {type: string, required: true}
  request: {type: string, required: true}
  target_directory: {type: string, required: true}
  candidate: {type: string, required: true}
  base: {type: string, required: true}
  documents: {type: artifact_map, default_value: {}}
  settings: {type: artifact, required: false}
inputs:
  target_directory: '${{ inputs.target_directory }}'
sequence:
  - id: run_repository_suite
    op: command_execution
    const: true
    inputs:
      env:
        TARGET: '{{ context.environment.op.worktree_path }}/{{ inputs.target_directory }}'
        OUTBOX: '{{ context.environment.op.outbox }}'
      run: |
        cd "$TARGET" || exit 1
        if bash ./build.sh > "$OUTBOX/tests.log" 2>&1; then
          printf passed
        else
          printf failed
        fi
outputs:
  api_version: c2.build-hook/v1
  status: '${{ sequence.run_repository_suite.outputs.stdout }}'
  summary: '${{ sequence.run_repository_suite.outputs.stdout == "passed" ? "Repository suite passed." : "Repository suite failed; inspect tests.log." }}'
  artifact_refs: '${{ sequence.run_repository_suite.artifacts }}'
```

This is a contract illustration, not a universal test runner. Production hooks
must declare their execution dependencies and distinguish ordinary test failures
from execution errors and timeouts. A missing explicitly requested script fails;
the example does not rediscover or silently skip it.

## Revalidation and native execution semantics

After upstream advancement, repeat prepare and verify against the new candidate,
even when the local change digest is unchanged. Recompute the digest after prepare
before deciding whether the existing approval can be reused. Preparation changes
must go through the usual assessment and review gates.

Changes to hook definitions and their local includes must be visible in review.
Approval reuse also requires unchanged relevant hook definitions; a change to
upstream hook code must not silently reuse approval merely because the local diff
digest stayed the same. Keep this check within the existing approval-reuse decision.
The implementation hashes hook definitions and their transitive local includes,
including includes outside the hook directory. External recipe references, selector
ops, and extension packages conservatively require renewed review on each new
candidate because their complete source identity is not available to this recipe.

Verification remains bound to the prepared and reviewed tree. The existing squash
step may change commit identity while preserving that tree. Publish receives the
actual resulting merged commit, not the pre-squash verification hash.

c2j records hook resolution or absence for an invocation. Its normal retries use
that captured definition; a later checkpoint visit resolves again from the new
candidate. Do not add recipe-level source caching or custom retry machinery.

Hooks run in the consuming repository. Ordinary ops and relative includes support
unpushed candidates. Local selector ops and local CEL packages currently need a
fetchable source commit; do not make those mechanisms a prerequisite for pre-merge
hooks.

## Permissions

Use c2j's existing permission administration keyed by the exact hook paths above.
The recipe does not configure permissions or inherit the caller's authority as a
substitute for hook grants. Test credentials generally belong to verify; registry
or deployment credentials generally belong to publish. Grant only what each hook
needs, with the source-trust policy chosen by the consuming cell's administrator.

No grants means no hook JobDB capabilities. Relative includes in the same repository
inherit hook authority; cross-repository includes require explicit delegation.
Publishing credentials do not become available to other hooks merely because
they are all called by build. Avoid embedding credentials in inputs or reports.

## Single-step replacement

Implement this as one coordinated change, without a compatibility or deprecation
phase:

1. Add configure and before-design wrappers, prompt-addition plumbing, and configured
   specialist checkpoints. Add shared prepare and publish wrappers; replace the implementation of
   `recipes/develop/verify.yaml` with the local verify hook wrapper.
2. Wire the same contracts into light and heavy state machines, including no-change
   completion, upstream-advance revalidation, and publication after successful merge.
3. Remove automatic `build.sh` discovery, the verification helper's `command` input,
   and the light agent's `verification_command` output and execution path. Agents
   still run appropriate checks while implementing; hooks define repeatable gates.
4. Update agent prompts, synopsis, merge review, README, and tests to describe hook
   results rather than assuming `build.sh` or `build.log` exists.
5. Provide examples for configuration, design research, security consultations,
   a shell test suite, an existing GitHub Actions workflow, preparation, and publication.
   Cells relying on the old convention add
   a verify hook explicitly. Do not delete their scripts or auto-generate hooks in
   other repositories.

With no verify hook, checks are explicitly skipped unless `require_verification`
is true. This is an intentional behavior change for cells that currently rely on
automatic discovery. Release notes must make the required opt-in clear.

Do not add generic before/after-every-state hooks or separate security-specific
recipe paths. Configure supplies values, before-design supplies research, and
existing expert consultations provide specialist dialogue and assessment.

## Acceptance statements for implementation

These statements define the implementation acceptance criteria.
Publish them as test-statement artifacts when implementing. Each statement below
is under 30 words; filenames and test metadata are annotations.

| Expectation | Importance | Kind / dependencies | Files |
| --- | --- | --- | --- |
| Light and heavy builds share applicable hook contracts; design hooks run only on the heavy path. | Critical | Integration / embedded c2j | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` |
| Configuration runs before classification and persists across revision, upstream chasing, and escalation. | High | Integration / embedded c2j | `build.yaml`, `recipe-tests/build-kernel.test.yaml` |
| Prompt additions reach their intended phases without replacing workflow instructions or accumulating duplicate text. | High | Integration / embedded c2j | `recipes/develop/agent.yaml`, `recipes/light/agent.yaml` |
| Named values reach later hooks through the settings artifact without being evaluated as templates. | High | Integration / embedded c2j | `recipe-tests/build-kernel.test.yaml` |
| Research evidence reaches design and plan review; redesign refreshes that evidence. | High | Integration / embedded c2j | `recipes/develop/develop.yaml`, `recipe-tests/build-kernel.test.yaml` |
| Required design work selects heavy; configured outcome specialists also run on light builds. | Critical | Integration / embedded c2j | `build.yaml`, `recipe-tests/build-light.test.yaml` |
| Required security consultation needs an explicit passing assessment; agreement on adverse findings cannot satisfy the gate. | Critical | Integration / embedded c2j | `recipe-tests/build-kernel.test.yaml` |
| Updated proposals and candidates cannot reuse stale specialist assessments. | Critical | Integration / embedded c2j | `recipe-tests/build-kernel.test.yaml`, `recipe-tests/merge-chase.test.yaml` |
| Missing hooks produce explicit skipped evidence without invoking an existing build script. | Critical | Integration / embedded c2j | `recipes/develop/verify.yaml`, `recipe-tests/verification.test.yaml` |
| Required verification blocks successful completion when the hook is absent or skips. | Critical | Integration / embedded c2j | `build.yaml`, `recipe-tests/verification.test.yaml` |
| Failing tests return evidence to implementation and prevent merge. | Critical | Integration / embedded c2j | `recipes/develop/verify.yaml`, `recipe-tests/verification.test.yaml` |
| Invalid hooks, denied capabilities, timeouts, and malformed outputs never become skipped or successful verification. | Critical | Integration / embedded c2j | `recipe-tests/verification.test.yaml` |
| Preparation changes appear in the candidate inventory and receive the normal assessment and outcome review. | Critical | Integration / embedded c2j | `recipes/kernel/git-candidate.yaml`, `recipe-tests/build-kernel.test.yaml` |
| Verification cannot approve a candidate it modified. | Critical | Integration / embedded c2j | `recipes/develop/verify.yaml`, `recipe-tests/verification.test.yaml` |
| Unchanged and delegated outcomes run configured verification before successful completion. | High | Integration / embedded c2j | `recipe-tests/build-light.test.yaml`, `recipe-tests/completion-review.test.yaml` |
| Upstream advancement repeats preparation and verification; changed preparation or hook definitions invalidate approval reuse. | Critical | Integration / embedded c2j, Git fixture | `recipe-tests/merge-chase.test.yaml` |
| Publish runs after successful merge using that exact commit, even if the target branch advances. | Critical | Integration / embedded c2j, Git fixture | `recipe-tests/build-merge.test.yaml` |
| Unchanged, delegated, cancelled, and failed-merge outcomes do not invoke publish. | Critical | Integration / embedded c2j | `recipe-tests/build-merge.test.yaml` |
| Publish failures propagate through ordinary execution handling without a recipe-specific recovery workflow. | High | Integration / embedded c2j | `recipe-tests/build-merge.test.yaml` |
| Hook evidence cannot overwrite approved specifications or canonical review reports. | High | Integration / embedded c2j | `recipe-tests/verification.test.yaml` |
| A local hook can include an unpushed relative recipe and run against its pinned candidate. | High | Integration / embedded c2j, Git fixture | `recipe-tests/verification.test.yaml` |

Use fixture hooks and mock publishing operations for recipe tests. Do not publish
real packages or deployments to validate orchestration. Confirm native hook behavior
with `c2j submit --recipe-file ... --run --embed`; static validation alone does not
resolve repository-local hooks.

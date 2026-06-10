# Superpowers Recipe Validation Test Plan

## Purpose

Validate that current c2j core and c2ops features are sufficient to implement
the C2-adapted Superpowers workflow before building the full recipe set.

This plan should answer two questions:

- Do the available primitives cover the workflow without adding a task-loop,
  request/result, or git-handoff subsystem?
- What recipe patterns should the actual implementation use?

## Latest Validation Result

Status after the 2026-06-09 UTC focused rerun: **sufficient to proceed with the
implementation plan, with live skill-quality validation included in the default
suite**.

Reverification on 2026-06-09 UTC against `/usr/local/bin/c2j`
(`c2j version v0.0.28-0.20260609031142-3374b852aa99`, SHA-256
`7e6c92ca316fb0e332d786facd2fb35070e9a589b88253977417efc83117427a`):

- `recipe-tests/verify-child-artifact-forwarding-live.sh` passed. The smoke
  validates child result artifact forwarding, not access to intermediate
  child-node artifacts. The non-blocking `persist task outcome chapter ...
  lease is required` story persistence errors no longer reproduce.
- The same child result artifact run no longer logs recoverable
  `replay cache miss: task_result_missing` errors in the cached/resume path.
- The child result artifact logs did not contain `ERROR`, duplicate artifact
  errors, or chapter ordinal conflict signatures.
- `recipe-tests/verify-codex-skill-execution-live.sh` passed, and its log did
  not contain the thin-pack restore or chapter ordinal conflict signatures.
- `recipe-tests/verify-superpowers-rule-gate-live.sh` passed. TS-047 validates
  JSON parse, JSON Schema, assertion policy failure, and `child_status` routing.
  TS-048 confirms invalid `rule_gate` input is rejected by selector validation.
- `recipe-tests/verify-superpowers-child-orchestration-live.sh` passed. TS-049
  validates failed-child status through `recipe.await_result_soft` and
  `rule_gate child_status`. TS-050 validates `child_group` required/optional
  reviewer aggregation.
- Focused mocked Superpowers recipe-shape suites passed. TS-051 validates native
  task selection, TS-052 validates required child-boundary detection without
  spawning child jobs, TS-053 validates same-job role sessions, TS-054 validates
  `sessionId` isolation/resume, and TS-055 validates adaptive plan iteration.
- Focused `codex/run_skill` recipe suites passed. TS-056 validates parsed output
  artifact and status-contract fields; TS-057 validates repair metadata is
  visible to recipes. c2ops `RunSkill` unit tests also passed at c2ops commit
  `8b37f01`.
- Focused static C2 Superpowers skill-bundle suite passed. TS-058 validates the
  ten local role skills and OpenAI metadata under
  `skills-bundle/.agents/skills/c2-superpowers-*`.
- Focused route recipe suite passed. TS-059 validates feature work routes to
  brainstorming before implementation; TS-060 validates user-input routes include
  a concrete question.
- Focused deterministic route cases passed. TS-065 validates submitted plans
  route to execution without skill invocation in the run path; TS-066 validates
  submitted designs route to planning without skill invocation in the run path.
- Focused brainstorm recipe suite passed. TS-061 validates plan-ready design
  output; TS-062 validates the phase stops before planning when open design
  questions remain.
- Focused write-plan recipe suite passed. TS-063 validates a ready dependent
  task chain; TS-064 validates required child-job boundaries are surfaced
  without creating child jobs.
- Focused execute-plan suite passed. TS-067 validates one same-job
  implementation/spec-review/quality-review task boundary; TS-068 validates the
  recipe stops before implementation when the selected task requires a child
  job, with an explicit node non-execution assertion for the implementer; TS-082
  validates recipe-enforced RED/GREEN/refactor TDD before task review.
- Focused verify suite passed. TS-069 validates fresh command evidence before
  success; TS-070 validates failed command evidence remains blocking workflow
  data instead of being hidden by a verifier summary.
- Focused finish suite passed. TS-071 validates merge-ready recommendation from
  verified evidence; TS-072 validates merge blocking when verification has
  issues; TS-073 validates explicit merge after the finish gate.

Validated:

- c2ops `rule_gate` Go tests passed.
- c2ops `codex` Go tests passed.
- static manifest checks passed for `codex/run_skill` and `rule_gate`.
- recipe scenario suites TS-001..TS-023 and TS-028..TS-041 passed.
- CLI framework checks TS-024..TS-027 passed.
- child result artifact forwarding TS-046 passed after updating the smoke to use
  the current `c2j run one` command instead of stale `c2j exec`.
- focused live Codex mutation/git-state smoke TS-044/TS-045 passed after the
  thin-pack restore fix.
- focused `rule_gate` smoke TS-047/TS-048 passed.
- focused child orchestration smoke TS-049/TS-050 passed.
- focused Superpowers recipe-shape smokes TS-051..TS-055 passed.
- focused `codex/run_skill` smokes TS-056/TS-057 passed.
- focused C2 Superpowers skill-bundle smoke TS-058 passed.
- focused Superpowers route recipe smokes TS-059/TS-060 passed.
- focused Superpowers brainstorm recipe smokes TS-061/TS-062 passed.
- focused Superpowers write-plan recipe smokes TS-063/TS-064 passed.
- focused deterministic route smokes TS-065/TS-066 passed.
- focused execute-plan smokes TS-067/TS-068/TS-082 passed compile/validate/run.
- focused verify smokes TS-069/TS-070 passed compile/validate/run.
- focused finish smokes TS-071/TS-073 passed compile/validate/run.
- focused debug smokes TS-074/TS-077 passed compile/validate/run.
- focused plan-review smokes TS-078/TS-079 passed compile/validate/run.
- focused primary-orchestrator smokes TS-080/TS-081 passed compile/validate/run.
- `recipe-tests/run-all.sh` passed end to end on 2026-06-10 with TS-058..TS-082
  included in the default compile/validate/run path and with TS-042/TS-043
  focused live skill-quality validation invoked as a required hard-failing
  check.
- focused live skill-quality smoke TS-042/TS-043 passed after narrowing
  `skill-quality-smoke.yaml` to triage and requirements contracts. The script
  compiles the scenario first, runs c2j with explicit lease/wait timeouts, and
  hard-fails on missing resources, timeout, story conflict, thin-pack restore,
  replay-cache, or c2j `ERROR` log signatures.
- the TS-044/TS-045 log did not contain the prior `Repository lacks these
  prerequisite commits` thin-pack signature.
- the TS-044/TS-045 log did not contain the separate `workflow state conflict`
  or chapter ordinal conflict signatures.

Previously blocked, now resolved by the focused rerun:

- `recipe-tests/verify-codex-skill-execution-live.sh` previously failed after a
  live Codex mutation because the following command op could not restore git
  state from the persisted thin pack.

Additional finding:

- The original broad `recipe-tests/verify-skill-quality-live.sh` failed after
  30 minutes while progressing through many live Codex steps. This was a
  live-smoke sizing issue, not evidence that one Codex op should take 30
  minutes. The current required smoke is focused and passed; broader
  skill-quality coverage should be split into smaller required phase smokes,
  not hidden behind an environment gate.
- The original broad skill-quality run also logged duplicate story chapter
  ordinal conflicts before timing out. That is tracked as a c2j reliability bug,
  separate from git-state propagation and separate from the now-fixed embedded
  child resume story/cache signatures.
- `recipe-tests/verify-child-artifact-forwarding-live.sh` previously logged
  recoverable `persist task outcome chapter ... lease is required` errors in a
  passing run. That signature is fixed and tracked historically in
  `guides/BUG_REPORT_C2J_STORY_CHAPTER_PERSIST_REQUIRES_LEASE_ON_CACHED_CHILD_RESUME.md`.
- `recipe-tests/verify-child-artifact-forwarding-live.sh` later logged
  recoverable `replay cache miss: task_result_missing` errors in a passing run.
  That signature is fixed and tracked historically in
  `guides/BUG_REPORT_C2J_REPLAY_CACHE_MISS_ON_EMBEDDED_CHILD_RESUME.md`.
- Encapsulation clarification: `recipe.await_result_soft` is expected to expose
  child job result data, not intermediate child-node artifacts. Parent-visible
  diagnostics should be exported as child job result outputs/artifacts by a
  completed child recipe.

Follow-up specs:

- `guides/new-ticket-simplification/REQUIREMENTS_C2J_GIT_STATE_RESTORE_AFTER_MUTATING_EXTENSION.md`
- `guides/BUG_REPORT_C2J_THIN_PACK_RESTORE_MISSING_PREREQUISITE_COMMITS.md`
- `guides/new-ticket-simplification/REQUIREMENTS_LIVE_CODEX_TIMEOUT_POLICY.md`
- `guides/BUG_REPORT_C2J_STORY_CHAPTER_DUPLICATE_ORDINAL_DURING_LIVE_REPLAY.md`
- `guides/BUG_REPORT_C2J_STORY_CHAPTER_PERSIST_REQUIRES_LEASE_ON_CACHED_CHILD_RESUME.md`
- `guides/BUG_REPORT_C2J_REPLAY_CACHE_MISS_ON_EMBEDDED_CHILD_RESUME.md`

## Reviewed Sources

Local c2ops checkout:

- path: `/tmp/c2ops-latest`
- commit: `63ba6ba Add rule_gate README`

Relevant selectors:

- `git+https://github.com/colony-2/c2ops.git//codex/run_skill@main`
- `git+https://github.com/colony-2/c2ops.git//rule_gate@main`
- `git+https://github.com/colony-2/c2ops.git//codex@main`

Relevant c2j/core docs:

- `guides/ops/RUN_RECIPE.md`
- `guides/CHILD_GROUP_USER_GUIDE.md`
- `guides/new-ticket-simplification/REQUIREMENTS_TASK_JOB_LOOP.md`
- `guides/new-ticket-simplification/REQUIREMENTS_TASK_PLAN_OPS.md`

## Confirmed Capability Surface

### c2ops `codex/run_skill`

The `codex/run_skill` selector has manifest name `skill.run`.

Required input:

- `skill`

Important supported inputs:

- `skills`
- `input`
- `prompt`
- `sessionId`
- `model`
- `return_on`
- `status_contract.path`
- `output.from`
- `output.path`
- `output.format`
- `output.schema`
- `output.required_when_incomplete`
- `output.validation.on_error`
- `output.validation.repair.enabled`
- `output.validation.repair.max_attempts`
- standard op paths for worktree, workdir, inbox, and outbox

Important outputs:

- normal Codex fields: `status`, `sessionId`, `assistantSummary`,
  `incompleteReason`, `incompleteCategory`, `pendingDependencies`,
  `skills_installed`, `outcome`
- skill wrapper fields: `skill`, `raw_summary`, `output_source`, `output_path`,
  `raw_output`, `parsed_output`, `output_schema_valid`,
  `output_schema_errors`, `output_repair_attempts`,
  `status_contract_present`, `status_contract_valid`,
  `status_contract_json`, `status_contract_errors`, `diagnostics`

Implementation implication:

- New C2-adapted skills should prefer artifact output validation through
  `output.from: artifact`, not JSON in `assistantSummary`.

### c2ops `rule_gate`

Selector:

- `git+https://github.com/colony-2/c2ops.git//rule_gate@main`

Rule types:

- `assert`
- `artifact_exists`
- `file_exists`
- `json_parse`
- `json_schema`
- `child_status`

Outputs:

- `version`
- `ok`
- `failed_rule_ids`
- `summary`
- `results`

Implementation implication:

- Recipes should route from `ok`, `failed_rule_ids`, and `results`.
- The current op does not expose `next_action`, severity, warnings, or waivers.
  If those are needed, express them in recipe state transitions or a separate
  planner step.

### c2j Child Orchestration

Covered primitives:

- `recipe.await_result_soft` for failed child jobs as workflow data.
- `child_group` for independent reviewer/adversarial fanout.
- ordinary state machines plus same-job Codex sessions for dependent task
  sequencing.
- child job invocation with normal recipe inputs, artifacts, outputs, and target
  refs when a C2 job boundary is required.

Implementation implication:

- Do not introduce a task-loop primitive.
- Do not introduce required `task_request.json`, `task_result.json`,
  `base_after`, thinpack, or parent-owned commit handoff.
- Sequential implementation tasks should run as same-job task sessions by
  default. If a task requires a child job because it needs independent
  target-ref advancement, it should target `main` by default or an explicitly
  selected experiment ref.

## Test Strategy

Use three levels of validation.

### Level 1: Static Contract Tests

Goal: catch selector and schema drift before any live agent work.

Tests:

- Verify c2ops selectors resolve:
  - `//codex/run_skill@main`
  - `//rule_gate@main`
- Verify manifests expose the expected input and output keys.
- Verify `rule_gate` supports `json_schema` and `child_status`.
- Verify `codex/run_skill` supports artifact-first output validation.
- Verify c2j recognizes `recipe.await_result_soft`.
- Verify c2j recognizes `child_group` with `children` and `children_from`.

Acceptance:

- All selector manifests load.
- Missing or renamed fields are caught before recipe implementation starts.

### Level 2: Mocked Recipe Tests

Goal: validate routing and state-machine shape without live Codex calls.

Tests:

- Parent selects one head task from plan state using native recipe
  state/CEL/templates.
- Parent runs exactly one task boundary at a time.
- The task boundary uses independent Codex sessions for implementer/reviewer
  roles inside the same job by default.
- Parent routes task status/output artifacts to plan update and next-task
  selection.
- When a child-job boundary is required, the parent uses
  `recipe.await_result_soft` and routes failed child status to the planner path.
- Parent does not require explicit commit/thinpack/base handoff.
- `child_group` reviewer fanout aggregates required and optional reviewer
  results.
- `rule_gate` gates planner output with `json_schema`.

Acceptance:

- The dependent task loop is expressible as a normal state machine.
- No mocked test needs a task-loop primitive or required request/result
  artifacts.

### Level 3: Live Embedded Smokes

Goal: prove the real c2ops and c2j runtime behavior that mocked tests cannot
prove.

Default live validation should stay focused on runtime primitives, not on
running the whole Superpowers cycle. The default suite should include:

- child result artifact forwarding through real embedded child jobs;
- live Codex mutation followed by deterministic command probes;
- git-state propagation across post-Codex ops;
- log scans for the thin-pack restore signature and story/chapter conflict
  signatures.

Broad multi-skill quality validation remains useful, but it is an extended
integration test because it runs many live Codex calls and can obscure the
specific primitive that failed.

For short jobs, run with:

```bash
c2j submit --recipe-file <recipe> --run --embed
```

For live jobs that may run longer than the default lease, submit first and run
with an explicit lease:

```bash
JOB_JSON="$(c2j submit --recipe-file <recipe> --embed --json)"
TENANT_ID="$(printf '%s' "$JOB_JSON" | jq -r .tenant_id)"
JOB_ID="$(printf '%s' "$JOB_JSON" | jq -r .job_id)"
c2j run one --embed --tenant-id "$TENANT_ID" --job-id "$JOB_ID" --lease-duration 45m --wait-timeout 45m
```

Focused smokes:

1. `superpowers-run-skill-output-smoke.yaml`
   - Status: implemented as TS-056.
   - Use `codex/run_skill`.
   - Require an output artifact with JSON Schema.
   - Assert `parsed_output`, `output_schema_valid`, and status-contract fields.

2. `superpowers-run-skill-repair-smoke.yaml`
   - Status: implemented as TS-057.
   - Configure `output.validation.repair.enabled: true`.
   - Confirm repair-attempt metadata is visible to recipes after the declared
     artifact validates.

3. `superpowers-rule-gate-schema-smoke.yaml`
   - Status: implemented as TS-047, with invalid-input rejection in TS-048.
   - Validate an artifact with `json_parse`.
   - Validate the same artifact with `json_schema`.
   - Confirm policy failure returns `ok=false` with zero process failure.
   - Confirm invalid rule input fails the node.

4. `recipe-tests/verify-superpowers-child-orchestration-live.sh`
   - Status: implemented as TS-049 for failed-child status and policy routing.
   - Start a child recipe that fails.
   - Await it with `recipe.await_result_soft`.
   - Confirm parent receives child status and failure metadata without failing
     the parent node.

5. `recipe-tests/verify-superpowers-child-orchestration-live.sh`
   - Status: implemented as TS-050.
   - Run required and optional reviewer children.
   - Confirm failed required child yields `ok=false`.
   - Confirm failed advisory child becomes warning data.
   - Confirm `review_pack` aggregate artifact is produced and group summary is
     consumable by `rule_gate`.

6. `superpowers-native-task-selection-smoke.yaml`
   - Status: implemented as TS-051/TS-052.
   - Select the first ready head task from plan state using native recipe
     templates.
   - Surface required child-job boundaries without starting child jobs.

7. `superpowers-task-session-smoke.yaml`
   - Status: implemented as TS-053.
   - Run implementer, spec reviewer, and quality reviewer as distinct same-job
     Codex sessions.
   - Confirm the task boundary does not use a child job.

8. `superpowers-session-contract-smoke.yaml`
   - Status: implemented as TS-054.
   - Confirm omitted `sessionId` starts isolated context.
   - Confirm explicit `sessionId` resumes the previous session.

9. `superpowers-adaptive-task-loop-smoke.yaml`
   - Status: implemented as TS-055.
   - Run task A, route task feedback to a planner session, update plan state,
     and select task B in the same job.

10. `superpowers-sequential-target-ref-smoke.yaml`
   - Add this only when implementation introduces a concrete task flow that
     requires a child job boundary.
   - Parent starts required child job A targeting `main` or a temporary
     experiment ref.
   - Child job A makes a small deterministic code/worktree change and completes its
     merge/advance path.
   - Parent starts required child job B targeting the same ref.
   - Child job B observes A's change without explicit parent commit/thinpack
     handoff.
   - This smoke depends on the fixed git-state restore behavior validated by
     TS-044/TS-045.

Required live smokes:

11. `skill-quality-smoke.yaml`
   - Status: implemented as TS-042/TS-043.
   - Exercises focused upstream/C2-adapted triage, requirements-author, and
     bad-requirements contrarian-review contracts.
   - Runs four live Codex calls plus deterministic assertions, so timeout
     policy is explicit and c2j error signatures are scanned.
   - Runs from `recipe-tests/run-all.sh` by default through
     `recipe-tests/verify-skill-quality-live.sh`; missing resources hard-fail
     the suite.
   - Broader implementation-planning and outcome-determination skill quality
     coverage should be added as separate required phase smokes rather than
     expanding this smoke into another long all-phase job.

12. `superpowers-mini-loop-e2e.yaml`
   - Planner emits a two-task plan.
   - Parent selects task A.
   - Same-job task boundary A runs through implementation/review/validation.
   - Parent routes task outputs to planner.
   - Planner updates plan state.
   - Parent selects task B.
   - Read-only reviewers fan out through `child_group`.
   - Final `rule_gate` validates the plan/output artifacts.

Acceptance:

- The full loop completes without `for_each`, task-loop primitive,
  `task_request.json`, `task_result.json`, `base_after`, or explicit parent git
  handoff.
- Any failure is inspectable through job story, child status, outputs, and
  artifacts.

## Decision Points

### Decide Whether `task_plan.select_next` Is Needed

`task_plan.select_next` does not exist today and should not be implemented
before validation. After the mocked parent-loop recipe is authored with native
recipe expressions, decide whether a helper would materially improve the
implementation.

Keep it unimplemented unless:

- task selection logic is repeated in multiple recipes;
- CEL/templates become hard to read;
- no-ready-task diagnostics are too noisy to express in recipe YAML.

Do not add the op if the first recipe can select the head task cleanly with
native templates.

### Use `run_skill` Versus Raw `codex`

Use `run_skill` when:

- a specific skill must be invoked;
- structured artifact output is required;
- status-contract validation matters;
- recipe readability benefits from avoiding repeated Codex path plumbing.

Use raw `codex` when:

- the work is open-ended agentic code editing;
- there is no top-level skill contract;
- the caller needs only the standard Codex output shape.

### Route From `rule_gate`

Use `rule_gate` for deterministic policy.

Do not expect it to decide the route name. Current c2ops output is:

- `ok`
- `failed_rule_ids`
- `results`

Recipe transitions should map failed rule IDs to route names.

## Implementation Inputs Produced By This Plan

When these tests pass, implementation should proceed with:

- C2-adapted Superpowers skill bundle.
- Static bundle validation through TS-058.
- Route/intake recipe validation through TS-059/TS-060.
- Brainstorm/design recipe validation through TS-061/TS-062.
- Write-plan recipe validation through TS-063/TS-064.
- Plan-review validation through TS-078/TS-079.
- Deterministic route-state validation through TS-065/TS-066.
- Execute-plan validation through TS-067/TS-068/TS-082.
- Verify validation through TS-069/TS-070.
- Finish validation through TS-071/TS-073.
- Debug validation through TS-074/TS-077.
- Task-plan JSON Schema.
- Parent execution recipe using a normal state machine.
- Same-job task boundary owning implementation, TDD, review, and validation.
- Child recipe only if the implementation adds a required job boundary such
  as target-ref advancement, cross-cell execution, reuse, true parallelism, or
  lifecycle isolation.
- Reviewer/adversarial fanout through `child_group`.
- Deterministic policy through `rule_gate`.
- Skill invocation through `codex/run_skill`.

## Remaining Unknowns To Resolve During Tests

- Exact live `run_skill` behavior for missing status contracts.
- Exact live `run_skill` behavior for `output.validation.on_error:
  incomplete|fail|warn`.
- Whether output repair is stable enough for production use or should remain
  advisory.
- Whether a dedicated job-story/node-output introspection op is needed for
  debugging failed child jobs. This is not normal recipe dataflow.
- Whether target-ref advancement needs additional recipe policy for experiment
  refs.
- Whether c2ops `codex/run_skill` live artifact validation passes in a focused
  artifact-first skill smoke.

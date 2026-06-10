# Superpowers Recipe Product Gaps

Companion to `guides/SUPERPOWERS_RECIPE_MAPPING.md`.

This review reflects the current product direction:

- c2ops has `run_skill`.
- c2ops has `rule_gate`, including JSON Schema validation.
- c2j core has `child_group`.
- c2j core has `recipe.await_result_soft`.

## Coverage Review

The major Superpowers-to-recipes platform primitives are present. A previously
blocking git-state restore bug after mutating Codex ops has been validated fixed
with a focused live smoke.

| Need | Current coverage | Status |
| --- | --- | --- |
| Skill-first prompting and enforced skill execution | c2ops `codex/run_skill` | Covered. Latest c2ops exposes `git+https://github.com/colony-2/c2ops.git//codex/run_skill@main`; its manifest name is `skill.run`. |
| Deterministic gates and schema checks | c2ops `rule_gate` with `json_schema` | Covered. Latest c2ops exposes `git+https://github.com/colony-2/c2ops.git//rule_gate@main`. This removes the need for a separate plan-update validation op. |
| Failed child jobs as workflow data | `recipe.await_result_soft` | Covered for failed-child status and failure routing by TS-049. Child internals remain encapsulated; parent-visible artifacts must be exported as child job result artifacts. |
| Parallel reviewer/adversarial fanout | `child_group` | Covered. TS-050 validates required/optional reviewer aggregation. |
| Dependent implementation tasks | ordinary recipe state machine plus same-job Codex sessions | Covered. TS-051..TS-055 validate native task selection, same-job role sessions, session isolation/resume, and adaptive task-plan iteration. No `for_each`, task-loop primitive, or child job is required for the normal Superpowers task chain. |
| Structured skill invocation | c2ops `codex/run_skill` | Covered. TS-056/TS-057 validate parsed output artifacts, status-contract fields, and repair metadata at the recipe boundary. c2ops `RunSkill` unit tests pass at commit `8b37f01`. |
| C2-adapted Superpowers role skills | local skill bundle plus static recipe smoke | Covered for initial implementation. TS-058 validates ten role skills and OpenAI metadata under `skills-bundle/.agents/skills/c2-superpowers-*`. |
| Route/intake recipe | `superpowers-route.yaml` state machine plus `codex/run_skill` fallback and `rule_gate` | Covered for initial implementation. TS-059/TS-060 validate heuristic prompt-only fallback; TS-065/TS-066 validate deterministic plan/design artifact routing without skill invocation in the run path. |
| Brainstorm/design recipe | `superpowers-brainstorm.yaml` plus `codex/run_skill` and `rule_gate` | Covered for initial implementation. TS-061/TS-062 validate plan-ready designs and stop-before-planning questions. |
| Write-plan recipe | `superpowers-write-plan.yaml` plus `codex/run_skill` and `rule_gate` | Covered for initial implementation. TS-063/TS-064 validate ready task plans and required child-job boundary surfacing. |
| Plan-review recipe | `superpowers-plan-review.yaml` plus `codex/run_skill` and `rule_gate` | Covered for initial implementation. TS-078/TS-079 pass focused compile/validate/run for aligned-plan approval and incomplete-plan replanning feedback. |
| Execute-plan recipe path | `superpowers-execute-plan.yaml` state machine plus role skills | Covered for initial implementation. TS-067/TS-068 pass focused compile/validate/run for same-job task execution and child-boundary stop behavior, including a node non-execution assertion for required child boundaries. |
| Verify recipe path | `superpowers-verify.yaml` command gates plus verify role skill | Covered for initial implementation. TS-069/TS-070 pass focused compile/validate/run for fresh command evidence and failed-command blocking data. |
| Finish recipe path | `superpowers-finish.yaml` finish gates plus optional `squashrebasemerge` | Covered for initial implementation. TS-071/TS-073 pass focused compile/validate/run for merge-ready recommendation, blocked merge evidence, and explicit merge after passing gates. |
| Debug recipe path | `superpowers-debug.yaml` reproduction state plus debug role skill and `rule_gate` | Covered for initial implementation. TS-074/TS-077 pass focused compile/validate/run for reproduced failure routing, missing-repro stop behavior, plan-update routing, and third-attempt architecture review. |
| Primary orchestrator | `superpowers.yaml` same-job state machine | Covered for initial implementation. TS-080/TS-081 pass focused compile/validate/run for normal design-to-finish orchestration and required child-boundary stop behavior. |
| Necessary child-job boundaries | target refs and child job result contracts | Covered for orchestration primitives. Create a child job only when the task requires a C2 job boundary such as independent target-ref advancement, cross-cell work, reuse, true parallelism, or lifecycle isolation. |
| Task handoff | normal recipe inputs, outputs, artifacts, and job stories | Covered. No required `task_request.json`, `task_result.json`, `base_after`, thinpack, or commit-handoff protocol is needed. |

## Not Product Gaps

These should not be treated as missing c2j/c2ops primitives:

- A dedicated task-loop primitive.
- A general `for_each` primitive for dependent implementation tasks.
- A child job for every Superpowers subagent.
- A parent-owned task acceptance or merge/adoption protocol.
- Required task request/result artifacts.
- Explicit parent-to-child git commit or thinpack handoff for normal target-ref
  execution.
- A dedicated plan-update validation op; use `rule_gate` with `json_schema`.
- Skill invocation for deterministic mechanics that recipe state can decide.
- External review ingestion, legacy Superpowers commands, and browser/UI
  support for this pass.

## Confirmed Product Gaps

No confirmed blocking c2j/c2ops product gaps remain for the initial
Superpowers recipe implementation.

One non-blocking c2j reliability bug remains from the original oversized live
skill-quality run: duplicate story chapter ordinals were logged before the job
eventually timed out. That does not require a new Superpowers primitive and did
not reproduce in the focused required smoke, but it should be fixed in c2j
because long selector-backed jobs must not produce conflicting story chapters.

## Encapsulation Clarification

Child recipe node internals are intentionally encapsulated. A parent can consume
the child job result outputs and result artifacts, not arbitrary artifacts
written by intermediate child nodes.

Implementation implication:

- If the parent planner needs diagnostic artifacts, the child recipe should
  complete with a structured status such as `needs_plan_update` or
  `needs_revision` and export those diagnostics as job result artifacts.
- If the child hard-fails, the parent should treat `recipe.await_result_soft`
  status/failure fields as the workflow data available for routing.
- Debugging a failed child job's intermediate nodes is an introspection concern,
  not normal parent recipe dataflow. If needed, it should be handled through job
  story inspection or a future targeted introspection op, not by breaking recipe
  node encapsulation.

### Embedded Child Resume Story/Cache Errors

Status: **fixed/validated**.

`recipe-tests/verify-child-artifact-forwarding-live.sh` passes, and the previous
`lease is required` signature is fixed. A later `replay cache miss` signature is
also fixed.

```text
lease is required
replay cache miss: task_result_missing
```

This is not the earlier duplicate chapter ordinal conflict: the focused logs do
not contain `workflow state conflict`, `chapter ordinal ... already exists`, or
duplicate ordinal errors. It is tracked separately because it can make passing
embedded child-job runs look failed in logs.

Reverified on 2026-06-09 UTC with `/usr/local/bin/c2j`
(`c2j version v0.0.28-0.20260609031142-3374b852aa99`, SHA-256
`7e6c92ca316fb0e332d786facd2fb35070e9a589b88253977417efc83117427a`): no
`lease is required`, no `replay cache miss`, no recoverable `ERROR`, no
duplicate artifact error, and no chapter ordinal conflict.

Bug reports:

- `guides/BUG_REPORT_C2J_REPLAY_CACHE_MISS_ON_EMBEDDED_CHILD_RESUME.md`
- `guides/BUG_REPORT_C2J_STORY_CHAPTER_PERSIST_REQUIRES_LEASE_ON_CACHED_CHILD_RESUME.md`

## Resolved Product Gaps

### Git State Restore After Mutating Codex Ops

Status: **fixed/validated**.

Validation command:

```bash
recipe-tests/verify-codex-skill-execution-live.sh
```

Current result: the live Codex step completed, wrote git changes, and the
following `command_execution` probes restored git state and completed.

The current live log did not contain the old restore signature:

```text
Repository lacks these prerequisite commits
```

Original result: the live Codex step completed and wrote git changes, but the
following `command_execution` probe failed while restoring git state:

```text
restore git state: failed to apply thin pack ... Repository lacks these prerequisite commits
```

Impact before fix: recipes could not rely on the core pattern "Codex mutates the
worktree, then recipe gates validate the changed worktree" in live embedded
execution.

Requirement doc:

- `guides/new-ticket-simplification/REQUIREMENTS_C2J_GIT_STATE_RESTORE_AFTER_MUTATING_EXTENSION.md`

Bug report:

- `guides/BUG_REPORT_C2J_THIN_PACK_RESTORE_MISSING_PREREQUISITE_COMMITS.md`

## Other Validation Findings

### Large Live Codex Smoke Timed Out

Status: **resolved in the default suite by focusing the smoke**. The original
timeout remains useful evidence for smoke sizing policy and for the separate
c2j story persistence bug.

Validation command:

```bash
recipe-tests/verify-skill-quality-live.sh
```

Original result: the broad recipe progressed through many live Codex steps and
then failed with:

```text
job total timed out after 30m0s
```

This did not show that a single Codex op should take 30 minutes. The old smoke
was a large multi-skill integration recipe with many Codex invocations. The
current required smoke is focused on triage and requirements contracts, uses an
explicit c2j lease/wait timeout, scans for failure signatures, and passed
TS-042/TS-043 on 2026-06-09 UTC.

Broader implementation-planning and outcome-determination skill quality should
be covered by smaller required phase smokes, not by an environment-gated or
optional live test.

### Duplicate Story Chapter Ordinals During Long Live Selector-Backed Run

Status: **confirmed c2j reliability bug, non-blocking for the current
Superpowers implementation path**.

The original broad live skill-quality run logged duplicate chapter ordinal
conflicts before the 30-minute timeout:

```text
workflow state conflict: chapter ordinal 13 already exists
workflow state conflict: chapter ordinal 26 already exists
```

This is separate from the fixed thin-pack git-state restore issue and separate
from the fixed embedded child resume `lease is required` and
`replay cache miss: task_result_missing` signatures. It is job-story
persistence/replay behavior. The focused required skill-quality smoke did not
reproduce the conflict, and the default suite scans for this signature so a
regression hard-fails.

Bug report:

- `guides/BUG_REPORT_C2J_STORY_CHAPTER_DUPLICATE_ORDINAL_DURING_LIVE_REPLAY.md`

Policy doc:

- `guides/new-ticket-simplification/REQUIREMENTS_LIVE_CODEX_TIMEOUT_POLICY.md`

## Deferred Authoring Helper

### Potential Future Authoring Helper: Next-Task Selection

**Current state:** Recipes can select the next task with CEL/templates when the
plan shape is simple. Plan validation can be done with `rule_gate`
`json_schema`.

**Potential issue:** If the Superpowers/C2 plan schema becomes nontrivial,
repeated next-task selection logic may become noisy in YAML.

**Current decision:** Do not implement this op now. First author and test the
parent task loop using native recipe state/CEL/templates. If that implementation
is readable and testable, no helper is needed.

If native selection becomes noisy, add a small c2ops-style
`task_plan.select_next` helper as described in
`guides/new-ticket-simplification/REQUIREMENTS_TASK_PLAN_OPS.md`.

This helper must not run child jobs, mutate git, inspect implementation
correctness, maintain a parallel job history, or replace recipe state machines.

## Remaining Spec/Authoring Work

These are real work items, but they are not platform gaps:

- Define the Superpowers/C2 task-plan JSON Schema.
- Define review rules for child-job eligibility: scope, dependencies,
  validation commands, compatibility notes, target ref policy, and whether the
  task requires a C2 job boundary.
- Refine the initial C2 Superpowers role skills as the phase recipes become
  concrete. The first bundle exists and is covered by TS-058; future edits
  should preserve the no-manual-commit, no-worktree, same-job session, and
  recipe-owned orchestration contract.
- Publish or otherwise expose the local skill bundle as a stable skill-source
  ref for live `codex/run_skill` execution. The route recipe accepts the ref as
  invocation metadata today, but does not yet install it dynamically.
- Continue refining the debug phase only as concrete workflows require deeper
  fix-loop integration. The initial debug recipe is implemented and covered by
  TS-074/TS-077.
- Add target-ref child-job validation only if a concrete flow requires that
  boundary.

## Validation Notes

I found enough local documentation to validate `child_group` behavior:
`guides/CHILD_GROUP_USER_GUIDE.md` documents modes, dynamic children, output
shape, soft failure behavior, and artifact input handling.

I found enough local documentation to validate `recipe.await_result_soft` as a
core child-lifecycle primitive after updating `guides/ops/RUN_RECIPE.md` to
include it.

I checked out the latest c2ops repo at commit `63ba6ba` and found concrete docs
and manifests for:

- `git+https://github.com/colony-2/c2ops.git//codex/run_skill@main`
- `git+https://github.com/colony-2/c2ops.git//rule_gate@main`

The implemented `rule_gate` surface is intentionally smaller than the earlier
requirements draft: it supports `assert`, `artifact_exists`, `file_exists`,
`json_parse`, `json_schema`, and `child_status`; outputs are `ok`,
`failed_rule_ids`, `summary`, and `results`. Recipes should route from those
outputs rather than expecting `next_action` or severity handling inside the op.

## Validation Run: 2026-06-08/09 UTC

Commands and results:

- `/tmp/c2ops-latest/rule_gate`: `go test ./...` passed.
- `/tmp/c2ops-latest/codex`: `go test ./...` passed.
- c2ops manifest checks for `codex/run_skill` and `rule_gate` passed.
- `./recipe-tests/run-all.sh` passed recipe scenario suites TS-001..TS-023 and
  TS-028..TS-041, then passed CLI framework checks TS-024..TS-027.
- The original run stopped at TS-046 because the live script used stale
  `c2j exec`; current c2j uses `c2j run one`. After updating the script,
  `recipe-tests/verify-child-artifact-forwarding-live.sh` passed.
- The original broad `recipe-tests/verify-skill-quality-live.sh` failed after
  progressing through many live Codex ops and reaching a 30-minute total
  runtime; treat this as a smoke sizing/configuration issue unless a smaller
  reproduction shows a timeout knob is ignored. The current focused smoke is
  required from `recipe-tests/run-all.sh`; missing live resources, nonzero live
  job exits, failed assertion diagnostics, and c2j infrastructure signatures
  hard-fail the suite.
- `recipe-tests/verify-codex-skill-execution-live.sh` originally failed after
  the live Codex step when the following command op could not restore the
  persisted git state from the thin pack. It passed on the focused 2026-06-09
  rerun after the thin-pack fix.
- `recipe-tests/verify-superpowers-rule-gate-live.sh` passed TS-047/TS-048:
  JSON parse/schema gates, routeable policy failures, `child_status`, and
  invalid-rule rejection.
- `recipe-tests/verify-superpowers-child-orchestration-live.sh` passed
  TS-049/TS-050 for failed-child status routing and required/optional reviewer
  aggregation.
- Focused mocked Superpowers recipe-shape suites passed TS-051..TS-055 for
  native task selection, required child-boundary detection without child job
  creation, same-job task role sessions, `sessionId` isolation/resume, and
  adaptive task-plan iteration.
- Focused `codex/run_skill` recipe suites passed TS-056/TS-057 for parsed output
  artifacts, status-contract fields, and repair metadata. c2ops `RunSkill` unit
  tests also passed at c2ops commit `8b37f01`.
- Focused static C2 Superpowers skill-bundle suite passed TS-058 for the nine
  C2-adapted role skills and their OpenAI metadata.
- Focused route recipe suite passed TS-059/TS-060 for feature-to-brainstorm
  routing and user-input question enforcement.
- Focused deterministic route cases passed TS-065/TS-066 for submitted
  plan/design routing without skill invocation in the run path.
- Focused brainstorm recipe suite passed TS-061/TS-062 for plan-ready design
  output and stop-before-planning behavior.
- Focused write-plan recipe suite passed TS-063/TS-064 for ready task plans and
  required child-job boundary surfacing.
- Focused execute-plan suite passed TS-067/TS-068 with compile/validate/run.
  TS-067 validates a same-job implement/review/gate task boundary. TS-068
  validates stop-before-implementation behavior with a node non-execution
  assertion for the implementer boundary.
- Focused verify suite passed TS-069/TS-070 with compile/validate/run. TS-069
  validates fresh command evidence before success. TS-070 validates failed
  command evidence remains blocking workflow data.
- Focused finish suite passed TS-071/TS-073 with compile/validate/run. TS-071
  validates merge-ready recommendation from verified evidence. TS-072 validates
  merge blocking when verification has issues. TS-073 validates explicit merge
  after the finish gate.
- Focused debug suite passed TS-074/TS-077 with compile/validate/run. TS-074
  validates reproduced-failure routing to fix-ready. TS-075 validates missing
  reproduction stops before skill invocation. TS-076 validates plan-caused
  failures route to plan update. TS-077 validates architecture review after a
  third reproduced failed attempt.
- Focused plan-review suite passed TS-078/TS-079 with compile/validate/run.
  TS-078 validates aligned-plan approval before execution. TS-079 validates
  incomplete-plan blocking feedback for replanning.
- Focused primary orchestrator suite passed TS-080/TS-081 with
  compile/validate/run. TS-080 validates the normal same-job design-to-finish
  path. TS-081 validates the required child-job boundary stop without invoking
  the implementer session.
- `recipe-tests/run-all.sh` passed end to end on 2026-06-10 with TS-058..TS-081
  included in the default compile/validate/run suite and TS-042/TS-043 focused
  live skill-quality validation invoked by the default runner as a required
  hard-failing live check.
- The focused rerun did not reproduce the story/chapter conflict signature
  (`workflow state conflict`, `chapter ordinal`, or duplicate ordinal errors).
  The original broad skill-quality run did reproduce that signature and has a
  standalone c2j bug report. A different non-blocking story persistence bug,
  `persist task outcome chapter ... lease is required`, reproduced in an earlier
  child-artifact smoke and is now fixed. A follow-up
  `replay cache miss: task_result_missing` signature also reproduced and is now
  fixed.

Decision: the primitive set is still the right shape, and no task-loop or
task-result subsystem is needed. Full Superpowers recipe implementation can
proceed from the initial C2-adapted skill bundle into the full Superpowers phase recipes.
Add target-ref child-job validation only when a concrete recipe flow requires a
child job boundary.

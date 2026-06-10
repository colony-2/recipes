# Superpowers Recipe Mapping Proposal

## Purpose

Recreate the current Superpowers software-development methodology as C2 recipes.
The goal is to preserve the workflow patterns, gates, prompt templates, and review
discipline while replacing in-session subagents with recipe-owned Codex sessions
and, only when needed, child recipe invocations. All agentic work should run
through the c2ops `codex` op.

This proposal is based on:

- Local C2 recipe examples in this repository, especially `new-ticket.yaml`,
  `new-ticket-*-planning.yaml`, `job-implement.yaml`, and `job-validate.yaml`.
- Local recipe authoring guidance in `guides/RECIPE_AUTHORING_GUIDE.md`,
  `guides/ops/README.md`, `guides/ops/RUN_RECIPE.md`,
  `guides/ops/OP_CODEX_EXEC.md`, `guides/NODE_SCOPE_SPEC.md`, and
  `guides/CHILD_GROUP_USER_GUIDE.md`.
- Upstream Superpowers source at `obra/superpowers` commit
  `f2cbfbefebbfef77321e4c9abc9e949826bea9d7` (`v5.1.0`, 2026-05-04 clone).
- Public plugin descriptions:
  [Claude plugin page](https://claude.com/plugins/superpowers) and
  [GitHub repository](https://github.com/obra/superpowers).

Docs under `guides/` that are future proposals, requirements, or bug reports were
not used as design authority.

## Current Validation Status

The recipe shape in this proposal remains the recommended implementation
direction. The previously blocking live git-state restore gap has been
validated fixed with the focused Codex mutation smoke.

Validated on 2026-06-08/09 UTC:

- c2ops `rule_gate` and `codex` Go tests passed.
- c2ops manifests for `codex/run_skill` and `rule_gate` expose the expected
  contract fields.
- Existing recipe scenario suites TS-001..TS-023 and TS-028..TS-041 passed.
- CLI framework checks TS-024..TS-027 passed.
- child artifact forwarding TS-046 passed after updating the smoke to use
  current `c2j run one` instead of stale `c2j exec`.
- focused live Codex mutation/git-state smoke TS-044/TS-045 passed after the
  thin-pack restore fix.
- focused `rule_gate` smoke TS-047/TS-048 passed for JSON Schema,
  policy-failure routing, `child_status`, and invalid-input rejection.
- focused child orchestration smoke TS-049/TS-050 passed for
  `recipe.await_result_soft` failed-child status routing and `child_group`
  required/optional reviewer aggregation.
- focused Superpowers recipe-shape smokes TS-051..TS-055 passed for native task
  selection, required child-boundary detection, same-job role sessions,
  `sessionId` isolation/resume, and adaptive task-plan iteration.
- focused `codex/run_skill` smokes TS-056/TS-057 passed for parsed output
  artifact/status-contract fields and repair metadata. c2ops `RunSkill` unit
  tests also passed at c2ops commit `8b37f01`.
- focused live `codex/run_skill` smoke TS-092/TS-093 passed. The actual c2ops
  op discovered a worktree skill, executed it through Codex, validated
  artifact-first JSON output, validated the status contract, exposed parsed
  fields, and made diagnostics/output artifacts available to a downstream
  same-recipe op.
- static C2 Superpowers skill-bundle smoke TS-058 passed. The repository now has
  ten C2-adapted role skills under
  `skills-bundle/.agents/skills/c2-superpowers-*` with recipe-owned
  orchestration, same-job session, status-contract, no-worktree, and
  no-manual-commit guardrails.
- focused route recipe suite TS-059/TS-060 passed. `superpowers-route.yaml`
  uses recipe state for deterministic artifact-backed routes and invokes
  `codex/run_skill` only for prompt-only heuristic fallback. It validates
  fallback route output through `rule_gate`, routes feature work to
  brainstorming, and requires a concrete user question when the route needs
  human input.
- focused deterministic route cases TS-065/TS-066 passed. Submitted plan
  artifacts route to execution and submitted design artifacts route to planning
  without skill invocation in the run path.
- execute-plan recipe TS-067/TS-068/TS-082/TS-084/TS-087 passed focused
  compile/validate/run. `superpowers-execute-plan.yaml` keeps task selection
  and child-boundary detection deterministic in recipe state, uses role skills
  only for implementer/spec-review/quality-review sessions, asserts the
  implementer node is not executed when a required child-job boundary is
  selected, enforces RED/GREEN/refactor TDD before task review, and routes spec
  and quality review failures through a revision session before re-review,
  including TDD spec-review revision with GREEN/REFACTOR command reruns.
- initial verify recipe TS-069/TS-070 passed focused compile/validate/run.
  `superpowers-verify.yaml` runs fresh validation commands through recipe state,
  then uses the verify role skill only to interpret/write the verification
  result contract. Failed command evidence remains blocking workflow data.
- initial finish recipe TS-071/TS-073 passed focused compile/validate/run.
  `superpowers-finish.yaml` summarizes verified work, gates merge readiness in
  recipe state, blocks merge when verification has issues, and invokes
  `squashrebasemerge` only after an explicit merge action passes the finish
  gate.
- initial debug recipe TS-074/TS-077 passed focused compile/validate/run.
  `superpowers-debug.yaml` stops before skill invocation when reproduction is
  missing, runs reproduction commands through recipe state, asks the debug role
  skill only to interpret evidence, and exposes fix-ready, plan-update, and
  architecture-review outcomes as recipe outputs.
- focused brainstorm recipe suite TS-061/TS-062 passed. `superpowers-brainstorm.yaml`
  validates plan-ready design output and stops before planning when design
  questions remain.
- focused write-plan recipe suite TS-063/TS-064/TS-089/TS-090 passed.
  `superpowers-write-plan.yaml` validates a ready dependent task chain,
  surfaces required C2 child-job boundaries without creating child jobs, and
  requires TDD command contracts for recipe-enforced gates. It also rejects
  child-job tasks that are missing matching boundary metadata.
- focused skill-bundle source wiring TS-091 passed. All Superpowers
  `codex/run_skill` role-skill invocations install the configured
  `skill_bundle_ref` through the op-level `skills` input.
- focused plan-review recipe suite TS-078/TS-079 passed. `superpowers-plan-review.yaml`
  approves aligned task plans and returns replanning feedback for incomplete
  plans without rewriting the plan.
- primary orchestrator recipe TS-080/TS-086/TS-088 passed focused
  compile/validate/run. `superpowers.yaml` routes the full same-job
  design-to-finish path, enforces RED/GREEN/refactor TDD before task review, and
  routes TDD spec-review failure through revision, GREEN/REFACTOR reruns, and
  re-review.
- `recipe-tests/run-all.sh` passed end to end on 2026-06-10 with TS-058..TS-093
  included in the default compile/validate/run path. Required live checks now
  include TS-092/TS-093 live `codex/run_skill`, TS-044/TS-045 live Codex skill
  execution, and TS-042/TS-043 focused live skill-quality validation.
- focused live skill-quality smoke TS-042/TS-043 passed after narrowing the
  smoke to triage, requirements-author, and bad-requirements contrarian-review
  contracts. The runner does not gate this check behind an environment flag;
  missing skill resources, timeouts, or c2j failure signatures hard-fail the
  suite.

Resolved runtime gap:

- A live Codex mutation followed by `command_execution` previously failed
  during git-state restore because the thin pack lacked prerequisite commits.
  The focused rerun now passes and did not contain the restore signature.

Additional validation finding:

- The original large live skill-quality smoke exceeded 30 minutes across many
  Codex invocations. That was a smoke sizing issue, not evidence that one Codex
  op should take 30 minutes. The default smoke is now focused; broader phase
  coverage should be added as smaller required smokes instead of gating or
  skipping live skill-quality coverage.
- The original large live skill-quality run also logged duplicate story chapter
  ordinal conflicts before timing out. That is a c2j story persistence
  reliability bug, not a Superpowers implementation design gap.
- Child recipe internals are encapsulated. A parent should consume child job
  result outputs/artifacts, not intermediate child-node artifacts. If the parent
  planner needs diagnostic artifacts, the required child recipe should complete with
  a structured `needs_plan_update` or `needs_revision` result and export those
  diagnostics as job result artifacts.

No chapter/story ordinal conflict reproduced in focused reruns. The separate
embedded cached/resume-path story issues, `persist task outcome chapter ...
lease is required` and `replay cache miss: task_result_missing`, were fixed and
validated with `c2j version v0.0.28-0.20260609031142-3374b852aa99`.

## Current Superpowers Shape

Current upstream Superpowers is primarily a skill library plus a session-start
bootstrap hook. The recipe mapping should target the durable skill workflows and
prompt templates rather than command shims or conversational session mechanics.

## Superpowers Task Vocabulary

In `subagent-driven-development`, a "task" is primarily an implementation-plan
item: "Task N" is handed to an implementer, implemented, tested, committed, then
reviewed for spec compliance and code quality. Reviewer prompts are also sent
through Claude's Task tool, but they are reviewer roles for the implementation
task, not separate implementation-plan tasks in the queue.

The Superpowers parent/controller does not do implementation work in the
subagent-driven path. It reads the plan, extracts task text, dispatches the
implementer, dispatches reviewers, handles questions/blockers, and decides when
to move to the next task.

Implementation tasks are expected to be mostly independent. Superpowers chooses
the subagent-driven workflow only when tasks are mostly independent, and its
implementer prompt asks the worker to implement exactly one task, write tests,
verify the implementation, commit the work, self-review, and report status. The
C2 recipe mapping should preserve that as independently verifiable task slices,
while removing the instruction for Codex to make manual git commits because C2
persists git state automatically. "Committable" here means the task produces a
coherent local changeset for review and sequencing; it does not necessarily mean
every task is independently mergeable to the base branch without later dependent
tasks.

## Design Principles

1. **Recipes own orchestration.** A C2 primary job should decide which workflow
   phase runs next, when to pause for human input, when to start or resume Codex
   sessions, when a child job boundary is actually needed, and when to merge.
2. **State machines own deterministic mechanics.** Use recipe transitions, CEL,
   command gates, and `rule_gate` for routing from existing artifacts, selecting
   ready tasks, enforcing schema/policy, and sequencing phases. Do not invoke a
   skill for work that the recipe can decide mechanically.
3. **Codex owns agentic work.** Each concrete authoring, implementation, review,
   or debugging step uses `git+https://github.com/colony-2/c2ops.git//codex@main`
   or `codex/run_skill` when a role skill and artifact contract are the intended
   interface.
4. **Separate role context from work boundaries.** Fresh Codex sessions provide
   the isolated agent context Superpowers gets from subagents. C2 jobs provide
   durable work, validation, and merge boundaries only when the workflow needs a
   job boundary.
5. **Artifacts replace conversation memory.** Specs, plans, task reports,
   reviews, debugging evidence, and verification results must be written to C2
   artifacts, then explicitly passed to later steps.
6. **C2 git isolation replaces manual worktree setup.** Do not create git
   worktrees inside recipes unless a specific integration harness needs an
   extra checkout. The C2 worktree and cell boundary already provide the
   isolation Superpowers seeks.
7. **Human gates stay explicit.** Superpowers asks for design approval, spec
   review, branch completion choices, and architecture discussion after repeated
   failed fixes. In recipes, those become structured `input` states.
7. **Recipe gates are stronger than prompt discipline.** Superpowers relies on
   an agent following skill instructions inside one conversation. C2 can make
   the same discipline structural: the next state should be unreachable unless
   required artifacts exist, command exits match expectations, review verdicts
   pass, and human gates are approved.
8. **Codex does work, recipes prove work.** Codex may author tests, code, plans,
   reviews, and summaries. Recipe states should run the proving commands and
   inspect machine-readable outputs before allowing progress.

## Enforcement Model

The C2 version should not be a weaker "skills over Codex" port. It should be a
recipe-enforced development loop.

Superpowers says "write the failing test first" and depends on the agent to obey.
C2 can split that into separate states:

1. Codex writes only the RED test.
2. `command_execution` runs the RED command with `continue_on_error: true`.
3. A rule/check state verifies the RED command failed for the expected reason.
4. Codex writes the minimal GREEN implementation.
5. `command_execution` runs the GREEN command and requires exit code `0`.
6. Codex refactors only after GREEN.
7. `command_execution` reruns the relevant commands and requires exit code `0`.

Codex cannot advance the recipe by saying the test failed or passed. Only the
recorded command outputs, exit codes, review JSON, and artifact presence should
drive transitions.

The same pattern should apply to debugging, reviews, and completion:

- no fix state before reproduced failure/root-cause evidence exists
- no quality review before spec review passes
- no finish/merge before fresh verification output exists
- no human-review bypass when a state requires approval

## Recipe-Native Solution Patterns

The migration should not treat Superpowers instructions as best-effort prompts.
Each Superpowers discipline should become a recipe-owned contract with explicit
inputs, outputs, artifacts, git state, and transitions.

### Sessions, Job Boundaries, And Parent Control

The Superpowers "fresh subagent per task" pattern has two separable meanings in
C2:

- A fresh worker context maps to a fresh Codex session.
- A child job is a durable C2 work boundary, not the default substitute for a
  Superpowers subagent.

The parent should not implement or re-review task correctness. It should keep
durable plan state, start or resume role-specific Codex sessions with ordinary
recipe inputs, collect session status/output artifacts, and route those artifacts
to the planner step that decides the next head task.

The `codex` op returns `sessionId`, and existing recipes already use that value
to resume an implementation session. The Superpowers port should apply that
inside each task execution boundary:

1. planning emits plan state with tasks, dependencies, write scopes, target ref
   policy, and optional parallel groups
2. the parent selects the next ready head task with native recipe
   state/CEL/templates; add a helper only if the authored recipe proves noisy
3. the selected task runs through a nested state machine in the same job by
   default, using separate Codex sessions for implementer, spec reviewer, quality
   reviewer, and revision roles
4. each role writes status and output artifacts that the enclosing task state
   exports explicitly
5. a planner step consumes the task boundary outputs/artifacts and updates plan
   state, then the loop selects the next head task from that updated state

Create a child job only when the workflow cannot satisfy the requirement inside
the current job:

- the task should advance a target ref independently as a small C2 changeset;
- the work belongs to another cell;
- the workflow is reusable across recipes;
- parallelism is valuable and scopes are independent;
- failure/cancellation should be isolated from the parent job lifecycle.

Upstream Superpowers explicitly avoids multiple parallel implementation
subagents in its main implementation loop, so the C2 default should also avoid
parallel code-mutating execution. The selected task should run as same-job
sessions unless one of those required job-boundary conditions applies. In both
cases, the controller should select one head task, run it, send its outputs to
the planner, and then choose the next task. What task 1 teaches may change the
prompt, validation, split, or ordering for task 2.

Session semantics:

- No `sessionId` means start a completely isolated Codex session. The session
  does not inherit prior conversational context from other sessions; it only sees
  the prompt, allowed tools, current worktree, and artifacts explicitly provided.
- Providing `sessionId` means continue that previous Codex session and carry
  conversational context forward for that ID.

### Nested State Machines

Nested state machines are the default structure for workflow depth:

- the outer recipe routes phases such as brainstorm, plan, execute, verify, and
  finish
- the execution state machine owns the task queue and selected task metadata
- the per-task nested state machine owns implement, spec review, quality review,
  revision, and task completion
- the TDD nested state machine owns RED, GREEN, refactor, and verification gates
- the debugging nested state machine owns reproduce, evidence, hypothesis, fix,
  and verify loops

Each nested boundary should export only the artifacts and status data the parent
needs. This keeps the job durable and inspectable without manufacturing a new
recipe/job for every logical agent role.

### Session Registry

The task execution boundary should maintain a small session registry artifact.
This is the same idea as Superpowers' controller remembering which worker did
what, but made explicit:

```json
{
  "tasks": {
    "TASK-1": {
      "implementer_session_id": "",
      "spec_reviewer_session_id": "",
      "quality_reviewer_session_id": "",
      "status": "pending|implemented|needs_revision|blocked|done",
      "artifacts": []
    }
  }
}
```

The registry lets one recipe own many discrete Codex sessions at once. A later
state can resume a specific session by passing its `sessionId`, or start a fresh
session by omitting `sessionId`.

### Git Advancement

Sequential Codex sessions inside one recipe use the normal C2 git persistence
model. After each mutating Codex op, C2 persists the current cell changes, and
later states continue from that updated recipe git context. No parent/child git
adoption is needed for the ordinary task loop.

Current validation note: the 2026-06-09 focused live Codex smoke validates this
model for a mutating Codex op followed by command probes. The original missing
prerequisite commit failure is tracked historically in
`guides/new-ticket-simplification/REQUIREMENTS_C2J_GIT_STATE_RESTORE_AFTER_MUTATING_EXTENSION.md`
and
`guides/BUG_REPORT_C2J_THIN_PACK_RESTORE_MISSING_PREREQUISITE_COMMITS.md`.

Same-job task sessions are the normal path for Superpowers role isolation and
task sequencing. Do not create child jobs for normal dependent tasks.

Create a child job only when the task must advance a target ref independently,
run in another cell, be reused from another recipe, fan out in true parallelism,
or have lifecycle isolation from the current job. When that job boundary is
required:

1. parent starts child job N with task inputs and a target ref, defaulting to
   `main`
2. child job N implements, tests, reviews, validates, and advances the target ref
   as part of its own success path
3. parent awaits the child job and routes child status, outputs, artifacts, and
   feedback to the planner
4. planner updates plan state
5. parent starts child job N+1 against the same target ref unless the updated
   plan chooses a different ref

Use this pattern only when the task is independently mergeable enough that
advancing a target ref is the right boundary. Otherwise, keep the task loop
inside one job and let normal C2 git persistence carry state between session
roles and task states.

The normal git handoff is the target ref itself. If child job N succeeds on
`main`, child job N+1 targeting `main` starts from the updated `main`. If the
plan is experimental, the same pattern uses an experiment ref. Parent recipes
should not need explicit commit or thinpack handoff for this common path.

### Review Fanout

The default review path is sequential sessions in the same recipe: spec
compliance first, then quality review only after spec compliance passes.

Use `child_group.mode: run_and_get_result` only when reviewer/checker work should
actually fan out in parallel or when the reviewer workflow is reused elsewhere:

- mark blocking reviewers as `required: true`
- mark advisory reviewers as `required: false`
- use `aggregate.shape: review_pack` for reviewer summaries, warnings, and
  blocking issues
- route back to revision whenever the group reports `ok=false` or required
  blocking issues

Do not use `child_group` for dependent implementation tasks. Its wait-for-all
shape is right for adversarial feedback packs, not for a task chain where each
successful task can change the next task's base and instructions.

### Prompt Routing

The "check/use skills before any response" behavior is enforceable in recipes.
`superpowers-route.yaml` should classify the ticket, select the required skill
contract, and render the final Codex prompt before any task-facing Codex op
runs. Phase states, task sessions, reviewer sessions, and any required child
recipes should receive that route result and embed the selected skill text or
skill selector directly in their Codex inputs.

### TDD, Debugging, Review, And Verification

Discipline loops should be split across states:

- TDD: RED Codex step, RED command, RED assertion, GREEN Codex step, GREEN
  command, refactor step, final verification command
- debugging: reproduction, root-cause evidence, pattern analysis, hypothesis,
  hypothesis test, regression test, fix, verification
- review: spec compliance first, quality review second, revision loop on
  blockers
- completion: fresh verification and explicit merge/finish decision

Codex can produce the artifacts and code, but recipe transitions decide whether
the workflow is allowed to move forward.

### Skill Adaptation

Start from upstream Superpowers skills at a pinned commit, then create a
C2-adapted skill bundle. The adapted skills should preserve the behavioral
patterns and prompt language while changing instructions that recipes now own:

- remove manual git commit instructions
- remove manual worktree setup instructions
- replace in-session subagent dispatch with same-job session contracts and
  child-job boundaries only where C2 workflow semantics require them
- require artifact paths, status contracts, and structured JSON outputs
- replace "agent verified" language with recipe-run command gates
- describe task boundaries as owning task-local success and validation; describe
  target-ref advancement only for child-job boundaries when required

## Proposed Recipe Inventory

This inventory names reusable workflow boundaries. It is not a requirement to
create a separate recipe for every Superpowers agent role. The MVP can inline
most of the task, review, TDD, and debugging roles as nested states inside one
execution recipe, while still extracting high-level phases when reuse or
readability justifies it.

### Primary Orchestrator

`superpowers.yaml`

Thin state-machine recipe that routes the ticket through the whole methodology:

1. `route`
2. `brainstorm_design`
3. `write_plan`
4. `review_plan`
5. `select_task` / `run_task_boundary`
6. `verify_work`
7. `finish_work`

This should be the equivalent of the Superpowers session bootstrap, but C2-native:
instead of injecting `using-superpowers` into every chat session, the recipe
routes from ticket intent and produced artifacts.

Inputs:

- `prompt`
- `mode` optional: `auto`, `brainstorm`, `write_plan`, `execute_plan`, `debug`,
  `review_feedback`, `finish`
- `spec_artifact` optional
- `plan_artifact` optional
- `validation_commands` optional

Outputs:

- route decision
- spec artifact key
- plan artifact key
- implementation status
- verification result
- merge/completion decision

Implementation status:

- `superpowers.yaml` is implemented as a same-job state machine for the normal
  design-to-finish MVP path. It does not invoke child recipes for ordinary
  Superpowers role sessions.
- TS-080 validates route, brainstorm, write-plan, plan-review, same-job
  implement/spec/quality sessions, fresh verification, and finish recommendation
  in one job.
- TS-081 validates that a task marked `requires_child_job=true` stops before
  the implementer session.
- TS-085 validates that a failed spec review in the primary same-job task
  boundary routes through revision and then re-runs spec and quality review
  before verification and finish.
- TS-086 validates that a primary task marked `requires_tdd=true` routes through
  recipe-enforced RED/GREEN/refactor gates before task review and does not invoke
  the normal implementer boundary.
- TS-088 validates that a primary TDD task with blocking spec feedback routes
  through a TDD revision session, reruns GREEN/REFACTOR verification, and
  completes post-revision spec/quality review before verification and finish.

### Bootstrap And Routing

`superpowers-route.yaml`

Maps `using-superpowers` into a deterministic C2 gate. It should inspect the
ticket prompt and submitted artifacts, then return:

```json
{
  "recommended_mode": "brainstorm|write_plan|execute_plan|debug|review_feedback|finish",
  "required_skills": ["brainstorming"],
  "rationale": "short explanation",
  "needs_user_input": false,
  "user_question": ""
}
```

Codex prompt source:

- Preserve the `using-superpowers` priority rules: user instructions first,
  Superpowers workflow second, default model behavior last.
- Preserve skill priority: process skills such as brainstorming/debugging before
  implementation skills.

Recipe behavior:

- If a submitted plan exists, route to execution.
- If a submitted spec exists and no plan exists, route to planning.
- If the prompt is a bug/test failure, route to debugging.
- If the prompt is feature/behavior work without an approved spec, route to
  brainstorming.
- If uncertain, pause with structured `input` rather than letting Codex improvise.

Implementation status: initial state-machine recipe implemented and validated by
TS-059/TS-060 and TS-065/TS-066. Submitted plan/design/verification artifacts
route deterministically without invoking Codex. Prompt-only classification uses
`codex/run_skill` as the heuristic fallback and validates that output with
`rule_gate`. When a `skill_bundle_ref` is provided, the route recipe installs it
through `codex/run_skill.inputs.skills`; the remaining deployment choice is the
stable published ref value used by production jobs.

### Brainstorming

Implementation status: initial `superpowers-brainstorm.yaml` recipe implemented
and validated by TS-061/TS-062. It uses `codex/run_skill` for the
`c2-superpowers-brainstorm` role and `rule_gate` for deterministic advancement
checks. Plan-ready designs must include plan inputs; designs that are not ready
for planning must include open questions.

`superpowers-brainstorm.yaml`

Maps the `brainstorming` skill.

Superpowers behavior to preserve:

- Explore project context before detailed questions.
- Ask one clarifying question at a time.
- Decompose oversized requests before specification.
- Present 2-3 approaches with tradeoffs and a recommendation.
- Present the design in reviewable sections.
- Require user approval before implementation planning.
- Perform a spec self-review for placeholders, contradictions, scope, and
  ambiguity.

C2 adaptation:

- Use Codex to produce a design artifact, not a repo doc by default.
- Store the design under `superpowers/brainstorm/design.md`.
- Store structured metadata under `superpowers/brainstorm/result.json`.
- Use an `input` state for section approval and final design approval.
- Optionally write a repo doc only when the cell's conventions require it.

Artifacts:

- `superpowers/brainstorm/design.md`
- `superpowers/brainstorm/result.json`
- `superpowers/brainstorm/latest-status.json`
- `superpowers/brainstorm/user-feedback.md` when revisions occur

### Writing Plans

Implementation status: initial `superpowers-write-plan.yaml` recipe implemented
and validated by TS-063/TS-064/TS-089/TS-090. It uses `codex/run_skill` for the
`c2-superpowers-write-plan` role, validates the task-plan artifact, exposes the
first ready task, and treats child-job boundaries as plan data rather than
automatically creating child jobs. TDD tasks must include executable RED,
GREEN, and refactor verification commands for the recipe-owned TDD loop. Tasks
marked `requires_child_job=true` must have matching `child_job_boundaries`
entries, and orphan boundary entries are rejected.

`superpowers-write-plan.yaml`

Maps the `writing-plans` skill.

Superpowers behavior to preserve:

- Build a comprehensive implementation plan from an approved spec.
- Make tasks bite-sized.
- Include exact files, steps, verification commands, and TDD requirements.
- For TDD tasks, include executable RED, GREEN, and refactor verification
  commands because the recipe, not the skill, owns loop enforcement.
- Assume an implementer has little project context.
- Apply YAGNI and DRY.
- Self-review the plan before execution.

C2 adaptation:

- Codex writes the plan as C2 artifacts.
- A separate Codex reviewer session reviews the plan with
  `skills/writing-plans/plan-document-reviewer-prompt.md`.
- The plan should be machine-readable enough for task sessions and required
  child recipes.

Artifacts:

- `superpowers/plan/plan.md`
- `superpowers/plan/plan.json`
- `superpowers/plan/tasks/<task-id>.md`
- `superpowers/plan/file-map.md`
- `superpowers/plan/verification-commands.txt`
- `superpowers/plan/self-review.json`
- `superpowers/plan/review.json`

Suggested `plan.json` shape:

```json
{
  "plan_id": "PLAN-1",
  "summary": "",
  "tasks": [
    {
      "id": "TASK-1",
      "title": "",
      "status": "pending",
      "dependencies": [],
      "target_ref": "main",
      "requires_child_job": false,
      "child_job_reason": "",
      "instructions": "",
      "validation_commands": [],
      "review_requirements": ["spec", "quality"]
    }
  ],
  "ready_task_ids": ["TASK-1"],
  "validation_strategy": {
    "commands": []
  },
  "child_job_boundaries": []
}
```

### Plan Review

`superpowers-plan-review.yaml`

Uses `c2-superpowers-plan-review` as a Codex review task.

Inputs:

- spec artifact
- plan artifact

Outputs:

```json
{
  "ok": true,
  "issues": [],
  "recommendations": [],
  "blocking_feedback": "",
  "requires_replan": false
}
```

The primary orchestrator should route back to `superpowers-write-plan.yaml` when
`ok=false`.

Implementation status:

- `superpowers-plan-review.yaml` is implemented for aligned-plan approval and
  incomplete-plan replanning feedback.
- TS-078 validates approval of a plan that covers the design and has validation
  evidence.
- TS-079 validates blocking feedback and `requires_replan=true` for incomplete
  plans.

### Execute Plan

`superpowers-execute-plan.yaml`

Implementation status: initial recipe implemented. TS-067 validates the run path
for one same-job implementation/spec-review/quality-review task boundary.
TS-068 validates deterministic stop-before-implementation behavior when the
selected task requires a child job. TS-082 validates recipe-enforced
RED/GREEN/refactor TDD before task review. TS-083 validates spec-review failure
routing through revision and re-review, including that initial quality review is
not invoked before spec passes. TS-084 validates quality-review failure routing
through revision and re-review, including that the initial task gate is not
invoked before quality review passes. All five pass focused compile/validate/run, and
the execute-plan suite is wired into
`recipe-tests/run-all.sh`.

Maps `subagent-driven-development` first, with `executing-plans` as a sequential
recipe-state implementation loop.

Superpowers behavior to preserve:

- Fresh isolated worker per task.
- Controller extracts full task text and gives it to the worker.
- Implementer performs TDD when required, verifies, self-reviews, and reports
  `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`.
- Spec compliance review runs before code quality review.
- Code quality review does not start until spec compliance passes.
- Review issues route back to implementation and then re-review.
- Continuous execution should not ask the human "should I continue?" between
  tasks.
- Stop only for true blockers, ambiguity, architecture concerns, or completion.

C2 adaptation:

- The controller is a state machine over durable plan state.
- For normal implementation, the controller selects one head task and runs it in
  a nested same-job task state machine.
- The task boundary receives only the selected task, selected skill contract,
  relevant artifacts, cell context, and constraints.
- Implementer, spec reviewer, and quality reviewer are separate Codex sessions.
  They are not separate jobs unless parallelization, reuse, cross-cell work, or
  target-ref advancement justifies it.
- The task boundary records implementer, spec reviewer, and quality reviewer
  `sessionId` values when the sessions may need to resume.
- Nested state machines inside the task boundary handle TDD, revision, review
  ordering, and completion without creating a new job per role.
- Use `child_group` with `children_from` only for true dynamic fanout:
  independent read-only checks or reusable child workflows.
- Use an ordinary recipe state machine for dependent implementation tasks so the
  controller can adapt after each task result. A new `for_each` or task-loop
  primitive is not required for this pattern.
- This is stronger than upstream Superpowers. Upstream uses one isolated
  worktree for the session and fresh subagent context per task; it explicitly
  avoids parallel implementation subagents because of conflicts.

Session roles:

- `task_implementer_session`
- `task_spec_reviewer_session`
- `task_quality_reviewer_session`
- `task_revision_session`, usually resuming or replacing the implementer session
- `final_code_reviewer_session`

Controller states:

1. `load_plan`
2. `select_next_task`
3. `run_task_boundary`
4. `handle_task_status`
5. `planner_update`
6. `final_review`
7. `done`

Artifacts per task:

- `superpowers/execution/tasks/<task-id>/implementer-report.md`
- `superpowers/execution/tasks/<task-id>/implementer-status.json`
- `superpowers/execution/tasks/<task-id>/spec-review.json`
- `superpowers/execution/tasks/<task-id>/quality-review.json`
- `superpowers/execution/tasks/<task-id>/revision-feedback.md`

Task boundary pattern:

- Planning emits plan state with task metadata, dependency metadata, write
  scopes, target ref policy, and optional parallel groups.
- The parent selects the next ready head task from plan state.
- For normal implementation, the next head task has one code-mutating task.
- The parent runs a same-job task state machine with ordinary inputs for the
  selected task, artifacts, constraints, and skill contract.
- The task boundary runs implementer, spec reviewer, and quality reviewer
  sessions.
- Review blockers route to a revision session inside the task boundary and then
  back through review.
- When the task boundary passes, it exports normal outputs/artifacts with
  feedback.
- The parent routes task status/outputs/artifacts to the planner step.
- The planner may revise the remaining task plan before the parent selects the
  next task.
- Read-only reviews/checks can fan out through `child_group` when parallelism is
  valuable.
- If the task requires independent target-ref advancement, cross-cell execution,
  reuse, true parallel execution, or lifecycle isolation, replace the same-job
  task boundary with a required child recipe that exports the same status/output
  contract.

Required child-job git sequencing pattern:

- Use this only when the task boundary requires a child job.
- Child job N starts from its target ref, usually `main`.
- A successful code-changing child job advances that target ref.
- If task N+1 also requires a child job and targets the same ref, it
  naturally starts from the updated ref.
- If the recipe intentionally uses parallel implementation jobs, each job starts
  from an explicit target-ref policy and returns normal recipe outputs. The
  integration policy must be explicit in the child workflow or a dedicated
  integration workflow before dependent work consumes the integrated ref.

### Task Implementer

`task_implementer_session` inside `superpowers-execute-plan.yaml`

Uses `skills/subagent-driven-development/implementer-prompt.md` as the core
prompt template.

Codex inputs:

- task id/title
- full task text artifact
- spec artifact
- plan artifact
- previous review feedback artifact, optional
- validation commands for this task

Codex prompt constraints:

- Work only in the current cell.
- Follow existing patterns.
- Use TDD when the task requires it.
- Verify before reporting.
- Commit cadence is handled by C2; the worker should still report files changed
  and verification evidence.
- Do not silently produce work if uncertain.

Outputs:

```json
{
  "status": "DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT",
  "summary": "",
  "tested": "",
  "files_changed": [],
  "self_review_findings": [],
  "concerns": [],
  "questions": []
}
```

### Spec Compliance Review

`task_spec_reviewer_session` inside `superpowers-execute-plan.yaml`

Uses `skills/subagent-driven-development/spec-reviewer-prompt.md`.

Review contract:

- Do not trust the implementer report.
- Read actual code/diff.
- Compare implementation to task requirements line by line.
- Detect missing requirements, extra work, and misunderstandings.

Outputs:

```json
{
  "ok": true,
  "missing_requirements": [],
  "extra_work": [],
  "misunderstandings": [],
  "feedback": ""
}
```

### Code Quality Review

`task_quality_reviewer_session` inside `superpowers-execute-plan.yaml`

Uses `skills/subagent-driven-development/code-quality-reviewer-prompt.md`, which
delegates to the consolidated code-reviewer template.

Review contract:

- Categorize findings by severity.
- Include file and line references.
- Check separation of concerns, tests, maintainability, compatibility, security,
  and architecture.
- Give a clear merge/readiness verdict.

Outputs:

```json
{
  "ready": "yes|no|with_fixes",
  "strengths": [],
  "critical": [],
  "important": [],
  "minor": [],
  "recommendations": [],
  "reasoning": ""
}
```

### Parallel Agent Dispatch

`superpowers-dispatch-parallel.yaml`

Maps `dispatching-parallel-agents`.

Use cases:

- Independent failing test files.
- Independent task groups with no shared files or state.
- Reusable workflow units that are worth running as separate jobs.

C2 adaptation:

- Use `recipes.run` for fire-and-forget fanout.
- Use `recipes.run_and_wait` when the parent should continue only after all
  children complete.
- Use separate cells whenever possible.
- For same-cell parallel work, require disjoint write scopes and review diffs
  before integration.
- If same-cell parallel children mutate code, treat each child result as a
  branch from a known parent git context. The parent chooses which child results
  to accept and integrates them one at a time with fast-forward/rebase/conflict
  gates.

Design note:

- This is more reliable than the upstream Superpowers parallel-agent pattern.
  Upstream parallel dispatch instructs the controller to manually check for
  conflicts and run the full test suite after agents return. C2 can make those
  checks explicit transition gates before accepting each child result.

### Test-Driven Development

Nested `tdd_task` state inside `superpowers-execute-plan.yaml`

Maps `test-driven-development`.

Implementation status: implemented. TS-082 validates that tasks marked
`requires_tdd=true` run RED, GREEN, and refactor command gates and cannot reach
task review until the recipe-owned TDD evidence passes.

Superpowers behavior to preserve:

- No production code without a failing test first.
- Delete any production code written before the failing test.
- Red: write one behavioral test and verify it fails for the expected reason.
- Green: write minimal code and verify it passes.
- Refactor only after green.
- Never fix bugs without a reproducing test.

C2 adaptation:

- Model TDD as a recipe state loop, not a single Codex instruction.
- Codex writes tests and code in separate phases.
- `command_execution` runs RED/GREEN/refactor verification commands.
- Transition guards check exit codes and required output artifacts.
- Reviewers inspect the evidence, but reviewer approval is not the primary
  enforcement mechanism.

Suggested state loop:

1. `write_red_test`: Codex may modify only test files for the selected behavior.
2. `run_red_test`: `command_execution` runs the focused test with
   `continue_on_error: true`.
3. `assert_red`: fail or route back unless the command failed for the expected
   reason.
4. `write_green_code`: Codex may modify implementation code and supporting tests.
5. `run_green_test`: `command_execution` reruns the focused test.
6. `assert_green`: fail or route back unless exit code is `0`.
7. `refactor`: Codex may clean up without adding behavior.
8. `run_refactor_verification`: run focused and relevant broader commands.
9. `assert_refactor`: fail or route back unless all required commands pass.

Evidence artifact:

```json
{
  "red_command": "",
  "red_exit_code": 1,
  "red_expected_failure": "",
  "green_command": "",
  "green_exit_code": 0,
  "refactor_verification_command": "",
  "refactor_exit_code": 0
}
```

Enforcement rule:

- A task with `requires_tdd=true` cannot transition to spec review unless RED,
  GREEN, and refactor verification evidence exists and the recipe checks pass.
- A bugfix cannot transition to `fix` until a reproducing RED test or approved
  one-off reproduction artifact exists.

### Systematic Debugging

`superpowers-debug.yaml`

Maps `systematic-debugging`.

Recipe states:

1. `collect_debug_inputs`: normalize the bug report, optional reproduction
   command, failure context, and failed-attempt count.
2. `needs_repro_command`: stop before skill invocation when reproduction is
   missing.
3. `investigate`: run the reproduction command with `continue_on_error`,
   invoke `c2-superpowers-debug` to interpret evidence, then gate the structured
   result with `rule_gate`.

Artifacts:

- `superpowers/debug/debug-inputs.json`
- `superpowers/debug/repro-command.sh`
- `superpowers/debug/repro-output.txt`
- `superpowers/debug/repro-output-tail.txt`
- `superpowers/debug/evidence.md`
- `superpowers/debug/result.json`
- `superpowers/debug/latest-status.json`
- `superpowers/debug/action.json` when reproduction is missing

The debug recipe exposes a `debug_status` output instead of creating child jobs
or fixing code itself. Current statuses are `needs_repro_command`, `fix_ready`,
`requires_plan_update`, `architecture_review_required`, and `not_reproduced`.
After three reproduced failed attempts, the output becomes
`architecture_review_required`; a parent recipe should route that to a
structured human/design gate before another fix attempt.

Implementation status:

- `superpowers-debug.yaml` is implemented for missing-reproduction,
  reproduced-failure, plan-update, and third-attempt architecture-review paths.
- TS-074 validates reproduced failure routing to fix-ready.
- TS-075 validates missing reproduction stops before skill invocation.
- TS-076 validates plan-caused failures route to plan update.
- TS-077 validates architecture review after a third reproduced failed attempt.

### Verification Before Completion

`superpowers-verify.yaml`

Maps `verification-before-completion` and can reuse or wrap `job-validate.yaml`.

Superpowers behavior to preserve:

- No completion claim without fresh verification.
- Identify commands that prove each claim.
- Run full commands, read output, check exit code, and report actual state.
- Verify requirements line by line, not just tests.

C2 adaptation:

- Always run before final review and before merge.
- Persist full output and tail output as artifacts.
- Require a structured result object.
- Route to finish/merge only when the verification result says the required
  commands passed. Human override, if allowed, should be explicit and recorded.

Artifacts:

- `superpowers/verification/commands.sh`
- `superpowers/verification/output.txt`
- `superpowers/verification/output-tail.txt`
- `superpowers/verification/result.json`
- `superpowers/verification/requirements-checklist.md`

### Requesting Code Review

`superpowers-request-code-review.yaml`

Maps `requesting-code-review`.

C2 adaptation:

- Use Codex as a reviewer session by default.
- Base/head should come from C2 git context or explicit diff artifacts.
- Findings should be artifacts and gate merge.
- Critical issues block progress.

This can share the same prompt contract as `task_quality_reviewer_session` and
`final_code_reviewer_session`.

### Receiving Code Review

`superpowers-receive-code-review.yaml`

Maps `receiving-code-review`.

Superpowers behavior to preserve:

- Read complete feedback before reacting.
- Understand and restate requirements.
- Verify before implementing suggestions.
- Ask when feedback is unclear.
- Push back on incorrect or overbroad feedback with evidence.

C2 adaptation:

- Human or reviewer feedback is an input artifact.
- Codex produces a response plan artifact.
- If implementation is required, route to a task implementation session with the
  accepted feedback as task text.

Artifacts:

- `superpowers/review-feedback/received.md`
- `superpowers/review-feedback/analysis.json`
- `superpowers/review-feedback/accepted-actions.md`
- `superpowers/review-feedback/pushback.md`

### Finishing A Development Branch

`superpowers-finish.yaml`

Maps `finishing-a-development-branch`.

Superpowers behavior to preserve:

- Verify tests before presenting completion options.
- Detect environment and branch state.
- Present clear choices: merge locally, push/create PR, keep as-is, discard.
- Clean up only workspaces created by the workflow.

C2 adaptation:

- Use `superpowers-verify.yaml` or `job-validate.yaml`.
- Use a structured `input` form for merge/PR/keep/cancel.
- Use `squashrebasemerge` for merge.
- Do not do manual worktree cleanup unless the recipe created an extra worktree.
- "Discard" should not destroy user work automatically; it should route to a
  cancelled/closed job state unless explicit cleanup support exists.

Implementation status:

- `superpowers-finish.yaml` is implemented for recommendation, hold/cancel,
  blocked merge, and explicit squash-rebase-merge paths.
- TS-071 validates merge-ready recommendation from verified evidence.
- TS-072 validates merge is blocked when verification evidence has blocking
  issues.
- TS-073 validates merge only runs after explicit action and a passing finish
  gate.

### Writing Skills

`superpowers-write-skill.yaml`

Maps `writing-skills` for future C2 skill/prompt authoring work.

C2 adaptation:

- Treat prompt/skill changes as process-code changes.
- Require failing pressure scenarios before editing skill text.
- Use C2 recipe tests or live Codex smoke tests as the RED/GREEN evidence.
- Store test transcripts and evaluation results as artifacts.

This is not required for the first Superpowers workflow MVP, but it should be
available if we want to maintain C2-specific Superpowers skill variants.

## Codex Op Usage Pattern

Every Codex-backed recipe should follow the local convention:

```yaml
op: git+https://github.com/colony-2/c2ops.git//codex@main
inputs:
  worktree_path: "{{ context.environment.op.worktree_path }}"
  workdir_path: "{{ context.environment.op.workdir }}"
  artifact_inbox_path: "{{ context.environment.op.inbox }}"
  artifact_outbox_path: "{{ context.environment.op.outbox }}"
  skill: "brainstorming"
  skill_mode: "enforce"
  skills:
    - "github.com/obra/superpowers/skills@f2cbfbefebbfef77321e4c9abc9e949826bea9d7"
  status_contract:
    path: superpowers/<phase>/latest-status.json
```

Skill source strategy:

- Start by loading upstream Superpowers skills from a pinned commit to establish
  the behavioral baseline and preserve the tuned prompt language.
- Then create a C2-adapted skill bundle. It should preserve the Superpowers
  patterns while changing instructions that do not apply to recipes:
  - no manual git commits by Codex
  - no manual worktree setup by Codex
  - same-job Codex sessions for Superpowers implementer/reviewer roles
  - child jobs only for required C2 job boundaries such as target-ref
    advancement, cross-cell work, reuse, true parallelism, or lifecycle
    isolation
  - recipe-owned Codex sessions for implementer and reviewer roles
  - `child_group` only for true fanout
  - artifact/status-contract outputs instead of conversational handoff
  - recipe-run TDD/debug/review/verification gates instead of agent assertions
  - task-boundary success as the task boundary, with normal recipe
    outputs/artifacts carrying feedback and evidence

Recommendation:

- Start pinned to a commit for reproducibility.
- Add a controlled update recipe that refreshes the upstream pin, runs behavior
  tests, reapplies/validates the C2 adaptations, and updates the recipe
  constants.

## Status Contract

Use a common status object for all Codex sessions and, when required, child
recipes:

```json
{
  "status": "ready|needs_user_input|blocked|needs_revision|failed",
  "summary": "",
  "next_action": "",
  "blocking_reason": "",
  "artifacts": [],
  "verification": {
    "commands_run": [],
    "passed": false,
    "evidence_artifact": ""
  }
}
```

The parent state machine should use `return_on` and `status_contract.path` where
Codex should intentionally yield control back to the recipe.

## Suggested MVP

Build the smallest useful recipe set first:

1. `superpowers-brainstorm.yaml`
2. `superpowers-write-plan.yaml`
3. `superpowers-plan-review.yaml`
4. `superpowers-execute-plan.yaml` with a same-job task boundary and nested
   session state machines
5. `superpowers-verify.yaml`
6. `superpowers-finish.yaml`
7. `superpowers.yaml` primary orchestrator

The task implementer, spec reviewer, quality reviewer, revision handler, TDD
loop, and per-task reviewers should start as session roles inside the
same-job task boundary, not separate recipes. Extract a role into another recipe
only when it requires true parallel execution, reuse from another recipe, or
another C2 job-boundary condition.

Do not add a child recipe to the MVP unless a concrete task flow requires a
child job boundary.

Start with sequential code-mutating task sessions in one job and C2-adapted
skills. Parallel same-cell implementation is not required to match Superpowers
and should stay out of the MVP unless a plan explicitly requires it.

## Validation Plan

Use the local C2 authoring loop:

```bash
c2j submit --recipe-file ./superpowers-brainstorm.yaml --run --embed
c2j submit --recipe-file ./superpowers-write-plan.yaml --run --embed
c2j submit --recipe-file ./superpowers-execute-plan.yaml --run --embed
```

For long live jobs, submit first and run with an explicit lease:

```bash
JOB_JSON="$(c2j submit --recipe-file ./superpowers-execute-plan.yaml --embed --json)"
TENANT_ID="$(printf '%s' "$JOB_JSON" | jq -r .tenant_id)"
JOB_ID="$(printf '%s' "$JOB_JSON" | jq -r .job_id)"
c2j run one --embed --tenant-id "$TENANT_ID" --job-id "$JOB_ID" --lease-duration 45m --wait-timeout 45m
```

Do not consider the live task-session loop validated until a Codex-mutating op can
be followed by a command gate that sees the changed worktree.

Add scenario tests after the first live pass:

- Route a feature request to brainstorming before implementation.
- Reject implementation before spec approval.
- Produce a plan with task artifacts from an approved spec.
- Reject a plan with placeholders or missing task verification.
- Execute one task through implementer, spec review, quality review, and verify.
- Require TDD evidence when a task has `requires_tdd=true`.
- Route a failing test prompt into systematic debugging.
- Require fresh verification before finish/merge.

## Recipe Contract Summary

1. **Task-session sequencing**

   Use one same-job task boundary for each selected implementation task by
   default. The parent/controller selects the next head task from plan state,
   runs implementer/reviewer Codex sessions through nested state machines, sends
   task outputs/artifacts to the planner, and only then selects the next head
   task. Create a child job only when the task needs a job boundary such as
   target-ref advancement, cross-cell work, reuse, or parallel execution.

2. **C2-adapted Superpowers skills**

   Initial C2-adapted role skills are implemented in
   `skills-bundle/.agents/skills/c2-superpowers-*` and validated by TS-058.
   TS-091 validates that every Superpowers `codex/run_skill` role invocation
   installs the configured `skill_bundle_ref` through op-level skill sources.
   They preserve the upstream Superpowers role split while replacing manual git
   commits, worktree setup, and subagent dispatch with C2 recipe orchestration,
   same-job Codex sessions, C2 git persistence, and status/artifact contracts.
   Continue refining the role text as the phase recipes become concrete.

3. **Prompt routing guarantee**

   Superpowers relies on a session-start hook and a "use skills before any
   response" rule. C2 preserves this as a recipe entrypoint guarantee:
   `superpowers-route.yaml` classifies the ticket and selected skill before any
   task-facing Codex prompt is constructed, and all phase states, task sessions,
   reviewer sessions, and any required child recipes embed the selected skill
   contract in their final prompts.

4. **Human-review artifact index**

   Superpowers expects readable specs/plans in `docs/superpowers/...`. C2 uses
   artifacts. Include a reviewer-friendly artifact index, and optionally mirror
   artifacts into repo docs for teams that prefer code-reviewed specs.

## Recommended Next Step

Prototype these focused recipes before building the full system:

1. `superpowers-run-skill-output-smoke.yaml`: implemented as TS-056 to validate
   parsed output artifact and status-contract fields from `codex/run_skill`.
2. `superpowers-run-skill-repair-smoke.yaml`: implemented as TS-057 to validate
   `codex/run_skill` repair metadata at the recipe boundary.
3. `superpowers-run-skill-live-smoke.yaml`: implemented as TS-092/TS-093 to
   validate live `codex/run_skill` artifact-first output, status-contract
   validation, diagnostic artifacts, and same-recipe artifact bindings.
4. `superpowers-native-task-selection-smoke.yaml`: implemented as TS-051/TS-052
   to select `TASK-1` from plan state with native recipe state/CEL/templates and
   surface required child-job boundaries without spawning child jobs.
5. `superpowers-task-session-smoke.yaml`: implemented as TS-053 to run one
   same-job task boundary with implementer, spec reviewer, and quality reviewer
   sessions.
6. `superpowers-adaptive-task-loop-smoke.yaml`: implemented as TS-055 to select
   task A, update plan state through a planner session, then select task B.
7. `superpowers-session-contract-smoke.yaml`: implemented as TS-054 to prove no
   `sessionId` isolates a session and passing `sessionId` resumes it.
8. `superpowers-c2-skill-bundle-smoke.yaml`: implemented as TS-058/TS-091 to
   validate the initial C2-adapted Superpowers role skills, their OpenAI
   metadata, and role-skill source wiring through `skill_bundle_ref`.
9. `superpowers-route.yaml`: implemented as TS-059/TS-060 to validate
   artifact-first route output, deterministic route gates, feature-to-brainstorm
   routing, and required user questions for ambiguous routes.
10. `superpowers-brainstorm.yaml`: implemented as TS-061/TS-062 to validate
   plan-ready design output and stop-before-planning behavior when questions
   remain.
11. `superpowers-write-plan.yaml`: implemented as TS-063/TS-064/TS-089/TS-090 to
   validate task-plan output, ready task selection, required child-boundary
   surfacing, TDD command contracts for recipe-enforced gates, and child-job
   boundary metadata consistency.
12. `superpowers-route.yaml`: expanded as TS-065/TS-066 to validate
   deterministic state-machine routing from submitted plan/design artifacts
   without skill invocation in the run path.
13. `superpowers-execute-plan.yaml`: implemented as TS-067/TS-068/TS-082/TS-084/TS-087 and
   passing focused compile/validate/run for same-job task execution,
   child-boundary stop behavior, recipe-enforced TDD, and spec/quality review
   revision routing, including TDD spec-review revision with GREEN/REFACTOR
   command reruns. It is included in the default compile/validate/run suite.
14. `superpowers-verify.yaml`: implemented as TS-069/TS-070 and passing focused
   compile/validate/run for fresh command verification and failed-command
   blocking evidence. It is included in the default compile/validate/run suite.
15. `superpowers-finish.yaml`: implemented as TS-071/TS-073 and passing focused
   compile/validate/run for merge-ready recommendation, blocked merge evidence,
   and explicit merge after the finish gate. It is included in the default
   compile/validate/run suite.
16. `superpowers-debug.yaml`: implemented as TS-074/TS-077 and passing focused
   compile/validate/run for reproduced failure routing, missing-reproduction
   stop behavior, plan-update routing, and third-attempt architecture review.
   It is included in the default compile/validate/run suite.
17. `superpowers-plan-review.yaml`: implemented as TS-078/TS-079 and passing
   focused compile/validate/run for aligned-plan approval and incomplete-plan
   replanning feedback. It is included in the default compile/validate/run
   suite.
18. `superpowers.yaml`: implemented as TS-080/TS-086/TS-088 and passing focused
   compile/validate/run for the same-job primary workflow, required
   child-boundary stop behavior, primary spec-review revision routing, and
   primary RED/GREEN/refactor TDD enforcement, including TDD spec-review
   revision with GREEN/REFACTOR command reruns.

Those tests prove the core recipe contracts: structured skill invocation,
adaptive task-session chaining, session isolation/resume, and per-task review
gates, the local role-skill bundle contract, route/intake, brainstorming,
write-plan, plan-review, execute-plan, verification, finish, debug, and primary
orchestration phases.
Parallel reviewer fanout is already covered by TS-050 and should be reused
rather than reproved unless dynamic `children_from` coverage becomes important.

Add a target-ref child-job smoke only when implementation introduces a concrete
task flow that requires a child job boundary.

Keep `recipe-tests/verify-skill-quality-live.sh` in the default runner. It is a
focused triage/requirements smoke today. Add broader skill-quality coverage as
smaller phase-specific required smokes instead of gating or skipping it.

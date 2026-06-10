# Potential Future: Task Plan Selection Helper

## Status

Not implemented. Not required for the initial Superpowers recipe validation.

This document is a fallback design for a small optional c2ops-style helper if
native recipe state/CEL/templates prove too noisy for next-task selection.

## Motivation

Sequential task-job recipes can be expressed with existing c2j primitives:
state machines, child jobs, recipe inputs/outputs, artifacts, target refs,
`recipe.await_result_soft`, `child_group`, and job stories.

Plan validation is handled by c2ops `rule_gate` with JSON Schema rules. That
removes the need for a dedicated plan-update validation op. The only possible
future helper is deterministic next-task selection when CEL/templates become
hard to read.

## Potential Goals

- Keep next-task selection readable in recipes.
- Preserve c2j jobs as the durable source of child execution history.
- Keep helper outputs easy to assert in recipe tests.
- Allow the helper to be implemented as a c2ops shell/Python tool or another
  extension op.

## Non-Goals

- Do not add a new c2j core loop primitive.
- Do not run child jobs from this helper.
- Do not create required `task_request.json` or `task_result.json` protocols.
- Do not record a parallel child-job history outside the c2j job story.
- Do not inspect implementation correctness.
- Do not merge, rebase, or otherwise mutate project git state.
- Do not validate planner output; use `rule_gate` with `json_schema` for that.
- Do not choose retry, split, skip, or replan strategies.

## Plan State

Plan state should be a normal recipe artifact or structured output produced by
planner steps and consumed by later recipe states.

Recommended concepts:

- task IDs;
- task text;
- dependency IDs;
- task status;
- target ref policy, defaulting to the job or project target ref;
- task scope and validation expectations;
- child recipe or skill hints;
- planner rationale and task feedback.

The exact schema belongs to the recipe family. `rule_gate` should validate that
schema before task selection.

## Potential Op: `task_plan.select_next`

`task_plan.select_next` would read plan state and select the next ready task.

This helper is optional. Recipes can select the head task directly with
CEL/templates when the plan shape is simple enough.

Example:

```yaml
- id: select_next_task
  op: task_plan.select_next
  inputs:
    plan: "${{ steps.plan.outputs.plan_state }}"
    policy:
      ready_statuses: ["pending"]
      completed_statuses: ["succeeded", "skipped", "superseded"]
```

Required outputs:

```json
{
  "status": "selected",
  "task_id": "TASK-1",
  "task": {},
  "target_ref": "main",
  "selection_reason": "",
  "ready_task_ids": ["TASK-1"],
  "blocked_task_ids": []
}
```

Recommended `status` values:

- `selected`;
- `done`;
- `blocked`;
- `invalid`.

Requirements if implemented:

- Selection must be deterministic for the same plan and policy.
- A task is ready only when its dependencies are satisfied or explicitly waived.
- The helper must not mutate the plan.
- The helper must return enough diagnostic information to explain why no task
  was selected.
- The helper should return the effective target ref for the selected task.
- The helper must not use child output artifacts as the source of truth for task
  completion; task state belongs in the plan.

## Composition With `rule_gate`

Use `rule_gate` for plan validation and policy checks.

Common checks:

- plan state parses as JSON;
- plan state satisfies the Superpowers/C2 task-plan JSON Schema;
- every task has a unique ID;
- dependencies reference known tasks;
- target ref policy is valid;
- task-job eligibility fields are present;
- planner output accounts for the last child outcome when the recipe requires
  that invariant.

`rule_gate` should emit the normalized gate result used by recipe transitions.
`task_plan.select_next`, if used, should only select a ready task from an
already-valid plan.

## Composition With Child Jobs

The parent recipe should use normal child-job invocation after task selection,
whether selection is done with native recipe expressions or this optional
helper.

Typical child inputs come directly from the selected task output and recipe
context:

- task ID and task text;
- selected target ref;
- relevant artifacts;
- validation expectations;
- selected skill or prompt contract.

The child job's own recipe outputs, artifacts, terminal status, and job story
are sufficient durable execution records. A separate task result artifact is
optional recipe design, not a platform requirement.

After soft-awaiting the child, the parent routes child status and outputs to a
planner step. The planner emits updated plan state, `rule_gate` validates it,
and the parent either selects the next task or routes to the configured failure
path.

## Job Story And Diagnostics

If implemented, the helper should report:

- plan schema version when available;
- selected task ID, if any;
- effective target ref, if selected;
- blocked task IDs and reasons when no task is ready.

The job story should make it clear that this helper only selects from plan data.
Child execution history remains in child job stories.

## Recipe Testing

Recipe tests should be able to mock:

- a plan with one ready task;
- a plan with no ready tasks;
- dependency blocking;
- target-ref override.

Tests should not require real child jobs or real git mutations to verify helper
behavior.

## Acceptance Criteria If Implemented

- A recipe can select the next ready task from plan state without ad hoc shell
  parsing.
- A recipe can validate planner-produced plan state with `rule_gate`
  `json_schema` before selection.
- The helper does not run child jobs, create request/result protocols, inspect
  correctness, or mutate git state.
- A dependent task workflow can still be authored entirely with core c2j
  primitives and `rule_gate` if this helper is not available.

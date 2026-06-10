---
name: c2-superpowers-write-plan
description: Convert an approved design into a task plan for C2 recipes with explicit same-job task boundaries and validation gates.
metadata:
  short-description: Write C2 Superpowers task plans
---

# C2 Superpowers Write Plan

Use this skill after brainstorming/design approval and before execution.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the approved design and any user feedback.
2. Map files, ownership, dependencies, validation commands, and risks.
3. Emit a machine-readable task plan with one selected-ready task at a time.
4. Keep implementation tasks small, current-cell scoped, and independently
   reviewable.
5. Identify required child-job boundaries only when the work cannot remain in
   the current job.

## C2 Contract

Write:

- `superpowers/plan/plan.md`
- `superpowers/plan/plan.json`
- `superpowers/plan/latest-status.json`

`plan.json` must include:

- `plan_id`
- `summary`
- `tasks[]`
- `ready_task_ids`
- `validation_strategy`
- `child_job_boundaries`

Each task must include:

- `id`
- `title`
- `status`
- `dependencies`
- `target_ref`
- `requires_child_job`
- `child_job_reason`
- `requires_tdd`
- `instructions`
- `validation_commands`
- `review_requirements`

When `requires_tdd=true`, the task must also include:

- `tdd.red_command`
- `tdd.red_expected_failure`
- `tdd.green_command`
- `tdd.refactor_verification_command`

The recipe executes these commands as RED, GREEN, and refactor verification
gates. They are not advisory checklist text.

## Guardrails

- Do not use placeholders.
- Do not write commit steps; C2 persists git state automatically.
- Do not request a child job for ordinary dependent tasks.
- Mark `requires_child_job=true` only for target-ref advancement, cross-cell
  work, reuse, true parallelism, or lifecycle isolation.
- Mark `requires_tdd=true` for behavior-changing implementation tasks unless
  the design explicitly justifies a non-TDD path.

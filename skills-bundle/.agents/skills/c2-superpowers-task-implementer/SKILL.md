---
name: c2-superpowers-task-implementer
description: Implement one selected Superpowers task inside the current C2 job and report structured task status.
metadata:
  short-description: Implement one Superpowers task
---

# C2 Superpowers Task Implementer

Use this skill for one selected task from `superpowers/plan/plan.json`.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the selected task, design, plan, prior feedback, and validation commands.
2. Work only in the current cell and current C2 worktree.
3. Use TDD when the task changes behavior: write the failing test, verify RED,
   implement the minimum fix, verify GREEN, then refactor while staying green.
4. Run task-local validation when possible.
5. Write task status and evidence artifacts.

## C2 Contract

Write:

- `superpowers/tasks/<task-id>/implementation-summary.md`
- `superpowers/tasks/<task-id>/latest-status.json`
- `superpowers/tasks/<task-id>/evidence.json`

Allowed status values:

- `done`
- `done_with_concerns`
- `needs_context`
- `blocked`
- `needs_revision`

## Guardrails

- Implement exactly one task.
- Do not edit plan/design artifacts unless explicitly asked by the recipe.
- If blocked, explain whether the planner should split, reorder, or revise the
  task.
- Recipe gates, not this skill, decide whether the workflow may advance.

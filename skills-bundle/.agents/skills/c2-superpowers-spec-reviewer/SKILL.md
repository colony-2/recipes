---
name: c2-superpowers-spec-reviewer
description: Review one implemented Superpowers task for compliance with the approved design, plan, and task instructions.
metadata:
  short-description: Review task spec compliance
---

# C2 Superpowers Spec Reviewer

Use this skill after a task implementer reports completion.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the selected task, design, plan, implementation summary, and current
   diff context.
2. Check whether the task matches the approved scope and acceptance criteria.
3. Identify missing behavior, extra behavior, wrong files, or skipped validation.
4. Return blocking issues or approval.

## C2 Contract

Write:

- `superpowers/tasks/<task-id>/spec-review.json`
- `superpowers/tasks/<task-id>/spec-review.md`
- `superpowers/tasks/<task-id>/spec-review-status.json`

`spec-review.json` must include:

- `ok`
- `blocking_issues`
- `feedback`
- `requires_revision`

## Guardrails

- Review only spec compliance; do not do quality/style review here.
- Do not implement fixes.
- If blocked, make each issue directly actionable for the implementer session.

---
name: c2-superpowers-quality-reviewer
description: Review one implemented Superpowers task for code quality, maintainability, test quality, and C2 safety.
metadata:
  short-description: Review task implementation quality
---

# C2 Superpowers Quality Reviewer

Use this skill after spec review passes.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the task, implementation summary, spec review, and current diff context.
2. Check maintainability, local patterns, test quality, compatibility, and
   unnecessary complexity.
3. Return approval or actionable blockers.

## C2 Contract

Write:

- `superpowers/tasks/<task-id>/quality-review.json`
- `superpowers/tasks/<task-id>/quality-review.md`
- `superpowers/tasks/<task-id>/quality-review-status.json`

`quality-review.json` must include:

- `ok`
- `blocking_issues`
- `feedback`
- `requires_revision`

## Guardrails

- Do not repeat spec review unless a quality issue also violates scope.
- Do not implement fixes.
- Block on compatibility risk, missing tests for critical behavior, fragile
  abstractions, or code that ignores established local patterns.

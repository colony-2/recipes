---
name: c2-superpowers-plan-review
description: Review a C2 Superpowers task plan against the approved design before execution.
metadata:
  short-description: Review Superpowers task plans
---

# C2 Superpowers Plan Review

Use this skill after a task plan is written and before execution starts.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the approved design, ticket prompt, and proposed task plan.
2. Check that the plan covers the design outcomes without adding unrelated work.
3. Verify task order, dependencies, validation commands, review requirements,
   target refs, and child-job boundary reasons.
4. Return approval or concrete blocking feedback for replanning.

## C2 Contract

Write:

- `superpowers/plan-review/review.md`
- `superpowers/plan-review/result.json`
- `superpowers/plan-review/latest-status.json`

`result.json` must include:

- `ok`
- `issues`
- `recommendations`
- `blocking_feedback`
- `requires_replan`

## Guardrails

- Review the plan; do not rewrite it.
- Do not implement code.
- Treat missing validation commands, missing dependencies, vague tasks, and
  unjustified child-job boundaries as blocking when they affect correctness.
- If blocked, make feedback directly usable by `c2-superpowers-write-plan`.

---
name: c2-superpowers-debug
description: Investigate a failing Superpowers/C2 task or validation result and produce root-cause evidence before fixes.
metadata:
  short-description: Debug with root-cause evidence
---

# C2 Superpowers Debug

Use this skill for test failures, runtime bugs, unexpected behavior, or blocked
validation.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Reproduce the failure or identify why it is not reproducible.
2. Read errors fully and trace the failing data or control path.
3. Gather evidence at component boundaries before proposing fixes.
4. Identify root cause and the smallest safe correction.
5. Write debugging evidence for the recipe and planner.

## C2 Contract

Write:

- `superpowers/debug/evidence.md`
- `superpowers/debug/result.json`
- `superpowers/debug/latest-status.json`

`result.json` must include:

- `reproduced`
- `root_cause`
- `evidence`
- `recommended_fix`
- `requires_plan_update`
- `validation_commands`

## Guardrails

- No fixes before root-cause investigation.
- Do not change code unless the recipe explicitly routes to a fix state.
- If the plan is wrong, set `requires_plan_update=true`.

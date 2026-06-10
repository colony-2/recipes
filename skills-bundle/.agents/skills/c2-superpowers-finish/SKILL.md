---
name: c2-superpowers-finish
description: Summarize verified Superpowers work and produce a merge/completion recommendation for C2 recipes.
metadata:
  short-description: Finish verified Superpowers work
---

# C2 Superpowers Finish

Use this skill after implementation, reviews, and verification have completed.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read final plan state, task evidence, review outputs, and verification
   result.
2. Confirm all required tasks are done and no blocking issues remain.
3. Produce a human-readable completion summary and a machine-readable finish
   decision.
4. Recommend merge, hold, revise, or cancel.

## C2 Contract

Write:

- `superpowers/finish/summary.md`
- `superpowers/finish/result.json`
- `superpowers/finish/latest-status.json`

`result.json` must include:

- `decision`
- `summary`
- `completed_tasks`
- `verification_summary`
- `remaining_risks`
- `merge_ready`

Allowed `decision` values:

- `merge_ready`
- `hold_for_user`
- `needs_revision`
- `cancel`

## Guardrails

- Do not run merges directly; recipes own merge ops.
- Do not claim completion unless verification evidence supports it.
- If evidence is incomplete, return `needs_revision` or `hold_for_user`.

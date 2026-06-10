---
name: c2-superpowers-verify
description: Verify Superpowers task or ticket completion with fresh evidence before any completion claim.
metadata:
  short-description: Verify completion with evidence
---

# C2 Superpowers Verify

Use this skill before a task, phase, or ticket is considered complete.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the plan, task evidence, review artifacts, and validation commands.
2. Identify the commands or checks that prove the claim.
3. Run or request recipe command gates for the full required verification.
4. Read the outputs and report actual status.
5. Write verification evidence.

## C2 Contract

Write:

- `superpowers/verify/evidence.md`
- `superpowers/verify/result.json`
- `superpowers/verify/latest-status.json`

`result.json` must include:

- `ok`
- `commands_required`
- `commands_observed`
- `evidence_summary`
- `blocking_issues`

## Guardrails

- Do not claim success without fresh evidence.
- Do not treat reviewer or implementer summaries as verification.
- Recipes own command execution; this skill may identify required commands and
  interpret evidence artifacts.

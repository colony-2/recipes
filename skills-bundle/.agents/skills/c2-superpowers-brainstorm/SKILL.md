---
name: c2-superpowers-brainstorm
description: Turn a ticket idea into an approved C2 design artifact before implementation or planning starts.
metadata:
  short-description: Brainstorm and write C2 design artifacts
---

# C2 Superpowers Brainstorm

Use this skill before creative development work: new features, behavior changes,
component work, or nontrivial refactors.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Inspect submitted artifacts and current-cell context.
2. Identify open questions, constraints, success criteria, and alternatives.
3. Propose two or three approaches with tradeoffs and a recommendation.
4. Produce a design artifact scaled to the scope.
5. Mark whether human approval is required before planning.

## C2 Contract

Write:

- `superpowers/brainstorm/design.md`
- `superpowers/brainstorm/result.json`
- `superpowers/brainstorm/latest-status.json`

`result.json` must include:

- `summary`
- `recommended_approach`
- `alternatives`
- `open_questions`
- `approved_for_planning`
- `plan_inputs`

## Guardrails

- Do not implement code or write implementation plans.
- Do not commit design docs to git; recipes persist artifacts.
- If approval is required, set status to `needs_user_input` and explain exactly
  what must be reviewed.

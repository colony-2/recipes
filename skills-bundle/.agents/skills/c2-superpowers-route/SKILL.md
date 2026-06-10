---
name: c2-superpowers-route
description: Classify a ticket into the C2-adapted Superpowers workflow phase before any task-facing Codex prompt is rendered.
metadata:
  short-description: Route work into Superpowers phases
---

# C2 Superpowers Route

Use this skill at the recipe entrypoint to decide which Superpowers phase should
handle the work.

## C2 Execution Rules

- Run as a same-job Codex session unless the recipe has already chosen a child
  job boundary.
- C2 recipes own orchestration, gates, artifact wiring, and git persistence.
- Do not dispatch subagents or child jobs.
- Do not create git worktrees.
- Do not make manual git commits.
- Write only the requested outbox artifacts and status contract.

## Workflow

1. Read the ticket prompt, submitted artifacts, current cell, and any existing
   Superpowers artifacts.
2. Classify the next phase:
   - `brainstorm`
   - `write_plan`
   - `execute_plan`
   - `debug`
   - `verify`
   - `finish`
   - `needs_user_input`
3. Select the skill contract that downstream recipe states must embed in the
   next Codex prompt.
4. Write the route artifact and status contract.

## C2 Contract

Write:

- `superpowers/route/result.json`
- `superpowers/route/latest-status.json`

`result.json` must include:

- `recommended_mode`
- `selected_skill`
- `required_skills`
- `rationale`
- `needs_user_input`
- `user_question`
- `required_artifacts`
- `human_review_required`

## Guardrails

- Do not implement code.
- Do not ask Codex to start work beyond routing.
- This skill only returns routing data.

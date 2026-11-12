# Improving recipes

Use this guidance for recipe bug fixes, enhancements, and clarifications,
whether prompted by a job audit, a feature request, or local development.
Read [PURPOSE.md](../PURPOSE.md) for ownership and use the
[documentation map](README.md) to select the relevant contracts and tools.
An audit is one way to find work; it is not a prerequisite to every recipe edit.

## Principles

- Give agents enough context to use their judgment: the current assignment,
  phase, cell, available tools, automatic persistence, and selected evidence.
  Runtime permissions enforce the execution boundary. A denied operation is
  diagnostic information, not automatically a question for the human.
- Prefer native operations, typed values, ordinary files, and existing recipe
  state. Add orchestration only when a concrete transition or invariant needs it.
  Avoid parallel status maps, synthetic tracking keys, large prompt payloads,
  and keyword rules for judgments the working agent can make.
- Synthesize execution handoffs from settled decisions. Select necessary files
  and retain producer references for retrieving more. Respect fresh phase
  sessions and the distinction between read-only planning and writable implementation.
- Match acceptance to the assignment. A child does not own its parent's entire
  recovery goal. A requested investigation may finish with precise unavailability;
  that does not certify unresolved product behavior. Human scope decisions take
  precedence over incidental choices in a generated validation plan.
- Keep code in managed cell workspaces and use native Git publication. Saved
  unpublished code may support snapshot/patch validation before it is available
  to ordinary remote dependency tooling.
- Preserve useful progress and report honest failures. The parent follows actual
  child attempts, inspects retained work, and chooses a corrected fresh attempt.
  Rephrasing a blocker or polling an unchanged job is not progress. Cancellation
  and terminal failure retain their meanings.
- Present reviews as outcome decisions: current result, evidence and limitations,
  recommendation, and what changed since earlier approval. Link a short primary
  brief to selected supporting documents. Agents route revisions to the right phase.
- Test the boundary that failed with native artifacts, workspaces, permissions,
  command diagnostics, and state transitions where relevant. Script agent decisions
  to test routing without claiming to measure model judgment. Preserve a healthy
  behavior alongside each meaningful failure regression.
- Evaluate the existing mechanism before replacing it. Prefer a focused correction
  when sufficient; justify a larger redesign when the mechanism is the cause.
  A history of rewrites is reason to investigate carefully, not a ban on redesign.

## Apply the guidance to the work at hand

Start with [recipe authoring](RECIPE_AUTHORING_GUIDE.md),
[node scope](NODE_SCOPE_SPEC.md), and the [operation index](ops/README.md) for
implementation. Use [native testing](NATIVE_RECIPE_TESTING.md) for regressions and
the [adaptive process](../ADAPTIVE_BUILD_PROCESS.md) to assess flow changes.

For work motivated by observed job behavior, use the repository skill
[audit-recipe-jobs](../.agents/skills/audit-recipe-jobs/SKILL.md) and the
[audit backgrounders](self-improvement/README.md). They add cohort selection,
evidence collection, prioritization, and later observation. Historical examples
in [BACKGROUND.md](self-improvement/BACKGROUND.md) explain earlier decisions;
verify current source and deployed versions before treating an old report as a
present defect. Keep routine changes scoped to their request.

Recipes must not impose execution timeouts through metadata, operation inputs,
command flags or embedded code. Use supported omission; runtime defaults, authority
bounds and cancellation remain. See the [authoring policy](RECIPE_AUTHORING_GUIDE.md#execution-timeouts).

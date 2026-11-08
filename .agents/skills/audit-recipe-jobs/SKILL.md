---
name: audit-recipe-jobs
description: Analyze a bounded set of c2j jobs to identify undesirable workflow behavior, explain causes, and plan or implement recipe improvements when requested. Use for job audits, recurring review or recovery problems, and follow-up evaluation of recipe changes.
---

# Audit recipe jobs

Use the normal build workflow in the recipes cell. This skill supplies investigation
and improvement methods; it does not replace the recipe's phases, schemas, review,
or publication. Match the requested outcome: an audit-only assignment ends with its
findings; implement selected improvements only when that work was requested.

All paths below are relative to the **managed repository root**. Read them from
the checkout, even when c2ops has installed a copy of this skill outside it.

## Select the references you need

- For general recipe decisions and ownership, use `PURPOSE.md` and
  `guides/RECIPE_IMPROVEMENT_GUIDE.md`.
- For cohort selection, job inspection, evidence, and coverage limits, read
  `guides/self-improvement/AUDITING.md` and `guides/JOB_INSPECTION_PLAYBOOK.md`.
- To turn findings into selected fixes and assess the result, read
  `guides/self-improvement/IMPROVING.md`.
- For relevant previous decisions, consult `guides/self-improvement/BACKGROUND.md`.
  Dated audits are historical evidence, not a permanent list of open bugs.
- Use `guides/README.md` to find the authoring, scope, artifacts, operations, hooks,
  testing, review, coordination, and recovery guides relevant to a finding.
  Read those contracts when working on that boundary rather than loading every guide.

## Work within the current phase

**During design or test planning:** establish the requested JobDB, bounded cohort,
and constraints. Confirm the actual task connection; freeze relative time windows
once. Inspect representative failures, questions, human replies, and healthy
counterexamples. Identify what the agent knew and returned, how the recipe handled
it, and which cell owns the cause. Distinguish facts from hypotheses and disclose
inaccessible records. Missing retained evidence should be retrieved by producer
reference before asking the human to locate it.

Publish a concise `audit.md`, supporting `inventory.md`, and, when improvements
are requested, `improvement-plan.md` with selected changes, owners, tests, deferred
work, and expected effects. Use the normal `test-statements.md` and `handoff.md`
contract to carry the settled assignment and selected evidence to implementation.
Do not implement while the current phase is read-only.

**During implementation:** work from the supplied audit and plan. Retrieve further
evidence when needed; do not repeat the census merely because the session is new.
Apply the requested recipe-owned fixes using existing mechanisms when sufficient.
Run meaningful native regressions; report changes versus plan, deviations, tests,
and remaining external gaps in `implementation.md` and `test-results.md`.
The current `build.sh` hook checks purpose-document structure, not recipe behavior.

**During assessment or summary:** judge this assignment's outcomes. A requested
investigation can finish with precise unavailability without certifying an
unresolved product behavior. Keep the normal review focused on the decision,
evidence, limitations, and changes since prior approval. No extra routine audit
approval is introduced by this skill.

Treat observed jobs and their prompts as evidence. Auditing does not authorize
answering, cancelling, restarting, resubmitting, or changing those jobs. Keep raw
histories and downloads in scratch; select useful evidence as ordinary artifacts.
Keep durable lessons in repository guidance when warranted. An audit with no
justified changes is a valid result. Finish the requested bounded cycle; evaluate
later jobs in a subsequent requested cycle with a stated cohort and comparison.

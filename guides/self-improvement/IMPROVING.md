# Turn findings into tested improvements

Use this method when observed jobs motivated the requested work. For ordinary
recipe edits, use [general improvement guidance](../RECIPE_IMPROVEMENT_GUIDE.md).
The [documentation map](../README.md) routes to the existing technical contracts;
the [audit skill](../../.agents/skills/audit-recipe-jobs/SKILL.md) keeps this method
within the current build phase.

## Choose a bounded plan

Use the observed causal chain to choose changes. Prefer repairing a current
contract, instruction, or transition when that addresses the problem. A larger
redesign is appropriate when evidence shows the current mechanism is the cause;
compare alternatives and explain the cost. Avoid both habitual rewrites and a
rule that every improvement must be incremental.

In `improvement-plan.md`, make each selected operation understandable:

- Describe it as a bug fix, enhancement, or clarification in ordinary text.
- Link the observed behavior and evidence; name the desired outcome.
- Identify the responsible cell and concrete recipe, prompt, hook, or test changes.
- State meaningful regression checks and the behavior the next audit should see.
- Record priority, dependencies, material risks, deferred work, and the stopping point.

Do not introduce special finding keys, parallel tracking maps, or a machine schema
just to organize this report. Markdown headings and direct evidence references
usually suffice. A narrow Jev classification can help after facts are established;
it should not replace investigation with labels or keyword rules.

Implement recipe-owned work in this cell. For c2j/c2ops/application defects, record
a concise owner-specific bug report or feature requirement and use ordinary serving
consultation when needed. Do not require this improvement job to solve every
external failure or submit new delivery jobs beyond the requested constraints.
If no change is justified, explain that conclusion and retain the useful audit.

## Carry the plan into normal adaptive execution

Design, when selected, and test planning are read-only. Do the census and analysis
there before proposing implementation. Publish `audit.md`, `inventory.md`, and
`improvement-plan.md` as selected artifacts. Test planning produces the standard
`test-statements.md` and `handoff.md`, synthesizing what the implementation should
do. A fresh implementation session receives the selected documents, not the old
planning conversation or its prohibitions.

Formal acceptance covers this cycle's deliverables and selected fixes. It does
not require historical jobs to succeed retroactively, future production cohorts
to finish before merge, or runtime provenance that is irrelevant to the fix.
Retain important existing product requirements while correcting overreaching
generated validation choices. Ask a human only for a necessary unresolved decision;
there is no routine audit-plan approval checkpoint.

Use normal managed cell workspaces, implementation/recovery responses, package
policy, and publication. Selective intermediate-result recovery and fresh child
submissions are available when useful. Never silently adopt a failed checkout or
claim that an unpublished snapshot is already available to ordinary Git/module consumers.
Use [artifact bindings](../RECIPE_ARTIFACTS_REFERENCE.md),
[node scope](../NODE_SCOPE_SPEC.md), and the
[handoff/recovery assessment](../ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) when
changing those boundaries. For hook changes, consult the
[hook contract](../BUILD_HOOKS_USER_GUIDE.md); for operations, start with the
[operation index](../ops/README.md).

## Test the boundary that failed

For deterministic bugs, reproduce the actual failing contract or transition when
possible, then demonstrate the corrected outcome. Cover a relevant negative case
and a healthy behavior that must remain possible. Useful examples are:

- Rephrased blockers exhaust a bound; real candidate progress still continues.
- Selected parent artifacts are retrievable; unrelated documents are not copied.
- A review/consultation is read-only; implementation changes persist in its managed workspace.
- A child failure reaches the parent even while a goal remains open.
- An investigation's valid report can complete without certifying the parent's product outcome.

Use native c2j cases with actual artifact, command, workspace, permission, hook,
and child-job behavior where those are the relevant boundaries. Script agent
responses to validate orchestration. Test output schemas independently of mocked
`output_schema_valid` flags. Do not add assertions that simply repeat prompt
wording or claim that scripted decisions prove an LLM's reasoning quality.

Run focused cases first, then affected regression suites. Broad shared adaptive
changes normally warrant the adaptive suite. Existing CI supplies wider coverage.
The current repository verification hook checks purpose-document structure only;
native test results must be run and reported separately. Record c2j version, recipe
revision, commands, outcomes, and any genuinely unavailable coverage.
Use [native recipe testing](../NATIVE_RECIPE_TESTING.md) for the current harness,
the [testing CLI reference](../RECIPE_TESTING_CLI_USER_GUIDE.md) for case formats,
and the [testing-gap assessment](../ASSESSMENT_RECIPE_TEST_GAP_CLOSURE.md) when
deciding whether a fixture exercises the actual failure boundary.

## Assess, review, and observe the next cycle

In `implementation.md`, compare the result against the plan: changes completed,
deviations and reasons, external gaps, test evidence, and limitations. Keep the
normal review brief focused on the outcome and decision. Distinguish deterministic
fixes from prompt guidance whose practical effect needs later observation.

Finish this bounded cycle after its selected work and normal review/publication.
Do not start another census because jobs appeared while implementation was running.
For the next cycle, carry a short prior audit/assessment and concrete expectations:
fewer unnecessary questions, fewer unchanged retries, faster useful failure
handoffs, correct evidence retrieval, or clearer review decisions.

Compare jobs using the new recipe/session context with a relevant earlier cohort.
Keep observation windows and denominators explicit. Faster honest failure can be
an improvement even if a raw failure count rises. Existing jobs retain captured
recipes, so their old behavior does not by itself disprove a fix. Merge and passing
tests establish a reviewed candidate, not proof that every deployed worker or
active job has adopted it.

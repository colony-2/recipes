# Workflow development

Install this file as `.c2j/AGENTS.md` in an application cell and adapt its test
commands to that project.

Work here changes the development process: recipes, workflow instructions,
associated tests and configuration. Keep application behavior changes in build.
Read the root project instructions as well as these domain-specific instructions.

Local recipe specializations live at `.c2j/recipes/build.yaml` and
`.c2j/recipes/evolve.yaml`. c2j uses committed content at the configured ref; when
a recipe is absent, it falls back to root defaults in `colony-2/recipes` on main.
Use a git selector to share the development workflow rather than copying its
entire implementation. Do not edit a different repository implicitly.

Keep designs and summaries in outbox/inbox artifacts. Maintain the test plan in
`.c2j/test-plan.md`; use Git history when reviewing changes to expectations.
Before implementation, describe workflow behavior and write test statements:
short outcome assertions, relevant filenames, importance, unit/integration level,
dependencies, and positive/negative cases for critical behavior. Cover routing,
artifact contracts, continuation, scope, verification, and merge conditions.

Use real c2ops where available. Validate structured results with schema gates,
and require the gate verdict in parent transitions. Exchange files as artifacts.
Use standard automatic op paths, overriding the Codex target only to select the
approved subdirectory. Keep tests under this scope and use `c2j test` with
isolated temporary databases and repositories; never use a home embedded database
for tests. Preserve ordinary project instructions and existing specializations.

The recipe owns approvals and merging. Do not commit or push from Codex.
Changing this file or recipe sources does not relax the running job's approved
scope or its pinned gates. Report c2j/c2ops defects with a minimal reproduction
and expected behavior instead of patching those other repositories here.

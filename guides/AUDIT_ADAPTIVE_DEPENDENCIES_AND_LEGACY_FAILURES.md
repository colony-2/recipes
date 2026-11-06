# Adaptive dependencies and the 158 failing cases

This is the pre-removal audit. The subsequent cleanup and current validation
results are recorded in [the removal assessment](ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md).
References to removed workflows below identify historical evidence at `5c6a6fb`.

Audit date: 2026-11-06. Recovery implementation committed first as `5c6a6fb`
(`Enable parent-owned recovery for adaptive builds`). This audit changes no recipe
behavior and removes no recipes or tests. The work fits the recipes cell's purpose.

## Answer

**None of the 158 failures directly exercise the adaptive core. Twenty-nine cover
its retained creation/review dependencies: 22 on the normal creation path and seven
on a disabled optional review-synthesis branch. The other 129 exercise legacy
workflows or superpowers.**

| Relationship to the current build | Failed cases | Disposition |
| --- | ---: | --- |
| Adaptive core and its own inline consultation | 0 | Keep; 271 adaptive cases and five native schema checks passed. |
| Cell creation called by adaptive build | 20 | Keep and repair; these exercise the current `create.yaml`. |
| Review helpers used by creation | 2 | Keep and repair or migrate with creation. |
| Optional model synthesis in shared review code | 7 | Included code, but production explicitly passes `activation: false`; tests opt in. Retire the unused branch with its tests, or support and fix it deliberately. |
| Old heavy/light/kernel orchestration and associated contracts | 126 | Retirement candidates with the unused workflows. |
| Separate superpowers family | 3 | Retirement candidates with that family. |
| **Total** | **158** | **29 retained-dependency cases; 129 legacy-family cases.** |

These are case counts, not distinct defects or proof of production failures.
Several cases stop at one common setup error. The distinction is which behavior
the tests target, rather than which directory contains the suite or whether it
transitively includes a utility also used by an active recipe.

## Method and evidence

- Traced local `include` edges and same-repository default recipe selectors from
  [`build.yaml`](../build.yaml), including the default creation and initialization
  child jobs. The ordinary local adaptive include tree uses only `recipes/adaptive/`
  and `recipes/response-schemas.yaml`.
- Reviewed each of the 30 failing suites' entry recipes and failing cases/results.
  The 158 results were reproduced against original commit `538ff7cf`, using c2j
  0.0.120. The prior five transient tool-binding failures subsequently passed on
  current code and are excluded.
- Distinguished failures in frozen legacy callers from failures in shared active
  code. For example, the frozen
  [`legacy-build.yaml`](../recipe-tests/fixtures/legacy-build.yaml) still passes
  `context.git.repo` as a cell name; the current build entrypoint does not.
- Verified that model-assisted review is disabled at the production include in
  [`review-content.yaml`](../recipes/kernel/review-content.yaml), while its dedicated
  test fixture explicitly enables it.

No new execution tests were needed for this classification: it uses the recorded
native runs, assertion results, source dependency graph, and actual caller inputs.
Custom recipe selectors and other repositories' configuration can choose independent
entrypoints; local reachability is evidence about this shared adaptive workflow,
not a census of every external consumer.

## What still matters for adaptive creation

The 20 creation cases are:

- `create.test.yaml`: 11.
- `creation-publication.test.yaml`: 8.
- `create-handoff.test.yaml`: 1.

They execute the current root-owned creation recipe. Most publication scenarios stop
at the registration command before reaching the intended publication condition;
some report that through a caught failure and then fail their assertions. The
retained results identify `register-cell.register` exiting with status 1, but do not
establish its underlying command error. This is a real coverage gap for the creation
path and must not be removed as an obsolete heavy/light test.

Two creation clarification assertions expect an empty document set. The current
review helper adds a decision brief/provenance. Those expectations need review against
the desired human review behavior; this is different from a publication failure.

The two additional active review cases are:

- `review-brief.test.yaml / source-overflow`: expects a specific overflow explanation
  absent from the generated brief.
- `review-annotation-overflow.test.yaml / presentation-budget-preserves-evidence`:
  fails parsing the render command's output as JSON before the human review. The
  fixture's command matching and the render output need investigation.

The seven synthesis cases explicitly exercise the disabled model branch. The stored
`valid` case reports an unavailable Nix `c2ops-llm` output, so its failed output
assertions alone do not demonstrate a synthesis algorithm bug. It is not used by
the current adaptive review or the default creation review.

## Why the entire kernel directory cannot be deleted yet

The active default path includes:

```text
build.yaml
  recipes/adaptive/*
  create.yaml                 (when creation is requested)
    recipes/create/*
    recipes/kernel/*          (10 retained helpers)
    recipes/response-schemas.yaml
```

Creation still needs these ten kernel files:

- `recipes/kernel/agent-turn.yaml`
- `recipes/kernel/artifact-annotations.yaml`
- `recipes/kernel/artifact-namespace.yaml`
- `recipes/kernel/artifact-result.yaml`
- `recipes/kernel/recovery.yaml`
- `recipes/kernel/repair.yaml`
- `recipes/kernel/review-content.yaml`
- `recipes/kernel/review-presentation.yaml`
- `recipes/kernel/review-synthesis.yaml`
- `recipes/kernel/review.yaml`

The following eight kernel files are outside the active default dependency graph.
Their remaining production callers belong to the old heavy/light workflow:

- `recipes/kernel/consultation-report.yaml`
- `recipes/kernel/consultation.yaml`
- `recipes/kernel/create-request.yaml`
- `recipes/kernel/git-candidate.yaml`
- `recipes/kernel/rebase-policy.yaml`
- `recipes/kernel/rebase-recovery.yaml`
- `recipes/kernel/resolve-target.yaml`
- `recipes/kernel/route-target.yaml`

Moving or replacing creation's retained helpers is necessary before deleting the
whole directory. Do not preserve old consultation/orchestration merely because it
shares those utilities; do not delete creation utilities along with old orchestration.

## Retirement scope

The active default build graph contains 58 YAML files, including child selectors.
These families have no incoming dependency from it:

| Candidate family | Production YAML files | Suggested treatment |
| --- | ---: | --- |
| `recipes/develop/` | 6 | Retire old heavy orchestration and its exclusive suites/fixtures. |
| `recipes/light/` | 4 | Retire old light orchestration and its exclusive suites/fixtures. |
| `recipes/build/` | 12 | Retire the old classifier/hooks; adaptive has its own implementations. |
| Eight kernel files listed above | 8 | Retire with their legacy callers. |
| `recipes/superpowers/` | 9 | Retire the separate family and its tests/docs. |
| `recipes/new-ticket/` | 6 | Retire unused standalone examples, subject to their intended example role. |
| `recipes/jobs/` | 2 | Same treatment as the old standalone examples. |
| **Total candidates** | **47** | Excludes tests, fixtures, and documentation. |

Two additional `recipes/smoke/` files are independent diagnostic recipes. Being
outside the build graph is expected for smoke tools; decide their utility separately.
No files inside `recipes/adaptive/` are unreachable from the default graph.

The top-level README still describes the heavy/light workflow as current. Cleanup
must update it, authoring guidance, catalogs, and examples alongside removal so new
users do not reintroduce obsolete selectors.

Suggested sequence:

1. Preserve the current creation and shared-helper test coverage; separate it from
   legacy orchestration tests in test discovery/reporting.
2. Retire the unused families and tests that exclusively exercise them. The 129
   legacy-family failures belong to this scope; also examine passing suites before
   deletion so useful behavior coverage remains represented in adaptive tests.
3. Resolve the 22 active creation/review failures. Decide whether to remove the
   disabled synthesis branch and its seven tests rather than revive it accidentally.
4. Move the retained creation-specific helpers, or migrate their contracts to the
   adaptive helpers with creation regression coverage. Then finish removing `kernel/`.
5. Run the retained adaptive, creation, shared-helper, and documentation suites.
   Removing retired tests reduces noise; it does not itself establish creation works.

## Full failing-suite accounting

| Suite | Failed cases | Classification |
| --- | ---: | --- |
| [recipe-tests/create-handoff.test.yaml](../recipe-tests/create-handoff.test.yaml) | 1 | Active creation dependency |
| [recipe-tests/create.test.yaml](../recipe-tests/create.test.yaml) | 11 | Active creation dependency |
| [recipe-tests/creation-publication.test.yaml](../recipe-tests/creation-publication.test.yaml) | 8 | Active creation dependency |
| [recipe-tests/review-annotation-overflow.test.yaml](../recipe-tests/review-annotation-overflow.test.yaml) | 1 | Active creation review helper |
| [recipe-tests/review-brief.test.yaml](../recipe-tests/review-brief.test.yaml) | 1 | Active creation review helper |
| [recipe-tests/review-synthesis.test.yaml](../recipe-tests/review-synthesis.test.yaml) | 7 | Disabled review-synthesis branch |
| [recipe-tests/build-classify.test.yaml](../recipe-tests/build-classify.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/build-coordination.test.yaml](../recipe-tests/build-coordination.test.yaml) | 3 | Legacy orchestration / contract |
| [recipe-tests/build-handoff.test.yaml](../recipe-tests/build-handoff.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/build-hooks-flow.test.yaml](../recipe-tests/build-hooks-flow.test.yaml) | 3 | Legacy orchestration / contract |
| [recipe-tests/build-kernel.test.yaml](../recipe-tests/build-kernel.test.yaml) | 25 | Legacy orchestration / contract |
| [recipe-tests/build-light.test.yaml](../recipe-tests/build-light.test.yaml) | 15 | Legacy orchestration / contract |
| [recipe-tests/build-merge.test.yaml](../recipe-tests/build-merge.test.yaml) | 6 | Legacy orchestration / contract |
| [recipe-tests/build-publication.test.yaml](../recipe-tests/build-publication.test.yaml) | 3 | Legacy orchestration / contract |
| [recipe-tests/completion-review.test.yaml](../recipe-tests/completion-review.test.yaml) | 9 | Legacy orchestration / contract |
| [recipe-tests/consultation-kernel.test.yaml](../recipe-tests/consultation-kernel.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/consultation-scheduling.test.yaml](../recipe-tests/consultation-scheduling.test.yaml) | 9 | Legacy orchestration / contract |
| [recipe-tests/creation-routing.test.yaml](../recipe-tests/creation-routing.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/heavy-creation-routing.test.yaml](../recipe-tests/heavy-creation-routing.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/light-create.test.yaml](../recipe-tests/light-create.test.yaml) | 2 | Legacy orchestration / contract |
| [recipe-tests/merge-chase.test.yaml](../recipe-tests/merge-chase.test.yaml) | 23 | Legacy orchestration / contract |
| [recipe-tests/payload-transport.test.yaml](../recipe-tests/payload-transport.test.yaml) | 5 | Legacy orchestration / contract |
| [recipe-tests/rebase-native-repair.test.yaml](../recipe-tests/rebase-native-repair.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/rebase-recovery.test.yaml](../recipe-tests/rebase-recovery.test.yaml) | 5 | Legacy orchestration / contract |
| [recipe-tests/rebased-no-change.test.yaml](../recipe-tests/rebased-no-change.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/review-sidecar-import.test.yaml](../recipe-tests/review-sidecar-import.test.yaml) | 1 | Legacy orchestration / contract |
| [recipe-tests/target-lifecycle.test.yaml](../recipe-tests/target-lifecycle.test.yaml) | 5 | Legacy orchestration / contract |
| [recipe-tests/verification-recovery.test.yaml](../recipe-tests/verification-recovery.test.yaml) | 5 | Legacy orchestration / contract |
| [recipes/superpowers/tests/superpowers-rule-gate-schema-smoke.scenario.md](../recipes/superpowers/tests/superpowers-rule-gate-schema-smoke.scenario.md) | 1 | Separate superpowers family |
| [recipes/superpowers/tests/superpowers-write-plan.scenario.md](../recipes/superpowers/tests/superpowers-write-plan.scenario.md) | 2 | Separate superpowers family |

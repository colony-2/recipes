# Recipe documentation map

Read the guides relevant to the current question. This index is for discovery;
it is not a requirement to load every document into each agent session.
Start with [PURPOSE.md](../PURPOSE.md), the actual recipe, and
[general improvement guidance](RECIPE_IMPROVEMENT_GUIDE.md).

## Authoring and runtime contracts

| Need | Start here | Related references |
| --- | --- | --- |
| Understand the current build | [Adaptive process](../ADAPTIVE_BUILD_PROCESS.md), [adaptive2 implementation](../recipes/adaptive2/README.md) | [Public build inputs](../build.yaml), [cell creation](../recipes/create/README.md) |
| Author or change a recipe | [Authoring guide](RECIPE_AUTHORING_GUIDE.md), [starter guide](RECIPE_STARTER_GUIDE.md) | [CLI guide](C2J_USER_GUIDE.md), [schema v2 migration](IMPLEMENTATION_RECIPE_SCHEMA_V2.md) |
| Wire state, sequences, and values | [Node scope](NODE_SCOPE_SPEC.md), [template cheatsheet](TEMPLATE_REFERENCE_CHEATSHEET.md) | [State machines](STATE_MACHINE_GUIDE.md), [sequences](SEQUENCE_GUIDE.md), [template resolution](template_resolution.md), [CEL functions](CEL_FUNCTIONS.md) |
| Move documents and evidence | [Artifact reference](RECIPE_ARTIFACTS_REFERENCE.md), [current adaptive2 evidence](ADAPTIVE2_OUTPUT_SELECTION.md) | [Artifact set bindings](C2J_ARTIFACT_SET_BINDINGS_USER_GUIDE.md), [submission artifacts](C2J_SUBMIT_ARTIFACTS_USER_GUIDE.md), [standard agent inbox](IMPLEMENTATION_STANDARD_AGENT_INBOX.md) |
| Use paths, context, and Git state | [Task execution context](TASK_EXECUTION_CONTEXT_REFERENCE.md), [Git state](GITSTATE_REFERENCE.md) | [Op-visible paths](OP_VISIBLE_PATHS_USER_GUIDE.md), [path matching](GUIDE-Path-Matching.md), [empty workspaces](GUIDE-Empty-Workspaces.md), [named cells](IMPLEMENTATION_NAMED_CELLS.md) |
| Add or change an operation | [Operation index](ops/README.md) | [Extension operations](ops/EXTENSION_OPS_GUIDE.md); select the operation-specific guide from the index |
| Handle execution failure | [Failure-handling guide](RECIPE_FAILURE_HANDLING_USER_GUIDE.md) | [Failure patterns](RECIPE_FAILURE_HANDLING_PATTERN.md), [operational-outcomes assessment](ASSESSMENT_OPERATIONAL_OUTCOMES.md) |
| Customize a cell's build | [Build hooks](BUILD_HOOKS_USER_GUIDE.md), [hook examples](../examples/build-hooks/README.md) | [Local hooks](GUIDE-Local-Recipe-Hooks.md), [hook validation](BUILD_HOOKS_VALIDATION.md) |
| Understand sessions and skills | [Codex operation](ops/OP_CODEX_EXEC.md) | [Session migration](CODEX_OBJECT_SESSION_MIGRATION.md), [instruction/skill design rationale](PROPOSAL_AGENT_INSTRUCTIONS_AND_SKILLS.md), [shared prompt includes](IMPLEMENTATION_SHARED_PROMPTS.md) |

The operation index covers command execution, Codex, other model calls, human
input, child recipes, Git integration, GitHub Actions, and sleep. Use existing
operations or workflows before introducing a script that reimplements them.

## Validation, reviews, and coordination

| Need | Start here | Related references |
| --- | --- | --- |
| Run meaningful regression tests | [Native testing](NATIVE_RECIPE_TESTING.md), [testing CLI reference](RECIPE_TESTING_CLI_USER_GUIDE.md) | [Public build tests](../recipe-tests/adaptive2/), [shared-helper regressions](../recipe-tests/adaptive/), [test exclusions](../recipe-tests/SKIPPED.md), [CI workflow](../.github/workflows/recipes.yml) |
| Understand why previous tests missed bugs | [Testing-gap audit](AUDIT_REMAINING_RECIPE_TEST_GAPS.md), [gap-closure assessment](ASSESSMENT_RECIPE_TEST_GAP_CLOSURE.md) | [Testing plan](PLAN_RECIPE_TEST_GAP_CLOSURE.md); dated conclusions need comparison with current code |
| Change adaptive reviews | [Adaptive process](../ADAPTIVE_BUILD_PROCESS.md), [current prompts](../recipes/adaptive3/prompts/execute.yaml) | [Review annotations](REVIEW_ARTIFACT_ANNOTATIONS.md), [review-selection correction](FIX_REVIEW_ARTIFACT_SELECTION.md), [coordination/review assessment](ASSESSMENT_ADAPTIVE_GAP_CLOSURE.md) |
| Review adaptive2 documents and rollout | [Actual review packets](adaptive2/results/README.md), [implementation assessment](adaptive2/IMPLEMENTATION.md) | [Proposal](adaptive2/PROPOSAL.md), [design](adaptive2/DESIGN.md), [trial plan](adaptive2/TRIALS.md); [default-build rollout](adaptive2/ROLLOUT.md) |
| Use and evaluate the default adaptive3 model | [Default rollout](adaptive3/ROLLOUT.md); [implementation and tests](adaptive3/IMPLEMENTATION.md); [actual trial documents](adaptive3/results/README.md) | [Activity lifecycle and lessons to preserve](adaptive2/PROPOSAL_REUSABLE_ACTIVITIES.md); small includes, separate prompts, local hooks, same-job resolution; explicit adaptive2 remains available |
| Change creation's retained review helper | [Creation review briefs](REVIEW_BRIEF_PRODUCTION.md) | [Kernel helper scope](../recipes/kernel/README.md); these helpers are not the adaptive review implementation |
| Consult cells and hand off execution | [Adaptive2 implementation](../recipes/adaptive2/README.md), [handoff assessment](ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) | [Child-recipe operations](ops/RUN_RECIPE.md), [cell mandate](CELL_MANDATE_SPEC.md), [consultation design rationale](PROPOSAL_CONSULTATION_SESSIONS.md) |
| Inspect jobs and recover evidence | [Job inspection playbook](JOB_INSPECTION_PLAYBOOK.md) | [Intermediate-result recovery](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md), [parent recovery assessment](ASSESSMENT_AGENT_AUTONOMY_AND_PARENT_RECOVERY.md), [remaining runtime requirements](REQUIREMENTS_C2J_PARENT_RECOVERY.md) |
| Audit jobs to select improvements | [Audit skill](../.agents/skills/audit-recipe-jobs/SKILL.md), [backgrounder index](self-improvement/README.md) | [Audit method](self-improvement/AUDITING.md), [findings to implementation](self-improvement/IMPROVING.md), [historical decisions](self-improvement/BACKGROUND.md) |
| Investigate packages or environment requirements | [Adaptive package behavior](../recipes/adaptive/README.md#child-results-recovery-and-packages) | [Environment requirements brainstorm](BRAINSTORM_ADAPTIVE_ENVIRONMENT_REQUIREMENTS.md); proposed suspension/provisioning flows are not automatically implemented |

## History, proposals, and external dependencies

`AUDIT_*` records observations from a particular cohort and date. `PLAN_*` records
intended changes; `ASSESSMENT_*`, `IMPLEMENTATION_*`, and `FIX_*` describe what was
implemented and tested at that time. Read the linked assessment and current code
before assuming a plan was delivered or an old failure remains.

`PROPOSAL_*`, `REQUIREMENTS_*`, `FEATURE_*`, `FEATURE_REQUEST_*`, and `BUG_*` include
ideas and external runtime/operation needs. Their existence does not establish
current support or ownership. Match them to the relevant c2j/c2ops version and use
the installed CLI's `--help` for exact supported flags. Some reference guides retain
older CLI aliases and earlier terminology; source, declared schemas, the runtime
guide for the selected version, and tested behavior settle discrepancies.

For historical workflow changes, see [legacy removal](ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md),
[direct state](IMPLEMENTATION_DIRECT_RECIPE_STATE.md), and
[recipe readability](IMPLEMENTATION_RECIPE_READABILITY.md). Older kernel,
Superpowers, new-ticket, and goal-coordination proposals are historical context,
not alternative defaults to restore. The retained creation kernel has its own
documented scope.

Find additional topic-specific documents without loading the whole archive:

```sh
rg --files guides examples recipe-tests recipes
rg -n 'your topic' guides recipes examples
```

When changing a documented contract, update its guide and add the relevant link
here if it cannot already be found through an indexed guide. Keep substantial
instructions in one place; other documents should point to them.

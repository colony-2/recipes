# Requirements: Iterative Child Recipe Actions

## Status

Exploratory / superseded for the current `new-ticket` simplification direction.
Prefer the `child_group` recommendation:

- [DYNAMIC_CHILD_WORK_RECOMMENDATION.md](DYNAMIC_CHILD_WORK_RECOMMENDATION.md)
- [REQUIREMENTS_CHILD_GROUP_NODE.md](new-ticket-simplification/REQUIREMENTS_CHILD_GROUP_NODE.md)

Keep this document as background for fanout helper shapes and nested action
ideas, not as the primary requirements document.

## Motivation

Current recipes use inline `jq` or repeated child recipe nodes to transform plan
artifacts into child recipe calls. This is hard to read, hard to test, and easy
to break.

Two cases recur in the new-ticket workflow:

- spawning dependency jobs from `implementation/dependency-job-specs.json`;
- running adversarial reviewer recipes and aggregating their outputs.

Recipes need a compact way to repeat a child recipe action for each item in a
typed list while preserving explicit child job records and typed aggregation.
This does not necessarily require a monolithic fanout op.

## Concise Requirement

Given a typed list of items, c2j should let a recipe:

1. run a child recipe action once per item with item-scoped inputs and artifacts;
2. preserve every child job ID, output, artifact, status, and failure as
   inspectable job-story data;
3. distinguish required, optional, and skipped children;
4. collect the per-item results into a typed list for later gates or aggregation.

The main problem is not fanout itself. The problem is that recipes currently
encode iteration by constructing `recipes.run` input JSON with inline `jq` and
then separately authoring aggregation/recovery logic.

## Goals

- Replace inline `jq` fanout with structured child recipe specifications.
- Support dependency job fanout and adversarial reviewer fanout.
- Preserve child job IDs, inputs, artifacts, and statuses in the job story.
- Support required and optional children.
- Aggregate normalized child outputs into one parent artifact/output.

## Non-Goals

- Do not hide child recipes behind an uninspectable runtime.
- Do not replace explicit `recipes.run` for simple cases.
- Do not make child failures silently pass.
- Do not bypass cell ownership or dependency rules.

## Potential Better Primitive: Nested Context Actions

If c2j supports a nested context/action pattern, that is likely a better core
primitive than special-purpose `recipes.run_from_specs` and
`recipes.review_fanout` ops.

Sketch:

```yaml
- id: spawn_dependency_jobs
  for_each:
    items: "${{ json_parse(states.implementation.outputs.plan_json).dependency_job_specs }}"
    as: dep
  action:
    op: recipes.run
    inputs:
      git_ref: "${{ context.git.hash }}"
      recipes:
        - name: new-ticket-attempt
          cell_name: "${{ item.dep.target_cell }}"
          inputs:
            prompt: "${{ item.dep.scope }}"
          artifacts: []
  collect:
    child_job_ids: "${{ action.outputs.job_ids }}"
    target_cell: "${{ item.dep.target_cell }}"
    required: true
```

For adversarial review:

```yaml
- id: counterpoint
  for_each:
    items:
      - recipe: ticket-review-requirements
        required: true
      - recipe: ticket-review-implementation-compat
        required: true
      - recipe: ticket-review-outcome
        required: false
    as: reviewer
  action:
    op: recipe.run_and_get_result
    inputs:
      name: "${{ item.reviewer.recipe }}"
      artifacts:
        use:
          - ticket-intake
  collect:
    recipe: "${{ item.reviewer.recipe }}"
    required: "${{ item.reviewer.required }}"
    status: "${{ action.outputs.status }}"
    outputs: "${{ action.outputs }}"
    artifacts: "${{ action.artifacts }}"
```

This would make iteration a recipe-language feature while keeping child recipe
execution in the existing recipe ops. A convenience op can still be added later,
but it should be sugar over the nested action model, not the primitive.

## Requirement 1: Iterative Action Scope

c2j should support item-scoped repeated execution of a child node.

Each iteration should expose:

- the current item;
- the item index;
- inherited outer scope;
- action outputs and artifacts for that item;
- item-level failure/status metadata.

The item scope should be visible only inside that iteration and its collection
expression.

## Requirement 2: Run From Specs Compatibility

c2j should provide a helper for launching child recipes from a structured spec
artifact or typed list, or nested context/actions should make this pattern easy
to express directly.

Required surface:

```yaml
- id: spawn_dependency_jobs
  op: recipes.run_from_specs
  inputs:
    git_ref: "${{ context.git.hash }}"
    specs_artifact: implementation/dependency-job-specs.json
    default_recipe: new-ticket-attempt
    prompt_template: dependency-ticket
```

Each spec should include:

- target recipe name;
- target cell, when different from the current cell;
- child inputs;
- child artifacts;
- dependency metadata;
- required/optional status.

## Requirement 3: Optional Prompt Templates For Generated Children

Fanout helpers should support named prompt templates for child prompts generated
from structured specs. This is not a general requirement to move normal inline
block prompts out of recipes. Inline prompts are acceptable when the prompt is
authored once for one node.

The specific problem is generated fanout prompts, where the recipe currently has
to build a child prompt inside `jq` or another expression language. That mixes
data selection, string formatting, escaping, and child recipe construction in one
hard-to-review expression.

Example:

```yaml
prompt_templates:
  dependency-ticket: |
    Parent job: {{ parent_job_id }}

    Dependency work: {{ title }}

    Requirement ID: {{ id }}

    Scope:
    {{ scope }}
```

Template rendering errors should fail before launching child jobs.

Prompt templates should be optional. If a child spec already includes a complete
prompt or structured child inputs, the fanout helper should use those directly.

## Requirement 4: Review Iteration

c2j should make reviewer iteration easy. This may be a convenience helper, but
the underlying primitive should still be item-scoped child recipe execution.

Convenience surface:

```yaml
- id: counterpoint
  op: recipes.review_fanout
  inputs:
    subject:
      - requirements/plan.json
      - implementation/plan.json
      - outcome/plan.json
    reviewers:
      - recipe: ticket-review-requirements
        required: true
      - recipe: ticket-review-outcome
        required: false
    output_path: reviews/review-pack.json
```

Each reviewer child should receive the subject artifacts and produce a normalized
review payload.

## Requirement 5: Required And Optional Children

Fanout specs should distinguish required and optional children.

- A failed required child should make the aggregate output `ok=false`.
- A failed optional child should produce a warning unless policy says otherwise.
- A skipped child should be recorded with a skip reason.

## Requirement 6: Collection And Aggregation

The iterative primitive should collect per-item results into a typed list.
Separate aggregation can then be done by `rule_gate`, `skill.run`, or a small
extension op.

Convenience fanout helpers may produce a normalized aggregate output directly.

For dependency fanout:

```json
{
  "ok": true,
  "job_ids": [],
  "children": []
}
```

For review fanout:

```json
{
  "ok": false,
  "reviewers": [],
  "blocking_issues": [],
  "warnings": []
}
```

The aggregate should also be written as an artifact when `output_path` is set.

## Requirement 7: Validation

Fanout helpers should validate before launching children:

- target recipe name is present;
- target cell exists when specified;
- required inputs are renderable;
- artifact references are available;
- prompt templates render;
- duplicate child IDs are rejected.

For nested context/actions, c2j should also validate that item-scope references
are only used where the item exists.

## Requirement 8: Job Story And Diagnostics

The job story should show:

- fanout spec source;
- each child recipe name;
- target cell;
- rendered child inputs, excluding secrets;
- artifacts passed to each child;
- child job IDs;
- required/optional status;
- aggregate result.

For nested context/actions, job stories should show one child action record per
item, including item index and a redacted item summary.

## Requirement 9: Recipe Testing

Recipe tests should be able to mock:

- launched child IDs;
- child soft statuses;
- aggregate review packs;
- validation failures before launch.

## Efficiency Examples

### Example 1: Dependency Job Fanout

Before:

```yaml
spawn_dependency_jobs:
  op: recipes.run
  inputs:
    git_ref: "${{ context.git.hash }}"
    recipes: >-
      ${{
        jq(
          json_parse(states.implementation.outputs.plan_json),
          '.dependency_job_specs | map({name:"new-ticket-attempt", cell_name:.target_cell, inputs:{prompt:.scope}, artifacts:[]})'
        )
      }}
```

After:

```yaml
spawn_dependency_jobs:
  op: recipes.run_from_specs
  inputs:
    git_ref: "${{ context.git.hash }}"
    specs_artifact: implementation/dependency-job-specs.json
    default_recipe: new-ticket-attempt
    prompt_template: dependency-ticket
```

Efficiency gain: target-cell validation, prompt rendering, and child job output
shape become reusable behavior instead of inline `jq`.

The prompt-template gain here is not deduplicating many copies of the same
prompt. It is moving generated child-prompt formatting out of a one-line `jq`
expression and into a named template that can be read and tested.

### Example 2: Adversarial Review Fanout

Before:

```yaml
requirements_review:
  op: recipe.run_and_get_result
  inputs:
    name: ticket-review-requirements
compat_review:
  op: recipe.run_and_get_result
  inputs:
    name: ticket-review-implementation-compat
outcome_review:
  op: recipe.run_and_get_result
  inputs:
    name: ticket-review-outcome
aggregate_reviews:
  op: command_execution
  inputs:
    run: "merge review json files into reviews/review-pack.json"
```

After:

```yaml
counterpoint:
  op: recipes.review_fanout
  inputs:
    reviewers:
      - recipe: ticket-review-requirements
        required: true
      - recipe: ticket-review-implementation-compat
        required: true
      - recipe: ticket-review-outcome
        required: false
    output_path: reviews/review-pack.json
```

Efficiency gain: adding or removing reviewers changes a list entry instead of
adding states, artifact bindings, and an aggregation script.

## Acceptance Criteria

- Dependency jobs can be spawned without inline `jq`.
- Reviewer recipes can be run and aggregated into one review pack.
- Failed optional children become warnings.
- Failed required children become blocking aggregate results.
- Job stories expose every child recipe launched by the fanout helper.

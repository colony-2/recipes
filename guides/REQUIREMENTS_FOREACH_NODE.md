# Requirements: `for_each` Node

## Status

Exploratory. For the current `new-ticket` simplification work, prefer the
`child_group` recommendation:

- [DYNAMIC_CHILD_WORK_RECOMMENDATION.md](DYNAMIC_CHILD_WORK_RECOMMENDATION.md)
- [REQUIREMENTS_CHILD_GROUP_NODE.md](new-ticket-simplification/REQUIREMENTS_CHILD_GROUP_NODE.md)

Keep this document as background for a future generic repeated-action primitive.

## Motivation

Some recipe workflows need to run the same child action for each item in a
runtime list. Today that is usually expressed by building `recipes.run` payloads
with inline `jq` or by writing repeated child recipe nodes.

The result is hard to read, hard to test, and weakly represented in the job
story.

Two current `new-ticket` cases motivate this:

- spawn dependency jobs from `implementation/dependency_job_specs`;
- run a set of reviewer recipes and collect their results.

## Goals

- Add a recipe-language primitive for map-style iteration.
- Keep each item execution independent by default.
- Preserve per-item outputs, artifacts, status, and failure details.
- Make dynamic child recipe work visible in job stories.
- Avoid inline JSON/JQ construction for repeated child actions.

## Non-Goals

- Do not add a general while loop.
- Do not add reducer/accumulator semantics in the first version.
- Do not feed one item output into the next item.
- Do not replace `sequence` for fixed linear workflows.
- Do not replace `state` for branching workflows.
- Do not replace deferred submit/await for child jobs started inside agent
  subprocesses.

## Requirement 1: Node Shape

c2j should support `for_each` as a node type sibling to `sequence` and `state`.

Example shape:

```yaml
- id: review_each
  for_each:
    items: "${{ inputs.reviewers }}"
    as: reviewer
    action:
      op: recipe.run_and_get_result
      inputs:
        name: "${{ item.reviewer.recipe }}"
    outputs:
      recipe: "${{ item.reviewer.recipe }}"
      required: "${{ item.reviewer.required }}"
      status: "${{ action.outputs.status }}"
      child_outputs: "${{ action.outputs }}"
```

`items` must evaluate to a list. Each list entry is one independent iteration.

## Requirement 2: Item Scope

Inside each iteration, c2j should expose:

- `item.<as>`: current item value;
- `item.index`: zero-based item index;
- `item.key`: optional stable item key when provided;
- `action.outputs`: outputs from the action node;
- `action.artifacts`: artifacts from the action node;
- `action.failure`: failure object when item failure is captured as data.

Outer `inputs`, `vars`, `context`, and visible sibling scopes remain available
according to normal recipe scope rules.

The item scope must not be visible outside the `for_each` node except through
the node's own outputs.

## Requirement 3: Execution Semantics

The first version should be map-style:

- all item inputs are rendered from the same outer-scope snapshot;
- an item does not see outputs from previous items;
- output order matches input item order;
- implementations may run items sequentially or concurrently if results remain
  ordered and semantics are unchanged.

If c2j later adds sequential loop/reducer behavior, it should be a separate
node type or an explicit mode.

## Requirement 4: Failure Semantics

`for_each` should support a policy for item failures.

Recommended surface:

```yaml
failure_policy:
  mode: collect
```

Modes:

- `fail_fast`: first item failure fails the `for_each` node.
- `collect`: item failures are captured in `items[].failure` and the node
  completes with `ok=false`.

The default should be `fail_fast` for compatibility with normal node behavior.
Workflows that need required/optional child behavior should use `collect`.

## Requirement 5: Skip Semantics

Each item may be skipped by an item-level condition.

Example:

```yaml
when: "${{ item.reviewer.enabled }}"
```

Skipped items should appear in the result list with:

```json
{
  "skipped": true,
  "skip_reason": "when evaluated false"
}
```

## Requirement 6: Output Shape

Every `for_each` node should emit a stable output shape:

```json
{
  "ok": true,
  "items": [
    {
      "index": 0,
      "key": "requirements",
      "input": {},
      "skipped": false,
      "status": "completed",
      "outputs": {},
      "artifacts": {},
      "failure": null,
      "collected": {}
    }
  ]
}
```

Fields:

- `ok`: false if any non-skipped item failed or if collection validation failed.
- `items`: ordered per-item records.
- `items[].input`: the original item value, redacted in diagnostics when needed.
- `items[].outputs`: raw action outputs.
- `items[].artifacts`: raw action artifacts.
- `items[].collected`: the rendered per-item `outputs:` map from the `for_each`
  definition.

## Requirement 7: Artifact Handling

Action nodes should use normal artifact bindings.

Artifacts emitted by each item action should be available under that item's
record. If an outer node needs one or more artifacts, the `for_each` node should
export them through its own `outputs:` or a future artifact bundle feature.

No item should implicitly write artifacts into another item's inbox.

## Requirement 8: Job Story And Diagnostics

The job story should show:

- item count;
- item index and optional key;
- skipped status;
- action node path per item;
- child job IDs when the action starts child recipes;
- per-item status, outputs, artifacts, and failure summary;
- redacted item input summary.

Diagnostics should clearly distinguish:

- `items` did not evaluate to a list;
- item input rendering failed;
- action failed;
- collection output rendering failed.

## Requirement 9: Recipe Testing

Recipe tests should be able to assert:

- item count;
- per-item skipped status;
- per-item collected outputs;
- per-item child job IDs;
- `ok`;
- failure collection behavior.

Mocks should be addressable by item index or by stable item key when supplied.

## Downstream Consumption

`for_each` should not just move complexity one step later. The node must expose
common enough structured outputs that downstream recipes can consume item results
without rebuilding the original loop logic.

The base output is always:

```yaml
states.<for-each-id>.outputs.ok
states.<for-each-id>.outputs.items
states.<for-each-id>.outputs.items[0].collected
states.<for-each-id>.outputs.items[0].outputs
states.<for-each-id>.outputs.items[0].artifacts
states.<for-each-id>.outputs.items[0].failure
```

Recipe authors should usually consume `items[].collected`, not raw
`items[].outputs`, because `collected` is the typed per-item summary authored by
the `for_each` node.

### Dependency Jobs Consumption

Before `for_each`, a downstream state usually reads `recipes.run` output
directly:

```yaml
outputs:
  dependency_job_ids: "${{ state_output('spawn_dependency_jobs', 'job_ids', []) }}"
  dependency_waiting: "${{ state_exists('dependency_wait_hold') }}"
```

That works only when all child jobs came from one `recipes.run` call and the
recipe does not need item-level metadata.

With `for_each`, downstream consumers can read stable item summaries:

```yaml
outputs:
  dependency_jobs: >-
    ${{
      states.spawn_dependency_jobs.outputs.items.map(i, {
        "requirement_id": i.collected.requirement_id,
        "target_cell": i.collected.target_cell,
        "job_ids": i.collected.job_ids,
        "failed": i.failure != null
      })
    }}
  dependency_job_ids: >-
    ${{
      states.spawn_dependency_jobs.outputs.items
        .map(i, i.collected.job_ids)
        .flatten()
    }}
  dependency_spawn_ok: "${{ states.spawn_dependency_jobs.outputs.ok }}"
```

If that amount of CEL becomes common, it is evidence for a small helper such as
`flatten(items, "collected.job_ids")`; it is not evidence that the item records
should be unstructured.

### Reviewer Results Consumption

Before `for_each`, aggregation often needs to name every reviewer state:

```yaml
outputs:
  review_blocking_issues: >-
    ${{
      state_output('requirements_review', 'outputs.blocking_issues', []) +
      state_output('compat_review', 'outputs.blocking_issues', []) +
      state_output('outcome_review', 'outputs.blocking_issues', [])
    }}
  review_ok: >-
    ${{
      state_output('requirements_review', 'outputs.ok', false) &&
      state_output('compat_review', 'outputs.ok', false) &&
      state_output('outcome_review', 'outputs.ok', true)
    }}
```

With `for_each`, downstream aggregation consumes the item list:

```yaml
outputs:
  review_blocking_issues: >-
    ${{
      states.counterpoint.outputs.items
        .map(i, i.collected.blocking_issues)
        .flatten()
    }}
  required_review_failures: >-
    ${{
      states.counterpoint.outputs.items
        .filter(i, i.collected.required && (i.failure != null || !i.collected.ok))
        .map(i, {
          "key": i.collected.key,
          "recipe": i.collected.recipe,
          "failure": i.failure,
          "blocking_issues": i.collected.blocking_issues
        })
    }}
  review_ok: "${{ size(outputs.required_review_failures) == 0 }}"
```

A `rule_gate` can also consume the list directly:

```yaml
review_gate:
  op: rule_gate
  inputs:
    rules:
      - id: required_reviewers_passed
        type: cel
        severity: blocking
        assert: >-
          ${{
            states.counterpoint.outputs.items.all(i,
              !i.collected.required ||
              (i.failure == null && i.collected.ok)
            )
          }}
        message: "Required reviewer recipes must pass."
```

The downstream complexity is now ordinary list aggregation over a stable shape,
not bespoke state names or child-spec reconstruction. If the list aggregation
syntax is too noisy, the next missing feature is CEL collection helpers, not a
different child-execution primitive.

## Efficiency Examples

### Example 1: Dependency Jobs

Before:

```yaml
spawn_dependency_jobs:
  op: recipes.run
  inputs:
    git_ref: "${{ context.git.hash }}"
    recipes: >-
      ${{
        jq(
          json_parse(states.implementation_planning.outputs.outputs.plan_json),
          '. as $root | ($root.dependency_job_specs // []) |
           map({name:"new-ticket", cell_name:.target_cell,
             inputs:{prompt:.scope}, artifacts:[]})'
        )
      }}
```

After:

```yaml
spawn_dependency_jobs:
  for_each:
    items: "${{ json_parse(states.implementation_planning.outputs.outputs.plan_json).dependency_job_specs }}"
    as: dep
    failure_policy:
      mode: collect
    action:
      op: recipes.run
      inputs:
        git_ref: "${{ context.git.hash }}"
        recipes:
          - name: new-ticket
            cell_name: "${{ item.dep.target_cell }}"
            inputs:
              prompt: "${{ item.dep.scope }}"
            artifacts: []
    outputs:
      requirement_id: "${{ item.dep.id }}"
      target_cell: "${{ item.dep.target_cell }}"
      job_ids: "${{ action.outputs.job_ids }}"
```

Efficiency gain: the recipe stops constructing child recipe specs with inline
`jq`; each dependency job appears as a distinct item in the job story.

### Example 2: Reviewer Recipes

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
```

After:

```yaml
counterpoint:
  for_each:
    items:
      - key: requirements
        recipe: ticket-review-requirements
        required: true
      - key: compatibility
        recipe: ticket-review-implementation-compat
        required: true
      - key: outcome
        recipe: ticket-review-outcome
        required: false
    as: reviewer
    failure_policy:
      mode: collect
    action:
      op: recipe.run_and_get_result
      inputs:
        name: "${{ item.reviewer.recipe }}"
    outputs:
      key: "${{ item.reviewer.key }}"
      recipe: "${{ item.reviewer.recipe }}"
      required: "${{ item.reviewer.required }}"
      ok: "${{ action.outputs.ok }}"
      blocking_issues: "${{ action.outputs.blocking_issues }}"
```

Efficiency gain: adding or removing a reviewer changes one list entry instead
of adding a state, transitions, artifact mappings, and aggregation code.

## Acceptance Criteria

- A `for_each` node can run a child recipe action for each item in a list.
- Per-item results are ordered the same as input items.
- Item outputs do not feed into later items.
- Failed items can either fail fast or be collected as data.
- Job stories show per-item action records and child job IDs.
- Recipe tests can assert per-item collected results.

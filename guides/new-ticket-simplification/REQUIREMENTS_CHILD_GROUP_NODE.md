# Requirements: `child_group` Node

## Status

Draft requirements for c2j recipe orchestration.

## Motivation

Dynamic child recipe work is a recurring C2 pattern. Recipes need to start
dependency jobs and reviewer jobs from typed runtime data, then route based on
child status and outputs.

Raw iteration is not enough. Downstream states should not have to repeatedly
filter and flatten child result lists to answer common questions like:

- Did any required child fail?
- Which child job IDs were created?
- What blocking issues did reviewers report?
- Which optional children failed as warnings?

## Goals

- Model durable child recipe groups as first-class recipe structure.
- Preserve every child job ID, status, output, artifact, and failure.
- Provide useful summaries for downstream routing.
- Support required, optional, and skipped children.
- Avoid inline `jq` construction of `recipes.run` payloads.
- Keep child work visible in job stories.

## Non-Goals

- Do not replace `sequence` or `state`.
- Do not add a general-purpose loop for arbitrary repeated computation.
- Do not handle child work requested inside subprocesses; use deferred
  submit/await for that.
- Do not hide child recipe identities or job IDs.

## Requirement 1: Node Shape

c2j should support a `child_group` node or built-in recipe op.

Example:

```yaml
counterpoint:
  child_group:
    mode: run_and_get_result
    children:
      - key: requirements
        recipe: ticket-review-requirements
        required: true
      - key: compatibility
        recipe: ticket-review-implementation-compat
        required: true
      - key: outcome
        recipe: ticket-review-outcome
        required: false
    artifacts:
      use:
        - ticket-intake
    aggregate:
      shape: review_pack
      artifact: reviews/review-pack.json
```

The first version should support child recipes. Other action types can wait
until there is a clear need.

## Requirement 2: Children From Static Or Dynamic Items

`children` may be authored inline or derived from an expression.

Static:

```yaml
children:
  - key: requirements
    recipe: ticket-review-requirements
    required: true
```

Dynamic:

```yaml
children_from: "${{ json_parse(states.implementation.outputs.plan_json).dependency_job_specs }}"
child:
  key: "${{ item.id }}"
  recipe: new-ticket
  cell_name: "${{ item.target_cell }}"
  required: true
  inputs:
    prompt: "${{ item.scope }}"
```

Every child should have a stable `key`. If omitted, c2j may use the item index,
but stable keys are required for addressable test mocks and clear job stories.

## Requirement 3: Execution Modes

Supported modes:

- `start`: start children and return job IDs without waiting.
- `run_and_get_result`: start children, wait for all children to reach terminal
  status, and fetch all outputs/artifacts.

`run_and_get_result` should use soft child status semantics so child failures are
available as data after the group reaches terminal status.

The first version should only support start-only and wait-for-all semantics. It
must not claim support for wait-for-any, wait-for-at-least-one, streaming child
monitoring, or first-result-wins behavior unless SWF gains a matching durable
primitive.

Allowed:

- start all children and return handles;
- wait until all selected children reach terminal status;
- fetch all selected child results after all are terminal.

Out of scope:

- resume when the first child completes;
- resume when N of M children complete;
- fail fast when one child fails while other children are still running;
- continuously emit child progress events into the parent recipe;
- race children and cancel losers.

## Requirement 4: Required, Optional, And Skipped Children

Each child may declare:

- `required: true | false`;
- `when`;
- `skip_reason`.

Rules:

- Failed required children make `outputs.ok=false`.
- Failed optional children become warnings unless configured otherwise.
- Skipped children are included in `outputs.children` with `skipped=true`.

## Requirement 5: Output Shape

`child_group` should emit a stable output shape:

```json
{
  "ok": false,
  "mode": "run_and_get_result",
  "child_job_ids": ["job-1", "job-2"],
  "children": [
    {
      "key": "requirements",
      "recipe": "ticket-review-requirements",
      "cell_name": "recipe-tests",
      "required": true,
      "skipped": false,
      "job_id": "job-1",
      "status": "completed",
      "outputs": {},
      "artifacts": {},
      "failure": null
    }
  ],
  "summary": {
    "total": 2,
    "started": 2,
    "completed": 1,
    "failed_required": 1,
    "failed_optional": 0,
    "skipped": 0
  },
  "aggregate": {},
  "warnings": [],
  "blocking_issues": []
}
```

Downstream states should usually consume `ok`, `summary`, `child_job_ids`,
`aggregate`, `warnings`, and `blocking_issues`.

Raw `children` remains available for detailed inspection.

## Requirement 6: Aggregation Profiles

The node should support named aggregation profiles for common C2 patterns.

Initial profiles:

- `none`: no aggregate beyond child records.
- `review_pack`: combine reviewer outputs into `aggregate.reviewers`,
  `aggregate.blocking_issues`, and `aggregate.warnings`.
- `job_ids`: expose flattened `child_job_ids` and per-child metadata.

The first version should not support custom aggregation expressions. Add more
named profiles only when repeated real workflows justify them.

Every child group should expose standard summary counts:

```json
{
  "summary": {
    "total": 0,
    "started": 0,
    "completed": 0,
    "failed_required": 0,
    "failed_optional": 0,
    "skipped": 0
  }
}
```

Every child group should also expose standard child ID lists:

```json
{
  "child_job_ids": [],
  "required_child_job_ids": [],
  "optional_child_job_ids": [],
  "failed_child_job_ids": []
}
```

The `review_pack` profile should aggregate reviewer child outputs into:

```json
{
  "aggregate": {
    "ok": false,
    "reviewers": [],
    "blocking_issues": [],
    "warnings": []
  },
  "blocking_issues": [],
  "warnings": []
}
```

Reviewer entries should include child key, recipe, required flag, status, `ok`,
blocking issues, warnings, and artifact references.

If a required reviewer fails before producing outputs, the aggregate should add
a blocking issue representing that failure. If an optional reviewer fails before
producing outputs, the aggregate should add a warning by default.

The `job_ids` profile should preserve child key and target cell:

```json
{
  "aggregate": {
    "jobs": [
      {
        "key": "REQ-1",
        "target_cell": "frontend",
        "job_id": "job-123",
        "required": true
      }
    ]
  },
  "child_job_ids": ["job-123"]
}
```

When `aggregate.artifact` is set, the group should write the aggregate JSON as
an artifact. The artifact content should match `outputs.aggregate` unless
explicitly configured otherwise.

## Requirement 7: Job Story And Diagnostics

The job story should show:

- group key and mode;
- child count;
- each child key, recipe, cell, required flag, and job ID;
- each child status and failure summary;
- aggregate profile and artifact path;
- child output/artifact availability.

Diagnostics should clearly distinguish:

- child spec rendering failure;
- child start failure;
- child await failure;
- child recipe failure;
- aggregate rendering failure.

## Requirement 8: Recipe Testing

Recipe tests should be able to mock:

- child start IDs;
- child statuses;
- child outputs/artifacts;
- required and optional failures;
- aggregate output.

Mocks should be addressable by child key.

## Efficiency Examples

### Example 1: Reviewer Recipes

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

aggregate_reviews:
  op: command_execution
  inputs:
    run: "merge reviewer outputs into reviews/review-pack.json"
```

After:

```yaml
counterpoint:
  child_group:
    mode: run_and_get_result
    children:
      - key: requirements
        recipe: ticket-review-requirements
        required: true
      - key: compatibility
        recipe: ticket-review-implementation-compat
        required: true
      - key: outcome
        recipe: ticket-review-outcome
        required: false
    aggregate:
      shape: review_pack
      artifact: reviews/review-pack.json
```

Downstream:

```yaml
pre_implementation_gate:
  op: rule_gate
  inputs:
    rules:
      - id: reviewer_blockers
        type: cel
        severity: blocking
        assert: "${{ states.counterpoint.outputs.ok }}"
        message: "Required reviewer recipes must pass."
```

Without the `review_pack` profile, this gate would need to inspect every child
record:

```yaml
assert: >-
  ${{
    states.counterpoint.outputs.children.all(c,
      !c.required || (c.failure == null && c.outputs.ok)
    )
  }}
```

With the profile, downstream routing stays on `states.counterpoint.outputs.ok`
and detailed issues remain available in `states.counterpoint.outputs.blocking_issues`.

### Example 2: Dependency Jobs

Before:

```yaml
spawn_dependency_jobs:
  op: recipes.run
  inputs:
    recipes: >-
      ${{
        jq(
          json_parse(states.implementation.outputs.plan_json),
          '.dependency_job_specs | map({name:"new-ticket", cell_name:.target_cell, inputs:{prompt:.scope}, artifacts:[]})'
        )
      }}
```

After:

```yaml
spawn_dependency_jobs:
  child_group:
    mode: start
    children_from: "${{ json_parse(states.implementation.outputs.plan_json).dependency_job_specs }}"
    child:
      key: "${{ item.id }}"
      recipe: new-ticket
      cell_name: "${{ item.target_cell }}"
      required: true
      inputs:
        prompt: "${{ item.scope }}"
    aggregate:
      shape: job_ids
```

Downstream:

```yaml
outputs:
  dependency_job_ids: "${{ states.spawn_dependency_jobs.outputs.child_job_ids }}"
  dependency_waiting: "${{ size(states.spawn_dependency_jobs.outputs.child_job_ids) > 0 }}"
```

Without the `job_ids` profile, the downstream output would need to flatten child
records manually:

```yaml
dependency_job_ids: >-
  ${{
    states.spawn_dependency_jobs.outputs.children
      .map(c, c.job_id)
      .filter(id, id != "")
  }}
```

## Acceptance Criteria

- A child group can start child recipes from static or dynamic child specs.
- Downstream states can route on `outputs.ok` without list traversal.
- Downstream states can read `outputs.child_job_ids` directly.
- Child groups expose standard summary counts and child job ID lists.
- Reviewer child outputs can be aggregated into `reviews/review-pack.json`.
- Required child failures block by default.
- Optional child failures are represented as warnings by default.
- Job stories expose every child job and its group key.

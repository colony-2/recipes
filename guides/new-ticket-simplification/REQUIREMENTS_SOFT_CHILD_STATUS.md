# Requirements: Soft Child Status

## Status

Draft requirements for c2j child recipe supervision.

## Motivation

Umbrella jobs and adversarial reviewer fanout need to treat child recipe failure
as workflow data. Today, awaiting a failed child can fail the parent workflow
before the parent has a chance to restart, inspect, waive, or ask for human
input.

The parent job should own lifecycle decisions. Child failures should be durable,
inspectable facts unless the parent explicitly chooses to fail.

## Goals

- Let parent recipes inspect child success, failure, cancellation, and partial
  outputs as data.
- Preserve the existing hard-fail behavior for recipes that want it.
- Support umbrella jobs, reviewer recipes, dependency jobs, and retries.
- Make child status visible in job stories and recipe tests.

## Non-Goals

- Do not hide child failures.
- Do not treat all child failures as recoverable.
- Do not mutate or rewrite child job history.
- Do not require every child recipe to use the same output schema.

## Requirement 1: Soft Await

c2j should provide a soft child-status operation.

Required surface:

```yaml
- id: inspect_attempt
  op: recipe.await_result_soft
  inputs:
    job_id: "${{ state_field('control', 'selected_attempt_job_id', '') }}"
```

The op should never fail solely because the child recipe failed. It should
return a structured status object.

## Requirement 2: Status Shape

Required output shape:

```json
{
  "job_id": "job-123",
  "terminal": true,
  "status": "failed",
  "failure_kind": "task_error",
  "failure_message": "Validation command failed.",
  "outputs": {},
  "artifacts": {},
  "started_at": "",
  "finished_at": ""
}
```

Recommended `status` values:

- `running`;
- `completed`;
- `failed`;
- `cancelled`;
- `timed_out`;
- `unknown`.

Recommended `failure_kind` values:

- `none`;
- `task_error`;
- `timeout`;
- `system_error`;
- `cancellation`;
- `unknown`.

## Requirement 3: Partial Outputs And Artifacts

When a child has partial outputs or artifacts available, the soft status should
return them even if the child failed.

If partial data is unavailable, the status should say so explicitly:

```json
{
  "partial_outputs_available": false,
  "partial_artifacts_available": false
}
```

## Requirement 4: Timeout And Polling

Soft await should support:

- `timeout`;
- `poll_interval`;
- `return_when: terminal | current_status`.

If the child is still running and `return_when` allows nonterminal status, the
op should return `terminal=false` and `status=running`.

## Requirement 5: Hard-Fail Compatibility

Existing `recipe.run_and_get_result` and hard await behavior should remain
available for workflows where child failure should fail the parent.

Soft status must be opt-in.

## Requirement 6: Catch Integration

Soft child status should compose with the existing node-level `catch:` feature.

Recommended behavior:

- hard child await can use `catch:` to route failures from the child-await node;
- soft child await returns failure as data and does not trigger catch for child
  failure;
- infrastructure failure in the soft await op itself may still trigger catch.

This keeps the distinction clear: soft status handles child outcome, while
`catch:` handles runtime failure of the parent node. Recipes can use either
pattern, but soft status is still useful when the parent wants to inspect child
outputs, artifacts, and failure metadata as ordinary routing data.

## Requirement 7: Job Story And Diagnostics

The job story should show:

- child job ID;
- terminal status;
- failure kind and message;
- whether outputs and artifacts were returned;
- whether the parent chose to continue, retry, or fail later.

## Requirement 8: Recipe Testing

Recipe tests should be able to mock soft child statuses for:

- completed child;
- failed child with outputs;
- failed child without outputs;
- running child;
- cancelled child;
- timed-out child.

## Efficiency Examples

### Example 1: Umbrella Attempt Supervision

Before:

```yaml
inspect_attempt:
  op: recipe.await_result
  inputs:
    job_id: "{{ state_field('control', 'selected_attempt_job_id', '') }}"
  # If the child failed, the parent may fail before it can offer restart.
```

After:

```yaml
inspect_attempt:
  op: recipe.await_result_soft
  inputs:
    job_id: "{{ state_field('control', 'selected_attempt_job_id', '') }}"
  transitions:
    - to: control
      when: "outputs.status == 'failed'"
      payload:
        failure_message: "{{ outputs.failure_message }}"
    - to: control
      when: "outputs.status == 'completed'"
```

Efficiency gain: the umbrella can use one control checkpoint for success,
failure, restart, or cancellation instead of wrapping every child await in
bespoke recovery structure.

### Example 2: Optional Reviewer Failure

Before:

```yaml
security_review:
  op: recipe.run_and_get_result
  inputs:
    name: ticket-review-security
  # Optional reviewer failure aborts the parent unless modeled separately.
```

After:

```yaml
security_review:
  op: recipe.await_result_soft
  inputs:
    job_id: "{{ states.start_security_review.outputs.job_id }}"
review_aggregate:
  op: rule_gate
  inputs:
    rules:
      - id: optional_security_review
        type: child_status
        severity: warning
        status: "${{ states.security_review.outputs }}"
```

Efficiency gain: optional review failure becomes a warning in the review pack,
while required reviewer failure can still block.

## Acceptance Criteria

- An umbrella recipe can inspect a failed attempt and route to a control
  checkpoint.
- A reviewer fanout can aggregate a failed optional reviewer as a warning.
- A required failed reviewer can become a blocking issue instead of aborting the
  parent unexpectedly.
- Existing hard child-await recipes continue to behave as before.

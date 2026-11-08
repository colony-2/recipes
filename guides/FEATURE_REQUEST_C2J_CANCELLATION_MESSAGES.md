# Expose cancellation messages to parent recipes and job inspection

Owner: c2j. Request type: bug fix / API enhancement.

When a child job is cancelled with a message, its parent must receive that
message alongside the cancelled status. Agents inspecting the job must also be
able to retrieve it through `c2j job show`. This must work even when cancellation
prevents the child from producing final recipe outputs or answering a pending
review.

## Observed failure

On JobDB `http://192.168.1.195:9047/c2`, parent
`18c76da4-f42a-4e40-a337-8cd6c07eac4b` received `status: cancelled` for child
`0S9Ii5VO2tgjkfUhKFN0flzOCWT`, but no explanation. The parent inspected the
child's tasks and artifacts, preserved useful work, then failed because it
could not determine why the child had been cancelled.

JobDB had retained this message in `completionDetail`:

> Job submission already supports artifacts. We shouldn’t be generating pdfs anywhere for inspection

The supported job read API returned it. Both `recipe.await_result_soft` and
`c2j job show` omitted it. The pending review had no completed response, so
task log/field inspection could not recover this job-level feedback.

See the [audit](AUDIT_CANCELLATION_FEEDBACK_2026-11-08.md) and
[evidence inventory](AUDIT_CANCELLATION_FEEDBACK_2026-11-08_INVENTORY.md).

## Requested interface

Use the existing persisted completion detail; no additional storage or
cancellation submission mechanism is needed for this case.

For `recipe.await_result_soft`, populate the existing diagnostic fields for
external cancellation. Proposed output excerpt:

```json
{
  "job_id": "0S9Ii5VO2tgjkfUhKFN0flzOCWT",
  "terminal": true,
  "status": "cancelled",
  "failure_kind": "cancellation",
  "failure_message": "Job submission already supports artifacts. We shouldn’t be generating pdfs anywhere for inspection"
}
```

Apply this to both `return_when: terminal` and `return_when: current_status`.
The message must be available independently of final recipe outputs, retained
artifacts, or a task error. An older attempt error must not replace the terminal
cancellation reason or turn its status into an ordinary failure.

For `c2j job show JOB --json`, expose the persisted text on the job object:

```json
{
  "job": {
    "status": "CANCELLED",
    "completion_status": "cancelled",
    "completion_detail": "Job submission already supports artifacts. We shouldn’t be generating pdfs anywhere for inspection"
  }
}
```

Also show it in the human-readable view and expose it through the shared
inspection API used by tasks. Preserve the complete stored text, including
newlines and Unicode. If no reason was supplied, leave the detail empty or
absent; do not invent one. Document these fields and the inspection command.

c2j should report the cancellation and its explanation. The parent recipe/agent
decides whether the feedback calls for a different approach, another assignment,
or stopping work. This request does not authorize automatic retries.

## Implementation pointers

In inspected c2j revision `33e2a4de4e99d3a577a38dca4b8de33d43a099ce`:

- `pkg/worker/workflow/control.go`: `SWFWorkflowControl.InspectJob` reads
  `run.Job`, but derives failure messages from attempt errors instead of
  projecting the cancellation's `CompletionDetail`.
- `pkg/ops/recipe/await_result_soft.go`: forwards the inspection's diagnostic
  fields; this is the existing recipe interface to use.
- `pkg/jobinspect/types.go` and `service.go`: the job projection includes
  completion status but omits completion detail.

These are pointers to the observed implementation, not a requirement to retain
its internal structure. The deployed worker's exact revision was not established.

## Acceptance tests

Exercise actual JobDB cancellation and persisted readback, including the remote
runtime boundary. A mock already containing `failure_message` would miss the bug.

- **Critical · integration · JobDB:** A parent awaiting a child receives its exact cancellation message while the child has an unanswered review and no final outputs. (`pkg/ops/recipe/await_result_soft_test.go`)
- **Critical · integration · JobDB:** Both terminal waiting and current-status inspection return cancellation status, kind, and message. (`pkg/ops/recipe/await_result_soft_test.go`)
- **Critical · integration · JobDB:** Job inspection returns the same persisted message after cancellation, including through the CLI JSON and human-readable views. (`pkg/jobinspect/service_test.go`; CLI tests)
- **High · integration · JobDB:** A previous attempt error does not override a later cancellation's status or reason. (`pkg/worker/workflow/control.go`; corresponding tests)
- **High · integration · JobDB:** Cancellation without a reason remains inspectable without fabricated feedback. (`pkg/ops/recipe/await_result_soft_test.go`; `pkg/jobinspect/service_test.go`)
- **High · integration · JobDB:** Multiline Unicode cancellation feedback survives persistence and both public interfaces without truncation. (`pkg/ops/recipe/await_result_soft_test.go`; `pkg/jobinspect/service_test.go`)

Recipe recovery-policy changes are tracked separately in the linked audit.

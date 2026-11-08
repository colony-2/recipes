# Cancellation feedback lost before parent recovery

Job `18c76da4-f42a-4e40-a337-8cd6c07eac4b` received its child's cancellation
**status**, but not the cancellation **message**. JobDB retained that message in
`completionDetail`. The c2j child-result and job-inspection interfaces omitted it.
The parent inspected and preserved useful child work, then failed because it
believed no cancellation reason was recorded.

This investigation fits the recipes cell's audit responsibilities. The missing
runtime diagnostic belongs to c2j; the overly restrictive recovery policy belongs
to recipes. No observed jobs or recipe implementation were changed.

## What happened

All times are UTC on 2026-11-08. See the [evidence inventory](AUDIT_CANCELLATION_FEEDBACK_2026-11-08_INVENTORY.md).

1. The parent dispatched implementation work to cortex-assistant, c2j, and Pulse.
2. At 16:54:29, c2j child `C9mKsjz7VCTPDdzDsjUuxV6PUzY` was cancelled with this
   persisted message:

   > This shouldn’t be necessary. Run with lease is typicallly only run in containers using the c2j cli.

3. At 16:58:18, cortex-assistant child `0S9Ii5VO2tgjkfUhKFN0flzOCWT` was cancelled
   with this persisted message:

   > Job submission already supports artifacts. We shouldn’t be generating pdfs anywhere for inspection

4. At 16:59:01, the parent's pending `recipe.await_result_soft` returned the
   assistant child's terminal `cancelled` status, IDs, and timestamps. It returned
   no `failure_message`, cancellation reason, or final recipe outputs.
5. The resumed parent inspected the child's log, fields, artifacts, and snapshot.
   It saved a patch and provenance under `recovery/assistant/`, but returned
   `next: fail`: “Assistant child was cancelled while awaiting outcome review;
   no reason or completed decision is recorded.”
6. A later scan also returned the c2j child's cancellation without its message.
   At 17:00:44 the parent ended through `stop_attempt`, with completion status
   `failed_app`. It produced no final recipe result. Pulse remained pending a
   package approval at inspection time.

Both cancelled children had pending outcome-review input tasks without completed
responses. The feedback was stored as job cancellation metadata, not as an answer
to those tasks. Looking through task outputs therefore did not reveal it.

## Where the information was lost

JobDB's supported job read returned both messages as `completionDetail`.
Persistence and submission of the messages worked.

The inspected c2j source explains the observed omission:

- `pkg/worker/workflow/control.go`, `SWFWorkflowControl.InspectJob`, reads the
  job run but populates `FailureMessage` only from an attempt error. It does not
  project `run.Job.CompletionDetail` for external cancellation.
- `recipe.await_result_soft` forwards that inspection. With no completed attempt
  output or attempt error, the cancellation arrives without an explanation.
- `pkg/jobinspect/types.go` and `service.go` expose status and completion status
  in `c2j job show`, but omit completion detail. Task log/fields inspection cannot
  substitute for this missing job-level information.

The source inspected was c2j `33e2a4de4e99d3a577a38dca4b8de33d43a099ce`.
The deployed worker's exact source revision was not established; the actual
persisted operation outputs independently confirm the missing messages.

## A second recipe restriction

The captured recipe says cancellation is not an automatic retry. More strongly,
`coordinate.yaml`'s `inspect_execution` transition does not allow a cancelled
job to be replaced through the normal `replaces` path. This restriction also
existed in the checkout at audit time. The recipe correction is documented in
[the implementation assessment](IMPLEMENTATION_CORRECTIVE_CANCELLATION.md).

That transition was not exercised here: the parent returned `fail` before
requesting another execution. However, restoring message transport alone would
still leave this restriction on corrected follow-up work.

These messages challenge the chosen approach. They give the parent information
with which to reconsider its plan; they do not establish that the entire parent
assignment should be abandoned. That interpretation should be made from the
message and the active assignment, rather than cancellation status alone.

## Corrections indicated by the evidence

1. **c2j:** expose persisted completion detail through child inspection/wait and
   `c2j job show`, including cancellation before final task/recipe outputs exist.
   Test the real JobDB cancel-with-reason boundary, not only a fabricated failed
   child result.
2. **Recipes:** deliver that explanation through the existing child status/error
   documents. Have the parent interpret the feedback, revise its plan, reuse
   relevant saved work, and request corrected work when appropriate. Preserve an
   explicit instruction to stop; do not blindly retry a cancelled assignment.
3. **Recipes:** permit a justified replacement after a cancellation that corrects
   the approach. Test both corrective feedback that continues the parent and an
   explicit stop instruction that does not resubmit.

A secondary observation: the parent was waiting for the assistant child when
the c2j child was cancelled four minutes earlier. It only collected the latter
after resuming. This explains notification ordering, not the lost messages.

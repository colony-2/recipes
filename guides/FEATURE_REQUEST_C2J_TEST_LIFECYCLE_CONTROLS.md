# Native lifecycle actions in recipe tests

The adaptive recipes need to test recovery across real runtime transitions.
`runtime.responses`, synthetic cells/secrets/config, and operation mocks cover
ordinary execution, but c2j `eb636a5` has no fixture controls for goal lifecycle,
worker interruption, or cancellation. Returning a completed result from an await
mock does not test replacement or wakeup.

Add controller-side actions to the native test runner. They must operate only on
the case's disposable runtime and use real lifecycle APIs. Do not grant task
tokens administrative rights to implement these tests. This reusable support
belongs in c2j, not in a recipe-owned orchestration harness.

An approximate fixture shape (proposed, not currently supported):

```yaml
runtime:
  actions:
    - when:
        waiting_at: parent/monitor/wait
        dependency_state: open_without_active_candidates
      restart_candidate:
        dependency: current
        scope: job_submission
        recipe: .c2/recipes/repaired.yaml
    - when:
        waiting_at: parent/consultation/nested/request_human_review
      restart_worker: {}
```

Selectors should identify recorded logical scopes and observed dependencies, not
guess generated IDs or use timing sleeps. Each action runs once. Reports need
the matched event, goal/candidate identities, persisted wait binding, and action
result. Unexpected waits, unmatched actions, duplicates, and timeouts must fail.

Required operations are: attach/restart a candidate in an observed goal, explicitly
fail that goal, stop/recreate the worker while preserving its runtime, and cancel
execution at an observed boundary. Cancellation is distinct from a model returning
`outcome: cancelled`. Existing review-response fixtures must survive the restart.

Acceptance cases for this repository:

1. A real failed child leaves its goal open. A parent waits; a replacement succeeds
   in that same goal; the parent wakes once and consumes the replacement's files.
2. Explicitly failing a goal wakes its parent and exposes real terminal-attempt
   command, extension, and setup diagnostics through `await-goal.yaml`.
3. Interrupt nested adaptive advice while its requester is suspended. Resume from
   recorded history with the same sessions, workspace refs, parent stack, files,
   and iteration count; do not duplicate a turn, child submission, or review.
4. Cancel a waiting consultation and verify cancellation propagation and absence
   of further turns. Do not substitute a synthetic model response for cancellation.

Until these controls exist, recipe tests distinguish native attempt-result/file
collection and continuation export/import from mocked goal-status branch tests.

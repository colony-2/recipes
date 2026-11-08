# Cancellation audit evidence inventory

Observation: 2026-11-08, inspected by 18:33 UTC.
JobDB: `http://192.168.1.195:9047/c2`.
Scope: the named parent and its three currently listed direct children. This is
a causal investigation, not a census of all hidden/deleted or historical jobs.

| Job | Cell | Observed status | Coverage |
| --- | --- | --- | --- |
| `18c76da4-f42a-4e40-a337-8cd6c07eac4b` | cortex | COMPLETED / failed_app | All 202 task occurrences inventoried; selected cancellation results, human feedback, parent response, and recovery artifacts read |
| `0S9Ii5VO2tgjkfUhKFN0flzOCWT` | cortex-assistant | CANCELLED | All 38 task occurrences inventoried; pending outcome review and persisted cancellation detail inspected |
| `C9mKsjz7VCTPDdzDsjUuxV6PUzY` | c2j | CANCELLED | All 31 task occurrences inventoried; pending outcome review and persisted cancellation detail inspected |
| `9aAH9sxUsAe4QdicgfVurBOavIG` | pulse | READY | All 20 task occurrences inventoried; pending package approval identified |

Parent recipe: `build.yaml` resolved to recipes commit
`91ac4e5ef1701918aabd3226af2bd5719bdf40ff`.
Read-only CLI: c2j v0.0.124, source
`33e2a4de4e99d3a577a38dca4b8de33d43a099ce`.

## Selected parent task occurrences

Use `c2j job log JOB --json`, then the returned exact `id` with `--task`.
The following selectors identify occurrences without copying the full history:

| Occurrence | Operation | Result |
| --- | --- | --- |
| `wait_children` run 3, nested `wait` | `recipe.await_result_soft:inspect` | Finished 16:59:01; assistant cancelled, no message |
| `work` run 21, `resume_implementation_session` | `extension_execution:extension_execution` | Finished 17:00:39; returned `next: fail` and preserved patch |
| `work` run 21, child `inspect` run 2 | `recipe.await_result_soft:inspect` | Finished 17:00:43; c2j cancelled, no message |
| `operational_failure`, `stop_attempt` | `command_execution:command_execution` | Failed 17:00:44 with parent cancellation-recovery summary |

Parent `work` run 21 artifacts read:

- `implementation.md`, especially “Cancellation recovery finding”.
- `recovery/assistant/handoff.md`, documenting the saved candidate and its
  claimed missing cancellation disposition.

The task inventory also records `recovery/assistant/source.patch` and
`recovery/assistant/provenance.json`. Their presence and the agent's report were
checked; this audit does not certify the patch's code or tests.

## Job-level evidence unavailable through c2j show

The supported read endpoint
`GET /v1/tenants/c2/jobs/{job_id}` returned `completionStatus`,
`completionDetail`, and `status` for the parent and both cancelled children.
The two child messages are quoted in the [audit](AUDIT_CANCELLATION_FEEDBACK_2026-11-08.md).

Raw inventories and selected downloads remain in scratch at
`/tmp/cancellation-audit-18c76d-aVuwQ2`; durable findings above contain the
producer references required to retrieve the evidence again. No review was
answered, job changed, replacement submitted, or runtime modified.

# Handoff and recovery behavior

Defined before implementation, 2026-11-07. These statements cover the accepted handoff, session, routing, waiting, and inspection plan.

| ID | Priority / level / dependencies | Relevant files | Statement |
| --- | --- | --- | --- |
| HR-01 | Critical / integration / c2j | `coordinate.yaml`, `prompts.yaml` | An execution child receives its generated assignment without inherited consultation prohibitions. |
| HR-02 | Critical / integration / c2j | `consultation.yaml`, `coordinate.yaml` | Consultation uses separate checkpoints while progression resumes its original session and unpublished candidate. |
| HR-03 | Critical / integration / c2j | `develop.yaml`, `agent.yaml` | Implementation starts a fresh session using the settled handoff and preserves its changes in the next task's checkout. |
| HR-04 | Critical / integration / c2j | `develop.yaml`, `agent-turn.yaml` | Planning recovery preserves planning instructions; implementation recovery persists a real repository edit. |
| HR-05 | High / integration / c2j | `agent-turn.yaml`, `consultation.yaml` | Consultation and response-correction experiments leave the managed candidate unchanged while preserving their output documents. |
| HR-06 | Critical / integration / c2j | `coordinate.yaml`, `route-target.yaml` | A root consultation referring work to recipes launches one recipes child and no root implementation child. |
| HR-07 | High / integration / c2j | `coordinate.yaml`, `consultation.yaml` | Nested and custom consultation referrals reach their explicit execution owners without another dispatch consultation. |
| HR-08 | Critical / integration / c2j | `coordinate.yaml`, document-binding helpers | Selected documents created after consultation arrive byte-for-byte in the execution child's materialized inbox. |
| HR-09 | High / integration / c2j | `coordinate.yaml`, document-binding helpers | Each child receives exactly its selected handoff files; unrelated parent documents, sibling outputs, and consultation history are absent. |
| HR-10 | High / integration / c2j | `coordinate.yaml`, `develop.yaml` | Missing handoff artifacts prevent submission and return a useful correction without asking the human. |
| HR-11 | Critical / integration / c2j | `develop.yaml`, `child-results.yaml` | A waiting parent suspends durably without another agent turn and receives the child's completed result. |
| HR-12 | High / integration / c2j | `develop.yaml`, `child-results.yaml` | Concrete independent parent work continues while children run; status-only continuation routes to waiting. |
| HR-13 | Critical / integration / c2j | `await-child.yaml`, `coordinate.yaml` | Child failure reaches the parent despite an open goal; a corrected attempt starts fresh and cancellation does not trigger resubmission. |
| HR-14 | High / integration / c2j | `classify.yaml`, `build.yaml` | A long README retains useful classification context; a complete execution handoff does not restart design. |
| HR-15 | Critical / integration / c2j | `verify.yaml`, `develop.yaml` | Failed hook status blocks merge and publication even when the helper operation succeeds. |
| HR-16 | High / integration / c2j | `develop.yaml`, `task-documents.yaml` | Subsequent tasks receive selected current files without accumulating superseded reports; earlier artifacts remain retained by their producers. |
| HR-17 | High / integration / inspection-capable c2j | `prompts.yaml`, `agent-turn.yaml` | New working, consultation, and review sessions receive inspection guidance even when job submission is disabled. |
| HR-18 | Critical / integration / task helper and failed child | `coordinate.yaml`, recovery tests | A parent retrieves selected failed-child outputs into a fresh handoff without forwarding unrelated artifacts or session state. |
| HR-19 | Critical / integration / task helper and scoped tokens | `agent-turn.yaml`, recovery tests | Inspection reads current-job and direct-child artifacts; unavailable parent or sibling inputs produce a specific unmet-input report. |
| HR-20 | Critical / integration / snapshot-capable c2j and Git | `coordinate.yaml`, recovery tests | Recovered changes are reviewed and applied in a writable task; unavailable snapshots preserve the option to start again. |

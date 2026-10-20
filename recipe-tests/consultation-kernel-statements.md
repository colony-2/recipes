# Consultation kernel test statements

Tests run through c2j's native runtime with mocked Codex and real Git, object,
artifact, and human-review handling. The handoff fixture publishes this document
as a c2 artifact before consultation.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, c2ops manifests | `recipes/kernel/consultation.yaml` | Only the consultant can establish agreement; requester acceptance still returns to the consultant. |
| Critical | Integration / c2j | `recipes/kernel/consultation.yaml` | Four unresolved consultant replies wait for human review inside consultation; agreement on the fourth reply completes without review. |
| Critical | Integration / c2j objects | `recipes/kernel/agent-turn.yaml` | Each participant resumes its own latest checkpoint; callers receive both checkpoints and the original requester checkpoint. |
| Critical | Integration / c2j artifacts | `recipes/kernel/consultation.yaml` | Both participants receive listed documents at iteration-specific paths; missing or escaping paths prevent agreement. |
| High | Integration / c2j artifacts | `recipes/kernel/consultation.yaml` | Unlisted temporary artifacts are excluded; earlier exchanged versions remain available for review. |
| Critical | Integration / c2j, Git | `recipes/kernel/consultation.yaml` | Expert consultations inspect the current unmerged candidate, while all consultation experiments are discarded. |
| Critical | Integration / c2j, Git | `recipes/kernel/consultation.yaml` | Foreign consultants inspect their target repository without replacing the requester's candidate. |
| High | Integration / c2j, c2ops manifests | `recipes/kernel/consultation.yaml` | Each participant receives consultation purpose and roles once, including an existing requester session; follow-ups carry new messages and file pointers. |
| Critical | Integration / c2j | `recipes/kernel/consultation.yaml` | Failed or incomplete agent turns cannot establish agreement or consume a successful negotiation iteration. |
| Critical | Integration / c2j objects | `recipes/kernel/consultation.yaml` | Retrying failed turns preserves participant checkpoints and the existing iteration budget. |
| High | Integration / c2j | `recipes/kernel/consultation.yaml` | Declines, redirects, and cancellations terminate; either participant's deconfliction request waits for human direction without submitting implementation jobs. |
| High | Integration / c2j artifacts | `recipes/kernel/consultation-report.yaml` | Requested summaries preserve consultant outcomes and point to exact final document revisions. |
| Critical | Integration / c2j objects | `recipes/kernel/consultation.yaml` | Summary consumers can continue the original requester checkpoint independently of the consultation's successor checkpoint. |
| Critical | Integration / c2j artifacts | `recipes/kernel/consultation-report.yaml` | Unresolved conversations produce independent review assets and focused questions without declaring agreement. |
| Critical | Integration / c2j objects | `recipes/kernel/consultation.yaml` | Expert-directed continuation preserves both sessions and prior evidence while opening an explicit bounded round. |
| Critical | Integration / c2j | `recipes/kernel/consultation.yaml` | Resuming unresolved consultation without expert direction cannot reset the iteration budget. |
| Critical | Integration / c2j artifacts | `recipes/kernel/consultation.yaml` | Human answers and attachments reach both participants; each receives new direction once, and only the consultant can subsequently establish agreement. |
| Critical | Integration / c2j | `recipes/kernel/consultation.yaml` | Repeated disagreement requires another human review before another bounded round; prior answers and sessions remain recorded. |
| High | Integration / c2j | `recipes/kernel/consultation-report.yaml` | Missing review documents preserve unresolved state with an explicit error; negotiation cannot continue without expert direction. |

# Coordination, reviews, and package request expectations

Defined before implementation; preserve existing expectations.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| CR-01 | Critical | Integration / c2j goals | Prerequisites and validation wait for goal success and consume the successful replacement attempt's evidence. | coordinate.yaml, validation-goals.yaml |
| CR-02 | Critical | Integration / c2j | Repeating an existing execution request waits without duplicate submission or another unchanged work turn. | coordinate.yaml, develop.yaml |
| CR-03 | High | Integration / mocked Codex | Agents request consultation and execution without inventing or repeating prerequisite keys; advisory agreements impose no implementation obligation. | agent.yaml, develop.yaml |
| CR-04 | High | Integration / mocked Codex | Consultation can request downstream advice and resume with its result without human scheduling. | consultation.yaml |
| CR-05 | Critical | Integration / c2j | Execution instructions authorize agreed implementation while preserving scope and task permissions, without appending stale consultation restrictions. | prompts.yaml |
| CR-06 | High | Integration / c2j | Human reviews present one current overview, relevant supporting evidence, and specific questions. | review.yaml, develop.yaml |
| CR-07 | High | Integration / mocked Codex | Requested changes return exact feedback to Codex for implementation or design routing without asking the user to select a phase. | develop.yaml, prompts.yaml |
| CR-08 | Critical | Integration / c2j artifacts | Returning unchanged test expectations succeeds; changed expectations require redesign rather than silent acceptance. | develop.yaml |
| CR-09 | Critical | Integration / package manager | Requested packages install only after policy authorization or explicit approval; failed validation leaves the parent's config unchanged. | packages.yaml, package-check.yaml |
| CR-10 | Critical | Integration / package manager | Successful package validation adopts the exact approved config and resumes blocked work; concurrent config changes prevent overwrite. | packages.yaml |
| CR-11 | High | Integration / mocked Codex | Agents receive the package-request syntax and goal-oriented monitoring instructions, including limits on direct child execution. | prompts.yaml |
| CR-12 | Critical | Integration / c2j | Failed attempts do not fail an open goal; explicitly failed goals remain blocking and never masquerade as success. | coordinate.yaml, validation-goals.yaml |
| CR-13 | Critical | Integration / c2j, mocked Codex | Top-level, nested, and repository-custom consultations return advice within one job, preserving each participant's workspace and session. | coordinate.yaml, consultation.yaml |
| CR-14 | Critical | Integration / c2j, mocked Codex | Nested siblings and deeper advice resume the correct suspended conversation; bounded failures never become agreements. | consultation.yaml |
| CR-15 | High | Integration / c2j | Custom consultation recipes run inline in participant workspaces; invalid sources fail visibly instead of silently selecting another recipe. | coordinate.yaml |

The custom-selection portion of CR-13 and CR-15 is pending the user's
investigation of c2j's hook workspace restriction. The existing custom-selector
interface remains in place until its inline replacement is settled.

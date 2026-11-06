# Shared prompt acceptance statements

Defined before implementation. This work fits the recipes cell; no c2j or c2ops
runtime changes are required. Existing behavior expectations remain in force.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| SP-01 | Critical | Integration / c2j | Shared prompt includes produce text without worker operations, child jobs, or artifact handoffs. | recipes/adaptive/prompts.yaml |
| SP-02 | Critical | Integration / c2j | Agents receive equivalent task wording and new-session instructions after prompt extraction. Resumed sessions receive no repeated system instructions. | recipes/adaptive/agent.yaml, recipes/adaptive/agent-turn.yaml |
| SP-03 | Critical | Integration / c2j | Inbox and outbox paths resolve at the consuming operation, including resumed sessions and foreign-cell consultations. | recipes/adaptive/agent-turn.yaml, recipes/adaptive/consultation.yaml |
| SP-04 | High | Integration / c2j | Classifier, reviewer, consultation, correction, child-request, and human-review text comes from the shared include without changing routing or decisions. | recipes/adaptive/*.yaml |
| SP-05 | Critical | Integration / c2j | Request text containing template-like syntax or formatting characters remains literal data when inserted into shared prompts. | recipes/adaptive/agent.yaml |
| SP-06 | High | Integration / c2j | Local prompt edits appear in consumers while schemas, permissions, phase choices, and artifact bindings remain recipe-owned. | recipes/adaptive/prompts.yaml, recipes/adaptive/*.yaml |
| SP-07 | High | Integration / c2j | New sessions identify their actual job and explain automatic persistence, child results, and exceptional authorized child-job use without relaxing assignment restrictions. | recipes/adaptive/prompts.yaml, recipes/adaptive/agent-turn.yaml |
| SP-08 | High | Integration / c2j | Agent instructions favor coordinated project work and describe bug reports, enhancements, and clarifications without requiring a new response field. | recipes/adaptive/prompts.yaml |

Validation compares operation inputs and task counts with the preceding refactor,
exercises shared text through a native command fixture, and runs the existing
adaptive regression suites. Retain this document as a native fixture artifact.

# Recipe readability acceptance statements

Defined before implementation. This cleanup fits the recipes cell. Runtime
support for ordinary map/list recipe inputs belongs to c2j.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| RC-01 | High | Integration / c2j | Inbox and agent fixtures accept specific values and artifact maps without serialized workflow envelopes or unused default fields. | recipe-tests/adaptive/agent-inbox.yaml, recipe-tests/adaptive/agent-prompt.yaml |
| RC-02 | Critical | Integration / c2j | Shared prompts use named template inputs; request text remains literal and consumer operations resolve their own artifact directories. | recipes/adaptive/prompts.yaml, recipes/adaptive/agent-turn.yaml |
| RC-03 | Critical | Integration / c2j | Prompt cleanup preserves assignments, new-session instructions, consultation behavior, and worker operation counts. | recipes/adaptive/agent.yaml, recipes/adaptive/inspect.yaml, recipes/adaptive/consultation.yaml |
| RC-04 | Critical | Integration / c2j | Renamed documents retain identity and source links; stale annotations and ambiguous or missing sources never describe a different artifact. | recipes/adaptive/artifact-annotations.yaml, recipes/adaptive/document-bindings.yaml |
| RC-05 | Critical | Integration / c2j | Human reviews preserve document priorities, reject invalid metadata, and omit stale or self-referential evidence links. | recipes/adaptive/review.yaml |
| RC-06 | High | Integration / c2j | Consultation replies read exchanged files from inbox without embedding a filename inventory or maintaining a parallel latest-files map. | recipes/adaptive/consultation.yaml |

The former consultation assertion requiring a filename in the prompt is replaced
under the user's explicit directory-handoff instruction. Its artifact-binding
assertions remain in force; this removes redundant prompt bookkeeping.

Retain this document as a fixture artifact. Reuse the native inbox/review cases
and adaptive regression suites; add focused negative source-link cases where
the existing suites do not cover the annotation rewrite.

# Clear reviews and a dependable Backstop

Implement the open [todos](TODO.md) using the existing activity lifecycle.
Recipes owns the prompts, choices, routing and tests. c2j owns dependency
preparation and permission enforcement; Cortex owns its review renderer.

## Milestone 1: clear writing and decisions

Restore adaptive2's guidance about owner voice, user-visible consequences and
meaningful design questions in the shared context. Keep the one-pager structure
and per-cell scope table. Have the existing validator assess readability.

Rename Resolver to Backstop throughout active adaptive3 code and tests. Keep a
single review activity, with the current stage and one decision kind determining
its title, question and buttons. Questions and change requests use the same
conversation agent. Tool refusal returns to the requester without a probe.

Test real native forms and transitions, then Cortex's renderer. Preserve human
receipts and reuse of approval after an unchanged rebase.

## Milestone 2: human guidance and recovery

Backstop reconsiders text and attachments submitted with Continue. A question
keeps the conversation open. Show the correction and any finite allowance clearly.
Use short self-contained recovery questions and selected existing documents;
validate links through the existing output validator. Keep native human input
available when agents or validation tools fail.

Test conflicting feedback, question-only replies, missing links, provider failure,
and repeated human discussion. Run the whole destination cycle after recovery.

## Milestone 3: real boundaries

Document and test supported inclusion from another recipe repository, including
input-secret grants and denied ceilings. Use fixture secrets and native permission
evaluation. Keep failures inside the containing workflow's recovery boundary.
Add concise diagnostic guidance and test that actual child findings return to
their requester, independently of job success.

Run validator behavior tests and provide a supported-worker check of the actual
declared dependencies, including fresh preparation and reuse. Track the filed
c2j Python bug; do not mask it with ambient packages or change c2j here. Compact
directory references remain a runtime/UI requirement until supported; do not
invent a manifest or archive transport.

Record completed checks, external blockers and differences from this plan in an
implementation assessment. Commit tested milestones separately.

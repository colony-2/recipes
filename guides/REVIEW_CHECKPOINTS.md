# Build/evolve document reviews

Build and evolve use c2j's native `input` op with `form.kind: review`. The runtime
owns request identity, stored documents, input validation, response attachments,
and receipts. There is no recipe-specific review transport or schema.

Use c2j `614bfac82f15` or later on workers and authoring tools. This includes the
simplified review API and portable JSON output fixes. Codex requirements remain
those in [the session migration guide](CODEX_OBJECT_SESSION_MIGRATION.md).

## Checkpoints

- Plan approval presents the design and Markdown test statements, after independent
  design and test-plan reviews. Its summary includes the mandate assessment and
  agreed external work.
- Outcome acceptance presents those documents plus the implementation summary and
  verification report for the tested candidate. Satisfied approval allows the
  existing verification/scope gates and squash merge.
- Clarification and outside-mandate checkpoints use the same native form pattern,
  exposing whichever documents are available.

The document IDs are `design`, `test_statements`, `implement`, and `verification`.
Values are complete stored artifact references, passed with `${{ ... }}`. Each
producer writes its Markdown as part of its normal output. Reviews require no
preparation recipe. Original document references remain on the frozen form.

## Responses and revision

All forms have a required `decision` field, optional `feedback`, and optional
`annotated_design` and `annotated_test_statements` uploads. Outcome and
implementation feedback forms also offer `annotated_outcome`. Decision options
are specific to the checkpoint; no decision is selected automatically.

A revision with text or files goes directly to the appropriate phase. A revision
without either opens a clarification review. Text-only and attachment-only
responses are supported. Uploaded edits accompanying approval require revision
and another review; they never approve a silently modified candidate. Text notes
accompanying approval are recorded, and do not themselves request changes.

The selected transition carries that exact response to the next phase. Returned
artifacts enter the agent inbox under `prior/review/`, separate from verification
logs. Agents read annotations, including CriticMarkup, as requested changes.
c2j does not apply them. Scope/requirement changes require redesign and renewed
plan approval. Implementation revisions explicitly resume the last successful
Codex session object. Design authors and critics retain their existing session
policies.

Changes produce new artifact references and another review occurrence. Earlier
feedback is not selected merely because its state still exists. Every occurrence
and its receipt remain in runtime history. Root `reviews` exports the most recent
receipt at each named checkpoint; `review_documents` exports current document
references. Existing `artifact_refs` continues to export verification evidence.

## Clients and tests

Clients discover reviews through c2j's `GetForm`/`GetDetails` library and submit
`fields` with the pending `request_id`, a submission ID, and an application-owned
actor using `SubmitFormResponse`. Optional upload fields may be absent. Runtime
`artifact_refs` contains returned attachments, not original review documents.

The ordinary interactive CLI does not render document reviews. Use
`--input-mode ops` to expose the pending form, submit through a review-capable
client, and continue the job. Submission IDs are correlation identifiers, not an
idempotency guarantee. Historical receipt lookup and ambiguous completion recovery
retain the limitations documented by c2j.

`recipe-tests/verify-native-reviews.py` runs both committed local defaults with a
separate ephemeral JobDB and a client using the public c2j input library. It
scripts model decisions but exercises real review publication, invalid and stale
submissions, uploaded bytes, worker replacement, sessions, gates, verification,
and squash merges. Production forms have no autofill.

The earlier [review handoff proposal](NATIVE_REVIEW_HANDOFF_PROPOSAL.md) and
`contracts/review` fixtures are historical design material. They are not the
implemented native review protocol or a prerequisite for these recipes.

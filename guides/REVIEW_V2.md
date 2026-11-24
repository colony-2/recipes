# Structured adaptive3 reviews

Adaptive3 emits Cortex `review/v2` forms for Preparation, explanation, Outcome,
merge, package and Backstop decisions. This presentation format is independent
of recipe YAML `schema_version: 2`.

Producers also return the complete [document details](adaptive3/DOCUMENT_DETAILS.md)
required by adaptive3. The ordinary validation cycle checks exact attachment IDs,
titles, purposes, roles, reading order and the primary document. Checked metadata
and the overview travel inside `request`, including discussion and routing
clarifications. Questions keep the current documents. The producer validates
revised documents before presenting them again.

Use `recipes/review-v2.yaml` with a `request` containing `title`, `question`,
`documents`, `directions`, `feedback`, `conversation` and optional `settings`,
`review_id` and document metadata. It returns the complete native input `form`.
The helper validates declarations before opening input and generates closed
request/response JSON schemas. Do not add native `kind`, ordinary `fields`, legacy
`feedback_required`, or a global upload permission.

Each direction declares `id`, `label`, `feedback_mode` (`forbidden`, `optional`,
`required`), `allow_attachments` and `continues_review`. Adaptive3 approvals allow
an optional text comment. It stays with the approval and its revision. Required
contributions need meaningful text or a permitted resolved new
upload; earlier files and settings do not satisfy that requirement. Native responses
always contain `direction`, `feedback`, `attachments` and sparse `settings`.
Preserve the complete native response and receipt, including exact human text.

Settings declare scalar schemas and explicit applicable directions. Optional reset
requires both a valid `default` and `reset_label`. False, zero, null and strings
remain distinct. Unknown, inapplicable or incorrectly typed edits fail. Adaptive3
currently uses only `return_to` for valid correction destinations. Apply it once,
then present Auto again. The generic helper supports other fixture settings without
adding model/reasoning controls or configuration propagation to adaptive3.

`recipes/review-v2/op.yaml` is a local source extension backed by the stdlib-only
`recipes/review-v2.py`. Structured operation output avoids command stdout truncation
on larger schemas. With normal Git recipe selectors, the relative operation is
resolved from the recipe source repository/ref. Inline test fixtures must provide
those source files explicitly. No new runtime service is required.

### Following a review across revisions

A plan keeps its `review_id` for the life of the job, including a return to
planning after implementation. An outcome, a package proposal and a Backstop
decision each have their own thread.

| What the reviewer sees | `review_id` | `revision` | Native `request_id` |
| --- | --- | --- | --- |
| Plan presented | A | 1 | First request |
| Answer to a question about the plan | A | 1 | Second request |
| Revised plan presented | A | 2 | Third request |
| Outcome presented | B | 1 | Fourth request |

Group the job's native requests by `review_id` to find a decision. Group those
requests by `revision` to find each version's documents. Read the producer
references from that version's form. A file can keep its name and change its
contents. Approval records the submitted request's receipt, revision and reviewed
document references.

The next form includes the ordered discussion and uploaded notes. Each turn
records the revision it belongs to. Answering a question or clarifying where a
correction belongs keeps the revision open. Presenting the author's revised work
increments the revision and asks for a fresh decision.

When calling `adaptive3/review.yaml` again, pass its previous `threads` output
to the next call's `threads` input. The `decision` key selects the thread. A new
package request or a separate escalation starts with an empty thread.

Use **Reply** for questions and edit requests. The receiving agent answers a
question in the thread, routes a requested edit, or asks what you meant. An
optional **Return to** setting applies to an edit. Scope changes go to Direction.
The agent asks about conflicting destinations before starting work. Review doc
comments appears only with originals and reruns their producer and validation,
keeping the discussion with the revised documents. Package comments regenerate the
proposal before probing. Backstop comments repeat read-only
investigation before any correction decision.

New jobs require compatible published Cortex reader support. Existing frozen legacy
forms retain their reader behavior. Backstop no longer offers model, reasoning or
settings-reconsideration actions; launch-time settings remain available. Custom
adaptive3 includes must consume structured results and preserve correction routing.

See [native and consumer checks](../recipe-tests/adaptive3/README.md), the shared
[contract vectors](../recipe-tests/review-v2/contract-vectors.json) and
[acceptance statements](../recipe-tests/review-v2/statements.md).

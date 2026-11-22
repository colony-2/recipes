# Structured adaptive3 reviews

Adaptive3 emits Cortex `review/v2` forms for Preparation, explanation, Outcome,
merge, package and Backstop decisions. This presentation format is independent
of recipe YAML `schema_version: 2`.

Producers also return the complete [document details](adaptive3/DOCUMENT_DETAILS.md)
required by adaptive3. The ordinary validation cycle checks exact attachment IDs,
titles, purposes, roles, reading order and the primary document. Checked metadata
and the overview travel inside `request`, including discussion and routing
clarifications. Questions retain that frozen collection; explicit corrections
receive full validation before a new review.

Use `recipes/review-v2.yaml` with a `request` containing `title`, `question`,
`documents`, `directions`, `feedback`, `conversation` and optional `settings`,
`review_id` and document metadata. It returns the complete native input `form`.
The helper validates declarations before opening input and generates closed
request/response JSON schemas. Do not add native `kind`, ordinary `fields`, legacy
`feedback_required`, or a global upload permission.

Each direction declares `id`, `label`, `feedback_mode` (`forbidden`, `optional`,
`required`), `allow_attachments` and `continues_review`. Approval forbids any text
or upload. Required contributions need meaningful text or a permitted resolved new
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

`recipes/adaptive3/discussion.yaml` freezes the original request and identity,
retains each exact human contribution and receipt, and appends actual read-only
answers. Questions reopen the same review with full ordered conversation and a
fresh native request. Uploads use distinct per-request/per-binding paths; originals
keep their producer references. The answering session resumes independently from
producer and diagnosis sessions. Questions never approve work or grant attempts.

Request changes routes through the selected complete stage cycle. Scope changes
require Direction; conflicting instructions require clarification. Review doc
comments appears only with originals and reruns their producer and validation,
requiring fresh approval under a new identity. Package comments regenerate the
proposal before probing; refusal runs no probe. Backstop comments repeat read-only
investigation before any correction decision.

New jobs require compatible published Cortex reader support. Existing frozen legacy
forms retain their reader behavior. Backstop no longer offers model, reasoning or
settings-reconsideration actions; launch-time settings remain available. Custom
adaptive3 includes must consume structured results and preserve correction routing.

See [native and consumer checks](../recipe-tests/adaptive3/README.md), the shared
[contract vectors](../recipe-tests/review-v2/contract-vectors.json) and
[acceptance statements](../recipe-tests/review-v2/statements.md).

# Native review handoffs through c2j input

Status: proposed contract; **not implemented by the current c2j input op**.
Schemas and fixtures are executable design artifacts, not a claim of runtime
support. Production build/evolve wiring remains unchanged pending native support.

## Recommendation and responsibility

Extend the existing `input` op with an optional, versioned review contract. Keep
ordinary forms working. A review is a durable input checkpoint with named files
and a structured response, not a new workflow engine or a new job type.

This request partially fits the recipes mandate. This cell owns the document
selection, workflow decisions, routing, and recipe integration tests (OWN-01
through OWN-04). c2j owns publishing and retrieving the review, validating its
response, persisting artifacts, and exposing it through its input API
(EXCLUDE-01). A UI owns rendering and editing. c2ops needs no change for this
contract: agent sessions already consume artifact-based feedback.

| Owner | Responsibility |
|---|---|
| Recipes | Summary and documents; offered decisions; meaning of each decision; session continuation; design/verification/merge gates |
| c2j | Immutable review identity; stored artifact resolution; hashes and download locations; transport schema; validation and durable receipt |
| UI / CLI clients | Present summary and files; collect a decision, feedback, and annotated Markdown; submit the published review identity |

Build and evolve use the same protocol. Cell identity and target directory affect
review content, not its transport.

## Evidence from the existing implementation

Inspected c2j commit `0a482892458ebf5c319b0700ad5b7fabd5c97ed2`:

- `pkg/input/activity.go` already separates form generation from durable input
  collection. `Config.Context` carries artifact context. Its
  `ArtifactsFromOutput` resolution is explicitly a placeholder.
- `pkg/input/types.go` defines a context artifact as `{path: string}`. It has no
  named review document, version hash, annotation policy, or review identity.
- `pkg/input/api/openapi/recipe-input-api.yaml` declares the existing pending,
  details, and respond endpoints. `FormResponse.fields` accepts arbitrary values;
  it has no declared review payload. Op `Output.metadata` is not exposed by that
  HTTP response schema, and `pkg/input/runtime.go:SubmitResponse` does not copy it.
- `pkg/artifacts/ref.go` defines durable stored references. Story already exposes
  task artifact downloads in `pkg/story/internal/service/service.go`.

The existing machinery is sufficient for an additive implementation. It does
not yet establish a portable review protocol. An adapter could put a manifest in
context and a submission in `fields.review`, but clients would need special
conventions, while validation would happen after the input was consumed. We
recommend native support before recipe adoption rather than publishing that
adapter as a second standard.

## Contract surface

The draft [JSON Schema](../contracts/review/v1.schema.json) contains four entry
points. The default schema validates `ReviewRequest`; use the named `$defs`
entries for the other shapes. c2j should adopt these into its canonical schema
and generated API types once agreed; this repository should then test against the
published version, rather than maintain an independent competing schema.

| Shape | Location | Producer |
|---|---|---|
| `ReviewSpec` | Recipe `inputs.form.review` | Recipe |
| `ReviewRequest` | Pending details `form.review`; `review-request.json` | c2j |
| `ReviewSubmission` | HTTP `FormResponse.review`; autofill `review` | Client / deterministic fixture |
| `ReviewReceipt` | Op `outputs.review` | c2j |

These are **proposed additions**, not accepted keys in today's runtime. In review
mode, `form.review` replaces the ordinary question/fields/options; mixing both
modes is a validation error. Do not silently ignore an unsupported review spec.
The runtime derives a decision control and feedback control for generic clients.
No decision is selected by default and no timeout approves a review.

A [recipe specification](../contracts/review/examples/spec.json) supplies:

- A title and summary in Markdown.
- Decision IDs and human labels, with `accepts_reviewed_content` and
  `feedback_required` flags. IDs stay recipe-defined: c2j does not learn what
  `redesign` or `satisfied` means.
- Files with stable IDs, titles, media types, stored artifact references, and an
  annotation policy (`criticmarkup` or `none`). File IDs are unique within a
  review. `files: []` is allowed for a summary-only clarification checkpoint.
- An optional subject `{id, version}`. Outcome acceptance supplies the canonical
  cell and exact verified candidate commit; other workflows can identify their
  own immutable subject without introducing Git concepts into the protocol.

c2j resolves each stored reference, verifies access in the request tenant, reads
its exact bytes, and publishes a [request](../contracts/review/examples/request.json)
with a runtime-owned `review_id`, origin, SHA-256 hashes, and download locations.
Original producer references remain intact, including files produced by child
jobs. No workspace/inbox path or mutable URL is a document identity. If a recipe
starts from an external resource it must first snapshot it as a stored artifact.

Hash exact bytes without newline or Unicode normalization. Markdown must decode
as UTF-8. Expiring download URLs may be refreshed; they do not change the review
identity or its immutable content. Use the existing authorized artifact download
service rather than introduce another file server. Download URLs are presentation
data, never filesystem destinations or authority to access another tenant.

The request identity binds the summary, decisions, document versions, and optional
subject. The same pending input retains its identity through worker replacement
and replay. Re-entering the review state after any revision creates a new request.
Unavailable artifacts prevent publication; failure must not drop a document and
present a partial package as though it were complete.

## Submission, validation, and receipt

The client posts a [submission](../contracts/review/examples/submission-revise.json)
to the existing respond endpoint, adding a typed `review` property to
`FormResponse`. It contains `review_id`, client-generated `submission_id`,
`decision`, `feedback`, and `annotations`. Keep `fields: {}` if the existing
transport continues to require it. Review clients need not mirror decisions into
legacy fields. If a client supplies conflicting legacy responses, reject them;
do not choose one silently. Plain forms retain their existing behavior.

Each annotation contains a file ID, its `base_sha256`, `format: criticmarkup`, and
the complete annotated Markdown document. This avoids a new upload lifecycle for
the initial version. Persist submitted Markdown as artifacts for later ops. Do
not interpret file IDs as arbitrary client-supplied filesystem paths.

The [CriticMarkup specification](https://github.com/CriticMarkup/CriticMarkup-toolkit)
provides insertion, deletion, substitution, comment, and highlight notation.
The example requests a change using `{~~stable~>creation-time~~}` and a comment.
c2j transports these suggestions as feedback; it does not apply them to Git or
need to implement a Markdown editing engine. The hash identifies the baseline;
it does not prove the annotated text preserves that baseline. The session reviews
the original and submitted documents together, asking for clarification when a
suggestion is malformed or ambiguous. A UI may add syntax assistance and previews.

Before completing the pending input, c2j must check:

1. The shape/version, active review ID, and offered decision.
2. Unique document and decision IDs in the request; unique annotated file IDs in
   the response.
3. Every annotation names an offered Markdown document allowing CriticMarkup, with
   an exact matching base hash. Evidence documents marked `none` cannot be edited.
4. A decision with `accepts_reviewed_content: true` has no annotations. Return a
   validation error inviting a revision decision; never silently change the user's
   decision or treat proposed edits as approval. Plain feedback is permitted with
   approval and is informational; changes require a revision decision.
5. A decision with `feedback_required: true` has nonblank feedback or at least one
   nonblank annotated document. This is a completeness check, not an AI judgment
   about the usefulness of feedback.
6. Publication and submission respect explicit runtime size limits. Return errors
   rather than truncating content. c2j must document the selected limits; this
   draft deliberately does not invent a second set of transport quotas.

JSON Schema covers shape and local constraints. Membership, uniqueness by ID,
matching hashes, and decision-specific requirements are runtime checks against
the stored request; they cannot be replaced by schema validation alone.

Persist the original submission, annotated documents, and a
[receipt](../contracts/review/examples/receipt.json) before completing the input.
The receipt returns the submission, runtime-recorded submitter/time, and durable
artifact references. Actor identity follows the existing authenticated transport;
a submission payload must not invent an authoritative reviewer identity. Existing
`outputs.response` mirrors the decision for compatibility. New recipes consume
`outputs.review.submission`, and explicitly export `outputs.review.artifact_refs`.

A validation failure leaves the same input pending and returns a structured field
error. A stale/cancelled/completed review is a conflict, not a new response for the
next review in that job. Identical retries of an accepted `submission_id` return
the same receipt without resuming twice; reuse of that ID with different content
is a conflict. Concurrent distinct submissions have one winner. Receipt durability
and task completion must provide these semantics even if the worker crashes
between persistence and acknowledgment; c2j chooses the implementation.

Autofill, HTTP, and any CLI submission must share this validation path. Tests
must not bypass it by injecting an already accepted op output. An old client can
still handle ordinary forms. For review forms, a client that cannot echo the
review identity must fail explicitly rather than bypass stale-review protection.

## Recipe adoption after c2j support

Keep orchestration in `recipes/develop/develop.yaml` and put common packaging in a
shared review recipe if needed. Export inner phase artifact references explicitly;
files are often produced before the final op of a phase. The UI should receive
human-readable Markdown, not require a reviewer to interpret internal result JSON.

| Existing checkpoint | Review package | Decisions and routing |
|---|---|---|
| `approve_plan` | Design, test statements, readable mandate assessment and external handoffs | `approve` starts implementation; `revise` with feedback/annotations resumes design |
| `plan_feedback` | Available design/test documents, questions, independent review findings | `revise` resumes design; no approval option |
| `accept` | Outcome summary, reviewed test statements, verification report/logs; subject binds verified candidate | `satisfied` reaches the existing squash/merge gate; `revise` resumes implementation; `redesign` resumes design |
| `implementation_feedback` | Candidate summary, specification/quality findings, failed verification evidence | `revise` resumes the same implementation session; changed scope still triggers redesign |
| `outside` | Mandate assessment and routing advice | `acknowledge` completes without merge; `revise` re-enters design |

Design and test-statement Markdown can accept annotations. Verification evidence
and command logs are read-only; users describe concerns in feedback. Test-statement
edits remain proposed changes, subject to the existing deprecation process.
Outcome review annotations of requirements/test statements must route to redesign,
not silently change approved expectations during implementation. The recipe should
offer or enforce the appropriate decision for that document role.

Feed the summary, submission, original documents, and submitted Markdown to the
continuing session through artifact references. Preserve those references across
child boundaries and worker replacement. Never apply uploaded text as an automatic
patch. A revised plan or candidate repeats its applicable checks and human review.

Feedback submitted with a revision decision should go directly to the appropriate
session; do not make users repeat it in today's second feedback prompt. Keep
feedback-only checkpoints for agent questions and failed independent checks.
Finish still checks verification, reviewed candidate identity, explicit satisfaction,
and the existing scope/merge constraints. c2j accepting a submission does not
perform or authorize a merge independently of the recipe.

## Delivery and acceptance

1. Agree the draft contract with c2j. Adopt the schema into its input types and
   OpenAPI; implement publication, validation, receipt persistence, and retries.
2. Provide the native contract tests below using a separate disposable JobDB and
   real input HTTP submission. No home database and no model calls are needed.
3. Update shared build/evolve checkpoints and agent feedback artifacts here.
   Extend real lifecycle tests before enabling the new mode in production defaults.
4. UI work can follow separately. A basic client displaying the request, downloading
   files, and submitting JSON is sufficient to validate the entire protocol.

The executable tests in this change validate schema fixtures only. These native
acceptance scenarios are **pending**, not covered by a simulated recipe adapter:

| ID | Expected outcome | Owning test |
|---|---|---|
| NR-01 | Published summary, choices, document names, hashes and downloadable bytes match the selected artifacts | c2j real input API |
| NR-02 | Restart preserves a pending review and its identity; accepted receipt and files remain retrievable | c2j + disposable JobDB |
| NR-03 | A structured approval completes exactly the pending input and returns a durable receipt | c2j real input API |
| NR-04 | All five CriticMarkup forms survive submission and artifact download byte-for-byte | c2j real input API |
| NR-05 | Stale review IDs, wrong hashes, unknown/duplicate file IDs, and forbidden annotations leave input pending | c2j real input API |
| NR-06 | Unknown decisions, approval with annotations, and feedback-required decisions without feedback are rejected | c2j HTTP and autofill |
| NR-07 | Concurrent submissions, identical retries, conflicting retries, cancellation and crash recovery cannot complete twice | c2j + separate workers |
| NR-08 | Missing/unauthorized artifacts, duplicate document/decision IDs, invalid UTF-8, and oversized content cannot publish or consume incomplete reviews | c2j artifact/input integration |
| NR-09 | Ordinary legacy forms still work; unsupported review payloads and conflicting legacy values fail explicitly | c2j compatibility tests |
| NR-10 | Child-produced artifacts retain producer identity and access checks when reviewed in a parent job | c2j + disposable JobDB |
| NR-11 | Revision feedback and annotation artifacts reach the same session without a second prompt; new review has a new ID | Recipes real lifecycle |
| NR-12 | Satisfaction merges only the reviewed verified candidate; annotations/redesign cannot bypass design approval or merge gates | Recipes real Git lifecycle |

Local contract checks: `uv run recipe-tests/verify-review-contract.py`. They are
also included in `recipe-tests/run-defaults.sh`. They do not start c2j or access
any database. The fixtures are synthetic; their example artifact IDs and URLs
are not live resources.

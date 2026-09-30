# Implementation handoff for c2j: native review protocol

> Historical proposal: c2j adopted the simpler `form.kind: review` model.
> See [the implemented build/evolve review pattern](REVIEW_CHECKPOINTS.md).
> The schemas and transport below are not the current runtime contract.

To: the c2j team. Requested outcome: extend the existing `input` op so a recipe
can present a summary and named review files, then receive a structured decision,
feedback, and optional CriticMarkup documents.

The agreed delivery order is **c2j contract first, recipe wiring afterward**.
Do not build a temporary recipe adapter. This is a proposed implementation
contract, not a description of functionality already shipped. Source observations
below are pinned to the inspected commit; reconcile them with current c2j before
implementation.

This document is the complete handoff. It includes the implementation requirements,
JSON Schema, concrete request/response examples, original Markdown bytes, validation
instructions, and acceptance criteria. No files from the recipes checkout are
needed to review or implement it. Example artifact IDs and URLs are synthetic.

## Requested c2j deliverables

1. Add typed review specification, published request, submission, and receipt
   shapes to the input op and its generated API contract.
2. Publish immutable review packages backed by existing stored artifacts, including
   exact content hashes and authorized download locations.
3. Validate submissions against the pending request before consuming input;
   persist the response and annotated documents with a durable receipt.
4. Preserve review identity through replay and provide retry/concurrency semantics
   that cannot complete an input twice.
5. Exercise the native acceptance cases below with a separate ephemeral JobDB,
   real input HTTP submissions, and replacement workers. Keep ordinary forms working.
6. Return the supported c2j version/capability, finalized schema/API documentation,
   and passing acceptance results to the recipes team for integration.

The implementation is ready for recipe adoption when NR-01 through NR-10 pass.
The recipes team then owns NR-11 and NR-12. UI editing work is not a prerequisite:
a basic client can display documents and submit the structured payload.

## Responsibility boundary

Extend the existing `input` op with an optional, versioned review contract. Keep
ordinary forms working. A review is a durable input checkpoint with named files
and a structured response, not a new workflow engine or a new job type.

c2j owns the shared transport and durable input behavior. The recipes team owns
document selection, workflow decisions, routing, and recipe integration tests.
A UI owns rendering and editing. c2ops needs no change for this contract: agent
sessions already consume artifact-based feedback.

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

The complete JSON Schema in Appendix A contains four entry points. The default
schema validates `ReviewRequest`; use the named `$defs` entries for the other
shapes. Adopt the agreed definitions into c2j's canonical schema and generated API
types. The recipes team will test against that published version after adoption.
Appendix B supplies all concrete payloads and their source Markdown documents.

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

A recipe specification (`spec.json` in Appendix B) supplies:

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
its exact bytes, and publishes a request (`request.json` in Appendix B)
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

The client posts a submission (`submission-revise.json` or
`submission-approve.json` in Appendix B) to the existing respond endpoint,
adding a typed `review` property to `FormResponse`. It contains `review_id`,
client-generated `submission_id`, `decision`, `feedback`, and `annotations`.
Keep `fields: {}` if the existing
transport continues to require it. Review clients need not mirror decisions into
legacy fields. If a client supplies conflicting legacy responses, reject them;
do not choose one silently. Plain forms retain their existing behavior.

Use the current input endpoints; `{inputId}` below is the pending input job ID
exposed as `{jobId}` by the existing input API, not necessarily the enclosing
recipe job ID:

```text
GET  /api/projects/{projectId}/user-inputs/{inputId}
     response.form.review = ReviewRequest

POST /api/projects/{projectId}/user-inputs/{inputId}/respond
     body = {"fields": {}, "review": ReviewSubmission}

completed input op:
     outputs.response = ReviewSubmission.decision
     outputs.review = ReviewReceipt
```

Names such as `ReviewSubmission` in this sketch denote the complete JSON object,
not a string. The HTTP response to a successful submission must expose the same
receipt on the initial call and identical retries; add a typed `review` receipt
property alongside the existing `ok` acknowledgment. Keep its identity and content
consistent with the completed op output. Preserve existing ordinary-form responses.

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
receipt (`receipt.json` in Appendix B) before completing the input.
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

1. Finalize this draft in c2j. Adopt the schema into the input types and OpenAPI;
   implement publication, validation, receipt persistence, and retries.
2. Provide the native contract tests below using a separate disposable JobDB and
   real input HTTP submission. No home database and no model calls are needed.
3. Hand the supported contract back to the recipes team. That team updates shared
   build/evolve checkpoints and agent feedback artifacts, extending real lifecycle
   tests before enabling the new mode in production defaults.
4. UI work can follow separately. A basic client displaying the request, downloading
   files, and submitting JSON is sufficient to validate the entire protocol.

The existing executable tests validate schema fixtures only. These native
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

The recipes repository's 16 existing schema/fixture tests passed when this
handoff was prepared. They cover required fields, versions, unknown fields,
artifact shapes, hashes, annotation types, identity ownership, provenance, and
receipt shape. They do not establish native runtime behavior. Appendix C provides
a standalone fixture check requiring only the content of this document.

## Appendix A: complete JSON Schema

Save this block as `v1.schema.json`. It is JSON Schema Draft 2020-12; all
references are internal, so validation needs no network schema lookup.

### v1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$comment": "DRAFT proposed c2j contract, not supported by current input op. Select a $defs entry for specification, submission, or receipt validation.",
  "title": "C2 native review handoff v1 (proposal)",
  "$ref": "#/$defs/ReviewRequest",
  "$defs": {
    "StoredArtifactRef": {
      "type": "object",
      "properties": {
        "kind": {
          "const": "stored"
        },
        "name": {
          "type": "string",
          "minLength": 1
        },
        "stored": {
          "type": "object",
          "properties": {
            "key": {
              "type": "object",
              "properties": {
                "jobId": {
                  "type": "string",
                  "minLength": 1
                },
                "taskOrdinal": {
                  "type": "integer",
                  "minimum": 0
                },
                "name": {
                  "type": "string",
                  "minLength": 1
                },
                "sizeBytes": {
                  "type": "integer",
                  "minimum": -1
                }
              },
              "required": [
                "jobId",
                "taskOrdinal",
                "name",
                "sizeBytes"
              ],
              "additionalProperties": false
            }
          },
          "required": [
            "key"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "kind",
        "stored"
      ],
      "additionalProperties": false,
      "description": "Existing c2j stored artifact reference; never a worktree, inbox, or external URL. Tenant is the input request tenant."
    },
    "Decision": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$"
        },
        "label": {
          "type": "string",
          "minLength": 1
        },
        "accepts_reviewed_content": {
          "type": "boolean"
        },
        "feedback_required": {
          "type": "boolean"
        }
      },
      "required": [
        "id",
        "label",
        "accepts_reviewed_content",
        "feedback_required"
      ],
      "additionalProperties": false,
      "description": "Recipes choose IDs and routing. Accepting reviewed content is incompatible with document annotations; feedback_required accepts nonblank feedback or annotations."
    },
    "Subject": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "minLength": 1
        },
        "version": {
          "type": "string",
          "minLength": 1
        }
      },
      "required": [
        "id",
        "version"
      ],
      "additionalProperties": false,
      "description": "Optional immutable subject identified by the recipe; outcome review uses cell identity and the verified candidate commit."
    },
    "FileSpec": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$"
        },
        "title": {
          "type": "string",
          "minLength": 1
        },
        "media_type": {
          "enum": [
            "text/markdown",
            "text/plain",
            "application/json"
          ]
        },
        "artifact_ref": {
          "$ref": "#/$defs/StoredArtifactRef"
        },
        "annotations": {
          "enum": [
            "none",
            "criticmarkup"
          ]
        }
      },
      "required": [
        "id",
        "title",
        "media_type",
        "artifact_ref",
        "annotations"
      ],
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "annotations": {
                "const": "criticmarkup"
              }
            }
          },
          "then": {
            "properties": {
              "media_type": {
                "const": "text/markdown"
              }
            }
          }
        }
      ]
    },
    "ReviewFile": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$"
        },
        "title": {
          "type": "string",
          "minLength": 1
        },
        "media_type": {
          "enum": [
            "text/markdown",
            "text/plain",
            "application/json"
          ]
        },
        "artifact_ref": {
          "$ref": "#/$defs/StoredArtifactRef"
        },
        "annotations": {
          "enum": [
            "none",
            "criticmarkup"
          ]
        },
        "sha256": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "download_url": {
          "type": "string",
          "minLength": 1
        }
      },
      "required": [
        "id",
        "title",
        "media_type",
        "artifact_ref",
        "annotations",
        "sha256",
        "download_url"
      ],
      "additionalProperties": false,
      "allOf": [
        {
          "if": {
            "properties": {
              "annotations": {
                "const": "criticmarkup"
              }
            }
          },
          "then": {
            "properties": {
              "media_type": {
                "const": "text/markdown"
              }
            }
          }
        }
      ],
      "description": "Runtime resolves exact bytes, computes SHA-256, and provides an authorized download URL; URL is presentation, artifact_ref is identity."
    },
    "ReviewSpec": {
      "type": "object",
      "properties": {
        "schema": {
          "const": "c2.review-spec/v1"
        },
        "title": {
          "type": "string",
          "minLength": 1
        },
        "summary_markdown": {
          "type": "string",
          "minLength": 1
        },
        "subject": {
          "$ref": "#/$defs/Subject"
        },
        "decisions": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/Decision"
          },
          "minItems": 1
        },
        "files": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/FileSpec"
          }
        }
      },
      "required": [
        "schema",
        "title",
        "summary_markdown",
        "decisions",
        "files"
      ],
      "additionalProperties": false,
      "description": "Recipe input at inputs.form.review. c2j supplies identity, hashes, and retrieval URLs."
    },
    "ReviewRequest": {
      "type": "object",
      "properties": {
        "schema": {
          "const": "c2.review-request/v1"
        },
        "title": {
          "type": "string",
          "minLength": 1
        },
        "summary_markdown": {
          "type": "string",
          "minLength": 1
        },
        "subject": {
          "$ref": "#/$defs/Subject"
        },
        "decisions": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/Decision"
          },
          "minItems": 1
        },
        "files": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/ReviewFile"
          }
        },
        "review_id": {
          "type": "string",
          "minLength": 1
        },
        "origin": {
          "type": "object",
          "properties": {
            "project_id": {
              "type": "string",
              "minLength": 1
            },
            "job_id": {
              "type": "string",
              "minLength": 1
            },
            "input_id": {
              "type": "string",
              "minLength": 1
            }
          },
          "required": [
            "project_id",
            "job_id",
            "input_id"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "schema",
        "title",
        "summary_markdown",
        "decisions",
        "files",
        "review_id",
        "origin"
      ],
      "additionalProperties": false,
      "description": "Immutable published request at form.review and review-request.json; runtime replays the same request for the same pending input."
    },
    "Annotation": {
      "type": "object",
      "properties": {
        "file_id": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$"
        },
        "base_sha256": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "format": {
          "const": "criticmarkup"
        },
        "markdown": {
          "type": "string",
          "minLength": 1
        }
      },
      "required": [
        "file_id",
        "base_sha256",
        "format",
        "markdown"
      ],
      "additionalProperties": false,
      "description": "Complete UTF-8 document with CriticMarkup suggestions. This is user feedback, never an automatic patch or repository destination."
    },
    "ReviewSubmission": {
      "type": "object",
      "properties": {
        "schema": {
          "const": "c2.review-submission/v1"
        },
        "review_id": {
          "type": "string",
          "minLength": 1
        },
        "submission_id": {
          "type": "string",
          "minLength": 1
        },
        "decision": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$"
        },
        "feedback": {
          "type": "string"
        },
        "annotations": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/Annotation"
          }
        }
      },
      "required": [
        "schema",
        "review_id",
        "submission_id",
        "decision",
        "feedback",
        "annotations"
      ],
      "additionalProperties": false,
      "description": "Client payload at FormResponse.review; authenticated submitter and timestamps belong to the runtime receipt."
    },
    "ReviewReceipt": {
      "type": "object",
      "properties": {
        "schema": {
          "const": "c2.review-receipt/v1"
        },
        "submission": {
          "$ref": "#/$defs/ReviewSubmission"
        },
        "user_id": {
          "type": "string",
          "minLength": 1
        },
        "submitted_at": {
          "type": "string",
          "format": "date-time"
        },
        "artifact_refs": {
          "type": "object",
          "properties": {
            "request": {
              "$ref": "#/$defs/StoredArtifactRef"
            },
            "submission": {
              "$ref": "#/$defs/StoredArtifactRef"
            },
            "annotations": {
              "type": "object",
              "additionalProperties": {
                "$ref": "#/$defs/StoredArtifactRef"
              }
            }
          },
          "required": [
            "request",
            "submission",
            "annotations"
          ],
          "additionalProperties": false
        }
      },
      "required": [
        "schema",
        "submission",
        "user_id",
        "submitted_at",
        "artifact_refs"
      ],
      "additionalProperties": false,
      "description": "Durable output at outputs.review; annotations artifact map is keyed by request file ID. Existing response mirrors submission.decision."
    }
  }
}
```

## Appendix B: complete examples

Save each block under its heading's filename in the same directory as the schema.
The source Markdown blocks are UTF-8, use LF line endings, and have exactly one
final newline. Their bytes determine the hashes and sizes in `request.json`.
The receipt's `sizeBytes: -1` values mean unknown size, as allowed by the current
stored artifact reference type; they are not content hashes.

### design.md

Original design document offered for review.

```markdown
# Design

Return matching items in stable order.
```

### test-statements.md

Original test statements offered for review.

```markdown
# Test statements

- T1: Results retain stable order. [files: search.test.ts; importance: high; level: integration; dependencies: none]
```

### spec.json

Recipe-supplied value of `inputs.form.review`.

```json
{
  "schema": "c2.review-spec/v1",
  "title": "Approve design and test plan",
  "summary_markdown": "Review the expected ordering behavior and its acceptance test before implementation.",
  "decisions": [
    {
      "id": "approve",
      "label": "Approve design and test plan",
      "accepts_reviewed_content": true,
      "feedback_required": false
    },
    {
      "id": "revise",
      "label": "Revise the plan",
      "accepts_reviewed_content": false,
      "feedback_required": true
    }
  ],
  "files": [
    {
      "id": "design",
      "title": "Design",
      "media_type": "text/markdown",
      "artifact_ref": {
        "kind": "stored",
        "name": "design.md",
        "stored": {
          "key": {
            "jobId": "job-build-demo",
            "taskOrdinal": 10,
            "name": "design.md",
            "sizeBytes": 49
          }
        }
      },
      "annotations": "criticmarkup"
    },
    {
      "id": "test-statements",
      "title": "Test statements",
      "media_type": "text/markdown",
      "artifact_ref": {
        "kind": "stored",
        "name": "test-statements.md",
        "stored": {
          "key": {
            "jobId": "job-build-demo",
            "taskOrdinal": 11,
            "name": "test-statements.md",
            "sizeBytes": 136
          }
        }
      },
      "annotations": "criticmarkup"
    }
  ]
}
```

### request.json

Runtime-published value of `form.review`, also stored as the request artifact.

```json
{
  "schema": "c2.review-request/v1",
  "title": "Approve design and test plan",
  "summary_markdown": "Review the expected ordering behavior and its acceptance test before implementation.",
  "decisions": [
    {
      "id": "approve",
      "label": "Approve design and test plan",
      "accepts_reviewed_content": true,
      "feedback_required": false
    },
    {
      "id": "revise",
      "label": "Revise the plan",
      "accepts_reviewed_content": false,
      "feedback_required": true
    }
  ],
  "files": [
    {
      "id": "design",
      "title": "Design",
      "media_type": "text/markdown",
      "artifact_ref": {
        "kind": "stored",
        "name": "design.md",
        "stored": {
          "key": {
            "jobId": "job-build-demo",
            "taskOrdinal": 10,
            "name": "design.md",
            "sizeBytes": 49
          }
        }
      },
      "annotations": "criticmarkup",
      "sha256": "489f63b748f8123b744c5b26dc7fb7da46c0ccfe0156557bcaee1a1c6e42762d",
      "download_url": "/api/projects/project-demo/jobs/job-build-demo/tasks/10/artifacts/design.md"
    },
    {
      "id": "test-statements",
      "title": "Test statements",
      "media_type": "text/markdown",
      "artifact_ref": {
        "kind": "stored",
        "name": "test-statements.md",
        "stored": {
          "key": {
            "jobId": "job-build-demo",
            "taskOrdinal": 11,
            "name": "test-statements.md",
            "sizeBytes": 136
          }
        }
      },
      "annotations": "criticmarkup",
      "sha256": "aba83f511f1431882e3e81ae09748e781467cb963b3abc85113df3e814d40141",
      "download_url": "/api/projects/project-demo/jobs/job-build-demo/tasks/11/artifacts/test-statements.md"
    }
  ],
  "review_id": "review-demo-1",
  "origin": {
    "project_id": "project-demo",
    "job_id": "job-build-demo",
    "input_id": "input-plan-demo"
  }
}
```

### submission-approve.json

Client value of `FormResponse.review` approving the unmodified review.

```json
{
  "schema": "c2.review-submission/v1",
  "review_id": "review-demo-1",
  "submission_id": "submission-demo-approve",
  "decision": "approve",
  "feedback": "",
  "annotations": []
}
```

### submission-revise.json

Alternative client value of `FormResponse.review` requesting revision with CriticMarkup.

```json
{
  "schema": "c2.review-submission/v1",
  "review_id": "review-demo-1",
  "submission_id": "submission-demo-revise",
  "decision": "revise",
  "feedback": "Specify the order and test equal timestamps.",
  "annotations": [
    {
      "file_id": "design",
      "base_sha256": "489f63b748f8123b744c5b26dc7fb7da46c0ccfe0156557bcaee1a1c6e42762d",
      "format": "criticmarkup",
      "markdown": "# Design\n\nReturn matching items in {~~stable~>creation-time~~} order.{>>Break equal timestamps by ID.<<}\n"
    }
  ]
}
```

### receipt.json

Runtime value of `outputs.review` for the revision submission. The HTTP success response also returns this under `review`.

```json
{
  "schema": "c2.review-receipt/v1",
  "submission": {
    "schema": "c2.review-submission/v1",
    "review_id": "review-demo-1",
    "submission_id": "submission-demo-revise",
    "decision": "revise",
    "feedback": "Specify the order and test equal timestamps.",
    "annotations": [
      {
        "file_id": "design",
        "base_sha256": "489f63b748f8123b744c5b26dc7fb7da46c0ccfe0156557bcaee1a1c6e42762d",
        "format": "criticmarkup",
        "markdown": "# Design\n\nReturn matching items in {~~stable~>creation-time~~} order.{>>Break equal timestamps by ID.<<}\n"
      }
    ]
  },
  "user_id": "reviewer-demo",
  "submitted_at": "2026-09-29T12:00:00Z",
  "artifact_refs": {
    "request": {
      "kind": "stored",
      "name": "review-request.json",
      "stored": {
        "key": {
          "jobId": "job-build-demo",
          "taskOrdinal": 12,
          "name": "review-request.json",
          "sizeBytes": -1
        }
      }
    },
    "submission": {
      "kind": "stored",
      "name": "review-submission.json",
      "stored": {
        "key": {
          "jobId": "job-build-demo",
          "taskOrdinal": 13,
          "name": "review-submission.json",
          "sizeBytes": -1
        }
      }
    },
    "annotations": {
      "design": {
        "kind": "stored",
        "name": "review-annotations/design.md",
        "stored": {
          "key": {
            "jobId": "job-build-demo",
            "taskOrdinal": 13,
            "name": "review-annotations/design.md",
            "sizeBytes": 105
          }
        }
      }
    }
  }
}
```

## Appendix C: standalone fixture validation

Place the eight blocks from Appendices A and B in one directory, then save the
following as `check_review.py` there. Run `uv run check_review.py`. This validates
the schema, payloads, hashes, byte sizes, and example provenance without c2j, a
recipes checkout, a database, or model calls. It does not replace NR-01–NR-12.

```python
# /// script
# dependencies = ["jsonschema>=4.23,<5", "rfc3339-validator>=0.1.4,<0.2"]
# ///
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

root = Path(__file__).resolve().parent

def load(name):
    return json.loads((root / name).read_text(encoding="utf-8"))

schema = load("v1.schema.json")
Draft202012Validator.check_schema(schema)
for kind, name in [
    ("ReviewSpec", "spec.json"),
    ("ReviewRequest", "request.json"),
    ("ReviewSubmission", "submission-approve.json"),
    ("ReviewSubmission", "submission-revise.json"),
    ("ReviewReceipt", "receipt.json"),
]:
    Draft202012Validator(
        {**schema, "$ref": "#/$defs/" + kind}, format_checker=FormatChecker()
    ).validate(load(name))

request = load("request.json")
for document in request["files"]:
    key = document["artifact_ref"]["stored"]["key"]
    content = (root / key["name"]).read_bytes()
    assert document["sha256"] == hashlib.sha256(content).hexdigest()
    assert key["sizeBytes"] == len(content)

for name in ["submission-approve.json", "submission-revise.json"]:
    submission = load(name)
    assert submission["review_id"] == request["review_id"]
    decision = next(d for d in request["decisions"] if d["id"] == submission["decision"])
    if decision["accepts_reviewed_content"]:
        assert not submission["annotations"]
    if decision["feedback_required"]:
        assert submission["feedback"].strip() or submission["annotations"]
    for annotation in submission["annotations"]:
        document = next(d for d in request["files"] if d["id"] == annotation["file_id"])
        assert annotation["base_sha256"] == document["sha256"]
        assert document["annotations"] == "criticmarkup"

receipt = load("receipt.json")
assert receipt["submission"] == load("submission-revise.json")
assert set(receipt["artifact_refs"]["annotations"]) == {
    a["file_id"] for a in receipt["submission"]["annotations"]
}
print("Schema, five payloads, document bytes, and example provenance validated.")
```

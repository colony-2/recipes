# Recipe kernel

`consultation.yaml` is the reusable conversation atom used by build for independent
assessment and by asynchronous cross-cell coordination.
The contract follows the [consultation specification](../../guides/PROPOSAL_CONSULTATION_SESSIONS.md).

A consultant decides agreement. Requester turns answer, negotiate, request expert
review, or cancel. The default budget is four consultant responses per round.
Messages use Codex's enforced `output.schema`: `outcome`, a concise shareable
`thinking` response, and `files` containing outbox-relative paths and descriptions.
The recipe checks artifact integrity and routing semantics without a second
schema validator or `result.json` readback.

## Include it

```yaml
- id: negotiate_api
  include: ./recipes/kernel/consultation.yaml
  inputs:
    thread: validation-api
    request: Agree a compatible strict-validation API and acceptance outcomes.
    consultant_cell: validation
    consultant_role: >-
      Evaluate whether this request fits the serving cell. Agree scope, interfaces,
      compatibility, acceptance outcomes, and conditions. Inspect PURPOSE.md when
      present and infer responsibilities contextually otherwise.
    requester_session: ${{ sequence.design.outputs.session }}
    documents: ${{ sequence.design.outputs.artifact_refs }}
    include_summary: true
```

Paths resolve relative to the including recipe; adjust the example accordingly.
Choose a distinct `thread` name for each topic in a job. Omit `consultant_cell` for
an expert inspecting the caller's current candidate. Explicit cell selection
opens a different workspace, even when selecting the same cell. For root
eligibility select the configured root and supply project-fit, overlap, and
technology criteria in `consultant_role`. This atom does not create repositories.

`consultant_ref` defaults to `main`; pass the configured target ref when different.
The first foreign turn captures the resolved base commit and later turns use that
commit, so a branch moving during negotiation does not silently change the target.
Requester and same-candidate expert turns inherit the caller's managed Git state.
All consultation turns use `const: true`; experimental edits do not advance that state.
Initial cell guidance is sent only when creating a session. Consultation purpose,
role, and advisory permissions are established once per participant: in
`instructions` for a fresh session, or the first prompt when entering from an
existing requester checkpoint. Permissions are scoped to this consultation so
the checkpoint can later seed real work. Follow-ups contain the new message,
new file pointers, and the current outbox prefix. New expert direction is
delivered once to each participant; the full setup and artifact inventory are
not repeated.

An existing caller should supply its full `requester_session` object. If omitted,
a requester session is created only when a reply is needed; immediate agreement
can therefore return an empty requester checkpoint. No diagnostic session ID is
used to resume work.

## Documents and results

Produce transferable documents at paths such as `iter1/requester/brief.md` and
`iter2/consultant/feature-spec.md`. Agents receive their current output prefix.
The shared agent turn supplies the actual inbox/outbox directories on every call,
including resumed sessions. `artifact-result.yaml` uses c2j's `path_match` to resolve
references against that turn's published documents. Exact matches win; otherwise
only a unique component-suffix match is accepted. `outbox/design.md` can therefore
select `design.md` without another agent turn. Stored artifact identities and
contents are unchanged. Logs and managed Git artifacts are excluded.

The default reference field is `files.*.path`. Callers can declare additional
`artifact_fields`; creation also resolves `cells.*.purpose_path`. Summary references
are matched against the conversation's final deliverables. Required documents,
iteration prefixes, duplicate references, and approval gates still apply after
matching for deliverable responses.

Build and creation `ask_user` responses request clarification before deliverables
may exist. They require usable questions, not files or phase documents. Optional
references are matched best-effort; missing or ambiguous ones are omitted from
the question form without an agent repair turn. The answer resumes the same
session and phase. The shared question form can carry supporting documents, but
clarification does not approve work. Formal reviews and consultation disagreement
reviews retain their artifact requirements.

For an ambiguous/missing reference or another correctable completed deliverable response,
`repair.yaml` prepares diagnostics in `repair.json` and preserves the response,
latest checkpoint, and all eligible output documents. The caller resumes that
same phase or participant; it does not rerun successful implementation or child
jobs. Result-only repairs run read-only against the managed Git candidate, including
registration evidence repairs after publication. Earlier output documents remain
eligible during repair, so a corrected reference does not require rewriting a valid
file.

Two automatic corrections are allowed per logical result. Further correction
requires a human review with the preserved documents and specific issues.
Direction or an attachment opens another bounded correction round; cancellation
stops the work. Empty retry feedback leaves the review pending. This review never
approves a build, authorizes publication, or declares consultation agreement.
Only a successfully validated consultation reply consumes a negotiation iteration.
Execution failures and unexpected direct job submission remain failures rather
than being retried as response corrections.

Supply only intended user documents, excluding managed Git snapshots and diffs.
Only listed output files are added to the exchange; experiments and logs are not
implicitly shared. Each turn's selected documents and prior exchanged versions
are bound into the next inbox. Keep supplied artifact-map keys equal to their native `name` fields: set bindings
materialize those names. `artifact-namespace.yaml` changes delivery names while
preserving immutable storage identities for aggregation across child jobs. Do not
supply `conversation.json`, which is reserved for the persisted conversation.

The terminal consultant publishes the full set of final documents in its file
list, republishing unchanged accepted versions when needed. `final_artifacts`
contains their native references. Their descriptions and all previous responses
remain in the conversation record.

| Output | Use |
| --- | --- |
| `outcome` | `agreed`, `declined`, `redirected`, `needs_review`, `cancelled`, or `failed`. |
| `assessment` | Expert verdict: `pass`, `revise`, or `not_applicable`; `not_applicable` for ordinary negotiation. Agreement and assessment are independent. |
| `requester_session`, `consultant_session` | Native latest successfully accepted checkpoints, kept separately. |
| `requester_start_session` | Original checkpoint for summary-based caller continuation. |
| `final_artifacts` | Exact terminal deliverables; dispositions other than agreement do not authorize implementation. |
| `artifacts` | All listed exchanged document references. |
| `state` | Typed conversation state, including counts, transcript, last message, and any failure. |
| `continuation`, `transcript` | The same persisted `conversation.json` artifact, usable for resumption or inspection. |
| `summary` | Optional `{text, outcome, final_artifacts}`; empty map when not requested or report generation failed. |
| `review` | Latest report's review documents, focused questions, and native form; empty when that report is a final summary. |
| `report_error` | Nonempty when independent synthesis failed; retry report preparation rather than inventing a summary or review. |

The caller may resume `requester_session`, supplying the terminal consultant
message and documents, or resume `requester_start_session` with `summary` and the
final documents. If unrelated work advanced the caller, deliver the summary to
that newer checkpoint. Choose a branch explicitly; do not merge session histories.
A requested summary is a prerequisite for summary-based continuation.

The calling snippet applies the decision. After its authorization gates, a
feature snippet submits target `build` without a session checkpoint, passing the
final agreement documents and transcript with an explicit execution request. Creation
also starts fresh with the agreed brief. Consultant checkpoints remain available for
consultation continuation; they are not implementation sessions. Expert
review feeds the current build. Agreement does not erase adverse findings or
replace normal review, verification, or merge gates. This atom submits no jobs.

## Expert direction and resumable rounds

When the iteration limit is reached or either participant requests deconfliction
with `needs_review`, an independent summary agent prepares `review.md` and focused
questions. The consultation itself presents a native review and waits for the
human's answers and optional attachments. No caller-side review wrapper, giant
JSON question label, or synthetic approval choice is needed. See the
[native review fixture](../../recipe-tests/fixtures/consultation-kernel-review.yaml).

The answers, review references, receipt, and attachments are recorded in the
transcript. Feedback opens a new bounded round using the same iteration limit
and both existing participant checkpoints. The requester responds to the
direction, then the consultant reassesses agreement. Further disagreement
requires another human review before another round; feedback never establishes
agreement automatically. When a requested final summary is produced, it reflects
the final outcome rather than the earlier disagreement.

If review preparation returns an unsuccessful result, the atom returns
`needs_review` with `report_error`
and saved state. Supplying its `continuation` retries review preparation and
waits for direction without restarting negotiation. A caller that already
obtained expert direction may instead supply `direction` and attachment
references in `documents` to open a bounded round explicitly.
Resubmitting a continuation from a returned unsuccessful turn retries the same participant
from the last accepted checkpoint without consuming or resetting iterations.
Invalid initial inputs are not retryable continuations. A caller that advanced
independently may also supply its current
`requester_session` when reopening; its original start checkpoint remains recorded.
Only the consultant can subsequently establish agreement.

An included consultation waits with its caller. Higher-level orchestration that
needs to advance independent work schedules consultation branches using
the runtime's job facilities; see `../develop/coordinate.yaml`.

Keep originating artifacts available for as long as their checkpoints and
continuations are needed. Session objects restore conversation state, not Git
state; cross-job callers must arrange the corresponding workspace separately.

## Implementation boundaries and tests

The public input schema uses strings, numbers, booleans, native checkpoints, and
artifact references. c2j currently reserves `type: object` for checkpoints and
rejects general map schemas. Internal included nodes carry native maps; public
resumption reads the persisted state artifact once. JSON encoding occurs only at
that artifact boundary, not inside agent prompts. No runtime changes are assumed.

`agent-turn.yaml` handles fresh/resumed Codex calls, schema enforcement, and static
read-only/mutating branches for consultation and build. Consultation owns its
participant roles, workspace selection, and file checks inline; there is no separate
consultation-turn wrapper. `consultation-report.yaml` prepares summaries and expert
reviews. `review.yaml` supplies build document reviews and feedback artifacts.
These helpers are internal includes, not standalone entrypoints. Their caller
supplies the structured inputs. The Codex selector follows c2ops' `published`
Nix package, with output schemas and initial-only instructions. The channel
advances after c2ops verifies its Linux packages and public cache downloads;
c2j records the resolved package for each invocation.

### Execution failures

`agent-turn.yaml` propagates execution failures, preserving the
original message, originating node, and structured failure. Build work,
independent assessment, and same-candidate expert calls use this behavior.
They do not route execution errors through a later shell command to fail again.
Completed responses with correctable schema or artifact problems still use
the normal result-repair loop.

Consultations, consultation reports, and creation calls use the same propagation
behavior. A caller that has a specific recovery action can use the existing
`catch` mechanism on its include; the shared helpers have no failure-mode switch.
Returned unsuccessful agent results remain distinct from execution errors and
can still follow the existing result-handling and continuation paths.

Build's `rejected` state is only for invalid requests or rejected returned
results, where there is no unhandled execution exception to propagate. Current
c2j has no standalone failure node, so this deliberate rejection still uses a
command with `catch.fail`, publishing `BUILD_REJECTED` and the specific reason.
It cannot replace an execution failure from an agent or assessment.

Focused regression suites are `agent-failure.test.yaml`,
`build-failure.test.yaml`, `consultation-failure.test.yaml`, and
`consultation-report-failure.test.yaml` in `recipe-tests`.
They cover propagation through includes to a caller catch, consultation and
assessment errors, rejection diagnostics, and normal completed-result routing. Their fast
cases mock operations; the invalid-directory case uses the native runtime.

Run the native suites with a current c2j and the op's declared tools available:

```sh
c2j test run --file recipe-tests/consultation-kernel.test.yaml
c2j test run --file recipe-tests/consultation-kernel-handoff.test.yaml
c2j test run --file recipe-tests/consultation-kernel-resume.test.yaml
c2j test run --file recipe-tests/consultation-kernel-review.test.yaml
c2j test run --file recipe-tests/consultation-kernel-retry.test.yaml
c2j test run --file recipe-tests/consultation-kernel-invalid-resume.test.yaml
```

Codex responses are mocked; Git workspaces, immutable checkpoints, artifact
materialization, included recipes, and human review transport run through the
native runtime. No live model calls or repository provisioning are required.
[Test statements](../../recipe-tests/consultation-kernel-statements.md) define the
expected outcomes. Worker crashes and low-level replay fault injection remain
c2j's responsibility; recipe tests cover state continuation across invocations.

Validated on 2026-10-21 with c2j main `94484c909de1`: all 39 consultation runtime
cases passed, including approximate references, bounded result repair, summary
repair, and checkpoint preservation. Build integration and the matching/repair
helpers have separate native suites.

## Stage recovery and target routing

`recovery.yaml` records stage errors and retained evidence in recovery artifacts.
Only callers explicitly declaring a safe repeat get two automatic retries. Otherwise
human direction or cancellation is required. This gate does not replay any operation;
the caller selects the exact resume point. Human recovery direction never grants
publication approval. File accounting uses it for validator execution errors; light
coordination preserves failed children without resubmission; creation uses it to
recover catalog application after publication.

`resolve-target.yaml` resolves naming in a read-only empty scope and probes Git refs
before serving checkout. It distinguishes ready, absent local repositories, empty,
missing ref, and unknown access. `route-target.yaml` preserves the original request,
submits/reuses root creation through `create-request.yaml`, and validates creation
and registration evidence before permitting a serving consultation. Root creation
has its own human review and may be coordinated by the light workflow.

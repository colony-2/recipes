# Adaptive3 follow-up implementation

Work requested on 2026-11-13 against [TODO.md](TODO.md) and
[the audit follow-up plan](PLAN_AUDIT_FOLLOWUPS.md). This record separates delivered
behavior from external requirements and test limitations.

## Milestone 1: usable feedback and shared validation

- Review and Resolver use `feedback` and `annotations`, with `revise` as the
  discussion action. All readers and tests changed together. Empty discussions
  reopen the form without calling an agent. Resolver answers retain their session.
- Confirmed the reported UI cause in Cortex main `ba5ed5b`: its review renderer
  specifically recognizes the field `feedback` for the action dialog.
- Configured specialists now run in Validate using its common prompt/schema.
  The fixed stage mapping and assessment guidance live there. Research remains
  in Execute. Required native/specialist/general findings are combined, including
  multiple failures; optional advice alone does not prevent acceptance.
- Corrections repeat full validation. No new specialist recovery loop, approval
  file or work ledger was added.
- Repaired an older false-positive const test: it now finishes the cycle and
  verifies that a planning write does not enter later workspaces or the repository.

Targeted native checks: five cycle cases, three resolver cases and four configured
validation cases passed. Two consumer tests passed using actual native forms and
Cortex's real adapter/renderer: click, type, upload, Back and submit. The consumer
check uses jsdom, not a deployed browser. The full milestone regression run passed all 51 native cases; source validation
also passed.

Native runs use the pinned c2j `c244db8`. As in the initial implementation, this
host requires a disposable copy with validator `execution_needs` removed and
preinstalled dependencies on PATH. Recipe graph, scripts and prompts remain the
same. This does not verify normal worker dependency provisioning; see
[RUNTIME_REQUIREMENTS.md](RUNTIME_REQUIREMENTS.md).

## Milestone 2: complete results and useful review content

- Removed the generic child-title fallback. An assignment without a title returns
  to its receiving author through Execute and full Validate before submission.
  Probe titles name the requested tools; resolver titles name the stage/request.
- Direction requests a per-cell Core code / Tests / Docs table with qualitative
  scope only. Outcome requests measured additions/removals, per-file support,
  separate cells, honest binary handling and completed-versus-pending owner work.
  Test frameworks, harnesses and fixtures explicitly count as test code.
- The existing approved-change validator emits Git's exact per-file numstat as
  a diagnostic file for validation. It neither classifies files nor invents a
  workflow accounting object. The assessor requests missing/inconsistent reports;
  the producer corrects them through the complete cycle.
- New-session instructions explain task occurrence IDs, field pointers, exact
  downloads, pagination, failed-task outputs, attempts and restart discovery.
  Inspection downloads stay in scratch.

Checks: incomplete child title corrected before one submission; incomplete outcome
report returned through two full validations; nine real validator tests, including
numeric and binary Git measurements; four package and three resolver regressions.
The inspection fixture runs the real CLI inside a native task, reads fields and
artifacts beyond the first page and retrieves exact bytes beyond a truncated
preview. Report-quality decisions are scripted in these orchestration tests;
they do not establish the quality of model writing or semantic classification.

## Milestone 3: human-directed model settings

- `build` and `adaptive3` accept optional `model` and `reasoning_effort` inputs.
  A two-field private `agent_settings` value carries only invocation choices
  through the existing activities. Resolver overrides persist for later stages.
- Each field independently uses the latest human choice, then the job input.
  Absent keys stay absent; c2ops applies `codex_model` and
  `codex_reasoning_effort`, or its own unspecified behavior. No model names or
  reasoning defaults are hardcoded in the recipe.
- The resolver's native form accepts explicit model/effort fields even when no
  model runs. Rejected choices show the actual error and attempted settings and
  return to that form. Questions do not authorize continuing work. Prose-only
  model suggestions are explained in review; the human enters the choice in
  the explicit fields. Agents do not select replacements.
- Direct Nix selector calls remain required. The full native cancellation test
  caught that generic `extension_execution` cannot prepare a Nix selector; mocked
  calls had hidden this. The corrected adapter uses four optional-setting variants
  for each existing call, sharing the call through YAML anchors. Exactly one op
  runs per turn. Unset inputs stay omitted in authored calls; the manifest applies
  defaults (including null when no setting exists). API-secret binding stays as before.
- Corrected an accidental field-name edit in the earlier feedback change that
  had made integration ignore its supplied commit message. Added an assertion
  that the actual squash receives the assignment text.

The four native model scenarios cover omitted fields, independent job overrides,
worker-default delegation, repeated provider failure and persistence after human
correction. Direct-selector mocks observe prepared inputs, including manifest defaults. The c2j `TestCodexConfigurationDefaultsMatrix` and
`TestConfigurationDefaultRequiredAndNested` tests passed for actual default
materialization. These checks do not invoke a model provider. The real prepared-operation cancellation
barrier verifies that the Nix adapter can start and remains cancellable. Resolver dialogue regressions and consumer checks cover the native form.

The runtime test pin advances to c2j main `3fec5e4`. No c2j source was changed.

## Milestones 4–6: requester recovery, continuation and local allowances

- Direct agent submissions and recipe delivery use the same terminal-result path.
  A failed or cancelled child returns its native identity, message and selected
  result/error directories to the requesting agent. The requester decides whether
  to retry, adopt existing work, continue or report that it is stuck. Invalid agent
  reports retain native submitted-job identities, so correction does not lose
  already-started children. Existing active and successful jobs can be consumed
  without another submission. Nested owner sessions are retained.
- Diagnostics retain original relative names under separate job/task/cause
  directories. Hook results cannot overwrite the current human review. Prepare
  failures return to the working agent; publish failures retain both the completed
  merge and the command log. Configured specialist failures join those findings.
- `resume_from` enters the resolver before configuration or work. It selects the
  remaining stage and recovers selected documents, original receipt values and
  recorded merge results, with their source job/task. There is no recovery manifest.
  Configuration preserves that choice; stage inputs do not assume earlier stages
  ran in this job. Missing history access asks a specific question. An approval
  without a patch cannot trigger unchanged-patch comparison.
- The resolver uses one agent conversation for investigation and dialogue, including
  repeated questions. A human model change starts a fresh invocation with the new
  settings, so an older answer cannot override the latest attempt.
- Automatic work corrections default to four; owner exchanges, child-result rounds
  continuations and package attempts have separate finite allowances. Nested owners have their
  own correction counts and finite nesting depth. Merge chasing keeps its own count
  across stage visits. Zero does not mean unlimited. An exhausted loop reports its
  own counts and limits in native state. A resolver can grant 1–20 further attempts
  to that loop; other counters remain unchanged. After two automatic resolver
  corrections, explicit human continuation is required. Questions remain unlimited.

The full regression run also exposed a model-variant bug: YAML merge anchors had
inherited the base node ID. Every variant now has its own ID, matching the state
whose result is read. The targeted model tests pass with this correction.

Tests distinguish orchestration from agent judgment. Continuation tests script the
resolver's recovered records and stage decision, then exercise native configuration,
managed workspaces, full validation and merge/publication routing. They do not prove
that a model will correctly interpret every prior history. The separate inspection
test exercises real pagination and exact CLI retrieval. The cancellation-message
case scripts a terminal child response; native parent cancellation is separately
covered by the prepared-operation barrier.

## Remaining external requirements

Compact directory references cannot be implemented against the current runtime.
The real collection test delivers 1,024 files but measures 202,940 bytes of expanded
reference metadata. [The runtime requirement](RUNTIME_REQUIREMENTS.md#4-transport-a-selected-directory-as-one-native-reference)
defines the missing c2j and Cortex contract; no custom archive or manifest was added.

[The requested Cortex job audit](AUDIT_3M28e5.md) found a real Pillow activation
failure and a recovery consultation blocked by that same validator. The local test
lane does not verify worker package activation. No deployed job or c2j source was
modified. Native dependency activation and the already-documented notification of
still-open children remain external requirements.

## Checklist against the requested plan

| Todo | Result | Principal checks |
| --- | --- | --- |
| 1. Human-directed models | Implemented; absent inputs use worker defaults, native form remains available after provider failure. | Four model cases, runtime default tests, real prepared-operation cancellation. |
| 2. Incomplete results | Implemented; no child-title filler, invalid reports preserve submitted children, missing content returns through the full cycle. | Title correction, invalid-report recovery, package and report validation. |
| 3. Scope and measurements | Implemented; qualitative per-cell 1p table and actual outcome counts including test frameworks. | Missing-report correction, real numeric/binary Git measurements, assessor instructions. |
| 4. Requester-led child recovery | Implemented; success/failure/cancellation messages reach the requester; correction, retry and adoption use native identities. | Real successful/failed/retried children, active/completed adoption, scripted cancellation message. |
| 5. Resolver-first continuation | Implemented; recover original records and selected artifacts, configure, then run the chosen stage's full cycle. | Approved implementation, changed scope, inaccessible history, remaining publication, recovered work classification. |
| 6. Diagnostic directories | Implemented with existing file refs; original producer/cause paths and bytes survive. | Same-named logs, nested causes, prepare/publish failures, specialist errors. |
| 7. Shared specialist validation | Implemented; fixed stage policy, common assessment and complete current findings. | Required rejection, optional advice, full rerun, native error and hook guidance. |
| 8. Local automatic limits | Implemented; independent counters, finite renewal and a separately bounded resolver. | Counter isolation, zero fallback, human discussion, finite renewal, real repeated upstream advancement. |
| 9. Inspection guidance | Implemented in initial context; exact task fields/artifacts and pagination are explained. | Real CLI retrieval beyond page one and beyond previews. |
| 10. Compact directory refs | Blocked on a missing runtime/consumer contract; selected relative subtrees and small presentation fields are used today. | Native 32-file and 1,024-file transport with measured metadata growth. |
| 11. Feedback UI | Implemented; supported field/action names, retained conversation and empty-discussion handling. | Native forms plus three real Cortex renderer/adapter DOM tests. |

A failed child may have no final output at all. In that case the requester receives
its identity and original failure message plus instructions to retrieve intermediate
task outputs through job inspection. The recipe preserves diagnostics returned by
the native wait, including command logs, but does not invent a final result or
pretend it has downloaded intermediate artifacts that the wait did not return.


Final validation: all 82 native cases have passing results after the documented
fixture/expectation corrections and targeted follow-ups; all source cases validate.
Nine direct validator tests and three actual Cortex DOM integration tests pass.
The execution-lane and live-worker limitations are detailed in
[TEST_RESULTS.md](TEST_RESULTS.md#follow-up-implementation-results).

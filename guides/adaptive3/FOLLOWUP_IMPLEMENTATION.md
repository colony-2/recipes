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

## Remaining milestones

Model overrides, reporting, requester-led recovery, resolver-first continuation,
diagnostics, local allowances, inspection guidance and directory transport remain
in progress. The todo list is the completion checklist.

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

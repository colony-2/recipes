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

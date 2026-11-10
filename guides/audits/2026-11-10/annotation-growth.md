# Fix duplicated review annotations after successful publication

## Incident and ownership

Job `3LtEddFZ73GwSmaEpKXc9I6ozD4` merged c2j commit
`b95477aa01bea5551c8bc76f63f5cc8c734e2536`, then failed to save its final
result. JobDB reported 312,473 bytes against its 262,144-byte application limit.
The annotations array alone contained 589 entries and occupied 297,747 bytes.
The captured recipe was `1006fc4`.

This fits the recipes cell. Adaptive2 inspection returns its input annotations
plus new annotations; outcome accounting appends the input again. Repeated
reviews amplify duplicates. Working turns also keep descriptors for superseded
or no-longer-selected document versions.

## Plan

1. Give inspection one contract: return current documents and their complete
   current annotations. Callers consume that list without appending history.
2. Select the last matching descriptor for each current document ID and immutable
   artifact identity. Ignore the artifact's delivery name when comparing identity.
   Keep source references, producer identity, titles, and attachment lineage.
3. Apply that selection at working-turn records, inspection attempts, and final
   output assembly. Keep evidence files and original task histories intact.
4. Test repeated human outcome revisions through native build, verification,
   review and merge. Measure the final serialized result and prove the previous
   recipe fails the regression. Test descriptor replacement and source identity,
   and rerun review evidence, repair, consultation and merge-approval regressions.

No arbitrary evidence cap, archives, hidden truncation, new agent task, or runtime
payload-limit change. This fixes annotation growth, not every conceivable large
result from an unbounded collection of distinct deliverables.

## Test statements

| Expectation | Priority | Kind / dependencies | Files |
| --- | --- | --- | --- |
| Repeated outcome revisions complete and publish without duplicating current document metadata or exceeding the result limit. | Critical | Integration / native c2j, Nix | `annotation-growth.test.yaml`, `develop.yaml`, `workflow.yaml` |
| The final result describes exported document versions and keeps their evidence references intact. | Critical | Integration / native c2j, Nix | `annotation-growth.test.yaml`, `current-annotations.yaml` |
| The latest matching descriptor replaces older metadata for the same document without accepting stale artifact identities. | High | Integration / native c2j | `current-annotations.test.yaml`, `current-annotations.yaml` |
| Aliased attachments preserve producer identity, lineage and source order. | High | Integration / native c2j | `current-annotations.test.yaml`, `annotation-identity.test.yaml` |
| Corrected review reports retain required attachments and valid source links. | Critical | Integration / native c2j, Nix | `review-packet.test.yaml`, `review-links.test.yaml`, `visual-evidence.test.yaml` |

New test paths are under `recipe-tests/adaptive2/`; annotation identity tests are
under `recipe-tests/adaptive/`. Production paths are under `recipes/adaptive2/`.

## Implementation assessment

All four plan items are implemented. `inspect.yaml` now returns the complete
current annotation list, and assessment/accounting consume it directly. Assessment
also passes the incoming annotations explicitly. The empty-sequence
`current-annotations.yaml` include selects the last matching descriptor at each
working record, inspection attempt and final export. It adds no agent or command
task. Selection uses the existing review policy: exact delivery ID and immutable
reference, ignoring only the reference's delivery name.

The selection preserves each surviving record intact, including unresolved source
claims, producer origin, source order and lineage. It does not remove files,
retarget old descriptions to new content, limit human turns, or change approval
and publication behavior. Historical annotations remain in their original task
outputs instead of being copied into every subsequent result.

### Validation

The new native regression runs the public `build.yaml` with scripted Codex
responses, real artifact storage, five native human review receipts, verification
and a Git merge into a disposable repository. It produces 24 separate evidence
logs over four implementation rounds. Model judgment is scripted; orchestration,
artifact transport and payload-limit enforcement are real.

- **Before:** running the same fixture against an isolated checkout of `e5f0af2`
  merged revision 4, then failed saving its final result: **627,972 bytes**, of
  which **612,832 bytes** were annotations, against the **262,144-byte** limit.
- **After:** the job completes with **31 current annotations**, **36 exported
  document references** and a **39,939-byte** compact JSON result. All 24 separate
  evidence logs and the merge summary's 26 source references are retained.
- Four selector cases check latest matching descriptors, stale identities, aliases,
  source order, unresolved source claims and empty selections.
- Two report-correction cases now verify that repeated corrections, including a
  human allowance increase, return three current annotations and retain the final
  gallery and screenshot links.

The native payload limit plus assertions on unique IDs, current immutable
references, source identities and successful merge catch this regression. The
reported JSON size is measured from the captured final output; it is not a new
recipe limit. A genuinely large set of distinct deliverables can still exceed
JobDB's limit. This change addresses repeated and obsolete metadata.

Using pinned c2j **0.0.124**, **39 native cases passed** across annotation
selection/growth, report corrections, public build delivery, visual evidence,
review links, consultation, handoff, merge approval reuse and annotation identity.
All **103 adaptive2 cases structurally validated**; that count is validation, not
execution of the whole suite. `git diff --check` passed. No live jobs were changed
or restarted for this fix.

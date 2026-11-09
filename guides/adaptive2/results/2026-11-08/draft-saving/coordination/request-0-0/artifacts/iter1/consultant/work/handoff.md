# storage — bug — atomic conditional draft writes under overlapping calls

Notebook's original problem is that unfinished text is lost when users switch notes. The requested direction adds saving while typing, keeps manual Save, and shows saving/saved/failed/conflict states, including two tabs and uncertain network outcomes. Reusing the existing draft API avoids a new endpoint, but its version check must prevent one accepted concurrent write from silently overwriting another. This follow-up repairs the supplied model's demonstrated concurrency gap.

## Expected and observed behavior

Expected: for two different texts submitted to one draft with the same current expected version, exactly one write commits and advances the version; the other raises Conflict with the now-current version and does not mutate storage. This invariant must hold when calls overlap, not just when they are made sequentially.

Observed: `drafts.py` reads/checks the version at lines 15–17 and assigns at line 19 without synchronization. Two calls can both pass the check, both return success at version 1, and retain only one of their texts. The README describes stale-version rejection, but the supplied test exercises sequential writes only.

## Reproduction and evidence

- Storage baseline: commit `4bfd5bd201e5e311442950dc394951e19171dc62`.
- [Source snapshots](../evidence/sources.md), especially drafts.py lines 12–20 and test_drafts.py lines 11–16.
- Both current tests pass: [baseline log](../evidence/baseline-tests.txt).
- Run `python3 /path/to/evidence/probe.py /path/to/storage-checkout` on the unchanged baseline. The probe uses a thread-local trace/barrier immediately before assignment to choose a valid overlapping schedule; it makes no source/method/local-variable modifications. [Output](../evidence/probe-output.txt) records the race in three trials.
- The probe is a baseline diagnostic, not a regression test to preserve verbatim: a correct critical section could prevent the second thread reaching the internal barrier. Write a concurrency test suited to the repaired synchronization boundary.

## Fix scope

Owner: **storage**. Work kind: **bug**. Status: agreed future scope, **blocked on notebook's requested human direction approval**, not authorized implementation in this advisory turn.

Make the entire read/version-compare/update operation atomic for overlapping calls on a shared Drafts instance. Keep existing GET/PUT shape, missing-note empty text/version 0, successful monotonic increments, exact text, inclusive 65,536-byte UTF-8 limit, and Conflict behavior. Choose a simple synchronization mechanism appropriate to this pure in-memory model. Add regression coverage that meaningfully exercises competing writers and document the concurrency boundary/assumptions.

No autosave-specific endpoint, idempotency-key feature, unconditional overwrite, UI/offline work, new HTTP server, persistence backend, or migration belongs in this fix. Do not interpret the model's dict as proof of production durability.

If the actual serving layer is provided, verify that all writers use atomic compare-and-write against one authoritative store and that reconciliation reads are current. A single-instance lock does not solve independent worker stores or a distributed backend. A larger deployment change requires concrete adapter/topology evidence and a revised storage-owned scope; it is not implicitly authorized here. Existing globally serialized handling could mean no deployment storage change is needed, but that must be demonstrated rather than assumed.

## Regression expectations and acceptance

1. Two competing writes with the same expected version to one draft yield exactly one success, one Conflict reporting the winning current version, one version increment, and the winner's text retained. Include creation from version 0 and update of an existing draft.
2. Sequential valid writes still increment once each; repeated/stale attempts never replace the accepted text. A lost-response retry with the original version conflicts after commit and GET returns the committed snapshot/version.
3. Existing tests pass. Exact Unicode text, empty text, boundary acceptance at 65,536 UTF-8 bytes, and rejection at 65,537 bytes remain intact, with rejected writes leaving the draft unchanged.
4. Return verification evidence and explicitly state the scope proven (shared in-process instance versus actual HTTP/worker deployment). Do not report end-to-end simultaneous-tab safety unless the serving layer has been verified.
5. Notebook retains its own per-note request serialization and conflict/recovery behavior; the fix must preserve its current GET/PUT compatibility.

## Required inputs, unresolved choices, and references

Required before implementation: the enclosing coordinator's direction approval and this handoff. Current sources suffice for the model correction. Actual connection/routes, handler source, concurrency topology, and cache/read-consistency configuration are needed only to verify deployment behavior; none is supplied by this checkout or available `c2j self` discovery.

Storage chooses the internal synchronization detail. Unresolved integration facts are the serving model, fresh-read guarantees, and exact HTTP error serialization; do not invent these in a model fix. These factual checks do not require asking the human to choose a technical mechanism.

Consultation: `3LqEUMQeF5AkHjjMaa7uzmhwnKW/request-0-0`, Storage API owner; requester input `inbox/request.md` (Notebook feature consultation: preserve unfinished notes when users switch notes). See [consultation summary](../summary.md) and [full findings](../findings.md). Advisory only: no job submission, implementation, or deployment was performed.

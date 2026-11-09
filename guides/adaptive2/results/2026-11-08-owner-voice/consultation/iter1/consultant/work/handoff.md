# Recover earlier note text

People need to recover text overwritten by a successful save, including after closing their browser or using another device. You will handle selection and preview in notebook. I will add bounded history to storage and keep restoration within the existing conflict-checked write contract.

## Desired behavior

Keep the current draft and up to **three earlier saved text states per note**, newest first. Three means three recovery choices in addition to the current note. Retention is by count, with no time expiry in this feature. Existing notes begin accumulating history on subsequent saves; text overwritten before history was enabled cannot be recovered.

For each successful write that changes the text, archive the displaced current `{text, version}` if it represents an actual save, then retain only the newest three entries. The absent-note value `{text: '', version: 0}` is a placeholder and must never become a historical entry. An explicitly saved empty string is a real state and can be archived and restored.

Consecutive identical saves must not add or evict history entries. They must still check the supplied version and increment the current version on success, as existing clients expect. Archive the latest version of that unchanged state when its text is eventually replaced. Compare text exactly; do not trim or normalize it. Nonconsecutive repetitions remain separate states: restoring A after B is a new save of A, not a reason to remove an older A from history.

For example, saves `A, A, B, C, D, E` produce current `E@6` and history `[D@5, C@4, B@3]`. The second A advanced the version but did not consume a history slot. Before B was saved, history was empty; after B, it contained `A@2`.

## Interface and restoration

Add `history(name)` to the Python interface and document `GET /drafts/{id}/versions`, returning a newest-first array of `{text, version}` entries for earlier states only. Return `[]` when no history exists. Including text supports your selection and preview without a separate fetch endpoint. History must use the same note identity and access boundary as the current draft.

Keep existing GET and PUT request/response shapes unchanged. To restore an entry, you submit its text through `PUT /drafts/{id}` with the current version that notebook last read or successfully saved. Never submit the historical entry's version as the write precondition, and never silently fetch a newer token to force restoration through.

A successful restore creates a new current version and archives the displaced text under the same rules as any save. Restoring text already current still advances the version without adding history. A concurrent change produces HTTP 409 with the current version and changes neither current text nor history. You retain the user's unsaved or selected text and let them resolve the conflict; do not blindly retry with the newer token. A lost successful response uses the existing read-and-compare recovery procedure.

## Persistence, limits, and compatibility

Commit current text, version, history insertion, and pruning atomically. The version precondition must hold across writers using the same durable store, not just within one Python object. Validation failures, stale writes, and failed transactions must leave both current and historical state unchanged.

Persist history beside the current draft in server-owned storage. The supplied repository only contains a Python model backed by a dictionary; it has no durable backend or HTTP server. I recommend a file-backed SQLite implementation as the minimal default here, unless an existing transactional service backend is established during implementation. Keep the existing zero-argument `Drafts()` model usable for compatibility and provide an explicit durable-store configuration. Recovery-enabled serving must use that durable store, and all requests for the same note must reach the same data. Reopening it must retain current text, versions, and history.

Implement the storage behavior and API contract in this repository without adding a web framework. Document the service integration requirement: the serving draft API must expose the history read and use the durable backend on persistent storage. Local model checks alone cannot establish that deployment or demonstrate recovery between devices.

Preserve valid UTF-8 input and the existing limit of 65,536 encoded bytes per saved text, including empty text. Reject oversized input without truncating it or disturbing history. Three full-sized historical texts require at most 192 KiB of raw text per note, or 256 KiB including current text, before metadata and encoding overhead. Existing large drafts within the limit remain accepted.

## Scope and differences from your proposal

I will implement history, persistence, API documentation, and regression checks. You own version selection, preview, restore confirmation, serialized writes, conflict presentation, and unsent browser text. A separate restore endpoint, autosave endpoint, offline sync, unlimited history, and a full audit trail are outside this change. The existing save operation already supplies the restoration behavior and conflict protection we need.

The recommended defaults resolve the open retention, repeated-save, empty-text, size, and concurrent-edit choices above. Persistence integration is the remaining deployment dependency; there is no demonstrated serving configuration in the supplied repository.

## Acceptance

- Existing read/write tests and response shapes continue to pass; ordinary and identical successful writes still advance the version.
- History is isolated per note, ordered newest first, bounded to three earlier states, and empty for an absent note. A preexisting current draft becomes recoverable when first replaced.
- Check the `A, A, B, C, D, E` example, repeated identical saves with full history, and nonconsecutive repeated text. Identical saves never evict history.
- Saving empty text over a nonempty note and restoring either state works. Never archive the version-zero placeholder.
- Accept exactly 65,536 UTF-8 bytes, including multibyte text. Reject larger or unencodable input without changing current text or history.
- Restore through the ordinary write operation. Test stale normal writes, stale restores, and stale identical writes; each conflicts without mutation. A successful restore preserves the displaced state subject to retention.
- Exercise two writers sharing the durable store: competing writes with the same expected version cannot both succeed. Test rollback so failed writes cannot leave partial history or pruning.
- Reopen the configured durable store and verify current text, monotonic versions, history, and note isolation. Document how the serving API uses it, and distinguish this check from an end-to-end browser/device check.

The [current implementation evidence](../evidence/current-behavior.md) records the baseline for compatibility.

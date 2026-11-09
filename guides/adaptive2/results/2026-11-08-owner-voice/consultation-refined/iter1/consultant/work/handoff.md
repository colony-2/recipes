# Recover the three earlier saved versions

People need the text they accidentally overwrote to remain available after closing a browser or opening the same note on another device. I will add bounded, durable history to storage. You will provide version selection, preview, and the recovery interaction in notebook.

## Desired behavior

For each note, retain its current saved text and up to three earlier saved states, newest first. I interpret “three versions” as three recovery choices in addition to the current text. This uses at most four text records per note and gives people three chances to recover an overwrite.

On a successful save that changes text, archive the previously saved current state, replace the current state, and discard history beyond the newest three entries. Treat text equality exactly, without trimming whitespace or normalizing Unicode. A return to text seen earlier is a new change; suppress only consecutive identical saves, not all duplicate text across history.

An unchanged save must still advance the current version token, as it does today, but must not add, replace, or evict a history entry. When that current text is eventually displaced, archive it with its most recent successful version token. History identifies saved states, not every save attempt.

The absent draft's empty text at version zero is a placeholder, not a saved version, so never archive it. The first successful save creates the current state with no history. An explicitly saved empty string is a real state: clearing a note preserves its former text, and the saved empty state can later appear in history and be restored.

Keep the existing limit of 65,536 UTF-8 bytes per text, including empty text as valid input. Reject invalid UTF-8 and oversized input without changing current text, tokens, or history. Four maximum-size records contain at most 256 KiB of text per note; database metadata and transaction files add overhead. Retention is by count, with no time expiry. Frequent autosaves with actual text changes can consume all three history slots quickly; the default introduces no time grouping or separate manual-save category.

## Read and restore contract

Preserve `GET /drafts/{id}` and `PUT /drafts/{id}` and their existing `{text, version}` shapes. Add a history read modeled by `Drafts.history(name)` and documented as `GET /drafts/{id}/history`:

```json
{
  "currentVersion": 7,
  "versions": [
    {"text": "Earlier text", "version": 6}
  ]
}
```

Return up to three complete historical texts in descending saved-version order and read `currentVersion` and history from one consistent snapshot. A new or absent note has an empty list; an absent note reports `currentVersion: 0`. The bounded response supplies previews without another detail endpoint. Historical tokens can have gaps because unchanged writes still advance the current token. Use the same note identity and access boundary as current draft reads.

I recommend no separate restore mutation. You can submit the selected historical text through the existing `PUT`, using the history response's `currentVersion` as the expected current version, never the selected entry's historical token. This creates a new current version; it does not rewind the token. If the text changes, it archives the displaced current state, allowing the user to undo the recovery while that entry remains retained. The selected entry otherwise stays subject to normal retention.

If another tab saves after the history snapshot, the restore must return the existing conflict result: HTTP 409 with the current version and no mutation. You should preserve the selected and unsaved text, refresh for comparison, and let the user decide whether to retry; do not fetch a new token and silently repeat the overwrite. A response lost after a successful save is handled by reading and comparing current text, as documented today. A historical text already fetched can be saved even if its history entry has since been pruned, provided the current-version check succeeds; this is an ordinary text save.

## Storage work and compatibility

I will implement durable storage of current text, current version, and history together. I recommend a configurable, file-backed SQLite store using Python's standard library for this repository. Keep no-argument `Drafts()` construction usable as an isolated in-memory model for existing callers and tests; application startup must explicitly configure a durable database path. Preserve the `read` and `write` call signatures, returned copies, `Conflict(current_version)` behavior, size validation, and version increment on every successful write, including unchanged writes.

Use a transaction to check the expected version, archive if necessary, update current state, and prune history. Reads must not see a partially completed save. Independent connections to the same database must not both accept writes against the same expected version. A conflict or failed transaction leaves current text and history unchanged. Reopening the store must preserve the complete committed state, including tokens, and a save must report success only after commit.

The checkout contains a pure API model and documentation, with no HTTP router or deployment configuration. I will add the model operation, durable implementation, checks, and API/startup documentation here. The deployed service must map the documented history read and point sessions from all devices at the same durable store. SQLite assumes the service uses one suitable persistent database location; a deployment with independent hosts or ephemeral disks would need a shared durable backend before this feature can promise recovery across those instances. No deployed route or storage topology was available to verify here.

Existing clients continue saving normally and automatically generate history. There is no existing durable schema to migrate in this checkout, and past overwritten text cannot be reconstructed. If an integration has an existing current draft to import, treat it as the current state without inventing earlier history.

## Scope and acceptance

Storage owns persistence, retention, atomic conflict handling, the history read, and their documentation. You own preview, selection, save orchestration, and conflict handling in notebook. Unsent browser text, offline recovery, time-based checkpoints, a full audit trail, and a separate restore endpoint are outside this change.

Acceptance checks must establish:

1. The existing read/write tests and client contract still hold. First saves create no history; unchanged saves advance tokens without consuming history; stale unchanged writes still conflict.
2. Saving A, B, C, D, E leaves E current and history D, C, B. Clearing text, restoring empty text, and nonconsecutive repeated text follow the same retention rules. Version zero never appears as a historical entry.
3. Restoring a retained text through the ordinary write creates a fresh token and archives the displaced current state. A competing save makes a stale restore fail without changing current text or history. Two independent database connections racing with the same expected token produce only one successful write.
4. The history read returns ordered, isolated records and a consistent current token. Mutating returned objects cannot mutate stored state. An absent note has empty history.
5. Exactly 65,536 encoded bytes are accepted; oversized and invalid UTF-8 writes leave the entire state unchanged. Failed transactions cannot leave partial history or consume a token.
6. Closing and reopening the same database, including from a new process, preserves current text, history, and conflict tokens. Document the persistent-path requirement and test with a real temporary database file.
7. At integration, notebook sessions using the same note and service can preview and restore retained text after closing a browser or changing device. This requires the deployed history route and shared durable storage described above; the Python checks alone cannot establish it.

The [evidence](../evidence.md) records the behavior that motivates the compatibility requirements.

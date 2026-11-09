# Storage — feature — durable recovery of recent saved draft versions

## Original problem and why this helps

Notebook users need to restore an earlier draft after accidentally overwriting a note. They must be able to recover the last three successfully saved versions after closing the browser and from another device. Current storage reads expose only the latest text; preserving recent committed snapshots in the shared backing store makes earlier text available independently of browser state.

This is a storage-authored feature handoff from consultation `3LqEU7G30jbYgMy22PwGPUocZzb/draft-conflicts`. It agrees the bounded storage work below. The numerical and product defaults identified as unresolved remain proposals for human review. This consultation performs no implementation.

## Desired behavior

1. Capture history for successful writes through the existing draft write path, including existing clients. A successful save means a storage commit, whether or not the response reaches the client. Invalid requests, conflicts, and failed commits do not produce versions or evict history.
2. Keep the current draft and a bounded number `H` of previous successful saves in durable shared storage. **Proposed `H = 3`**, meaning three earlier restore choices plus current. If review selects three saves total, use `H = 2`. Confirm this interpretation before fixing the product contract and tests.
3. Store each previous snapshot's exact text and version. Retain by successful-save order; use version numbers for ordering. No time-based expiry is proposed. Old versions leave the retained set only when subsequent successful saves exceed the count, or through the draft's existing deletion lifecycle if one exists in the deployed service.
4. Perform the version comparison, head update, history capture, and pruning atomically for each draft. Concurrent writes with the same valid base version have at most one successful commit. History reads return a coherent snapshot of head version and retained entries.
5. Restore by submitting selected historical text through the existing PUT with the **current version the user intends to replace**. The historical version is not the write precondition. Restoration is a normal new save, advances the head version, captures the former head, and participates in retention. A stale restore returns the existing conflict response without changing head or history.
6. Preserve exact empty text as a valid saved snapshot. An absent draft's synthetic version zero is not a successful save and must not enter history. Proposed behavior counts identical-text successful saves as separate versions, matching today's version increments; see unresolved choices below.
7. Make the retained versions accessible for the same draft identity across browser sessions and devices through the existing service access rules. No dependence on browser storage. Do not claim recovery of unsent text or versions overwritten before history capture was introduced.

## Scope and non-goals

Storage owns the history state, retention, atomic write behavior, additive read interface, and durable-service validation. Reuse the existing persistence mechanism if available; select the smallest compatible adapter only after inspecting the deployed service. An in-memory list is adequate for contract modeling but does not fulfill persistence acceptance.

Notebook owns history display, previews, restoration confirmation, unsaved editor contents, save cadence, and conflict interaction. Keep that work in a separate notebook-authored assignment.

No new autosave or restore endpoint, offline synchronization, automatic merge, unconditional conflict retry, full audit archive, revision search, increased text limit, or new deletion API is included. No new timestamp requirement is needed for ordering. Exactly-once save actions and idempotency keys are outside this proposal.

## Interfaces and compatibility

Existing `GET /drafts/{id}` and `PUT /drafts/{id}` retain their request/response shapes and behavior: `{text, version}`, absent draft returns empty text/version zero, valid stale writes return HTTP 409 with the current version, and text is valid UTF-8 with a maximum encoded size of 65,536 bytes. Do not require an opt-in flag or new headers from older clients to preserve history.

Propose one additive read:

```http
GET /drafts/{id}/history
```

```json
{
  "current_version": 4,
  "versions": [
    {"text": "third save", "version": 3},
    {"text": "second save", "version": 2},
    {"text": "first save", "version": 1}
  ]
}
```

Entries are newest first and contain at most `H` **previous** saves; current text remains available through the existing GET. An absent draft returns `{"current_version":0,"versions":[]}` under the existing absence/access rules. No paging or per-version content endpoint is needed at this bound. The head version and history in this response belong to one consistent read.

For the example, restoring version 2 sends `{"text":"second save","version":4}` to PUT. On success the head is version 5; with `H = 3`, previous versions are 4, 3, and 2. If another device commits version 5 first, the restore using 4 conflicts. A client must not automatically substitute the new version and overwrite the competing edit. History can be pruned between read and write; the fetched text can still be saved through PUT if its head precondition is valid. This API promises content restoration, not proof that a selected version remains retained at commit time.

Lost responses keep the current documented recovery path: read current state and compare text, retaining unsaved text while resolving ambiguity. Matching text can establish that the desired content is current; it cannot establish which writer committed it or guarantee exactly-once provenance. A retry with the stale precondition does not create another version.

Keep the 64 KiB per-text ceiling. For `H = 3`, raw text storage is at most 256 KiB per draft and the history read contains at most 192 KiB of raw text, plus metadata and JSON encoding overhead. Transport limits must allow JSON escaping overhead; do not incorrectly treat 192 KiB as a hard wire-size ceiling. Total storage across draft IDs is not bounded by this feature's per-draft count.

At rollout, existing current drafts remain readable with their existing versions and initially empty history. On their next successful save, capture that preexisting current value if its version is positive. Do not invent older snapshots or renumber current versions.

## Acceptance

- Existing tests and unmodified GET/PUT clients continue to work. Successful writes through the old API populate history without client migration.
- After saving A, B, C, D with `H = 3`, head is D/version 4 and history is C/3, B/2, A/1. Saving E gives D/4, C/3, B/2; A is evicted. Adapt the expected count explicitly if review selects `H = 2`.
- Explicit empty saves and identical-text saves follow the selected, documented policy. Version zero is never included. Snapshot contents are independent of subsequent edits.
- Invalid UTF-8, payloads above 65,536 encoded bytes, valid stale saves/restores, and persistence failures leave both head and history unchanged. Exactly-at-limit multibyte text succeeds; limits measure UTF-8 bytes, not characters.
- Concurrent same-base saves yield one commit; a concurrent update during restoration causes a conflict and preserves the competing head. Test real transaction behavior, not just sequential model calls.
- Restoration produces a fresh version and retains the displaced head according to the same count. Lost-response retry with an old version does not duplicate history. Restore from a previously fetched snapshot remains well-defined if that snapshot was later pruned.
- A fresh browser session and another authorized client for the same draft can fetch history without transferring browser data. Committed head/history survive backing-service restart and are visible to distinct service instances where the deployment uses them. Demonstrate this through the actual HTTP and persistence layers.
- Failure injection around head/history update and pruning cannot leave a committed head without required history or evict snapshots for a failed save. A coherent read cannot mix unrelated head/history states.
- Existing drafts migrate without head/version changes; only known saved text is seeded. Different draft identities remain isolated under the existing access model. Document retention, response bounds, conflict recovery, and rollout limitations.

## Required inputs, unresolved choices, and references

**Required implementation inputs:** locate the production durable store and HTTP adapter, deployment routes, draft identity/access mapping, and any existing delete/reset lifecycle. None is present in the supplied checkout, and `c2j` cannot resolve deployment metadata without `.c2/config.yaml`. Do not choose a database or claim durability from the pure model alone. The coordinator must route these missing integration inputs to the storage implementation task.

**Human review:** confirm whether “three” excludes current; whether repeated identical successful saves should consume slots; whether count-only retention without a time guarantee is sufficient at notebook's actual save cadence; and how any existing deletion/reset lifecycle should remove retained snapshots. Recommended defaults and consequences are in [review choices](../review-choices.md). Empty saves count, 64 KiB remains the limit, and conflicts require an explicit client resolution under this proposal. Requests for distinct edits, time windows, larger content, or automatic merging change the scope and need a revised storage agreement.

**References:** [consultation summary](../summary.md), [source evidence and validation](../evidence.md), repository `PURPOSE.md`, `README.md`, `drafts.py`, and `test_drafts.py` at commit `f7183c4`. The inbox contained no exchanged documents. This handoff is authored by storage; notebook has not agreed UI work through it.

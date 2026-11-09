# Draft API findings for notebook's direction review

Reuse the existing GET/PUT interface. Its documented version protocol is sufficient for autosave **when the server enforces atomic compare-and-write**. The supplied model has a reproducible race under overlapping calls. Recommend a narrow storage bug follow-up and verification of the serving layer before claiming simultaneous-tab safety; a new autosave endpoint is unnecessary.

All local source citations below are to storage commit `4bfd5bd201e5e311442950dc394951e19171dc62`, reproduced with original line numbers in [source snapshots](evidence/sources.md). The repository contains a pure in-memory model and two tests, not an HTTP service. Findings about that model and the README contract must not be represented as measurements of a deployed service.

## Interface and version semantics

| Topic            | Established behavior and source                                                                                                                                                                                                           | Consequence for notebook                                                                                                                                                                                      |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reads            | `GET /drafts/{id}` returns `{text, version}`; an absent draft yields empty text and version 0. README lines 3–4; drafts.py lines 9–10.                                                                                                    | Successfully load the active note's baseline before the first save. A failed GET is not evidence of an absent note. Keep active ID separate from the editable navigation target.                              |
| Writes           | PUT takes `{text, version}` and returns the updated draft. The model returns both text and version, increments the supplied matching version by one, and creates a missing draft with version 0. README lines 4–6; drafts.py lines 12–20. | Echo the last confirmed version for that note. Use the returned version after a valid success; do not predict it in the client.                                                                               |
| Version type     | Normal initial/read/write flow produces nonnegative integers starting at 0. The Python model has no strict version-type validator; no separate wire schema is supplied. drafts.py lines 10, 16–18.                                        | Validate the documented response shape and a usable integral version. Do not assume float, string, Boolean, null, or arbitrary opaque-token support based on Python's permissive equality.                    |
| Conflict         | README promises HTTP 409 and the current version without writing. The model raises `Conflict(current_version)` with a single exception argument. It does not return current text. README lines 5–6; drafts.py lines 16–17.                | Fetch the current draft to compare text. Do not assume the 409 body is JSON `{version: ...}`: exact HTTP serialization is unspecified. Never merely copy a 409 version and resubmit local text automatically. |
| Overwrite/delete | No unconditional write flag, delete method, tombstone, or deletion API exists in supplied sources.                                                                                                                                        | Stale writes must remain conditional. Clearing text is a supported empty-text write, not deletion. External deletion/recreation semantics cannot be inferred from version-zero reads.                         |

The model returns copies of its result dictionaries; callers cannot mutate stored state by editing a returned dict. This is confirmed locally, but does not constitute a durability guarantee. Data is held in `self.values`, initialized empty for each Drafts instance (drafts.py lines 5–10).

## Concurrent tabs: interface adequate, model not atomic

Sequential stale writes are rejected as expected. `test_conflicting_tab_cannot_overwrite` finishes A's write before starting B's (test\_drafts.py lines 11–16). That check does not prove atomicity for requests that overlap.

In drafts.py lines 15–19, reading/checking the current version and assigning the new value are separate operations with no lock or transaction. A permitted threaded schedule is:

1. A and B each read version 0 and pass their comparisons.
2. Both construct a different result at version 1.
3. A stores its result; B then stores its result.
4. Both calls return success; only the last text remains and no conflict was reported.

The [probe](evidence/probe.py) pauses unchanged write calls using a thread-local trace immediately before line 19, after each version comparison. A barrier lets both calls reach that point. It does not replace methods, change locals, or modify source. All three bounded trials observed two successful version-1 writes with only one text retained; [raw output](evidence/probe-output.txt) records the actual order/outcomes. This proves the model lacks atomicity when invoked concurrently, not the frequency of the race in any deployment.

A per-note request queue in one tab cannot serialize other tabs. Storage must protect the comparison and write together across all writers sharing the authoritative state. A guard can address one model instance; a multi-process service would need appropriate shared-store concurrency control. No actual serving layer is available to determine whether it already provides this protection.

**Recommendation:** accept the [storage bug handoff](work/handoff.md). An independently verified globally serialized serving layer could make deployment changes unnecessary, but that is presently unestablished. Do not replace conditional writes with last-write-wins or add an autosave endpoint to address this issue.

## Lost responses, exact text, and recovery

The README explicitly anticipates a committed write whose response is lost and recommends reading and comparing text (lines 10–13). The model is not an idempotent-write API: retrying the same text with the old version conflicts after a successful commit; writing identical text with the current version increments the version again. There are no idempotency keys. They are not required for safe content reconciliation under an atomic version protocol.

Recommended notebook flow:

1. Capture an immutable submitted text `T`, its expected version `V`, active note ID, and request identity. Keep edits made afterward separately as dirty text. Serialize that note's requests, including manual Save.
2. On a lost, invalid, or otherwise uncertain response, retain both `T` and the newest local text. Say that saving could not be confirmed; do not claim the request definitely failed to commit.
3. Obtain a fresh authoritative GET for the same note. If returned text equals `T`, content `T` was present at that read and its returned version can become the confirmed baseline. Only show the current editor as Saved if it still represents that same submitted snapshot and has no newer changes. Equality proves content, not which request authored it or that another tab cannot change it later.
4. If the GET shows different text at an advanced version, pause autosave for that note and offer comparison/recovery. Preserve local text. Do not adopt that newer version merely to overwrite the server. A different value does not prove the uncertain write never committed; another writer could have changed it afterward.
5. If a fresh GET still shows the original version `V`, a retry of the original `T,V` remains conditional. The first request could still be in progress: with atomic compare-and-write, at most one such attempt can win and the other must conflict. A retry must not be treated as permission to overwrite a different version. If GET itself fails, keep the outcome unresolved.

Direct model reads consult the current in-process dictionary. There is no HTTP cache configuration, replica/read-consistency specification, or adapter source. Request an uncached reconciliation read in the client and confirm the serving layer provides an authoritative result; a client cache option alone does not prove server consistency. No guarantee about stale responses or replicas can be supplied from this checkout.

Text is stored and returned exactly as passed after UTF-8 encoding validation; the model does not normalize or truncate it (drafts.py lines 13–20). Probes preserve combining versus precomposed accents, CR/LF, tabs, NUL, and emoji. Compare the immutable submitted string with returned text, not with the live textarea after further editing or any UI/import normalization. HTTP transport fidelity remains untested.

## Size, validation, identifiers, and error behavior

The limit is **65,536 bytes of UTF-8-encoded text, inclusive**, not characters and not the entire JSON body. The model rejects only lengths greater than 65,536 (drafts.py lines 13–14). Empty text is allowed and creates or clears a draft through normal versioned writes. The probe accepted exactly 65,536 ASCII characters and 16,384 four-byte emoji, and rejected one additional ASCII byte in each case without modifying storage.

Use a UTF-8 byte counter on the same snapshot sent to storage, such as `new TextEncoder().encode(snapshot).byteLength`, after checking well-formed text. JavaScript string length is not a UTF-8 byte count; UTF-8 encoding alone is not a malformed-surrogate validator. Preserve oversized text in the editor, show the byte limit, offer copy/export, and allow saving again after the user reduces the content. Do not truncate silently. The server remains authoritative.

| Case                                                | What storage establishes                                                                                                                                 | Recommended UI response                                                                                                                |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Stale version                                       | Documented HTTP 409, current version, no write; model `Conflict`.                                                                                        | Pause automatic overwrites, fetch current text, compare, keep local text.                                                              |
| Text too large                                      | Model `ValueError('draft is too large')`; HTTP status/body absent. Size check runs before version check, so oversized stale writes hit validation first. | Stop repeated sends of unchanged oversized text; retain text and actionable size feedback. Do not hardcode 413 as a verified contract. |
| Invalid text                                        | Unpaired surrogate raises `UnicodeEncodeError` before mutation in the probe. Non-string request/type mapping is not specified.                           | Preserve input, report validation issue, and require correction. No verified 400/422 response schema exists here.                      |
| Network failure, timeout, malformed success         | No transport implementation. A malformed/lost response may follow a committed write.                                                                     | Keep dirty/pending snapshots and reconcile; bounded retries with backoff rather than immediate repeated PUTs.                          |
| Service failure (e.g. 5xx)                          | No deployment status guarantees.                                                                                                                         | Preserve text; treat ambiguous outcomes conservatively, reconcile, and retry with bounded backoff when appropriate.                    |
| Throttling (429)                                    | No rate limits or retry headers documented.                                                                                                              | If present, honor valid server retry guidance and reduce cadence. This is defensive behavior, not a confirmed API requirement.         |
| Unauthorized/expired session (401), forbidden (403) | No auth model or headers supplied.                                                                                                                       | If encountered, retain text, stop automatic retries, and offer the applicable sign-in/access recovery.                                 |

No identifier syntax, maximum length, empty-ID rule, URI decoding rule, tenant scope, or authorization behavior is documented. The model uses `name` as a dictionary key; that does not establish allowable HTTP IDs. Notebook already URL-encodes note IDs in the supplied UI. Preserve that supported route usage, bind saves to a successfully loaded active ID, and avoid inventing broader ID rules or requiring a new endpoint. Proxy/body limits and transport handling of unusual characters are integration unknowns.

## Cadence, compatibility, and review consequences

README lines 7–10 says this API supports frequent saves and consumers serialize writes. It specifies no rate limit, write cost, latency, or quota. The proposed 800 ms idle debounce and 5 s maximum dirty interval are reasonable provisional UI settings, not verified service limits. Use one in-flight write per note, coalesce queued changes to the newest text, and route manual Save through the same queue. The 5 s interval is a scheduling target while dirty and eligible to send; it cannot be a completion guarantee during slow requests, failures, or conflicts. Avoid overlapping writes to satisfy that timer.

No schema migration or route change is indicated. The supplied notebook already reads `{text, version}` and PUTs `{text, version}`; its success path uses the returned version (inbox/notebook-index.html lines 17–31, copied in the source evidence). Keeping that interface preserves the observed caller. No additional clients or deployment configuration are present to audit. Notebook's import CLI, UI behavior, and offline storage remain notebook-owned per both purposes; no importer storage change is justified by this review.

For the direction review, carry forward these consequential constraints:

* Keep the existing endpoint and online scope; implement notebook scheduling, immutable snapshots, guarded switching, manual Save, accessible status, and compare/copy/export recovery after approval.

* Require atomic version enforcement for two tabs. The supplied model needs the agreed narrow fix for overlapping calls; actual server serialization and all writers must be checked before deployment claims.

* Confirm HTTP error mapping and fresh reconciliation reads against the actual adapter when available. A conflict version by itself does not authorize replacing text.

* State the inclusive UTF-8 limit and preserve oversized/failed/conflicting local text. Closing/reloading cannot promise saving unsent browser memory.

The [handoff](work/handoff.md) defines the future storage scope. No production code, tests, endpoint, or configuration was changed; all advisory experiments were created and run from scratch outside the checkout.

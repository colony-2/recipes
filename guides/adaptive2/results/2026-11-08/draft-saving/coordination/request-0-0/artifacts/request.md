# Notebook feature consultation: preserve unfinished notes when users switch notes

Users lose unfinished text when opening another note. Notebook owns this **feature**: saving while typing, keeping manual Save, and clear saving, saved, failed, and conflict states. Storage owns persistence and its API. The immediate decision is whether the existing draft API can safely support this behavior, or whether storage work is necessary. This is a direction consultation only; implementation and delivery must wait for human direction approval.

The user's suggestion of a new autosave endpoint is a hypothesis to evaluate. Please challenge it. Our provisional preference is to reuse the supported draft API if its concurrency and failure semantics suffice.

## Submitted context and observed behavior

- [Original user request](user-request.md).
- [Notebook purpose](notebook-purpose.md) assigns persistence/API ownership to `storage` and requires consultation before requesting a new interface.
- [Notebook README](notebook-readme.md) identifies the draft API as the supported persistence boundary.
- [Current UI](notebook-index.html), from notebook commit `ef2b83120121e9190ec3edc53d6cdbc29f35ddf5`, calls `GET /drafts/{encoded note ID}` and `PUT /drafts/{encoded note ID}` with JSON `{text, version}`. It reads `{text, version}` from GET and `{version}` from successful PUT. Other contract details are not established by notebook code.
- Local checks of the unchanged inline UI script with a stub DOM and mocked fetch reproduced unsaved text replacement on Open, saving A's text to B after changing the destination input, and a stale Saved label when more typing occurs during a request. These are notebook-owned concerns, not requests to storage to solve UI behavior.

## Questions for storage

Please inspect your repository and applicable context, cite specific source paths, and run useful bounded checks if available. Distinguish current guarantees from recommendations or changes that would be needed.

| Question | What we need for the direction review |
| --- | --- |
| Can autosave use the existing GET/PUT draft API? | Give a clear recommendation and reasons. Is any new endpoint actually needed? Identify a specific gap before proposing storage work. |
| How does concurrency control work? | Meaning/type of `version`; atomic compare-and-write behavior across simultaneous requests/tabs; success response; stale-version HTTP status and body; whether conflict returns current text/version or requires a GET. Any unconditional overwrite path to avoid? |
| How are new or missing notes handled? | Initial version, GET of an unknown note, creation through PUT, and deleted/missing-note behavior if supported. What should the UI do before a first save? |
| How should a lost response be reconciled? | A PUT may commit even if the client times out. Is retry with the same expected version safe? Are idempotency keys supported or needed? Can a fresh GET determine whether the submitted text is stored, and what read consistency/cache behavior is guaranteed? |
| Does storage preserve text exactly? | Normalization, truncation, encoding, and whether returned text can be compared exactly with an immutable submitted snapshot. If content equality cannot establish a match, recommend a safe alternative. |
| What limits apply to draft size and identifiers? | Exact size limit and unit (UTF-8 text bytes, characters, or total request bytes), inclusivity, over-limit status/body, empty text support, and note ID constraints. Include practical UI preflight guidance. |
| Which errors require which response? | Validation, oversized text, conflict, unavailable service, throttling, unauthorized/expired access, forbidden, malformed response, and relevant retry headers. Distinguish supported errors from hypothetical deployment behavior. |
| What request cadence is practical? | Any rate limits or write costs that should affect a provisional 800 ms idle debounce, 5 s maximum interval during continuous typing, one in-flight write per note, and coalescing to the newest text? These are proposed UI choices, not a requested API contract. |
| Are there compatibility or rollout constraints? | Existing clients/importers, schema migration, version formats, supported routes, configuration or security requirements, and whether a UI-only rollout is viable. No live deployment is requested. |
| What work, if any, does storage own after approval? | If no change is needed, say so explicitly. If necessary, provide a receiver-authored handoff classified as feature, bug, explanation, or oversight with owner/ref, acceptance, and dependency on direction approval. Do not implement or submit a delivery job. |

## Notebook direction being considered, pending your findings

Keep the active note ID separate from the navigation target; associate text, revision, request identity, and errors with the right note. Capture immutable submitted text; never replace a newer local edit with an old response. Debounce saves and use one write at a time per note, with manual Save flushing the same path. Only label current text Saved once its storage state is confirmed. Preserve local text on failure/conflict and offer explicit recovery/compare/export choices rather than unconditional overwrite. Evaluate a guarded note-switch flow that completes or explicitly resolves pending work before replacing the editor. Browser reload/close cannot promise a completed network save; offline editing and collaboration are excluded. Two tabs are still a required conflict case.

Please return a concise consultation summary with supporting evidence. Notebook will incorporate all consequential answers and unresolved decisions into `one-pager.md` and produce `mockup.html` for the human direction review.

## Discovery limitation

`c2j self` and `c2j cells` both returned `Error: requires .c2/config.yaml` in this supplied checkout; that file is absent. This CLI also reports `unknown command "job" for "c2j"`. No feedback, coordination, results, or error artifacts were supplied. The registered owner name `storage` is documented in both notebook PURPOSE.md and README.md, so the consultation uses that owner through the coordinator. No alternative deployment or repository URL was assumed.

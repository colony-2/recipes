# Notebook inspection and checks

Classification: **feature**. Notebook owns the web UI; storage owns persistence/API. Scope is direction review and proposed UI only. No implementation or delivery has been performed.

Inspected repository commit: `ef2b83120121e9190ec3edc53d6cdbc29f35ddf5`.

Read all supplied repository files: PURPOSE.md, README.md, index.html, import_notes.py, and test_import_notes.py, plus the submitted request. No applicable AGENTS.md was found in the checkout or parent locations. No error/, feedback/, coordination/, or results/ input was present. Import CLI changes are outside this request.

## Source findings

- PURPOSE.md:3–5 assigns web UI/import CLI to notebook and persistence/API to storage; requires consulting storage before proposing an interface.
- README.md:3–5 documents unsaved-text loss on navigation and the supported draft API; no offline support exists.
- index.html:16–21 replaces the editor after GET without preserving unsaved text, checking response status, or guarding response ordering.
- index.html:23–30 saves to the current navigation input rather than a separately tracked loaded note identity. The one global version and status are not tied to a submitted snapshot. Every successful response says Saved, including when typing continued after submission.
- index.html:28 collapses all non-success responses into Save failed. Rejected fetches/JSON parsing failures are not handled. Storage conflict and size semantics cannot be inferred here.

## Actual checks

Executed the unchanged inline script with Node's built-in VM, a minimal DOM stub, and controlled fetch responses. The reproduction script is [check-current-ui.cjs](check-current-ui.cjs); results are [current-ui-checks.txt](current-ui-checks.txt).

1. Load A, type unfinished A, open B: the editor becomes B and no save is requested.
2. Load A, edit A, change the destination input to B, press Save: the request targets `/drafts/b` with A's edited text.
3. Submit A, type more before its response, resolve the response: the status says Saved while the newer text is still unsaved.

All three reproductions completed with assertions passing. These establish current client behavior only; they are not browser, accessibility, integration, or storage-contract tests. Production files remain unchanged. No live service routes were available from task metadata.

## Environment discovery

- `c2j self`: exit 1, `Error: requires .c2/config.yaml`.
- `c2j cells`: exit 1, same error. Checkout has no .c2/config.yaml.
- `c2j self --help` and `c2j cells --help`: available flags provide no alternate task connection.
- `c2j job --help`: exit 1, `Error: unknown command "job" for "c2j"`.

Missing optional discovery metadata does not prevent a documented-owner consultation. No configuration was invented or modified, no delivery job was submitted, and no human environment decision is required for the direction work.

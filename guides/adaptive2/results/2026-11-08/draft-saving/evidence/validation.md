# Direction and mockup validation

Validated on 2026-11-08. Production checkout remains at `ef2b83120121e9190ec3edc53d6cdbc29f35ddf5` with no changes. No implementation, delivery job, endpoint, migration, or deployment was made.

## Notebook baseline

Reran [check-current-ui.cjs](check-current-ui.cjs) against the current unchanged index.html. All three assertions again reproduced the behaviors in [current-ui-checks.txt](current-ui-checks.txt): unsaved text replaced on Open, text sent to the navigation target rather than loaded note, and Saved displayed after newer unsaved typing. This is a stub-DOM check, not a live service test.

## Browser checks of the proposal

Ran [check-mockup.cjs](check-mockup.cjs) against [mockup.html](../mockup.html) with installed Playwright and cached Chromium. [Raw results](mockup-checks.txt) record eleven passing groups:

- All ten selectable scenarios show the intended labels.
- Changing the navigation target preserves the active note. The switch dialog preserves text, contains keyboard focus, supports Escape, and restores focus.
- A simulated acknowledgement for earlier text does not replace newer edits or mark them Saved.
- Canceling a switch prevents late navigation; Save & open waits for simulated confirmation.
- Failed/uncertain recovery simulations retain text.
- A 65,537-byte draft remains intact, blocks saving/switching, and downloads in full without being labeled Saved.
- Comparison has a separate reviewed draft; choosing stored text does not replace the original, and reopening comparison retains the reviewed draft. Explicit simulated reviewed-save retains the original for recovery.
- The failed-target-load scenario keeps the original note visible.
- Inputs have labels, IDs are unique, and status uses a live region. At 390 px the editor and stacked comparison have no horizontal page overflow.
- No browser script errors, HTTP requests, external assets, or local/session-storage writes occurred.

The first browser launch looked for a different Playwright-managed browser revision. Used the compatible Chromium already installed at `/home/shai/.cache/ms-playwright/chromium-1228/chrome-linux/chrome`; no package or worker configuration change was needed. An initial keyboard check exposed focus leaving the prototype dialog's controls on Tab wrap; an explicit focus loop corrected it, and the final full browser run passed.

Visually inspected full-page screenshots of [Saved on desktop](mockup-saved.png), [conflict comparison on desktop](mockup-conflict.png), and [uncertain save on mobile](mockup-mobile.png). Labels, focus treatment, action placement, and stacked layout were readable without clipping.

## Evidence and artifact checks

The supplied storage consultation, conversation, source evidence, and receiver-authored bug handoff are preserved byte-for-byte. The direction explicitly carries forward the overlapping-write defect, UTF-8 size boundary, lost-response guidance, and deployment unknowns. Storage's advisory experiments were read, not represented as new live integration tests.

Validated relative links in authored review documents and the selected inner consultation records; checked required one-pager sections and retained source records. The coordinator's duplicate outer summary is not selected as a review source because its relative links assume a different directory; the original inner summary has valid links and is selected unchanged.

## Limits and deferred verification

This is a scripted **proposed UI**. Scenario selection resets sample text. Save/retry/reviewed-save buttons simulate chosen outcomes; typing does not issue automatic network saves. The mockup does not implement the planned queue, authoritative reconciliation, conditional writes, production Unicode validation, automatic timeout/retry policy, or browser-close warning. Those belong to later approved implementation. It is not a storage-backed autosave feature.

Browser checks cover Chromium and selected keyboard/layout behaviors, not screen-reader conformance, every browser, zoom setting, clipboard permission behavior, or a real two-tab server integration. Actual concurrency control, durable persistence, read freshness, HTTP error serialization, request limits, and performance remain unverified because no serving adapter or task connection was supplied. These are recorded in the one-pager as release checks, not hidden assumptions or reasons to invent an endpoint.

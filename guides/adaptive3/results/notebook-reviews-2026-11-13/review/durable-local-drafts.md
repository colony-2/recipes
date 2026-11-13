# Restore notebook drafts after reopening the browser

## Problem Description

The notebook loses unsent text when its module is reloaded. I recommend saving the active draft locally after every edit and restoring it when the notebook next opens in the same browser profile and origin. Cloud sync remains out of scope.

`README.md` describes the desired recovery behavior, but `app.js` only keeps a module-level string behind `updateDraft(value)` and `getDraft()`. I verified that an edit is readable in the current module instance and becomes an empty string in a fresh instance. There is no rendered UI, storage adapter, or test setup in this repository. I classify this as a **feature**: adding persistence to the existing in-memory notebook.

## Non Goals

Cloud sync, servers, accounts, cross-device recovery, multiple notebooks, draft history, conflict merging, and a new editor or visual redesign are excluded. This change does not promise recovery after browser data is cleared, private browsing ends, or storage fails.

## What we are planning to do

I will keep the existing draft functions and add browser-local persistence for one active text draft. Each `updateDraft` will update memory and immediately attempt to save the exact text. The first use of either function will initialize the draft from storage; an absent saved value means an empty draft. Saving an empty string will persist the user's clearing of the draft.

I recommend `localStorage` because this module has a synchronous API and stores just one text value. Saving on each update avoids a debounce window or dependence on a shutdown event. A separate persistence-status query will let callers distinguish a restored or saved draft from text held only in memory, without changing the existing functions' return behavior. Storage failures will preserve current editing and remain observable through that query.

I will add focused tests with controlled browser-storage substitutes and document the browser's retention limits. Acceptance requires exact text recovery in a fresh module, persistence of an empty draft, and observable read/write failures without losing the in-memory edit. A browser smoke check must also confirm recovery after reopening the same origin. A failed recovery check is failed acceptance.

No visual change is proposed: this repository supplies only a JavaScript module, so there is no existing screen to mock up.

## Compat/Upgrade (what existing users need to do)

Users need no account or migration. Existing callers can continue using `updateDraft` and `getDraft`; callers that need to display save health can use the new status query. The first edit after upgrade will create the saved draft. Text already lost before upgrade cannot be recovered.

Recovery requires the same browser profile and origin with storage available. Moving the notebook to another origin or clearing browser data removes access to that saved draft. Other people using the same browser profile and origin can access it; this feature adds no encryption or access control.

## Key challenges/design questions & answers

| Question | Answer and consequences |
| --- | --- |
| Which storage should we use? | I recommend a stable, namespaced `localStorage` key containing the draft as plain text. This fits the synchronous API and needs no database migration. IndexedDB would better suit large documents or multiple records, but would require asynchronous initialization and more machinery. |
| When is a draft saved? | Attempt a synchronous write on every update, including empty text. Debouncing reduces writes but leaves recent edits vulnerable to interruption. Large drafts may cause latency or exceed browser quotas; this proposal targets the current single text draft. |
| What does “durable” mean here? | Recovery across ordinary reloads and browser restarts while browser storage is retained. Browser storage is not a backup or a guarantee against power loss, eviction, or deliberate deletion. |
| What happens when storage is unavailable or full? | Keep editing in memory, report the failed operation through the status query, and retry writes on subsequent edits. Do not throw storage errors through existing draft calls. A read failure must not trigger an automatic write of an empty draft. A caller must consume the status to show a warning; no warning UI exists here today. |
| What happens with two tabs? | I recommend last successful write wins for the persisted draft. Each tab keeps its own in-memory text, so another tab does not replace text while someone is typing. Reopening restores the most recent successful write. Conflict detection or merging would prevent some overwrites but substantially expands this feature. |
| How do we avoid overwriting a saved draft during startup? | Restore once before serving the first draft operation; initialization itself never writes. An explicit edit may then replace the saved text. Persist raw text without trimming or interpretation. |
| Does another cell need to change? | No foreign code or API is present in the inspected repository; `PURPOSE.md` assigns the local notebook UI to root. The registry lookup failed with “JobDB runtime URL is required,” so registry ownership could not be independently checked. No cross-cell change is proposed. |

## Expected scope

| Cell | Core code | Tests | Docs |
| --- | --- | --- | --- |
| root | small | small | small |

Tests include the new lightweight harness and storage fixtures as well as recovery, empty-text, failure, and last-writer cases. Documentation will explain restoration, save-status handling, and local-storage limits.

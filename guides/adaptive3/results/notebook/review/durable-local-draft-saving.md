# Approve durable local draft saving

**Assignment:** Feature. **Decision requested:** Approve the scope below before implementation.

Human direction (current request): “Add durable draft saving to this local notebook. Keep cloud sync out of scope.”

## Problem Description

The active draft disappears when the notebook reloads. `app.js` initializes `draft` to `""`; `updateDraft(value)` only assigns that variable, and `getDraft()` returns it. A runtime check confirmed that an edited draft is present in one module instance and empty in a fresh instance. `README.md` explicitly expects recovery of the latest unsent draft when users reopen this browser.

The repository contains only this module and two descriptive Markdown files. There is no renderer, server, account system, or existing persistence layer.

## Non Goals

Cloud sync, servers, accounts, cross-device recovery, multiple notes, draft history, conflict merging, export/backup, and a new editor UI are excluded. This change does not promise recovery after browser data is cleared or private browsing storage is discarded.

## What we are planning to do

Restore the active draft from browser `localStorage` when the module initializes. Save the complete text synchronously on every `updateDraft(value)` call, using the dedicated key `notebook.draft.v1`. Store the text directly; an empty string is a valid saved draft. Preserve whitespace, newlines, and Unicode exactly.

Keep editing functional if storage cannot be read or written. Add a read-only `getDraftPersistenceStatus()` export returning `"saved"` or `"memory-only"`: `"saved"` means the current text was successfully restored or written; `"memory-only"` means it has not been persisted. A fresh empty draft with no stored value starts as `"memory-only"`. Retry saving on each subsequent update, allowing recovery after a temporary storage failure.

Validate restoration across fresh module loads and a real browser reload/reopen; exact text round trips; clearing; denied or full storage; successful retry; and the documented two-tab policy. Document the storage boundary and failure behavior in the README. There is no visual change or existing UI to mock up; the status export lets a future UI report persistence accurately.

## Compat/Upgrade

Keep `updateDraft(value)` and `getDraft()` synchronous and preserve their existing return behavior. The new status export is additive. Text drafts are the supported persistence input. Guard browser storage access so importing the module without browser storage still permits in-memory use.

No migration is needed because there is no existing durable format. Existing unrelated browser storage stays untouched. Recovery applies to the same browser profile and origin; changing the host, port, or protocol can select different storage. Browser-controlled retention remains a limit on durability.

## Key challenges/design questions & answers

| Question | Answer and consequences |
| --- | --- |
| Why `localStorage` rather than IndexedDB? | One text draft fits the existing synchronous API. IndexedDB offers asynchronous writes and better scaling but would require an initialization/readiness contract. Revisit it if large notes or multiple documents become requirements. |
| Save on every edit, debounce, or save on close? | Save on every update so a successfully completed write does not depend on a timer or close event. Synchronous writes may slow editing for very large drafts; the current repository supplies no size requirement. |
| What does deleting all text do? | Persist `""` immediately. Reopening must show an empty draft, not resurrect an earlier nonempty value. |
| What happens if storage is unavailable or full? | Retain the current in-memory text, expose `"memory-only"`, and retry on the next edit. Do not throw a storage error through the editor API or report an unsuccessful write as saved. A failed write leaves the previous stored draft available for a later reopen. |
| How do multiple tabs behave? | The last successful write wins for the next reopen. Open tabs keep their own text; there is no live synchronization. Editing a stale tab can overwrite a newer saved draft. Conflict detection would add UI and revision handling beyond this single-draft proposal. |
| Is the saved draft backed up or protected from other same-origin scripts? | No. It stays in this browser's origin-scoped storage and is available to scripts on that origin. Cloud recovery and additional encryption are outside this proposal. |
| Does another owner need to change an API or service? | No external component appears in the supplied repository. This is local to the notebook module. Cell discovery was unavailable (`c2j cells`: “JobDB runtime URL is required”); no cross-cell dependency was identified in the inspected code. |

Approval authorizes implementing this local persistence behavior and its focused validation. Cloud sync remains excluded.

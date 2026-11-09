# Progress

Direction ready for review: [one-pager.md](one-pager.md) and [mockup.html](mockup.html). The proposal retains manual Save, adds autosave states and guarded switching, and preserves drafts through failures, conflicts, and oversize input. Offline editing and collaboration remain excluded.

Storage recommends the existing API and supplied a bounded concurrency bug handoff. The review makes that fix and serving-layer verification explicit dependencies; no storage work has been dispatched. Original consultation records are retained.

Reproduced current UI flaws again. Browser checks of the proposed UI passed, including keyboard dialog behavior, late-response handling, recovery, full draft download, and mobile layout. Screenshots and limits are in [validation](evidence/validation.md). Production files are unchanged. Awaiting the requested human direction approval before specification or implementation.

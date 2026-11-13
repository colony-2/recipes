# Approve five distinct saved versions using existing recovery APIs

I can do this, but recovery already has the necessary API shape. The useful storage change is to retain five distinct saved versions, including current, and keep the existing version-checked save path for restoration.

## Request and evidence

Original human wording, supplied in this consultation request from root: “I'm root. Our notebook needs users to recover old saves. Can you add a new restore endpoint and keep five versions, including every autosave?”

`PURPOSE.md` assigns persistent notebook text, history and version checks to storage, and the notebook UI to notebook. `README.md` documents three distinct retained versions including current, `GET /notebooks/:id/history` returning retained text and version, and `PUT /notebooks/:id` accepting `expected_version` and rejecting stale writers. It explicitly calls for product agreement on retention counting and autosave granularity.

`storage.js` sets `retainedVersions = 3`. Its `save` function checks the expected version before comparing text, returns the existing record for identical text, and increments the version for changed text. This checkout contains no HTTP handlers or history persistence implementation; the API behavior above is documented, while the save semantics are visible in code.

## Proposed feature assignment

Increase storage retention from three to five distinct saved versions, counting current as one of the five. Count each content-changing save, including autosaves; keep identical saves as no-ops. Preserve monotonically increasing versions and stale-writer rejection. Verify the retention setting and save behavior with focused checks, including changed saves, identical saves, and stale writes.

Recovery should select retained text through the existing history GET and submit it through the existing PUT with the current notebook version as `expected_version`, not the selected historical version. Restoring different text creates a new current version and follows normal retention. A concurrent save must cause a conflict rather than an automatic overwrite. Restoring text already current remains a no-op after the version check.

Notebook owns the history picker and recovery interaction. A visible recovery feature needs that owner's UI work; changing storage retention alone does not provide it.

## Decision requested and differences

Approve five total distinct versions: current plus up to four older versions. This is not five older versions plus current. Each changed autosave consumes a slot, so frequent editing can quickly replace older history; this proposal adds no autosave grouping or time-based recovery guarantee.

The proposed shape omits the new restore endpoint because the existing PUT already provides the required conflict protection. It also excludes identical autosave events from version counting. If “every autosave” means retaining duplicate events even when text is unchanged, that is a separate change to the current history semantics and should be explicitly agreed before delivery.

Work type: **feature**. Use the normal **adaptive3** delivery workflow for the storage retention change after agreement on these semantics.

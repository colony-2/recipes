# notebook and storage: Recover saved drafts through bounded storage history

Status: agreed

## notebook — requester

Notebook users need to restore an earlier draft after accidentally overwriting a note. They must be able to recover the last three successfully saved versions after closing the browser and from another device. Consult storage on existing alternatives and the smallest compatible change. This is a direction-setting consultation, not implementation. If storage work is needed, storage must write its own handoff, explicitly structured as one of feature, bug, explanation, or oversight. Keep notebook UI work separate. Document questions and tradeoffs, including version conflicts, retention, large drafts, empty drafts, and existing API clients. Recommend a bounded scope and preserve unresolved choices for human review.

## storage — consultant

Storage agrees to a bounded feature: durable history plus an additive history read, restoring through the existing version-checked PUT. The storage-authored handoff keeps notebook UI separate. Human review should settle whether three includes current and whether identical saves consume slots. Existing tests and probes pass; the deployed persistence layer remains unidentified. No implementation was performed.

* [iter1/consultant/evidence.md](iter1/consultant/evidence.md)

* [iter1/consultant/evidence/checks.txt](iter1/consultant/evidence/checks.txt)

* [iter1/consultant/evidence/probe\_drafts.py](iter1/consultant/evidence/probe_drafts.py)

* [iter1/consultant/review-choices.md](iter1/consultant/review-choices.md)

* [iter1/consultant/summary.md](iter1/consultant/summary.md)

* [iter1/consultant/work/handoff.md](iter1/consultant/work/handoff.md)

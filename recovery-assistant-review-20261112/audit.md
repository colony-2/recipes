# Assistant final-review failure

Job: `3LzThfsN8qmLoKXO42qCPoyrsFb`

Goal: `3LyMcyLCgQnFSusa2zF4Im7RELW`

JobDB: `http://192.168.1.195:9047/c2`
Observed: 2026-11-12, after completion at 18:55 UTC.

The implementation reached final human review preparation. Root's prerequisite
`P6udJLLYhZ3ag7kERbiiVMM4WBu` succeeded, the final verification command passed,
and independent assessment approved the candidate with no blocking findings.
The assistant job then failed before opening the review. It has not merged.

## Exact cause

The accounting agent repaired the review attachments and exported 72 selected
files. Its corrected `evidence-index.md` is 2,580 bytes, stored at task ordinal
195. The native attachment checker accepted this packet at 18:55:02 UTC.

The acceptance step then merged verification artifact references over the
accounting documents. That replaced the corrected index with verification's
13,807-byte `evidence-index.md` from task ordinal 191. The older index links to
raw case files that are not in the selected review packet. For example, it points
to `go-test.jsonl`, whereas the corrected index points to the attached
`review-evidence/go-test.jsonl`.

The final checker therefore generated a large missing-link report. Its command
succeeded, but command stdout was truncated and included an output-truncation
notice. The recipe called `json_parse` on that incomplete stdout and failed with
`invalid character 'O' looking for beginning of value`.

Both causes belong to recipes: changing a validated packet before displaying it,
and treating potentially truncated command output as a complete JSON document.
The source is the captured recipe at commit
`2fa3296836b2faf8aa1ff8ece7bb44ac1b15bda4`, particularly the acceptance document
merge in `recipes/adaptive2/develop.yaml` and stdout parsing in
`recipes/adaptive2/review-links.yaml`.

## Recovery

Restart immediately before final review validation, at chapter 197's unique
`state_machine:validate` scope. Replace only the selected `evidence-index.md`
reference with the existing corrected artifact from ordinal 195. Keep every
other selected artifact, the candidate, verification, and assessment.

The attached patch does this without replacing the complete context or using
redacted snapshot values. The normal validator still runs; human approval is
still required. The script continues the existing goal and has no `/tmp`
dependencies. It has been prepared, not submitted.

## Checks and limits

- All 72 paths from the corrected accounting packet remain in the final packet.
- Comparing unredacted document identities identifies `evidence-index.md` as
  the only changed Markdown/HTML reference. `secret-audit.md` is fully redacted
  in the snapshot and is left untouched; the acceptance merge does not replace it.
- Additional selected verification artifacts are JSON; the link checker does
  not parse them for document links. Candidate copies differ in producer identity
  but are not parsed as linked documents.
- The corrected packet already passed the recorded native checker. This audit
  did not rerun the product tests or submit the recovery.
- The restart script passes `bash -n`; the selected document names are all
  within the review title fallback length limit.

For a durable fix, preserve the accounting packet's corrected document versions
at acceptance and add a regression covering this name collision. Separately,
make validator results safe when diagnostics exceed stdout limits: return a
small bounded result and retain full diagnostics as an artifact. Truncation
must never be interpreted as a successful validation.

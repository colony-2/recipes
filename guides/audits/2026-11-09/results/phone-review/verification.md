# Verification evidence

## Supplied statements

`test-statements.md`:

> VIS-1 [High] [integration; Chromium] [index.html] Save remains clearly readable on a 390-pixel phone layout.

`test-results.md`:

> VIS-1: Chromium rendered the actual index.html at 390x844; inspect phone.png. Static fixture, no backend or production data.

`implementation.md` reports a dark blue background and white text and links the capture. No skipped or failed product tests are listed in the supplied report.

## Independent review

- Read root `PURPOSE.md`: “Own this static notebook page.” No applicable `AGENTS.md` was found.
- Read the complete candidate HTML and supplied merge diff; working tree was clean.
- Compared candidate bytes with base HTML after replacing `background:#777` with `background:#1447c4`: equality was `True`. This verifies all other source and layout declarations remain identical.
- Calculated white-text contrast with sRGB linearization and relative-luminance weights 0.2126, 0.7152, 0.0722: old 4.478:1; new 7.698:1.
- Inspected [phone.png](phone.png) directly: blue Save button, legible white label, readable note and status, no visible clipping. Read PNG header independently: 390×844 pixels.
- Screenshot SHA256: `16edba61ed83b048aed1078e2067ec92b1bb9da88bfeb29db27c19e2716194d2`. The published image is an unchanged copy of the supplied capture.

## Unsuccessful diagnostics and resolution

- `c2j self` returned `Error: requires .c2/config.yaml`. Local candidate and supplied artifacts contained the evidence needed; no job inspection or submission was necessary.
- Initial calculation command used `python`, which was unavailable (exit 127).
- Retrying with `python3` and Pillow failed because `PIL` was unavailable (exit 1), before any checks executed.
- The corrected `python3` command used only standard-library modules (`subprocess`, `hashlib`, `struct`), completed successfully (exit 0), and produced the comparison, contrast, dimensions, and hash recorded above. Pixel sampling through Pillow was not completed; direct visual inspection and source-based contrast calculation supplied the relevant evidence.

No independent browser rerun was performed. This review accepts the supplied Chromium execution statement together with the actual inspected capture and independent source checks.

## Merge-review checks

The merge-review task independently confirmed the single modified file,
background-only byte replacement, and working file equality with the candidate
head. The supplied diff equals `git diff --full-index` for the recorded base and
head. An initial byte comparison against the default abbreviated-index diff
returned false; using full index hashes resolved this formatting difference.
The contrast values, PNG dimensions, and SHA256 above were independently
reproduced with Python 3 standard-library code. The actual screenshot was
visually inspected again; no clipping or unreadable Save label was observed.
No browser rerun was performed in the merge-review task.

The actual inbox contains implementation, test statements, test results,
assessment, verification, candidate diff, candidate inventory, phone capture,
and a duplicate assessment under `feedback/`. Both assessments were read and
are identical. No `approved-direction/one-pager.md`, `approved/`, `error/`,
separate specialist reports, or child outcomes were supplied. Root `PURPOSE.md`
identifies ownership of the static notebook page; no applicable `AGENTS.md`
was found. `c2j self` and `c2j cells` both returned
`Error: requires .c2/config.yaml`; this environment cannot supply additional
job or cell metadata through those commands. No child completion is inferred.

The candidate working tree was clean before preparation. Review artifacts were
written outside the checkout; the source candidate was not changed.

# Approve 1p for notebook bug: preserve final notes without a trailing newline

## Problem Description

The text importer silently drops the final note when its input file has no trailing newline. **Owning cell: `notebook`. Kind of work: bug. Decision needed now: approve a bounded parser correction and regression coverage, to be implemented only after direction approval.**

The [original request](request.md) reports lost final notes in files edited by hand. The repository already defines the expected behavior: a nonempty final line is a note with or without a trailing newline (`README.md:14–16`). The current parser always drops the last segment after splitting on LF (`import_notes.py:7`). That segment is empty in a terminated file, but contains the final note in an unterminated file.

These reproductions were run through the actual CLI. Here `\n` denotes an LF byte:

| File content | Expected JSON | Observed JSON |
| --- | --- | --- |
| `First\nSecond\n` | `["First", "Second"]` | `["First", "Second"]` |
| `First\nSecond` | `["First", "Second"]` | `["First"]` |
| `Only` | `["Only"]` | `[]` |

Every CLI invocation above returned exit code 0 with empty stderr. This explains the silent failure. It is a confirmed trigger consistent with the reports; no affected users' original files were supplied.

Evidence: [recorded checks and numbered source excerpts](evidence/checks.txt), from revision `9fd2e6c5c76c15135da7aba9191d45f374b5be07`. Both existing unit tests pass; both use newline-terminated input. The investigation found 5 mismatches in 13 direct-parser cases and 4 in 12 CLI cases, all involving an unterminated final note. The remaining cases establish compatibility examples.

## Non Goals

This direction excludes changes to the web editor, storage APIs, persistence, autosave, the CLI interface, JSON formatting, encoding policy, or line-separator definitions. It does not add trimming, Unicode normalization, blank notes, new dependencies, or recovery of previously lost output. No UI mockup is needed.

## What we are planning to do

After approval, correct `parse_notes` so it considers every segment produced by the existing LF split, including the final segment, and continues filtering only empty strings. This removes the unconditional last-segment discard. The existing empty-string filter already handles a trailing file terminator.

Add focused regression coverage in the notebook repository for single and multiple unterminated notes, alongside compatibility checks for terminated files, empty/blank lines, whitespace content, and Unicode. Validate the real CLI with UTF-8 files and existing newline handling, then rerun the repository suite. The change is confined to the parser and its tests; no cross-cell execution is needed.

The [reproduction script](evidence/reproduce.py) exercises the unmodified implementation. Run `python3 -B evidence/reproduce.py /path/to/notebook/checkout` from this artifact directory. Its current exit code 1 records the reproduced mismatches; it is not a successful fix verification. No implementation, repository test edits, or detailed specification has been written.

## Compat/Upgrade

No migration or new dependency is required. The intended output difference is that an unterminated, nonempty final segment is retained. Empty files and leading, interior, or trailing empty lines still produce no empty notes. Spaces and tabs remain content, including in a final note; they are not treated as empty lines.

Keep UTF-8 decoding, character sequences, ordering, and current JSON escaping unchanged. Preserve LF-only splitting in direct parser calls, including Unicode separator characters as note content. Preserve the CLI's existing text-reader behavior for CRLF and CR files. Already emitted JSON cannot be repaired by this parser change; regenerating it requires the original input file.

## Key challenges/design questions & answers

| Question | Answer |
| --- | --- |
| Is this a bug or a new capability? | A bug: accepting a final note without a trailing newline is explicitly documented in `README.md:14–16`. Approval is for restoring that contract. |
| What causes the missing note? | `source.split('\n')[:-1]` drops the final segment unconditionally. A trailing LF makes that segment empty; without one it holds note text. The CLI and direct parser both reproduce the loss. |
| Why is the proposed scope sufficient? | Considering all LF-separated segments retains the final note; the existing empty-string filter already removes terminator segments and other empty lines. This addresses the cause in the owning parser without changing surrounding interfaces. This reasoning remains to be verified against an implementation after approval. |
| What exactly counts as a blank line? | An empty string between separators. Existing behavior retains spaces, tabs, and surrounding whitespace verbatim. Keep that distinction; do not add `strip()` or broaden the blank-line definition. |
| Could fixing the final line create an extra empty note? | The proposed direction retains the existing empty-string filter, so an empty final segment remains ignored. Empty files and repeated trailing newlines are explicit compatibility cases. |
| How will Unicode be preserved? | Leave decoding and JSON serialization alone and preserve each nonempty segment's characters. The checks cover accents, CJK, emoji, combining characters, and U+0085/U+2028/U+2029 inside notes. Keep LF-only splitting rather than adopting a broader line-splitting rule. |
| What about Windows or CR-only files? | The actual CLI already imports terminated CRLF and CR inputs as separate notes through its text reader. CRLF input without a final terminator loses its last note too. Keep file reading unchanged. Direct parser calls have different CR behavior: literal CR remains content, as captured in the checks. |
| Why did existing tests miss this? | Both tests end their input with LF. They cover terminated notes and an interior blank line, but never exercise a final nonempty segment. Add regression coverage for that boundary, retaining the existing tests. |
| Does storage need consultation or a new interface? | No. `PURPOSE.md:3–5` assigns the text import CLI to notebook, and `import_notes.py:10–11` reads a file and prints JSON without calling storage. Storage behavior does not determine this fix. |
| What evidence is available, and what remains uncertain? | Local checks on Python 3.11.2 reproduce the defect and document compatibility examples. There are no supplied real-world failing files, so we cannot attribute every reported loss to this trigger. No changed implementation has been tested. `c2j self` and `c2j cells` were unavailable because `.c2/config.yaml` is absent; local ownership and reproduction are established from repository sources. No feedback or returned-work files were present. |
| What is the recommendation and decision? | Approve the parser-only correction plus focused tests described above. The documented contract resolves the behavior questions; the only pending decision is direction approval before implementation. |

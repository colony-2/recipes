# Notebook bug: retain the final note without a trailing newline

People lose the last note when importing a text file without a trailing newline. I recommend retaining every nonempty newline-delimited segment, including the last one, while preserving existing blank-line and Unicode behavior. This restores the behavior already promised by the README.

## Problem Description

The [submitted request](request.md) describes silent final-note loss, often with hand-edited files. I reproduced it in both the parser and CLI: `First\nSecond` imports only `First`, and a single unterminated note imports nothing. The CLI exits successfully without a warning.

`parse_notes` unconditionally discards the last segment after splitting on `\n`. That segment is empty when a file has a final newline, but otherwise contains a real note. Both existing tests end their input with a newline, so they pass despite the bug. The [source findings](evidence/findings.md) and [reproduction results](evidence/reproduction.txt) establish the cause.

## Non Goals

Changes to the editor, persistence, import format, supported encodings, JSON output, or error reporting; whitespace trimming; Unicode normalization; and recovery of previously omitted notes.

## What we are planning to do

I will correct final-segment handling in the notebook parser, keeping its existing LF delimiter and empty-segment filter. A missing final newline will produce the same notes as the equivalent file with a final newline.

I will add regression coverage for single and multiple unterminated notes, blank-line boundaries, and Unicode content. Compatibility checks will cover empty files, whitespace-only notes, embedded Unicode separators, and the CLI's existing newline handling. Validation will include the full unittest suite and actual UTF-8 files passed through the CLI.

## Compat/Upgrade

No migration or command change is needed. Newline-terminated files keep their current results. Unterminated files gain the final note that was incorrectly omitted. Empty lines remain ignored, including the empty segment after a final newline. Spaces and tabs remain note content. UTF-8 decoding and JSON serialization stay unchanged.

Existing source files can be imported again after the fix to obtain the full JSON result; the importer itself does not persist notes or restore prior output.

## Key challenges/design questions & answers

| Question                                             | Answer                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Is the absent final newline invalid input?           | No. README.md explicitly says a nonempty final line is a note with or without a newline. I recommend accepting it without a new warning or format requirement.                                                                                                                                                                                                                         |
| Why does the current logic lose data?                | It removes the last split segment without checking whether it is empty. Filtering empty segments already handles file terminators, so dropping a segment is unnecessary.                                                                                                                                                                                                               |
| What counts as a blank line?                         | An empty segment. Existing behavior preserves spaces and tabs, including whitespace-only notes. I will preserve this distinction and retain an unterminated whitespace-only note too.                                                                                                                                                                                                  |
| Should splitting or Unicode handling change?         | No. Keep splitting only on LF, without stripping or normalization. A broader line splitter would also split Unicode separators such as U+0085, U+2028, and U+2029, which currently remain inside notes. Accents, combining marks, non-Latin text, and emoji must retain their exact content.                                                                                           |
| What about CRLF and CR files?                        | The CLI currently normalizes these through text-file reading; observed terminated files import correctly and unterminated ones show the same loss. Keep that behavior. Direct parser calls retain carriage returns as content; the fix should not introduce new normalization there.                                                                                                   |
| Does storage need to change?                         | No. PURPOSE.md assigns this CLI to notebook, and the importer reads a file and prints JSON without calling storage. The correction belongs entirely to notebook.                                                                                                                                                                                                                       |
| What evidence will show the correction works?        | The existing two tests must still pass. Regression checks must retain the final note with and without a newline, including single-note, blank-line, whitespace, and Unicode cases. CLI checks must verify the JSON contents as well as successful exit status. The current reproduction records five parser mismatches and four CLI mismatches, all caused by discarded final content. |
| How certain is the diagnosis for the reported files? | The deterministic failure is established locally and explains the report. No original affected files were supplied, so I cannot establish which editor omitted their final newline or exclude unrelated issues in those files. No unresolved product choice prevents this bounded correction.                                                                                          |

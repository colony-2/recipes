# Notebook importer investigation

Confirmed silent final-note loss when a file lacks a trailing newline. Both existing tests pass; the diagnostic reproduces five parser mismatches and four CLI mismatches, with compatibility cases for blank lines, whitespace, Unicode, and conventional file line endings.

[The proposed direction](one-pager.md) is ready for review. Repository code and tests are unchanged. After direction approval, correct final-segment handling and add regression coverage, then rerun the suite and CLI checks.

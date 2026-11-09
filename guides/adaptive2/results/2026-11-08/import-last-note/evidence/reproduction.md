# Importer reproduction and compatibility evidence

Baseline collected on 2026-11-08 with Python 3.11.2 at commit `ef2b83120121e9190ec3edc53d6cdbc29f35ddf5`. No importer or repository tests were changed.

## Reproduction

From the repository root, create a temporary UTF-8 input and invoke the existing CLI:

```sh
input_dir=$(mktemp -d)
printf 'First\nSecond' > "$input_dir/notes.txt"
python3 import_notes.py "$input_dir/notes.txt"
```

Observed stdout: `["First"]`; exit code: `0`; stderr: empty. Expected: `["First", "Second"]`.

The exact input bytes are `46697273740a5365636f6e64`. Appending byte `0a` yields `["First", "Second"]`. A file containing only `Only` yields `[]` with exit code 0.

## Why it happens

`import_notes.py:7` splits on LF, then unconditionally slices off the last segment with `[:-1]`. With a trailing LF that segment is empty. Without it, that segment is the final note. The existing `if line` filter already ignores empty segments. The CLI at line 11 emits the shortened list without any indication of failure.

`README.md:14–16` explicitly promises that a nonempty final line is a note with or without a newline. Both existing tests use terminated input, so [their successful baseline](baseline-tests.txt) does not cover the failing case. See [source snapshots](repository-context.md).

## Observations

The [diagnostic script](reproduce.py) collected 37 observations: 12 contract mismatches and 25 matching observations. All mismatches concern a nonempty final segment without a terminator; parser and CLI observations overlap. These are baseline findings, not results for an implemented fix.

Inputs and outputs below use JSON string escaping so invisible characters remain visible. CLI results are decoded JSON; [raw stdout, exit codes, stderr, and input hex](results.json) are retained separately.

| Mode | Case | Input | Actual | Expected | Matches? |
| --- | --- | --- | --- | --- | --- |
| parser | two_notes_terminated | `"First\nSecond\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| parser | two_notes_unterminated | `"First\nSecond"` | `["First"]` | `["First", "Second"]` | **no** |
| parser | one_note_unterminated | `"Only"` | `[]` | `["Only"]` | **no** |
| parser | empty_file | `""` | `[]` | `[]` | yes |
| parser | newline_only | `"\n"` | `[]` | `[]` | yes |
| parser | multiple_empty_lines | `"\n\n\n"` | `[]` | `[]` | yes |
| parser | interior_empty_line | `"First\n\nSecond\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| parser | leading_and_trailing_empty_lines | `"\nFirst\n\nSecond\n\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| parser | empty_lines_unterminated | `"\nFirst\n\nSecond"` | `["First"]` | `["First", "Second"]` | **no** |
| parser | whitespace_line_terminated | `"First\n \t\nLast\n"` | `["First", " \t", "Last"]` | `["First", " \t", "Last"]` | yes |
| parser | whitespace_final_unterminated | `"First\n \t"` | `["First"]` | `["First", " \t"]` | **no** |
| parser | unicode_terminated | `"caf\u00e9\n\u6771\u4eac \ud83d\udcdd\n"` | `["caf\u00e9", "\u6771\u4eac \ud83d\udcdd"]` | `["caf\u00e9", "\u6771\u4eac \ud83d\udcdd"]` | yes |
| parser | unicode_unterminated | `"caf\u00e9\n\u6771\u4eac \ud83d\udcdd"` | `["caf\u00e9"]` | `["caf\u00e9", "\u6771\u4eac \ud83d\udcdd"]` | **no** |
| parser | unicode_no_normalization | `"\u00e9\ne\u0301\n"` | `["\u00e9", "e\u0301"]` | `["\u00e9", "e\u0301"]` | yes |
| parser | embedded_unicode_separators | `"A\u0085B\u2028C\u2029D\n"` | `["A\u0085B\u2028C\u2029D"]` | `["A\u0085B\u2028C\u2029D"]` | yes |
| parser | embedded_control_separators | `"A\u000bB\fC\n"` | `["A\u000bB\fC"]` | `["A\u000bB\fC"]` | yes |
| cli | two_notes_terminated | `"First\nSecond\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| cli | two_notes_unterminated | `"First\nSecond"` | `["First"]` | `["First", "Second"]` | **no** |
| cli | one_note_unterminated | `"Only"` | `[]` | `["Only"]` | **no** |
| cli | empty_file | `""` | `[]` | `[]` | yes |
| cli | newline_only | `"\n"` | `[]` | `[]` | yes |
| cli | multiple_empty_lines | `"\n\n\n"` | `[]` | `[]` | yes |
| cli | interior_empty_line | `"First\n\nSecond\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| cli | leading_and_trailing_empty_lines | `"\nFirst\n\nSecond\n\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| cli | empty_lines_unterminated | `"\nFirst\n\nSecond"` | `["First"]` | `["First", "Second"]` | **no** |
| cli | whitespace_line_terminated | `"First\n \t\nLast\n"` | `["First", " \t", "Last"]` | `["First", " \t", "Last"]` | yes |
| cli | whitespace_final_unterminated | `"First\n \t"` | `["First"]` | `["First", " \t"]` | **no** |
| cli | unicode_terminated | `"caf\u00e9\n\u6771\u4eac \ud83d\udcdd\n"` | `["caf\u00e9", "\u6771\u4eac \ud83d\udcdd"]` | `["caf\u00e9", "\u6771\u4eac \ud83d\udcdd"]` | yes |
| cli | unicode_unterminated | `"caf\u00e9\n\u6771\u4eac \ud83d\udcdd"` | `["caf\u00e9"]` | `["caf\u00e9", "\u6771\u4eac \ud83d\udcdd"]` | **no** |
| cli | unicode_no_normalization | `"\u00e9\ne\u0301\n"` | `["\u00e9", "e\u0301"]` | `["\u00e9", "e\u0301"]` | yes |
| cli | embedded_unicode_separators | `"A\u0085B\u2028C\u2029D\n"` | `["A\u0085B\u2028C\u2029D"]` | `["A\u0085B\u2028C\u2029D"]` | yes |
| cli | embedded_control_separators | `"A\u000bB\fC\n"` | `["A\u000bB\fC"]` | `["A\u000bB\fC"]` | yes |
| cli | crlf_terminated | `"First\r\nSecond\r\n"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| cli | crlf_unterminated | `"First\r\nSecond"` | `["First"]` | `["First", "Second"]` | **no** |
| cli | cr_terminated | `"First\rSecond\r"` | `["First", "Second"]` | `["First", "Second"]` | yes |
| cli | cr_unterminated | `"First\rSecond"` | `["First"]` | `["First", "Second"]` | **no** |
| parser | raw_crlf_preserved | `"First\r\nSecond\r\n"` | `["First\r", "Second\r"]` | `["First\r", "Second\r"]` | yes |

## Alternatives checked

A direct Python probe of `"A\u0085B\u2028C\u2029D\n"` produced:

```json
{"LF_split": ["A\u0085B\u2028C\u2029D", ""], "splitlines": ["A", "B", "C", "D"]}
```

Changing to `splitlines()` would therefore create extra notes from Unicode characters currently preserved inside one note. A whitespace probe of `" \t"` showed `bool(source) == True` and `bool(source.strip()) == False`; trimming would discard an existing nonempty note. Neither behavior change is needed to repair the final-segment loss.

## Re-running the observations

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/reproduce.py /path/to/notebook/repository > /tmp/notebook-import-observations.json
```

Run from the artifact directory, or adjust the script path. The script writes input files into a temporary directory and does not modify the repository. Exit 0 means evidence collection completed; inspect `contract_mismatches` and each result to assess behavior.

## Limits

No original user file was supplied, so this proves a cause consistent with the report rather than identifying every affected editor or every possible loss mechanism. Checks ran on the available Linux/Python 3.11.2 environment; they do not establish a platform/version support matrix. CLI byte fixtures verify its existing CRLF and CR normalization. Direct parser strings retain CR, and the proposed scope preserves that distinction. No replacement parser was implemented or tested.

[Environment discovery](environment-discovery.txt) records the unavailable optional c2j configuration. No external cell behavior is implicated by the current CLI.

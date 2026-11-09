# Importer investigation evidence

I inspected all five tracked files at repository commit `e207d35` using Python 3.11.2. The product and test files remain unchanged. The supplied context consists of [request.md](../request.md); no feedback, error, coordination, or results directories were present in the checkout or supplied inbox.

## Source evidence

`README.md:14–16` defines the expected behavior:

> An empty final line is a file terminator, not an extra note. A nonempty final
> line is a note whether or not the file ends with a newline. Empty lines within
> the file are ignored. The CLI prints the imported notes as JSON.

`import_notes.py:6` contains the entire parser:

```python
return [line for line in source.split('\n')[:-1] if line]
```

Splitting `First\nSecond` yields two nonempty segments. The slice drops `Second`; the empty-segment filter cannot recover it. Splitting `First\nSecond\n` yields an additional empty segment, so dropping the final segment happens to be harmless. Empty strings are already removed by the filter. Spaces, tabs, and Unicode content are retained without modification within the surviving segments.

`import_notes.py:10` reads with UTF-8 and prints JSON. It makes no storage calls. `test_import_notes.py:6–10` covers only terminated two-note input and terminated input with an internal empty line. `PURPOSE.md:3–5` assigns the text import CLI to notebook and persistence to storage. `index.html` uses the draft API separately and has no importer implementation.

## Checks and results

The [baseline test log](baseline-tests.txt) records both existing tests passing. The [read-only probe](reproduce.py) exercises the unchanged parser and invokes the actual CLI on temporary files; its [complete output](reproduction.txt) records:

- Parser: eight matching cases and five mismatches. Missing final notes include a single note, a note after an internal blank line, whitespace-only content, and Unicode content.
- CLI: five matching cases and four mismatches. LF, CRLF, CR, and UTF-8 examples all lose the unterminated final note while exiting with status zero and empty stderr.
- Preserved baseline behavior: empty files and empty lines yield no extra notes; whitespace remains content; accents, combining marks, CJK text, emoji, and Unicode line separators survive inside retained notes.

The CLI normalizes conventional line endings through its text read. Direct parser input has no such normalization, as confirmed by a separate carriage-return case. The proposed correction preserves both boundaries.

Reproduce from the repository root with the supporting script's absolute path substituted below:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
PYTHONDONTWRITEBYTECODE=1 python3 /absolute/path/to/evidence/reproduce.py .
```

The probe prints comparisons rather than asserting a passing suite: its zero exit status only indicates the diagnostic completed. `MISMATCH` entries expose the current bug. These are baseline findings, not validation of an implemented fix.

## Limits and environment

No original affected files were supplied. Missing final newline is a demonstrated sufficient cause, not proof of how any particular editor saved a user's file.

`c2j self` and `c2j cells` both returned `Error: requires .c2/config.yaml`; that file is absent. Local source and checks establish notebook ownership and the cause without external inputs or another cell's interface changes.

"""Read-only characterization of the checked-out importer; no proposed fix."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("import_notes", repo / "import_notes.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cases = [
    ("terminated notes", "First\nSecond\n", ["First", "Second"]),
    ("unterminated final note", "First\nSecond", ["First", "Second"]),
    ("single unterminated note", "Only", ["Only"]),
    ("empty file", "", []),
    ("only blank lines", "\n\n", []),
    ("blank lines around notes", "\nFirst\n\nSecond\n\n", ["First", "Second"]),
    ("blank lines before unterminated note", "First\n\nSecond", ["First", "Second"]),
    ("spaces and tabs preserved", "  First  \n \n\t\n", ["  First  ", " ", "\t"]),
    ("unterminated whitespace note", "First\n ", ["First", " "]),
    ("terminated Unicode", "café\n東京 📝 e\u0301\n", ["café", "東京 📝 e\u0301"]),
    ("unterminated Unicode", "café\n東京 📝 e\u0301", ["café", "東京 📝 e\u0301"]),
    ("Unicode separators in note", "A\u0085B\u2028C\u2029D\n", ["A\u0085B\u2028C\u2029D"]),
    ("direct parser retains carriage return", "First\r\nSecond\r\n", ["First\r", "Second\r"]),
]
mismatches = 0
print("Direct parser: expected results follow README and existing content preservation.")
for label, source, expected in cases:
    actual = module.parse_notes(source)
    matches = actual == expected
    mismatches += not matches
    print(f"{'MATCH' if matches else 'MISMATCH'} {label}: input={ascii(source)} expected={ascii(expected)} actual={ascii(actual)}")
print(f"Parser: {len(cases) - mismatches}/{len(cases)} match; {mismatches} reproduce final-segment loss.")

cli_cases = [
    ("LF terminated", b"First\nSecond\n", ["First", "Second"]),
    ("LF unterminated", b"First\nSecond", ["First", "Second"]),
    ("CRLF terminated", b"First\r\nSecond\r\n", ["First", "Second"]),
    ("CRLF unterminated", b"First\r\nSecond", ["First", "Second"]),
    ("CR terminated", b"First\rSecond\r", ["First", "Second"]),
    ("CR unterminated", b"First\rSecond", ["First", "Second"]),
    ("UTF-8 terminated with blank lines", "\ncafé\n\n東京 📝 e\u0301\n\n".encode("utf-8"), ["café", "東京 📝 e\u0301"]),
    ("UTF-8 unterminated", "café\n東京 📝 e\u0301".encode("utf-8"), ["café", "東京 📝 e\u0301"]),
    ("UTF-8 separators in note", "A\u0085B\u2028C\u2029D\n".encode("utf-8"), ["A\u0085B\u2028C\u2029D"]),
]
cli_mismatches = 0
print("CLI: temporary UTF-8 files; output decoded as JSON; return code checked.")
with tempfile.TemporaryDirectory(prefix="notebook-import-probe-") as tmp:
    input_file = Path(tmp) / "notes.txt"
    for label, contents, expected in cli_cases:
        input_file.write_bytes(contents)
        result = subprocess.run([sys.executable, str(repo / "import_notes.py"), str(input_file)], text=True, capture_output=True, check=True)
        actual = json.loads(result.stdout)
        matches = actual == expected
        cli_mismatches += not matches
        print(f"{'MATCH' if matches else 'MISMATCH'} {label}: exit={result.returncode} expected={ascii(expected)} actual={ascii(actual)} stderr={ascii(result.stderr)}")
print(f"CLI: {len(cli_cases) - cli_mismatches}/{len(cli_cases)} match; {cli_mismatches} reproduce silent loss.")

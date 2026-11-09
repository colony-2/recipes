"""Observe current parser/CLI behavior; does not implement a replacement parser.

Usage: python3 reproduce.py /path/to/notebook/repository
Prints JSON evidence, including contract mismatches. Exit 0 means collection
completed, not that the importer meets its contract. Input files are temporary.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("import_notes", repo / "import_notes.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Expected results express README behavior plus preservation of existing text.
cases = [
    ("two_notes_terminated", "First\nSecond\n", ["First", "Second"]),
    ("two_notes_unterminated", "First\nSecond", ["First", "Second"]),
    ("one_note_unterminated", "Only", ["Only"]),
    ("empty_file", "", []),
    ("newline_only", "\n", []),
    ("multiple_empty_lines", "\n\n\n", []),
    ("interior_empty_line", "First\n\nSecond\n", ["First", "Second"]),
    ("leading_and_trailing_empty_lines", "\nFirst\n\nSecond\n\n", ["First", "Second"]),
    ("empty_lines_unterminated", "\nFirst\n\nSecond", ["First", "Second"]),
    ("whitespace_line_terminated", "First\n \t\nLast\n", ["First", " \t", "Last"]),
    ("whitespace_final_unterminated", "First\n \t", ["First", " \t"]),
    ("unicode_terminated", "café\n東京 📝\n", ["café", "東京 📝"]),
    ("unicode_unterminated", "café\n東京 📝", ["café", "東京 📝"]),
    ("unicode_no_normalization", "é\ne\u0301\n", ["é", "e\u0301"]),
    ("embedded_unicode_separators", "A\u0085B\u2028C\u2029D\n", ["A\u0085B\u2028C\u2029D"]),
    ("embedded_control_separators", "A\vB\fC\n", ["A\vB\fC"]),
]

rows = []
for name, source, expected in cases:
    actual = module.parse_notes(source)
    rows.append(dict(mode="parser", case=name, source=source, expected=expected,
                     actual=actual, matches_contract=(actual == expected)))

env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
with tempfile.TemporaryDirectory(prefix="notebook-import-inputs-") as temp:
    for name, source, expected in cases + [
        ("crlf_terminated", "First\r\nSecond\r\n", ["First", "Second"]),
        ("crlf_unterminated", "First\r\nSecond", ["First", "Second"]),
        ("cr_terminated", "First\rSecond\r", ["First", "Second"]),
        ("cr_unterminated", "First\rSecond", ["First", "Second"]),
    ]:
        path = Path(temp) / (name + ".txt")
        path.write_bytes(source.encode("utf-8"))
        result = subprocess.run([sys.executable, str(repo / "import_notes.py"), str(path)],
                                capture_output=True, text=True, encoding="utf-8", env=env)
        actual = json.loads(result.stdout) if result.returncode == 0 else None
        rows.append(dict(mode="cli", case=name, source=source,
                         input_hex=path.read_bytes().hex(), expected=expected, actual=actual,
                         exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
                         matches_contract=(result.returncode == 0 and actual == expected)))

# Raw parser strings retain CR; the CLI's text reader normalizes CR/CRLF first.
source = "First\r\nSecond\r\n"
expected = ["First\r", "Second\r"]
actual = module.parse_notes(source)
rows.append(dict(mode="parser", case="raw_crlf_preserved", source=source,
                 expected=expected, actual=actual, matches_contract=(actual == expected)))

print(json.dumps(dict(
    purpose="Baseline evidence only; contract mismatches are reproduced bugs, not successful tests.",
    python=sys.version,
    repository_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
    observations=len(rows),
    contract_mismatches=sum(not row["matches_contract"] for row in rows),
    results=rows,
), ensure_ascii=True, indent=2))

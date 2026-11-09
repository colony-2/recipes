# Repository context

Inspected commit: `ef2b83120121e9190ec3edc53d6cdbc29f35ddf5`.

Source snapshots below are unchanged repository files. Line numbers are included for review.

## PURPOSE.md

```text
  1: # Notebook purpose
  2: 
  3: Own the notebook web interface and text import CLI. Storage owns persistence and
  4: its API in the `storage` cell. Keep UI behavior here; consult storage about its
  5: interfaces before asking it to build a new one.
```

## README.md

```text
  1: # Notebook
  2: 
  3: Users edit one note in `index.html` and press Save. Navigating to another note
  4: reloads the editor and loses unsaved text. Storage is another registered cell;
  5: its draft API is the supported persistence boundary. No offline support exists.
  6: 
  7: The import CLI accepts one note per line in a UTF-8 text file:
  8: 
  9: ```
 10: python3 import_notes.py notes.txt
 11: python3 -m unittest
 12: ```
 13: 
 14: An empty final line is a file terminator, not an extra note. A nonempty final
 15: line is a note whether or not the file ends with a newline. Empty lines within
 16: the file are ignored. The CLI prints the imported notes as JSON.
```

## import_notes.py

```text
  1: import json
  2: import sys
  3: from pathlib import Path
  4: 
  5: 
  6: def parse_notes(source):
  7:     return [line for line in source.split('\n')[:-1] if line]
  8: 
  9: 
 10: if __name__ == '__main__':
 11:     print(json.dumps(parse_notes(Path(sys.argv[1]).read_text(encoding='utf-8'))))
```

## test_import_notes.py

```text
  1: import unittest
  2: from import_notes import parse_notes
  3: 
  4: 
  5: class ImportTests(unittest.TestCase):
  6:     def test_newline_terminated_notes(self):
  7:         self.assertEqual(parse_notes('First\nSecond\n'), ['First', 'Second'])
  8: 
  9:     def test_blank_lines_are_ignored(self):
 10:         self.assertEqual(parse_notes('First\n\nSecond\n'), ['First', 'Second'])
```

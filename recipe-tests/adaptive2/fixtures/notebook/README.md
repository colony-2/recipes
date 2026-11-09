# Notebook

Users edit one note in `index.html` and press Save. Navigating to another note
reloads the editor and loses unsaved text. Storage is another registered cell;
its draft API is the supported persistence boundary. No offline support exists.

The import CLI accepts one note per line in a UTF-8 text file:

```
python3 import_notes.py notes.txt
python3 -m unittest
```

An empty final line is a file terminator, not an extra note. A nonempty final
line is a note whether or not the file ends with a newline. Empty lines within
the file are ignored. The CLI prints the imported notes as JSON.

# Source snapshots and inspection bounds

Reviewed storage commit: `4bfd5bd201e5e311442950dc394951e19171dc62` (`Test fixture`). The checkout was clean before inspection. No repository changes were made. Inbox identifies notebook source commit `ef2b83120121e9190ec3edc53d6cdbc29f35ddf5`; that provenance is supplied by notebook, not independently fetched.

No applicable AGENTS.md was found in the checkout or its ancestor directories. Root PURPOSE.md was read. The tracked repository contains only PURPOSE.md, README.md, drafts.py, and test_drafts.py; no HTTP handler, deployment configuration, persistence adapter, or dependency manifest is available.

Checks ran with Python 3.11.2 on Linux. The probes used the unchanged checkout and wrote no bytecode or temporary files there.

Environment discovery: `c2j self` and `c2j cells` each exited 1 with `Error: requires .c2/config.yaml`. `c2j --help` lists no `job` inspection command. There is no reported connection or route metadata. No alternate deployment was assumed and no child job was submitted. These limits prevent claims about live HTTP, caching, worker serialization, or durable persistence.

## storage/PURPOSE.md

SHA-256: `e4c5f75fb6e4ed4ceb3bbdc472c39cdf5fa53401e298bc9701ce4a48fe22d0ad`

Line numbers below refer to the original file.

```text
  1 # Storage purpose
  2 
  3 Own draft persistence and the draft API. UI interactions and offline browser
  4 storage belong to the notebook cell. Prefer existing interfaces when sufficient.
```

## storage/README.md

SHA-256: `43604d7cffa4e95250806f2cd6976ed69e524d37678825291104c30ac898c827`

Line numbers below refer to the original file.

```text
  1 # Draft API
  2 
  3 `GET /drafts/{id}` returns `{text, version}`. An absent draft returns empty text
  4 and version zero. `PUT /drafts/{id}` accepts `{text, version}` and returns the
  5 updated draft. The version must match the current draft; otherwise it returns
  6 HTTP 409 and the current version without writing. Text must be valid UTF-8 and
  7 at most 64 KiB. This API already supports frequent draft saves. There is no
  8 separate autosave endpoint.
  9 
 10 Consumers serialize their writes and retain unsaved text on errors. A successful
 11 write followed by a lost response can cause a conflict on retry; read the draft
 12 and compare its text before deciding how to recover. Do not blindly overwrite a
 13 new version. Saving is online only; the API cannot preserve unsent browser text.
 14 
 15 The pure implementation in `drafts.py` models the write contract. Run
 16 `python3 -m unittest` for its checks.
```

## storage/drafts.py

SHA-256: `cc40a9c84791dc0b4d95c0cd56e222e8686074129d069ae6ebc64a48849afb9e`

Line numbers below refer to the original file.

```text
  1 class Conflict(Exception):
  2     pass
  3 
  4 
  5 class Drafts:
  6     def __init__(self):
  7         self.values = {}
  8 
  9     def read(self, name):
 10         return self.values.get(name, {'text': '', 'version': 0}).copy()
 11 
 12     def write(self, name, text, version):
 13         if len(text.encode('utf-8')) > 65536:
 14             raise ValueError('draft is too large')
 15         current = self.read(name)
 16         if version != current['version']:
 17             raise Conflict(current['version'])
 18         result = {'text': text, 'version': version + 1}
 19         self.values[name] = result
 20         return result.copy()
```

## storage/test_drafts.py

SHA-256: `1b3cb3bbcdffc6f3c0348dc886c446458b1b84e83a0d7fe39c0851a97170dc53`

Line numbers below refer to the original file.

```text
  1 import unittest
  2 from drafts import Conflict, Drafts
  3 
  4 
  5 class DraftTests(unittest.TestCase):
  6     def test_save_then_read(self):
  7         store = Drafts()
  8         store.write('one', 'Draft', 0)
  9         self.assertEqual(store.read('one'), {'text': 'Draft', 'version': 1})
 10 
 11     def test_conflicting_tab_cannot_overwrite(self):
 12         store = Drafts()
 13         store.write('one', 'First tab', 0)
 14         with self.assertRaises(Conflict):
 15             store.write('one', 'Second tab', 0)
 16         self.assertEqual(store.read('one')['text'], 'First tab')
```

## inbox/notebook-index.html

SHA-256: `19a037b4136f100f2a23802ed0c1627ac4013389f589f030854e697cb36086b8`

Line numbers below refer to the original file.

```text
  1 <!doctype html>
  2 <html lang="en">
  3 <meta charset="utf-8">
  4 <title>Notebook</title>
  5 <h1>Notebook</h1>
  6 <label>Note <input id="note" value="welcome"></label>
  7 <button id="open">Open</button>
  8 <p><textarea id="text" rows="12" cols="60" aria-label="Note text"></textarea></p>
  9 <button id="save">Save</button>
 10 <p id="status" role="status"></p>
 11 <script>
 12 let version = 0;
 13 const editor = document.querySelector('#text');
 14 const status = document.querySelector('#status');
 15 const note = document.querySelector('#note');
 16 document.querySelector('#open').onclick = async () => {
 17   const response = await fetch('/drafts/' + encodeURIComponent(note.value));
 18   const draft = await response.json();
 19   editor.value = draft.text;
 20   version = draft.version;
 21   status.textContent = '';
 22 };
 23 document.querySelector('#save').onclick = async () => {
 24   const response = await fetch('/drafts/' + encodeURIComponent(note.value), {
 25     method: 'PUT', headers: {'Content-Type': 'application/json'},
 26     body: JSON.stringify({text: editor.value, version})
 27   });
 28   if (!response.ok) { status.textContent = 'Save failed'; return; }
 29   version = (await response.json()).version;
 30   status.textContent = 'Saved';
 31 };
 32 </script>
 33 </html>
```

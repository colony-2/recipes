# Draft API

`GET /drafts/{id}` returns `{text, version}`. An absent draft returns empty text
and version zero. `PUT /drafts/{id}` accepts `{text, version}` and returns the
updated draft. The version must match the current draft; otherwise it returns
HTTP 409 and the current version without writing. Text must be valid UTF-8 and
at most 64 KiB. This API already supports frequent draft saves. There is no
separate autosave endpoint.

Consumers serialize their writes and retain unsaved text on errors. A successful
write followed by a lost response can cause a conflict on retry; read the draft
and compare its text before deciding how to recover. Do not blindly overwrite a
new version. Saving is online only; the API cannot preserve unsent browser text.

The pure implementation in `drafts.py` models the write contract. Run
`python3 -m unittest` for its checks.

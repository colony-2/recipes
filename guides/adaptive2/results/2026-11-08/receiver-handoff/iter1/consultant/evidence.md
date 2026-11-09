# Current storage behavior and consultation checks

## Inspected sources

Managed checkout commit: `f7183c4` (`Test fixture`). It contains four tracked files and no `AGENTS.md`. No repository files were changed.

| Source | Evidence |
| --- | --- |
| `PURPOSE.md:1–5` | Storage owns persistence and the draft API. Notebook owns UI interactions and offline browser storage. Prefer existing interfaces when sufficient. |
| `README.md:3–8` | GET/PUT use `{text, version}`; absent is empty/version zero; stale writes return 409/current version; valid UTF-8 text is capped at 64 KiB; frequent saves use the existing endpoint. |
| `README.md:10–16` | Serialize client writes, retain unsaved text on errors, reconcile a lost-response conflict by reading/comparing text. The implementation is a pure contract model; saving is online only. |
| `drafts.py:5–10` | New instances have an empty dictionary. Reads return the current value or synthetic empty/version zero. No persistence or history read exists. |
| `drafts.py:12–20` | UTF-8 byte size is checked, then version equality; each valid save increments the version and replaces the one stored record. There is no special handling for identical or empty text. |
| `test_drafts.py:5–16` | Two baseline tests cover save/read and sequential stale-tab rejection. They do not establish concurrent transaction safety, HTTP integration, or durable persistence. |

The HTTP behavior above is documented, not exercised by a server in this checkout. The pure model's check-then-write sequence does not establish atomicity under concurrent access. No database, transport adapter, authentication mapping, deployment route, or backup configuration is supplied. Lack of these files is not evidence that an actual deployed service lacks them.

## Local validation

Both baseline unit tests passed with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v`.

An isolated scratch probe imported the unmodified model and verified: only current content survives four writes; stale writes report the head and do not mutate it; identical and empty text create new versions; 65,536 UTF-8 bytes succeed while 65,538 fail; an unencodable surrogate fails without mutation; a lost-response retry conflicts without another commit; a new model instance has no saved state; and no history method exists.

The complete results are in [checks.txt](evidence/checks.txt); the reproducible [probe script](evidence/probe_drafts.py) is evidence only, not an implementation or repository test change. Run it with the checkout on `PYTHONPATH`. Temporary execution files stayed in `/tmp/storage-draft-consult.cjIdQi`, outside checkout and outbox.

## Discovery limits

The inbox directory was empty; there were no exchanged documents or producer references to recover. Both `c2j self` and `c2j cells` returned `Error: requires .c2/config.yaml` (exit 1). The JSON form of self returned the same error. Therefore no reported connection, routes, cell relationships, or `jobs.inspect` capability could be obtained. No child jobs were submitted and no configuration was invented. The consultation is complete on local source evidence; deployment integration remains a required input to the proposed feature.

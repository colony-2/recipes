# Current storage behavior

I inspected the supplied storage repository at commit `3f16094` and `inbox/request.md`. The inbox contained no previous replies. These findings concern the supplied model and documented API; no deployed service was available to verify.

| Source | Finding and consequence |
| --- | --- |
| `PURPOSE.md:3–4` | Storage owns draft persistence and the draft API. Notebook owns UI interactions and offline browser storage. Existing interfaces should be preferred when sufficient. |
| `README.md:3–8` | GET returns `{text, version}`; an absent note is empty at version zero. PUT checks the current version and returns 409 with the current version without writing on a mismatch. Input is valid UTF-8 up to 64 KiB. No separate autosave operation is needed. |
| `README.md:10–13` | Clients serialize writes and retain unsaved text on errors. A lost response can lead to a conflict on retry; read and compare before recovery. The API preserves only text actually sent online. |
| `drafts.py:5–10` | Each instance creates its own dictionary. Reads return a copy of the current value or the version-zero placeholder. There is no durable storage in this implementation. |
| `drafts.py:12–20` | A write validates encoded byte length, checks the supplied version, and replaces the current value with version plus one. It does not preserve the replaced value. Identical text also advances the version. |
| `test_drafts.py:5–16` | The existing two checks cover save/read and rejecting a stale tab's write. They do not establish history or durability. |

The public write contract already allows restoration: chosen historical text is ordinary text input, and the current version supplies the concurrency precondition. A new restore operation would duplicate that behavior. The necessary interface addition is reading earlier text.

I ran `python3 -B -m unittest -v`: both existing tests passed. I also ran the [focused probe](probe.py) against the unchanged repository. It verified the absent-note value, version advancement on identical saves, rejection of a stale identical save, explicit empty saves, exact UTF-8 byte limits, invalid UTF-8 rejection, and loss of data in a newly constructed store. See the [check output](checks.log). These are current-behavior checks, not tests of the proposed feature.

The repository contains only `PURPOSE.md`, `README.md`, `drafts.py`, and `test_drafts.py` as tracked source. There is no HTTP server, persistence adapter, or service configuration to inspect. Both `c2j self` and `c2j cells` returned `Error: requires .c2/config.yaml`; the supplied checkout therefore provided no runtime connection or related-cell metadata. This does not prevent the storage proposal, but deployment durability and route availability remain unverified.

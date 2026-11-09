# Current storage behavior

I inspected the complete checkout at commit `f0a791e` and the request in `inbox/request.md`. The inbox contains no previous replies. There is no applicable `AGENTS.md` in the checkout or its ancestor directories checked.

| Source | Finding |
| --- | --- |
| `PURPOSE.md:3–4` | Storage owns draft persistence and the draft API; notebook owns UI and offline browser storage. Existing interfaces are preferred when sufficient. |
| `README.md:3–8` | Reads return text and a version. Writes require the current version, return a conflict without writing when stale, and accept at most 64 KiB of UTF-8 text. Frequent saves already use the ordinary write operation. |
| `README.md:10–13` | Clients serialize writes, retain unsaved text on errors, and read/compare after an ambiguous retry. Saves are online only. |
| `drafts.py:5–20` | Each `Drafts` instance owns a dictionary holding only current values. There is no history, durable backend, or transaction mechanism. Every successful write advances the version, even when text is unchanged. Reads and writes return copies. |
| `test_drafts.py:5–16` | Two tests cover save/read and rejection of a stale tab's write. They do not establish durability, history, or concurrent transaction behavior. |

The checkout contains only these four files and Git metadata. The documented HTTP operations have no router implementation here. I therefore recommend a model/API change and explicit deployment prerequisites rather than claim a deployed history route exists.

## Local checks

`python3 -B -m unittest -v` passed both existing tests:

```text
test_conflicting_tab_cannot_overwrite ... ok
test_save_then_read ... ok
Ran 2 tests
OK
```

Additional assertions against the unchanged `Drafts` implementation passed:

```text
Absent draft: empty text, version 0.
Identical saves: successful write advances version from 1 to 2.
Stale identical save: conflicts with current version 2; state unchanged.
Empty text: valid saved state, version 3.
New store instance: prior instance data unavailable (no shared backing store).
UTF-8 boundary: 65,536 bytes accepted; 65,537 bytes and lone surrogate rejected without mutation.
Read results: mutating a returned dict does not change stored state.
```

The boundary probe used 32,768 copies of `é`, then appended one ASCII byte for the rejection case. These checks establish compatibility details for the proposed assignment; they do not test the proposed feature.

## Environment discovery

Both `c2j self` and `c2j cells` returned exit code 1 with `Error: requires .c2/config.yaml`. This checkout has no such configuration. Consequently, no task connection, deployed routes, dependent-cell listing, or `jobs.inspect` capability could be established through that discovery. The complete local request and source were available, so this does not prevent the recommendation. Persistent-volume availability and any routing outside this repository remain unverified.

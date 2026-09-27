# Default recipe smoke test opened the persistent user database

## Finding

The initial build/evolve smoke-test attempt used `c2j submit --run --embed`.
That command opens the persistent user runtime, not an ephemeral test database.
The failure was a test-isolation mistake combined with an intentionally
unsupported old database format. It is not evidence of a c2j migration bug.

Observed on 2026-09-27 with `/usr/local/bin/c2j`, version `v0.0.53`:

```text
Error: open JobDB runtime: build sqlite runtime: sqlite runtime: unsupported database format; create a fresh database
```

Binary SHA-256:
`4cc827da70167715f38d2a6bb72a1a218a8e03a8c836ab6da021b21ce82caa1a`.
Bundled JobDB: `v0.0.19-0.20260919034646-71b6668a65db`.

## Reproduction and evidence

On the affected environment, even this listing command exits 1 with the error
above, without executing a recipe:

```bash
cd /src
c2j list --self --embed
```

At investigation time there was no database under `/src/.c2j`. The affected database was
`/home/shai/.c2j/embed/default/swf.db`, 546226176 bytes, last modified
2026-06-20 00:10:28 UTC. Read-only inspection found `PRAGMA user_version = 0`
and populated `swf_jobs` and `strata_*` tables.

The bundled JobDB SQLite runtime's `migrate` function accepts schema version 3
or an empty version-0 database. It deliberately rejects populated version-0
databases. The current c2j upgrade notes require fresh format-3 storage and
state that existing jobs are not migrated.

The initial test attempted to set `C2J_EMBED_ROOT`, but that variable is not
supported by this c2j version. `swfruntime.resolveEmbedRoot` unconditionally
uses the user's home directory for ordinary `--embed` commands. No database
was moved, reset, or deleted during investigation.

## Correct test configuration

Use `c2j test run` with explicit `mode: passthrough` mocks for real operations.
The test runner's `buildHarnessOptions` / `openDisposableEmbedRuntime` creates
a temporary embedded database for passthrough suites and removes it on cleanup.
Mock-only suites do not need an embedded database.

`recipe-tests/run-defaults.sh` now sets a per-run `TMPDIR` so those temporary
databases and harness files are isolated below the test run directory. Its exit
trap removes the runtime scratch directory; the Python harness also cleans its
disposable repositories and result artifacts on exit.
`recipe-tests/verify-default-recipes.py` exercises the real merge operation
against disposable local upstream repositories through this harness.

## Handoff to the c2j team

No database migration fix is requested for this incident. The supported test
harness supplies the needed isolation. A configurable runtime root for ordinary
`submit --embed` could help future CLI lifecycle tests, but it is separate from
this recipe test correction; tests must not silently fall back to user storage.

Acceptance: the default recipe test suite passes with an incompatible persistent
user database still present, creates no jobs there, and cleans up its ephemeral
runtime storage after completion.

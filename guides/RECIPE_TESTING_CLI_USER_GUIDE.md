# c2j Recipe Testing CLI User Guide

This guide covers local recipe test suites with `c2j test`.

The default authoring loop is still:

```bash
c2j submit \
  --recipe-file ./recipes/my-recipe.yaml \
  --run \
  --embed
```

Use `c2j test` when you need curated suites, mocks, repeated cases, artifact assertions, or regression coverage beyond one interactive run.

## Commands

1. `c2j test compile`
   Compile a suite into canonical IR JSON.
2. `c2j test validate`
   Validate selected cases locally.
3. `c2j test run`
   Execute selected cases locally and write run artifacts.
4. `c2j test case validate`
   Validate one case by ID.
5. `c2j test case run`
   Execute one case by ID.

The old `c2 recipe test ...` server path is no longer the normal local harness. See `../RECIPE_TESTING_MIGRATION_GUIDE.md` for command mapping.

## Recipe Targets

Prefer `--recipe-file` while authoring:

```bash
c2j test run \
  --recipe-file ./recipes/my-recipe.yaml \
  --file ./tests/my-suite.scenario.md
```

Named recipes resolve from the current c2j cell:

```bash
c2j test run \
  --recipe default \
  --file ./tests/default.scenario.md
```

Use a git selector when you need an exact remote recipe ref:

```bash
c2j test run \
  --recipe 'git+https://github.com/acme/demo.git//.c2j/recipes/default.yaml@main' \
  --file ./tests/default.scenario.md
```

## Suite Formats

Supported formats:

1. `canonical_yaml`
2. `canonical_json`
3. `compact_yaml`
4. `scenario_md`

`scenario_md` extracts the first fenced YAML or JSON block. A markdown file without a fenced block fails compile.

## Mocks

`mocks.ops` entries match a node invocation and are consumed once per unique invocation.

Matching precedence:

1. `node_path + op`
2. `node_path`
3. `op`
4. declaration order tie-break

For selector-backed extension ops, mock selector resolution and then mock the node path reported by c2j diagnostics:

```yaml
mocks:
  ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: "job-implement/new_session/git+https://github.com/colony-2/c2ops.git//codex@main"
      behavior:
        mode: return
        outputs:
          status: completed
```

If matching the selector-backed op by op name instead of node path, use `extension_execution`. Sequence selector-backed ops generally use the authored node id; state-machine selector-backed ops include the selector in diagnostics.

## Compile

```bash
c2j test compile \
  --recipe-file ./recipes/my-recipe.yaml \
  --file ./tests/my-suite.scenario.md \
  --out /tmp/my-suite.compiled.json \
  --strict
```

## Validate

```bash
c2j test validate \
  --recipe-file ./recipes/my-recipe.yaml \
  --file ./tests/my-suite.scenario.md \
  --parallelism 1
```

Useful flags:

- `--case <id>` can be repeated.
- `--fail-fast` stops scheduling after the first invalid/error result.
- `--json` emits machine-readable validation output.

## Run

```bash
c2j test run \
  --recipe-file ./recipes/my-recipe.yaml \
  --file ./tests/my-suite.scenario.md \
  --parallelism 1 \
  --artifact-mode inline \
  --out-dir /tmp/my-suite.run \
  --evaluation-mode enforce
```

Useful flags:

- `--case <id>` can be repeated.
- `--stop-on-failure` stops scheduling after the first failed/error/invalid result.
- `--case-timeout <duration>` sets a per-case timeout.
- `--artifact-mode none|inline` controls artifact capture.
- `--jsonl-events <path>` writes machine-readable events.

Default output directory:

```text
.c2j/test-results/<timestamp>/
```

## Current c2j Caveats

- `jq(value, expr)` remains a default template helper. Keep jq programs static when possible and pass recipe context as input data.
- `cells()` is a Cortex/runtime helper and is not currently registered by local `c2j test`; recipes that need a cell catalog should run `c2j cells --json` in a `command_execution` step and mock that `load_cells` node in local suites.
- The live Codex smoke recipes set `sandbox.type: none` on c2ops Codex calls, which disables the c2j extension wrapper sandbox. Current c2ops `codex@main` invokes Codex directly and does not require Docker/Podman for an internal Shai runner.
- Prompts and command bodies should reference `{{ context.environment.op.inbox }}` and `{{ context.environment.op.outbox }}` instead of host-only paths or hard-coded `/src/inbox` and `/src/outbox`.
- The op-visible path contract is documented in `../OP_VISIBLE_PATHS_USER_GUIDE.md`.
- If `context.environment.op.worktree_path` resolves empty in `c2j test run`, see `BUG_REPORT_C2J_OP_WORKTREE_PATH_EMPTY_IN_TEST_RUN.md`.
- If live extension steps leave jobs active with a story conflict, see `BUG_REPORT_C2J_STORY_CONFLICT_AFTER_EXTENSION_FAILURE.md`.

## Repository Runner

Run the repo suite with:

```bash
./recipe-tests/run-all.sh
```

That script compiles, validates, and runs all recipe cases with c2j `v0.0.6` or newer. Any failed case should make the script fail.

The repo runner executes the live c2j smoke checks (TS-042..TS-045) and should fail if they fail.

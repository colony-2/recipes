# Requirements: c2j Extension Op Selector Cache

## Status

Product requirement for c2j test and local embedded execution performance.

This document is motivated by Superpowers primary recipe validation on
2026-06-11 UTC using:

```text
c2j version v0.0.33-0.20260611190424-7c9337cb536d
```

## Problem

`c2j test validate` repeatedly prepares the same git-backed c2ops extension
selectors during mocked recipe tests. This makes deterministic tests slow even
when the mocked op never invokes Codex, never mutates git state, and never runs
the extension's real implementation.

Observed with a one-selector mocked suite:

```bash
c2j test validate \
  --recipe-file /src/recipes/superpowers/tests/superpowers-run-skill-output-smoke.yaml \
  --file /src/recipes/superpowers/tests/superpowers-run-skill-output-smoke.scenario.md \
  --parallelism 1 \
  --json
```

Result:

```text
case duration: about 4.5s to 5.9s
/usr/local/bin/codex execs: 0
git clone https://github.com/colony-2/c2ops... execs: 3
git remote-https helpers: 6
git index-pack execs: 3
```

Observed with a partial trace of primary Superpowers validation:

```text
/usr/local/bin/codex execs: 0
git clone https://github.com/colony-2/c2ops... execs in first 90s: 44
git remote-https helpers in first 90s: 88
git index-pack execs in first 90s: 44
```

The cost is not Codex execution and not C2 job git thin-pack restore. It is
repeated git selector resolution/materialization for extension ops, mostly
remote HTTPS clone/fetch plus pack processing.

## Goals

- Make deterministic recipe tests with mocked selector-backed ops complete in
  seconds.
- Resolve and materialize a given extension selector at most once per c2j
  invocation unless the caller explicitly asks to refresh it.
- Reuse previously resolved/materialized extension selectors across c2j
  invocations.
- Preserve correctness for floating refs such as `@main`.
- Keep cache behavior diagnosable in c2j logs and job stories.
- Avoid changing recipe authoring syntax.

## Non-Goals

- Do not cache Codex model responses.
- Do not cache op execution results by default.
- Do not bypass real extension execution when an op is not mocked.
- Do not weaken selector integrity, commit pinning, or manifest validation.
- Do not require recipe authors to vendor c2ops into the worktree.

## Definitions

**Selector-backed extension op:** an op referenced by a git selector, for
example:

```yaml
op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
```

**Resolution:** mapping a submitted selector and ref to immutable metadata such
as repository URL, subpath, resolved commit, manifest path, and content hash.

**Materialization:** making the selected op directory and manifest available on
local disk so c2j can validate schemas or run the extension.

**Execution:** actually invoking the extension op implementation.

## Requirements

### Requirement 1: In-Process Selector Resolution Cache

Within one c2j process, the same normalized selector must be resolved once and
reused everywhere in that process.

Acceptance criteria:

- A test suite with many cases using the same c2ops selector does not run `git
  clone` once per case.
- A recipe graph with many nodes using the same selector does not run `git
  clone` once per node.
- Inline recipe includes share the same selector cache as their parent recipe.
- `child_group`, child recipe, and state-machine validation paths share the
  same cache inside one c2j invocation.
- Concurrent validations deduplicate in-flight resolution work instead of
  racing multiple clones of the same selector.

### Requirement 2: Persistent Selector Cache Across Invocations

c2j should persist resolved/materialized selector data in a local cache and
reuse it across separate c2j commands.

Acceptance criteria:

- Running the same `c2j test validate` command twice does not reclone the same
  c2ops repository on the second run when the resolved ref has not changed.
- The persistent cache key includes at least repository URL, selector subpath,
  submitted ref, resolved commit, and platform-sensitive extension build inputs
  if compiled artifacts are cached.
- The cache location is deterministic and user-inspectable.
- A user or CI job can override the cache directory with an environment variable
  or flag.
- A user or CI job can disable the persistent cache for isolation/debugging.

Suggested controls:

```text
C2J_SELECTOR_CACHE_DIR
c2j --selector-cache-dir <path>
c2j --selector-cache=auto|off|read-only|refresh
```

Exact flag names may vary.

### Requirement 3: Separate Remote Ref Refresh From Repo Materialization

For floating refs such as `@main`, c2j must not reclone the repository just to
learn whether the ref changed.

Acceptance criteria:

- A floating ref can be refreshed with a cheap remote-ref check such as
  `ls-remote` or an equivalent cached mirror operation.
- If the remote ref resolves to a commit already present in cache, no fresh full
  clone is performed.
- If the remote ref resolves to a new commit, c2j fetches only the missing data
  needed for that commit.
- Pinned commit selectors can use the cache without remote access when the
  required commit is already present.

### Requirement 4: Cache Materialized Op Manifests

c2j should cache enough op metadata to validate mocked selector-backed ops
without preparing the full extension working directory repeatedly.

Acceptance criteria:

- Input schema, output schema, manifest name, and validate-mode zero-output
  behavior are available from cache after first resolution.
- `c2j test validate` can validate many mocked nodes that use the same selector
  without repeated git materialization.
- Cache entries record the manifest content hash used for validation.
- If a manifest changes at a floating ref, c2j refreshes the cached manifest
  after resolving the new commit.

### Requirement 5: Mocked Op Short-Circuit

When a test case fully mocks a selector-backed op invocation, c2j should avoid
extension execution and avoid unnecessary extension materialization.

Acceptance criteria:

- A mocked selector-backed op does not execute the extension binary.
- A mocked selector-backed op does not invoke Codex.
- If c2j only needs the manifest for semantic validation, it reads the manifest
  from the selector cache.
- If the mock includes enough output shape to satisfy the recipe contract, c2j
  does not require validate-mode execution of the extension implementation.
- Missing mock outputs should produce recipe semantic diagnostics, not trigger
  repeated remote clone work.

### Requirement 6: Cache Extension Build/Executable Artifacts Separately

If c2j builds or prepares an executable wrapper for an extension op, that
artifact should be cached separately from repository checkout data.

Acceptance criteria:

- Build cache keys include resolved commit, subpath, manifest content hash,
  c2j/c2ops runner ABI version, GOOS, GOARCH, and relevant build options.
- A repeated test run does not rebuild the same extension executable when the
  cache key is unchanged.
- A corrupt build cache entry is detected and evicted.
- Build-cache failures fall back to rebuilding once, then report a clear error
  if rebuild also fails.

### Requirement 7: Cache Integrity And Invalidation

The cache must be safe for floating refs, interrupted runs, and concurrent c2j
processes.

Acceptance criteria:

- Cache writes are atomic.
- Concurrent c2j invocations do not corrupt shared cache entries.
- A partially written cache entry is ignored or cleaned up.
- The cache records resolved commit, source URL, subpath, manifest hash, fetch
  time, and c2j version that wrote it.
- Users can force refresh when debugging stale selector behavior.
- Users can prune old cache entries.

Suggested controls:

```text
c2j cache selectors list
c2j cache selectors prune
c2j cache selectors clear
c2j cache selectors refresh <selector>
```

Exact command names may vary.

### Requirement 8: Observability

c2j should make selector-cache behavior visible without requiring `strace`.

Acceptance criteria:

- Debug logs identify selector cache hits, misses, refreshes, and evictions.
- Test output can optionally summarize selector-cache activity.
- When a selector-backed op is slow to prepare, diagnostics say whether time was
  spent in remote ref refresh, fetch/clone, checkout/materialization, manifest
  loading, build, or extension execution.
- `--json` output can include cache statistics when a verbose or diagnostics
  flag is enabled.

Useful metrics:

- selectors resolved;
- in-process cache hits;
- persistent cache hits;
- remote ref checks;
- git fetch/clone count and duration;
- materialization count and duration;
- extension build count and duration;
- extension execution count and duration.

### Requirement 9: Test Performance Targets

Mocked selector-backed tests should be fast enough to use in the normal recipe
authoring loop.

Acceptance criteria:

- A one-selector mocked `c2j test validate` case should usually complete in
  under one second after a warm cache.
- A suite with many cases using the same selector should not scale linearly
  with remote clone count.
- Full primary Superpowers validate should not reclone c2ops for each
  selector-backed node and case.
- Parallel test execution should not increase total remote clone/fetch count
  for the same selector/ref.

## Superpowers Impact

The Superpowers primary recipe is intentionally composed from inline phase
recipes. Whole-graph validation walks a large selector-backed graph:

- brainstorm;
- write-plan;
- plan-review;
- execute-plan;
- verify;
- finish;
- debug.

The execute-plan phase is the largest multiplier. It includes many
implementation, review, revision, TDD, and gate states. The recipe shape is
reasonable, but the current selector preparation cost makes full primary
validation too slow for routine use.

With selector caching, the same production recipe can remain the validation
target without splitting tests into artificial harness-only recipes just to
avoid selector-preparation overhead.

## Validation Plan

### Baseline Reproduction

Run a one-selector mocked validate with process tracing:

```bash
strace -ff -tt -T -e trace=process \
  -o /tmp/c2j-selector-cache-baseline/trace \
  c2j test validate \
    --recipe-file /src/recipes/superpowers/tests/superpowers-run-skill-output-smoke.yaml \
    --file /src/recipes/superpowers/tests/superpowers-run-skill-output-smoke.scenario.md \
    --parallelism 1 \
    --json
```

Current baseline shows no Codex execution and multiple c2ops git clones.

### Warm Cache Check

After implementing caching:

1. Clear the selector cache.
2. Run the one-selector mocked validate once.
3. Run it a second time.
4. Confirm the second run has no fresh c2ops clone when the selector commit is
   unchanged.

### Full Graph Check

Run:

```bash
c2j test validate \
  --recipe-file /src/recipes/superpowers/superpowers.yaml \
  --file /src/recipes/superpowers/tests/superpowers.scenario.md \
  --parallelism 1 \
  --json
```

Expected after caching:

- all primary cases remain valid;
- c2ops clone/fetch count is bounded by unique selector/ref, not by node count
  or case count;
- repeated invocation is substantially faster with a warm cache;
- `/usr/local/bin/codex` is not invoked for mocked validate cases.

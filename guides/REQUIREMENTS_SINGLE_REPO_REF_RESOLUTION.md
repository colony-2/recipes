# Requirements: Single repo@ref Resolution

## Status

Product requirement for c2j recipe resolution, recipe testing, embedded runs,
and replay.

## Motivation

Recipes can reference git-backed content in multiple places:

- the root recipe source;
- inline recipe nodes;
- child recipe selectors;
- selector-backed extension ops.

Those references often point at different paths in the same repository and the
same submitted ref. For example, a recipe may use both:

```yaml
include: git+https://github.com/colony-2/c2ops.git//recipes/foo.yaml@main
```

and:

```yaml
op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
```

within the same recipe graph.

The submitted ref `main` is mutable. If each reference independently resolves
`repo@main`, one recipe execution can observe different commits for different
nodes. Even when the remote branch does not move, repeated resolution causes
unnecessary network work and makes recipe tests slow.

## Core Requirement

Within one recipe resolution snapshot, a normalized `repo@ref` pair MUST resolve
to exactly one commit. Every recipe selector, inline include, child recipe
selector, and extension op selector using that same normalized `repo@ref` MUST
use that same resolved commit, regardless of repository-relative path.

The resolved commit is part of the recipe snapshot. Runtime execution, test
validation, test run, replay, and mocked-op handling MUST use the snapshot's
resolved commit instead of resolving the same `repo@ref` again.

## Definitions

**Submitted selector:** the selector authored in YAML, such as:

```text
git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
```

**Normalized repo:** the canonical repository identity after equivalent URL
forms have been normalized according to c2j's selector rules.

**Submitted ref:** the ref string authored after `@`, such as `main`,
`refs/heads/main`, a tag, or a commit hash.

**repo@ref key:** the normalized repo plus normalized submitted ref. The
repository-relative path is not part of this key.

**Resolved commit:** the immutable commit hash selected for a `repo@ref key`.

**Recipe resolution snapshot:** the fully resolved graph that c2j executes,
tests, or replays. The snapshot includes expanded inline recipes and resolved
selector metadata.

## Scope

This requirement applies to git-backed selectors for:

- root recipes submitted by selector;
- inline recipe nodes;
- recipe-run and child-recipe selectors;
- selector-backed extension ops;
- selectors reached while validating a test suite;
- selectors reached while running a test suite;
- selectors reached while replaying or resuming an embedded job.

This requirement does not require two independent jobs to share the same
floating-ref resolution. A child job that is submitted as a separate durable job
has its own recipe resolution boundary unless c2j explicitly passes a parent
resolution snapshot or pinned selector into that child job.

## Requirements

### Requirement 1: Resolve repo@ref Once Per Snapshot

During recipe snapshot construction, c2j MUST resolve each unique normalized
`repo@ref key` at most once.

Acceptance criteria:

- Two selectors with the same repo and ref but different paths share one
  resolved commit.
- `git+https://example.com/repo.git//a.yaml@main` and
  `git+https://example.com/repo.git//ops/b@main` do not independently choose
  commits.
- Repeated appearances of the same extension op selector do not trigger
  repeated remote ref resolution inside one snapshot.
- Repeated appearances of different extension op paths in the same repo/ref do
  not trigger repeated remote ref resolution inside one snapshot.

### Requirement 2: Path Resolution Uses The Pinned Commit

After a `repo@ref key` is resolved, every path lookup in that repository MUST be
performed against the pinned resolved commit.

Acceptance criteria:

- Inline recipes in the same repository and ref load content from the same
  commit.
- Extension op manifests in the same repository and ref load content from the
  same commit.
- A later selector path cannot refresh the floating ref and observe a newer
  commit inside the same snapshot.
- Same-repo relative includes inherit the parent recipe's already-resolved
  commit.

### Requirement 3: Runtime Must Not Re-Resolve Snapshot Selectors

The executor MUST treat selector resolution as a snapshot concern. Runtime
execution should consume resolved selector metadata from the snapshot.

Acceptance criteria:

- `c2j test validate` does not run `git ls-remote` for the same `repo@ref key`
  during each mocked extension op.
- `c2j test run` does not run `git ls-remote` for the same `repo@ref key`
  during each extension op execution.
- Embedded execution and replay use the resolved selector metadata recorded in
  the submitted job snapshot.
- If runtime cannot find resolved selector metadata for a git-backed selector,
  it fails with a clear internal consistency error rather than silently
  resolving a new commit.

### Requirement 4: Mocked Tests Preserve Snapshot Semantics

Mocks can replace op behavior, but they MUST NOT weaken selector snapshot
consistency.

Acceptance criteria:

- A fully mocked selector-backed op can return the mocked output without
  re-resolving the selector at execution time.
- If semantic validation needs the op manifest, c2j reads the manifest from the
  snapshot's resolved commit or from a cache entry keyed by that commit.
- Missing mock output fields produce test diagnostics without causing a fresh
  floating-ref lookup for the same selector.

### Requirement 5: Snapshot Metadata Is Visible And Auditable

c2j MUST record enough selector metadata to prove which commit was used.

Acceptance criteria:

- The recipe snapshot records each unique `repo@ref key` and resolved commit.
- Each resolved recipe boundary records source kind, submitted selector,
  resolved selector, resolved commit, and content hash.
- Each resolved extension op records source kind, submitted selector, resolved
  selector, resolved commit, manifest path, and manifest content hash.
- Job stories and test diagnostics can identify the resolved commit used by a
  selector-backed recipe or op.

### Requirement 6: Persistent Caches Must Respect Snapshot Pinning

Persistent selector caches are allowed, but they MUST be subordinate to snapshot
pinning.

Acceptance criteria:

- A cache hit for a floating ref can only be used after the snapshot has chosen
  the resolved commit for that `repo@ref key`, unless the cache entry itself is
  the source of that choice for the snapshot.
- Once the snapshot chooses a commit, later cache refreshes cannot change that
  commit inside the same snapshot.
- Materialized recipe content, op manifests, and extension build artifacts are
  keyed by resolved commit, not only by submitted ref.
- Cache invalidation can affect future snapshots but cannot mutate an already
  built snapshot.

## Expected Behavior Example

Given this recipe:

```yaml
sequence:
  - id: plan
    include: git+https://github.com/colony-2/c2ops.git//recipes/plan.yaml@main

  - id: run_skill
    op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main

  - id: gate
    op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
```

c2j resolves this key once:

```text
https://github.com/colony-2/c2ops.git@main -> <commit-sha>
```

Then all three paths are loaded from `<commit-sha>`:

```text
recipes/plan.yaml
codex/run_skill/op.yaml
rule_gate/op.yaml
```

No runtime node should ask GitHub what `main` means again for this snapshot.

## Validation Plan

### Static Snapshot Check

Create a recipe that references at least two paths in the same repo/ref:

- one inline recipe path;
- two extension op paths.

Run recipe compile or test validation with diagnostics enabled and confirm that
the snapshot records one resolved commit for the shared repo/ref.

### Process Trace Check

Run a mocked test suite that executes multiple selector-backed nodes from the
same repo/ref:

```bash
strace -ff -tt -T -e trace=process \
  -o /tmp/c2j-single-repo-ref/trace \
  c2j test validate \
    --recipe-file ./recipe.yaml \
    --file ./recipe-tests/scenario.md \
    --parallelism 1 \
    --json
```

Expected result:

- at most one remote ref resolution for the shared repo/ref during snapshot
  construction;
- zero additional `git ls-remote` calls for that repo/ref during node
  execution;
- zero `git clone` or `index-pack` calls when the required commit and manifests
  are already materialized in cache;
- all mocked selector-backed ops return their mocked outputs without resolving a
  new commit.

### Moving Ref Check

Use a controlled test repository where a branch can be advanced during a recipe
run.

Expected result:

- the recipe snapshot resolves the branch to commit A;
- the branch moves to commit B while the recipe is running;
- all selectors in the already-built snapshot continue using commit A;
- a later independent job may resolve the same branch to commit B.

## Relationship To Inline Recipe Snapshot Consistency

`guides/INLINE_RECIPE_NODE_USER_GUIDE.md` already states that inline recipe
resolution is snapshot consistent and that the same git repository and submitted
ref resolve to one commit. This document generalizes that expectation to all
git-backed recipe and op selectors used by c2j.

## Relationship To Selector Caching

Single `repo@ref` resolution is a correctness requirement. Selector caching is a
performance mechanism that should make the correctness requirement cheap.

A c2j implementation can satisfy snapshot consistency without a persistent
cache by resolving each unique `repo@ref key` once per snapshot. Persistent
caches improve repeated invocations, but they do not replace the need for a
single resolved commit inside each snapshot.

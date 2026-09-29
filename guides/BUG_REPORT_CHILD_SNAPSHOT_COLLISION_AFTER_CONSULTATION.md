# Awaiting a merged child collides with the parent's workspace snapshot

Status: fixed in c2j `0a48289`, verified 2026-09-29 on clean commit
`0a482892458ebf5c319b0700ad5b7fabd5c97ed2`. Owner: c2j runtime.

Both full build/evolve lifecycle tests now complete, including child verification
and merge, parent worker replacement, dependency consumption, and parent verification
and merge. The companion recipe fix explicitly exports verification artifacts
through `outputs.artifact_refs`; tests check their original child job/task keys.

The historical failure and reproduction are retained below.
Detected 2026-09-29 on clean c2j commit
`bfc97e35b72c2708de7dd7c474375abb0d805783`, built from `git archive` without the
checkout's unrelated uncommitted changes. Local c2ops commit: `73165cf`.
JobDB test service: `v0.0.19-0.20260919034646-71b6668a65db`, in-memory HTTP runtime.

The earlier compiled-include broker and workspace replay regressions pass on
this build. Full default-recipe coverage exposes a separate failure once a child
actually writes, verifies, and merges code. Both build and evolve reproduce it.

## Reproduce

```sh
C2J_BINARY=/path/to/fixed/c2j C2OPS_REPOSITORY=/path/to/c2ops \
  C2J_TEST_LOG_DIR=/tmp/recipe-regression-logs \
  ./recipe-tests/run-defaults.sh
```

For a focused run with the fixed `c2j` on `PATH`, use
`C2J_TEST_LOG_DIR=/tmp/recipe-regression-logs uv run recipe-tests/verify-development-lifecycle.py build`
(or `evolve`). This directly resolves the c2ops selectors unless a Git URL rewrite
is supplied; the full runner above configures that rewrite automatically.

The `verify-development-lifecycle.py` suite installs the production default
recipes as committed `.c2j/recipes/` specializations in two disposable cells.
Only Codex and human decisions are scripted; verification commands run locally
instead of in Shai. All includes, scope/schema gates, broker submissions, waits,
artifacts, Git snapshots and merges use actual c2j operations. No home database
or external repository is modified.

1. Submit A with `--build` or `--evolve`.
2. A completes design and test-plan review/approval, then writes a local candidate.
3. Implementation discovers missing behavior and consults a separate B session
   through node `workspace`. B's temporary experiment is discarded.
4. A returns to design, retains the dialogue, and gets renewed plan approval.
5. A submits the agreed work with `c2j submit --cell B --build` / `--evolve`.
6. Observe A at `PENDING_JOBS` and terminate its worker. Neither upstream has
   changed, and A has not reached final acceptance.
7. Run B's real default recipe: mandate assessment, design, test-plan review,
   implementation, specification/quality reviews, verification, satisfaction,
   and squash merge. B completes successfully, including `merged: true`.
8. Start a replacement A worker. It reconstructs the earlier workflow, then
   fails in the production `recipe.await_result_soft` operation:

```text
ERROR failed to execute op op=recipe.await_result_soft
err="ambiguous workspace snapshot: multiple thin packs in task result"
```

Subsequent automatic job retries can restart the conversation against B's now
advanced upstream; fixture assertions then reject repeated model turns. The
snapshot ambiguity is the first failure, before those secondary errors. Logs
are retained under `lifecycle-build/` and `lifecycle-evolve/` when
`C2J_TEST_LOG_DIR` is set, including parent/child job records and decision traces.

## Expected behavior

Child Git artifacts remain dependency evidence with child provenance. Awaiting
B must not adopt B's snapshot as A's working state or conflict with A's existing
candidate. A should resume its original implementation session, consume the
verified dependency version and artifacts, then complete its own reviews,
verification, acceptance and squash merge. No consultation, approval or child
submission should be repeated.

## Cause and fix

In `pkg/ops/recipe/recipe_output.go`, `decodeRecipeJobOutput` filters internal Git
artifacts from operation output only when `deps.GitContext().Workspace != nil`.
After returning from a foreign workspace, A's root operations have a nil explicit
workspace while workspace-aware forwarding remains active. The await operation
can therefore emit both its own restored thin pack and B's returned thin pack.
`pkg/worker/compiler/artifact_job_context.go` rejects multiple thin packs once
scoped forwarding is active.

The runtime fix preserves child Git artifacts as references while excluding them
from the awaiting task's automatic Git state, including the implicit root workspace.
The recipe fix addresses a separate evidence-export gap: build/evolve now forward
the verification step's artifact references through the coordinator and public
entrypoints. No post-await filtering or synthetic child success is used.

## Acceptance coverage

Keep both original regressions passing. Both full lifecycle cases must then
pass without inlining children, replacing child outputs with synthetic success,
dropping dependency evidence, suppressing errors, or skipping worker replacement.
The tests already assert one child submission, retained candidate/session/history,
real verification evidence, no B experiment propagation, and one squash commit
per cell. No c2j source was changed in this repository.

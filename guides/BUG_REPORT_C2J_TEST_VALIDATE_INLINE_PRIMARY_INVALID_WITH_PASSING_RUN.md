# Bug Report: `c2j test validate` Marks Passing Inline Primary Scenario Invalid

## Summary

`c2j test compile` and `c2j test run` now work for the Superpowers primary
recipe with local inline recipe nodes, but `c2j test validate` still reports the
same passing primary case as `invalid` and emits no actionable diagnostic.
With `v0.0.31-0.20260610223609-4786011e04bd`, validate starts executing the
inline graph before returning `invalid`, so this is no longer the earlier
local-include resolution failure.

This is distinct from the earlier local-include and built-in-op parse failures:

- local inline includes resolve;
- included recipes with `squashrebasemerge` parse;
- `c2j test run` passes the primary inline scenario suite;
- focused phase recipe `validate` still passes, including
  `superpowers-finish.yaml` with `squashrebasemerge`.

## Version

Observed with:

```text
c2j version v0.0.31-0.20260610223609-4786011e04bd
/usr/local/bin/c2j sha256 3e2a2d5dc35ca9e2a298d98b4ab3ad5417ddc56772297fd20d79c5ffd50d5622
```

## Reproduction

Use the Superpowers recipe files in this repository:

- `superpowers.yaml`
- `superpowers-brainstorm.yaml`
- `superpowers-write-plan.yaml`
- `superpowers-plan-review.yaml`
- `superpowers-execute-plan.yaml`
- `superpowers-verify.yaml`
- `superpowers-finish.yaml`
- `superpowers-debug.yaml`
- `recipe-tests/superpowers.scenario.md`

The primary recipe uses local inline includes for the phase recipes.

Compile passes:

```bash
c2j test compile \
  --recipe-file superpowers.yaml \
  --file recipe-tests/superpowers.scenario.md \
  --out /tmp/superpowers.primary.compiled.json \
  --strict
```

Observed:

```text
compiled 5 case(s) to /tmp/superpowers.primary.compiled.json
```

Run passes:

```bash
c2j test run \
  --recipe-file superpowers.yaml \
  --file recipe-tests/superpowers.scenario.md \
  --parallelism 1 \
  --artifact-mode inline \
  --out-dir /tmp/superpowers.primary.run \
  --evaluation-mode enforce
```

Observed:

```text
ts-080-superpowers-orchestrates-same-job-happy-path passed
ts-081-superpowers-stops-at-required-child-boundary passed
ts-085-superpowers-primary-routes-spec-failure-through-revision passed
ts-086-superpowers-primary-enforces-tdd-red-green-refactor passed
ts-088-superpowers-primary-routes-tdd-spec-failure-through-revision passed
```

Validate fails for the same suite:

```bash
c2j test validate \
  --recipe-file superpowers.yaml \
  --file recipe-tests/superpowers.scenario.md \
  --case ts-080-superpowers-orchestrates-same-job-happy-path \
  --parallelism 1 \
  --json
```

Observed:

```text
ts-080-superpowers-orchestrates-same-job-happy-path invalid
{"cases":1,"invalid_or_error":1}
Error: 1 case(s) invalid or errored
```

`c2j test case validate` reports the same status and also does not explain why:

```bash
c2j test case validate \
  --recipe-file superpowers.yaml \
  --file recipe-tests/superpowers.scenario.md \
  --case-id ts-080-superpowers-orchestrates-same-job-happy-path \
  --parallelism 1 \
  --strict
```

Observed:

```text
ts-080-superpowers-orchestrates-same-job-happy-path invalid
Error: 1 case(s) invalid or errored
```

## Control Cases

Focused phase validation still works:

```bash
c2j test validate \
  --recipe-file superpowers-finish.yaml \
  --file recipe-tests/superpowers-finish.scenario.md \
  --parallelism 1 \
  --json
```

Observed:

```text
ts-071-finish-recommends-merge-ready-from-verified-evidence valid
ts-072-finish-blocks-merge-when-verification-has-issues valid
ts-073-finish-merges-only-after-gate-and-explicit-action valid
{"cases":3,"invalid_or_error":0}
```

A small local inline recipe with a selector-backed `codex/run_skill` op,
`node_executed`, and exact mocks also validates successfully. That suggests the
bug is not generic to all inline recipe nodes or all selector-backed extension
mocks.

## Expected Result

`c2j test validate` should report the same primary scenario cases as valid when
`c2j test run --evaluation-mode enforce` passes the same cases with the same
recipe file and scenario file.

If validate intentionally rejects something that run accepts, it should report a
diagnostic explaining the invalid condition, such as a specific stale mock,
schema issue, unsupported assertion, or node path.

## Actual Result

`c2j test validate` reports `invalid` for the primary inline case and provides
no cause beyond the aggregate `invalid_or_error` count.

## Impact

The Superpowers production primary recipe can now be compiled and run under
`c2j test`, but the repository harness cannot yet put `superpowers.yaml` on the
standard compile/validate/run path. The harness must temporarily compile and run
the primary scenario suite while skipping `validate` for that recipe.

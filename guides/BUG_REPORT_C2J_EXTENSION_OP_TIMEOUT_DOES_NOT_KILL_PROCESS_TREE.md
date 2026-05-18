# Bug Report: c2j extension op timeout does not kill process tree

Detected: 2026-05-16 UTC, during the live Codex skill execution smoke.

## Summary

`c2j test run --case-timeout 20m` did not stop an in-flight selector-backed extension op after the case exceeded the configured timeout. The c2j test process remained active, its extension op subprocess tree remained active, and no case failure result was written.

This ticket is about c2j timeout enforcement and process cleanup. The separate Codex hang observed in the same run is tracked in `guides/BUG_REPORT_C2OPS_CODEX_OP_HANGS_DURING_LIVE_SKILL_SMOKE.md`.

## Environment

- Repo: `/src`
- c2j checkout: `/c2j` on `main`, HEAD `fc19fd1 Fix passthrough recipe test op paths`
- c2j binary used: `/tmp/c2j-local-bin/c2j`
- c2ops checkout: `/c2ops` on `main`, HEAD `775ab63 fix codex op path defaults`
- Extension op selector in the observed case: `git+https://github.com/colony-2/c2ops.git//codex@main`

## Reproduction

```bash
/tmp/c2j-local-bin/c2j test run \
  --recipe-file /src/codex-skill-execution-smoke.yaml \
  --file /src/recipe-tests/codex-skill-execution-smoke.scenario.md \
  --parallelism 1 \
  --artifact-mode inline \
  --out-dir /tmp/run-codex-skill-execution-smoke \
  --evaluation-mode enforce \
  --case-timeout 20m
```

Observed case:

- `ts-044-live-codex-skill-executes-and-writes-marker`

## Expected

When a test case exceeds `--case-timeout`, c2j should:

1. Terminate the active extension op and its subprocess tree.
2. Mark the case failed with an explicit timeout error.
3. Write the usual failure result files under the requested `--out-dir`.
4. Return a non-zero process exit code.

## Actual

After the case exceeded 20 minutes, the process tree was still alive:

- `c2j test run ... --case-timeout 20m`
- `go run .`
- the selector-backed c2ops extension wrapper binary
- `node /usr/local/bin/codex exec --experimental-json --dangerously-bypass-approvals-and-sandbox ...`
- the native Codex executable

`/tmp/run-codex-skill-execution-smoke` had no result files. The run had to be terminated externally with `kill -TERM <c2j-pid>`.

## Requirements

- c2j should run each case or extension op with a cancellation context tied to `--case-timeout`.
- Timeout cancellation should terminate the whole process group or subprocess tree, not just the immediate child.
- Timeout cancellation should still produce a durable failed case result with enough diagnostic context to identify the timed-out node.
- Timeout cleanup should work for selector-backed extension ops regardless of the extension implementation.

## Reevaluation 2026-05-18 UTC

Status: confirmed fixed with `/c2j` on `main` at `2863bbb Overlay recipe test timeouts onto execution`.

Evidence:

- A controlled local selector-backed extension op that slept for 30 seconds was run with `--case-timeout 2s`.
- c2j returned in about 2 seconds with process exit status `4`.
- The case result was written as `timed_out` with `failure_category: "timeout"` and `failure_reason: "execution timed out"`.
- No hanging extension-op, `go run`, or c2j child process remained after the run.
- In the live Codex smoke, `ts-045-live-codex-skill-contract-artifacts-and-ref` also timed out at 20 minutes and c2j cleaned up the Codex subprocess tree.

Remaining related issue:

- A later run with `/c2j` at `30581a6`, `/c2ops` at `4bc8d1c`, and `--case-timeout 5m` did not reproduce the Codex hang or timeout-cleanup issue. The remaining failure in that run came from the smoke recipe still expecting the removed cell-path model.
- After updating the smoke recipe to the worktree-root cell model and rebuilding c2j at `cadea4c`, both live Codex skill cases passed with `--case-timeout 5m` (`83,195 ms` and `76,404 ms`).

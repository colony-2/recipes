# Workspace dialogue followed by child wait fails replay

Owner: c2j/JobDB runtime. Reproduced 2026-09-29 against a clean build of c2j
commit `9f9d9d0cfa78` (source extracted with `git archive HEAD`, excluding local
uncommitted runtime edits). JobDB service version:
`v0.0.19-0.20260919034646-71b6668a65db`.

## Reproduction and regression test

Run the committed default-recipe test suite against a workspace-capable c2j:

```sh
C2J_BINARY=/path/to/c2j C2OPS_REPOSITORY=/path/to/c2ops \
  ./recipe-tests/run-defaults.sh
```

The `handoff-replay` case in `recipe-tests/verify-consultations.py` is the regression.
It runs independently of the `broker-includes` regression, so neither hides the other.
It uses disposable Git repositories, deterministic command fixtures for Codex,
a separate in-memory JobDB HTTP service, and real c2j workers. It requires no
model credentials and never uses the home embedded database. Local c2ops
resolution removes repeated GitHub requests from the test.

1. Submit an A job containing the actual shared design recipe.
2. Run the A/B/A/B/A conversation. B runs under an explicit node workspace;
   its Codex fixture is const. Checkpoints restore each cell's separate session.
3. A produces a partial assessment and an agreed external handoff.
4. The implementation session asynchronously submits an inline B child through
   the inherited broker. The production agent captures `jobs.job_ids` and waits.
5. Observe the parent at `PENDING_JOBS`, terminate its worker, run B to completion,
   then start a replacement worker for A.

Expected: replay restores the consultation history and pinned workspaces,
records the child's terminal result, and resumes the existing implementation
session exactly once. No model turn or submission should be repeated.

Observed on replacement worker:

```text
job ... did not reach a terminal state after execution: status=ACTIVE:
workflow was not deterministic: unexpected chapter type "TaskAttemptOutcome" at ordinal 19
```

The replay log ends while reconstructing a design agent turn, before it reaches
the pending implementation continuation. Other runs produced ordinal 15 or 23.
Keeping workers concurrently active also produced nondeterminism; increasing
the await threshold did not establish a reliable fix.

## Isolation and scope

The same dialogue without the subsequent child wait completes and verifies A/B
identity, session restoration, pinned B commit despite upstream movement,
no experimental Git propagation, and no consultation-created jobs. Existing
non-workspace dependency cases pass worker replacement with the same JobDB
harness. The failure is therefore exposed by the combined workflow; the precise
runtime root cause is not yet established.

The child fixture is inline to isolate this from the separately reported
[compiled-include broker failure](BUG_REPORT_CHILD_BROKER_COMPILED_INCLUDES.md).
The [nested JSON serialization issue](BUG_REPORT_NESTED_CEL_JSON.md) is already
avoided by the recipe's transport expressions.

## Requested fix and acceptance

Inspect durable chapter ordering and workspace/state-machine reconstruction
across the parent yield. Preserve task identities, invocation counters, workspace
resolution pins and scoped snapshot forwarding when replaying nested includes
and re-entered consultation states. Do not repair this by re-running submissions
or silently creating new sessions/workspaces.

The final live regression should pass without suppressing errors, resetting the
JobDB, replaying Codex turns, or weakening the identity/provenance assertions.
Keep the existing successful dependency-recovery tests passing. No c2j/runtime
source files were changed in the recipes cell.

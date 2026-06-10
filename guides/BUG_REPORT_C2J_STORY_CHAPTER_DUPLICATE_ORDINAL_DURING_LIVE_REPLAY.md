# Bug Report: c2j story chapter duplicate ordinal during long selector-backed live run

Detected: 2026-06-09 UTC, during a long embedded recipe run with sequential
selector-backed c2ops Codex extension ops.

## Status

Open. Non-blocking for the current Superpowers recipe implementation because
the default live smoke has been narrowed and no longer reproduces the conflict.
Still a c2j reliability bug: job stories should be replay-safe and must not
emit duplicate chapter ordinals during a valid run.

## Environment

- c2j binary: `/usr/local/bin/c2j`
- c2j version: `v0.0.28-0.20260609031142-3374b852aa99`
- c2j binary SHA-256:
  `7e6c92ca316fb0e332d786facd2fb35070e9a589b88253977417efc83117427a`
- Runtime mode: embedded `c2j submit --embed` followed by `c2j run one --embed`
- Extension selector shape:
  `git+https://github.com/colony-2/c2ops.git//codex@main`

## Summary

A long embedded job with many sequential selector-backed Codex extension ops
logged duplicate story chapter ordinal conflicts, then later hit the job total
timeout. The duplicate ordinal errors appeared before the timeout and are
separate from git thin-pack restore failures.

Observed log signatures:

```text
ERROR failed to execute op op=git+https://github.com/colony-2/c2ops.git//codex@main err="persist task outcome chapter 13 for extension_execution:extension_execution: workflow state conflict: chapter ordinal 13 already exists"
ERROR failed to execute op op=git+https://github.com/colony-2/c2ops.git//codex@main err="persist task outcome chapter 26 for extension_execution:extension_execution: workflow state conflict: chapter ordinal 26 already exists"
Error: job total timed out after 30m0s
```

After the timeout, one Codex subprocess from the timed-out extension run was
still present and had to be terminated externally. Timeout cleanup has passed in
other focused tests, so this may be a cleanup regression or a distinct path when
the job total timeout fires after story persistence conflicts.

## Expected Behavior

- c2j assigns story chapter ordinals exactly once per persisted task outcome.
- Re-entry, retry, replay, cached execution, and story refresh paths are
  idempotent for chapter persistence.
- If an extension op result is already represented in the story, c2j updates or
  skips that chapter safely instead of trying to create the same ordinal again.
- A story persistence conflict should either be recovered without an `ERROR` log
  or fail the job immediately with a clear c2j error.
- If the job times out, c2j should cancel the active extension op and its
  subprocess tree.

## Actual Behavior

- c2j tried to persist two task outcome chapters with ordinals that already
  existed.
- The run continued after the duplicate ordinal errors.
- The job eventually timed out at 30 minutes.
- A Codex subprocess remained active after the timeout.

## Why This Is Not The Thin-Pack Restore Bug

The thin-pack restore issue failed the next op while restoring git state and
logged:

```text
Repository lacks these prerequisite commits
```

This bug occurs while persisting job-story chapters:

```text
workflow state conflict: chapter ordinal ... already exists
```

The focused mutating-Codex/git-state smoke passed on the same c2j build and did
not log the thin-pack restore signature.

## Self-Contained Reproduction Shape

The original failure was observed in a broad live skill-quality recipe. The
script below creates a temporary cell repository and a temporary recipe with the
same relevant runtime shape: many sequential selector-backed c2ops Codex
extension ops in one embedded job. It does not depend on any files from this
repository.

Prerequisites:

- `/usr/local/bin/c2j` available.
- `jq` available.
- Codex credentials and c2ops selector access available in the environment.

```bash
#!/usr/bin/env bash
set -euo pipefail

work_dir="$(mktemp -d)"
cell_repo="$work_dir/cell-repo"
recipe="$work_dir/duplicate-chapter-stress.yaml"

git init -b main "$cell_repo" >/dev/null
git -C "$cell_repo" config user.email c2j-repro@example.com
git -C "$cell_repo" config user.name "c2j repro"
printf '# c2j duplicate chapter ordinal repro\n' >"$cell_repo/README.md"
git -C "$cell_repo" add README.md
git -C "$cell_repo" commit -m "seed repro cell" >/dev/null

cat >"$recipe" <<'EOF_RECIPE'
id: duplicate-chapter-stress
version: 0.1.0
sequence:
  - id: prepare
    op: command_execution
    inputs:
      timeout: 2m
      working_directory: /tmp
      run: |
        set -euo pipefail
        test -d "{{ context.environment.op.worktree_path }}"

EOF_RECIPE

for i in $(seq 1 14); do
  cat >>"$recipe" <<EOF_NODE
  - id: codex_$i
    op: git+https://github.com/colony-2/c2ops.git//codex@main
    inputs:
      sandbox:
        type: none
      worktree_path: "{{ context.environment.op.worktree_path }}"
      workdir_path: "{{ context.environment.op.workdir }}"
      artifact_inbox_path: "{{ context.environment.op.inbox }}"
      artifact_outbox_path: "{{ context.environment.op.outbox }}"
      prompt: |
        Write exactly one JSON artifact to:
        {{ context.environment.op.outbox }}/step-$i.json

        The JSON must be:
        {"step": $i, "ok": true}

        Final response must be only that JSON object.

EOF_NODE
done

job_json="$(/usr/local/bin/c2j submit --cell "$cell_repo" --recipe-file "$recipe" --embed --json)"
tenant_id="$(printf '%s' "$job_json" | jq -r .tenant_id)"
job_id="$(printf '%s' "$job_json" | jq -r .job_id)"

/usr/local/bin/c2j run one \
  --embed \
  --tenant-id "$tenant_id" \
  --job-id "$job_id" \
  --lease-duration 45m \
  --wait-timeout 45m \
  2>&1 | tee "$work_dir/live.log"

rg -n 'workflow state conflict|chapter ordinal|job total timed out|ERROR' "$work_dir/live.log" || true
printf 'work dir: %s\n' "$work_dir"
```

If this stress recipe does not reproduce the issue immediately, increase the
Codex node count or run it under a test configuration that triggers c2j
re-entry/replay while the job is active. The bug is in the story chapter
persistence path, so a deterministic c2j-level reproduction should not require
any specific skill prompt content.

## Acceptance Criteria For Fix

- Long sequential selector-backed extension jobs do not log duplicate chapter
  ordinal conflicts.
- Replaying or resuming an embedded job does not create a chapter with an
  ordinal that already exists.
- c2j treats story persistence as idempotent or fails immediately with a clear
  fatal error; it must not keep running after a story state conflict.
- Job timeout cancellation cleans up the active extension subprocess tree on
  this path.
- The Superpowers live smoke log scan remains clean for
  `workflow state conflict`, `chapter ordinal`, `ERROR`, and timeout
  signatures.

## Related Docs

- `guides/SUPERPOWERS_RECIPE_GAPS.md`
- `guides/SUPERPOWERS_RECIPE_VALIDATION_TEST_PLAN.md`
- `guides/new-ticket-simplification/REQUIREMENTS_LIVE_CODEX_TIMEOUT_POLICY.md`
- `guides/BUG_REPORT_C2J_THIN_PACK_RESTORE_MISSING_PREREQUISITE_COMMITS.md`
- `guides/BUG_REPORT_C2J_EXTENSION_OP_TIMEOUT_DOES_NOT_KILL_PROCESS_TREE.md`

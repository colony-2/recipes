# Bug Report: c2j Embedded Child-Job Resume Logs Recoverable Replay Cache Miss

## Status

Fixed/validated. Originally observed on 2026-06-09 UTC with:

```text
c2j version v0.0.27-0.20260609025537-b146839f2598
```

Binary used:

```text
/usr/local/bin/c2j
SHA-256: b7d2d0c7e93265b0c9d24f22e6bfec7141d035edd3072cc05df145adbe47fbae
```

Reverified fixed on 2026-06-09 UTC with:

```text
c2j version v0.0.28-0.20260609031142-3374b852aa99
/usr/local/bin/c2j
SHA-256: 7e6c92ca316fb0e332d786facd2fb35070e9a589b88253977417efc83117427a
```

The reproduction completed and the parent/child logs did not contain
`replay cache miss`, `lease is required`, `ERROR`, duplicate artifact errors, or
chapter ordinal conflicts.

## Summary

An embedded parent/child recipe run completes successfully, but logs
recoverable `ERROR` entries for replay cache misses:

```text
replay cache miss: task_result_missing (task=recipe_root_source_resolve ordinal=1 attempt=1)
replay cache miss: task_result_missing (task=recipe.run_and_get_result:finish ordinal=3 attempt=1)
```

The old `persist task outcome chapter ... lease is required` error is gone in
this build. This report is for the remaining noisy replay cache miss errors.

## Impact

The job eventually completes. The issue is that a passing embedded run emits
`ERROR` log entries that look like task failures. That can make it hard to
distinguish real child-job failures from recoverable resume/cache behavior.

## Minimal Reproduction

This reproduction is self-contained and only needs a working `c2j` binary.

Create a temporary cell repository:

```bash
set -euo pipefail

WORK_DIR="$(mktemp -d /tmp/c2j-replay-cache-repro.XXXXXX)"
CELL_REPO="$WORK_DIR/cell-repo"
mkdir -p "$CELL_REPO/.c2j/recipes"

git init -b main "$CELL_REPO" >/dev/null
git -C "$CELL_REPO" config user.email c2j-repro@example.com
git -C "$CELL_REPO" config user.name "c2j repro"

cat >"$CELL_REPO/.c2j/config.yaml" <<EOF_CONFIG
self:
  repo: $CELL_REPO
  ref: main
EOF_CONFIG

cat >"$CELL_REPO/.c2j/recipes/parent-artifact-forwarding.yaml" <<'EOF_PARENT'
id: parent-artifact-forwarding
version: "1.0"
sequence:
  - id: child
    op: recipe.run_and_get_result
    inputs:
      name: child-artifact-forwarding
      inputs: {}
      artifacts: '${{ context.artifacts.map(k, context.artifacts[k]) }}'
outputs:
  child_received: "${{ sequence.child.outputs.outputs.received }}"
EOF_PARENT

cat >"$CELL_REPO/.c2j/recipes/child-artifact-forwarding.yaml" <<'EOF_CHILD'
id: child-artifact-forwarding
version: "1.0"
sequence:
  - id: verify
    op: command_execution
    artifacts:
      submitted/: '${{ context.artifacts }}'
    inputs:
      timeout: 10s
      run: |
        set -euo pipefail
        test -f "{{ context.environment.op.inbox }}/submitted/brief.md"
        grep -q "child-artifact-forwarding-ok" "{{ context.environment.op.inbox }}/submitted/brief.md"
        mkdir -p "{{ context.environment.op.outbox }}/result"
        printf '{"received":true}\n' > "{{ context.environment.op.outbox }}/result/child-artifact.json"
outputs:
  received: true
EOF_CHILD

cat >"$CELL_REPO/README.md" <<'EOF_README'
# c2j replay cache miss reproduction
EOF_README

git -C "$CELL_REPO" add .
git -C "$CELL_REPO" commit -m "seed c2j replay cache repro" >/dev/null

printf 'child-artifact-forwarding-ok\n' > "$WORK_DIR/brief.md"
export C2J_EMBED_ROOT="$WORK_DIR/embed"
```

Submit the parent recipe with one input artifact:

```bash
JOB_JSON="$(c2j submit \
  --cell "$CELL_REPO" \
  --recipe parent-artifact-forwarding \
  --artifact "$WORK_DIR/brief.md" \
  --embed \
  --tenant-id replay-cache-repro \
  --json)"

JOB_ID="$(printf '%s' "$JOB_JSON" | jq -r .job_id)"
```

Run the parent until it starts the child and becomes pending on that child:

```bash
set +e
c2j run one \
  --embed \
  --tenant-id replay-cache-repro \
  --job-id "$JOB_ID" \
  --lease-duration 2m \
  --wait-timeout 30s \
  --on-not-ready fail-on-pending-jobs \
  >"$WORK_DIR/parent-start.log" 2>&1
PARENT_START_STATUS=$?
set -e

test "$PARENT_START_STATUS" -ne 0
CHILD_ID="$(grep -Eo 'wait_for=[A-Za-z0-9]+' "$WORK_DIR/parent-start.log" | head -1 | cut -d= -f2)"
test -n "$CHILD_ID"
```

Run the child:

```bash
c2j run one \
  --embed \
  --tenant-id replay-cache-repro \
  --job-id "$CHILD_ID" \
  --lease-duration 2m \
  --wait-timeout 2m \
  >"$WORK_DIR/child.log" 2>&1
```

Resume the parent:

```bash
c2j run one \
  --embed \
  --tenant-id replay-cache-repro \
  --job-id "$JOB_ID" \
  --lease-duration 2m \
  --wait-timeout 2m \
  >"$WORK_DIR/parent-finish.log" 2>&1
```

Confirm the child and parent completed:

```bash
grep -Eq '\[(live|cached)\] done child-artifact-forwarding' "$WORK_DIR/child.log"
grep -Eq '\[(live|cached)\] done parent-artifact-forwarding' "$WORK_DIR/parent-finish.log"
```

Scan for the unexpected recoverable errors:

```bash
grep -n 'replay cache miss' \
  "$WORK_DIR/parent-start.log" \
  "$WORK_DIR/child.log" \
  "$WORK_DIR/parent-finish.log"
```

Observed output contains:

```text
parent-start.log: replay cache miss: task_result_missing (task=recipe_root_source_resolve ordinal=1 attempt=1)
child.log: replay cache miss: task_result_missing (task=recipe_root_source_resolve ordinal=1 attempt=1)
parent-finish.log: replay cache miss: task_result_missing (task=recipe.run_and_get_result:finish ordinal=3 attempt=1)
```

## Expected Behavior

A passing embedded run should not log `ERROR` entries for expected cache misses
that are handled by live execution.

Expected behavior is one of:

- cache miss is treated as normal control flow and logged below `ERROR`;
- the runtime avoids attempting cached resolution when no cached result exists;
- the runtime records a cache miss without formatting it as a task failure.

## Actual Behavior

The runtime logs task failures for replay cache misses, then continues through
`[live]` execution and completes successfully. Chapters upload with increasing
ordinals and the child artifact is available to the child command op.

## Distinction From Chapter-Ordinal Conflicts

This is not a duplicate chapter ordinal conflict:

- no `workflow state conflict` error appeared;
- no `chapter ordinal ... already exists` error appeared;
- chapters eventually uploaded with increasing ordinals.

## Acceptance Criteria For Fix

- The minimal reproduction above completes child and parent jobs.
- The parent and child logs do not contain recoverable `ERROR` entries for
  `replay cache miss`.
- Existing child artifact forwarding behavior remains intact.

# Bug Report: c2j Cached Child-Job Resume Logs Chapter Persist `lease is required`

## Status

Fixed/validated for the `lease is required` signature. Observed during embedded
child-job validation on 2026-06-09 UTC. Reproduced with the standalone
reproduction below using `c2j run one --on-not-ready fail-on-pending-jobs`.

Reverified fixed on 2026-06-09 UTC against `/usr/local/bin/c2j`
(`c2j version v0.0.27-0.20260609025537-b146839f2598`, binary mtime
`2026-06-09 02:57 UTC`, SHA-256
`b7d2d0c7e93265b0c9d24f22e6bfec7141d035edd3072cc05df145adbe47fbae`): the
reproduction completes and the logs no longer contain `lease is required`.

Follow-up finding: the same run still emits recoverable `ERROR` lines for
`replay cache miss: task_result_missing`. Track that separately from this fixed
lease bug.

Final validation on 2026-06-09 UTC against `/usr/local/bin/c2j`
(`c2j version v0.0.28-0.20260609031142-3374b852aa99`, SHA-256
`7e6c92ca316fb0e332d786facd2fb35070e9a589b88253977417efc83117427a`): the
reproduction completed and the logs did not contain `lease is required`,
`replay cache miss`, recoverable `ERROR`, duplicate artifact errors, or chapter
ordinal conflicts.

## Summary

The embedded child-job artifact-forwarding reproduction completes, but its logs
contain recoverable story/chapter persistence errors:

```text
persist task outcome chapter 1 for recipe_root_source_resolve: lease is required
persist task outcome chapter 3 for recipe.run_and_get_result:finish: lease is required
```

This is not a duplicate chapter ordinal conflict. The logs did not contain
`workflow state conflict`, `chapter ordinal`, or duplicate ordinal errors. This
is a separate story persistence or cached/resume lease handling issue.

## Impact

The job eventually completes. It does create noisy `ERROR` log entries in a
passing embedded run and can make it harder to distinguish real child-job
failures from recoverable cached/resume behavior.

If the same behavior appears in production jobs, operators may see false
failure signals in job logs even though the job later recovers and completes.

## Minimal Reproduction

This reproduction is self-contained and does not depend on any repository other
than a working `c2j` binary.

Create a temporary cell repository:

```bash
set -euo pipefail

WORK_DIR="$(mktemp -d /tmp/c2j-lease-repro.XXXXXX)"
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
# c2j lease-required reproduction
EOF_README

git -C "$CELL_REPO" add .
git -C "$CELL_REPO" commit -m "seed c2j lease repro" >/dev/null

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
  --tenant-id lease-repro \
  --json)"

JOB_ID="$(printf '%s' "$JOB_JSON" | jq -r .job_id)"
```

Run the parent until it starts the child and becomes pending on that child:

```bash
set +e
c2j run one \
  --embed \
  --tenant-id lease-repro \
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
  --tenant-id lease-repro \
  --job-id "$CHILD_ID" \
  --lease-duration 2m \
  --wait-timeout 2m \
  >"$WORK_DIR/child.log" 2>&1
```

Resume the parent:

```bash
c2j run one \
  --embed \
  --tenant-id lease-repro \
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

Now scan for the unexpected story persistence errors:

```bash
grep -n 'lease is required' \
  "$WORK_DIR/parent-start.log" \
  "$WORK_DIR/child.log" \
  "$WORK_DIR/parent-finish.log"
```

Observed output contains:

```text
parent-start.log: persist task outcome chapter 1 for recipe_root_source_resolve: lease is required
child.log: persist task outcome chapter 1 for recipe_root_source_resolve: lease is required
parent-finish.log: persist task outcome chapter 3 for recipe.run_and_get_result:finish: lease is required
```

## Expected Behavior

A passing embedded run should not log `ERROR` entries for story/chapter
persistence when the runtime can recover and complete the job.

Expected behavior is one of:

- the cached task outcome is not persisted without a lease;
- the runtime reacquires or carries the required lease before persisting the
  chapter;
- the runtime treats this as an internal retry detail and does not emit it as a
  user-visible task failure.

## Actual Behavior

The runtime logs task failures in the `[cached]` section of a resumed child-job
path, then continues with `[live]` execution and completes successfully. The log
evidence supports a cached/resume-path issue, but does not by itself prove that
the failing operation is a formal replay step inside c2j internals.

Representative observed flow:

- parent root source resolution first logs a `[cached]` task failure because
  chapter persistence requires a lease;
- parent live execution continues and starts the child;
- child root source resolution logs the same `[cached]` lease error before live
  execution;
- parent finish logs another lease error for `recipe.run_and_get_result:finish`;
- both child and parent eventually upload later chapters and complete.

## Distinction From Chapter-Ordinal Conflicts

This is not a duplicate chapter ordinal conflict:

- no `workflow state conflict` error appeared;
- no `chapter ordinal ... already exists` error appeared;
- chapters eventually uploaded with increasing ordinals.

## Acceptance Criteria For Fix

- The minimal reproduction above completes child and parent jobs.
- The parent and child logs do not contain `lease is required`.
- The logs do not contain recoverable `ERROR` entries for cached task
  outcome persistence.
- Existing child artifact forwarding behavior remains intact.

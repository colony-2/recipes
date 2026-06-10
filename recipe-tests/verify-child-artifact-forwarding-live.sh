#!/usr/bin/env bash
set -euo pipefail

WORK_DIR="/tmp/c2j-child-artifact-forwarding-live"
C2J_BIN="${C2J_BIN:-c2j}"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

prepare_cell_repo() {
  local cell_repo="$WORK_DIR/cell-repo"
  git init -b main "$cell_repo" >/dev/null
  git -C "$cell_repo" config user.email c2j-smoke@example.com
  git -C "$cell_repo" config user.name "c2j smoke"
  mkdir -p "$cell_repo/.c2j/recipes"

  cat >"$cell_repo/.c2j/config.yaml" <<EOF_CONFIG
self:
  repo: $cell_repo
  ref: main
EOF_CONFIG

  cat >"$cell_repo/.c2j/recipes/parent-artifact-forwarding.yaml" <<'EOF_PARENT'
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

  cat >"$cell_repo/.c2j/recipes/child-artifact-forwarding.yaml" <<'EOF_CHILD'
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

  cat >"$cell_repo/README.md" <<'EOF_README'
# Child Artifact Forwarding Smoke Cell
EOF_README

  git -C "$cell_repo" add .
  git -C "$cell_repo" commit -m "seed child artifact forwarding smoke cell" >/dev/null
  printf '%s\n' "$cell_repo"
}

fail_with_log() {
  local message="$1"
  echo "$message"
  for log in "$WORK_DIR/parent-start.log" "$WORK_DIR/child.log" "$WORK_DIR/parent-finish.log"; do
    if [[ -f "$log" ]]; then
      echo "== ${log##*/} =="
      tail -120 "$log"
    fi
  done
  exit 1
}

CELL_REPO="$(prepare_cell_repo)"
printf 'child-artifact-forwarding-ok\n' > "$WORK_DIR/brief.md"
export C2J_EMBED_ROOT="$WORK_DIR/embed"

JOB_JSON="$("$C2J_BIN" submit \
  --cell "$CELL_REPO" \
  --recipe parent-artifact-forwarding \
  --artifact "$WORK_DIR/brief.md" \
  --embed \
  --tenant-id recipe-tests \
  --json)"
JOB_ID="$(printf '%s' "$JOB_JSON" | jq -r .job_id)"

set +e
"$C2J_BIN" run one \
  --embed \
  --tenant-id recipe-tests \
  --job-id "$JOB_ID" \
  --lease-duration 2m \
  --wait-timeout 30s \
  --on-not-ready fail-on-pending-jobs \
  >"$WORK_DIR/parent-start.log" 2>&1
PARENT_START_STATUS=$?
set -e

if [[ "$PARENT_START_STATUS" -ne 0 ]] && ! rg -q 'wait_for=' "$WORK_DIR/parent-start.log"; then
  fail_with_log "TS-046 failed: parent start execution failed"
fi

CHILD_ID="$(rg -o 'wait_for=[A-Za-z0-9]+' "$WORK_DIR/parent-start.log" | head -1 | cut -d= -f2 || true)"
if [[ -z "$CHILD_ID" ]]; then
  fail_with_log "TS-046 failed: parent did not start a child job"
fi

"$C2J_BIN" run one \
  --embed \
  --tenant-id recipe-tests \
  --job-id "$CHILD_ID" \
  --lease-duration 2m \
  --wait-timeout 2m \
  >"$WORK_DIR/child.log" 2>&1
"$C2J_BIN" run one \
  --embed \
  --tenant-id recipe-tests \
  --job-id "$JOB_ID" \
  --lease-duration 2m \
  --wait-timeout 2m \
  >"$WORK_DIR/parent-finish.log" 2>&1

if rg -q 'duplicate submitted artifact' "$WORK_DIR/child.log" "$WORK_DIR/parent-finish.log"; then
  fail_with_log "TS-046 failed: child saw duplicate submitted artifact"
fi

if ! rg -q 'op executed successfully op=command_execution' "$WORK_DIR/child.log"; then
  fail_with_log "TS-046 failed: child did not execute its artifact-reading command"
fi

if ! rg -q '\[(live|cached)\] done child-artifact-forwarding' "$WORK_DIR/child.log"; then
  fail_with_log "TS-046 failed: child recipe did not complete"
fi

if ! rg -q '\[(live|cached)\] done parent-artifact-forwarding' "$WORK_DIR/parent-finish.log"; then
  fail_with_log "TS-046 failed: parent recipe did not complete after child finished"
fi

echo "TS-046 passed"

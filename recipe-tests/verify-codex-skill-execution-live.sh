#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/codex-skill-execution-live"
C2J_BIN="${C2J_BIN:-c2j}"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

prepare_cell_repo() {
  local cell_repo="$WORK_DIR/cell-repo"
  git init -b main "$cell_repo" >/dev/null
  git -C "$cell_repo" config user.email c2j-smoke@example.com
  git -C "$cell_repo" config user.name "c2j smoke"
  mkdir -p "$cell_repo/.c2/tests"
  cat >"$cell_repo/README.md" <<'EOF_README'
# Live Codex Skill Execution Smoke Cell

Temporary cell repository used by c2j live smoke tests.
EOF_README
  git -C "$cell_repo" add README.md .c2
  git -C "$cell_repo" commit -m "seed live codex skill execution smoke cell" >/dev/null
  printf '%s\n' "$cell_repo"
}

"$C2J_BIN" test compile \
  --recipe-file "$PWD/recipes/smoke/codex-skill-execution-smoke.yaml" \
  --file "$ROOT_DIR/codex-skill-execution-smoke.scenario.md" \
  --out "$WORK_DIR/codex-skill-execution.compiled.json" \
  --strict

if [[ ! -s "$WORK_DIR/codex-skill-execution.compiled.json" ]]; then
  echo "TS-044 failed: codex-skill-execution-smoke scenario did not compile"
  exit 1
fi

CELL_REPO="$(prepare_cell_repo)"

run_live() {
  local job_json tenant_id job_id
  job_json="$("$C2J_BIN" submit --cell "$CELL_REPO" --recipe-file "$PWD/recipes/smoke/codex-skill-execution-smoke.yaml" --embed --json)"
  tenant_id="$(printf '%s' "$job_json" | jq -r .tenant_id)"
  job_id="$(printf '%s' "$job_json" | jq -r .job_id)"
  "$C2J_BIN" run one --embed --tenant-id "$tenant_id" --job-id "$job_id" --lease-duration 45m --wait-timeout 45m
}

if ! run_live >"$WORK_DIR/live.log" 2>&1; then
  echo "TS-044/TS-045 failed: c2j live Codex skill execution smoke did not complete"
  cat "$WORK_DIR/live.log"
  exit 1
fi

echo "TS-044 and TS-045 passed"

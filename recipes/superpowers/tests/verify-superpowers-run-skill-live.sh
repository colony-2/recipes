#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/superpowers-run-skill-live"
C2J_BIN="${C2J_BIN:-c2j}"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

prepare_cell_repo() {
  local cell_repo="$WORK_DIR/cell-repo"
  git init -b main "$cell_repo" >/dev/null
  git -C "$cell_repo" config user.email c2j-smoke@example.com
  git -C "$cell_repo" config user.name "c2j smoke"
  cat >"$cell_repo/README.md" <<'EOF_README'
# Live run_skill Smoke Cell

Temporary cell repository used by c2j live smoke tests.
EOF_README
  git -C "$cell_repo" add README.md
  git -C "$cell_repo" commit -m "seed live run_skill smoke cell" >/dev/null
  printf '%s\n' "$cell_repo"
}

dump_diagnostics() {
  if [[ -s "$WORK_DIR/assertions.json" ]]; then
    echo "superpowers run_skill live assertion diagnostics:"
    cat "$WORK_DIR/assertions.json"
  fi
}

"$C2J_BIN" test compile \
  --recipe-file "$TEST_DIR/superpowers-run-skill-live-smoke.yaml" \
  --file "$TEST_DIR/superpowers-run-skill-live-smoke.scenario.md" \
  --out "$WORK_DIR/superpowers-run-skill-live.compiled.json" \
  --strict

if [[ ! -s "$WORK_DIR/superpowers-run-skill-live.compiled.json" ]]; then
  echo "TS-092 failed: superpowers-run-skill-live-smoke scenario did not compile"
  exit 1
fi

CELL_REPO="$(prepare_cell_repo)"

run_live() {
  local job_json tenant_id job_id
  job_json="$("$C2J_BIN" submit --cell "$CELL_REPO" --recipe-file "$TEST_DIR/superpowers-run-skill-live-smoke.yaml" --embed --json)"
  tenant_id="$(printf '%s' "$job_json" | jq -r .tenant_id)"
  job_id="$(printf '%s' "$job_json" | jq -r .job_id)"
  "$C2J_BIN" run one --embed --tenant-id "$tenant_id" --job-id "$job_id" --lease-duration 10m --wait-timeout 10m
}

if ! run_live >"$WORK_DIR/live.log" 2>&1; then
  echo "TS-092/TS-093 failed: c2j live run_skill smoke did not complete"
  dump_diagnostics
  cat "$WORK_DIR/live.log"
  exit 1
fi

if [[ ! -s "$WORK_DIR/assertions.json" ]]; then
  echo "TS-092/TS-093 failed: live run_skill smoke did not produce assertion diagnostics"
  cat "$WORK_DIR/live.log"
  exit 1
fi

if ! jq -e '
  (.failures | length == 0)
  and (.expected_true | to_entries | all(.value == "true"))
  and (.expected_values | to_entries | all(.value.actual == .value.expected))
  and (.artifact_checks.result_exact == true)
  and (.artifact_checks.status_exact == true)
  and (.artifact_checks.validation_schema_valid == true)
  and (.artifact_checks.validation_status_valid == true)
' "$WORK_DIR/assertions.json" >/dev/null; then
  echo "TS-092/TS-093 failed: live run_skill assertions did not pass"
  dump_diagnostics
  cat "$WORK_DIR/live.log"
  exit 1
fi

if rg -n 'workflow state conflict|chapter ordinal|Repository lacks|lease is required|replay cache miss|job total timed out|thin pack|missing prerequisite commit' "$WORK_DIR/live.log"; then
  echo "TS-092/TS-093 failed: c2j live run_skill smoke log contained infrastructure failure signatures"
  dump_diagnostics
  cat "$WORK_DIR/live.log"
  exit 1
fi

echo "TS-092 and TS-093 passed"

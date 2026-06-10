#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/skill-quality-live"
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
# Live Skill Quality Smoke Cell

Temporary cell repository used by c2j live smoke tests.
EOF_README
  git -C "$cell_repo" add README.md .c2
  git -C "$cell_repo" commit -m "seed live skill quality smoke cell" >/dev/null
  printf '%s\n' "$cell_repo"
}

dump_diagnostics() {
  if [[ -s "$WORK_DIR/assertions.json" ]]; then
    echo "skill-quality assertion diagnostics:"
    cat "$WORK_DIR/assertions.json"
  fi
}

# Keep the local scenario compile-valid before running the live c2j submission.
"$C2J_BIN" test compile \
  --recipe-file "$PWD/skill-quality-smoke.yaml" \
  --file "$ROOT_DIR/skill-quality-smoke.scenario.md" \
  --out "$WORK_DIR/skill-quality.compiled.json" \
  --strict

if [[ ! -s "$WORK_DIR/skill-quality.compiled.json" ]]; then
  echo "TS-042 failed: skill-quality-smoke scenario did not compile"
  exit 1
fi

CELL_REPO="$(prepare_cell_repo)"

run_live() {
  local job_json tenant_id job_id
  job_json="$("$C2J_BIN" submit --cell "$CELL_REPO" --recipe-file "$PWD/skill-quality-smoke.yaml" --embed --json)"
  tenant_id="$(printf '%s' "$job_json" | jq -r .tenant_id)"
  job_id="$(printf '%s' "$job_json" | jq -r .job_id)"
  "$C2J_BIN" run one --embed --tenant-id "$tenant_id" --job-id "$job_id" --lease-duration 45m --wait-timeout 45m
}

if ! run_live >"$WORK_DIR/live.log" 2>&1; then
  echo "TS-042/TS-043 failed: c2j live skill-quality smoke did not complete"
  dump_diagnostics
  cat "$WORK_DIR/live.log"
  exit 1
fi

if [[ ! -s "$WORK_DIR/assertions.json" ]]; then
  echo "TS-042/TS-043 failed: skill-quality smoke did not produce assertion diagnostics"
  cat "$WORK_DIR/live.log"
  exit 1
fi

if ! jq -e '
  (.failures | length == 0)
  and (.expected_true | to_entries | all(.value == "true"))
  and (.expected_values | to_entries | all(.value.actual == .value.expected))
' "$WORK_DIR/assertions.json" >/dev/null; then
  echo "TS-042/TS-043 failed: skill-quality assertions did not pass"
  dump_diagnostics
  cat "$WORK_DIR/live.log"
  exit 1
fi

if rg -n 'workflow state conflict|chapter ordinal|Repository lacks|lease is required|replay cache miss|job total timed out|thin pack|missing prerequisite commit' "$WORK_DIR/live.log"; then
  echo "TS-042/TS-043 failed: c2j live skill-quality smoke log contained infrastructure failure signatures"
  dump_diagnostics
  cat "$WORK_DIR/live.log"
  exit 1
fi

echo "TS-042 and TS-043 passed"

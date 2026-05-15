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
  "$C2J_BIN" submit --cell "$CELL_REPO" --recipe-file "$PWD/skill-quality-smoke.yaml" --run --embed
}

if ! run_live >"$WORK_DIR/live.log" 2>&1; then
  echo "TS-042/TS-043 failed: c2j live skill-quality smoke did not complete"
  cat "$WORK_DIR/live.log"
  exit 1
fi

echo "TS-042 and TS-043 passed"

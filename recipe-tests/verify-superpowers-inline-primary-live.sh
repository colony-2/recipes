#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="/tmp/superpowers-inline-primary"
LOG="$WORK_DIR/run.log"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

cd "$ROOT_DIR"

timeout 5m c2j submit \
  --recipe-file ./superpowers.yaml \
  --inputs-json '{"prompt":"debug missing repro","mode":"debug","bug_report":"failing command needs reproduction"}' \
  --run \
  --embed >"$LOG" 2>&1

if ! grep -q 'sequence include_superpowers_debug' "$LOG"; then
  echo "expected embedded run to execute the included debug recipe" >&2
  cat "$LOG" >&2
  exit 1
fi

if ! grep -q 'recipe execution completed successfully' "$LOG"; then
  echo "expected embedded include run to complete successfully" >&2
  cat "$LOG" >&2
  exit 1
fi

if grep -E 'relative include .* has no local recipe directory|unresolved include|ERROR|panic' "$LOG" >/dev/null; then
  echo "inline include runtime log contained a failure signature" >&2
  cat "$LOG" >&2
  exit 1
fi

echo "TS-094 passed"

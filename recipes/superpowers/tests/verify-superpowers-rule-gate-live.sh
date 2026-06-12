#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/superpowers-rule-gate-live"
C2J_BIN="${C2J_BIN:-c2j}"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

"$C2J_BIN" test compile \
  --recipe-file "$TEST_DIR/superpowers-rule-gate-schema-smoke.yaml" \
  --file "$TEST_DIR/superpowers-rule-gate-schema-smoke.scenario.md" \
  --out "$WORK_DIR/rule-gate-schema.compiled.json" \
  --strict

"$C2J_BIN" test validate \
  --recipe-file "$TEST_DIR/superpowers-rule-gate-schema-smoke.yaml" \
  --file "$TEST_DIR/superpowers-rule-gate-schema-smoke.scenario.md" \
  --parallelism 1 \
  --strict

"$C2J_BIN" test run \
  --recipe-file "$TEST_DIR/superpowers-rule-gate-schema-smoke.yaml" \
  --file "$TEST_DIR/superpowers-rule-gate-schema-smoke.scenario.md" \
  --parallelism 1 \
  --artifact-mode inline \
  --out-dir "$WORK_DIR/rule-gate-schema.run" \
  --evaluation-mode enforce \
  --case-timeout 5m

"$C2J_BIN" test compile \
  --recipe-file "$TEST_DIR/superpowers-rule-gate-invalid-input-smoke.yaml" \
  --file "$TEST_DIR/superpowers-rule-gate-invalid-input-smoke.scenario.md" \
  --out "$WORK_DIR/rule-gate-invalid-input.compiled.json" \
  --strict

set +e
"$C2J_BIN" test validate \
  --recipe-file "$TEST_DIR/superpowers-rule-gate-invalid-input-smoke.yaml" \
  --file "$TEST_DIR/superpowers-rule-gate-invalid-input-smoke.scenario.md" \
  --parallelism 1 \
  --strict >"$WORK_DIR/rule-gate-invalid-input.log" 2>&1
INVALID_RC=$?
set -e

if [[ "$INVALID_RC" -eq 0 ]]; then
  echo "TS-048 failed: invalid rule_gate input unexpectedly validated"
  cat "$WORK_DIR/rule-gate-invalid-input.log"
  exit 1
fi

if ! rg -q "missing property 'type'|missing property type|/rules/0" "$WORK_DIR/rule-gate-invalid-input.log"; then
  echo "TS-048 failed: invalid rule_gate input failed with an unexpected diagnostic"
  cat "$WORK_DIR/rule-gate-invalid-input.log"
  exit 1
fi

echo "TS-047 and TS-048 passed"

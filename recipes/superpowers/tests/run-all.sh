#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECIPE_DIR="$(cd "$TEST_DIR/.." && pwd)"
WORK_DIR="/tmp/superpowers-recipe-test-suite"
C2J_BIN="${C2J_BIN:-c2j}"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

run_suite() {
  local recipe_dir="$1"
  local recipe_file="$2"
  local suite_file="$3"
  local name="$4"

  echo "== superpowers/$name: compile =="
  "$C2J_BIN" test compile \
    --recipe-file "$recipe_dir/$recipe_file" \
    --file "$TEST_DIR/$suite_file" \
    --out "$WORK_DIR/${name}.compiled.json" \
    --strict

  echo "== superpowers/$name: validate =="
  "$C2J_BIN" test validate \
    --recipe-file "$recipe_dir/$recipe_file" \
    --file "$TEST_DIR/$suite_file" \
    --parallelism 1 \
    --strict

  echo "== superpowers/$name: run =="
  "$C2J_BIN" test run \
    --recipe-file "$recipe_dir/$recipe_file" \
    --file "$TEST_DIR/$suite_file" \
    --parallelism 1 \
    --artifact-mode inline \
    --out-dir "$WORK_DIR/${name}.run" \
    --evaluation-mode enforce \
    --case-timeout 90s
}

run_recipe_suite() {
  run_suite "$RECIPE_DIR" "$1" "$2" "$3"
}

run_test_recipe_suite() {
  run_suite "$TEST_DIR" "$1" "$2" "$3"
}

run_test_recipe_suite "superpowers-native-task-selection-smoke.yaml" "superpowers-native-task-selection-smoke.scenario.md" "native_task_selection"
run_test_recipe_suite "superpowers-task-session-smoke.yaml" "superpowers-task-session-smoke.scenario.md" "task_session"
run_test_recipe_suite "superpowers-session-contract-smoke.yaml" "superpowers-session-contract-smoke.scenario.md" "session_contract"
run_test_recipe_suite "superpowers-adaptive-task-loop-smoke.yaml" "superpowers-adaptive-task-loop-smoke.scenario.md" "adaptive_task_loop"
run_test_recipe_suite "superpowers-run-skill-output-smoke.yaml" "superpowers-run-skill-output-smoke.scenario.md" "run_skill_output"
run_test_recipe_suite "superpowers-run-skill-repair-smoke.yaml" "superpowers-run-skill-repair-smoke.scenario.md" "run_skill_repair"
run_test_recipe_suite "superpowers-run-skill-live-smoke.yaml" "superpowers-run-skill-live-smoke.scenario.md" "run_skill_live"
run_test_recipe_suite "superpowers-c2-skill-bundle-smoke.yaml" "superpowers-c2-skill-bundle-smoke.scenario.md" "c2_skill_bundle"
run_test_recipe_suite "superpowers-rule-gate-schema-smoke.yaml" "superpowers-rule-gate-schema-smoke.scenario.md" "rule_gate_schema"

run_recipe_suite "superpowers-route.yaml" "superpowers-route.scenario.md" "route"
run_recipe_suite "superpowers-brainstorm.yaml" "superpowers-brainstorm.scenario.md" "brainstorm"
run_recipe_suite "superpowers-write-plan.yaml" "superpowers-write-plan.scenario.md" "write_plan"
run_recipe_suite "superpowers-plan-review.yaml" "superpowers-plan-review.scenario.md" "plan_review"
run_recipe_suite "superpowers-execute-plan.yaml" "superpowers-execute-plan.scenario.md" "execute_plan"
run_recipe_suite "superpowers-verify.yaml" "superpowers-verify.scenario.md" "verify"
run_recipe_suite "superpowers-finish.yaml" "superpowers-finish.scenario.md" "finish"
run_recipe_suite "superpowers-debug.yaml" "superpowers-debug.scenario.md" "debug"
run_recipe_suite "superpowers.yaml" "superpowers.scenario.md" "primary"

"$TEST_DIR/verify-superpowers-rule-gate-live.sh"
"$TEST_DIR/verify-superpowers-child-orchestration-live.sh"
"$TEST_DIR/verify-superpowers-run-skill-live.sh"
"$TEST_DIR/verify-superpowers-inline-primary-live.sh"

echo "Superpowers recipe tests and required live smokes passed."

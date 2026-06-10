#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/recipe-test-suite-all"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

run_suite() {
  local recipe_file="$1"
  local suite_file="$2"
  local name="$3"

  echo "== $name: compile =="
  c2j test compile \
    --recipe-file "$PWD/$recipe_file" \
    --file "$ROOT_DIR/$suite_file" \
    --out "$WORK_DIR/${name}.compiled.json" \
    --strict

  echo "== $name: validate =="
  c2j test validate \
    --recipe-file "$PWD/$recipe_file" \
    --file "$ROOT_DIR/$suite_file" \
    --parallelism 1

  echo "== $name: run =="
  c2j test run \
    --recipe-file "$PWD/$recipe_file" \
    --file "$ROOT_DIR/$suite_file" \
    --parallelism 1 \
    --artifact-mode inline \
    --out-dir "$WORK_DIR/${name}.run" \
    --evaluation-mode enforce
}

run_suite "new-ticket-triage.yaml" "new-ticket-triage.scenario.md" "triage"
run_suite "new-ticket-requirements-planning.yaml" "new-ticket-requirements-planning.scenario.md" "requirements"
run_suite "new-ticket-implementation-planning.yaml" "new-ticket-implementation-planning.scenario.md" "implementation_planning"
run_suite "new-ticket-outcome-determination.yaml" "new-ticket-outcome-determination.scenario.md" "outcome_determination"
run_suite "new-ticket.yaml" "new-ticket.scenario.md" "new_ticket"
run_suite "job-implement.yaml" "job-implement.scenario.md" "implement"
run_suite "job-validate.yaml" "job-validate.scenario.md" "validate"
run_suite "job-merge.yaml" "job-merge.scenario.md" "merge"
run_suite "superpowers-native-task-selection-smoke.yaml" "superpowers-native-task-selection-smoke.scenario.md" "superpowers_native_task_selection"
run_suite "superpowers-task-session-smoke.yaml" "superpowers-task-session-smoke.scenario.md" "superpowers_task_session"
run_suite "superpowers-session-contract-smoke.yaml" "superpowers-session-contract-smoke.scenario.md" "superpowers_session_contract"
run_suite "superpowers-adaptive-task-loop-smoke.yaml" "superpowers-adaptive-task-loop-smoke.scenario.md" "superpowers_adaptive_task_loop"
run_suite "superpowers-run-skill-output-smoke.yaml" "superpowers-run-skill-output-smoke.scenario.md" "superpowers_run_skill_output"
run_suite "superpowers-run-skill-repair-smoke.yaml" "superpowers-run-skill-repair-smoke.scenario.md" "superpowers_run_skill_repair"
run_suite "superpowers-run-skill-live-smoke.yaml" "superpowers-run-skill-live-smoke.scenario.md" "superpowers_run_skill_live"
run_suite "superpowers-c2-skill-bundle-smoke.yaml" "superpowers-c2-skill-bundle-smoke.scenario.md" "superpowers_c2_skill_bundle"
run_suite "superpowers-route.yaml" "superpowers-route.scenario.md" "superpowers_route"
run_suite "superpowers-brainstorm.yaml" "superpowers-brainstorm.scenario.md" "superpowers_brainstorm"
run_suite "superpowers-write-plan.yaml" "superpowers-write-plan.scenario.md" "superpowers_write_plan"
run_suite "superpowers-plan-review.yaml" "superpowers-plan-review.scenario.md" "superpowers_plan_review"
run_suite "superpowers-execute-plan.yaml" "superpowers-execute-plan.scenario.md" "superpowers_execute_plan"
run_suite "superpowers-verify.yaml" "superpowers-verify.scenario.md" "superpowers_verify"
run_suite "superpowers-finish.yaml" "superpowers-finish.scenario.md" "superpowers_finish"
run_suite "superpowers-debug.yaml" "superpowers-debug.scenario.md" "superpowers_debug"
run_suite "superpowers.yaml" "superpowers.scenario.md" "superpowers_primary"

echo "Recipe scenario suites passed: TS-001..TS-023, TS-028..TS-041, and TS-051..TS-093."
"$ROOT_DIR/verify-cli-framework.sh"

"$ROOT_DIR/verify-superpowers-rule-gate-live.sh"
"$ROOT_DIR/verify-child-artifact-forwarding-live.sh"
"$ROOT_DIR/verify-superpowers-child-orchestration-live.sh"
"$ROOT_DIR/verify-superpowers-run-skill-live.sh"
"$ROOT_DIR/verify-codex-skill-execution-live.sh"
"$ROOT_DIR/verify-skill-quality-live.sh"

echo "All recipe tests passed."

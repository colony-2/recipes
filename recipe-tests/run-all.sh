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

run_suite_compile_and_run() {
  local recipe_file="$1"
  local suite_file="$2"
  local name="$3"

  echo "== $name: compile =="
  c2j test compile \
    --recipe-file "$PWD/$recipe_file" \
    --file "$ROOT_DIR/$suite_file" \
    --out "$WORK_DIR/${name}.compiled.json" \
    --strict

  echo "== $name: run =="
  c2j test run \
    --recipe-file "$PWD/$recipe_file" \
    --file "$ROOT_DIR/$suite_file" \
    --parallelism 1 \
    --artifact-mode inline \
    --out-dir "$WORK_DIR/${name}.run" \
    --evaluation-mode enforce
}

run_suite "recipes/new-ticket/new-ticket-triage.yaml" "new-ticket-triage.scenario.md" "triage"
run_suite "recipes/new-ticket/new-ticket-requirements-planning.yaml" "new-ticket-requirements-planning.scenario.md" "requirements"
run_suite "recipes/new-ticket/new-ticket-implementation-planning.yaml" "new-ticket-implementation-planning.scenario.md" "implementation_planning"
run_suite "recipes/new-ticket/new-ticket-outcome-determination.yaml" "new-ticket-outcome-determination.scenario.md" "outcome_determination"
run_suite "recipes/new-ticket/new-ticket.yaml" "new-ticket.scenario.md" "new_ticket"
run_suite "recipes/jobs/job-implement.yaml" "job-implement.scenario.md" "implement"
run_suite "recipes/new-ticket/job-validate.yaml" "job-validate.scenario.md" "validate"
run_suite "recipes/jobs/job-merge.yaml" "job-merge.scenario.md" "merge"

echo "Recipe scenario suites passed: TS-001..TS-023 and TS-028..TS-041. Superpowers suites run below from recipes/superpowers/tests."
"$ROOT_DIR/verify-cli-framework.sh"

"$PWD/recipes/superpowers/tests/run-all.sh"
"$ROOT_DIR/verify-child-artifact-forwarding-live.sh"
"$ROOT_DIR/verify-codex-skill-execution-live.sh"
"$ROOT_DIR/verify-skill-quality-live.sh"

echo "All recipe tests and required live smokes passed."

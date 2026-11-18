#!/usr/bin/env bash
# Run the checks shared by CI and the Recipes verify hook from the repository root.
set -euo pipefail
results=${1:?Usage: scripts/test-recipes.sh RESULTS_DIR}
mkdir -p "$results"
bash build.sh
c2j test run --file recipe-tests/adaptive/consultation-continuation.test.yaml \
  --case native-nested-advice-returns-once --case-timeout 5m --out-dir "$results/authored-smoke" \
  2>&1 | tee "$results/authored-smoke.log"
python3 recipe-tests/checks/recipe_timeout_policy.py .
python3 -B -m unittest discover -s recipe-tests -p test_merge_queue.py
python3 recipe-tests/checks/package_restore_control.py --out-dir "$results/package-restore-unfiltered" \
  2>&1 | tee "$results/package-restore-unfiltered.log"
c2j test run --directory . --case-timeout 10m --out-dir "$results" 2>&1 | tee "$results/run.log"

#!/usr/bin/env bash
# Run the checks shared by CI and the Recipes verify hook from the repository root.
set -euo pipefail
results=${1:?Usage: scripts/test-recipes.sh RESULTS_DIR}
mkdir -p "$results"
bash build.sh
python3 -B -m unittest discover -s recipe-tests/adaptive3 -p 'test_*.py' \
  2>&1 | tee "$results/validators.log"
c2j test validate --directory . 2>&1 | tee "$results/validate.log"
c2j test run --file recipe-tests/adaptive/consultation-continuation.test.yaml \
  --case native-nested-advice-returns-once --case-timeout 5m --out-dir "$results/authored-smoke" \
  2>&1 | tee "$results/authored-smoke.log"
python3 recipe-tests/checks/recipe_timeout_policy.py .
python3 recipe-tests/checks/ask_resumption.py --out-dir "$results/ask-resumption" \
  2>&1 | tee "$results/ask-resumption.log"
python3 recipe-tests/checks/ask_agent_acceptance.py --validate-only --out-dir "$results/ask-agent-declarations" \
  2>&1 | tee "$results/ask-agent-declarations.log"
python3 -B -m unittest discover -s recipe-tests -p test_merge_queue.py
python3 recipe-tests/checks/package_restore_control.py --out-dir "$results/package-restore-unfiltered" \
  2>&1 | tee "$results/package-restore-unfiltered.log"
python3 recipe-tests/checks/package_preparation.py --out-dir "$results/package-preparation" \
  2>&1 | tee "$results/package-preparation.log"
python3 recipe-tests/checks/package_negative_preparation.py --out-dir "$results/package-negative-preparation" \
  2>&1 | tee "$results/package-negative-preparation.log"
c2j test run --directory . --case-timeout 10m --out-dir "$results" 2>&1 | tee "$results/run.log"
python3 recipe-tests/adaptive3/merge-queue-title-checks.py --results "$results"

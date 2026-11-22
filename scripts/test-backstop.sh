#!/usr/bin/env bash
# Fail early on Backstop authority, routing and native review boundaries.
set -euo pipefail
results=${1:?Usage: scripts/test-backstop.sh RESULTS_DIR}
mkdir -p "$results"
python3 -B -m unittest discover -s recipe-tests/review-v2 -p 'test_contract.py' 2>&1 | tee "$results/review-contract.log"
python3 -B -m unittest discover -s recipe-tests/adaptive3 -p 'test_schemas.py' 2>&1 | tee "$results/schemas.log"
for suite in backstop-policy backstop-return backstop-instructions backstop-amendment backstop-configure-recovery; do
  c2j test run --file "recipe-tests/adaptive3/$suite.test.yaml" --case-timeout 5m --out-dir "$results/$suite" 2>&1 | tee "$results/$suite.log"
done

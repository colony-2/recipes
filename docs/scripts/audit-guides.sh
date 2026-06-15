#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "Guides with audit records:"
rg '^  - source: ' docs/data/guide-audit.yaml | sed 's/^  - source: //'

echo
echo "Guides missing audit records:"
while IFS= read -r guide; do
  if ! rg -q "source: ${guide}$" docs/data/guide-audit.yaml; then
    echo "$guide"
  fi
done < <(rg --files guides | sort)


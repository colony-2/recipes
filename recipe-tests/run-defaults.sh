#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$(mktemp -d /tmp/default-recipe-runtime.XXXXXX)"
trap 'rm -rf "$RUNTIME_DIR"' EXIT
# c2j test passthrough creates disposable databases beneath this scratch root.
export TMPDIR="$RUNTIME_DIR"
# Optional workspace-capable binary, without replacing the user's installation.
if [[ -n "${C2J_BINARY:-}" ]]; then
  mkdir -p "$RUNTIME_DIR/bin"
  ln -s "$(realpath "$C2J_BINARY")" "$RUNTIME_DIR/bin/c2j"
  export PATH="$RUNTIME_DIR/bin:$PATH"
fi
# Optional committed local c2ops source keeps repeated selector resolution offline.
if [[ -n "${C2OPS_REPOSITORY:-}" ]]; then
  config_index="${GIT_CONFIG_COUNT:-0}"
  export "GIT_CONFIG_KEY_${config_index}=url.file://$(realpath "$C2OPS_REPOSITORY").insteadOf"
  export "GIT_CONFIG_VALUE_${config_index}=https://github.com/colony-2/c2ops.git"
  export GIT_CONFIG_COUNT="$((config_index + 1))"
fi
# Attempt every family and report any failure, including runtime regressions.
failures=0
for suite in verify-review-contract.py verify-default-recipes.py verify-dependencies.py verify-implementation-consultations.py verify-consultations.py verify-development-lifecycle.py; do
  if ! uv run "$ROOT_DIR/recipe-tests/$suite"; then
    failures=$((failures + 1))
  fi
done
if (( failures > 0 )); then
  printf '%s suite(s) failed; all suites were attempted.\n' "$failures" >&2
  exit 1
fi

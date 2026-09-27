#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$(mktemp -d /tmp/default-recipe-runtime.XXXXXX)"
trap 'rm -rf "$RUNTIME_DIR"' EXIT
# c2j test passthrough creates disposable databases beneath this scratch root.
export TMPDIR="$RUNTIME_DIR"
uv run "$ROOT_DIR/recipe-tests/verify-default-recipes.py"
uv run "$ROOT_DIR/recipe-tests/verify-dependencies.py"

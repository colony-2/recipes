#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "== c2j version =="
c2j version

echo "== example submits =="
c2j submit --recipe-file docs/examples/recipes/hello-command.yaml --inputs-file docs/examples/inputs/hello.yaml --run --embed
c2j submit --recipe-file docs/examples/recipes/artifact-handoff.yaml --run --embed
c2j submit --recipe-file docs/examples/recipes/state-switch.yaml --inputs-json '{"route":"fast"}' --run --embed
c2j submit --recipe-file docs/examples/recipes/include-parent.yaml --inputs-json '{"subject":"docs"}' --run --embed
c2j submit --recipe-file docs/examples/recipes/input-autofill.yaml --run --embed

echo "== example test validation =="
c2j test validate --recipe-file docs/examples/recipes/hello-command.yaml --file docs/examples/tests/hello-command.scenario.md --parallelism 1
c2j test run --recipe-file docs/examples/recipes/hello-command.yaml --file docs/examples/tests/hello-command.scenario.md --parallelism 1 --artifact-mode inline
c2j test validate --recipe-file docs/examples/recipes/artifact-handoff.yaml --file docs/examples/tests/artifact-handoff.scenario.md --parallelism 1
c2j test validate --recipe-file docs/examples/recipes/state-switch.yaml --file docs/examples/tests/state-switch.scenario.md --parallelism 1
c2j test validate --recipe-file docs/examples/recipes/include-parent.yaml --file docs/examples/tests/include-parent.scenario.md --parallelism 1
c2j test validate --recipe-file docs/examples/recipes/input-autofill.yaml --file docs/examples/tests/input-autofill.scenario.md --parallelism 1
c2j test validate --recipe-file docs/examples/recipes/rule-gate.yaml --file docs/examples/tests/rule-gate.scenario.md --parallelism 1

echo "== Hugo build =="
if [ -n "${HUGO_BIN:-}" ]; then
  "$HUGO_BIN" --source docs --destination public
elif command -v hugo >/dev/null 2>&1; then
  hugo --source docs --destination public
elif [ -x /tmp/c2j-docs-bin/hugo ]; then
  /tmp/c2j-docs-bin/hugo --source docs --destination public
else
  echo "hugo is not installed; skipping static-site build" >&2
fi

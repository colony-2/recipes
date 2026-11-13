# Check the validator on a supported worker

The local preinstalled-tool tests check validation behavior. They do not establish
that c2j prepares the declared Python interpreter and libraries correctly.

This check runs the actual validator twice, in separate task environments, against
a Markdown file and a small PNG. It does not alter the validator's package list or
inject Python paths. The second task exercises repeated preparation; inspect each
task's `_c2j/preparation.json` to establish whether packages were prepared or reused.
A first task on an already-warm worker is not proof of fresh-cache coverage.

From this repository:

```sh
# Collect real preparation and validation results on the selected worker pool.
c2j submit 'Check the actual validator dependencies in two separate tasks.' \
  --cell recipes --jobdb http://192.168.1.195:9047/c2 \
  --title 'Check adaptive3 Python and Markdown tools' \
  --advanced-recipe-file guides/repros/validator-environment-check.yaml \
  --artifact review/README.md=recipe-tests/adaptive3/fixtures/validator/README.md \
  --artifact review/pixel.png=recipe-tests/adaptive3/fixtures/validator/pixel.png \
  --json
```

The job collects both outcomes even when validation fails. Its `summary`, `first`
and `repeat` outputs distinguish successful collection from successful validation.
Use `c2j job log` and exact task IDs to inspect command logs and preparation records.

Run on 2026-11-13 at 17:02 UTC:

- Job: `3M3pwm8Fo0AQPLpEYfw5lZMUi2K`.
- Goal: `3M3pwfdfmHTI53t0xqMzewyFC4e`.
- Both tasks failed with `ModuleNotFoundError: No module named 'PIL'`.
- Final summary: “Validator environment check did not pass.”

The [c2j bug](../BUG_REPORT_C2J_PYTHON_DEPENDENCY_ENVIRONMENT.md) remains the blocker.
Its owner must confirm the supported interpreter/library declaration and verify
fresh preparation, retained-cache reuse and explicit rejection of unsupported
dependencies. Rerun this check after that correction is deployed. Do not mark the
worker-preparation todo complete based on the local preinstalled-tool tests.

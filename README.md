# C2 Recipe Examples and Tests

This repository is a working collection of example C2 recipes, recipe authoring
guides, and c2j test suites. The recipes are intended to be run directly from
their YAML files while authoring, then validated with the embedded c2j runtime.

## Directory Layout

- `recipes/new-ticket/` contains the primary new-ticket orchestration example,
  its planning child recipes, and the validation child recipe it invokes by
  name.
- `recipes/jobs/` contains standalone job-phase recipes for implementation and
  merge flows.
- `recipes/smoke/` contains live smoke recipes for c2ops Codex and skill
  execution behavior.
- `recipes/superpowers/` contains the Superpowers recipe family and its local
  test fixtures.
- `recipe-tests/` contains scenario markdown suites and shell runners for the
  top-level example recipes.
- `docs/examples/` contains smaller documentation examples used by the docs
  site and docs validation script.
- `guides/` contains recipe authoring, testing, operation, and design notes.

All recipe YAML files should live under a subdirectory of `recipes/`. Keep test
fixtures either in `recipe-tests/` for repository-wide examples or beside the
recipe family under `recipes/<family>/tests/`.

## Authoring Loop

Start by checking the current cell:

```bash
c2j self
```

Run a recipe directly from its file:

```bash
c2j submit \
  --recipe-file recipes/new-ticket/new-ticket-triage.yaml \
  --inputs-json '{"prompt":"Add retry handling"}' \
  --run \
  --embed
```

Run a scenario suite for one recipe:

```bash
c2j test validate \
  --recipe-file recipes/new-ticket/new-ticket-triage.yaml \
  --file recipe-tests/new-ticket-triage.scenario.md \
  --parallelism 1
```

Run the repository recipe suites:

```bash
./recipe-tests/run-all.sh
```

The full runner includes live smoke tests that require the relevant c2ops,
Codex, git, and `jq` environment to be available. For docs examples only, use:

```bash
./docs/scripts/validate-docs.sh
```

## Authoring Notes

- Prefer `c2j submit --recipe-file ... --run --embed` for local iteration.
- Keep `--recipe-file` examples as repository-relative paths. Bare child recipe
  names inside orchestration recipes still depend on the configured c2 recipe
  source or registry.
- Prefer real C2 ops over ad hoc shell scripts when an op already models the
  workflow.
- Use artifacts for cross-step file handoff instead of relying on implicit
  filesystem state.
- Keep recipe changes small and update `RECIPE_TEST_STATEMENTS.md` when recipe
  behavior or test coverage changes.
- Review `guides/RECIPE_AUTHORING_GUIDE.md`, `guides/ops/README.md`, and
  `guides/NODE_SCOPE_SPEC.md` before making substantial recipe changes.

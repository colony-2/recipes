# C2 Recipe Examples and Tests

This repository is a working collection of example C2 recipes, recipe authoring
guides, and c2j test suites. The recipes are intended to be run directly from
their YAML files while authoring, then validated with the embedded c2j runtime.

## Directory Layout

- `build.yaml` and `evolve.yaml` are the shared c2j default entrypoints.
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

Recipe YAML files should live under a subdirectory of `recipes/`, except for
the two root default entrypoints required by c2j's fallback selectors. Keep test
fixtures either in `recipe-tests/` for repository-wide examples or beside the
recipe family under `recipes/<family>/tests/`.

## Default Build and Evolve

`build.yaml` and `evolve.yaml` are thin entrypoints into
[`recipes/develop/develop.yaml`](recipes/develop/develop.yaml). Both run:

1. Design and independent design review.
2. Test statements and executable test-plan authoring, followed by independent review.
3. Human approval of the design and reviewed test plan.
4. Implementation, independent specification review, and independent quality review.
5. Fresh verification commands and retained evidence.
6. Human satisfaction, then squash merge into the cell's upstream branch.

Feedback continues the same implementation Codex session. Reviewers use fresh
sessions. Requirement changes return to design and require renewed plan approval.
Rejected planning results also return to the design/test-plan cycle, preserving
prior artifacts and feedback. Incomplete implementation requests feedback; invalid
artifacts and missing continuation sessions fail without merging. Automatic c2j
checkpoints preserve edits; only final acceptance publishes them.

Each phase writes a schema-validated `result.json` artifact. Test statements are
also rendered as Markdown, with requirement IDs, filenames, importance, test
level and dependencies. The contract rejects uncovered requirements, duplicate
IDs, missing critical negative cases, and statements without verification commands.
Verification runs the approved commands, saves logs and exit codes, and rejects
changes to the candidate during checks. Merge gates require the accepted, clean,
verified candidate. The merge op uses `rebase: false`: upstream advancement stops
integration rather than silently publishing an unverified rebased tree.

Build starts at the cell root. Evolve starts in `.c2j` and reads the applicable
root and `.c2j/AGENTS.md` instructions. The optional `target_directory` input sets
a different cell-relative scope, for example `.` when editing shared defaults in
this repository. Scope validation rejects traversal, symlink escapes, out-of-scope
changes, and writes during design/review.

Codex and verification use `sandbox.type: shai`. Codex's artifact/runtime paths
retain their defaults; evolve intentionally overrides only `worktree_path`.
**Current upstream limitation:** Shai grants workspace-wide writes, and c2ops
disables Codex's native sandbox. A scoped cwd is not yet a write-isolation boundary.
See [the sandbox bug report](guides/BUG_REPORT_SCOPED_CODEX_SANDBOX.md). Scope gates
block progression after violations; running sandboxed jobs requires a working
Shai/Docker environment.

c2j resolves committed target-cell `.c2j/recipes/build.yaml` or `evolve.yaml` at
the configured ref. Only a missing recipe falls back to the root defaults on
`main` in [colony-2/recipes](https://github.com/colony-2/recipes). Invalid recipes
and access failures remain errors. Evolve creates or edits local specializations;
changing shared defaults requires targeting their repository explicitly.

For a local specialization, reference the shared workflow by selector instead
of copying a root entrypoint whose relative includes expect this repository:

```yaml
id: evolve
version: 0.2.0
input_schema:
  prompt:
    type: string
    required: true
inputs:
  prompt: '${{ inputs.prompt }}'
sequence:
  - id: develop
    include: git+https://github.com/colony-2/recipes.git//recipes/develop/develop.yaml@main
    inputs:
      prompt: '${{ inputs.prompt }}'
      mode: evolve
      target_directory: .c2j
outputs:
  merged: '${{ sequence.develop.outputs.merged }}'
  merged_hash: '${{ sequence.develop.outputs.merged_hash }}'
```

An example domain instruction file is provided at
[`recipes/develop/evolve-AGENTS.md`](recipes/develop/evolve-AGENTS.md).
The [workflow design](guides/BUILD_EVOLVE_SHARED_WORKFLOW_PROPOSAL.md) describes
the phase boundaries and acceptance contracts.

Run a default while authoring:

```bash
c2j submit --recipe-file ./build.yaml --inputs-json '{"prompt":"Add retry handling"}' --run --embed
c2j submit --recipe-file ./evolve.yaml --inputs-json '{"prompt":"Improve workflow feedback","target_directory":"."}' --run --embed
```

Run `./recipe-tests/run-defaults.sh` for comprehensive default-recipe tests.
It requires c2j, git, Python, uv/PyYAML, and Go/access to the c2ops selector for
real gate checks. Codex and human replies are mocked; tests execute real scope
checks, test-plan contracts, verification commands, schema gates and git merges
against disposable repositories. c2j passthrough runtimes use temporary databases,
with scratch files under a per-run `TMPDIR`; tests never submit to the home
embedded database. Rendered sandbox configuration is covered, but a live Codex
or Shai container run is not part of this deterministic suite.

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

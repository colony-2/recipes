# C2 Recipe Examples and Tests

This repository is a working collection of example C2 recipes, recipe authoring
guides, and c2j test suites. The recipes are intended to be run directly from
their YAML files while authoring, then validated with the embedded c2j runtime.

This cell's responsibility boundary is [.c2j/mandate.md](.c2j/mandate.md), using
the [cell mandate specification](guides/CELL_MANDATE_SPEC.md). The
[cross-cell repository sessions design](guides/CROSS_CELL_REPO_SESSIONS_DESIGN.md)
describes implemented conversations against another cell's repository inside the
current job, with disposable code and separate persistent sessions. Both defaults
check mandate fit before implementation.

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

1. Mandate assessment, design, optional cross-cell design dialogue, and independent review.
2. Test-plan authoring, followed by independent review.
3. Human approval of the design and reviewed test plan.
4. Implementation, independent specification review, and independent quality review.
5. The optional verification hook and retained execution evidence.
6. Human satisfaction, then squash merge into the cell's upstream branch.

The entrypoints select the working directory. `develop.yaml` owns the phase order,
human reviews, and merge. It calls one `agent.yaml` loop with a named phase;
the phase prompts and routing schemas live together there. There are no separate
forwarding recipes for design, implementation, or individual reviewers.
`consult.yaml`, `wait-children.yaml`, and `verify.yaml` handle foreign-cell
conversations, prerequisite jobs, and the replaceable verification hook.
Specializations that included an old phase file should now include `agent.yaml`
with its phase name, for example `phase: design` or `phase: implement`.

Design assesses whether the request fits, partially fits, or belongs outside the
plain Markdown `.c2j/mandate.md`. The design explains the ownership split and any
agreed external work. Missing or ambiguous mandates require clarification; outside
requests return routing advice without implementation or merge. These are agent
and human judgments, not machine-validated ownership certificates.

Designs and implementation summaries live in outbox/inbox artifacts. The maintained
test plan lives in `.c2j/test-plan.md` in Git, alongside the mandate. The recipe
copies the exact plan to a review artifact. Agents compare changes through c2j's
existing Git history; no requirement IDs, statement catalogs, or hash ledgers are
required. Test statements retain the Markdown, word-count, annotation, and coverage
conventions, assessed by an independent test-plan reviewer.

Each phase writes a small schema-validated `result.json` containing `summary` and
`next`. Design and implementation can request `consult` with a destination cell
and message. The recipe starts or resumes a separate session in that workspace,
then resumes the originating agent. Foreign experiments are discarded through
`const: true`; session objects and the latest replies survive. This works during
design, late dependency discovery, and human revision rounds. New external work
returns through design approval. See [cross-cell conversations](guides/CROSS_CELL_REPO_SESSIONS_DESIGN.md).

Implementation submits approved prerequisite work asynchronously using `c2j submit
--cell <owner> --build` or `--evolve`. Native `jobs.job_ids` supplies dependencies;
`recipe.await_result_soft` waits for all children and resumes the same session with
results and namespaced artifacts. Failed, cancelled, or unmerged dependencies also
return to that session for diagnosis and recovery. The agent must incorporate the
correct dependency version before proceeding. A cancelled parent does not
necessarily cancel its children.

Cross-cell work requires a shared JobDB service, available workers, and inherited
broker environment in the op sandbox. Tests use clean workspace/object/review-capable
c2j commit `f82bdd2` and a matching disposable JobDB. The historical
[broker](guides/BUG_REPORT_CHILD_BROKER_COMPILED_INCLUDES.md),
[replay](guides/BUG_REPORT_WORKSPACE_DIALOGUE_CHILD_WAIT_REPLAY.md), and
[snapshot collision](guides/BUG_REPORT_CHILD_SNAPSHOT_COLLISION_AFTER_CONSULTATION.md)
regressions remain covered. An older installed CLI is not sufficient.

Verification runs `bash ./build.sh` in the target directory when present, saves
`build.log` and `verification.md`, and uses the native command status and timeout.
A missing hook is explicitly **skipped**, and human acceptance remains available.
Failure returns to implementation with evidence. Projects can specialize the phase
with a real verification op, such as an existing GitHub Actions workflow.

Human satisfaction authorizes squash merge into upstream. The merge uses c2j's
current Git candidate and `rebase: false`; upstream advancement stops integration.
Feedback preserves the implementation session. Reviewers have independent sessions,
and changed requirements require renewed design/test-plan approval.

Build starts at the cell root. Evolve starts in `.c2j` and reads the applicable
root and `.c2j/AGENTS.md` instructions. The optional `target_directory` input sets
a different cell-relative scope, for example `.` when editing shared defaults in
this repository. The recipes set the working directory and instruct agents to respect
the approved design; they do not add a separate changed-file scope enforcement layer.

Build/evolve use native document reviews for plan approval, outcome acceptance,
and feedback. Reviewers can submit text or annotated files, including Markdown
with CriticMarkup. Revisions return to the appropriate agent and require another
review before merge. Workers and authoring tools require c2j `614bfac82f15` or
later. See [review checkpoints and client usage](guides/REVIEW_CHECKPOINTS.md).

Codex and `codex/run_skill` now use c2ops revision
`ded76dfbd877d3d0749e509844ecdbc57197b572`. Workers and authoring tools need c2j
immutable-object support (at least `e1334817a353d4868a97fa5452fe8fe3aee2fc13`)
and Codex CLI **0.157.1** in the execution environment. Continuations forward the
complete `session` object; `session_id` outputs are diagnostic only. Legacy
ID/artifact sessions cannot be resumed with these recipes. Start fresh jobs when
upgrading, carrying any useful summary as ordinary task context. See
[the session migration guide](guides/CODEX_OBJECT_SESSION_MIGRATION.md).

Codex and verification use `sandbox.type: shai`. Codex's artifact/runtime paths
retain their defaults; evolve intentionally overrides only `worktree_path`.
**Current upstream limitation:** Shai grants workspace-wide writes, and c2ops
disables Codex's native sandbox. A scoped cwd is not yet a write-isolation boundary.
See [the sandbox bug report](guides/BUG_REPORT_SCOPED_CODEX_SANDBOX.md).
Running sandboxed jobs requires a working Shai/Docker environment.

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
  type:
    type: string
    default_value: evolve
inputs:
  prompt: '${{ inputs.prompt }}'
  type: '${{ inputs.type }}'
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

Run the declared tests with a c2j binary containing native directory and runtime
fixture support (c2j commit `9e34b70` or later):

```bash
c2j test run --directory recipe-tests --case-timeout 5m --out-dir .c2j/test-results
```

Model replies and human answers are declared fixtures. c2j owns isolated JobDB,
cell repositories, workers, child submission, reviews, snapshots, and cleanup.
Verification commands, schema gates, dependency waits, and merges execute normally.
The deterministic cases explicitly run verification on the host. There is no
separate test server, generated suite, Python driver, or JobDB module pin here.
External gate ops still require their normal execution dependencies, including
Go for the current c2ops `rule_gate`; this is not test orchestration.

See [native testing](guides/NATIVE_RECIPE_TESTING.md) for authoring, live suites,
and [coverage ownership](guides/NATIVE_TEST_MIGRATION.md) for the migration map.

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
c2j test run --directory . --case-timeout 5m --out-dir .c2j/test-results
```

Live suites require explicit `--include-live`, Codex credentials, and the tools
required by their recipes. They are reported as excluded by default. For docs
examples only, use:

```bash
c2j test run --directory docs/examples/tests
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

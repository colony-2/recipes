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
2. Test statements and executable test-plan authoring, followed by independent review.
3. Human approval of the design and reviewed test plan.
4. Implementation, independent specification review, and independent quality review.
5. Fresh verification commands and retained evidence.
6. Human satisfaction, then squash merge into the cell's upstream branch.

Design classifies requested outcomes as `fits`, `partial`, or `outside` against
`.c2j/mandate.md` at the job's initial commit. Missing or uncertain mandates require
clarification. Partial requests retain local requirements and agreed external
handoffs; outside requests return routing advice with `merged: false`. Before
submission, A can host a separate session in B using node `workspace`, exchange
design feedback, and return to A. B's commit and session are retained while
experimental code is discarded with `const: true`. Human approval displays the
ownership split and external briefs. Planning/review phases cannot submit jobs.

These defaults require workspace-capable c2j compilers **and workers**; older
versions can ignore the workspace declaration. The consultation also checks for
an active workspace scope. The installed v0.0.53 predates this requirement.

Feedback continues the same implementation Codex session. Reviewers use fresh
sessions. Requirement changes return to design and require renewed plan approval.
Rejected planning results also return to the design/test-plan cycle, preserving
prior artifacts and feedback. Incomplete implementation requests feedback; invalid
artifacts and missing continuation sessions fail without merging. Automatic c2j
checkpoints preserve edits; only final acceptance publishes them.

Implementation can also start or continue a cell-B conversation when it discovers
a missing feature or dependency bug. It retains its coding session, local edits,
and dependency history. Advice can lead directly back to implementation; a new
or changed external handoff returns through design and test-plan approval before
submission. Design and implementation share pinned conversation threads, including
across human feedback rounds. Each thread keeps its latest reply and session object;
the coordinator passes that map between phases. Conversation history lives in the
session objects and c2j execution story, without transcript artifacts or history merging.
See [remaining custom logic](guides/BUILD_EVOLVE_REMAINING_LOGIC.md) for the next review.

After design/test-plan approval, implementation can request agreed external work with asynchronous
`c2j submit ... --cell <owner> --build` (or `--evolve`). The shared agent captures
the submitting op's `jobs.job_ids`, waits for every child using
`recipe.await_result_soft`, and resumes the same Codex session with child results
and namespaced artifacts. It deduplicates by job ID and retains results across
dependency rounds. A successful child cannot approve the parent's earlier result:
Codex must incorporate the dependency before reviews and verification continue.
Failed, cancelled, or explicitly unmerged children also resume the requesting
session with failure details, partial outputs, and available artifacts. The
session diagnoses the issue and can submit corrected prerequisite work or use
another valid approach within scope. Only unresolved blockers or decisions
requiring input go to human feedback. The phase must produce a fresh result
explaining the resolution before it can advance. The workflow does not blindly
retry submissions or cancel children automatically.
Cancelled parents may leave children running; operators must cancel those separately.

Cross-cell submission requires a JobDB service, available workers, and `c2j`
installed in the op sandbox with `C2J_JOBDB` configured for that service and tenant.
Embedded execution is suitable for local authoring without subprocess children.
The inherited broker environment must reach Codex subprocesses. Use c2j containing
`0a48289` (child snapshot isolation), which also includes the earlier broker and
workspace replay fixes. The full lifecycle is verified against clean commit
`0a482892458ebf5c319b0700ad5b7fabd5c97ed2`. The
[broker](guides/BUG_REPORT_CHILD_BROKER_COMPILED_INCLUDES.md),
[replay](guides/BUG_REPORT_WORKSPACE_DIALOGUE_CHILD_WAIT_REPLAY.md), and
[snapshot collision](guides/BUG_REPORT_CHILD_SNAPSHOT_COLLISION_AFTER_CONSULTATION.md)
reports retain historical reproductions. Child completion
does not refresh the parent's repository snapshot: the resumed agent must consume
the correct dependency version within its approved scope. An upstream advancement
still requires a fresh verified candidate before merge.

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

Run `./recipe-tests/run-defaults.sh` for comprehensive default-recipe tests.
Set `C2J_BINARY=/absolute/path/to/c2j` to test a workspace-capable binary without
replacing the installed CLI. `C2OPS_REPOSITORY=/path/to/c2ops` uses committed local
c2ops source for deterministic selector resolution without GitHub requests.
It requires c2j, git, Python, uv/PyYAML, and Go/access to the c2ops selector for
real gate checks. Codex and human replies are mocked; tests execute test-plan
contracts, verification commands, schema gates and git merges
against disposable repositories. c2j passthrough runtimes use temporary databases,
with scratch files under a per-run `TMPDIR`; tests never submit to the home
embedded database. Rendered sandbox configuration is covered, but a live Codex
or Shai container run is not part of this deterministic suite.
The suite also starts a separate temporary in-memory JobDB service and independent
c2j workers to test brokered cross-cell submission, durable waits, worker replacement,
session resumption, and dependency artifacts. The test server binds only to loopback
and exits with the suite; it uses no persistent database. Its JobDB version is
pinned to `6da2fab0502e`, matching c2j `f82bdd2`; use a compatible CLI when
running the multi-worker tests.
`verify-implementation-consultations.py` runs actual implementation/foreign-cell
loops with deterministic model turns, covering late bug discovery, advice, evolve
scope, multiple cells, design-thread reuse, human feedback, dependency history,
invalid replies/sessions/checkpoints, unavailable cells, mandate failures, and
bounded discussions. Local edits are made before consultation and checked after
resumption; B experiments and moving upstream refs test snapshot isolation.
The broker/include and workspace/handoff replay regressions run independently.
`verify-development-lifecycle.py` runs the complete defaults in both cells through
committed `.c2j/recipes/` specializations and named `--build`/`--evolve` submission.
A discovers missing dependency behavior during implementation, consults B, repeats
design/test-plan approval, and submits B. The test replaces A's worker while it
waits, runs B through real verification and squash merge, then requires A to resume
through its own verification and squash merge. It checks candidate/session preservation,
no premature parent acceptance, and exactly one child submission and merge per cell.
Only model/human decisions are scripted; verification runs on the host without Shai.
Both full lifecycle cases guard the resolved child snapshot collision and verify
that `artifact_refs` exports the verification report and command logs. The parent
receives identical child-owned artifact references after worker replacement;
evidence is available even though the child's last operation was its merge.
The runner attempts every suite and exits nonzero if any fails; neither regression
has an expected-failure exemption.

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

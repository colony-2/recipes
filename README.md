# C2 recipes

This repository maintains shared development recipes, authoring guides, and native
c2j tests. [PURPOSE.md](PURPOSE.md) describes its responsibilities. A cell covers
its entire repository; a task directory does not define a smaller cell.

Cell configuration lives in `.c2/config.yaml` and local recipe overrides in
`.c2/recipes/`. Move existing configuration and overrides from `.c2j/` when
upgrading to the current c2j main.

## Build

[`build.yaml`](build.yaml) is the development entrypoint. It uses root PURPOSE.md
when present and infers responsibilities from the repository otherwise. It does
not initialize a mandate. The evolve entrypoint and workflow-editing mode have
been removed.

At entry, [Jev classification](recipes/build/classify.yaml) reads the root purpose,
`ARCHITECTURE.md`, and the first available README. It evaluates the scope, complexity,
uncertainty, and risk of **this cell's work**, including whether its role is simply
delegating bounded requests to existing children. Each child classifies its own work.
The operation explicitly references the `jev_api_key` secret. The published Jev
manifest marks `api_key` with `x-secret: true`, allowing c2j to pass that reference.

Jev's `noul` value is the probability that `is_heavy` is true. Only a valid value
between 0 and 0.10 selects light (at least 90% probability of light work). Uncertainty,
invalid answers, unavailable Jev, or unusable/truncated repository context select
heavy. Missing PURPOSE.md is acceptable when README supplies context; neither
document is created just to classify a request. Each document is capped at 64 KiB.
The public outputs include `process` and `classification` to explain the decision.

The [light workflow](recipes/light/develop.yaml) runs:

1. Implement and test using existing patterns, without separate design, test-statement,
   or plan-approval phases. Existing test expectations still apply.
2. Consult serving cells inline, sequentially, and immediately launch agreed child
   builds. There is no human plan-approval gate. Child builds can run concurrently;
   the parent waits for every launched child before completing.
3. Inspect the actual repository diff. Only no-change jobs with successful children
   may finish as `delegated` without local review. Without children, run verification
   and present the evidence-backed no-change rationale for human acceptance. Acceptance
   finishes as `unchanged` without squash or merge.
4. For local changes, rebase, run repository verification, and present `synopsis.md`
   with the outcome, exact file inventory, verification evidence, and proposed commit
   message. Failure returns to implementation. Human feedback repeats implementation
   and verification; acceptance without feedback permits squash and merge.

Light verification runs `bash ./build.sh` when present, followed by any additional
repository check command supplied by the agent. Missing checks are reported as skipped
and allow normal synopsis review and merge. The light synopsis uses
the implementation session's explanation and the shared Git inventory; it does not
start an independent file-accounting session. If complexity emerges, the agent can
escalate to heavy after its children finish, retaining its session, candidate,
documents, and child outcomes in `light-handoff.json`.

The existing heavy [development workflow](recipes/develop/develop.yaml) runs:

1. Design and test statements, with serving-cell consultations where needed.
2. Independent assessment through the consultation kernel, then human plan review.
3. Implementation and approved prerequisite jobs, continuing independent work
   before waiting for named dependencies.
4. Rebase onto the current target branch, independent inspection, and executable verification.
5. A fresh Codex session accounts for every changed file and proposes the commit message;
   inappropriate changes return to implementation.
6. Human outcome acceptance, then separate squash and fast-forward merge operations.

Heavy no-change outcomes also require human acceptance. `merge-review.md` explains
why the request is satisfied without repository changes, including any child
outcomes. Acceptance finishes as `unchanged` without creating an empty commit.

Design, test statements, implementation summaries, reviews, and feedback travel
as artifacts. Questions are focused fields alongside documents. Uploaded edits
or guidance require revision and another review, including when accompanied by
an approval selection. Agreement with an expert's adverse findings does not pass
an assessment: the consultant must explicitly report `assessment: pass`.

Clarification (`ask_user`) requires focused questions, without requiring artifacts.
Optional documents are included when their references resolve; missing or ambiguous
references never delay clarification. Answers resume the requesting phase and do
not approve work. Formal reviews still require their expected artifacts.

Agent file references are resolved against published artifacts with `path_match`.
For deliverable responses, correctable errors resume the same session with preserved documents;
after two automatic corrections, the workflow asks for human direction.
Correction never substitutes for the normal design or outcome approval.

Verification runs an existing `build.sh` in `target_directory`, retaining its output
in `build.log` and its status in `verification.md`. Failed checks return to implementation.
An absent script is reported as skipped and permits normal review and merge; agents
do not need to create `build.sh` to satisfy the workflow. Projects can
specialize this include to use their own verification op. Verification is read
only with respect to the managed Git candidate. Build uses the native `rebase`,
`squash`, and `merge` ops (c2j v0.0.104 or later). Rebase happens before inspection,
verification, and file accounting. Squash happens after human acceptance and preserves the reviewed
tree. Merge publishes that prepared commit without rewriting it; upstream advancement
after review stops publication if it prevents a fast-forward.

The [file accounting include](recipes/develop/merge-review.yaml) and shared
[Git inventory](recipes/kernel/git-candidate.yaml) declare pinned
Nix Python through `execution_needs.packages` on their inventory and Markdown-rendering
commands. c2j prepares Python and adds it to each command's PATH; host Python is
not required for these steps. Its independent, read-only Codex session
explains every added, changed, and deleted file against the approved scope, including
files outside `target_directory`. Renames appear as deletion/addition pairs. The recipe
checks complete inventory coverage and attaches `merge-review.md`, `merge-candidate.json`,
and `merge-candidate.diff` to the existing outcome review. A `revise` verdict returns
the findings to the original build session and repeats rebase, inspection, verification,
and accounting. Execution errors propagate normally.

The document shows the proposed squash subject and review message. The recipe appends
`https://jobs.colony2.com/<tenant>/jobs/<jobid>` using c2j's current-job environment,
so the reviewed message and published commit link to the actual originating job.

```sh
c2j submit --recipe-file ./build.yaml \
  --inputs-json '{"prompt":"Add retry handling"}' --run --embed
```

`target_directory` defaults to `.` and scopes the task; agents still operate from
the repository root. `session` accepts a complete Codex checkpoint and `documents`
accepts native artifact references. Resume only compatible build sessions;
consultation handoffs pass agreed documents into a fresh execution session. The
deprecated `type` input is accepted and ignored because c2j v0.0.82 still injects
it; it selects no mode.

## Reusable kernel and coordination

The [kernel guide](recipes/kernel/README.md) documents consultation and its return
contract. Build and consultation share `agent-turn.yaml` for fresh/resumed calls,
Codex-enforced schemas, and read-only or mutating execution. Cell instructions
are injected only on fresh sessions. Prerequisite builds start fresh sessions so
consultant restrictions cannot carry into implementation. Consultation participant
setup is delivered once when entering from an existing checkpoint. Subsequent turns
carry the next message and relevant artifacts.

The consultant decides agreement. After four consultant responses, or an explicit
deconfliction request, consultation runs independent synthesis and a human review.
Direction opens another bounded round; it does not establish agreement itself.

[Heavy build coordination](recipes/develop/coordinate.yaml) includes the shared consultation
recipe inline for batches of up to 40 new, distinct serving consultations. They run
sequentially, carrying the requester checkpoint forward; human feedback pauses the
parent build. Larger batches launch child consultation jobs before waiting, allowing
local work to continue. The mode is fixed for the batch; existing threads, duplicate
keys, and same-candidate experts do not count toward the threshold. Experts remain
inline. Adjust `vars.inline_consultation_limit` in the coordinator to tune the threshold.
Stable keys prevent duplicate requests and submissions. Changed scope needs a new key and renewed plan approval.

[Light coordination](recipes/light/coordinate.yaml) uses the same consultation
kernel inline for every request. Stable keys still prevent duplicate submission;
reusing a key with a different request requires correction. A completed child may
report `delegated` or `unchanged` without a merge; both build paths accept those
successful dispositions as dependency completion.
`build_recipe` selects child builds in both paths. `consultation_recipe` selects
the heavy path's consultation jobs. Explicit non-default selectors always use child
jobs, preserving project customization: includes resolve before runtime inputs are
available. The default inline path includes the kernel shipped with the parent recipe;
the child path resolves the configured selector. Light always includes the shared
kernel inline.

On the heavy path, only agreed prerequisite keys explicitly listed in the approved
proposal can be submitted. Each child receives the final agreement documents and
an explicit execution request in a fresh session. The consultation transcript is
bound as `consultation/conversation.json`, leaving the next consultation's own
transcript filename available. Waiting preserves the caller's
newer checkpoint, records failures, and exposes summaries and evidence through
`context.json` and the inbox. Child documents are namespaced by request key;
their immutable stored identities remain unchanged. A failed child does not
silently pass a dependency gate or get resubmitted.

Design review validates prerequisite keys before advancing to test-plan. Invalid keys
are corrected in the design phase with the latest session and documents retained.
Keys identify this build's agreed serving-cell requests; the parent's request identifier
is not a local prerequisite. Builds without external prerequisites return `keys: []`.

Root identity comes from `root_cell`/`root_ref`, falling back to `c2j self --json`.
Creation eligibility always consults that root about project fit, existing owners,
excluded alternatives, and technology tradeoffs. The shared [create recipe](create.yaml)
starts a fresh session with the agreed creation brief and presents one consolidated
proposal review.
After approval, each new workspace starts with `initial: empty`, copies the
approved `PURPOSE.md`, and publishes through `squashrebasemerge`. Gitvend creates
an authorized missing repository during that ordinary push. The recipe then
registers the published cells in the root's existing catalog and merges that
root change separately.
The created cell then needs its own feature consultation before a build is submitted.

`consultation_recipe` defaults to the shared consultation selector on `main`;
`create_recipe` defaults to the shared `create.yaml` selector on `main`, and
`build_recipe` defaults to `build`. Override selectors for a local specialization
or when testing an unpublished revision. Cross-cell execution requires the native
shared job service and workers. Workspace snapshots preserve the unmerged caller
candidate; recipes do not manipulate Git packs or implement refresh workarounds.

Creation requires c2j's [empty-workspace support](guides/GUIDE-Empty-Workspaces.md).
Invoke it in the project root, or supply `root_cell` and `root_ref`. Repository
destinations and credentials come from project configuration and the reviewed
proposal. No root recipe boilerplate or separate provisioning service is needed.
See [creation behavior and failure handling](recipes/create/README.md).

## Tests

Run the current deterministic build and consultation suites:

```sh
c2j test run --directory recipe-tests --case-timeout 10m --out-dir .c2/test-results
```

These suites mock model responses and declare human answers while running native
Git, artifacts, checkpoints, reviews, child jobs, verification, and merges. The
current kernel uses c2ops' `published` Nix packages, including Codex's
`instructions` and `output.schema` contracts.
Install the latest c2j release with `npm install --global @colony2/c2j@latest`
and provide the op's declared execution tools,
including Nix. No live model credentials or external repository provisioning are
needed. See [routing and light workflow statements](recipe-tests/build-light-statements.md),
[build test statements](recipe-tests/build-kernel-statements.md),
[consultation statements](recipe-tests/consultation-kernel-statements.md),
[consultation scheduling statements](recipe-tests/consultation-scheduling-statements.md), and
[coverage ownership](guides/NATIVE_TEST_MIGRATION.md).

[Recipe CI](.github/workflows/recipes.yml) runs on pushes to `main` and pull
requests using the latest stable c2j Linux release, Nix, and the public `colony2`
Cachix cache. It discovers deterministic suites across the entire repository,
including the examples and superpowers recipes. Live suites remain excluded.
Each run records the selected c2j version and uploads test reports and logs as
`recipe-test-results`, including when tests fail. See the
[CI test statements](recipe-tests/ci-statements.md).

## Other recipes and authoring

- `recipes/new-ticket/` and `recipes/jobs/` contain standalone workflow examples.
- `recipes/superpowers/` contains a separate recipe family and tests.
- `recipes/smoke/` contains opt-in live execution checks.
- `docs/examples/` contains documentation examples and validation fixtures.
- `guides/` contains operation contracts, authoring guidance, and historical designs.

Use `c2j self` to check the target cell and
`c2j submit --recipe-file ... --run --embed` for local iteration. There is no
separate registry update step. Read the [authoring guide](guides/RECIPE_AUTHORING_GUIDE.md),
[operation catalog](guides/ops/README.md), and [scope rules](guides/NODE_SCOPE_SPEC.md).
Use real ops where available, explicit outputs across include boundaries, and
artifacts for substantial context. Live suites require `--include-live`.

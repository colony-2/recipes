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

The shared [development workflow](recipes/develop/develop.yaml) runs:

1. Design and test statements, with serving-cell consultations where needed.
2. Independent assessment through the consultation kernel, then human plan review.
3. Implementation and approved prerequisite jobs, continuing independent work
   before waiting for named dependencies.
4. Independent inspection of the actual candidate and executable verification.
5. Human outcome acceptance, then squash merge of that candidate.

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

Verification runs `bash ./build.sh` in `target_directory`, retaining `build.log`
and `verification.md`. Failed or missing verification returns to implementation;
a missing hook is reported as skipped and cannot authorize merge. Projects can
specialize this include to use their own verification op. Verification is read
only with respect to the managed Git candidate. Merge uses native
`squashrebasemerge` with `rebase: false`; upstream advancement stops integration.

```sh
c2j submit --recipe-file ./build.yaml \
  --inputs-json '{"prompt":"Add retry handling"}' --run --embed
```

`target_directory` defaults to `.` and scopes the task; agents still operate from
the repository root. `session` accepts a complete Codex checkpoint and `documents`
accepts native artifact references. This lets a serving build start from its
consultant's session and agreed specification. The deprecated `type` input is
accepted and ignored because c2j v0.0.82 still injects it; it selects no mode.

## Reusable kernel and coordination

The [kernel guide](recipes/kernel/README.md) documents consultation and its return
contract. Build and consultation share `agent-turn.yaml` for fresh/resumed calls,
Codex-enforced schemas, and read-only or mutating execution. Cell instructions
are injected only on fresh sessions. A build entered from a consultant checkpoint
establishes its workflow rules in the first prompt without repeating cell context. Consultation participant setup is delivered
once when entering from an existing checkpoint. Subsequent turns carry the next
message and relevant artifacts.

The consultant decides agreement. After four consultant responses, or an explicit
deconfliction request, consultation runs independent synthesis and a human review.
Direction opens another bounded round; it does not establish agreement itself.

[Build coordination](recipes/develop/coordinate.yaml) launches foreign consultations
as native child jobs. Multiple requests can be launched before waiting; the build
can continue local work while another thread awaits human feedback. Same-candidate
expert consultation is included locally. Stable keys prevent duplicate requests
and submissions. Changed scope needs a new key and renewed plan approval.

Only agreed prerequisite keys explicitly listed in the approved proposal can be submitted. Each child receives the
serving consultant's checkpoint and final documents. Its inherited transcript is
bound as `consultation/conversation.json`, leaving the next consultation's own
transcript filename available. Waiting preserves the caller's
newer checkpoint, records failures, and exposes summaries and evidence through
`context.json` and the inbox. Child documents are namespaced by request key;
their immutable stored identities remain unchanged. A failed child does not
silently pass a dependency gate or get resubmitted.

Root identity comes from `root_cell`/`root_ref`, falling back to `c2j self --json`.
Creation eligibility always consults that root about project fit, existing owners,
excluded alternatives, and technology tradeoffs. The shared [create recipe](create.yaml)
resumes root's consultant session and presents one consolidated proposal review.
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
c2j test run --directory recipe-tests --case-timeout 3m --out-dir .c2/test-results
```

These suites mock model responses and declare human answers while running native
Git, artifacts, checkpoints, reviews, child jobs, verification, and merges. The
current kernel pins a c2ops revision supporting `instructions` and `output.schema`.
Use the c2j revision in [native testing](guides/NATIVE_RECIPE_TESTING.md) and the op's declared execution tools,
including Nix. No live model credentials or external repository provisioning are
needed. See [build test statements](recipe-tests/build-kernel-statements.md),
[consultation statements](recipe-tests/consultation-kernel-statements.md), and
[coverage ownership](guides/NATIVE_TEST_MIGRATION.md).

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

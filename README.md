# C2 recipes

This repository maintains the adaptive software-development recipe, root-owned
cell creation, authoring guides, and native c2j tests. [PURPOSE.md](PURPOSE.md)
describes this cell's responsibilities.

## Build

[`build.yaml`](build.yaml) runs [`recipes/adaptive/`](recipes/adaptive/README.md).
It classifies whether design is needed, writes formal test statements, implements
and coordinates prerequisite work, verifies the candidate, and presents an outcome
review before publication. Agent feedback returns to the appropriate working phase.
See [the process description and diagrams](ADAPTIVE_BUILD_PROCESS.md).

```sh
c2j submit --recipe-file ./build.yaml \
  --inputs-json '{"title":"Retry handling","prompt":"Add retry handling"}' --run --embed
```

`prompt` is required. `title` is optional; `target_directory` defaults to `.`.
The cell encompasses the whole repository. Other inputs, including verification
requirements, child recipe selectors, documents and checkpoints, are declared in
the entrypoint's schema v2 contract.

Prompts live in `recipes/adaptive/prompts.yaml`, included through an empty sequence
that creates no worker task. Specific typed values carry orchestration state;
files carry evidence, feedback, command diagnostics, and review documents.
Standing context is supplied when a session starts. Agents can use `c2j self` to
inspect their execution context and capabilities, and `c2j job log`, `fields`,
`artifacts`, and `snapshot` to retrieve selected work from this job or its direct children.

Serving consultations resolve external scope. The working agent generates a focused
`handoff.md` and selects supporting files for an explicit execution owner. The parent
follows the exact job and can submit a corrected fresh attempt after failure, carrying
selected artifacts or a reviewed patch when useful. Sessions and execution history are
not inherited. See [handoffs and recovery](guides/ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md).

Repository hooks live under `.c2/recipes/hooks/build/`. See the
[hook guide](guides/BUILD_HOOKS_USER_GUIDE.md) and
[examples](examples/build-hooks/README.md). Package requests use the explicit
reference/probe contract and the configured package approval policy; accepted
changes are validated before adoption.

## Cell creation

[`create.yaml`](create.yaml) runs in the cell named `root`. Human review covers
repository identities, exact initial purposes, and exact root configuration.
After approval it registers cells with `c2j cell create`, starts destination-owned
initialization jobs, and publishes the approved root catalog after they succeed.
Creation alone does not complete the original feature request.
See [creation behavior and failure handling](recipes/create/README.md).

The helpers still needed by creation remain in [`recipes/kernel/`](recipes/kernel/README.md).
The old heavy/light build, ticket/job workflows, superpowers family, and their
exclusive helpers and tests have been removed. Adaptive is the sole build path.

## Tests

Use the c2j release pinned in [`.c2j-version`](.c2j-version), Nix with flakes,
and the public `colony2` Cachix cache. [CI](.github/workflows/recipes.yml) installs
these dependencies and records the exact runtime version.

```sh
c2j test run --directory . --case-timeout 10m --out-dir .c2/test-results
```

Deterministic suites mock model responses and declare human answers while exercising
native artifacts, Git, reviews, child jobs and publication. Adaptive coverage lives
in `recipe-tests/adaptive/`; retained creation and shared-helper coverage is in
`recipe-tests/`. Documentation examples are also discovered. Live model/skill checks
are opt-in with `--include-live` and require configured authentication.

See [retirement expectations](recipe-tests/retirement-statements.md),
[coverage ownership](guides/NATIVE_TEST_MIGRATION.md), and
[the cleanup assessment](guides/ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md).

## Authoring

Read the [authoring guide](guides/RECIPE_AUTHORING_GUIDE.md),
[operation catalog](guides/ops/README.md), and [scope rules](guides/NODE_SCOPE_SPEC.md).
Use `c2j self` to confirm the cell, then submit local recipe YAML directly;
there is no separate recipe registry/update step.

`docs/examples/` contains small executable examples. `recipes/smoke/` contains
opt-in execution checks. Historical proposals and audits in `guides/` describe
past revisions and are not alternate active workflow contracts.

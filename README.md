# C2 recipes

This repository maintains the adaptive software-development recipe, root-owned
cell creation, authoring guides, and native c2j tests. [PURPOSE.md](PURPOSE.md)
describes this cell's responsibilities.

## Build

[`build.yaml`](build.yaml) runs [adaptive3](recipes/adaptive3/README.md).
It frames the request as a feature, bug, explanation, or oversight assignment.
Five stages share one Execute → full Validate → Review cycle: Direction,
Preparation, Implementation, Outcome acceptance, and Integration/publication.
Direction and Outcome have human review. Questions stay in Review; corrections
repeat the destination stage's complete cycle. An accepted explanation can finish
at Direction. See [the process description](ADAPTIVE_BUILD_PROCESS.md).

```sh
c2j submit --recipe-file ./build.yaml \
  --inputs-json '{"title":"Retry handling","prompt":"Add retry handling"}' --run --embed
```

`prompt` is required. Optional inputs are `title`, `target_directory`, `documents`,
`require_verification`, `max_iterations` and `resume_from`. `type: build` is also
accepted from CLI callers. The cell encompasses the whole repository. The
[rollout notes](guides/adaptive3/ROLLOUT.md) explain the changed public contract.

Prompts live in `recipes/adaptive3/prompts/`, using empty-sequence includes.
Standing context is supplied when a session starts. Agents can use `c2j self`
and the job inspection commands to retrieve selected earlier work. Native outputs
carry workflow state; files carry actual work, diagnostics and human review content.

Consultation runs inline in the receiving cell's workspace. The receiver writes
any delivery assignment, which can start a child job. A caught failure enters
resolution inside the parent job. The [workflow guide](recipes/adaptive3/README.md)
and [runtime requirements](guides/adaptive3/RUNTIME_REQUIREMENTS.md) distinguish
implemented recovery from remaining runtime limitations.

Use the [documentation map](guides/README.md) and
[general improvement guidance](guides/RECIPE_IMPROVEMENT_GUIDE.md) for recipe work.
For analysis of observed job behavior, the repository skill
[audit-recipe-jobs](.agents/skills/audit-recipe-jobs/SKILL.md) works within ordinary
build phases and existing hooks. Put the JobDB, bounded cohort, and constraints
in the normal build request. The [backgrounder index](guides/self-improvement/README.md)
explains invocation, evidence, planning, tests, and later observation.

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
exclusive helpers and tests have been removed. Adaptive3 is the default build path. Adaptive2 remains explicitly available at
`recipes/adaptive2/build.yaml`, with its shared `recipes/adaptive/` helpers and
separate regression tests.

## Tests

Use the c2j runtime pinned in [`.c2j-version`](.c2j-version), Nix with flakes,
and the public `colony2` Cachix cache. [CI](.github/workflows/recipes.yml) installs
these dependencies and records the exact runtime version. Install the selected runtime
with `bash scripts/install-c2j.sh /tmp/recipes-c2j` and put `/tmp/recipes-c2j/bin`
first on `PATH`; see [native testing](guides/NATIVE_RECIPE_TESTING.md).

```sh
c2j test run --directory . --case-timeout 10m --out-dir .c2/test-results
```

Deterministic suites mock model responses and declare human answers while exercising
native artifacts, Git, reviews, child jobs and publication. Public build coverage
lives in `recipe-tests/adaptive3/`, including repository-improvement hook coverage.
Retained adaptive2 tests use its explicit entrypoint; older adaptive and shared-helper
regressions live in `recipe-tests/adaptive/`. Creation coverage is in
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

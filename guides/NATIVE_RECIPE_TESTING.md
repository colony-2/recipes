# Native recipe testing

Use c2j with native directory/runtime test support (`9e34b70` or later). Until a
release includes it, build that c2j revision and invoke its binary directly.

```sh
c2j test validate --directory .
c2j test run --directory . --case-timeout 5m --out-dir .c2j/test-results
c2j test run --file recipe-tests/build.scenario.md --case happy
```

Discovery recursively finds `*.test.yaml`, `*.test.yml`, `*.test.json`, and
`*.scenario.md`. Each suite declares `recipe`, relative to that suite. Tests
are text declarations; adding one does not require editing a manifest or runner.
The result directory includes aggregate and per-suite/per-case reports. Any
required failure returns nonzero; the runner attempts the remaining suites.

For example:

```yaml
recipe: ../recipes/develop/verify.yaml
cases:
- id: failed-hook
  type: integration_case
  inputs: {timeout: 1s}
  runtime:
    command_sandbox: none
    cells:
      root:
        files:
          build.sh: "echo verification failed; exit 7\n"
  mocks:
    ops:
    - repeat: true
      match: {op: command_execution}
      behavior: {mode: passthrough}
  assertions:
  - {type: output_equals, path: ok, value: false}
  - {type: output_equals, path: result.status, value: failed}
```

Use ordinary cases with explicit mocks for branch coverage. Add `runtime: {}`
when the test needs actual Git snapshots, artifact/object storage, input/review
submission, child jobs, waiting, or merges. c2j creates disposable JobDB and cell
repositories and runs normal workers, including children. It never uses the
home embedded database for these cases.

Runtime mocks can match a node, selector, and cell. They are consumed in order;
`repeat: true` is useful for a real schema gate or command used repeatedly.
Mock only external decisions. Declare `behavior.artifacts`, `effects.worktree`,
`effects.objects`, and `effects.children` to produce real persisted data and
broker-submitted children. Do not invent object storage keys in runtime cases.
Declare `runtime.responses` with input node paths, fields, and attachment-file
paths to answer real reviews. Fixture paths resolve relative to the suite.

`command_sandbox: none` is an explicit test environment choice for trusted
commands. It does not change production recipes. Omit it to use their sandbox.
External ops still need their declared dependencies (the current rule_gate uses
Go). There is no separate Python/Go test server or client to install.

Use CEL assertions over `outputs`, `calls`, `reviews`, `artifacts`, and
`repositories` to check routing and actual upstream file changes. Use
`expect_error` for a specific expected execution failure; unrelated errors and
timeouts still fail. See the c2j native-testing guide for the complete schema.

## Live suites

Live suites declare `live: true` and are reported as `excluded_live` by default.
They require the recipe's normal credentials, skill sources, and execution tools:

```sh
c2j test run --directory . --include-live --case-timeout 45m --out-dir .c2j/live-results
```

Only run this when live model work is intended. A missing credential or tool
fails the selected case; exclusion is never reported as a passing test.

## Ownership

Test recipe decisions, documents, prompts, sessions, dependencies, and merge
policy here. Put compiler, CLI, lease, worker-replay, snapshot, object-storage,
and input API regressions in c2j. Put Codex adapter implementation tests in c2ops.
The [migration map](NATIVE_TEST_MIGRATION.md) records the split and retired tests.

Some mock cases select `options.validation_mode: path_only`: a fresh-session
case must not validate an unselected resume branch against a null checkpoint.
The default `all` mode remains useful for whole-graph checks. Runtime cases are
structurally validated; their actual path and assertions execute under `run`.

The build/evolve mock routing suites and agent schema suite use
`validation_mode: structure_only`. Their templates consume mocked artifact data
and runtime histories that the validation-only compiler replaces with placeholders.
Preflight checks syntax, case declarations and dependencies, and reports that
execution validation is deferred. `run` executes these data-dependent paths and
all assertions; a structural preflight alone is not a passing behavior test.

Use `runtime.observe_files` to select cell-relative files to record before each
op. Assert on `calls[].worktree` for retained candidates or absent foreign edits.
Compare `calls[].inputs.inputs.session` to the preceding model call's
`outputs.session` when exact checkpoint routing matters. A matching object type
alone does not prove that the intended checkpoint was used.

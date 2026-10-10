# c2j: recipe-test passthrough loses prepared Nix extension context

Resolved upstream in `b6f6a04a5086cac882b5eea6d6a22a9dfce35578`, with a macOS
fixture-path follow-up in `14e8ddf`. Verified on 2026-10-10 using a clean build
of main `b98e25fcba7fe00101d49db8455cf0d5ebc0a4cb`: the original `valid-initial`
reproducer passes with the real Nix-packaged gate. The upstream passthrough,
setup, recording/replay, scoped-tools, and timeout regression tests also pass.
All 35 recipe cases previously affected by this bug now pass with real gates.
The original report follows.

Observed on 2026-10-10 with c2j main
`82362f0ec1ad68b79ed2fb078ca9418e722de0cd`, built from a clean source snapshot.
c2ops main was `0ba79fa444f4227b5cc44b522e0df2b0e098823c`; its publication
workflow completed successfully. Platform: aarch64-linux.

## Reproduction

With Nix available for manifest resolution, run this repository's migrated test:

```sh
c2j test run --file recipe-tests/agent-gates.test.yaml --case valid-initial
```

The recipe correctly authors the gate as:

```yaml
op: nix:github:colony-2/c2ops/main#rule_gate
```

The test mocks Codex and passes the gate through to its real implementation.
It fails with:

```text
state 'schema' execution failed:
passthrough invoke failed for extension_execution:extension_execution:
error executing step: invoke a Nix extension directly with op:
nix:github:colony-2/c2ops/main#rule_gate so c2j can prepare it before execution
```

The same failure affects consultation schema tests and
`recipes/superpowers/tests/superpowers-rule-gate-schema-smoke.scenario.md`.

A smaller reproducer is an ordinary `recipe_case` targeting a sequence with one
Nix `rule_gate` node, an assert rule with `value: true`, and this mock:

```yaml
mocks:
  ops:
    - match: {op: extension_execution}
      behavior: {mode: passthrough}
```

## Expected behavior and likely cause

Native test passthrough should execute an authored Nix selector through the
normal preparation lifecycle and preserve its prepared manifest/environment.
It should not treat a correctly lowered selector as a manually authored
`extension_execution` call.

Source inspection at the c2j revision above:

- `pkg/recipetest/harness.go` invokes the passthrough chain directly using
  `chain[idx].Invoke(deps, ctx, inv.Input)` without attaching prepared extension
  context or performing the normal setup-recovery handshake.
- `pkg/worker/ops/taskworker.go` handles setup readiness and uses
  `extensions.WithPreparedOp` before invoking a real op.
- `pkg/ops/extensions/execution_op.go` rejects Nix selectors when that prepared
  context is absent, producing the message above.

This is separate from this test environment's blocked Nix/Cachix downloads.
Nix manifest resolution and fully mocked build execution succeeded. The
passthrough error occurs before package execution; enabling cache access alone
does not supply the missing invocation context.

## Requested regression coverage

Cover a directly authored Nix op under native fast-test passthrough: successful
execution, schema-invalid input, a schema-rejected result artifact, and setup
failure. Preserve real op validation; replacing the gate with a mocked success
would remove the behavior these recipe tests are intended to check.

c2j owns the fix. Recipes should continue using the public Nix coordinates and
existing native tests, without a local extension runner or Git-selector fallback.

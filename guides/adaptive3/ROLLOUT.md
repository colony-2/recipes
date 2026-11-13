# Adaptive3 is the default build

Root [`build.yaml`](../../build.yaml), version 4.0.0, now forwards to
[`adaptive3.yaml`](../../adaptive3.yaml). The direct adaptive3 entrypoint remains
available. This changes future submissions using the published recipe revision;
already submitted jobs retain their captured recipe.

## Public contract

Required input: `prompt`.

Optional inputs: `title`, `target_directory`, `documents`, `require_verification`,
`max_iterations`, and `resume_from`. The wrapper also accepts `type: build` from
CLI callers. Inputs are passed directly to adaptive3.

Outputs are `summary`, `work_kind`, `artifact_refs`, `reviews`, `merge`, and
`publication`. They are the adaptive3 outputs, without a second result format.

The old public fields for sessions, annotations, root selection and injected
child recipe selectors are no longer accepted by default build. Callers using
those fields must adopt the adaptive3 contract or explicitly select
[`recipes/adaptive2/build.yaml`](../../recipes/adaptive2/build.yaml). For a retained
adaptive2 workflow that also needs adaptive2 delivery children, explicitly set
its `build_recipe` to that adaptive2 selector; the name `build` now means adaptive3.

Adaptive3's own delivery children already select `adaptive3.yaml` explicitly.
Package probes select its dedicated probe recipe. Publish the corresponding
sources together before using those remote selectors.

## Coverage of the switch

The new [`default-build.test.yaml`](../../recipe-tests/adaptive3/default-build.test.yaml)
calls root `build.yaml` directly. All three cases passed:

- An explanation enters adaptive3 and completes after human acceptance.
- Feature work completes both human reviews and a native merge through adaptive3.
- Repository-improvement inputs and backgrounders reach the normal build; the
  local verification hook executes before completion.

The tests also assert the default never enters adaptive2 and that the supplied
title reaches the working agent. The existing 42 adaptive3 cases cover the
underlying activity and recovery behavior; their results are recorded in
[TEST_RESULTS.md](TEST_RESULTS.md).

Adaptive2 suites and fixtures now target its existing explicit entrypoint. Their
native paths and named-child fixture layouts were updated accordingly. Source
validation passed for all 228 retained adaptive2 cases. Focused native checks cover the
retained direction-cancellation path and named receiving-cell child submission.
Public default coverage is owned by adaptive3's suite.

Execution used the same preinstalled-tool test environment described in
[TEST_RESULTS.md](TEST_RESULTS.md). The named adaptive2 child check also needed
validator dependency declarations removed from disposable copies of shared
adaptive/adaptive2 helpers after this host's portable Nix rejected tool setup.
Production dependency declarations are unchanged. These tests do not resolve the
documented normal-worker Nix activation requirement.

## Follow-up work

The agreed [three todo items](TODO.md) remain open. This switch does not implement
model overrides, complete the incomplete-result correction audit, or add the new
qualitative/actual change reports. The [runtime requirements](RUNTIME_REQUIREMENTS.md)
also remain open. The preceding adaptive2 process is preserved in
[ADAPTIVE2_BUILD_PROCESS.md](../../ADAPTIVE2_BUILD_PROCESS.md).

# c2j value-artifact compatibility findings

Owner: c2j. Observed on main `393531b2f402f3b6007256c262e0ddefbc3bded1`,
which includes value-artifact commit `66cbded` and test follow-up `7bdeab7`.
Recipe baseline: `586e9ff`. These findings are separate from the older
[child hook snapshot blocker](BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md).

## Blocker: exported artifact maps change their JSON/CEL contract

`completeNodeScope` in `pkg/worker/compiler/execution_scope.go` binds any
`outputs.artifact_refs` map and replaces the ordinary output with a typed
`map[string]artifacts.Ref`. Two regressions result:

1. `artifactBindingAccumulator.bindings()` returns nil for an empty map.
   A declared `artifact_refs: {}` becomes JSON null. Local hook validation rejects
   it with `at '/artifact_refs': got null, want object`. Default absent hooks fail
   as well as repository hooks.
2. Nonempty typed maps (and empty typed maps) cannot be consumed by existing
   `jq` expressions. Review feedback merging fails with
   `jq: execution failed: ... invalid type: map[string]artifacts.Ref`.

Expected: retain `{}` for an explicitly empty artifact map and expose normalized
JSON-compatible values to recipe expressions while separately maintaining the
runtime's typed artifact export inventory. Value refs should still materialize
and be persisted at standalone job boundaries.

Reproduce with an unmodified binary from the revision above:

```bash
c2j test run --file recipe-tests/build-hooks.test.yaml --case missing-hooks
c2j test run --file recipe-tests/build-hooks.test.yaml --case configuration-values
c2j test run --file recipe-tests/result-repair.test.yaml --case exhaustion-cancel-preserves-work
c2j test run --file recipe-tests/result-repair.test.yaml --case human-attachments-are-retained-for-correction
```

The hook failure was reproduced before migrating the settings writer. The
unmodified runtime failed six of seven hook cases and four of five repair cases;
`automatic-preserves-session-and-documents` passed.

Suggested upstream regression coverage:

- Inline exports preserve an explicitly empty object through `expect_outputs`.
- Both empty and populated exported artifact maps can participate in `jq` merges.
- Typed native input outputs remain JSON-compatible after scope publication.
- Value sources exported from child jobs still become stored result attachments.

## Diagnostic runtime used for recipe validation

No c2j checkout files were changed. A temporary Go build overlay makes exactly
two adjustments:

```diff
 func (a *artifactBindingAccumulator) bindings() map[string]recipeartifacts.Ref {
-    if len(a.out) == 0 {
-        return nil
-    }
     return a.out
 }
```

In `completeNodeScope`, replace `output.Outputs["artifact_refs"] = refs` with a
JSON marshal/unmarshal into `map[string]any`, assign that plain map to the output,
and continue merging the original typed `refs` into `output.ArtifactRefs`.
This is diagnostic validation, not a shipped fix or a recommendation to remove
export binding. The source checkout stays unchanged; production compatibility
requires an upstream correction and revalidation without the overlay.

## Existing hook-source test also fails on current main

`build-hooks.test.yaml::prepare-new-hook` expects a verify hook created by prepare
to be available later in the same job. Current main reports verification skipped.
The same test fails against recipes baseline `586e9ff` with the diagnostic
artifact-map correction, so the value-artifact migration did not introduce it.
Current main includes hook-source changes in `393531b`; c2j should determine
whether this is a regression or an intentional contract change requiring a
separate hook design update. The assertion has not been weakened or skipped.

## Large review-field limitation

A synthetic review whose question text is 128 KiB plus an 80-character suffix
fails submitting the fixture response with:
`submit review: request_id does not match the pending input`.
At 512 KiB, the ordinary input-op output containing the fields instead exceeds
the 262,144-byte application payload limit. Neither case is a large review
*document*: 512 KiB correction documents persist and review successfully.

To reproduce the request-ID failure, temporarily change `1000` to `131072` in
`recipe-tests/fixtures/payload-documents.yaml`, including its Python comparison,
and run `recipe-tests/payload-documents.test.yaml` with the diagnostic runtime.
The failure is observed; its cause is not established here. Keep large evidence
in review documents rather than large form-field strings. This report does not
claim that value artifacts lift ordinary op-output limits.

## Validation record

The direct `value-artifact-smoke.test.yaml::two-megabyte-values-remain-literal`
case and the 512 KiB stored-transcript comparison pass on the unmodified runtime.
Five large-context build cases and the 512 KiB document comparison pass with the
diagnostic runtime. Across the original 269-case directory run, two targeted
fixture corrections, and eight new payload cases, **276 of 277 unique cases pass**
using the diagnostic correction where required. The remaining failure is
`build-hooks.test.yaml::prepare-new-hook`, reproduced against the unchanged
recipes. This is an aggregate of each case's latest result, not an uninterrupted
green directory run.

The fixture corrections remove the now-unused repair-writer command mock in
`execution-failure-after-repair-propagates` and expect c2j's earlier path-binding
rejection in `unsafe-artifact`. The failure-propagation and unsafe-path rejection
requirements remain intact. All 23 merge-recovery cases pass.

Full directory validation reports **277 valid cases, zero invalid**. The existing
`heavy-accepts-successful-unmerged-child` disabled case remains excluded and was
not rerun. Live-service scenarios remain excluded. `bash build.sh` and
`git diff --check` also pass.

The environment uses real Nix packages and the temporary Nix JSON adapter
already described in the earlier hook validation report. Agent/classifier
responses are mocked in integration suites; Git, artifact materialization,
review persistence, renderer execution, and child orchestration use the native
runtime. No live deployment or publication was performed.

Validation commands (use the diagnostic executable for the directory runtime run):

```bash
c2j test validate --directory recipe-tests --parallelism 4
c2j test run --directory recipe-tests --out-dir /tmp/values-regression \
  --parallelism 6 --case-timeout 5m
c2j test run --file recipe-tests/payload-transport.test.yaml
c2j test run --file recipe-tests/payload-documents.test.yaml
c2j test run --file recipe-tests/payload-consultation.test.yaml
c2j test run --file recipe-tests/value-artifact-smoke.test.yaml
c2j test run --file recipe-tests/consultation-kernel.test.yaml \
  --case execution-failure-after-repair-propagates
c2j test run --file recipe-tests/verification.test.yaml --case unsafe-artifact
```

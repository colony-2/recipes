# Remaining recipe test gaps

Evaluated after committing `8930386`, on 2026-11-06. This is an assessment, not
another implementation change. Scope: current adaptive recipes, their native
boundaries and fixtures, and the repository's CI configuration. Older kernel
suites were checked for coverage attribution, not exhaustively audited.

Follow-up: see the [closure plan](PLAN_RECIPE_TEST_GAP_CLOSURE.md) and
[implementation assessment](ASSESSMENT_RECIPE_TEST_GAP_CLOSURE.md) for fixes,
validation, and the remaining c2j-owned lifecycle fixture controls. Findings below
describe the audited revision, not the subsequent implementation.

The two production fixes are committed. The custom-consultation route remains
unchanged pending the user's investigation of c2j hook workspace support.

## Findings in priority order

| Priority | Finding | Evidence | Next change |
| --- | --- | --- | --- |
| P1 | Failed child diagnostics are read from the wrong part of the result. | Confirmed with an actual failed child and native result inspection. | Correct the shared failure collector and test actual failing children. |
| P1 | Evidence naming can silently overwrite a different file. | Three native probes lost distinct evidence from the returned inbox maps. | Make filename transformations collision-safe and test preservation of every source. |
| P2 | The package concurrency test passes without the concurrency guard. | Both existing guard tests passed after removing that guard in an isolated copy. | Isolate each rejection condition and add a valid adoption control. |
| P2 | Goal replacement and consultation resumption lack matching native coverage. | Goal replacement is mocked; saved-continuation suites exercise the old kernel. | Add lifecycle and adaptive continuation tests, including interrupted nested advice. |
| P2 | Permission and package validation cover only part of the production boundary. | Credential probes replace task bodies; hooks mostly have no configured grants; local packaged-op execution was unavailable. | Add deterministic authorized/denied hook cases and require an authored-package smoke result on the intended runtime. |

## 1. Failed child diagnostics: another mock/contract mismatch

The failed-attempt branch of
[`await-goal.yaml`](../recipes/adaptive/await-goal.yaml) uses
`recipe.await_result_soft` to inspect a terminal attempt. It then forwards only
`states.attempt.outputs.artifacts` to the error-directory helper.

A native probe submitted a child whose command printed a distinctive stderr
message and exited with code 7. The real inspection returned:

```yaml
status: failed
artifacts: {}
outputs:
  attrs:
    c2j_failure:
      attrs:
        command:
          diagnostics:
            _c2j/execution/fail.log: <stored artifact reference>
```

The reference exists, but the collector never examines that structured failure
output. Once a goal is explicitly failed and its terminal attempts are inspected,
the repair inbox can receive a generic failure summary without the actual log.
An open goal still waits for recovery; the probe does not imply that an attempt
failure should automatically fail its goal.

The `approved-proposal-reuses-goal-and-diagnostics` case in
[`package-repeat.test.yaml`](../recipe-tests/adaptive/package-repeat.test.yaml)
places a preparation diagnostic directly in the mocked top-level `artifacts`
map. Its assertion therefore passes without checking how a real failure is
represented. This is the same class of problem as the invented consultation
`outputs` collection.

Next: establish one shared collector for native failure envelopes, including
command/extension diagnostics and wrapped causes. Preserve the actual stored
references. Test a real failing command, an extension failure, and an early setup
failure; require their distinctive diagnostics to reach the repair inbox. If a
canonical diagnostic field is needed from c2j, specify that contract there rather
than fabricating it in recipe tests. Recipe collection is owned here; runtime
contract additions belong to c2j.

## 2. Artifact naming loses distinct sources

The new single inbox binding fixes duplicate expansion of returned copies. It
does not establish that earlier filename transformations preserve every source.
Native probes against the production helpers confirmed these cases:

| Inputs | Actual consumer result |
| --- | --- |
| `_c2j/execution/check.log` with runner output, plus `check.log` with different hook output | Both map to `verification/check.log`; only the hook output survives in the agent inbox. |
| Hook artifact `verification.md` containing detailed evidence | The generated verification summary replaces it in the agent inbox. |
| Error artifact `failure.md` containing original diagnostic detail | The generated failure summary replaces it in the error-directory map. |

The first two probes used a real, successful local verification hook and checked
that its status remained `passed`. This isolates filename loss from failed hook
execution. Raw hook references remain available in the producer/result; the loss
is in the files prepared for the consuming agent, not deletion from storage.

Affected code:
[`verify.yaml`](../recipes/adaptive/verify.yaml) and
[`error-documents.yaml`](../recipes/adaptive/error-documents.yaml).
The helpers use map addition and `from_entries`, which overwrite duplicate keys.
Current tests usually select one expected filename. They do not verify that all
distinct source identities/content remain available after renaming.

Next: make the mapping one-to-one. Separate runner captures, hook files, and
recipe-generated summaries into defined locations, or reject an ambiguous
mapping explicitly. Apply that rule consistently, rather than adding individual
exceptions for these three names. Tests should compare preserved source identities
and materialized contents, including a source whose name resembles a reserved or
already-prefixed path.

## 3. A negative test rejects for the wrong reason

[`package-adoption-guard.test.yaml`](../recipe-tests/adaptive/package-adoption-guard.test.yaml)
uses both `base: stale` and `validated: not-this-config` in its concurrency case.
The fixture catches any non-cancellation failure and reports `rejected: true`.

I removed only the parent-config concurrency check from an isolated copy of
`package-tools.yaml`. Both existing guard cases still passed. The command log
showed rejection by the remaining digest check:

```text
ValueError: Successful goal did not validate this config
```

This demonstrates a test weakness, not a currently missing production guard.
The production guard is present and was not edited by this audit.

Next: use a valid candidate digest when testing a stale parent, and a current
parent digest when testing invalid validation evidence. Preserve and assert the
specific rejection reason. Add a case in the same fixture where both digests are
valid and adoption succeeds, so unrelated Python/tool failures cannot satisfy all
negative assertions. Removing either guard should fail its corresponding test.

## 4. Recovery claims exceed the tested lifecycle

`successful-goal-replaces-failed-attempt` in
[`goal-monitoring.test.yaml`](../recipe-tests/adaptive/goal-monitoring.test.yaml)
returns a completed replacement result from a mock. It checks how the recipe
consumes that shape. It does not create a failed attempt, keep its goal open,
start a replacement in that goal, or resume the parent wait.

The new nested consultation cases test workspace/session routing within an
uninterrupted execution. They do not restart a worker while a parent conversation
is suspended for advice. Existing saved-continuation tests target
`recipes/kernel/consultation.yaml`, not the current adaptive implementation.
Returning `outcome: cancelled` from a model also differs from cancelling execution.

Next: add native same-goal replacement and terminal-failure cases with real
artifacts; add an adaptive transcript export/import round trip and an interrupted
nested-consultation recovery case. Assert no duplicate advice, child execution,
or human review. Keep mock tests for branch behavior, but label their scope
accurately. If the native fixture runner needs lifecycle controls, that reusable
support belongs in c2j rather than a new recipe-owned test engine.

## 5. Permissions and deployment-equivalent validation

The credential regressions are useful: they exercise the real credential helper
and submission broker. However,
[`permissions.yaml`](../recipe-tests/adaptive/permissions.yaml) extracts selected
production nodes and replaces their operation/input bodies with command probes.
It cannot establish that the complete packaged Codex operation, nested hook
source, forwarded secrets, and checkpoint/artifact setup work together.

Most hook fixtures run simple local commands or empty sequences without a
configured hook authority grant. They do not establish permitted and denied
secret access through actual hook/include boundaries. The custom-workspace
limitation found during the preceding work illustrates why composing individually
working capabilities still needs a boundary test.

CI already installs Nix and the colony2 cache and runs authored recipe suites;
this is not a claim that CI omits packaged operations. But
[the workflow](../.github/workflows/recipes.yml) selects npm `@colony2/c2j@latest`,
while recent local validation used a particular Git main build. Those are different
selection rules. This audit did not inspect the latest remote CI result or claim
that the versions currently differ.

Next: record the exact runtime identity alongside each result and test the intended
deployment version. Add small hook authority cases using synthetic secrets, with
positive and negative outcomes. Require a passing authored-package smoke test
before describing the whole production setup as verified. A deterministic fixture
model is sufficient; this does not require testing Codex's intelligence.

## Audit evidence and limits

The probes used c2j `eb636a5`, disposable native JobDB/Git fixtures, real operations,
and no live model calls or production writes. Unlike the prior broad local run,
these probes did not lower Nix selectors: their operations were native commands,
includes, and child-result inspection.

The following temporary reports contain the observed outputs:

- `/tmp/recipe-gap-audit/failed-child-results/summary.json`: actual failed child
  has an empty top-level artifact map and a stored log inside its failure envelope.
- `/tmp/recipe-gap-audit/evidence-results2/summary.json`: two preservation assertions
  fail after successful hook execution.
- `/tmp/recipe-gap-audit/error-results/summary.json`: original failure detail is
  overwritten by the generated summary.
- `/tmp/recipe-gap-audit/mutation-results2/summary.json`: both existing guard cases
  pass with the concurrency guard removed; recorded logs identify the wrong guard.

These deliberately failing preservation assertions are audit probes, not new
passing regression coverage. The findings above remain unfixed by this evaluation.
The recommended next work is narrow: repair the two demonstrated contract/naming
problems and strengthen tests at these boundaries, without redesigning the recipe
framework or replacing fixture model responses with live-agent tests.

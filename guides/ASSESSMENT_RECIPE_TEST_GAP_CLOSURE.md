# Recipe test gap implementation assessment

This implements the recipe-owned work in the
[closure plan](PLAN_RECIPE_TEST_GAP_CLOSURE.md), following the
[audit of revision 8930386](AUDIT_REMAINING_RECIPE_TEST_GAPS.md).
It fixes evidence loss and strengthens deterministic runtime coverage without
changing the overall adaptive workflow or the custom consultation selector.

## Changes versus the plan

| Plan | Implementation | Assessment |
| --- | --- | --- |
| Collect native failure evidence | `goal-attempt-errors.yaml` inspects an actual terminal attempt and passes its failure output and artifacts to the shared collector. `await-goal.yaml` uses that helper for each failed-goal attempt. Preparation, verification, and package adoption pass their original failure envelopes too. | Implemented; real failed children supply the contract, rather than invented top-level artifacts. |
| Preserve distinct filenames | `error-documents.yaml` separates summaries, returned files, and diagnostic sets while retaining complete original relative paths. Verification and rebase recovery use the same collector. | Implemented; collision and file-content regressions pass. |
| Isolate package guards | The stale-base case now has a valid validation digest; the bad-validation case has a current base. Each asserts its specific diagnostic, alongside a successful adoption control. | Implemented; removing either guard makes only its corresponding rejection case fail. Production guards needed no change. |
| Exercise recovery | Adaptive transcript export/import preserves completed and nested conversations. Explicit expert direction resumes a declined thread with its saved session and correct round counters. Native failed-child tests confirm the goal remains open. | Implemented for these boundaries. Replacement/wakeup, interrupted-worker replay, and native cancellation still need c2j fixture controls. |
| Test authority and authored packages | Actual `cell://` hooks invoke a local include using a synthetic secret. Grants succeed; absent authority and enclosing limits fail for the expected reasons. CI pins c2j and requires an authored packaged-operation smoke before broad tests. | Implemented. Model responses remain deterministic; runtime preparation and data transport execute normally. |

## Evidence behavior

For a current verification failure, the inbox contains:

```text
error/
  summary/verification.md
  files/<original hook artifact path>
  diagnostics/<set number>/<original diagnostic path>
```

Successful verification uses `verification/` instead of `error/`. Each explicitly
failed goal attempt uses its own `error/attempt-N/` directory. Rebase recovery uses
`error/rebase/`. The number distinguishes independent diagnostic sets with
same-named files; prompts still direct the agent to a directory, not an inventory.

Consequently, a hook's `check.log`, `_c2j/execution/check.log`, `verification.md`,
and `summary/failure.md` remain independent files. Recipe summaries cannot overwrite
them. Stored artifact identity is preserved even when the inbox binding name changes.

The collector follows structured diagnostic/artifact maps through nested failures,
including native `attrs.c2j_failure`, `cause`, and catch wrappers. It does not parse
log text to decide success. Setup failures without an execution log retain their
actual failure message; no synthetic log is invented. Hook exceptions retain their
failure envelope, and consuming agents receive the collector's `agent_artifacts`.

Two related issues were corrected during implementation:

- Rebase recovery also stripped prefixes and merged distinct sources. Saved
  candidate evidence and native rebase diagnostics now remain separate.
- A verification hook that changes the candidate and subsequently fails must
  preserve both facts. The candidate guard now retains the hook's original failure
  details instead of replacing the entire result with its own explanation.

Package failures merge already-prepared attempt directories directly, rather than
passing them back through a filename transformation. The package repeat fixture
now uses the observed command-failure envelope; it no longer invents a setup log
in the top-level artifact map.

## Validation and limits

Validation completed on 2026-11-06:

| Check | Result |
| --- | --- |
| Authored adaptive suites, source build of `eb636a5`, Nix 2.34.8 | 46 suites, 225 cases: 195 native-runtime cases and 30 fast branch cases. The full run passed 224; the package-repeat regression was corrected and rechecked as described below. |
| Final package-repeat and package suites on released c2j `0.0.120` | 7/7 pass after the scope correction. Together with the full run, all 225 current cases have passing results. |
| Authored packaged-operation smoke on released c2j `0.0.120` | 3/3 pass: completed, expert-directed, and nested transcript round trips. |
| Focused failure, collision, authority, guard, and rebase suites on the release binary | 15/15 pass. The four failure cases were rechecked with native open-goal assertions. |
| Guard mutations | Each deliberately removed guard fails its own negative test; the other negative test and valid adoption control still pass. |
| Structural validation and whitespace | All adaptive cases validate; `git diff --check` passes. |

The broad run caught one regression introduced during this change: package failure
outputs tried to inspect an enclosing state from inside a nested sequence and
therefore omitted collected attempt errors. The recipe now imports those errors
as a named input at the scope boundary before merging them with its own summary.
The full run was not repeated after this isolated correction; both affected package
suites were rerun successfully. No failing result was silently marked passing.

Local reports are `/tmp/gap-adaptive-final`, `/tmp/gap-package-repeat-final`,
`/tmp/gap-packages-final`, `/tmp/gap-release-smoke`, and the focused
`/tmp/gap-release-*` reports. `/tmp/gap-final-verification.json` records each of the
225 case results with the source report, retaining the original failed run.

The new native suites cover actual command and extension failures, wrapped causes,
early extension setup failure, open goals after failed attempts, source identity,
filename preservation, hook authority, package adoption guards, and adaptive
continuation I/O. Acceptance statements are also published as a test artifact by
the failed-child fixture.

Both guard mutations were made only in temporary copies. Removing the concurrency
guard fails `changed-parent-config-is-not-overwritten`; removing the validation
guard fails `different-validated-config-is-not-adopted`. The other rejection case
and the positive control pass in each mutation run.

CI now reads `.c2j-version` (`0.0.120`), whose published source commit is
`eb636a529263ab3914ae96df382a375bd6baf957`. It records the CLI/package/source and
recipe identities, Nix version, authored smoke report, and broad test reports.
The release binary used for the smoke was verified against its published checksum.

Local authored tests use Nix 2.34.8 with the colony2 cache and a portable store
mounted through proot on Linux ARM64. Recipes retain their original selectors and
declared package requirements. CI runs Linux x86_64; this local run does not claim
that remote CI has executed. An initial Nix 2.20.6 run exposed a c2j derivation JSON
compatibility bug, documented in
[the Nix report](BUG_REPORT_C2J_NIX_DERIVATION_INPUTS.md). The recipes pass the
affected setup boundary unchanged with the current Nix.

## Remaining external work

The current c2j native fixture schema supports cells, secrets, configuration,
responses, and operation effects, but has no controller-side goal actions or
worker restart/cancellation controls. Therefore this implementation does not
claim to test same-goal replacement/wakeup or interruption during nested advice.
Mocked goal-status cases remain branch tests. A model's `cancelled` response is
not a runtime cancellation test.

[The lifecycle feature request](FEATURE_REQUEST_C2J_TEST_LIFECYCLE_CONTROLS.md)
defines the required native actions and acceptance scenarios. It keeps lifecycle
administration outside task tokens and avoids building a second test engine in
this repository. Custom consultation workspace selection remains on hold pending
the separate c2j hook-workspace decision.

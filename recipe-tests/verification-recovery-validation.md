# Verification recovery validation

## Incident and scope

This fits the recipes cell: hook validation, verification outcomes, and the
transition back to implementation are recipe responsibilities.

Job `4HYqDZ4Z15Y6pMZgdmnoKn2SWJU` ran recipes revision
`f22ac49908b1aa6db939982340f6798dd9649c4c` for the `base` cell. Its JobDB record
and chapters establish:

- Chapter 48 returned `status: passed` from the repository's Python checks.
- The resolved verify hook returned `artifact_refs: ${{ sequence.verify.artifacts }}`.
  The operation's artifacts included the reserved `__git_state_thin_pack__`.
- Chapter 49 confirmed the managed candidate was unchanged.
- Chapter 50 rejected the artifact map at
  `build/run/heavy/heavy/develop/verify/sequence/verify/development-verify/check/build-hook-verify/report/build-hook-report/invalid/invalid`.
- The job ended `failed_app` with a command-execution error instead of returning
  the failure to implementation.

The previous workflow repaired returned `status: failed` results but propagated
hook exceptions. Existing verification tests explicitly expected terminal errors
for malformed YAML/output, unsafe artifacts, mutation, command failure, and timeout.
The publication/rebase fixes did not change that verification policy.

The corrected policy keeps hook validation strict. The shared development verify
wrapper catches non-cancellation errors across hook loading, execution, validation,
candidate checks, and reporting. It supplies failed verification and independent
value artifacts containing the diagnostic report and original structured failure.
It does not try to bind the rejected artifact map again. Invalid report errors now
identify the offending names and preserve the original failure as their cause.

Both build paths return failed or required-skipped verification to their existing
implementation session, clear cached outcome approval, and repeat the ordinary
checks and review before publication. Other hook and implementation errors retain
their existing propagation.

## Test method

Runtime: `c2j dev-e7e2184`, built from
`e7e2184f843500db9d6fe3dd2b6149a25de26aba`.

| Check | Result |
| --- | --- |
| `verification.test.yaml` | All 18 cases passed, including the two additional evidence/capability cases run separately. |
| `verification-recovery.test.yaml` | All 5 full workflow cases passed across focused runs. |
| `build-hooks.test.yaml` | All 7 general hook regressions passed. |
| `merge-chase.test.yaml`, `light-verification-repair-preserves-budget` | Passed; verification repair retains the existing chase allowance. |
| Strict native validation of the workflow recovery suite | All 5 valid. |
| `bash build.sh`, `git diff --check` | Passed. |

`verification.test.yaml` uses native hook loading, command execution, schema
validation, timeouts, candidate checks, and artifact binding. The report-render
and denied-capability errors are injected; cancellation uses a native classified failure to check that
the recovery boundary does not swallow cancellation.

`verification-recovery.test.yaml` reproduces the incident by returning the entire
artifact map after a real candidate edit. Model decisions and human input are
mocked; hook execution, report rejection, subsequent hook loading, Git operations,
and publication are real. Repair changes the hook to export only `tests.log`.
The cases cover both build paths, missing/skipped required verification, readable
failure artifacts in the resumed agent, fresh assessment and review, and an
implementation-agent failure that must still propagate. Heavy cases publish
[`verification-recovery-statements.md`](verification-recovery-statements.md) as
their test-plan artifact.

Reproduce with the required c2j build and a working Nix installation:

```sh
c2j test run --file recipe-tests/verification.test.yaml
c2j test run --file recipe-tests/verification-recovery.test.yaml
c2j test run --file recipe-tests/build-hooks.test.yaml
c2j test run --file recipe-tests/merge-chase.test.yaml --case light-verification-repair-preserves-budget
```

The local portable Nix setup is described in the
[Nix prerequisite](../guides/BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md#separate-local-test-prerequisite).
Running all Go/runtime work under its filesystem adapter caused initial local
timeouts. Native-only suites were also run directly; full build cases used
`GOMAXPROCS=2` and longer case timeouts. No runtime or operation behavior was
mocked to work around those timing limits.

Reports are under `/tmp/verify-contract-final`, `/tmp/verify-evidence-errors`,
`/tmp/verify-flow-one`, `/tmp/verify-flow-remaining`, `/tmp/verify-agent-error-final`,
`/tmp/verify-hooks-direct`, and `/tmp/verify-chase-regression`. The final negative
workflow case was rerun after removing an unused approval response from its fixture;
the verified behavior is failure before any approval or publication.

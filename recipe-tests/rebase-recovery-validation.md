# Structured rebase recovery validation

Validated on 2026-11-01 using **c2j dev-e7e2184**, built from the clean archive of
`e7e2184f843500db9d6fe3dd2b6149a25de26aba`. This includes structured rebase
errors (operation metadata 1.1.0, failure payload version 1). The installed
`a501d923f053` binary lacks that contract and was not used for these checks.
The test binary is `/tmp/rebase-c2j-bin/c2j`; no c2j source was modified.

| Suite / check | Result |
| --- | --- |
| `rebase-policy.test.yaml` | 27 passed: valid conflicts, exhausted allowance, malformed/missing evidence, wrong origin, unsupported schema, cleanup failure, cancellation, timeout, and unrelated errors. |
| `rebase-native-repair.test.yaml` | Passed: real conflicting history, native restore, durable diagnostic bindings, fresh local repair, native rebase, and verification of the adopted base. |
| `rebase-recovery.test.yaml` | 5 passed: failed repair agents, preserved allowance during light-to-heavy escalation, and fresh review after repair on both paths. |
| `merge-chase.test.yaml` | All 23 cases passed across the full regression run and targeted rerun described below. |
| `build-merge.test.yaml`, `rebase-failure-propagates-before-final-review` | Passed: unclassified rebase failure still propagates before final review. |
| Strict native validation of `rebase-recovery.test.yaml` | All 5 valid. |
| `bash build.sh`, `git diff --check` | Passed. |

The full-build conflict cases use real native rebase failures and mocked model
responses. They assert the original failure code and node, bound diagnostic
content, session retention, and publication counts. The two budget-exhaustion
cases in `merge-chase.test.yaml` replace the former broad op-name-only checks,
which could mistakenly pass when a catch expression itself failed.

The full merge-chase run passed 21 cases. Its two new exhaustion cases reached
the expected native third conflict, but a session assertion initially addressed
the extension wrapper instead of its nested op inputs. After correcting that
assertion, both passed on a targeted rerun. The 23 cases cover ordinary approval
reuse, independent chase limits, unrelated merge/squash errors, revisions,
escalation, changed reviewed content, no-change completion, and conflict limits.

The fresh-review cases simulate a successful third rebase to isolate subsequent
recipe routing. They require new verification and human approval, and fresh
heavy file accounting, without another publication. Actual Git repair mechanics
are tested separately by `rebase-native-repair.test.yaml`: a command stands in
for the agent's local repair commands; all Git operations and workspace restores
are real. The test checks the original restored HEAD and clean index before
starting a new rebase, reads diagnostic artifacts in a subsequent task, and
checks both candidate and concurrent upstream contents after native refresh.

The new heavy workflow cases publish
[`rebase-recovery-statements.md`](rebase-recovery-statements.md) as their test-plan
artifact. Per-round failure artifacts preserve their original stored diagnostic
identities and supply delivery names required by downstream assessment.

These checks cover task-to-task persistence in the native runtime. They do not
simulate process termination during a repair or an unavailable artifact store.
The native c2j contract owns completed-task replay and worker replacement; the
recipes retain the counter and evidence in durable flow and artifact references.

With a c2j binary containing the required commit:

```sh
c2j test run --file recipe-tests/rebase-policy.test.yaml
c2j test run --file recipe-tests/rebase-native-repair.test.yaml
c2j test run --file recipe-tests/rebase-recovery.test.yaml
c2j test run --file recipe-tests/merge-chase.test.yaml
c2j test run --file recipe-tests/build-merge.test.yaml --case rebase-failure-propagates-before-final-review
```

Local execution used the existing portable Nix store setup and temporary static
`inputDrvs` compatibility adapter described in the
[local Nix prerequisite](../guides/BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md#separate-local-test-prerequisite).
The adapter does not replace packages or recipe operations. Test reports are in
`/tmp/rebase-policy-final`, `/tmp/rebase-native-final`,
`/tmp/rebase-recovery-complete`, `/tmp/rebase-merge-regression`,
`/tmp/rebase-exhaustion-final`, and `/tmp/rebase-unclassified`.

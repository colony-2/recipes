# Adaptive2 native tests

`direction-review.test.yaml` and `build-delivery.test.yaml` run the public root
`build.yaml`, so changing its routing cannot leave these tests exercising a stale
standalone entrypoint. `default-child.test.yaml` also resolves a real named build
with that entrypoint in a disposable repository. Consultation and handoff suites
exercise the inline protocol and original artifact identity.

`../self-improvement/build.test.yaml` covers the public build's existing local
hooks and audit inputs. The previous `../adaptive/` flow suites intentionally use
`../adaptive/build.yaml`, a test-only copy of the old public input contract which
includes the retained adaptive implementation. Their helper coverage remains
useful, but they do not prove the new direction flow.

Run the normal native suite with the pinned c2j and packaged operations:

```sh
c2j test run --directory recipe-tests/adaptive2 --case-timeout 3m --out-dir /tmp/adaptive2-tests
c2j test run --directory recipe-tests/self-improvement --out-dir /tmp/build-hooks
```

Live trials are explicitly selected `.live.yaml` files, use actual Codex, and
retain generated packets through `export_review_packet.py`. They are documented
in [the workflow guide](../../recipes/adaptive2/README.md) and
[the rollout assessment](../../guides/adaptive2/ROLLOUT.md).

The automatic-limit regressions use real input receipts, inline consultations,
package decisions, child submission, Git races, and artifact transport. Model
decisions are scripted. `build-handoff-recovery.test.yaml` exercises parent output
normalization and correction through the public build, including identical and
changed outbox copies. `human-turns.test.yaml` repeats human reviews under an
explicit one-turn allowance. `merge-turns.test.yaml` uses a real concurrent Git
writer to check approval reuse and renewed retry allowances.

The November 9 additions cover selected review links, actual native approval
recovery, correction/implementation grants, receipt expiry, parent waiting, and
UI validation routing. `../adaptive/approval-equivalence.test.yaml` uses real Git
history to test same-file context, binary changes, executable modes and extra edits.
The older cap assertions now explicitly choose Stop at the new decision; their
work-pass counts and human-exclusion assertions remain unchanged.

`visual-review.live.yaml` renders an actual static page with `chromium` on PATH,
then uses live Codex assessment and summary plus the normal final review selector.
It retains the original binary screenshot for export. It does not publish code.
`limit-decision.live.yaml` produces live implementation, mechanical-report and
scope-conflict decision briefs. Native choices are scripted to finish these local
trials; the explanatory text is model-generated.

```sh
c2j test run --file recipe-tests/adaptive2/visual-review.live.yaml \
  --include-live --case-timeout 4m --parallelism 1 --out-dir /tmp/visual-review
c2j test run --file recipe-tests/adaptive2/limit-decision.live.yaml \
  --include-live --case-timeout 4m --parallelism 1 --out-dir /tmp/limit-reviews
```

`limit-child.test.yaml` exercises actual child submission, native input, parent
waiting and terminal completion status. The harness answers pending forms promptly;
it cannot test a prolonged unanswered review, process-restart replay, or deadline
expiry while waiting. Receipt replay tests exercise the recipe's idempotent
accounting; they are not a substitute for those runtime lifecycle tests.

`cross-parent-recovery.test.yaml` creates a previous parent and receiver jobs in
two cells, then runs the production coordinator and receiving build with an empty
coordination history. It checks recovery with separate approval/attempt IDs,
recovery with only `resume_from`, selective artifacts, duplicate prevention, and
reuse of completed work. `accepted-recovery.test.yaml` verifies that a recovery
source cannot bypass comparison with a current receiver agreement.
`recovery-status.test.yaml` runs the native recipe engine with scripted job-status
responses to check waiting and unreadable-source correction; it does not simulate
a worker restart or a prolonged human wait.

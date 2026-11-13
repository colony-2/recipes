# Adaptive2 native tests

The suites use `recipes/adaptive2/build.yaml` explicitly. Default explicit adaptive2 build
coverage now lives in `../adaptive3/default-build.test.yaml`; retargeting these
regressions preserves their adaptive2 purpose after the default switch.
Named-child fixtures install the real adaptive2 entrypoint and its companion
recipes into disposable repositories. Existing consultation/recovery assertions
remain specific to adaptive2.

`../self-improvement/build.test.yaml` retains the adaptive2 hook regression;
adaptive3's default-build suite separately checks repository-improvement inputs,
backgrounders and native verification through the new default.

`../adaptive/hook-const.test.yaml` checks discarded read-only hook edits, nested
`const` inheritance, persisted prepare edits, and floating branch advancement.
`build-delivery.test.yaml` also completes the explicit adaptive2 build after configure attempts
an edit. See the [hook expectations and validation](../adaptive/hook-const-statements.md).

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
normalization and correction through the explicit adaptive2 build, including identical and
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
source cannot bypass comparison with a current receiver assignment, while supporting
files can change independently. `handoff-documents.test.yaml` exercises the public
build and receiving child with new evidence, moved and omitted files after correction,
and consultation history retained outside subsequent inboxes. These regressions
check actual materialized child artifacts, not just the returned filename list.
`recovery-status.test.yaml` runs the native recipe engine with scripted job-status
responses to check waiting and unreadable-source correction; it does not simulate
a worker restart or a prolonged human wait.

`annotation-growth.test.yaml` runs four implementation/review rounds through the
explicit adaptive2 build, with 24 separate evidence logs, three human revisions and a final
merge. It checks current artifact identity, unique annotations and retained source
links. The previous recipe exceeded JobDB's final-output limit on this fixture.
`current-annotations.test.yaml` covers descriptor replacement, stale references,
aliases and unchanged provenance. `review-packet.test.yaml` also checks annotation
replacement across repeated report corrections and a human allowance increase.

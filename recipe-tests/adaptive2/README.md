# Adaptive2 native tests

`direction-review.test.yaml` and `build-delivery.test.yaml` run the public root
`build.yaml`, so changing its routing cannot leave these tests exercising a stale
standalone entrypoint. `default-child.test.yaml` also resolves a real named build
with that entrypoint in a disposable repository. Consultation and handoff suites
exercise the inline protocol and original artifact identity.

`../self-improvement/build.test.yaml` covers the public build's existing local
hooks and audit inputs. The previous `../adaptive/` flow suites intentionally use
`../adaptive/build.yaml`, a test-only copy of the old public input contract which
includes the unchanged adaptive implementation. Their helper coverage remains
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

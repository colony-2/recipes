# Native recipe test ownership

The current build and consultation kernel are covered by native integration cases
in `recipe-tests`. The old build/evolve, mandate-bootstrap, phase-wrapper, and
ad hoc consultation fixtures were replaced alongside their implementations.
Their historical assertions remain in Git history; removed interfaces are not
kept executable solely to satisfy old fixtures.

| Behavior | Current suites |
| --- | --- |
| Build lifecycle, optional purpose, initial instructions, checkpoint continuation, independent assessment, focused questions, annotated reviews, verification repair, cancellation, merge | `build-kernel.test.yaml` |
| Build entry from a serving checkpoint and namespaced transcript, followed by assessment, reviews, and merge | `build-handoff.test.yaml` |
| Concurrent consultation jobs, later caller progress, target checkpoint handoff, root eligibility, duplicate submission, child failure, artifact collisions | `build-coordination.test.yaml` |
| Approval and agreement gates, stable keys, missing root/provisioning configuration, retained failures | `build-coordination-gates.test.yaml` |
| Verification success, failure, external timeout, missing hook, retained logs | `verification.test.yaml` |
| Consultant-owned agreement, bounded exchanges, document validation, expert escalation and adverse outcomes | `consultation-kernel.test.yaml` |
| Candidate isolation, immutable checkpoints, caller and serving-cell continuation | `consultation-kernel-handoff.test.yaml` |
| Human-directed continuation, repeated review, attachments, failed-turn retry, invalid resumption | `consultation-kernel-{resume,review,retry,invalid-resume}.test.yaml` |

Codex responses are fixtures. Native runtime execution handles Git workspaces,
immutable objects, artifact materialization, included recipes, asynchronous jobs,
human reviews, and merge. Build coordination uses a small stand-in dependency
recipe to verify the exact checkpoint and document handoff; provisioning a real
new repository is outside these cases.

[Build statements](../recipe-tests/build-kernel-statements.md) and
[consultation statements](../recipe-tests/consultation-kernel-statements.md) specify
expected outcomes. The build lifecycle publishes the build statements as an artifact.
The remaining repository examples retain their own scenario or fixture suites.

Runtime persistence, cancellation of leased workers, crash recovery, pack handling,
and low-level replay faults belong to c2j tests. Session serialization and schema
enforcement internals belong to c2ops. Recipe tests check routing and observable
contracts without implementing substitute infrastructure or a second schema validator.

```sh
c2j test run --directory recipe-tests --case-timeout 3m --out-dir .c2j/test-results
```

Validated with c2j v0.0.82 on 2026-10-20: 67 native integration cases passed
(34 consultation, 17 build lifecycle, 12 coordination/handoff, and 4 verification).

# Native recipe test ownership

Adaptive is the build implementation. Tests for retired heavy/light, old ticket/job,
and superpowers workflows have been removed with their sources. Their contracts
remain in Git history, not executable compatibility entrypoints.

All paths below are relative to `recipe-tests/`.

| Behavior | Current suites |
| --- | --- |
| Build lifecycle and outcomes | `adaptive/flow.test.yaml`, `adaptive/standalone.test.yaml` |
| Consultation, nesting and requester candidate | `adaptive/consultation.test.yaml`, `adaptive/consultation-continuation.test.yaml`, `adaptive/consultation-candidate.test.yaml` |
| Coordination agreements, submissions and failure recovery | `adaptive/build-coordination.test.yaml`, `adaptive/coordination-contract.test.yaml`, `adaptive/parent-recovery.test.yaml`, `adaptive/required-jobs.test.yaml` |
| Current review and meaningful questions | `adaptive/current-review.test.yaml`, `adaptive/review.test.yaml` |
| Error evidence, artifact selection and response correction | `adaptive/failure-evidence.test.yaml`, `adaptive/artifact-selection.test.yaml`, `adaptive/response-files.test.yaml` |
| Package approval, probes and recovery | `adaptive/package-recovery.test.yaml`, `adaptive/package-policy.test.yaml` |
| Creation review and catalog integration | `create.test.yaml`, `create-handoff.test.yaml` |
| Native registration and publication boundaries | `cell-registration.test.yaml`, `registered-cell-publication.test.yaml`, `creation-publication.test.yaml` |
| Creation response repair and artifact matching | `result-repair.test.yaml`, `artifact-result.test.yaml` |
| Retained creation brief, presentation and optional synthesis | `review-*.test.yaml` |

Models are mocked in deterministic suites. Native runtime execution handles Git
workspaces, checkpoints, artifacts, included recipes, child jobs, human reviews,
and merge. Model/schema acceptance has separate explicit live coverage; mocked
`output_schema_valid: true` does not establish provider acceptance.

Runtime persistence, leased-worker cancellation, crash recovery, pack handling,
low-level replay and reusable fixture infrastructure belong to c2j. Session
serialization and provider behavior belong to c2ops. Recipe tests check routing
and observable contracts without substituting an execution engine.

```sh
c2j test run --directory . --case-timeout 3m --out-dir .c2/test-results
```

Use the release in `.c2j-version`. See [the cleanup assessment](ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md)
for current results and [retirement expectations](../recipe-tests/retirement-statements.md)
for what this removal must preserve. Earlier 107/111-case migration results describe
an obsolete workflow revision and are available in Git history.

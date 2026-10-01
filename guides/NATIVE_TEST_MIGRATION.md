# Test coverage and ownership migration

The baseline is recipes `3d3f24e`. The native runner executes the production
recipes and their normal includes. Static model outputs replace external
reasoning; actual schema gates, commands, input submissions, dependencies,
snapshots, and merges remain real in runtime cases.

## Recipe-owned coverage

| Former source / cases | Native declarations |
|---|---|
| Default routing: 26 cases per entrypoint, phase order, scoped paths, repeated feedback, invalid outcomes and merge gates | `recipe-tests/build.scenario.md`, `evolve.scenario.md` |
| Real agent gates: valid/invalid result artifacts, initial and resumed sessions (26 cases) | `recipe-tests/agent-gates.test.yaml` |
| Foreign result gates: done, ask-user, incomplete/error, missing session and malformed/schema-invalid replies (8 cases) | `recipe-tests/consultation-gates.test.yaml` |
| Test-plan publication and missing maintained plan | `recipe-tests/test-plan.test.yaml` |
| Verification pass, failure, timeout and skipped hook, exported report/log names | `recipe-tests/verification.test.yaml` |
| Empty, duplicate, already-recorded, multi-round, failed/cancelled/unmerged dependencies (10 cases) | `recipe-tests/dependencies.test.yaml` |
| Actual child submission, multiple children, scoped work, successive rounds, failed-child recovery, unmerged outcomes, missing session and invalid reply | `recipe-tests/dependency-runtime.test.yaml` |
| Late advice, bug/evolve redesign, multiple cells, missing mandate/outside ownership, failed history, malformed reply, missing checkpoint, forbidden children, unavailable cell | `recipe-tests/implementation-consultations.test.yaml` |
| Design dialogue, design-to-implementation conversation reuse, later human feedback | `recipe-tests/consultation-{design,reuse,feedback}.test.yaml` |
| Both full lifecycles: consultation, redesign/reapproval, real child submission, child verification/merge, parent verification failure/recovery and merge | `recipe-tests/{build,evolve}-lifecycle.test.yaml` |
| Both review flows: two/four documents, text and file revisions, annotations, redesign, edits accompanying approval, final receipts/documents | `recipe-tests/{build,evolve}-reviews.test.yaml` |
| New-ticket/jobs routing, example recipes, Superpowers phase/task/skill routing and static bundle checks | Existing self-contained `.scenario.md` files |
| Superpowers primary's missing-reproduction branch through actual inline includes | `recipes/superpowers/tests/superpowers-inline.test.yaml` |
| Real Codex skill/quality and run_skill smoke tests | Explicit `live: true` suites; require `--include-live` and service credentials |

The cancelled-dependency decision remains a recipe test; cancelling a leased job
and replacing workers are c2j mechanics. Likewise the already-finished child and
feedback-history cases split into normal dependency/history assertions here and
c2j's execution/replay guarantees below. They are not replaced by sleeps or
process management hidden in YAML.

## Runtime guarantees retained in c2j

These destinations are in the c2j repository. They execute without this recipes
checkout. The native runner has its own Go integration tests as well.

| Guarantee / transferred statements | c2j destination |
|---|---|
| CLI compile, invalid declarations, empty selection, result files; TS-024–027 | `cmd/c2j/internal/testjob/runner_test.go`, `discovery_test.go` |
| Child status and required/optional group policy; TS-049–050 | `pkg/ops/recipe/await_result_soft_test.go`, `child_group_test.go`, `child_job_id_test.go` |
| Submitted and bound artifacts, child evidence forwarding | `pkg/child/test-fixtures`, `pkg/worker/compiler/child_snapshot_integration_test.go`, `artifact_bindings_test.go` |
| Broker compiled includes and lineage; TS-146 | `pkg/childbroker/compiled_recipe_test.go` and broker integration tests |
| Local/default selectors, nested/git includes, no sibling-copy requirement | `pkg/worker/compiler/inline_resolution_test.go`, `root_source_test.go`; CLI submit tests |
| Explicit workspace isolation and fresh experiments | `pkg/worker/compiler/workspace_integration_test.go`, `workspace_replay_test.go` |
| Parent resumes after child merge without snapshot collision, duplicate submission, or changed evidence keys; runtime portions of TS-147–151, TS-159 | `TestAwaitMergedChildPreservesParentSnapshotAndChildEvidence`, `TestReplayLegacyArtifactOrderWithRealJobDB` |
| Immutable checkpoints, parallel branches, failed attempts, later jobs, hidden state and invalid refs; TS-163–165 | `pkg/objects/store_test.go`, `pkg/worker/compiler/objects_integration_test.go`, `objects_input_test.go` |
| Invalid/stale review answers, attachment binding and replay; TS-168 and runtime part of TS-171 | `pkg/input/review_test.go`, `pkg/input/test-fixtures/review_test.go` |
| Nested history survives JSON/CEL conversion | `pkg/template/native_result_test.go` |
| Native isolated cells, broker child effects, reviews/uploads, real merge, fixture failures, timeout, parallelism and matching | `cmd/c2j/internal/testjob/runtime_test.go`, `pkg/recipetest` tests |

## Codex adapter coverage

The old `verify-object-sessions.py` combined generic c2j checkpoint tests with
Codex private-home/session implementation checks. The latter already live in
c2ops `ded76dfbd877d3d0749e509844ecdbc57197b572`:

- `codex/pkg/codex/session_test.go`: `TestSessionBranchesRestoreExactCheckpoint`,
  `TestSessionExportIncludesWALAndRejectsIncompleteState`,
  `TestSessionRejectsLegacyInputsAndInvalidState`, `TestRunFailureDoesNotPublish`,
  `TestSessionRejectsUnsupportedMetadataAndCorruptDatabase`.
- `codex/pkg/codex/op_skill_run_test.go` and `internal/extensioncmd/command_test.go`
  cover skill continuation and extension result envelopes.

`go test ./pkg/codex ./internal/extensioncmd` passed at that revision. The
recipe-owned part of TS-157–162 is retained in routing, consultation, dependency,
and review cases. This migration makes no c2ops implementation changes.

## Superseded review proposal

`verify-review-contract.py` tested the earlier hash/download-URL review proposal,
not the implemented questions/documents input model. TS-152–156 and
`contracts/review/v1.schema.json` remain historical design material; their old
schema tests are retired. TS-166–172 and native review declarations exercise the
supported model. Runtime API validation belongs to c2j as listed above.

## Native compatibility CI

c2j's `.github/workflows/test.yaml` now runs native directory discovery against
pinned recipes and c2ops checkouts. The Python runner, external server setup and
both transitional patch files are removed. There is no migration patch to apply.
Publish the pinned companion recipes commit before running the coupled c2j CI
revision, so GitHub can fetch it.

```sh
c2j test run --directory test-repos/recipes --case-timeout 5m --out-dir "$RUNNER_TEMP/recipe-results"
```

## Assertion audit follow-up

The initial 220-case run did not by itself establish equivalence. The follow-up
adds exact checkpoint comparisons, consultation worktree observations and cell
order, dependency evidence/history delivery, all-failed recovery, a separate
feedback continuation, and absence of stale review attachments. The runtime
runner captures selected files before each op and successful op outputs so these
assertions can inspect actual execution.

c2j now has dedicated `TestChildWaitSurvivesWorkerReplacementAndCancellation`,
`TestAwaitAlreadyFinishedChildAfterWorkerReplacement`, and
`TestFreshConsultationSeesAdvancedUpstreamWithoutLosingCandidate` regressions.
Its `testdata/recipe-compatibility/MIGRATION.md` records concrete destinations
and explicitly distinguishes retired proposal tests and excluded live work.

## Verification for this migration

- Clean c2j `go test ./...` and focused race tests for the runner passed.
- Initial repository discovery ran 220 cases in 50 suites successfully. Three live suites
  were reported as excluded, not passed; live model work was not run.
- Preflight validation passed for every suite, including live declarations.
- Added commit/file assertions passed for both complete lifecycles, both review
  flows, and consultation isolation. Strengthened feedback/session assertions
  passed for both entrypoints.
- An intentionally broken verification recipe reported success for a failed
  hook; the declared case rejected that policy defect with an assertion failure.

Follow-up audit: a fresh checkout and empty selector cache passed **222 cases in
51 suites** through the compatibility CI command; three live suites were
excluded. Later strengthened lifecycle assertions passed for both build and
evolve. c2j's full integration-tagged suite and focused race tests passed,
including three repeated runs of the new restart/upstream regressions. The
pinned c2ops Codex/session and extension-command tests also passed.

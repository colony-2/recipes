# Adaptive3 regression results

## November 27 delegate implementation

**118 cases passed across 19 focused native suites** with pinned c2j `a6de3eca`. Repository-wide validation compiled 1,114 cases in 196 suites and excluded three live suites. All 66 Python checks across Adaptive3, the merge queue and review/v2 passed. The repository purpose and workflow timeout checks passed.

The native tests script the model’s decisions. The runtime executes the dispatch loop, review submissions, workspace restoration, hooks and Git operations. These cases establish which actions the recipe permits and what information reaches the next actor. Real jobs are needed to measure how often a model makes a good decision.

| Tested behavior | Observed result |
|---|---|
| A person asks a question about a plan | The delegate answers in the same review with the files closed. The later approved change lands through the grouped queue. [Default build](../../../recipe-tests/adaptive3/default-build.test.yaml) |
| The planner’s assumptions need a check | The native form collects an Other answer and a skip together. The planner receives the actual choices, typed words, source references and submission. Stopping the worker and reopening SQLite after the submission creates exactly one form. [Interview and restart](../../../recipe-tests/adaptive3/delegate-build.test.yaml) |
| The delegate decides the assignment is complete | An explanation finishes directly. A parent can receive its verified patch. A covered change can land under Take to Completion. A requested final review still blocks completion until answered. [Public build](../../../recipe-tests/adaptive3/build.test.yaml) · [Permission checks](../../../recipe-tests/adaptive3/dispatch-check.test.yaml) |
| An operation fails or needs help | A local repair receives its saved edit and diagnostic. A negotiation retains the owner’s agreement. The package probe receives the reviewed configuration. Three malformed delegate decisions stop with the recorded error. [Delegate operations](../../../recipe-tests/adaptive3/delegate-build.test.yaml) |
| A job needs to retry publication | The recipe accepts the native merge and approval producers. An unverified claim from a dependency cannot skip the queue. [Recovery](../../../recipe-tests/adaptive3/merge-receipt.test.yaml) · [Dependency](../../../recipe-tests/adaptive3/dependency-feedback.test.yaml) |

## Earlier review and recovery implementation

All 114 cases across 20 focused native recipe suites passed with the repository’s pinned c2j, `a6de3eca`. The fixtures script agent decisions. C2 executes the workspace, receipt, routing and Git operations under test. The queued merge case passed on rerun after a local tool-cache collision. The 61 Python checks, repository purpose checks and workflow timeout checks also passed.

| Replay | What the test checks |
|---|---|
| Saved Cortex candidate | A second writable turn opens the first turn’s partial edit and receives its diagnostic. The completed change lands through native Git integration. |
| Repeated review | A human reply carries its presented packet to the next author. An internal draft leaves the first presentation intact. A cited wrapper already present in Tests clears review with the original file. |
| Shared scope and withdrawal | Three owners receive the same source receipt and one raises a local conflict. A confirmed withdrawal reaches the parent. Cancelling a child without a withdrawal leaves the assignment open. |
| Negotiation and repair limits | Receiver corrections leave room for a counteroffer. Four unresolved exchanges stop. Repeated internal corrections stop without creating an agreement. |
| Outcome and publication | Full approval with eligible evidence goes through merge to the requested consumer check. Missing hosted evidence returns to implementation. A necessary exception goes to the delegate. A failed consumer check can retry against the same landed result. |

The consumer fixture reports a scripted observation against the actual landed hash. It exercises the handoff and records the evidence. Live consumer behavior, human reading effort and the exceptional-help rate belong to the next job cohort. [Field measurements](improvement-plan.md#check-the-effect)

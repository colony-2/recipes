# Recovery implementation and runtime bug report

## Outcome

Completed the [recipe plan](improvement-plan.md). A new parent can continue work
assigned by a previous parent without importing its coordination history or
repeating consultation solely to recreate records. The receiver still checks the
actual prior approval and the current scope before implementation.

The independent numeric restart defect was confirmed and submitted to c2j:

- New goal: `3LtEdXpnSuxCzcrEcirncuL8W7j`.
- Initial job: `3LtEddFZ73GwSmaEpKXc9I6ozD4`.
- JobDB: `http://192.168.1.195:9047/c2`.
- Attachments: [bug report](c2j-bug-report.md) and [Go reproduction](restart-counter.go).

The reproduction resolves the actual CEL default rather than supplying an
assumed numeric type. It repeats the unchanged expression successfully, then
fails only after c2j's native restart clone/adopt converts an interface-held int64
to float64. A concrete typed Go field retains its type through the same JSON
round trip. No numeric casts or runtime workaround were added to recipes.

## Changes versus plan

- **Prior work inspection stays with the agent.** Shared prompts explain that the
  earlier attempt and receiver handoff may come from another parent. The agent
  reads prior status, human feedback, and the receiver assignment, then selects
  useful files. `replaces` identifies the unsuccessful attempt; `resume_from` can
  identify a different job containing the approved direction.
- **Existing lifecycle handling covers earlier parents.** The coordinator no
  longer requires `replaces` to occur in its own history. It inspects that job,
  or the approval source when no replacement is given. Active work is awaited;
  successful results are consumed. Once this parent starts a replacement, repeated
  requests reuse its recorded attempt.
- **Approval checking remains in the receiver.** Without a current agreement,
  an explicit recovery source permits the selected handoff to reach the existing
  approval inspection and scope assessment. No synthetic approval or copied
  coordinator history is created. Missing approval and changed scope still enter
  ordinary design review.
- **Current agreements remain protected.** If this parent has an agreement with
  the receiver, its existing handoff selection and byte comparison still apply.
  Supplying a recovery source cannot bypass a changed-file correction.
- **Inspection failures are actionable.** An unreadable previous attempt becomes
  a correction for the working agent rather than aborting coordination without
  a chance to fix the reference. Cancellation still propagates.

The last item is a small addition to the plan: accepting external references
makes their inspection a possible error boundary. It reuses the existing invalid
response path, with no new review or recovery service.

## Verification

Used pinned c2j **0.0.124**. **26 executed cases passed**:

| Suite under `recipe-tests/` | Cases | Coverage |
| --- | ---: | --- |
| `adaptive2/cross-parent-recovery.test.yaml` | 4 | Real previous parent/receiver jobs, production receiving build, selected artifacts, earlier approvals, merge, duplicate prevention and missing agreement |
| `adaptive2/accepted-recovery.test.yaml` | 2 | Current assignment comparison still applies during recovery |
| `adaptive2/recovery-status.test.yaml` | 2 | Native engine with scripted active/unavailable status observations |
| `adaptive2/build-handoff-recovery.test.yaml` | 3 | Original copies, changed-file correction, bounded human decision |
| `adaptive2/approved-recovery.test.yaml` | 6 | Large history, missing/active source, revised direction, changed scope, retained candidate |
| `adaptive2/sibling-recovery.test.yaml` | 1 | Actual task-token reads of earlier approval/artifacts |
| `adaptive2/handoff.test.yaml` | 3 | Ordinary receiver handoffs, rewritten scope, selected recovery evidence |
| `adaptive/parent-recovery.test.yaml` | 3 | Failed/cancelled children, corrected replacement, parent checkout isolation |
| `adaptive/required-jobs.test.yaml` | 2 | Completion and failed-child recovery before outcome review |

Structural validation passed for **98 adaptive2 cases**. This is not a claim
that all 98 were executed. The status-only suite initially used the simulated
runner, whose structural evaluation traversed unpopulated coordination paths;
it now uses the native runtime consistently with the other new cases.

The two central regressions were also run against isolated copies of the old
coordinator and handoff checker. They failed with the original messages:

- `A replacement must identify a recorded execution job in the same cell.`
- `No accepted receiver-authored assignment is recorded for storage. Consult that owner before requesting execution.`

Tests script model decisions; they exercise artifacts, task permissions, child
jobs, ordinary reviews, workspaces and publication through c2j. The active-status
case checks routing with a scripted observation rather than claiming a sustained
live wait. Runtime process-restart coverage belongs to the submitted c2j bug.

## Deployment and user guidance

No observed job was answered, restarted, cancelled, or changed. The only remote
submission was the explicitly requested c2j bug-report goal. These recipe changes
must be published before new jobs can consume them; existing executions retain
their captured recipes.

[Recovery commands for Cortex job 3LsmZNUoxBXwnTcoJKekMAZagiX](guidance-recovery.md)
start a new goal using the published recipe, select the prior job with
`resume_from`, and explicitly prioritize the latest human corrections. Its latest
consultation had already withdrawn the proposed reader interface; the remaining
checkpoint-type proposal should be judged against existing c2j capabilities.

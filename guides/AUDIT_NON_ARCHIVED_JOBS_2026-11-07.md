# Non-archived job audit, 2026-11-07

Observed JobDB: `http://192.168.1.195:9047/c2`. Read-only investigation begun at approximately 23:51 UTC November 6, using the census and chapter snapshot below. I did not submit, answer, cancel, restart, or modify jobs. No recipe changes were made.

The census at **23:59:47 UTC November 6** contains **22 non-archived jobs**, including hidden jobs: 17 ACTIVE, four PENDING_JOBS, and one READY with an outstanding human-input form. There were nine at the initial inspection; the root configuration job subsequently launched twelve children, and the consumer-validation chain launched another c2j child. These are observations of ongoing execution, not final outcomes.

Twenty-one jobs resolve recipes commit `a3fea1fcfefb3b403dad1e9e20cf9ab48953411c`. Root configuration job `3Lkm5MsE1rhgvkrWp1U47u0k6ib` resolves `5c6a6fbb3d3c40c83ebc03574f7591b4d92ed5ff`; the intervening commit preserved adaptive recipe behavior. Recorded runtime version is `v0.0.122-0.20261106203926-483cb48a328e+dirty`.

This investigation fits the recipes cell's responsibility for orchestration, prompts, artifact handoffs, and regression tests. Gitvend owns the Git routing defect. Runtime/test-observation capabilities belong to c2j. Deployment of the gateway is a separate operational outcome; this audit does not establish its operator.

**Current chains**

| Job | Cell | Observed state and purpose |
| --- | --- | --- |
| `3Lkn1955P8gAaHVdCfJSseHtvCm` | cortex | PENDING_JOBS; historical review/input UI, awaiting c2j implementation. |
| `SVYbGlC2gSzO0r8bUo1bEkBx1tT` | c2j | ACTIVE; child above, missing authoritative input documents; later produced implementation during a const recovery turn. |
| `3Lkmx2cuJfjwLkQJWCcvRq3078w` | cortex | PENDING_JOBS; verification hook blocked by dependency-fetch routing failure. |
| `Ml2DvQlSxpW9LgLVMSooNak4PU1` | gitvend | READY with human input; routing repair locally verified, waiting for gateway operator/adoption information. |
| `3LkmsHa9110zYoDvdSpKsO7tyKk` | gitvend | ACTIVE; verification hook passed; repeatedly polling root for extra consumer-validation evidence. |
| `8j669T4el8xw5ZqpxfxZysGKWIR` | root | PENDING_JOBS; child of Gitvend, forwarding recipes-owned consumer validation. |
| `3Lkp3SLrLzI1zxGYBzfJyDgh019` | recipes | PENDING_JOBS; child of root, awaiting extra c2j test-observation support. |
| `WP1Pq14GIkydOCYzP859iqIIoMa` | c2j | ACTIVE; child of recipes, planning the test-observation bridge. |
| `087c1f39-8ba0-4ccf-83b3-30124e288a11` | cortex | ACTIVE; cell-label/UI layout work. No corresponding child failure observed. |
| `3Lkm5MsE1rhgvkrWp1U47u0k6ib` | root | ACTIVE; repository configuration/package rollout across thirteen cells, including root. |

The twelve new configuration children all start ACTIVE. Their creation is consistent with the root job's cross-cell assignment; they are not twelve observed failures:

| Cell | Job |
| --- | --- |
| c2j | `L5QmAI2EMRHOtqkmZwLiMUn4fw0` |
| base | `3aKthmcnebnZX6TkrltVtzBWl8k` |
| cortex | `DEtNVnwNGkaHHyCKdwYERNxLqcq` |
| pulse | `ZxUweP1MyuSHlMmroPyCeeynl9L` |
| jobdb | `QDSslDbvjPLKzqf0MUuYeRHBqkw` |
| pgjobdb | `N03FKcIdgwdtILA7srDzE178SUA` |
| shai | `OEb903bZ3COXrP1LOJEBIn4SbMa` |
| c2ops | `7Jdq9aFoKKZ65cGcbfpoFvmWqkl` |
| recipes | `Nnr58Os0KWVbcZHEndBzmwBtIeZ` |
| gitvend | `2pqfqtCM7GUHummYOGOapyJBJGe` |
| cortex-assistant | `14UmO6ESycQVc1ifCCXEHB4WbZP` |
| pulse-tart | `AmszkryfVGkgLpzVtffbMjNQ0Ax` |

**1. The GetForm child has a contradictory assignment and incomplete handoff**

`SVYbGlC2gSzO0r8bUo1bEkBx1tT` is intended to implement a c2j historical-input API needed by Cortex. Its prompt mentions `input.Runtime.GetForm` because that is the existing current-input interface; the reference itself is not evidence of a GetForm execution failure.

The launch prompt combines:

- “This is an execution assignment.”
- The old consultation request: “Design consultation only; do not implement or submit jobs.”
- A new request to implement `input.HistoryService` against `design.md` and `test-statements.md`.
- On its first agent turn, the ordinary design-phase instruction prohibiting implementation.

The launch at parent chapter 27 supplies only `consultation/conversation.json`, `iter1/consultant/agreement.md`, and `iter1/consultant/evidence.md`. The accepted design and subsequent formal test statements are absent. The child attempts to retrieve the parent design through `c2j job artifact`; that fails with `task inspection rejected (400): lease permission denied`.

This is an artifact handoff defect, not evidence that Git access or the proposed HistoryService is broken. `coordinate.yaml` supplies only `agreement.result.final_artifacts` and the conversation when launching an execution. It omits current requester documents, including those produced after consultation.

Both sides then spend consultations trying to deliver documents to an already-running execution. The consultations correctly report that they have no supported operation to add files to that execution's inbox and resume it. Asking a new consultant in the same cell does not address that limitation.

Evidence: parent chapters 24, 27–44; child chapters 16, 20, 22; child chapter 22 `execution-readiness.md`. At 23:59:30 the child progressed with the available agreement, but still reported that the missing formal statements prevented authoritative RI-032–RI-051 mapping.

**2. Recovery directed implementation into a const task**

The same c2j child's chapter 23 reports implemented history APIs and passing focused checks. It publishes a **115,158-byte `implementation.patch`**. However, the task is `resume_read_only_session`, declared `const: true`.

Recorded workspace head before and after this task is the same commit: `483cb48a328ea58fe8c231b8a4e3a1c11bf39422`. There is no resulting Git thin-pack artifact. The implementation patch survives as an artifact; the implementation did not advance the managed candidate.

The cause is visible in the recipes:

- `develop.yaml` recovery sets `assignment: recovery` while retaining the original design phase.
- `agent.yaml` chooses the recovery prompt from the assignment, but chooses read-only behavior from the phase.
- The recovery prompt says to diagnose and correct the problem without retaining the design-phase restriction.

The agent followed the execution/recovery request, but the workflow treated its changes as disposable. A successful implementation report must not be accepted as a durable candidate from this path. Subsequent work may recover the saved patch; this audit does not claim the patch itself was lost.

**3. The Git error is a real gateway route defect; its repair is blocked by expanded acceptance**

Cortex parent `3Lkmx2cuJfjwLkQJWCcvRq3078w`, chapter 42, fails during `go mod download`:

```text
git ls-remote ... https://github.com/colony-2/c2j
remote: unsupported Git route
fatal: repository 'http://192.168.1.195:8082/github/colony-2/c2j/' not found
```

The recorded probes distinguish an extensionless URL failure from a successful equivalent `.git` URL. That supports a gateway URL-routing defect, not a general inability to authenticate to private repositories. The full command log is `_c2j/execution/go-module-verify.log` at parent chapter 42.

Gitvend child `Ml2DvQlSxpW9LgLVMSooNak4PU1` implements the optional-`.git` repair at candidate `5d351088dad925eae6f6f1cdc39614e50f08bc09`. Chapter 29 records all five automatic repository checks passing. Chapter 30's assessment nevertheless requests revision because the running gateway has not adopted the candidate and fresh Cortex verification is missing.

The child was explicitly told not to deploy. Its formal plan nevertheless made live adoption/downstream validation mandatory before acceptance. The human question at chapters 40–43 is now:

> Who operates the gateway at 192.168.1.195:8082, or where can its authoritative fleet, deployed-artifact, and adoption records be read?

The operator question is understandable for deployment work, but it is premature as a gate on this source-repair job. The parent is waiting for the child to finish; the child is demanding running-service adoption and downstream validation before finishing. The code repair, deployment/adoption, and parent retry need distinct completion conditions.

**4. A passing Gitvend hook expanded into a four-job validation chain**

`3LkmsHa9110zYoDvdSpKsO7tyKk` reports that its existing hook already meets the request, and automatic verification passes. Its assessment additionally requires proof that the shared consumer rejects an ordinary failed hook result even when the helper exits zero.

Root's inline consultation explicitly identifies **recipes** as the owner and returns an execution request for recipes. The coordinator nevertheless launches the execution in **root**, because `coordinate.yaml` chooses `agreement.target.cell`, the original consultant's cell. Root then creates the recipes job itself. The extra root job is an orchestration mistake, not a requirement of cell workspaces.

The recipes job runs consumer checks but considers its evidence incomplete because native reports do not expose every internal composite output and transition together. It subsequently launches c2j child `WP1Pq14GIkydOCYzP859iqIIoMa` for an observation bridge. The resulting chain is:

```text
Gitvend hook → root intermediary → recipes validation → c2j test instrumentation
```

There may be useful c2j testing improvements here, but a repository hook request has expanded into proving and extending the shared workflow test infrastructure. No demonstrated consumer acceptance defect is recorded. Reassess the required behavior and sufficient evidence before treating every internal observation as a delivery prerequisite.

The Gitvend parent also returns `next: continue` in **17 consecutive recorded turns**, chapters 40–56, mainly reporting that the same child is still pending. `develop.yaml` automatically awaits known coordinator children for `review`, `outside`, or `blocked`, but not `continue`. The agent is therefore consuming new turns to poll work that the workflow can durably await.

**5. The new configuration children repeat the missing-document pattern**

Root chapter 81 produces `package-matrix.json`, `test-statements.md`, and `validation-plan.md`. Its twelve execution requests refer to formal statements; some explicitly refer to the package matrix or validation plan.

The submitted children receive only their consultant's earlier outputs and conversation. None receives those three current root documents. The c2j configuration child's prompt explicitly says to follow `package-matrix.json`, which is absent from its input document map. Earlier consultant briefs may contain enough information for some children to proceed, but this is the same confirmed handoff defect, now repeated across a batch. Their eventual outcomes are not yet known.

**6. Context truncation causes unnecessary design work**

`classify.yaml` writes full repository context to an artifact, then replaces stdout with empty context and `usable: false` when serialized context exceeds 8,000 bytes. The classifier consumes that stdout, and the recipe requires design whenever it is unusable.

For example, the small Cortex UI job has an 18,038-byte context artifact; the c2j history child has a 41,505-byte artifact. Both pass empty context to classification. This explains some repeated design work even when repository context exists and an execution brief is already supplied.

**Recommended order of correction**

1. Make recovery prompts and workspace behavior consistent. Keep planning recovery within planning, or explicitly transition to implementation before allowing durable code changes. Test actual candidate persistence.
2. Submit a complete, current execution handoff, including referenced requester documents. Use a current execution brief as the task; retain old consultation instructions only as clearly labelled history. Test actual child inbox contents with documents created after consultation.
3. Route agreed execution to the named implementation owner. A consultant's ownership referral must not silently turn into a new job for that consultant.
4. Separate source acceptance from later deployment and downstream verification. Escalate to a human only for the actual next decision; do not ask for deployment inventory to close an undeployed source patch.
5. Allow independent parent work, then use durable child waits when no useful local work remains. Test that a waiting parent does not enter an unbounded sequence of agent polling turns.
6. Preserve useful bounded repository context for classification and recognize supplied execution briefs. Do not let a large README erase all context.

These are specific corrections to the current orchestration, not grounds for replacing the workflow wholesale. Existing deterministic tests cover many transitions, but these observations expose missing cases for late-created handoff documents, owner referrals, recovery persistence outside implementation, and repeated wait-only responses. The expanded acceptance requirements also need prompt/plan review; a passing mocked state-machine test alone cannot establish that generated requirements stayed within the user's requested outcome.

Evidence was read from JobDB job records, chapter inputs/outputs, selected original artifacts, and the corresponding local recipe sources. Chapter numbers above refer to the named current jobs, not their historical restart sources. Raw audit snapshots and selected artifacts are retained locally under `/tmp/current-active-audit/` for this session.

# All-job audit: questions, recovery, and delivery

JobDB: `http://192.168.1.195:9047/c2`. Audit performed November 7, 2026, from approximately 05:21 UTC. Initial census at 05:22:19 UTC; a follow-up census and selected histories were read before writing this report. This was a read-only investigation: no job was answered, restarted, submitted, cancelled, or modified. Recipe code is unchanged.

**The confusing questions mostly come from incorrectly scoped acceptance and recovery decisions, not from agents failing to learn the inspection command syntax.** There are also concrete missed opportunities to retrieve retained files and code. Two examples below identify the actual producer and saved artifacts that the agents asked the human to locate.

This fits recipes ownership for prompts, orchestration, handoffs, review, and tests. c2j owns inspection and managed-workspace runtime behavior. The relevant project cells own their code and deployment outcomes.

## Coverage and census

Both ACTIVE and ARCHIVED stores were queried across all cells and statuses, including hidden/soft-deleted jobs, through the final pagination token. All **184 jobs** returned readable chapter histories. The visible-only query contains 34 jobs; **150 are hidden**. This cannot include physically purged records that JobDB no longer returns.

The follow-up census contains:

| Outcome or state | Count |
| --- | ---: |
| Succeeded | 57 |
| Failed application | 62 |
| Cancelled | 34 |
| Waiting on a human form: READY | 16 |
| Waiting on dependencies: PENDING_JOBS | 14 |
| ACTIVE | 1 |

These combine different recipe versions and both delivery jobs and small validation experiments. They are not a single-version failure rate. Seventy-six jobs were created after midnight UTC, since the preceding audit's final census. Thirty-two jobs resolved recipes commit `de2e9cdc3a113f3c811c3ca998815b0b45adf143`; the follow-up has ten successes, four failures, thirteen READY, four PENDING_JOBS, and one ACTIVE in that group. Some are package helpers rather than adaptive build entrypoints.

I inventoried all histories, **119 generated forms** including historical/answered forms, responses, recorded source versions, and terminal errors. Follow-up concentrated on every outstanding non-merge question, relevant ancestors, and repeated reviews. I retrieved 105 selected review/handoff/evidence documents and additionally checked the specific retained manifests and Git bundle described below. This is not a claim to have independently rerun every job's application tests.

[The companion inventory](AUDIT_ALL_JOBS_2026-11-07_INVENTORY.md) lists every job and every generated form. Raw snapshots and selected artifacts are retained locally under `/tmp/job-audit-20261107T0521/`.

## 1. What happened in QCGloOidC2uYDRDWfASY1akY1Zx

This c2j job is an evidence-collection child of recipes job `V5v6CXnoeBJiChdIZhkVQ5J4NC0`, which is a child of root configuration job `3Lkm5MsE1rhgvkrWp1U47u0k6ib`.

The original root request was to configure each cell's JobDB URL, root repository, and appropriate base packages. Two earlier configuration children failed: JobDB hit the review-selection null-key exception, and Pulse exceeded the serialized payload limit. The recipes child prepared a source correction and reported 66 native cases passing for its source-contract checks. It then made historical recovery evidence a remaining prerequisite, WF-013, and dispatched this c2j investigation.

The current child **does have the new handoff and inspection guidance**. It resolves recipes `de2e9cd`; its runtime header records c2j `v0.0.124-0.20261107020754-03391a60a417+dirty`. This is not simply an old prompt surviving in this child's recipe.

The actual assignment asks for:

1. Exact original review-selection inputs from JobDB job `QDSslDbvjPLKzqf0MUuYeRHBqkw`.
2. The exact complete rejected serialization from Pulse job `ZxUweP1MyuSHlMmroPyCeeynl9L`.
3. Original restart eligibility and which source a continuation would use.
4. Original executable/build provenance and availability of safe compatibility inspection.
5. Non-mutating advice about a failed synthetic fixture whose corrected successors already succeeded.

Crucially, the handoff explicitly permits **“individual evidence or item-specific refusal/unavailability records”**, says to stop at precise unsupported findings, and distinguishes source acceptance from original-job recovery. No source change, restart, deployment, or new execution was requested.

At chapter 14 the agent delivered that report: both resolved recipes were retrieved and hashed; it exhausted 423/968 scope inventories and 40/36 task inventories; unavailable original inputs and serialization were reported precisely. It did not invent missing data or claim the original failures were resolved.

At chapter 29 the assessor nevertheless returned `revise / intervention` because the broader original-behavior verification remained incomplete. Its assessment even says the collection subtask can be recorded as delivered with limitations, while still blocking this collection job. The child had also received the parent's entire WF-001–013 implementation baseline, rather than acceptance statements specific to evidence collection. That conflated the investigator's completion with the parent repair/recovery outcome.

The resulting chain was:

- Chapters 30–38: JobDB consultation, including two response/file corrections.
- Chapter 43: Pulse consultation.
- Chapter 49: pgjobdb consultation.
- Chapter 51: agent reports the unmet need as `blocked`.
- Chapter 53: recipe recovery gives it no new evidence, so it turns the blocker into a human question.
- Chapter 55: form titled **“Identify the original evidence custodian.”**

The question asks who operated `192.168.1.195:9047/c2` around 23:58 UTC November 6 and who holds its deployment/storage/worker records. In ordinary language: **“We could not retrieve some historical internal data. Who else might have it?”** That is why the question seems disconnected from configuring cells.

**Assessment:** the investigation should be able to finish successfully with its permitted unavailability findings while the parent records historical recovery as unresolved. Finishing this bounded investigation does not mark the original product checks passed. The parent should decide whether more historical forensics is necessary for its actual outcome. It should not automatically make the user identify infrastructure custody to accept an unrelated source correction.

Evidence: parent chapter 39 `work/c2j-read-only-verification/handoff.md` and `test-statements.md`; child chapters 14, 29, 30, 43, 49, 51, 53, and 55. The parent's baseline even describes WF-013 in terms of supported metadata and negative fixtures, not proof that every original record can be recovered.

## 2. The allegedly missing immutable commit is retained

JobDB recovery job `RCQZ9XvZ5WXUQiATrHE2FWJy6B6` asked you to locate commit `de0a367fde0d9d46045c79eab8f32a2162024e7e` and its producer. At chapter 47 you answered: **“you're asking me to do something you should do. if you can't, fail”.**

I found its producer in the already-recorded ancestor chain:

| Item | Verified location |
| --- | --- |
| Producer job | `Xmo8HrJaS8wszYpQ30Ogo48QUQy`, cell `jobdb` |
| Producing chapter | 24, implementation work occurrence 6, attempt 1 |
| Workspace scope | `a402c3465b3d1404ec2a7454915b3ef24a9d584ad587a503e8327e0b2cba5170` |
| Recorded output head | `de0a367fde0d9d46045c79eab8f32a2162024e7e` |
| Base | `f92ae253a5da7a6b81944d0bdf4cadb085772140` |
| Retained artifact | `__git_state_thin_pack__`, 82,816 bytes |

The supported `c2j job snapshot` metadata call identifies this workspace as available and names that bundle. I downloaded the original bundle; `git bundle list-heads` reports the exact requested commit as `HEAD`. This establishes a retained producer/export, not publication to the canonical repository or completion of downstream module validation. I did not apply, publish, or execute that candidate.

The delivery problem is that an **unpublished managed commit** was treated as if consumers could already fetch it from the normal Git/Go module route. The producer's chapter 26 requested pgjobdb implementation against that commit before publication. The descendant handoff then demanded successful exact Git fetch and clean module resolution while forbidding publication/substitution. An additional JobDB recovery child was created to find the original source, although the ancestor had it.

The lineage is `Xmo8…` → pgjobdb `CIkfEMSNyA4ojSb9lLB1fAKM0Fz` → recovery `RCQZ…`. After RCQZ failed, **CIkf now asks the same question** in chapter 65, “Locate the required immutable JobDB source.” Its latest question is answerable from the producer above.

**Correction:** carry the producer job/task/workspace reference when handing off unpublished code, and use selected snapshots/patches for validation where appropriate. When the required outcome is normal remote module resolution, order source publication before that consumer gate. Retrieving a bundle alone does not satisfy publication. Do not commission another owner-discovery job or ask the human for a commit location already in the ancestor history.

## 3. A child asks for documents its parent still has

`BK0QNKp2JRWBvI8609SZQ9UXCbP` has asked three times for retained recovery inputs. You twice directed it to job inspection. It successfully inspected its own log/snapshot but concluded the corrected assignment and manifest were missing.

They are retained in its parent `14UmO6ESycQVc1ifCCXEHB4WbZP`, chapter 65:

- `recovery-execution.md`, 3,552 bytes.
- `delivery-manifest.json`, 3,357 bytes.
- **All 21 files listed in that manifest**, including the harness source, instrumentation diff, mismatch/stack logs, original statements, fixture setup, and module files.

I downloaded those 21 files through the recorded artifact endpoint and verified every declared byte count and SHA-256 digest. The assignment is explicitly source-only; the absent private runtime checkpoint is a separate prerequisite for later execution, not for inspecting these source files.

The child's submitted input map contains only the older consultation output and transcript. Its parent still runs the older `a3fea1f` coordinator, which omitted newly prepared requester files. Starting a child on `de2e9cd` did not repair the parent's old submission logic. The same old-parent/new-child issue affects failed Base recovery `HLEhX7fl9m6up5SqNoRzo1Urotg`; its supposedly missing request and manifest are retained in root chapters 225 and 230/232.

There is also a stale permission assertion. BK0's latest review says its authority excludes its parent. The shared prompt/playbook currently hard-code that restriction, but completed c2j job `10b14040-1454-4f6f-b446-852bec151a1d` changed inspection to follow existing JobDB read permissions. Later observed workers are on `03391a60…`; BK0 initially used the older worker and later resumed under newer code. Our instructions should not preserve the old restriction as a universal rule.

**Correction:** use the actual task's supported permission report and attempted read, follow the known producer reference, and retrieve only the selected files. If the task cannot read its parent, return that exact unmet input to the parent/controller, which can bind the files into a fresh handoff. Do not ask the human to establish whether files exist when the submitting agent still holds them. These audit reads used operator access; they prove retention, not every task token's permission.

## 4. “Fail if you cannot proceed” becomes repeated recovery

RCQZ did follow your direction at the agent level. Starting at chapter 49 it repeatedly returned `next: blocked` and said the execution failed, no new inputs existed, and no further question or unchanged retry was requested. The recipe has no explicit terminal-failure choice in this response contract. `blocked` without a package or pending child routes to `recover_work`.

The recovery counter only increments when the summary text is **byte-identical**, the candidate is unchanged, and work turns are consecutive. Paraphrasing the same blocker resets it. Blocked turns are excluded from the implementation-turn cap. RCQZ therefore made **12 agent turns after your instruction**, chapters 49 through 68, before failing at 05:23:08 UTC. The final four identical summaries finally satisfied the guard. The code and candidate were unchanged.

This is not an agent refusing to obey. It is an inadequate terminal outcome and a fragile progress guard. Its parent subsequently repeated the locate-source question, compounding the failure.

A historical related issue remains in the current failure exporter: `operational-failure.yaml` binds `./` documents and an explicit `recovery.md`. If the selected documents already contain `recovery.md`, artifact binding can fail before the intended diagnostic is exported. Job `LxoKYzYNcioweEKVI0uaFlj8l2f` records that collision.

**Correction:** provide an unambiguous terminal failure outcome that preserves evidence and returns control to the parent. Bound consecutive unsuccessful recovery turns using observed outcomes, not prose equality. A changed explanation is not evidence of progress. Make failure-artifact binding collision-safe. Preserve the ability to continue when a real repair or newly supplied prerequisite makes progress possible.

## 5. Generated plans become harder constraints than the user's request

The older configuration chain has grown into implementation of persistent job-input lifecycle APIs, storage fencing, historical replay, and exact executable recovery. Some of that work may be useful; it is not all a prerequisite to setting package defaults.

Examples:

- Root's simple configuration request has 44 frozen outcomes. The serving lifecycle branch has 59 formal expectations and a growing multi-cell implementation. Recovery repeatedly preserves all prior plan additions instead of reconsidering whether they belong to the user's outcome.
- pgjobdb job `N03FKcIdgwdtILA7srDzE178SUA` received your chapter-73 instruction to **focus on Linux arm64 tests**. Its chapter-86 assessment still cites missing native AMD64/macOS evidence as blockers. Docker may be a real prerequisite for the chosen smoke test, but a proposed validation plan must not silently outrank the user's narrowed scope.
- Both N03 and its root parent now ask for a Docker/BuildKit endpoint. That duplicates one underlying unmet capability at two levels.
- c2j verify-hook job `57cdc919-c9d7-47dd-8718-a0b4c73e9262` had Go 1.26.8 available, but its generated acceptance required exactly 1.26.1. It requested tool approval twice, the second time for a corrected probe of the same package. The original request said to use GitHub Actions as inspiration; it did not require that exact patch version.

The new root verify-hook job `23a69302-e319-4813-b7a8-5cf73928f7fa` explicitly excludes Docker/other architectures for now, and its new children generally respect those holds. Do not conflate that healthier new chain with the older configuration chain.

**Correction:** distinguish user requirements, generated implementation choices, and optional validation. Human scope corrections supersede generated plans; updating an overreaching test plan is not automatically deprecating shipped behavior. Prefer adequate existing tools unless a specific compatibility requirement justifies replacement. Use the existing package-policy mechanism for agreed automatic approvals; genuine new tools without such policy still correctly require review. Consolidate an environmental request at the coordinating level.

## 6. The current forms mix legitimate approvals with avoidable questions

At follow-up, the 16 outstanding forms comprise **ten merge decisions and six operational/evidence questions**:

| Job | Question now shown | Assessment |
| --- | --- | --- |
| `QCGloOidC2uYDRDWfASY1akY1Zx` | Original evidence custodian | Evidence collection completed with permitted limitations; assessment is blocking on the parent's broader recovery outcome. |
| `CIkfEMSNyA4ojSb9lLB1fAKM0Fz` | Location of immutable JobDB source | Producer and bundle found above; return that reference through the coordinator. |
| `BK0QNKp2JRWBvI8609SZQ9UXCbP` | Whether correction evidence was retained | Parent's assignment and 21 manifest files are retained and verified. |
| `6JEK7yzNVsHTlsp9VWpHAqQvE6D` | Administrator/inventory for the JobDB listener | Historical exporter has expanded into proving deployment custody. It should return supported evidence and precise limits; larger investigation is a separate choice. |
| `N03FKcIdgwdtILA7srDzE178SUA` | Docker connection and smoke endpoint | Real execution capability may be absent, but reassess the config task's scope and honor Linux-arm64 narrowing. |
| `3Lkm5MsE1rhgvkrWp1U47u0k6ib` | Existing Docker/BuildKit worker for pgjobdb | Same underlying unmet capability as its child; avoid duplicate human requests. |

The ten merge reviews cover four verify-hook candidates (base, shai, Pulse, pulse-tart), the managed-hook restore fix, canonical lease events, and four Cortex UI changes. Their decision controls are clear: “Merge these changes?” / “Request changes.” Those gates should not be removed simply to reduce the count.

However, the prose still often leads with hashes, “source acceptance,” or internal artifact-routing language. In `8kIVSQou7k1PUkcHqK97fMyZ7nB`, you explicitly requested a plain-English explanation because the review sounded like old-job restoration. The needed explanation was: **a fresh validation job could not load the selected saved code for its hook; the fix lets it read that exact input while still executing as a new job.** The agent provided that explanation after your feedback. It should have been the opening explanation.

Repeated approvals also need clear context. Cortex goal-column job `8ac558fe-5679-471f-8cc3-f8a103668606` was approved at chapter 104, then rebased after the target advanced and returned for review at 139. Cancellation-message job `cdc5c269-4c35-471d-8377-34a715e8aafa` was approved at 111 and later returned at 152 after reconciliation with relationship tests. These are recorded candidate changes, not lost answers. Explain immediately why approval is being requested again and whether product behavior changed. Changing the approval policy for equivalent rebases is a separate decision; this audit does not authorize bypassing review.

## 7. Actual runtime and historical recipe failures

The all-job inventory includes genuine defects in addition to unproductive questions:

- Four recorded `hook workspace restore artifact missing` failures in small validation jobs. c2j repair `8kIV…` addresses this and is awaiting merge review. Reuse that existing work.
- Eight submission-schema failures across older jobs and custom experiments, including undeclared `title`/`prompt` and schema-v1 `object` misuse. Several latest examples are ad hoc validation recipes, not the shared adaptive build rejecting `title` again.
- Six historical review null-key failures. The current source-ID guard addresses one verified class; no new `de2e9cd` example of that exception was observed in this census.
- Eighteen terminal `stop_attempt`-reported failures including RCQZ's follow-up. This label is a failure-reporting node; inspect its reason rather than treating all eighteen as one tool problem.
- Older oversized-payload and private Git routing failures remain in history. The recipes transport correction in `V5v6…` is already implemented and tested in that job's candidate; it is blocked on the investigation chain above. Do not start another transport rewrite before assessing that existing candidate.

Among the four failures resolving the current recipe source, two are children of old coordinators with missing delivery (`HLEh…`, `0sIi…`), one is a package validation probe (`G9VF…`), and one is RCQZ's final unrecoverable-source disposition. This matters when deciding what tuning has actually regressed.

## Recommended next changes

| Priority | Concrete change | Owner and useful verification |
| --- | --- | --- |
| P0 | Let an agent return terminal failure directly; stop repeated recovery without new evidence. | Recipes. Test varied summaries for the same unresolved attempt, terminal failure propagation, retained evidence, and parent receipt. |
| P0 | Review each child against its own assigned deliverable; findings/unavailability can complete an investigation without completing the investigated product. | Recipes prompts and handoffs. Separate child acceptance statements from reference-only parent expectations. |
| P0 | Repair the two concrete deliveries using known producer references: BK0's parent chapter 65 and RCQZ/CIkf's producer chapter 24. | Coordinating jobs. Select needed files or a snapshot/patch; do not pass every historical document or silently publish the commit. |
| P1 | Order canonical dependency publication before consumer checks that require remote module resolution; otherwise explicitly supply unpublished code for bounded validation. | Recipes coordination and producer/consumer cells. Verify an unpublished candidate can be consumed through the intended transport. |
| P1 | Remove hard-coded own-job/direct-child inspection limits; rely on the current permission contract and actual read results. | Recipes, aligned with the completed c2j inspection fix. Update new-session context and focused recovery guidance; do not assume old sessions absorbed new instructions. |
| P1 | Route missing internal inputs back to the producer/coordinator before human questions; consolidate environmental requests. | Recipes. Human questions should identify an actual user decision or information the system cannot obtain. |
| P1 | Allow explicit user scope corrections to update an overreaching generated validation plan; avoid unnecessary exact tool patch requirements. | Recipes prompts/plan routing and cell package policies. Preserve actual product expectations, not every earlier proposed procedure. |
| P1 | Make failure output binding safe when selected files already contain `recovery.md`. | Recipes. One native negative case should preserve the original failure and all selected evidence. |
| P2 | Lead reviews with user-visible outcome, why this decision is needed now, and what changed since prior approval. Put hashes and implementation mechanics in supporting evidence. | Recipes review prompts; project-specific summaries should explain the actual feature. |

The immediate opportunity is to finish or fail the bounded jobs correctly and give the parent the evidence needed to choose the next useful action. The new handoff selection, isolated phases, durable waits, inspection commands, and ordinary merge gates are working in several new chains. These findings call for specific corrections to completion, delivery, and review scope, not another wholesale workflow replacement.

## What the existing tests missed

The prior 289 adaptive cases and focused inspection tests establish selected-file transport, task-field retrieval, snapshots, phase persistence, explicit waiting, and a number of exact-repeat recovery paths. They do not establish that a prose-based repeat counter recognizes semantically identical blockers, that a human's requested failure reaches a terminal branch, or that older submitting recipes deliver late-created files to a newer child recipe. The permission model also changed after the runtime pinned for those tests.

Add deterministic contract cases for those execution boundaries. Treat the investigation-versus-parent-acceptance mismatch and overly technical review language as prompt/scope corrections, with production audits of their outcomes. A mocked agent response cannot prove that an LLM will always write a clear review or choose an appropriate acceptance scope.

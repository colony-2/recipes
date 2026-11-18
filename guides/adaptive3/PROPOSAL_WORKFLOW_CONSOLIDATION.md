# Adaptive3 workflow consolidation

Keep the existing human Direction and Outcome decisions. Use two continuing author sessions for the local work, one independent assessment for each distinct review decision, and native operations for Git, file checks, and verification. A failed output check should go straight back to its author. Rebase onto the latest upstream before managed verification. Send rebase repairs and verification failures straight to the implementer with the original evidence. A successful merge should complete from its recorded result and any required publication work.

## What the jobs show

The effective history of c2j job `3MFtT9O165Y2JtWM9CCvZYuGF5J` contains 156 task occurrences and 49 Codex invocations, including inherited work and inline consultations. Forty invocations started sessions and nine resumed them. These counts exclude child job internals and count operation calls rather than individual model requests. The job completed successfully. It contains several different reasons for returning to work, so the phase name alone is a poor guide to which work was repeated unnecessarily.

| Evidence in the c2j job | What should change |
| --- | --- |
| At 64–65, Preparation validation passed and a second agent accepted the same plan. At 132–133 and 158–159, Implementation followed the same pattern. Inline owner advice has similar pairs, including 82–83. | Turn a passing independent assessment into acceptance in recipe logic wherever the decision is automatic. |
| At 107–109, module verification failed and a separate assessor restated the failure while also finding a real inherited-wait defect. At 119–121, managed checks had passed, but independent assessment identified a missing acceptance case and the implementer added tests. | Send the existing verification failure directly to the implementer. Keep independent assessment once checks pass so it can still find defects and gaps that the tests miss. Verification of the subsequent code and test changes was justified. |
| At 145, the merge hit an advanced target branch. A fresh worker at 146 reconciled overlapping grouping and metrics changes and ran a full integration suite. The native rebase at 147 was followed by another managed integration run at 155. The approval comparison at 164 could not establish equivalence. | Try native rebase first and resume the existing implementer for a conflict. Verify the prepared candidate. If the normalized diff matches the approved change, retry the merge with the original approval. |
| At 172, the merge succeeded. The final publication result says no publish hook was configured. At 175–177 the recipe still checked the accepted files, started a validator, and started an acceptance agent. The two Codex calls took about 4 minutes 16 seconds and reported no new finding. | Complete from the native merge receipt and skipped publication result. |

The reference audit is `review/inventory.md` from recipes job `3MFo2XBxI3vGsGe9deOtnUvm2He`, producer ordinal 50. It tracks **15 sessions across 17 invocations** in an earlier JobDB example. Its proposed merges of advice, preparation, and implementation acceptance into their validators are the starting point here. This proposal also selects its two authoring combinations, Direction with Preparation and Implementation with Outcome. Those reuse context across a phase transition and can still require a new turn. The audit's large token totals accumulate overlapping model requests within a session, so they cannot measure how much context was rebuilt or how much this change would save.

The JobDB example has a clear unchanged-work case. At ordinals 73–74 on `3MFnX75xovVhqhwaFmLdSIOBrW2`, the assessor asked for an Outcome accounting file during Implementation. The worker added only that artifact and the recipe spent about 10½ minutes rerunning passing checks. The phase-scoping fix already landed in recipes commit `6599c98`, delivered by job `3MFpyyGz9ky9ovQTrzgB0eqMPTY`. Preserve its coverage. The remaining problem is that the recipe repeats work after a correction even when the inputs to that work have stayed the same.

## Proposed flow

| Phase | Who does the work | What advances it |
| --- | --- | --- |
| Direction | Planning session writes the proposal and handles revisions. | Output checks, one independent assessment, then human approval. |
| Preparation | Resume the planning session with the approved scope to produce the plan and test statements. | Output checks and one independent assessment. A pass advances automatically. |
| Implementation | Core implementer writes and repairs the candidate. Keep its checkpoint after the phase completes. | Output checks, native rebase onto the latest upstream, preparation, required verification, then one independent assessment. A pass advances automatically. |
| Outcome | Resume the core implementer in a read-only repository operation to write the human review from current evidence. | Output checks, Git measurements and approval comparison, and one independent assessment of the report and any new facts. Then human approval or recorded reuse of an applicable approval. |
| Integration | Native merge and any configured publication hook. On upstream advancement, reuse the rebase and verification steps. | Matching normalized changes carry the original approval into a merge retry. The recorded merge and publication result satisfy the integration contract. |

Inline owner advice follows the same output-check and single-assessment pattern. Keep separate owner sessions and required specialists. Reject a consultation to the current workspace cell before opening a recipient session. The requester retains its checkpoint and handles the local work. An explicit, separately scoped same-cell child assignment can use direct submission. Preserve human questions, revisions, and explicit stage choices. A distinct independent assessment has a distinct job to do. For example, Outcome should reconcile the report with the actual diff, owner dependencies, and verified candidate. It can rely on an applicable Implementation assessment for code already assessed. The author never accepts its own work.

### Bound session starts per job

The normal build path uses at most **three Codex sessions**, excluding consultations. Open each session on first use and resume it whenever its role runs again.

| Sessions | Role |
| --- | --- |
| 1 | Planning author for Direction and Preparation |
| 1 | Core implementer for Implementation, Outcome drafting, and repairs |
| 1 | Independent read-only assessor for Direction, Preparation, Implementation, and Outcome |

File checks, managed verification, automatic acceptance, and ordinary integration use native results. An explicit publication assessment uses the same assessor. Human questions use the current phase's author and revision routing uses the same assessor when judgment is needed. A revision, failed check, or rebase can add turns, but re-entering a role resumes its last successful checkpoint. Each turn receives the current candidate, evidence, and decision. Prior conversation supplies context for a new assessment.

Backstop and package management can each open one additional session on demand. Backstop retains its checkpoint across visits. Package proposal and approved adoption share a checkpoint, with each operation's permissions applied separately. That gives a per-job maximum of **five shared recipe sessions**, counting both optional services. Configured specialist consultations have one checkpoint per configured request key and are outside that count, as are other consultations. Separate child jobs and project hooks have their own execution scope. [Backstop](../../recipes/adaptive3/backstop.yaml) · [Package management](../../recipes/adaptive3/packages.yaml) · [Specialists](../../recipes/adaptive3/specialists.yaml)

Preserve checkpoints when leaving a phase or service and on failed invocations. If a role's checkpoint was lost or is incompatible, report the recovery requirement. A continuation that needs a fresh session can start in a new job. This keeps the per-job limit independent of how many times a phase or service runs.

### Keep each decision in one place

Use short phase sequences that call existing includes. Give each shared step one job. The output check validates a producer's packet. Rebase returns the current candidate or repair evidence. Verification returns the check result and logs. Approval comparison answers whether the prepared candidate carries the approved change. Merge and publication consume those results. Keep each decision next to the step that supplies its evidence and route on that result once. Implementation and merge recovery call the same rebase, prepare, and verify steps. Merge recovery adds the approval comparison at its own decision point.

Pass the candidate and base, worker checkpoint, approval receipt and patch, and selected evidence through existing inputs and outputs. Keep hook resolution inside the hook include. Use short transitions at the actual decision points, such as sending a failed check to repair or an unproven approval match to Outcome. This keeps common paths readable and limits phase conditions to the caller that selects the sequence. [Cycle](../../recipes/adaptive3/cycle.yaml) · [Lifecycle](../../recipes/adaptive3/lifecycle.yaml)

### Check the output before spending time on validation

Make the cheap, deterministic checks a blocking gate. Check the response schema, required fields and artifacts, selected review files, links, and document metadata before starting the verification hook, specialists, or independent assessment. The current `files` state runs early, but routes onwards regardless of its result. Findings are collected after the expensive work has run. A missing file or invalid response should stop that pass at the gate. Check generated outputs after a step changes them when necessary. [Validation flow](../../recipes/adaptive3/validate.yaml)

Send the exact schema or file findings to the session that produced the output and recheck its correction first. Use existing bounded schema repair and the last usable checkpoint. If a tool, permission, or storage failure prevents the check itself, carry that failure and its diagnostics through the normal recovery path. Keep the existing phase contracts, including Outcome-only Git measurements.

### Rebase before managed verification

After the output checks pass, resolve and pin the latest tip of the target branch. Run native rebase before preparation and any managed verify hook invocation, including the first pass and every retry. An already current candidate passes this gate without replay. Preparation and verification use the resulting managed candidate. Use the same gate after an upstream-advancement merge error, since the target can move again after verification. [Merge and chase routing](../../adaptive3.yaml) · [Git operations](../../recipes/adaptive3/integration.yaml)

When native rebase fails and the managed candidate is safe to repair, resume the original implementer with the failure, pinned target, and available diagnostics. Give the implementer one instruction. “Reconcile the saved candidate changes on the latest upstream in this workspace. Resolve conflicts and persist the result.” After a supported conflict, native replay has already aborted. On the pinned runtime, the existing recovery flow saves the complete candidate patch and aligns the managed workspace to the target. The implementer reconciles the saved changes there. Return through the rebase gate before verification so a newer upstream tip is picked up. Keep the existing repair and merge retry bounds. Failures that prevent safe restoration or repair keep their native recovery path.

### Reuse approval when the rebased diff matches

Keep the human approval receipt and the exact patch it approved. After an approved merge fails because upstream advanced, rebase and prepare the candidate, verify it afresh, and compare the prepared change with the approved patch. Use the existing Git comparison as the basis for normalization. Apply the approved patch to the new base in a temporary index and compare that tree with the current prepared tree. This compares both changes on the same base and preserves paths, file modes, binary contents, and meaningful whitespace. Bind the comparison and fresh verification to the candidate that will be merged. [Git comparison](../../recipes/adaptive3/tools.yaml#L144) · [Existing approval reuse](../../recipes/adaptive3/review.yaml#L164)

If fresh verification passes and the normalized changes match, retry the merge with the original approval. This path goes directly to merge after the checks pass. If the diff changed or the comparison cannot prove a match, use normal candidate validation and Outcome review for a new human decision. A verification failure returns to the implementer, and any repair goes through comparison again before merge. Keep the original receipt tied to its approved patch across retries. Record which rebased candidate reused it.

### Send verification failures to the implementer and reuse passes when they still apply

When required verification fails, route the hook status, failing check, and original log references straight to the core implementer. Hook load and execution failures should carry their native error and diagnostics. The implementer can inspect the evidence, fix the problem, and run targeted checks. The managed hook remains the source of required full verification. A mechanical hook summary can remain useful alongside the logs. A general assessment or separate model summary adds another turn before the worker can act. Required verification that is absent or skipped still needs correction. [Hook contract](../BUILD_HOOKS_USER_GUIDE.md)

For a correction limited to a report or artifact, rerun its output checks and any assessment affected by the correction. After confirming that upstream is current, reuse a passing verification result within the same job only when the recipe can establish that it applies to the same prepared repository snapshot, base, effective hook, and verification inputs and requirements. Documents and configuration can be hook inputs. A changed relevant binding, candidate, base, verification requirement, or unproven match requires fresh checks. Use retained native results and artifact references for the comparison and record which pass was reused. Keep the first required verification on an unchanged delivery. A failed check must pass before completion, including when a transient failure is retried against the same candidate.

### Keep the original implementer available for recovery

Pass the full last successful worker checkpoint across the lifecycle boundary. Direction and Preparation can share a checkpoint after Direction approval. Implementation and Outcome can share one because the phase prompt and current operation define what each turn can do. Start with phase-neutral persistent instructions and send the current scope, approval, task, paths, and evidence in each turn. Retained developer instructions survive a resume. Restore Git and enforce writable or read-only behavior separately from session reuse. Preserve the last successful checkpoint on failure and surface a specific recovery reason if a checkpoint is unavailable or its instructions are incompatible. Keep each owner and reviewer on its own session, and give scope changes their normal Direction decision. [Agent routing](../../recipes/adaptive3/agent.yaml) · [Lifecycle](../../recipes/adaptive3/lifecycle.yaml)

### Complete integration from its actual result

After a successful merge, resolve publication for the merged commit. When the runtime reports an absent hook and there is no explicit publication requirement, complete with the merged hash and skipped status. The review files and verified candidate already passed Outcome. When a configured hook runs, use its structured result and retained evidence to satisfy publication. Scope any required independent assessment to new publication evidence. On publication failure, preserve the merge receipt and retry or recover publication against that same commit. [Integration execution](../../recipes/adaptive3/execute.yaml) · [Publish hook](../../recipes/adaptive3/hooks.yaml)

## Implementation sequence and acceptance

This fits the **recipes** cell. Recipes owns the phase and session routing, prompts, and workflow tests. c2j owns Git replay, snapshot identity, and persisted execution contracts. c2ops owns the Codex adapter and checkpoint import. Project cells own the meaning and requirements of their hooks. Use the existing contracts described in the reference audit and confirm support on the pinned runtime, particularly conflict recovery and fresh-worker session restore.

1. **Remove redundant work at known decisions.** Make output checks blocking, route failed verification directly, map a passed independent assessment to autonomous acceptance, and finalize successful no-hook merges from their receipts. Keep specialist and human gates in the cases that require them.
2. **Carry checkpoints across phase and service visits.** Resume each author and assessor on re-entry. Reuse those checkpoints for human feedback and send genuine repairs to the candidate's implementer. Keep separate authorization, workspace, and evidence bindings for each operation.
3. **Share the rebase and verification path.** Use the native latest-upstream gate on initial and repeat passes. Resume the implementer with the short rebase prompt when repair is needed. In merge recovery, use the Git comparison to choose between verify and merge with the existing approval or the normal Outcome review. Reuse matching verification evidence for corrections that leave every relevant input unchanged and the base current.

Use the native Adaptive3 suites to test the following workflow outcomes. Dependencies for each integration statement are the pinned c2j and normal test harness. Session and Git cases need retained objects and disposable Git workspaces. The filenames identify the expected starting suites.

| Priority and type | Test statement | Suites |
| --- | --- | --- |
| Critical · Integration | A malformed response or incomplete review packet returns to its author before repository verification or independent assessment starts. | `cycle.test.yaml`, `reporting.test.yaml` |
| Critical · Integration | Failed required verification reaches the original implementer with its diagnostics and blocks acceptance until the required checks pass. | `hook-recovery.test.yaml`, `lifecycle.test.yaml` |
| Critical · Integration | A report-only correction reuses applicable passing verification. Changed code, base, hook inputs, or unverifiable evidence triggers fresh checks. | `cycle.test.yaml`, `lifecycle.test.yaml` |
| High · Integration | Autonomous phases accept one passing independent assessment. Required specialist failures and pending human decisions block advancement. | `review.test.yaml`, `consultation.test.yaml` |
| High · Integration | Planning and implementation authors resume across their phase boundaries without acquiring new permissions from the checkpoint. Independent assessors use separate sessions. | `lifecycle.test.yaml`, `reuse-permissions.test.yaml` |
| Critical · Integration | Repeated phase visits, human questions, and revisions reuse their designated checkpoints. A standard build starts at most three sessions. | `lifecycle.test.yaml`, `review.test.yaml`, `discussion-context.test.yaml` |
| High · Integration | Repeated Backstop and package visits each use one session. An unavailable checkpoint reaches recovery without a fresh session in the same job. | `backstop-actions.test.yaml`, `package-routing.test.yaml`, `lifecycle.test.yaml` |
| Critical · Integration | Initial and repeat verification run on a candidate prepared after rebasing onto the latest upstream. An already current candidate advances without replay. | `integration.test.yaml`, `lifecycle.test.yaml` |
| Critical · Integration | A failed rebase returns to the original implementer with the target and diagnostics before verification can run. | `integration.test.yaml`, `lifecycle.test.yaml` |
| Critical · Integration | After upstream advancement, a matching normalized diff and fresh passing verification permit merge with the original approval and no further review. | `integration.test.yaml`, `lifecycle.test.yaml` |
| Critical · Integration | Changes to approved contents, binaries, or modes and unproven comparisons require fresh human approval. Failed verification blocks the merge retry. | `integration.test.yaml`, `hook-recovery.test.yaml` |
| Critical · Integration | A no-hook merge completes without further assessment. Failed publication retains the merged commit and retries publication without repeating the merge. | `integration.test.yaml`, `backstop-publication.test.yaml` |

Observe later jobs on the revised recipe. Count fresh and resumed author calls, redundant acceptance calls, verify-hook runs by evidence identity, preflight failures that reached expensive steps, clean rebases that used an agent, and post-merge calls on the no-hook path. Compare by path and recipe revision. Scripted responses establish routing and invocation counts. Assess live judgment and elapsed work separately. [Native testing guide](../NATIVE_RECIPE_TESTING.md)

Evidence was read from `http://192.168.1.195:9047/c2`. The c2j job used recipes revision `a50133564379bbb47700641a928b0b842a2ddb21`. The inspection CLI could not decode some later task outputs using the newer stored envelope. The post-merge findings use the final merge and publication result, task history, and the two retained Codex transcripts. The recovery finding uses the merge error, retained worker transcript, candidate verification report, and approval-comparison logs. The two supplied jobs and the prior JobDB finding describe behavior before these changes. The local implementation uses the pinned c2j runtime and the focused native cases listed above. Production job savings still need measurement on new runs.

# Adapting Adaptive3 in place

Start with one change at the existing Preparation review. Put the requested outcome on the approval screen and give the implementer room to correct a designer’s assumptions. Keep the session split and review frequency steady for this trial. Then shorten the repair loop. Change session count only after measuring those effects. The recent commits identify which checks to keep when removing a step. [Design principles](../../adaptive3/PRINCIPLES.md) · [Lessons from 40 commits](#lessons-from-40-commits)

The cohort gives us two cases to replay. A proposed goal reservation grew into its own assignment. Separately, 38 recorded trips sent work from Implementation to Backstop and straight back. The counter change at `6b5a701c` already renews allowances after verified progress or a new instruction. Measure that revision on fresh jobs before attributing a repair improvement to further changes. [Cohort and revisions](inventory.md) · [Retry policy](../../../recipes/adaptive3/retry.yaml)

## 1. Make clear what approval commits us to

Preparation asks the designer for “evidence required.” Full plan approval refers to “these criteria.” Outcome then asks the assessor to check every applicable criterion against the frozen plan. The file check enforces packet structure. The assessor interprets the prose, and a `revise_plan` judgment routes work to Preparation. This is where a speculative test can cost another round of design and human review. [Preparation and Outcome prompts](../../../recipes/adaptive3/prompts/execute.yaml) · [Review question](../../../recipes/adaptive3/prompts/review.yaml) · [Assessment prompt](../../../recipes/adaptive3/prompts/validate.yaml) · [Validation routing](../../../recipes/adaptive3/validate.yaml)

| Where to change Adaptive3 | Proposed change |
|---|---|
| Preparation and its review question | Show “What should work” and any exact method the requester or cell requires. Put the designer’s test ideas under “How we could check it.” Use the existing files, including `review/acceptance.md`, and keep the approval receipt. |
| Implementation and Outcome | Let the author replace a proposed check with equivalent evidence, or retire a newly invented obligation after checking its source. Record one sentence explaining a consequential difference. Compare with the original approval. Preserve missing evidence as missing. |
| Assessment and routing | Ask “Which promised behavior is missing or broken?” A changed test method with equivalent coverage can qualify for `covered` under an applicable full approval. A defect gets repaired. A material change to the promise reopens the plan. If an earlier approval leaves a consequential choice unclear, use the existing human review. |
| Cell instructions | Clarify that the deprecation rule protects established behavior and its published test statements. A current designer’s draft example can be corrected during the job. Apply the same distinction to recovery prompts so it survives a handoff. |

Reserve “acceptance criteria” for conditions someone has actually made binding. Use ordinary questions in default prompts. A renamed heading alone leaves the same review decision. The audit shows scope drift but does not establish a causal effect from those two words. [Themes](audit.md) · [Cell test-statement rules](../../../AGENTS.md#test-statements) · [Coverage decision](../../../recipes/adaptive3/cycle.yaml)

**Replay the same request three ways.** A designer specifies a new reservation. The existing dependency demonstrably delivers the wait, so the reviewer can accept the evidence. A second candidate starts the dependent job early, so it goes back for repair. In the third case the requester explicitly requires a named verification method and the author omits it, so the reviewer keeps it open. Exercise the real routing with scripted outcomes, then sample fresh author and reviewer decisions to see whether they make the distinction. Count avoidable returns to Preparation alongside missed defects. [Build regressions](../../../recipe-tests/adaptive3/build.test.yaml)

At each handoff, display the originating request, the latest applicable human decision with its native receipt, and the worker’s proposed approach as separate items. Keep them short. Link to the source job/task or review for exact text. The existing human response, approval, parent reference and assignment are sufficient for a first version. If the origin is unknown, say so once. A child may trust its parent to delegate ordinary work while still challenging an expensive prerequisite. A person’s approval of a plan applies to its recorded scope. An agent’s interpretation can be corrected.

For the JobDB bridge example, the handoff should have read:

> **Requested outcome** — When I create a job, let it wait for an existing job ID.
>
> **Parent’s proposal** — Reserve a goal so a particular receiver can complete it.
>
> **Question for JobDB** — Can the existing dependency or receiver contract do this? If a change is needed, identify the smallest one and the evidence for it.

Change the consultation prompt to answer “How can I do this today?” Finish there. Only the requester can open negotiation with a specific change it wants. The receiver can make an offer or decline. Delivery needs agreement from both. [Consultation prompt](../../../recipes/adaptive3/prompts/consultation.yaml) · [Coordination](../../../recipes/adaptive3/consultation.yaml)

The receiving cell could have answered with the existing capability, identified a receiver bug, or justified a delivery. Only a consequential new choice needs the human. When a later human changes scope, carry the exact instruction and supersede the conflicting agent assumption once. Do not reopen already settled unrelated decisions. Test an agent-authored request claiming “the human requires X,” an actual human receipt narrowing X, and a legitimate delegated prerequisite that can proceed without another approval. [Child brief and assessment history](http://db.lab.c2.run:8081/c2/jobs/FSfzVHCD63fKGZDNpNzKNebE57G) · [Existing review fields](../../../recipes/adaptive3/review.yaml)

## 2. Give repair to the worker that can do it

Recipes should implement one ordinary phase cycle. The worker gets the assignment and current evidence, acts, and reports the result or the next concrete need. Deterministic checks run at the earliest point when their inputs are settled. Each phase uses the following few decisions.

| What just happened | Who acts next |
|---|---|
| A check failed and there is a specific authorized repair | The worker with the writable candidate gets the failing check, its diagnostics and the last passing evidence. It repairs locally. |
| An assessor found a defect in the candidate or its planned behavior | The phase owner receives the finding, its source and the consequence. The independent assessor can withdraw it when the premise is wrong. |
| Only reviewer-facing material changed | Its author fixes it. Recheck the material and links. Reuse verification only when the checked candidate, base and relevant verification inputs still match. |
| A reviewer clarified an unapproved plan | The planning author edits the current plan and returns it to review. Change phase only if the actual work moves. |
| The request needs another cell, a package or a different worker | Use the existing service. If a matching child already started, recover its job ID. Wait only while its result is needed. If an adopter depends on this producer’s publication, let the producer finish first. |
| A candidate is ready and a person must make a consequential choice | Ask at the existing review boundary. Route an answer to the owner of that choice. |
| The queue rejected a candidate before merge | On a passing base, send the original failing evidence to its author. If the unchanged base also fails, keep the failure with the base or worker owner. |
| A merge landed and publication failed | Resume publication at the recorded source. For a batch, the original receiver publishes the verified tip. Each submitting job checks its own contribution receipt. |
| The worker has no authorized way forward | Enter Backstop with the blocking fact, what was tried, and the smallest decision or external action that would unblock it. |

**Remove from the normal path** the Backstop investigation whose only output is an extra Implementation pass, the full-cycle rerun for a presentation edit, and routine recovery-authored restatement of a human correction. Keep cancellation, managed workspace persistence, read-only planning, real child waits, verified integration and approval tied to the candidate. The existing four-work-pass and three-consultation/child/package limits describe different activities. In the pilot, use one bounded no-progress check for repeated attempts at the *same unresolved problem*. Reuse the last diagnostic, candidate and passed-check evidence. A different failure uncovered by the candidate is progress. Rewording a summary, producing a new file with the same failure, or polling an unchanged job buys no extra pass. Start with one materially different retry for an unchanged blocker. Continued failure goes to the responsible owner or Backstop. Make that rule visible in the trace so it can be evaluated.

A known worker incident takes an operational route. Retain the candidate and the failing operation and let the runtime or operator recover it. The six mirror cases show why sending a Git fetch failure to a model that needs the same Git mirror is ineffective. Where native retry cannot resume the failed operation, return one actionable failure to its owner. c2j and the worker operators own durable execution and transport. Recipes owns how the result is displayed and routed. [Lifecycle](../../../recipes/adaptive3/lifecycle.yaml) · [Integration](../../../recipes/adaptive3/integration.yaml) · [Recovery policy](../../../recipes/adaptive3/backstop-policy.yaml)

Test child recovery at the decision the parent makes. Start one real child, then return an invalid author report. Recover the same child ID and assert exactly one submission. If a human subsequently drops that prerequisite, the failed attempt stays visible and the parent can finish the remaining work. With the prerequisite still in scope, the parent must account for it. Retain the producer/adopter case where the wait runs in the opposite direction. [Child report repair](https://github.com/colony-2/recipes/commit/30b8b2bae3ceca1798566f8656427cadf74f1ec4) · [Observed producer and adopter waits](inventory.md#reading-the-decisions-in-context)

**First regression pair.** Reproduce the drawer case where a real change outside Review v2 requires code repair, and a subsequent title edit on the verified candidate requires only document checks. Assert the actual number of verification, assessment and Backstop calls. Pair that with a changed base or verification configuration that forces fresh verification. Replay the inbox case with successively different failing checks, then with the same unresolved failure twice. Confirm that useful repairs continue and the stalled one ends.

## 3. Keep independent judgment and spend it at the right point

For the later review trial, retain the read-only planning session and a fresh writable implementer. Preserve the implementer’s session across corrections on the same candidate. Use one independent assessor before a consequential approval or integration decision, and earlier when the worker identifies a concrete risk such as breaking compatibility or delegating new public behavior. A specialist answers a named uncertainty and returns evidence. It gets no independent approval gate. Use the existing review conversation for routine translation. Either author may call on the delegate at an impasse. Count those exceptional visits separately.

Give the assessor a short job: “What could a user do successfully before this change that now fails? What part of the request is missing? Show the evidence. Which findings should block this decision?” An agent proposing a new obligation must trace it to the request, a repository contract, a human decision, or an observed defect. It can offer the rest as advice. Treat prior generated test choices as revisable when better evidence covers the same obligation. Retain hard machine checks for real failures and the repository’s standard test-statement contract.

Replay the process-tree case, where the independent check found a surviving child despite green tests, and the inventory case, where the assessor correctly removed an impossible check. Count lost findings as a cost of reducing assessment. After routing stabilizes, compare **three sessions** with **one author spanning planning and implementation plus an independent assessor** on matched low-risk local tasks. Keep the phase-level read-only and writable grants intact in both arms. Compare user corrections, confirmed defects missed, turns and elapsed active work. Expand the two-session model only if those outcomes justify it. [Process-tree finding](http://db.lab.c2.run:8081/c2/jobs/3MUFFEL5WjDHMIWBFUgHG99mqD1) · [Overreaching inventory check](http://db.lab.c2.run:8081/c2/jobs/3MUFDucdzjLUUqY2dGMBawjtSys)

## 4. Put the user’s decision first and make the C2 guide findable

### Let a follow-up be a conversation

Adaptive3 already sends its background instructions only when it creates a session. It does not set the Codex op’s optional `prompt_prefix_file`. What repeats is the recipe’s task text. At revision `6b5a701c`, the execute template appends 531 words shared across stages, counting whitespace-separated words after removing interpolation expressions. That includes instructions for child jobs, scope amendments and document metadata even on a local repair. The wrapper also appends the current identity and paths. Discussion sends the ordered conversation again, and consultation wraps the owner’s reply in another negotiation assignment. [Agent calls](../../../recipes/adaptive3/agent.yaml) · [Execute prompt](../../../recipes/adaptive3/prompts/execute.yaml) · [Discussion](../../../recipes/adaptive3/discussion.yaml) · [Consultation](../../../recipes/adaptive3/consultation.yaml)

| When the agent is called | Send |
|---|---|
| Fresh session, including a replacement worker starting fresh | Short orientation, assignment, applicable human decision, current workspace and links to selected evidence. Put uncommon procedures in the guide. |
| Same checkpoint, next stage | One sentence about the new job for this turn, current permissions or paths if they changed, and the new evidence. |
| Same checkpoint, repair or reply | The reviewer’s finding, owner’s reply or human’s words, attributed to the actual speaker. Attach the diagnostic or changed file. Deliver any messages that checkpoint has yet to see. |

Start with one Implementation repair. Use the existing session, summary, artifacts and output schema. Let the reviewer say “Both jobs ran at once. See the trace.” The author can reply “I reproduced it and fixed the dependency check.” The workflow verifies the candidate. Keep the full exchange retrievable for a fresh session, a dispute or a replay. Human approval, child waits and publication still go through their native operations. A peer message can request a change. Only the requester can open negotiation. [Discussion regression](../../../recipe-tests/adaptive3/discussion-context.test.yaml) · [Approval and coverage](../../../recipes/adaptive3/cycle.yaml)

Compare the rendered prompts for a fresh author, a resumed repair and a fresh handoff. Have an agent quote a human whose original decision is beyond the first page of history. The next author should retrieve that decision and its attachment using its current grant. Also try a missing decision and a failed read. Only a confirmed gap in approval calls for a new decision. On comparable new jobs, measure follow-up prompt length, repeated turns, missed defects and unnecessary human questions. Keep the session and retry policies fixed. [Cohort counts](inventory.md#fresh-and-resumed-agent-calls) · [Long-history approval case](../2026-11-09/approval-recovery-fix.md)

### What the reader needs

For the blocked merge, the human could see “Your change passed verification. It hasn’t landed because the merge receiver can’t use the recovery receipt. Recipes owns that fix. Your existing approval covers the same verified change.” Put the receipt underneath. Ask for a rewrite when the wording would mislead the reader. Test the first screen with a human. Can they tell what happened, who acts next and what their choice would do?

Publish a single **agent-facing guide to working in C2**, with a stable entry in every fresh session and an accessible local or inbox copy of the index when web access is unavailable. Make it navigable by task. Start with “Where am I and what can I change?”, “How do I get a different worker?”, “Where did my files and Git changes go?”, “How do I retrieve a prior result?”, “How do I ask another cell or wait?”, and “Who can approve, merge or deploy?” Point each answer to an existing maintained reference. Show one working example, who owns the operation, and where the agent can inspect its own route/version. Include health, failures, package availability and escalation in the index. Keep recipe authoring as a separate entry for agents actually writing recipes. Test navigation on a fresh session in a consuming cell without a Recipes checkout. Verify deployed links and offline discovery with the same permissions as that session. [Guide index](../../README.md) · [Task context](../../TASK_EXECUTION_CONTEXT_REFERENCE.md) · [Job inspection](../../JOB_INSPECTION_PLAYBOOK.md)

The first worked example should be a verify hook that needs Docker:

```yaml
execution_needs:
  base: 'ubuntu*'
  capabilities: [docker]
```

An authorized diagnostic submission can request the same allocation with `--require-base 'ubuntu*' --require-capability docker`. The successful ARM/KVM diagnostic used `ubuntu*-arm64` and `kvm`. Teach workers to check their current assignment, task grant and execution facts, choose an available matching base, declare packages separately, and wait for eligible capacity. A matching base does not authorize a release, disclose credentials or establish that a host is deployed. Ask an operator for a real external dependency such as confirming publication on named release hosts. A positive test should get the Docker check onto a suitable worker with no human question. A negative test should preserve a genuine unavailable-capacity or publication decision. Recipes owns the guide and prompt link, c2j owns the execution-needs contract, and Pulse/providers own allocation and capability reporting. [Docker result](http://db.lab.c2.run:8081/c2/jobs/3MRw7IfjU0dx5hP2RI42JUvFqU5) · [ARM result](http://db.lab.c2.run:8081/c2/jobs/3MRyfToV8ipYS3Dp98c0YSXxTCV) · [Release-host question](http://db.lab.c2.run:8081/c2/jobs/3MUL3OE4HKlpfTfdhBxJCkX2ZDB)

## 5. Test phase decisions at their own boundary

First shrink one suite using today’s runner. Exercise a leaf include with a thin wrapper, table-test its structured outputs, and keep the public build’s actual cross-phase route covered once. Start with the missing, null, whitespace and invalid-stage recovery decisions. Record authored lines, distinct behaviors covered, and elapsed case time on the same runner. This step belongs to Recipes and can proceed independently of any framework change.

When c2j’s include mocks are available, try them on the same parent route. One test can substitute several include sites and supply successive responses on revisits. Inspect the parent’s actual inputs, evidence and transitions. Keep the real include as a contract check. [Request to c2j](../../FEATURE_REQUEST_C2J_OPTIONAL_INPUTS_AND_INCLUDE_MOCKS.md)

Keep a few public-flow tests with real bindings for human receipts, child waits, base changes, failed verification and partial publication. Check the wrapper on its native extension selector with the target cell’s actual permission rules. A mock once hid a broken Nix call path. Retire redundant broad cases after mapping their failure cases to retained checks. Judge the change by whether a private rename stops breaking parent tests and an incompatible output still fails them. [Native test contract](../../NATIVE_RECIPE_TESTING.md) · [Model wrapper regression](../../adaptive3/FOLLOWUP_IMPLEMENTATION.md) · [Continuation permissions](../../../recipe-tests/adaptive3/reuse-permissions.test.yaml)

## Where simpler primitives would pay off

| Pattern and evidence | Smallest change to try |
|---|---|
| A repair allowance crosses module boundaries. The lifecycle counts work, consultations, children and packages. The cycle reports progress, Backstop grants extra attempts, and the outer recipe also reads retry state. A local correction can become a decision about granting another turn. | Let the stage decide whether its current repair made progress. Let integration own retries for a moving base and resume publication from its receipt. Return the result or the unresolved blocker to the caller. Replay a progressing repair, a repeated blocker and a merge followed by failed publication. [Lifecycle](../../../recipes/adaptive3/lifecycle.yaml) · [Progress](../../../recipes/adaptive3/retry.yaml) · [Return from recovery](../../../recipes/adaptive3/backstop-return.yaml) |
| Two optional settings multiply four agent call paths into sixteen declarations. One runs per turn. Inherited YAML node IDs caused a real bug. | When c2j supports forwarding optional inputs, verify omission and explicit overrides with the native selector before removing the duplicate declarations. The four start/resume and read/write paths can keep their own permissions. [Adapter](../../../recipes/adaptive3/agent.yaml) · [Request to c2j](../../FEATURE_REQUEST_C2J_OPTIONAL_INPUTS_AND_INCLUDE_MOCKS.md) |
| A parent routing test sets up an included recipe’s internal operations and reviews. A private change can break its caller’s fixtures. | Try the test-only include substitution described above with c2j. Keep a real include contract test and real approval and merge receipts. [Recipe testing](../../NATIVE_RECIPE_TESTING.md) |

Iteration earns its place when the next turn can fix something. When a failure recurs, first ask which existing module owns the decision. Put the fix and regression there. A prompt, counter or state added to several layers for one local failure is a reason to revisit that boundary. The cohort shows the detours. A separate trial must establish which simplification removes them.

## Lessons from 40 commits

Reviewed the 40 most recent first-parent commits on Recipes `main` at `6b5a701`, November 13–23, 2026. The count includes test, documentation, configuration and pin changes. Each commit is counted once by its primary concern. The patches show which behaviors the project chose to protect. The job cohort measures how often a route was taken. [Commit range](https://github.com/colony-2/recipes/compare/c3e0b1e5e61a7affec3c38e4d132a9281f54f996...6b5a701c677cd69ac027b24b635f18d3f119258f) · [Job cohort](inventory.md)

| Primary concern | Commits | What to carry into the pilot |
|---|---:|---|
| Merge and publication | 10 | Replay three cases: rejected candidate on a healthy base, failing base, and publication failure after landing. Assert who acts next, which original log they receive and which commit they publish. The latest receiver follow-up added test coverage for the actual rejection bytes. [Queue cases](../../../recipe-tests/adaptive3/merge-queue-statements.md) |
| Human decisions and review | 6 | Keep the first screen short and preserve the original question, attachments and receipt. Replay a question, a correction and an approval. When changing what a package install may run, check whether the existing approval or cell policy covers it. [Review contract](../../REVIEW_V2.md) · [Recorded writing trial](../../adaptive3/results/notebook-reviews-2026-11-13/dialogue.md) |
| Recovery and progress | 5 | A new instruction and a newly passing check can each justify another attempt. Replaying the same evidence earns no extra attempt. Exercise both paths. Keep a usable human question when the failed worker also prevents an agent from investigating. [Retry proposal and examples](../../adaptive3/PROPOSAL_BACKSTOP_COUNTERS.md) · [Validator deadlock](../../adaptive3/AUDIT_3M28e5.md) |
| Cell ownership and handoffs | 5 | Try the dependency locally, then ask its owner about the gap. Carry selected producer references and check that the recipient can read the original evidence. Test a required deployment where the source has merged but the target still runs the old version. Creation ends when the approved cells are initialized. [Selected outputs](../../ADAPTIVE2_OUTPUT_SELECTION.md) · [Cell creation](../../../recipes/create/README.md) |
| Verification and test fidelity | 7 | Put a check in the stage that can satisfy it. Outcome-only change counts once sent Implementation back for repairs. Reuse the pinned CI checks for the real candidate. Retain native setup and permission tests when narrowing parent tests. [Stage-specific regression](../../../recipe-tests/adaptive3/change-count-scope.test.yaml) · [Verify hook](../../../.c2/recipes/hooks/build/verify.yaml) |
| Module boundaries and public callers | 5 | Queue selection moved into a unit-testable operation while the recipe retained durable waits and Git effects. Apply that split when another decision grows. Keep CLI and included-recipe callers working when adding display fields. A title helps someone find a job. A receipt identifies its result. [Queue refactor](../../adaptive3/MERGE_QUEUE_REFACTOR_PLAN.md) · [Probe callers](../../../recipes/adaptive3/package-probe.md) |
| Runtime and infrastructure | 2 | One commit pinned a cell-hook fix and one changed the JobDB endpoint. Record recipe revision, runner pin and destination before attributing a failure or an improvement to a prompt. |

<details>
<summary>Commit IDs by primary concern</summary>

- Merge and publication — `af7a65d`, `c5e4a9b`, `c3f6b6b`, `2c8438d`, `fb4824c`, `752cfc3`, `919a845`, `e93a235`, `1d7826e`, `34ad8bd`
- Human decisions and review — `38bcd16`, `6b905c9`, `e582e04`, `4064120`, `411f3ef`, `23323cf`
- Recovery and progress — `6ffbf4f`, `23792b9`, `a61d3ca`, `61c4dba`, `6b5a701`
- Cell ownership and handoffs — `01028a1`, `ecc602c`, `a501335`, `9ea5c1d`, `24f0e21`
- Verification and test fidelity — `0e1ba2a`, `37e74b9`, `ededfb3`, `6599c98`, `aa693c6`, `e04b915`, `236d7be`
- Module boundaries and public callers — `74e72fb`, `7156b43`, `b900b87`, `eeca2e9`, `e09552c`
- Runtime and infrastructure — `7a74068`, `556d76e`

</details>

### What the preceding 54 commits add

The extension starts November 1 and ends at `c3e0b1e` on November 13 at 04:03 UTC. The two ranges cover 94 consecutive first-parent commits on Recipes `main` through November 23, including the switch to Adaptive3. The older fixes give us cases to replay. The recent job sequences still set the priorities. [Earlier commit range](https://github.com/colony-2/recipes/compare/84a889884fcf78f44de9ab80dcfb99ddf5329d5e...c3e0b1e5e61a7affec3c38e4d132a9281f54f996) · [November 13 comparison](../../adaptive3/AUDIT_ADAPTIVE2_HISTORY.md)

| Lesson | What the earlier work showed | How it changes the plan |
|---|---|---|
| Read the state C2 already keeps | Comparing Git hashes across tasks could blame a read-only hook for a branch that advanced between calls. Other fixes removed a copied workflow-state bundle and a separate consultation transcript. | Use the runtime’s read-only grant and original task results. Before adding a counter, handoff file or prompt field, name the decision it enables and check whether C2 already records the answer. [Hook fix](https://github.com/colony-2/recipes/commit/d102ce6ce65ac9d2735f538c8816f696aa37f3ab) · [State cleanup](https://github.com/colony-2/recipes/commit/23d376cc0ed4a6d0d311d4da93f50e6b3ef5cbeb) · [Consultation cleanup](https://github.com/colony-2/recipes/commit/71a0253ccf64e2e3a2c041c0373cf77ad900a154) |
| Recover what actually happened | A child could start before its author returned an invalid report. A different fix dealt with a failed child whose assignment had become obsolete after a human correction. | At recovery ask two questions. “What already ran?” comes from the job record. “What do we still need?” comes from the current assignment. Test both before allowing another submission or wait. The recent publication fixes apply the same rule after a merge lands. [Report repair](https://github.com/colony-2/recipes/commit/30b8b2bae3ceca1798566f8656427cadf74f1ec4) · [Obsolete prerequisites](https://github.com/colony-2/recipes/commit/c0c69bdca6788657ba02a2a53bd84c63c4d6d7cc) · [Publication recovery](https://github.com/colony-2/recipes/commit/e93a235136fad0dab24e36b7674f79ff7d4559d7) |
| Find the decision before asking again | A job supplied the right source ID. Its first page of tasks exceeded the CLI output limit. The recipe treated inspection failure as missing approval, entered read-only design, and the next execution request was denied. | Give the agent guide one worked example of retrieving the original decision across pages. Replay an unreadable result and a genuinely missing approval separately. This sequence can look like a permissions or session problem from its last step alone. [Job diagnosis and regression](../2026-11-09/approval-recovery-fix.md) |
| Test where a conversation should end | A live storage receiver showed that the existing save operation could restore a version. The requester also wanted to retain five versions, a separate decision. Another trial produced roughly 700 words for a small draft-saving change. | Try the storage question twice. “How do I restore a version?” should end with the existing route. “I want five versions” can open negotiation. Read the replies. Can the requester act from the first screen, and did either answer create unnecessary work? [Storage exchange](../../adaptive3/results/storage/dialogue.md) · [Review samples](../../adaptive3/results/README.md) |
| Keep repair with someone who can act | On November 1 a verify-hook fix sent failures back to the implementer. On November 7 a handoff fix kept planning instructions from following work into execution. In the recent cohort, 38 trips through Backstop led straight back to Implementation. | Keep the direct-repair trial. Give the current author the failing check and its actual grant. Hold session count steady until we can see whether the extra trip still buys a different decision. [Verify fix](https://github.com/colony-2/recipes/commit/c505b9926fdb2637f61c525b01d3c2f001e150b2) · [Execution handoff](../../ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) · [Recorded transitions](inventory.md#reading-the-decisions-in-context) |

<details>
<summary>All 54 earlier commits by primary concern</summary>

- Workflow structure and rollout (12) — `d89a87e`, `65c1861`, `23d376c`, `777a2b6`, `0e04887`, `7a0e7c0`, `a3fea1f`, `610a59b`, `71a0253`, `16c7427`, `78a7bcd`, `47016ff`
- Recovery and progress (10) — `5c6a6fb`, `91ac4e5`, `33f6474`, `1c7cdc7`, `75730dd`, `83c771b`, `e5f0af2`, `30b8b2b`, `a43ff5a`, `c0c69bd`
- Cell coordination and handoffs (9) — `d667c8a`, `562ff6a`, `8930386`, `8cecc78`, `e1bded0`, `dc0d369`, `a431e25`, `67dc672`, `7f7f213`
- Human decisions and review (8) — `bb4f4a4`, `1006fc4`, `a6874d9`, `c7385f0`, `27bb83d`, `50cce57`, `f198c2d`, `c3e0b1e`
- Runtime, access and inspection (7) — `649f22a`, `04d3120`, `531599a`, `b687a62`, `de2e9cd`, `834b088`, `2fa3296`
- Verification, testing and audit (6) — `c505b99`, `53a44f1`, `538ff7c`, `75d341d`, `d102ce6`, `2808ce0`
- Merge and publication (2) — `f22ac49`, `da6148a`

</details>

## Rollout and decision to continue

1. **Establish the control.** Keep the default on Adaptive3. Collect the same measures for fresh jobs on 6b5a701c or its deployed successor. Mark the exact recipe revision. Identify the Git incident from failed tasks and retain both raw and incident-adjusted numbers. No historical build in this audit tests that fix.
2. **Pilot one Adaptive3 revision at a time.** Start with the three approval cases above. Next try the shorter repair prompt on the existing route, then change repair routing in a separate revision. Follow with consultation and review. Use comparable new work through the existing build entrypoint. Record each revision. Pinned jobs finish on their captured recipes.
3. **Measure at job and decision level.** The main rate is distinct eligible build IDs whose own execution enters Backstop divided by all eligible build IDs. Also report mature/terminal cohorts, inherited history, recorded-parent status, source revision and incident exclusions. Count B visits and forms separately. Track Implementation → Backstop → Implementation, direct repair cycles, phase reentries, human corrections to new requirements, unnecessary access requests, active agent time, time waiting on operators, and successful delivery. Sample the actual checks and outcome documents for missed defects. A lower Backstop rate bought by abandoning jobs earlier fails the pilot.
4. **Use the stated target.** Review the next 100 eligible jobs as an early signal, then a second 100. Aim for at most one or two jobs touching Backstop per hundred. Inspect every exception and any increase in failures, cancellations, unverified merges, duplicated external effects or human questions. Keep valid escalations. One small or unfinished cohort cannot establish a stable 1% rate. If the counter fix alone brings escalation into range with comparable delivery and quality, retain that simpler change. If the pilot reduces detours without losing defects or approval integrity, promote it in stages. If a revision loses defects or approval integrity, return new work to the last proven Adaptive3 revision.

Recipes owns the recipe, prompts, guide, tests and pilot design. c2j owns framework include substitution and runtime retry. Providers own worker allocation. The implementation record lists the local pilot revisions and the checks completed after this plan was written. [Pilot implementation](implementation.md) · [Test results and rollout status](test-results.md)

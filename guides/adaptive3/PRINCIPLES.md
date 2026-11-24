# Design principles for evolving Adaptive3

Start with the outcome the person wants. Check whether it works today. Sometimes an explanation finishes the job.

## Personas

Author, reviewer and delegate are roles a human or an agent can fill. A human can start as the author, hand the work to an agent, then return as the reviewer.

| Persona | Job |
|---|---|
| **Author** | Understand the need, choose the approach, do the work and repair defects. |
| **Reviewer** | Check the result against the need. Explain what fails, for whom, and why it matters. Mark optional improvements as suggestions. |
| **Delegate** | Represent the human’s intent. Explain the result, help resolve an impasse, or bring the human a concrete choice. |

A session carries an agent’s working context. Pilot two author sessions. One handles Direction and Preparation with read-only access. The other edits the candidate and stays through repairs and Outcome. Use an independent reviewer where a consequential defect could escape the checks. On small jobs, compare one author session with two. Keep review and stage permissions alike. Measure missed defects, human corrections and time spent. [Sessions](../ops/OP_CODEX_EXEC.md)

## What becomes a requirement?

“Maybe use a queue” stays a suggestion even when the human says it. “Keep drafts after the tab closes” is a requested behavior.

- Carry the requester’s words and their source. Identify a parent agent’s proposal, a reviewer’s finding or an unknown origin. A child can question an assumption in its assignment.
- Ask the person to approve the behavior and name any exact method they must decide on. Examples, suggested tests and design choices stay flexible unless explicitly adopted or required by a cell contract.
- The author can change the design or proof method while preserving the promised behavior. Repetition in plans, tests and reviews adds no commitment.
- A blocking finding names an agreed behavior at risk, an applicable contract or an observed defect. Withdraw it when its premise falls away.
- When the person corrects an assumption, update the handoff. Retire checks and waits that depended on it. Keep the history of each attempt and any commitments that still apply.

**Example.** “Let a new job wait for an existing job.” Design suggests reserving a new goal. If an existing dependency makes the job wait, the implementer can show the wait directly. The reviewer can accept that check. Check the dependency contract for separate questions such as what happens if the prerequisite fails.

## What the delegate does for the human

Before asking the human to approve the same decision again, the recipe calls the delegate. The delegate compares the proposed revision with the last version the person saw and reads their approval and latest reply. It can continue under that approval, return a specific repair to the author, or ask about a new tradeoff. Honor a request to see the final result.

Keep one review thread (`review_id`) per decision. Read the message and attached comments. Answer questions at the same revision. Send edits to the author in the human’s words. Revised documents stay in the thread. Each approval stays with its version. Either approval can carry optional guidance. Pass the person’s words to the author and reviewer. [Reviews across revisions](../REVIEW_V2.md#following-a-review-across-revisions)

When asking again, say in a sentence or two what changed since the last version shown and why their answer matters. Give a recommendation when there is a tradeoff. Put the question in the message so it makes sense on its own. The team handles stage names and retries.

**Reward comprehension.** Lead with the result, any material failure and the choice. Sample actual reviews. Could the person act from the first screen? Did they ask for a simpler explanation? Did an omission change their decision?

## What an agent receives

Give a fresh session the assignment, relevant evidence and a stable link to the C2 guide in its initial instructions. Index procedures by task. A handoff to a new author includes what was agreed and where to find the work. [Working in C2](../WORKING_IN_C2.md) · [Guide index](../README.md) · [Task context](../TASK_EXECUTION_CONTEXT_REFERENCE.md) · [Job inspection](../JOB_INSPECTION_PLAYBOOK.md)

On a resumed turn, pass the speaker’s words and what changed. “The second job started while the first was still running. Here’s the trace.” Link to original evidence and leave nested conversations at their source. If a preview omits something, read the original before asking again. On a stage change, give the new assignment and permissions. Create a document only when someone needs it to act.

## Stage, cycle and turn

A **job** is one durable recipe execution in a cell. A primary job tracks its ticket through completion or cancellation. A **stage** (or phase) owns one decision. A **visit** lasts until control leaves that stage. A **cycle** does the work, checks it and seeks review when needed. A correction can start another cycle in the same visit. A **turn** is one agent invocation. [Jobs and cells](../../AGENTS.md#c2-concepts) · [Transitions](../STATE_MACHINE_GUIDE.md#how-transitions-work)

| Stage | Handoff |
|---|---|
| Direction | Requested outcome, owning cell and simplest plausible route. An accepted explanation can finish here. |
| Preparation | Behavior to approve, constraints, suggested checks and links to accepted agreements. Identify any checks the cell or requester requires. |
| Implementation | Saved candidate, matching verification evidence and remaining gaps. |
| Outcome | What works, what remains and which candidate the decision covers. |
| Integration | Landed commit and any publication result the cell promised, or the failed step and evidence needed to resume. |

**Keep test statements.** Before implementation, give a short example under “How we could check it.” Trace a disputed expectation to the request, an explicit decision or a cell contract. The implementer can correct an unsupported assumption or show equivalent evidence. Explain the change once in the handoff and keep the approved record intact. [Test statement format](../../AGENTS.md#test-statements)

If a check exposes a real regression, repair it. If a proposed change would weaken an agreed outcome or exact required check, take that choice back to its owner. An established cell guarantee follows the cell’s change or deprecation process. [Deprecation](../../AGENTS.md#deprecation-workflow)

Validate each promise when the inputs it depends on are ready. Run cheap scope checks after preparation can change the candidate and before expensive verification. Keep Outcome reporting in Outcome. A wording fix needs a document check. Reuse verification when the candidate, base and check inputs match. Return the original diagnostic to the owner who can act. [Verification hooks](../BUILD_HOOKS_USER_GUIDE.md#start-with-verification)

For standard delivery, present one plan at Preparation. Open with `1P: <what is proposed>`, then Design and Tests. Put relevant negotiation summaries, transcripts and other evidence after those three. Use the same document shapes across revisions so the person knows where to look. They can request final review or approve completion after independent verification against the plan. A bounded local change can skip the 1P and design, go straight to Implementation and get human approval at Outcome. Preserve the original decision, attachments and receipt. [Review contract](../REVIEW_V2.md)

## Consultation, negotiation and delivery

For “how does this work?”, read the source for the version your project uses, check the docs or try the interface. Use whichever answers the question most directly. The reviewer can rely on that evidence.

**Consultation** is for a need another cell can help with. The owner may know an existing solution. An explanation can finish the exchange. [Consult another cell](../WORKING_IN_C2.md#consult-another-cell)

- **A requirement.** “Our inbox needs the last update time. Can your API provide it?”
- **A suspected bug.** “Saving a note succeeds, but it disappears when I reopen it. Can you investigate?”
- **A question only the owner can settle.** When the source is private or available evidence leaves a meaningful gap, ask directly. “If I retry with the same request ID, do I get the original result?”

**Only the requester opens negotiation** when the available behavior falls short and they want a change. Name the needed outcome or bug. The receiver chooses what it can offer and how to implement it. It can decline. The requester can accept the offer, walk away, take an impasse to the delegate, or consult Root about a new cell. [Cell responsibilities](../../AGENTS.md#cells-purpose-and-parameters) · [Cell creation](../../recipes/create/README.md)

**Delivery** starts once both sides agree. Record the accepted terms once. Pass the reference through handoffs, including nested consultations. The implementer checks that the work fits the agreement and the requester’s decision. A paraphrase keeps the same agreement. If the work changes materially, the requester reopens negotiation. Start the child from the recorded terms and reuse its job ID on retry. Wait only on dependencies needed to finish. [Child jobs and waits](../ops/RUN_RECIPE.md)

Each cell owns the behavior it promises callers. When several cells must change in order, the provider states the constraint. “We can read both formats. We can remove the old reader once all writers switch.” A coordinator such as Root arranges the writer changes and confirms when the provider can remove the old reader in a separate change. [Deprecation](../../AGENTS.md#deprecation-workflow)

## Iteration and recovery

Keep repairs with the author while checks show progress. Clearing one failing check and exposing the next is progress. Rephrasing the same failure is insufficient. Pilot one materially different repair for an unchanged blocker. Discussion and durable waits consume no repair attempts. Apply a new instruction or newly passing check once when deciding whether work can continue.

Keep the four-round limit within one consultation. Pilot ten distinct consultations per phase. If four rounds leave the question unresolved, or the author needs an eleventh thread, the delegate decides how to proceed. Ask the human only when their answer would change the work.

Either author can escalate when promising options run out. Give the delegate the blocker, completed actions, any offer and a link to saved work. A firm refusal can establish an impasse. Resume at the first unfinished action. If a child started and the author’s report failed, recover its job ID and repair the report. If the unchanged base fails the same check, route that failure to its owner. Ask the human when the remaining choice is theirs. [Failure handling](../RECIPE_FAILURE_HANDLING_USER_GUIDE.md)

Aim for at most two builds per hundred needing exceptional help. Count each escalated build once. Count routine delegate work, including screening repeat approvals, separately. Record stage visits, cycles and why control moved. Track repeat visits, decisions the delegate settled, avoidable questions, missed defects and delivery. Show unfinished builds and worker incidents separately.

## Module boundaries

- **Orchestration.** Each stage owns its cycles. Return a decision, remaining work and links to evidence. Use native records to identify an agreement, approved revision, child job or candidate. Agents judge what a decision covers. Rewording a summary or repairing a supporting link preserves the decision. Add a transition when the owner, decision or external action changes. Put a growing calculation behind one tested operation. Keep waits and external effects visible. [Node scope](../NODE_SCOPE_SPEC.md) · [Artifacts](../RECIPE_ARTIFACTS_REFERENCE.md)
- **Execution environment.** The workspace is temporary. Keep code in the managed worktree and save other outputs in the outbox. For a check that needs Docker, request a suitable base and the Docker capability. Use package requests for installed tools. Ask the operator only for what the cell cannot obtain itself. [Workspaces and saved work](../WORKING_IN_C2.md#workspaces-and-saved-work) · [Build hooks](../BUILD_HOOKS_USER_GUIDE.md)
- **Merge queue.** Group approved changes by cell and branch. Verify again when the base moves. Reuse approval only if the approved change is intact. Each caller checks whether its change landed. The queue publishes the verified batch tip. After a publication failure, the original publisher resumes at that recorded commit, even if the branch advanced. The cell responsible for a required deployment confirms it in the target environment. [Queue receipts](../BUILD_HOOKS_USER_GUIDE.md#queue-receipt-and-upgrade) · [Deployment questions](../ASK_RECIPE.md)
- **Recipe tests.** Test each module’s public result and failure path. Mock the relevant include sites to test a parent’s routing. Exercise the real interface for permissions, worker setup, approvals, waits and Git effects. Sample actual replies to judge whether a person can use them. [Native recipe testing](../NATIVE_RECIPE_TESTING.md)

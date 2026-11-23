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

- Carry the requester’s words and link to their source. Label a parent agent’s proposal and a reviewer’s finding as such. If the origin is unknown, say so. A child can act on delegated work and still question an expensive assumption.
- On the approval screen, say what should work and name any exact method the person is being asked to require. A detail in a design attachment stays a working choice unless explicitly adopted or required by a cell contract.
- The author can change the design or proof method while preserving the promised behavior. Repetition in plans, tests and reviews adds no commitment.
- A blocking finding names an agreed behavior at risk, an applicable contract or an observed defect. Withdraw it when its premise falls away.
- When the person corrects an assumption, update the handoff. Retire checks and waits that depended on it. Keep the history of each attempt and any commitments that still apply.

**Example.** “Let a new job wait for an existing job.” The designer writes “Reserve a new goal and prove it was reserved.” If the existing dependency makes the new job wait, the implementer can drop the reservation and show the wait directly. The reviewer can accept that evidence in the same cycle. Whether a failed prerequisite should cancel the new job is a separate behavior. Look up the existing dependency contract. Ask only if an unresolved choice would change what the requester gets.

## What the delegate does for the human

Lead with what happened, why it matters and any decision needed. Reuse the author’s words if they already do that. Offer a recommendation and tradeoff when a choice is open. Keep material failures visible. On a second review, lead with what changed.

> Jobs can already wait for another job. The creation form is missing that option. I recommend adding it there.

Preserve the human’s words and send their meaning to the person who can act. Answer a question in the open review. “Move the switch into the About menu” settles placement. Offer actions the team can actually take. The human sees a useful title. The team chooses the stage and keeps the original decision receipt.

**Reward comprehension.** Prefer the shortest answer that supports an informed choice. Sample actual reviews. Could the person act from the first screen? Did they ask for a simpler explanation? Did an omission change their decision?

## What an agent receives

Give a fresh session the assignment, relevant evidence and a stable entry to the C2 guide. Put procedures there, indexed by task and accessible locally in every cell. A handoff to a new author includes what was agreed and where to find the work. [Guide index](../README.md) · [Task context](../TASK_EXECUTION_CONTEXT_REFERENCE.md) · [Job inspection](../JOB_INSPECTION_PLAYBOOK.md)

On a resumed turn, pass the speaker’s words and the evidence that changed. A reviewer can say “The second job started while the first was still running. Here’s the trace.” Link to the producer’s original evidence and leave nested conversations there. If a preview is incomplete, retrieve the original before asking someone to decide again. On a stage change, give the new assignment and its actual permissions. Create a document only when someone needs it to act.

## Stage, cycle and turn

A **job** is one durable recipe execution in a cell. A primary job tracks its ticket through completion or cancellation. A **stage** (or phase) owns one decision. A **visit** lasts until control leaves that stage. A **cycle** does the work, checks it and seeks review when needed. A correction can start another cycle in the same visit. A **turn** is one agent invocation. [Jobs and cells](../../AGENTS.md#c2-concepts) · [Transitions](../STATE_MACHINE_GUIDE.md#how-transitions-work)

| Stage | Handoff |
|---|---|
| Direction | Requested outcome, owning cell and simplest plausible route. An accepted explanation can finish here. |
| Preparation | Behavior to approve, constraints, suggested checks and agreed external work. Identify any checks the cell or requester requires. |
| Implementation | Saved candidate, matching verification evidence and remaining gaps. |
| Outcome | What works, what remains and which candidate the decision covers. |
| Integration | Landed commit and publication result, or the failed step and evidence needed to resume. |

**Keep test statements.** Before implementation, write a short example under “How we could check it.” A designer can be wrong about the expected behavior as well as the test method. When a statement is disputed, trace it to the request, an explicit decision or an existing cell contract. The implementer can correct an unsupported assumption or use equivalent evidence. Give the reason once in the handoff. Keep the approved record intact. [Test statement format](../../AGENTS.md#test-statements)

If a check exposes a real regression, repair it. If a proposed change would weaken an agreed outcome or exact required check, take that choice back to its owner. An established cell guarantee follows the cell’s change or deprecation process. [Deprecation](../../AGENTS.md#deprecation-workflow)

Validate each promise when the inputs it depends on are ready. Run cheap scope checks after preparation can change the candidate and before expensive verification. Keep Outcome reporting in Outcome. A wording fix needs a document check. Reuse verification when the candidate, base and check inputs match. Return the original diagnostic to the owner who can act. [Verification hooks](../BUILD_HOOKS_USER_GUIDE.md#start-with-verification)

For standard delivery, ask for a plan decision at Preparation. The person may choose final review or approve completion if independent review confirms the verified result meets the agreed plan. For a short local change, go from Direction to Implementation and obtain human Outcome approval. Preserve the original decision, attachments and receipt. [Review contract](../REVIEW_V2.md)

## Consultation, negotiation and delivery

**Consultation** asks “How can I do this today?” Try a cheap local check. Ask the owner about an unknown whose answer would change what you do. The owner can correct the premise, show an existing route or explain a limit. That answer can finish the consultation.

**Only the requester opens negotiation** when it finds the available options too limiting. Name the change and why it matters. “I think this needs a bug fix. A job started before its prerequisite succeeded.” Or “I want a feature. Our release needs to wait for two jobs.” The receiver can decline or propose work that fits its cell. Acceptance requires its explicit agreement.

**Delivery** starts when the requester chooses the receiver’s terms. The receiver records what it agreed to deliver. The requester can walk away, escalate an impasse to the delegate, or consult root about a new cell for the unmet need. Wait only on a dependency needed to finish. If an adopter needs the producer’s publication, let the producer finish first. [Cell responsibilities](../../AGENTS.md#cells-purpose-and-parameters) · [Child jobs and waits](../ops/RUN_RECIPE.md) · [Cell creation](../../recipes/create/README.md)

## Iteration and recovery

Keep repairs with the author while checks show progress. Clearing one failing check and exposing the next is progress. Rephrasing the same failure is insufficient. Pilot one materially different repair for an unchanged blocker. Discussion and durable waits consume no repair attempts. Apply a new instruction or newly passing check once when deciding whether work can continue.

Either author can escalate when promising options run out. Give the delegate the blocker, completed actions, any offer and a link to saved work. A firm refusal can establish an impasse. Resume at the first unfinished action. If a child started and the author’s report failed, recover its job ID and repair the report. If the unchanged base fails the same check, route that failure to its owner. Ask the human when the remaining choice is theirs. [Failure handling](../RECIPE_FAILURE_HANDLING_USER_GUIDE.md)

Aim for at most two builds per hundred needing exceptional help. Count each build once when its own execution escalates. Count routine summaries and translation separately. Record each stage visit, cycle and reason for a transition. Track repeat visits, decisions the delegate settled, avoidable questions, missed defects and delivery. Show unfinished builds and worker incidents separately.

## Module boundaries

- **Orchestration.** Each stage owns its cycles. Return a decision, remaining work and links to evidence. Read job state, approvals and completed actions from their native records. Add a transition when the next owner, decision or external action changes. Put a growing calculation behind one tested operation. Keep waits and external effects visible in the recipe. [Node scope](../NODE_SCOPE_SPEC.md) · [Artifacts](../RECIPE_ARTIFACTS_REFERENCE.md)
- **Execution environment.** Inspect the task’s workspace and permissions first. For a check that needs Docker, request a worker with a suitable base and the Docker capability. Declare missing packages through the package route. Ask the operator only for what the cell cannot obtain itself. [Task context](../TASK_EXECUTION_CONTEXT_REFERENCE.md) · [Build hooks](../BUILD_HOOKS_USER_GUIDE.md)
- **Merge queue.** Group approved changes by cell and branch. Verify again when the base moves. Reuse approval only if the approved change is intact. Each caller checks whether its own change landed. The queue publishes the verified batch tip. After a publication failure, the original publisher resumes at that recorded commit, even if the branch advanced. Confirm a required deployment in its target environment. [Queue receipts](../BUILD_HOOKS_USER_GUIDE.md#queue-receipt-and-upgrade) · [Deployment questions](../ASK_RECIPE.md)
- **Recipe tests.** Test each module’s public result and failure path. Substitute include results to test a parent’s routing when runner support is available. Exercise the real interface for permissions, worker setup, approvals, waits and Git effects. Sample actual replies to judge whether a person can use them. [Native recipe testing](../NATIVE_RECIPE_TESTING.md)

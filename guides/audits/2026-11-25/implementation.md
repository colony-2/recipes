# Adaptive3 changes from the November 25 audit

## November 27 delegate implementation

The public build now gives one continuing delegate the next decision after every operation. It selects the operation, writes the assignment and chooses what evidence to pass along. The top-level recipe went from 58 transitions to four. Verification, negotiation and integration still enforce their own contracts. The planner and implementer each retain their session. [Dispatch loop and primitive catalog](../../adaptive3/DELEGATE_ORCHESTRATION.md)

The delegate sees every build presentation. A direct question carries enough context to answer with the files closed. An interview can probe the whole private proposal in one sitting. Each round returns the source documents, wording, offered choices, skips, typed answers and receipt to the planner. The planner decides whether the proposal needs revision. This implementation uses the native review form for independent questions. Conditional branches and inline editing in the client remain integration work. [Presentation](../../../recipes/adaptive3/delegate-present.yaml) · [Interview preparation](../../../recipes/adaptive3/prepare-interview.yaml)

The runtime records who said what, which candidate passed verification and what the person authorized. The delegate can send ordinary repairs back to the author, finish an explanation directly, return a tested patch to its caller or integrate the change. A requested final decision still goes to the person. Direct native questions wait for a reply. The public completion summary can answer the requester and close the job. A mid-job thread message that lets work continue immediately would need a send operation. Behavioral impact on real requests remains to be measured. [Regression results](test-results.md) · [Field measurements](improvement-plan.md#check-the-effect)

## Earlier implementation

The first plan describes the proposal. A revised review compares against the last packet presented for that decision with a human reply. The author gets the packet, the question, the reply and its source. Outcome uses the measured candidate to identify the pending decision. The 1P, Design and Tests keep their existing order. [Review cycle](../../../recipes/adaptive3/cycle.yaml) · [Discussion](../../../recipes/adaptive3/discussion.yaml)

| Finding | What changed |
|---|---|
| A saved candidate could fail to reopen | An implementation retry carries the author’s diagnostic files under `error/`. C2 restores the candidate through its normal workspace mechanism. |
| The delegate diagnosed a local repair and still asked the person | The delegate can send either author one concrete instruction within the agreed assignment. After the ordinary retry allowance, the final local attempt needs a specific repair instruction. A changed promise still goes back for a decision. |
| An internal correction looked like a human revision | The writer gets the last human presentation for the relevant decision. Internal drafts and automated replies do not replace it. A same-stage planning correction gets a short message with the finding, its source and applicable guidance. The author can cite existing lines and the reviewer can withdraw the finding. |
| Historical attachment labels consumed negotiation rounds | The renderer labels open exchanges. The reviewer sees the descriptions the author controls. Receiver corrections have a bounded allowance within a round. The requester still gets up to four exchanges and can decline the offer. |
| Sibling jobs kept asking the same scope question | A coordinator can pass a review reply with its original words, source job and receipt to each affected owner. Direct and running jobs can look up the source through the job guide. The receiving owner can identify a conflicting local requirement. |
| A withdrawn child assignment kept asking how to proceed | Either author can identify the withdrawal. The delegate checks the original words and which assignment they cover. At an impasse the delegate can also recognize the withdrawal directly. The parent gets its source and the unfinished work. A bare child cancellation leaves the assignment open. |
| A verified candidate got another approval request | Take to Completion sends a covered candidate to merge under the plan receipt. Missing pre-merge evidence returns to Implementation. A necessary exception goes to the delegate. An explicitly requested published-consumer check runs after merge and the configured publish step. Its result and evidence reach the job result. A check retry resumes at that boundary. |
| Agents asked for an operator before trying the work | New sessions describe candidate verification, hook execution needs and package requests. The guide directs authors to try the accessible interface or a local fixture, inspect recorded failures, and take an actual owner dependency to its cell. |

A landed-consumer check uses the existing implementation session. Sharing a review is selective because a reply may address only one cell. An already running sibling can read the source at its next turn. Immediate delivery into another job’s pending form would require a runtime feature.

The next field check is the first 100 eligible builds, followed by a second 100. Measure repeat approvals and exceptional delegate visits alongside missed defects, requested final reviews and completed consumer checks. [Improvement plan](improvement-plan.md) · [Regression results](test-results.md)

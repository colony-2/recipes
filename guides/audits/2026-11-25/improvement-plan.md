# Adaptive3 improvement plan from the November 24–25 audit

**Keep the small set of roles. Fix what happens before a job asks the human for help.** Fifteen of 36 builds reached exceptional Backstop, against a goal of one or two per hundred. Eleven of 86 review messages asked for an owner, contact or confirmation from an operator. The changes below belong to Recipes unless another owner is named. [Job inventory](inventory.md)

## First, fix the routes that send work back to the human

1. **Let the delegate carry out an agreed local repair.** Either author can escalate. When the scope is settled and a bounded retry remains, let the delegate return the repair instructions to that author using the existing decision. Replay macVZ’s model-capacity failure. One retry should resume the author. A change to the promised outcome still needs a decision. [macVZ](https://jobs.colony2.com/c2/jobs/3MaP2kRI3WNr7CDRbWhR3EXS65U)

   A follow-up after the cutoff adds a recovery test. Cortex saved a candidate and requested one more implementation turn. The repair route forwarded all task artifacts as diagnostics, including the Git restore pack. The worker reported duplicate matches for its selected restore artifact. Pass only the diagnostics needed for repair and let c2j restore the managed worktree. Test that the next writable turn opens the saved candidate and can finish its checks. [Cortex goal retirement](https://jobs.colony2.com/c2/jobs/UiOXfJCyb3nLw5G7TmWyq0Z7jOs) · [Repair handoff](../../../recipes/adaptive3/cycle.yaml#L62)

2. **Carry a parent decision to the children it affects.** The coordinator should pass the person’s words and the source receipt. Each child applies the decision or raises a specific conflict with its own requirements. Replay the retirement of Intel Mac support across the three siblings. An explicit withdrawal conveyed in a child review should also reach the parent and close the withdrawn assignment. Cancelling a child review by itself leaves the parent’s assignment open. [Root verification audit](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) · [Withdrawal](https://jobs.colony2.com/c2/jobs/3MaP2haaC0PgRUrbmwZFl2cvRyV)

3. **Write each review from the person’s place in the job.** Give the writer the last packet actually presented in that review thread, the person’s reply, and the decision the recipe is waiting for. Apply that context to the message and primary document. Let the delegate screen repeat approvals and carry forward a decision that still covers the work. Fix generated attachment labels in the recipe that renders them. [Review evidence](inventory.md#which-earlier-review-could-the-person-have-seen)

   | When the person sees it | What to show |
   |---|---|
   | First plan | The proposal and decision. Fold internal revisions into the proposal. Show the 1P first, then Design and Tests. |
   | Revised plan or outcome | What materially changed since their last packet and why it matters. Use the same review thread. |
   | Reply to a question | Answer directly. Keep the packet when the proposal stands. Guidance can accompany any review choice. |
   | First outcome after plan approval | What was delivered and verified against the plan. If they chose **Review before Complete**, explicitly ask whether to merge. |

   Put the decision and material change in the opening two sentences. Leave supporting evidence in the attachments. Replay the Cortex first plan, its revision after human feedback, and the parallel-node outcome that claimed approval while waiting for a merge decision. [Cortex](https://jobs.colony2.com/c2/jobs/3MaLY2L6g3nUBQneygaCbyE2GKa) · [Parallel nodes](https://jobs.colony2.com/c2/jobs/3MaP1pW9YHeX1ZHvWiGOKO0EUfQ)

## Then, make the job’s purpose clear from the start

4. **Tell the planning author and reviewer how verification works.** Use the initial session context and a link to the C2 guide. The implementer changes the managed worktree and runs focused checks. The recipe runs the cell’s verify hook on the candidate before merge and returns failures for repair. A hook step can request its base and capabilities within the job. Use package requests for missing tools. Inspect the recorded run. In the c2j case, the pre-run question about access should have led to trying the hook. Six leases with no test output later gave Pulse a concrete incident to diagnose. [C2 guide](../../WORKING_IN_C2.md) · [Apple Silicon run](https://jobs.colony2.com/c2/jobs/3MbjBfYF4QgmFoxvmGc4SUEynuN)

5. **Keep investigation and coordination with the people doing the work.** Say which operation was attempted, what happened and what remains possible. Use accessible code, existing interfaces or a local fixture first. Consult an owner for information the cell cannot obtain. The requester can open a negotiation for a needed fix, and the receiving cell decides what it can deliver. Bring the human an incompatible offer, a consequential scope choice or a real access grant. Route a failure reproduced on the unchanged base to its owner while fixing the local defect. Preserve useful disagreement by checking a disputed claim against the pinned API, commit or run. [Cortex 403](https://jobs.colony2.com/c2/jobs/3MaLY2L6g3nUBQneygaCbyE2GKa) · [Chapter status negotiation](https://jobs.colony2.com/c2/jobs/3MbmPf0wjAWwY0E8QulCUrBn1ds) · [Labels investigation](https://jobs.colony2.com/c2/jobs/3MaMm0UTSTnRMuxQ0GI4yvO4EQT)

6. **Finish the outcome the requester asked for.** An explanation can end with an answer. A coordinator owns agreed handoffs. A change job carries its candidate through validation, the selected review, merge and any configured publish step. If the request requires a fresh consumer to use the published artifact, arrange that check and record its result. If the publishing mechanism needs modification, the coordinator sequences a separate contribution with its owner. Raise deployment status only when it affects the requested outcome. Replay the timestamp job with a successful merge, an absent publish hook and an explicit fresh-consumer check still due. [Timestamp job](https://jobs.colony2.com/c2/jobs/3MZhCiRqRik9j9YjNpJNalziOSe) · [Publish hook contract](../../BUILD_HOOKS_USER_GUIDE.md#choose-your-hooks)

## Check the effect

Keep the planning author, implementation author, independent reviewer and delegate. Preserve the short path for small changes, four rounds per consultation, and the current allowance of ten distinct consultations per phase. Use focused native recipe tests for the routing changes. Judge prompt changes on subsequent jobs. [Design principles](../../adaptive3/PRINCIPLES.md)

Compare like requests in the next cohort and report large sibling groups separately. Count exceptional builds, phase returns, human messages per parent request, repeated decisions and references to unseen drafts. Separate pre-run operator questions from evidenced failures and grant decisions. Check whether requested post-merge tests ran. Track requested final reviews, useful clarification answers and missed defects alongside the counts so a shorter thread still delivers the right result. [Baseline](audit.md) · [Request and reply counts](requests-and-interventions.md)

# Fewer repeat approvals in Adaptive3

The human decides what they want and which tradeoffs they accept. The author carries that out. The reviewer checks the result against that decision. The delegate uses the conversation to settle routine questions and brings the human a choice when their answer would change the work. Recipes owns these corrections. [Four-job audit](audit.md)

### 1. Deliver the agreement the owner accepted

Remove `plan.assignments`, the second list of cell names and assignment text. In the lease job, one synonym made a recorded agreement look new. In the switcher job, Root’s agreement existed and the approved brief included it. Three delivery requests nevertheless went back to planning because the copy omitted Root.

Give the implementer one rule. Use the owner’s accepted agreement when it covers the work and the work still fits the requester’s decision. Pass the reference to that agreement back through nested conversations. The recipe resolves it, sends the recorded assignment to the child, and reuses the child on retry. Remove the instruction to reproduce the owner’s words. If the work changes materially, the requester reopens negotiation. The delegate brings the human any new tradeoff.

Replay the lease paraphrase and the nested Root handoff. Each should start one child and find that child on retry, even when the cell has multiple agreements. Advice, a superseded offer, and a proposed amendment awaiting the receiver’s agreement cannot start new work. [Saved copy](https://github.com/colony-2/recipes/blob/2aa5580/adaptive3.yaml#L674-L677) · [Delivery gate](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/lifecycle.yaml#L107-L119) · [Wording instruction](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/prompts/execute.yaml#L136-L138)

### 2. Ask about the behavior your cell needs

For “how does this work?”, read the relevant source, look at the docs, or try the interface. Use whichever is quickest. If an owner keeps its implementation private, asking how its interface behaves is a normal consultation. A reviewer can accept evidence the author gathered directly.

Give agents examples in the guide. Use them as illustrations, with no required wording or proof of prior investigation. [Current consultation guide](../../../WORKING_IN_C2.md#consult-another-cell)

- **A requirement.** “Our inbox needs to show when each lease was last updated. Can your list API give us that value?” The owner can point to an existing field or propose a change.
- **A suspected bug.** “I saved a sidebar note and got a success response. When I reopened the review, the note was gone. Can you investigate?” The requester supplies what it observed. The owner chooses how to investigate and fix it.
- **A question about a private interface.** “If I retry with the same request ID after a timeout, do I get the original result?” An answer can finish the conversation. Only the requester opens negotiation when it wants something changed. The receiver decides what it can deliver.

Each cell owns the behavior it promises to callers. Other cells choose how to deliver theirs. Keep instructions for operating a service with the cell assigned that work. For a two-step upgrade, the provider might say, “We can read both formats now. We can remove the old reader once all writers have switched.” A coordinator such as Root owns the cross-cell requirement, arranges the writer changes, and confirms when the provider can make the separate removal. Put that guidance in the coordinator’s reference. [Current cross-cell coordination guidance](../../../WORKING_IN_C2.md)

Keep the current default of four rounds per conversation. Start with a proposed ten distinct consultations per phase, up from three. Count each thread once. Send an exhausted conversation or a proposed eleventh consultation to the delegate. Revisit twenty if later jobs regularly need it.

Use the Sidebar handoff to test both outcomes. If the pinned recipe already passes the file correctly, the author can verify that and continue. If it drops the file, Recipes can be the fourth owner contacted without a human prompt. Also test that one unresolved conversation stops at four rounds even when other phase slots remain. [Phase quota](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/lifecycle.yaml#L306-L310) · [Conversation limits](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/consultation.yaml#L69-L77)

### 3. Give routine repairs back to the author

When the delegate has a concrete repair within the assignment, let it direct the author to make it. Retry counts can trigger diagnosis. Exhausting one does not create a decision for the human. If the remaining choice belongs to the human, preserve the delegate’s plain-language question even when a supporting link fails.

Also align each phase’s advertised replies with its routes. In Preparation, a completed revised draft goes to ordinary validation. During implementation, discovering a material change sends the plan back for revision. Both paths preserve the work already done.

In the regression cases, the switcher author fixes the table after the delegate identifies the two blank lines. The hook author can submit a revised draft from Preparation and receive a review. If private-package replay really needs an owner decision, the message asks whether that capability is needed for the first release. [Execution routes](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/cycle.yaml#L56-L85) · [Delegate return](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/backstop.yaml#L125-L137)

### 4. Put the delegate before a repeat approval

When the recipe would ask for a decision the human already made, it calls the delegate first. The delegate reads the last version the human saw, their latest words and approval, and the proposed change. It can continue under the recorded decision, return a specific repair to its owner, or ask the human about a new tradeoff. Honor a request to see the final result. An author can answer a question while the original decision is still pending.

#### Present each review as one message

Each review carries **one agent-written prompt to the human, one primary document and any relevant supporting documents**. The agent presenting the review writes what it wants to say or ask on this turn. Put that text in the form’s existing `question` field. Keep the prompt with the documents it refers to.

- **Initial review.** “Do you approve this plan?”
- **Answer to a human question.** The person replies, “Will my draft survive a restart?” The next review uses the same documents. Its entire prompt can be “Yes. Your draft comes back when you reopen the app on this device. Shall we go ahead with that plan, or would you like a change?”
- **Revised work.** Lead with what changed since the version the person saw. In the hook job, the prompt could have said “We added a test to protect normal builds. Those builds would still need a new job after a permission change. Do you want them covered in this release?”

The choice tells the agent how far to proceed. The person can give guidance with any of the three choices.

- **Revise** keeps the decision open. Read the reply and any annotated documents. Answer questions, make requested edits, or do both in the next review prompt. This covers the former **Ask a question** action.
- **Review before Complete** approves the plan and asks to see the result before the job finishes. The person might add “Show me the empty state in the final review.”
- **Take to Completion** approves finishing once the work is verified. The person might add “Use the existing wording for the empty state.” The author can act on that and finish under the same approval.

Both approvals work with an empty comment. When the person adds guidance, keep their words with the approval and pass them to the author and reviewer. Follow instructions and keep suggestions optional.

Use the job’s ordered review requests and human submissions as the message history. Retire the separately tracked `conversation` list and the loop that appends an answer before replaying a standing question. Each prompt or reply appears once in the job thread. Keep a stable `review_id` for the decision. An answer reuses the document revision. Revised documents advance it. The approval receipt identifies exactly which request and version the human accepted. Recipes owns the form and routing changes. Coordinate the history display with Cortex. [Current review message](https://github.com/colony-2/recipes/blob/2aa5580/recipes/adaptive3/review.yaml#L85-L96) · [Current discussion loop](../../../../recipes/adaptive3/discussion.yaml)

Replay a question with a commented attachment and a requested edit. Check that the answer appears once as the next prompt and that the new prompt explains any revision. Exercise each approval choice with and without guidance. Check that the approval records the version shown, the author and reviewer receive the person’s words, and the job honors the selected stopping point. A wording repair covered by an earlier approval should consume no new human decision.

### 5. Simplify three other decisions

- **Review attachments.** The switcher and Sidebar recovery forms lost their useful questions when supporting files failed validation. Build the displayed list from the selected artifacts. Reuse descriptions for unchanged files and ask the author only for new or changed descriptions. Get a negotiation’s origin from the producing job and agreement. Keep the question readable while the author repairs optional links. A missing document essential to a decision still needs repair.
- **The delegate’s own proposals.** Answering a question can rephrase a proposed repair. Today, that alone can make the recipe reassess the action. Keep the proposal already shown while answering. Let the delegate explicitly replace it when the intended action changes. A person choosing Apply acts on the displayed proposal.
- **Returning to work after an interruption.** The recovery policy compares saved copies of whole results and document lists. In a fixture, editing only a summary disabled the return to Implementation. Use the recorded decision and let the delegate judge whether later changes affect the work. Continue to verify the actual candidate and required check inputs before merge.

Fix the attachment problem alongside repeat reviews. The other two behaviors were reproduced in isolation. Check them against the next affected jobs before expanding recovery work. [Evidence, source and regression cases](inventory.md#checks-for-similar-structure)

### 6. Make the plan review recognizable

All 17 plan presentations in the four-job audit selected the one-pager first, Design second and Tests third. These include repeat presentations. None of the 17 primary attachment titles began with `1P:`. The lease brief opened with “What should work” as its title. Someone scanning the attachment list or opening the document could easily miss that this was the proposal. [Lease review](https://jobs.colony2.com/c2/jobs/0983ec11-ec4c-4c41-8f99-09efb51e2a15)

Adaptive2 and the first Adaptive3 Direction prompt specified the same five sections. A saved Adaptive3 1P shows them in use. On November 23 the Preparation prompt started asking authors to open the same document with “What should work.” Restore one shared outline for Direction and Preparation. Keep “What should work” in Tests. [Adaptive2 prompt](https://github.com/colony-2/recipes/blob/610a59bba9eb707b96f84972b929958dff1c6dcb/recipes/adaptive2/prompts.yaml#L33-L42) · [First Adaptive3 prompt](https://github.com/colony-2/recipes/blob/78a7bcd6d583873314abd7f027b5e4dfadc2eec1/recipes/adaptive3/prompts/execute.yaml#L14-L22) · [Notebook 1P](../../../adaptive3/results/notebook-reviews-2026-11-13/review/durable-local-drafts.md) · [November 23 Preparation prompt](https://github.com/colony-2/recipes/blob/9b2f6077320a281b4244835eb0c288da2ab9f315/recipes/adaptive3/prompts/execute.yaml#L37-L45)

Open the combined plan review with `1P: <what is proposed>` as both its Markdown heading and its attachment title. Link Design and Tests near the top. Show them as the next two attachments, followed by relevant negotiation summaries, transcripts and other evidence. On revision, put a sentence below the title saying what changed since the version the human last saw. [Author prompts](../../../../recipes/adaptive3/prompts/execute.yaml) · [Review ordering](../../../../recipes/adaptive3/tools.yaml)

Use these five headings in order in the standard 1P.

1. **Problem Description** — Who has the problem, what happens today and what do we recommend?
2. **Non Goals** — What is deliberately outside this proposal?
3. **What we are planning to do** — Describe the change the person is being asked to approve. Put the expected scope by cell here.
4. **Compat/Upgrade** — What changes for existing users or callers? If they need to do nothing, say so in one line.
5. **Key challenges/design questions & answers** — Use a two-column question-and-answer table for consequential choices. Give the recommendation and reason, or say what remains open. Include rows only for real questions.

For a job **started through consultation or negotiation**, put **Why this job exists** inside Problem Description, directly after the opening. In one or two sentences, name the requesting cell, the outcome it needed and the contribution this cell agreed to make. Link the parent job and the originating consultation or negotiation. Use the recorded summary and transcript when available. Keep those links on revisions. For a direct child assignment, cite the initiating request. For an ordinary standalone job, omit this paragraph. [Incoming assignment guidance](../../../adaptive3/PROPOSAL_PREPARATION_REVIEW.md#how-either-job-explains-a-cross-cell-request) · [Negotiation documents](../../../../recipes/adaptive3/negotiation-report.yaml)

Check the initial and revised forms for a consultation-started job. Open the 1P first, confirm the five headings and follow its links back to the incoming exchange. Design and Tests should still occupy the next two slots. Check a standalone plan for the same outline and a short-path job for its first review at Outcome. [Templates for the other documents](#8-give-each-key-document-a-template)

### 7. Keep routine updates on the short path

The short route exists. A completed Cortex job went from Direction straight to Implementation and reached its first human review at Outcome. Before this prompt change, Direction asked for a one-pager on every delivery. The native validator still requires a titled primary document even on the short route. The existing end-to-end test supplies one, so it proves the review can be skipped while leaving that paperwork in place. [Cortex job](https://jobs.colony2.com/c2/jobs/3MUSQihJHKW0v6Q6SStjOdUrHMM) · [Route](../../../../adaptive3.yaml) · [Document check](../../../../recipes/adaptive3/validate.yaml) · [Short-route test](../../../../recipe-tests/adaptive3/build.test.yaml)

Three actual Cortex dependency updates on November 17–19 all entered Preparation and showed a Direction review. Each ran a recipe revision from before November 22, when the short route was added. They explain the earlier experience. We still need a dependency update on the newer recipe to measure the author's route choice. [c2j and JobDB update](https://jobs.colony2.com/c2/jobs/3MD9lQbGm3xI6pi5r0eD0rh0OZd) · [c2j update](https://jobs.colony2.com/c2/jobs/3MI3fDJ4gdnqrKvDsIRX83tQx9g) · [c2j upgrade](https://jobs.colony2.com/c2/jobs/3MIt6E4gqAgItisv7S6rsdjNEGW) · [Route added November 22](https://github.com/colony-2/recipes/commit/23323cf)

Choose the route before writing. A compatible dependency update with a known check can go straight to Implementation. The prompt now asks for only a few lines for the implementer on that path. Next, carry those lines in the existing work summary and let short Direction finish without authoring a document. Preserve any supplied evidence. Verify the actual change and ask the human to review the outcome before merge. A requested plan review, required cell design, breaking migration or necessary external delivery goes through Preparation. If the need emerges during implementation, keep the candidate and bring the material choice back.

Exercise both cases through the build entrypoint. A compatible bump should author no planning documents and show its first review at Outcome. A bump requiring a migration should show the 1P, Design and Tests before implementation. In later dependency jobs, inspect the route actually taken and the reason for it. A scripted route choice alone cannot show how often agents choose well.

### 8. Give each key document a template

Embed each outline as literal text in the recipe YAML that builds its author’s task prompt. Direction and Preparation share the 1P text. Each writer receives the headings and guidance in the agent call, even in a cell whose checkout contains none of the Recipes guides. Reuse the outline on revisions. Keep the first screen useful on its own. A short answer can be one sentence. The short delivery route uses the handoff and Outcome templates. [1P template and review order](#6-make-the-plan-review-recognizable) · [Stage author prompts](../../../../recipes/adaptive3/prompts/execute.yaml)

#### Design

Use this outline for `review/design.md`. The 1P explains why the change is worth doing. Design gives the implementer a route.

```markdown
# Design
## Approach
<How the proposed change works. Identify the components that change.>
## Affected interfaces
<What callers or other cells will observe. Link any agreement this relies on.>
## Tradeoffs
<A consequential choice, the alternative considered and why this approach fits.>
```

#### Tests

Use this outline for `review/acceptance.md`. Include critical success and failure cases. Mark an exact check as required only when the requester or cell contract requires it. [Test statement format](../../../../AGENTS.md#test-statements)

```markdown
# Tests
## What should work
- <Observable behavior in 30 words or fewer.>
## How we could check it
- <Behavior> — <suggested check>. <File, priority, unit/integration, dependencies>.
- Required check, if any — <exact method and source>.
```

#### Outcome

Use the result as the document title. On a repeat review, the opening sentence says what changed since the version the person last saw.

```markdown
# <Result the person can now review>
<What the person can accept or still needs to decide.>
## What changed
<Observable result. Include interface changes, other cells’ contributions and departures from the plan where relevant.>
## How we checked it
<Promised behavior, observed result and link to evidence for this candidate.>
## What remains
<Known gap, impact and any choice for the requester.>
```

#### Documents and messages used when needed

| When it is needed | Template in reading order |
| --- | --- |
| Explanation or consultation reply | **Answer** — what works today. **Evidence** — a source or observed example. **Limits** — any uncertainty that affects the answer. An answer can finish the thread. |
| Author handoff | **Assignment** — agreed outcome and original decision or agreement. **Next action** — what to do or check. **Where to find the work** — candidate or evidence link. Use the existing handoff message. |
| Implementation note | **What changed** — behavior and candidate. **Checks run** — result and evidence. **Remaining gaps** — what the next author needs to know. Write a separate note only when the handoff needs it. |
| Verification or test results | **Candidate checked** — revision. **Results** — for each relevant behavior, give the check run, what happened, its status and the evidence link. **Gaps** — what an unrun or failed check leaves unknown. Use the Outcome evidence section when it fits. |
| Reviewer finding | **Expected** — promise or contract and source. **Observed** — concrete result and evidence. **Impact** — who is affected and what needs repair. Mark optional suggestions as such. Send the finding in the review thread. |
| Prompt accompanying every human review | Ask for the decision in the agent’s own words. After a question, answer it in this prompt and say what decision is still open. After an edit, say what changed and why the person’s answer matters. Attach the primary document and relevant supporting documents. [Review examples](#present-each-review-as-one-message) |
| Package proposal | **Tools and purpose** — exact package references and reason. **What installation can run** — effects the person would approve. **How we will check** — probe commands. Attach the proposed configuration. |

The recipe already renders the following documents. Keep the layout with its renderer. Ask the producer only for the content it supplies.

| Document | Existing template to reuse |
| --- | --- |
| Negotiation summary | **Why this job was requested** — parent job and transcript links, requesting and receiving cells, parent objective, original request, decision, agreed assignment when present, and delivery status when known. |
| Transcript | **Negotiation transcript** — one speaker heading per turn, followed by that speaker’s recorded words, in order. |
| Delegate decision | **What needs your decision** — blocker. **Suggested next step** and **Your options** — recommendation and tradeoffs. Follow with relevant work already done, request source and evidence. |

Keep these templates at their producers. [Consultation prompt](../../../../recipes/adaptive3/prompts/consultation.yaml) · [Assessment prompt](../../../../recipes/adaptive3/prompts/validate.yaml) · [Package prompt](../../../../recipes/adaptive3/prompts/packages.yaml) · [Negotiation documents](../../../../recipes/adaptive3/negotiation-report.yaml) · [Delegate report](../../../../recipes/adaptive3/backstop-report.yaml)

At integration, use the native merge and publication results for any completion message. Lead with what landed, the commit or receipt, and any remaining action. The implementer supplies the Git subject and body. The recipe appends the job link. [Commit message](../../../../recipes/adaptive3/commit-message.yaml)

Verify that each producing prompt receives its own outline and that generated reports use the recorded data. Sample a standard review, a short-path Outcome and a conditional review such as a package request. Check whether a reader can find the decision, evidence and any gaps on the first screen. Use the headings as writing guidance. A harmless wording variation alone should never send work back to the author.

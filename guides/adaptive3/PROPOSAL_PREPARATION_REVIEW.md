# Adaptive3 proposal for Preparation review and the short path

Move the first human decision for standard delivery to the end of Preparation. At that point a reviewer can decide whether the proposed work solves their problem, whether they agree with the design, and whether the stated evidence would convince them it succeeded. Offer two explicit approvals. For small, well-understood changes, let Direction send the implementer straight to work and bring the result to the human at Outcome.

## Where the decision moves

Today the delivery stages are Direction, Preparation, Implementation, Outcome and Integration. Managed candidate verification runs during Implementation validation. Integration lands and publishes accepted changes. Direction already produces the one-pager. Preparation shares the planning session, develops test statements, and can omit a detailed design. Passing Preparation advances automatically. Outcome currently asks for acceptance or merge, with approval reuse for qualifying retries. [Stage transitions](../../adaptive3.yaml) · [Stage assignments](../../recipes/adaptive3/prompts/execute.yaml) · [Current review routing](../../recipes/adaptive3/review.yaml)

| Delivery route | Before implementation | After candidate verification |
| --- | --- | --- |
| Standard, **Accept to Outcome** | Direction → Preparation → human approves the plan | Produce Outcome and ask the human to accept it. Integrate changed work after acceptance. |
| Standard, **Accept fully** | Direction → Preparation → human approves the plan and authorizes completion within it | Produce and validate Outcome. Complete or integrate automatically when the evidence satisfies the approved criteria. |
| **Short path** | Direction records its rationale and hands the assignment directly to Implementation | Produce Outcome and ask the human to accept it. Integrate changed work after acceptance. |

For an explanation that Direction can answer in full, retain **Accept answer** as the terminal decision. Delivery reviews are distinct from tool authorization, human cancellation and Backstop recovery. Each keeps its own trigger.

## What the human opens at Preparation

The planning author returns one complete review collection. The first three attachments have stable identities and appear in this order. Deep detail can live in additional supporting documents.

| Document | What the reviewer should learn |
| --- | --- |
| **1. One-pager** | The existing Direction brief, including the problem, recommendation, non-goals, expected scope by cell, compatibility and consequential choices. Carry it forward and reconcile it with facts learned in Preparation. |
| **2. Design** | What will change, where, and in what sequence. Cover affected interfaces, owner responsibilities, dependency order, compatibility and rollout where relevant. Detail should be sufficient for a fresh implementer to act. |
| **3. Acceptance criteria** | What observable results constitute success, what evidence will demonstrate each, and when it can be checked. Include Markdown test statements of at most 30 words each, annotated with filenames, importance, unit or integration level, and dependencies. Cover success and failure cases for critical behavior. |

Use the one-pager as the single native overview. Link Design and Acceptance criteria near its top and give them the first two supporting positions. This presents three main documents using the existing review renderer. Planning emits the complete collection whenever it replaces files. Check distinct required attachment IDs, readable content, links, metadata and ordering before independent assessment or human input. The assessor checks that the design delivers the stated scope and the criteria can distinguish success from failure. [Document presentation contract](DOCUMENT_DETAILS.md)

When another agent or cell requested this job, attach the **incoming negotiation report** immediately after the three main documents in the child's Preparation review. Link to it from **Why this job exists** near the top of the one-pager. The reviewer should be able to see who asked, what the parent was trying to accomplish, what the two owners agreed this job would deliver, and why. The report links to the originating negotiation transcript and parent job. Include it even when the child has made no requests of its own. If the requester assigned the work directly without a negotiation, show the original assignment and its source in that position and say how the request arrived.

**Accept to Outcome** means “Implement this plan and bring me the result before completing or merging.” **Accept fully** means “Implement this plan and complete or merge it when its acceptance criteria pass.” Use separate buttons with those consequences visible on the form. Both require empty feedback and no uploads. Questions keep the same packet open. Document comments or a change request return to the planning author and require a freshly validated packet and decision. Scope changes go through Direction first. Keep a requested plan review on the standard route through revisions.

## How Direction chooses the short path

Give the Direction author a structured delivery route, standard or short, and a brief reason. Default to standard when the route is absent or eligibility is uncertain. The existing independent Direction assessment checks the choice against the actual request. The test is whether one brief can tell a fresh implementer exactly what to do and how to tell it worked, with no consequential design choice awaiting the human. This is a judgment about the change, independent of its ticket label.

A tooltip with agreed copy and placement, a CLI option with defined default and error behavior, or a compatible dependency bump with a known regression check can qualify. A dependency upgrade requiring a data migration or delivery by another cell goes through Preparation. Honor an explicit request for plan review. If Implementation discovers a material choice or a new external assignment, preserve the candidate and return to planning before proceeding with the expanded work.

On the short route, pass the validated Direction documents, instructions, scope limits and concrete success checks directly into the implementation session. The current Implementation input defaults look to Preparation, so skipping that state requires an explicit handoff. Use the ordinary candidate preparation and verification steps. At Outcome show the original brief, actual result, evidence and deviations, and require human acceptance even for a no-change result. This route never grants full acceptance.

## How two cells negotiate a request

Call this a **negotiation** in the workflow, agent instructions and review documents. Today the receiving owner already has instructions to inspect its APIs, challenge the request and suggest an alternative. The requester can ask again after an advice reply, and the receiver can consult a third cell. In delivery mode, however, an accepted receiver-authored assignment can go straight to child submission. The requester might first see the counterproposal after the child has finished. Give both parties a turn on the same request whenever the answer changes what would be delivered. The existing `consult` selector and historical job records can keep their names. [Owner instructions](../../recipes/adaptive3/prompts/execute.yaml) · [Consultation routing](../../recipes/adaptive3/consultation.yaml) · [Requester resumption](../../recipes/adaptive3/lifecycle.yaml)

The requester opens with “I want this because…” and gives a concrete consumer case. The receiving owner evaluates that case against its own system. For a validation request, ask what happened, what was expected, and whether the requester saw a failure or wants assurance about a particular risk. Either can justify a check. For a feature, try the closest existing capability against the example. Consider what the consumer would have to build around it, how often, and what supporting a change would cost the owner. One real consumer can justify a small improvement. A speculative future audience is a weak reason to take on a broad new interface.

For example, suppose a consumer asks for a new job-status API because it cannot decide when to stop polling. The owner points to the existing status command. The consumer shows that one state requires parsing a human-readable message. The owner then proposes exposing that state in the command's existing JSON output, and the consumer confirms that this removes the workaround. The resulting assignment is small and its acceptance check follows directly from the example. If the JSON already exposed the state, showing the consumer how to read it could close the request in one reply.

| What the receiving owner finds | What happens next |
| --- | --- |
| The original request is sound and its scope is clear | Accept those terms. The opening request and matching acceptance establish agreement in one exchange. |
| Evidence or intent is unclear | Ask a focused question. Resume the requester and return its answer to the same owner in the same thread. |
| An existing capability may suffice | Show its use on the consumer case. The requester can close the request or explain the remaining gap. |
| A narrower or different change would serve the consumer | Propose concrete behavior and a success check. The requester can accept, counter, or withdraw. |
| The benefit does not justify the work | Explain the tradeoff and any practical alternative. The requester can provide new evidence, change its own plan, or surface the unresolved dependency. |

Keep a single durable thread per request. Resume the appropriate agent session with the prior turns and evidence. Record which proposal each side accepted. Submit a child only for the agreed assignment once the parent stage permits delivery. Planning can reach agreement and reference it later without reopening the exchange just to launch the child. If terms change, resume the thread. Replaying the agreement should resolve to the same delivery. Use the existing finite allowances to stop an exchange that stalls. Return the open question and each owner's position to the parent so it can replan or use Backstop.

## How either job explains a cross-cell request

At Preparation, a reviewer should be able to open the one-pager and see, for every planned external request, **who needs what from whom, why the parent needs it, what the owner actually said, and what happens next**. Give each request its own entry, even when two requests target the same cell. Link each entry directly to its negotiation transcript. Once a delivery exists, add its job link and status. Distinguish a proposed assignment, owner disagreement, pending delivery and verified completion.

Capture the original request and parent objective when negotiation starts. In the summary, explain what evidence or alternative changed the decision and why the final scope serves the consumer. Append the actual exchanges in order, including the receiving owner's proposed assignment and any revised terms. Store the transcript once as a producer artifact or use an existing addressable transcript. Keep a compact list of request summaries and exact producer references in recipe state across negotiation turns, retries and stage changes. A reference should identify the job, task occurrence and artifact or response. This matters because advice runs inline in the receiving workspace and may finish before any delivery job exists. The most recent owner reply in stage feedback cannot represent multiple requests. [Consultation and child submission](../../recipes/adaptive3/consultation.yaml) · [Producer inspection](../JOB_INSPECTION_PLAYBOOK.md)

- **In the parent**, negotiate with planned owners during planning using the existing advice-only mode. Surface the agreements and open questions with the plan. Describe pending or declined requests accurately. Submit agreed delivery through the ordinary execution route after plan approval.
- **In the child**, pass the originating negotiation report and its transcript reference alongside the receiver-authored assignment at submission, using the existing documents input. Put a visible **Why this job exists** entry near the top of its one-pager, Outcome and Backstop diagnosis. Include the parent job, requesting cell, intended parent outcome and the specific contribution requested. A child can see its own obligation without reconstructing the parent story.
- **At Outcome and Backstop**, show the same incoming and outgoing entries with current statuses, including requests added later, failed attempts and outstanding dependencies. Make this available in Backstop even if planning or submission failed partway through. For adopted or directly submitted children, link the actual initiating task and assignment. If no negotiation took place, say so. Retain each original request when retrying delivery.
- **For clickable transcripts**, prefer an existing durable review-accessible link. Where native task links cannot open the exchange, attach the producer's transcript as a selected supporting document and link it with the renderer's supported document link. Verify navigation from both jobs using reviewer permissions. For incomplete or older history, expose the available turns and exact producer locator, and identify the missing part. Keep unrelated nested conversations at their producers.

## How full acceptance reaches Integration

Persist the native Preparation choice, review receipt and exact approved document references in job state. Carry the approved criteria separately from each stage's replaceable review files. At Outcome, the independent assessor matches each applicable criterion to the actual candidate and its verification evidence and records omissions or deviations. Make this report available in the completed job even when full acceptance removes the human stop. Criteria that depend on publication are checked after the relevant integration or publication step.

An ordinary failed check returns to Implementation with its diagnostics. A material change to the agreed behavior, acceptance criteria, or another cell's assignment returns to Preparation for fresh approval, via Direction if scope changed. If the assessor cannot establish that the result is covered, present Outcome for human judgment or enter Backstop for a blocker. A missing or unverifiable full-acceptance receipt requires ordinary human Outcome acceptance. No approval propagates to a child job.

Record two distinct facts for Integration and recovery: the human authorized a particular plan, and a validated Outcome tied that plan to a particular patch and verification result. Today cross-job recovery checks the actual human acceptance workspace against the patch. A Preparation receipt predates that patch. Extend receipt verification to follow both producers, including the target and landed change, before reusing a full acceptance. Keep native Outcome receipts valid for ordinary approvals. Reuse existing patch comparison and fresh verification on equivalent rebases. Reassess a changed patch against the plan before integration. A publish retry after confirmed landing should reuse the landing record. [Approval comparison](../../recipes/adaptive3/compare-approval.yaml) · [Merge receipt verification](../../recipes/adaptive3/merge-receipt.yaml)

## Implementation and acceptance

This fits the recipes cell. Stage routing, review documents, request provenance, decision handling and recipe tests belong here. Receiving cells own their assignments and deliveries. Use the existing review form and artifact interfaces. A new native deep-link capability, if desired beyond linked attachments, belongs with the inspection and review clients.

1. Define the review and routing test statements first. Update the planner and validator contracts, then move the delivery checkpoint in the entrypoint, cycle and review policy. Preserve explanation routing and check package-approval consumers that currently rely on Direction. Carry only explicitly scoped tool authority.
2. Implement requester and receiver turns, capture the agreement and transcript at the source, pass it across child submission and adoption, and expose it to Preparation, Outcome and Backstop. Exercise two requests to one cell, an inline reply with no child, a failed delivery and a nested request. Check the transcript opens at the relevant exchange from each review.
3. Wire the short route and full-acceptance decision through the lifecycle, public review results, correction routes, Integration and recovery. Report the actual human checkpoint and decision mode. Older runs and recovered records lacking the new decision carry only the authority their original receipts establish.
4. Exercise the default build entrypoint and explicit adaptive3 entrypoint with native recipe fixtures. Include these observable release checks:

| Scenario | Expected result |
| --- | --- |
| Standard delivery with a missing design or broken criteria link | Planning receives actionable feedback before a human form opens. |
| Accept to Outcome, then request changes at Outcome | The human sees both checkpoints and revised work returns for acceptance. |
| Accept fully, all criteria met | The human sees one delivery checkpoint. Outcome evidence is retained and the verified candidate follows normal integration. |
| Full acceptance followed by a failed check or changed scope | The failure is repaired and rechecked, or the revised scope is submitted for fresh plan approval. |
| Short-path CLI change; implementation later discovers a migration | A bounded change first asks at Outcome. Discovery of the migration sends the revised plan to Preparation review. |
| Owner counters a broad request with a small enhancement | The requester can demonstrate the remaining gap or accept the revision. Only mutually agreed work starts a child. |
| Existing behavior satisfies the consumer, or the requester withdraws | The thread closes with its rationale. No delivery job is created. |
| A validation request needs more evidence and the turn allowance ends | The parent sees the unanswered question and transcript. The request remains unresolved. |
| A requested child reaches Preparation review without having delegated any work | Its review includes the incoming report. From the one-pager, the reviewer can open the report and follow it to the parent negotiation. |
| Child stalls before preparing its own plan | Its Backstop explains the parent objective and opens the initiating exchange. The parent can identify the same request. |
| Restart, rebase or publication retry | Decisions resolve to the right plan and candidate. Recovery preserves a confirmed landing and surfaces missing approval evidence. |

Roll out the packet and negotiation transcripts with **Accept to Outcome** first. Enable **Accept fully** once integration and recovery can verify its authority, and enable the short path once direct handoff and escalation pass. Check the rendered forms and linked transcripts in a parent/child run before promoting the default build.

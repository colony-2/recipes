# Adaptive3 review options: audit and proposed corrections

Audited 2026-11-13 at recipes `6ffbf4f`. This is an audit and proposal; the
changes below are not implemented.

Adaptive2 usually named the decision and its consequence. Adaptive3 reused one
review activity but lost that distinction in its wording. Keep the shared
activity; restore clear decisions and make the current stage its visible author.

This fits recipes ownership. c2j owns the Python preparation issue, filed
[separately](../BUG_REPORT_C2J_PYTHON_DEPENDENCY_ENVIRONMENT.md). Cortex owns how
native forms are displayed. The immediate presentation improvements below use
existing form fields.

## What became harder to understand

| Situation | Adaptive2 | Current adaptive3 | Proposed primary action |
| --- | --- | --- | --- |
| Direction for a feature or fix | “Approve direction” | “Accept this result” | **Approve direction** |
| Explanation is complete | Review the answer | “Accept this result”; approval can finish the job at Direction | **Accept answer** |
| Repository changes ready | “Accept and merge” | “Accept this result” | **Accept and merge** |
| Outcome without repository changes | “Accept no-change outcome” | “Accept this result” | **Accept outcome**; question says this completes the job without a merge |
| Tools require approval | “Approve tools and validation” / “Do not add these tools” | Ordinary outcome review, with “Accept this result” | **Add tools and run checks** / **Do not add these tools** |
| Automatic attempts exhausted | Choices named the work and number of additional attempts | “Continue with this correction” | **Try another N attempts**, with the proposed correction immediately above |
| Other recovery | A described alternative or scope change | “Continue with this correction” | A concrete action such as **Retry validation** |

Sources: [adaptive2 prompts](../../recipes/adaptive2/prompts.yaml),
[adaptive2 limit decisions](../../recipes/adaptive2/limit-decision.yaml),
[adaptive3 review prompts](../../recipes/adaptive3/prompts/review.yaml), and
[resolver prompts](../../recipes/adaptive3/prompts/resolver.yaml).
Adaptive2's limit forms were too long; retain their explicit consequences without
restoring the long explanation of every possible choice.

### Questions and requested changes are different actions

“Discuss or request changes” combines two intentions. Resolver's “Ask a question
or change the direction” also makes a simple question sound like replanning.

Show **Ask a question** and **Request changes** separately alongside the relevant
approval action. Both use the existing read-only conversation agent. It answers
questions in the review and interprets requested changes; the human does not
choose an internal stage. A question does not approve work or grant more attempts.

Keep native field IDs `feedback` and `annotations`. The inspected Cortex renderer
supports arbitrary choice values and opens feedback after any selection; separate
choices do not require a new input API. Empty question/change submissions must
reopen the form with a short request for text or an attachment. Verify this through
the real renderer before shipping.

Do not restore a recipe failure outcome as a “decline” action. Declining tools
returns that decision to the requesting agent to find another approach. Stopping
the job remains the explicit native cancellation action.

### Resolver can continue without reconsidering new feedback

In [resolver.yaml](../../recipes/adaptive3/resolver.yaml), `continue` with a valid
proposed stage goes straight to completion. New text or attachments are forwarded
but do not cause the resolver to reconsider its existing plan. Explicit model
fields take a different path and are reconsidered.

Ordinary [review.yaml](../../recipes/adaptive3/review.yaml) already handles this
better: approval with feedback goes through the conversation agent first.

Use that same rule for Resolver. Plain approval resumes the displayed proposal.
Approval accompanied by text or attachments goes through the resolver first. It
can incorporate a compatible correction, answer a question, or present a changed
proposal. It must not silently treat conflicting human direction as approval of
its previous plan. Once a stage is chosen, its complete activity cycle runs.

## Make the stage the visible author

The human should see who is asking and what approval does, without reading the
task path. Use the actual stage in the form title. Resolver identifies itself as
**Resolver**, with the interrupted stage stated separately if useful.

Examples:

| Request title | Question | Main choices |
| --- | --- | --- |
| **Direction — Approve Cortex's review scrolling fix** | Approve this direction so detailed planning can begin? | Approve direction · Ask a question · Request changes |
| **Direction — Explain how Cortex restores a conversation** | Does this answer your question? Accepting it completes this job. | Accept answer · Ask a question · Request changes |
| **Outcome review — Merge Cortex's review scrolling fix** | Merge these changes? | Accept and merge · Ask a question · Request changes |
| **Implementation — Add Pillow for image checks** | Add Pillow to this cell's worker configuration after its checks pass? | Add tools and run checks · Do not add these tools · Ask a question · Request changes |
| **Resolver — Restore image checks** | Validation cannot import Pillow. The runtime fix is now deployed. Retry validation in a fresh task? | Retry validation · Ask a question · Request changes |

The last example illustrates a future request after deployment; it is not a claim
that the runtime repair has been deployed.

Keep agent-authored titles descriptive, with a deterministic stage prefix applied
by the review activity. Use the available cell identity when needed to distinguish
work. Preserve that identity when reopening a question. A tool request belongs to
its requesting stage; it is not an Outcome review just because it needs approval.
Keep the complete title within the supported limit, including its prefix. Return
an overlong subject for shortening instead of replacing it with a generic title.

For an exhausted allowance, show the proposed correction and the exact local
allowance, for example: “The browser now starts. Allow 3 more implementation
attempts?” The button must agree with the allowance actually granted.

The current resolver title, “Continue direction: …”, names a destination rather
than its author or immediate problem. Its form also prints agent-settings JSON
on every request. Put model details next to the model controls when needed; keep
the question about the correction the human is being asked to approve. The native
model controls must remain usable if the resolver's agent cannot run.

## What the observed job shows

Job `3M28e5T04Yl6CQBKQpa0Or9Tj4M` captured older recipes `47016ffd5aa3`.
Its saved resolver form at 04:13 UTC has:

- Title: **Decide how to continue**.
- Choices: **Continue with this correction** and **Ask a question or change the direction**.
- A question about delivering a runtime repair through a “bootstrap path”.
- A link to `/tmp/recipe-worktree-2823629518/outbox/review/approve-runtime-repair-and-same-job-recovery.md`.
- Only the scrolling-design document in the form's attached documents.

The linked correction was not attached to that request, and a worker-local path
is not a usable review link. The human was looking at a product design while being
asked to authorize infrastructure work. This is a concrete explanation for the
confusion, separate from the Python failure itself.

Current recipes have corrected the old feedback field names. They still lack a
clear Resolver title and do not select an overview document for Resolver. The
inspected Cortex viewer selects the first ordered/alphabetical document when no
overview is provided, which can put the old design ahead of the current blocker.

Keep simple resolver questions self-contained: what stopped, the proposed
correction, and what approval allows. Do not require a new recovery document.
When existing supporting material is useful, attach it and use a working review
link. If a substantive correction document already exists, select it as the
overview. Do not create internal handoff files or forward every old document.

## Small implementation plan

1. **Separate the decision from the activity implementation.** Keep one review
   activity and the existing prompt includes. At the call site, derive the review
   decision from the stage, work kind, and validated candidate already available.
   Pass only the missing presentation facts. Do not add a compound context object
   or duplicate review state machines. Package approval needs its own decision
   wording and the caller's stage instead of borrowing `purpose: outcome`.
2. **Restore action-specific choices and stage titles.** Use the examples above.
   Add question/change choices to the same conversation path. Preserve approval
   receipts, unchanged-diff approval reuse, and native cancellation.
3. **Align Resolver's feedback handling with ordinary review.** Reconsider new
   human text and attachments before resuming. Show the actual correction and
   allowance. A question keeps the review pending; it does not renew a loop.
4. **Make recovery readable where it is requested.** Put the short correction in
   the question. Reject worker-local links in human-facing review content through
   the existing validation path. Select an existing relevant overview when useful;
   no new document-management activity is needed.

Current native input schemas expose title, questions, options and document
presentation, but no dedicated stage/requester field. Cortex's review queue and
detail page already display the form title, so the stage prefix works now. A
separate stage badge would be a later c2j/Cortex improvement, not a prerequisite.
Keep the shared native `ask` operation; duplicating it per stage would not improve
the human conversation.

## Tests needed when implementing

- Generate real native forms for direction, explanation, changed and unchanged
  outcomes, package approval and Resolver. Assert title, question, actions and
  the resulting recipe path agree. Include forms reopened after a question.
- Render those forms with Cortex's actual adapter and components. Exercise both
  question/change choices, feedback, uploads, and returning to the choices. Check
  stage titles in the review list and detail view, not only the input widget.
- Submit Continue with conflicting scope feedback and with an annotated document.
  Assert the resolver reads it before choosing a stage. A question-only reply
  must neither resume work nor renew an allowance.
- Decline a package request. Assert no probe or config adoption occurs, and the
  requesting agent receives the decision and can continue with another approach.
- Show a resolver request alongside an old design. The correction must be readable
  immediately; a local-only or unattached correction link must not pass review
  validation. Cover agent failure so native model correction remains available.

Existing consumer tests exercise feedback, attachments and model fields. They do
not assert the meaning of approval, the visible stage, package refusal or the
Resolver feedback conflict. The existing resolver attachment test checks that
notes are forwarded while retaining the old stage; that does not establish that
new human guidance was understood.

Inspection used c2j `3fec5e455133` and Cortex `ba5ed5b` source, plus the retained
production form described above. This audit does not claim a new browser test or
a successful worker-environment reproduction.

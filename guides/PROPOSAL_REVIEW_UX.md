# Proposal: useful assets, focused questions, and clear review decisions

Status: draft for discussion; no recipe or runtime changes implemented.

The later [recipe kernel goal](GOAL_RECIPE_KERNEL.md) incorporates this review
approach and supersedes this draft's assumptions about retaining `evolve` and
initializing missing mandates. Its target uses `build` and optional `PURPOSE.md`.

This proposal responds to [Recipes-Review-UX-Request.md](../Recipes-Review-UX-Request.md).
It uses the existing native review pattern: `input`, `form.kind: review`, stored
documents, and ordinary question fields. It proposes changes to recipe content
and orchestration, without making a new input framework a prerequisite.

The recipe work fits this cell's mandate. c2j owns input validation, persistence,
and review identity; Cortex owns rendering and submission. Any gaps found in
those capabilities should be demonstrated and discussed with their owners.

## Recommendation

Treat a review as a small, purposeful package:

1. **Assets:** the proposal, question context, or outcome that the person needs
   to inspect, with supporting evidence available alongside it.
2. **Questions:** the specific information or judgment needed from that person.
3. **Direction:** an explicit account of what their response will cause next.

The same review mechanism serves clarification, plan approval, outcome acceptance,
and requests for changes. Those situations need different content and questions.
A person should be able to understand why they were interrupted and give a useful
answer without reconstructing the workflow's internal state.

Keep explanations with the assets. Give question fields short, actual questions.
Use choice controls for real alternatives. A text answer or returned document
does not need an extra one-option choice that merely means “submit.”

## What the current recipes do

Inspected recipes at `d569722` and c2j at `6a25847a90d0`.

- `plan_feedback` combines results from design, design review, test planning,
  test review, and implementation into a single question as serialized JSON.
  Several entries can be absent or left over from an earlier iteration.
- `implementation_feedback` does the same for implementation and its reviews.
- Agents provide `summary` and `next`; `ask_user` does not require an explicit
  question. The recipe consequently cannot reliably distinguish an explanation
  from the answer it needs.
- Plan feedback always returns to design, even when a later phase asked the
  question. Most forms always offer the same document uploads.
- A request for changes without text or files can produce another form without
  explaining what is missing.
- The outcome title says “verified” even when the verification recipe reports
  that no automated verification ran because `build.sh` was absent.

Sources: [development workflow](../recipes/develop/develop.yaml),
[agent result contracts](../recipes/develop/agent.yaml),
[verification reporting](../recipes/develop/verify.yaml), and
[native review authoring](../GUIDE-Review-Recipe-Authors.md).

Changing “Revise the plan” to “Send answer” would improve one label. The larger
improvement is to author the review around the current decision and its assets.

## What a person should see

Each review has a specific title, the relevant documents, and a small set of
questions. Important caveats must be visible in the main review asset, rather
than discoverable only in raw logs. Full documents remain available; readability
must not depend on truncating an agent's explanation.

### Clarification

Illustrative review title: **Choose how long to retain completed job history**.

The attached `review.md` explains:

> The requested history view needs a retention period. The request does not
> specify one, and I found no existing retention policy in this repository.
>
> A longer period helps investigate older incidents but retains more data.
> I suggest 90 days as a starting point; this is a proposed product decision,
> not a requirement discovered in the repository.
>
> Your answer will be incorporated into the design. The resulting design and
> test plan will still come back for approval before implementation.

The questions are:

- **How long should completed job history be retained?** Choices: 30 days,
  90 days, or a different policy.
- **If you want a different policy, describe it here.** Optional text, required
  by the recipe's continuation rules when that alternative is selected.

There is no additional “Revise the plan” question. Submission answers the
question; it does not approve a plan. No choice is preselected.

For an open question, use an ordinary text field instead. For a request such as
“Which existing policy should govern this behavior?”, allow an explanation or a
supporting document when either would answer it. Do not manufacture choices
when the agent does not know the alternatives. Use other supported field types
when the requested information genuinely calls for them.

### Plan approval

Review title: **Review the job-history retention plan**.

Assets: the design and test statements. The design begins with a readable
overview of the proposed behavior, scope, important tradeoffs, external work,
and unresolved limitations. On a revision, it also explains what changed in
response to the previous review.

The decision question is **May implementation proceed with this design and test
plan?** Its choices are **Approve this plan** and **Request changes**. These are
real workflow alternatives, so a decision field is appropriate. Retain the
existing internal values `approve` and `revise`.

Offer **Comments or requested changes** and annotations of the available
documents. State: “Approval starts implementation. Requested changes return the
plan for revision and another review.” A comment is not required for approval.

### Outcome acceptance

Review title: **Review the completed job-history change**.

Assets: the implementation summary and verification report, with the approved
design and test statements available for comparison. The summary describes
achieved behavior, departures from the plan, and limitations. Verification
status comes from the recorded checks, rather than the agent's confidence.

The decision question is **What should happen to this candidate?** Choices:

- **Accept and merge** — incorporates the reviewed candidate into the named
  upstream branch.
- **Request implementation changes** — keeps the approved requirements and
  returns the candidate for revision, verification, and another review.
- **Change the plan** — returns to design and requires renewed plan approval.

Retain the existing values `satisfied`, `revise`, and `redesign`. Explain the
merge consequence before submission. If verification was skipped, say
**“Automated verification was not run”** prominently. This proposal makes that
status explicit; changing the policy that permits skipped verification is a
separate decision.

### The missing-mandate example

The newly added setup flow already handles an absent mandate through a child
build. Absence alone should not become another question for the parent user.
The child presents its inferred responsibility boundary as a design asset for
the normal plan review. If inspection exposes a real ownership ambiguity, it
asks about that specific boundary with the evidence and alternatives available.

## Preparing the review

### Let the working agent author the questions

Extend the recipe-owned agent result contract so that `next: ask_user` includes
an explicit human-review request: a title and question definitions using the
existing input field vocabulary. Require an accompanying `review.md` when the
question needs rationale or supporting context beyond the available documents.
The agent should usually ask one question, or a few closely related questions
that can sensibly be answered together.

The producing agent already knows the uncertainty. It should identify what is
unknown, explain why it matters, and offer a recommendation when justified.
Do not add a separate model call merely to extract a question from a long
summary. Do not serialize the result object into the human-facing form.

The recipe validates the request, binds available artifacts, and owns the
continuation. Generated questions collect task information; they cannot add
approval actions, override gates, or choose arbitrary destination states.
Reserve recipe-owned field names such as `decision` to avoid collisions.

For approval reviews, keep the decision and its alternatives authored by the
recipe. Improve the existing design and implementation assets' opening summaries
instead of generating another mandatory document that repeats them. A short
review note is useful when several assets need an explanation tying them together.

### Assemble only the current evidence

Carry the source phase, the current question, and relevant artifact references
explicitly into the review. Do not infer the current blocker by concatenating
every state that has ever produced a result.

Include documents that help answer the question. Offer annotation uploads only
for documents actually present. A request for an external policy may separately
offer a supporting-file field even when no draft document exists yet.

The primary asset should make these points easy to find, in ordinary prose:

- What is proposed, completed, or unresolved?
- Why does the user need to act now?
- What evidence, alternatives, and limitations matter to this decision?
- What will happen after the response?

These are authoring guidelines, not mandatory empty headings. Detailed evidence
belongs in supporting assets. Internal phase results remain in job execution
details for debugging.

## Using the response

| Situation | Meaningful response | Continuation |
| --- | --- | --- |
| Agent asks a question | The requested choice, answer, or supporting file | Return the exact response to the phase that asked; retain downstream gates. |
| Plan ready for approval | Approve, or request changes with text/files | Begin implementation, or revise and present the plan again. |
| Outcome ready for acceptance | Accept, request implementation changes, or change the plan | Merge the reviewed candidate, revise and reverify, or return to design approval. |
| User requested changes but supplied no direction | Text or annotated document describing the changes | Return to the relevant author, without asking the user to select “revise” again. |
| Work belongs outside this cell | Acknowledge the assessment, or revise the request | Complete without a local merge, or reassess the revised request. |

“Return to the phase” means the logical workflow phase, using its established
session policy. A test-plan question should not automatically restart design.
An answer that changes approved scope must still trigger design approval.
Changes to an artifact invalidate dependent reviews and verification as required;
an answered question never substitutes for those approvals.

### Insufficient or contradictory responses

Where a text answer is mandatory, use the native required-field and type checks.
The recipe must also check for meaningful non-whitespace content before
progressing; a required field alone is not a sufficient continuation rule.
Where text **or** an attachment is sufficient, keep both fields individually
optional and check the combination in the recipe. Likewise, selecting “a different
policy” requires the explanation that makes that answer actionable.

If that check fails, present the same question and assets again with a specific
explanation: “Please describe the requested change or attach an annotated
document.” A whitespace-only answer must not cause an unexplained repeat.
Carry forward the attempted response as context so the follow-up does not lose
valid information. Under today's recipe-level check this is a new review
occurrence; do not claim it is validation within the original pending form.

Returned annotations remain requests for revision. An approval accompanied by
edited assets must not merge a changed candidate. Preserve the existing rule
requiring revision and another review, and explain it alongside the upload
questions. Plain comments accompanying approval retain their current meaning as
notes; the form should clearly tell users to choose “Request changes” when edits
are required. Do not use a model to reinterpret an explicit approval decision.

Original documents stay immutable. Pass the exact accepted answers and returned
artifacts to the next phase, separate from originals and previous review responses.

## Existing capabilities and limits

This design starts with native `title`, `documents`, `fields`, field validation,
and existing review submission and receipt handling. A clarification review can
have answer/upload fields without a `decision` field: that name has no built-in
meaning in c2j. The ordinary client submission completes the form.

Short prompts work in the existing field `question`. Longer context is an asset.
The recipe should not depend on Cortex recognizing a build phase, interpreting
JSON, or promoting a particular field into a button. Cortex's existing action
rendering can improve the presentation of real decision choices; other clients
can show them as ordinary choices with the same semantics.

Do not invent `intro` or `actions` properties in recipe YAML. c2j also has generic
structured input and presentation hints, but its documented review pattern uses
ordinary fields and cannot be mixed with structured schemas. There is no need
to switch review protocols to solve the problem described here. Reference:
[c2j structured input and review guide at the inspected revision](https://github.com/colony-2/c2j/blob/6a25847a90d0303f700bbade1bda7f67d858ce48/GUIDE-Structured-Input-And-Review.md).

Evaluate the resulting native forms in Cortex before proposing API additions.
For example, if a short review note is hard to discover among documents, discuss
generic document presentation with Cortex. If accepted empty responses cannot
be explained adequately through a follow-up review, discuss validation with c2j.
Neither is assumed to require a new contract in this proposal.

## A related workflow policy to consider separately

Current critic `revise` results often lead straight to human feedback. When a
critic has already provided actionable findings within approved scope, the
author can often address those findings without asking the human what to do.

I recommend evaluating bounded author/critic revision loops as a follow-up.
Escalation should explain the unresolved disagreement or decision, the attempts
already made, and the useful direction a human can provide. Scope changes and
actual human questions still require the appropriate review. This changes when
the workflow interrupts people, so it should be assessed separately from the
content and form improvements above.

## Proposed rollout and validation

First, improve asset summaries and replace JSON dumps with the current phase's
human-readable explanation. Make feedback labels accurate and show why an
insufficient response is being requested again. Preserve existing approval and
annotation rules.

Next, add explicit questions to `ask_user` results and route answer-only reviews
back to their originating phases. Support legacy results during migration with
a plain-language explanation and answer field; never fall back to raw JSON.
Version recipe contracts and update producer prompts, consumers, and fixtures
together. Preserve recorded forms for running jobs. Any later removal of legacy
result support should follow the separate deprecation process.

Validate the resulting forms and transitions in the native recipe runner, then
inspect their rendering in Cortex. Use the same generated review structure for
different domains, including ownership, product choices, and missing evidence.

Acceptance outcomes for that implementation:

- Clarification displays a specific question and relevant assets without raw result JSON or empty phase sections.
- Text, meaningful choices, and appropriate attachments answer questions without a redundant one-option decision control.
- Answers reach their originating phase; scope changes still require renewed plan approval.
- Plan and outcome approval retain explicit decisions and state what proceeding will do.
- Whitespace-only feedback produces useful guidance; attachment-only responses work where a document is a valid answer.
- Annotations require revision and another review, including when submitted alongside approval.
- Revised reviews present current assets, explain changes, and preserve earlier documents and responses.
- Outcome reviews distinguish passed, failed, and skipped verification in human-readable content.
- Build and evolve follow the same conventions; recipe-specific meaning stays out of Cortex's generic renderer.

These are proposed outcomes, not claims of implemented or tested behavior. This
draft changes no recipes, prompts, gates, or input APIs.

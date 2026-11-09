# Adaptive2: review the real outputs before rollout

**Current status:** `build.yaml` now selects adaptive2 for new submissions.
See [the rollout assessment](ROLLOUT.md). The plan and initial trial results below
record the earlier opt-in milestone; pending capabilities remain identified.

**Status: initial slice implemented, 2026-11-08.** See the [implementation assessment](IMPLEMENTATION.md) and
[actual trial packets](results/README.md). The broader cohort below remains the rollout plan.
[Examples](EXAMPLES.md) are handwritten; the result packets are actual live outputs.

The experiment has two questions: does the recipe enforce the right checkpoints,
and can a human understand the documents its agents actually produce? Use native
tests for the first and live recipe runs for the second.

## Implementation and review order

1. **Agree the shape.** Review [PROPOSAL.md](PROPOSAL.md), especially the explanation
   exception and reuse of explicitly approved child briefs. The detailed design
   records the proposed defaults rather than leaving implementation to guess.
2. **Build the smallest runnable slice.** Start adaptive2 from current adaptive;
   wire the new initial prompt, consultation summary/history, one-pager, and real
   `input` checkpoint. Keep the production entrypoint unchanged. Run a feature/UI
   case and a bug case with live agents in disposable cells. Stop at the checkpoint
   and present the actual produced documents for review.
3. **Revise with examples in view.** Record what the human could not understand.
   Adjust instructions and templates, then rerun the affected cases. Retain both
   versions; do not silently edit the model's output into a successful example.
4. **Complete the path.** Add detailed planning, explanation completion, approved
   prerequisites, child approval reuse, and outcome presentation around the existing
   implementation/recovery loop. Continue the accepted live cases through real
   changes, verification, and final review in their disposable repositories.
5. **Compare and decide.** Review outcomes from all four assignment types, run the
   native regressions, and write an implementation-versus-plan assessment. Promote
   adaptive2 only after its real documents are useful. Default routing stays a
   separate decision, not a side effect of passing tests.

This deliberately puts reviewable live output early, before building the entire
variant. It does not ask the human to debug recipe YAML or judge abstract prompts.

## A small live cohort

Use fixed small fixtures with real code and documentation. Keep fixtures realistic
enough to reveal choices, but small enough that inspecting their outputs is easy.
Record exact request, fixture revision, recipe revision, runtime/op identities,
job/task IDs, human responses, and retained artifact references.

| Case | What should be visible |
| --- | --- |
| Feature with UI and another cell's existing alternative | A one-pager and mockup; consultation grounded in the existing interface; no unnecessary implementation child; final screenshots and tests. |
| Reproducible bug with initially uncertain cause | Expected versus observed behavior; uncertainty acknowledged; approved direction; an actual regression test and result. |
| Explanation requiring repository inspection | Direct answer with sources and limits; no implementation, package request, or merge review unless actually needed for the scoped question. |
| Oversight with two owners | Parent problem, typed child assignments, dependency order, full exchanges, suspension/resumption, and combined outcome evidence. |

For delegated work, inspect the receiving cell's authored handoff and follow its
artifact reference into the child. Include a requester objection that makes the
receiver revise the assignment. Verify that the final document uses the structure
of its declared work type and that the requester did not rewrite it at dispatch.

In the oversight case, include a failed child with a useful retained artifact and
a corrected retry. This checks that the new presentation preserves recovery and
explains what changed between attempts. Include an unanswered consultation issue;
the summary must preserve it instead of calling the discussion an agreement.

Include a proposal with enough consequential design questions that its Q&A table
is the largest section. Check that important questions and answers remain visible
in full, with useful grouping and explicit unresolved choices. A shorter packet
that omits those choices is not an improvement.

Use the native recipe execution path from the
[authoring guide](../RECIPE_AUTHORING_GUIDE.md):
`c2j submit --recipe-file ... --run --embed`, with explicit disposable cell and
test JobDB configuration. Inspect `c2j self` before submission. Use real packaged
Codex operations, normal managed workspaces, artifact bindings, and input forms.
Do not use canned model responses for these quality trials.

For human-facing trial checkpoints, retain the actual review form and response.
Scripted human responses belong in routing tests and must be labeled as such;
they do not count as a human finding the document understandable. Keep trial
publication in disposable repositories. Do not mutate or resubmit audited
production jobs or create real external cells to manufacture an example.

## What to present from each run

Put a short index first, then the actual files:

- Original request and the first one-pager as shown to the human.
- Mockups, consultation summary, and readable replies, including open objections.
- Receiver-authored typed handoffs and the agreed versions actually supplied to children.
- One intermediate view while waiting or recovering, with its producing task/time.
- The approved direction, any revision, and the eventual outcome review or answer.
- Supporting tests/evidence and the concrete human feedback on the presentation.

The run index states which parts were live and which were fixture setup. A failed
model invocation or missing credential is a failed/unavailable trial, not evidence
of a prompt defect or a passing substitute. Deterministically rendered sample
Markdown does not satisfy the live-run requirement.

Assemble the initial feature/bug packets first and pause for document feedback at
the real review checkpoint. Do not overwhelm the reviewer with four full runs at
once. Compare one representative current-adaptive packet with the adaptive2 packet
for the same fixture/request; use comparable model settings and disclose differences.

## Human evaluation

Someone who did not follow the job should be able to answer these from the primary
document, opening supporting links only when they want more detail:

1. From the title alone, which cell, kind of work, and specific change or question is this about?
2. From the opening, who needs the result, why, and what decision do I need to make?
3. What is proposed or achieved, and what are the important design choices and answers?
4. What did other cells recommend or challenge, and what is still unresolved?
5. What was actually verified, and what remains outside the scope?
6. What changed since I approved the direction?

Also check that an observer can trace a child's request back to the parent's
original problem and find the actual replies without reading JSON or a full job
log. Record confusing phrases, unnecessary pages, missing context, and mistaken
claims. Evaluate how quickly the expert becomes oriented and can make a sound
decision. Use rough reading time and document length as signals, not automatic
pass/fail scores. A long, necessary Q&A section is acceptable; omitted important
questions, generic titles, and short but misleading summaries are failures.

This evaluates our workflow's outputs. It is not a benchmark of whether Codex is
generally intelligent, and no assertion on prompt wording proves comprehension.

## Native regression acceptance

These statements were written before implementation. The table retains the target
coverage and proposed file organization; the implementation assessment identifies
what now exists and what remains. Each behavior needs a positive and relevant negative case.
Use [native testing](../NATIVE_RECIPE_TESTING.md) with real state, artifacts, review
receipts, workspaces, and child operations; mock only the external decisions.

| Statement | Importance; level/dependencies | Proposed files |
| --- | --- | --- |
| Delivery waits for direction approval; revisions and unanswered reviews cannot start implementation. | Critical; integration, c2j | `recipe-tests/adaptive2/direction-review.test.yaml` |
| Approval binds the reviewed document version; later edits cannot silently replace it. | Critical; integration, c2j artifact storage | `recipe-tests/adaptive2/direction-review.test.yaml` |
| Detailed planning follows approval, and implementation starts in a fresh writable session. | Critical; integration, c2j workspaces/checkpoints | `recipe-tests/adaptive2/phase-persistence.test.yaml` |
| A completed explanation returns its answer without creating changes or requesting a merge. | High; integration, c2j | `recipe-tests/adaptive2/explanation.test.yaml` |
| Consultation history preserves original requests, public replies, unresolved questions, and nested exchanges. | High; integration, c2j artifacts/workspaces | `recipe-tests/adaptive2/consultation.test.yaml` |
| A human can open the primary review and its selected sources without unrelated documents crowding the review. | High; integration, c2j input/artifact bindings | `recipe-tests/adaptive2/review.test.yaml` |
| A child receives necessary parent context and the selected handoff, while unrelated parent files remain unbound. | High; integration, c2j children/artifacts | `recipe-tests/adaptive2/handoff.test.yaml` |
| Dispatch preserves the agreed receiver-authored handoff's artifact identity and work type; a requester-written replacement is rejected. | Critical; integration, c2j consultation/children/artifacts | `recipe-tests/adaptive2/handoff.test.yaml` |
| Receiver revisions replace earlier drafts; referrals obtain the actual owner's handoff, and completed advice creates no unnecessary delivery child. | High; integration, c2j consultation/children | `recipe-tests/adaptive2/consultation.test.yaml` |
| Explicitly reviewed child briefs reuse approval; absent, fabricated, or changed scope cannot silently bypass review. | Critical; integration, c2j review receipts | `recipe-tests/adaptive2/delegated-direction.test.yaml` |
| Approved prerequisites can run during planning; unapproved delivery cannot, and the planning workspace stays read-only. | Critical; integration, c2j permissions/workspaces | `recipe-tests/adaptive2/planning-dependencies.test.yaml` |
| Oversight waits for required results, handles child failure, and never equates submission or agreement with completion. | Critical; integration, c2j children | `recipe-tests/adaptive2/oversight.test.yaml` |
| Adaptive2 children use the intended adaptive2 revision rather than silently returning to adaptive. | High; integration, c2j recipe resolution | `recipe-tests/adaptive2/routing.test.yaml` |
| Unchanged rebases reuse merge approval; changed work receives a focused review referencing the accepted candidate. | Critical; integration, c2j native Git/input | `recipe-tests/adaptive2/rebase-approval.test.yaml` |

Port the existing recovery, cancellation, package approval/probe, verification,
artifact identity, permission, and merge regressions to the variant where affected.
Also run adaptive's existing suites to detect accidental shared-helper changes.
Mocked decisions can establish scope-change routing; live trials must establish
whether the agent recognizes and explains a real scope change.

## Stopping point and report

Finish a bounded trial cycle with `assessment.md`: implemented versus planned,
actual commands/results, document links, human feedback, remaining gaps, and a
recommendation to iterate or promote. Do not claim success merely because all
headings exist. No production switch or removal of final human review is implied.

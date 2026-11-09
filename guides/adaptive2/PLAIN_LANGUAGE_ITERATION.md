# Speak as the owner, explain the work

The first trial sounded like an administrator describing agents. The prompts
asked for agreement, ownership accounting, evidence, and phase distinctions in
every reply. The trial request itself contained those instructions. The result
repeated the workflow instead of explaining a recommendation.

This is a recipe-owned communication fix. Keep the existing approval and
handoff rules; change how the participants are addressed and what they write.

## Changes

1. Tell each participant which cell it owns and whom it is speaking with. Use
   first person for its own proposals and commitments, and address the other
   owner directly. Keep roles and routing fields in the recipe.
2. Have the requester explain the user problem, proposed work, and specific
   advice it wants. Put the proposed requirements in `request.md` when useful.
   The receiver examines them, explains what it would change and why, and
   writes the revised assignment in `work/handoff.md`.
3. Make replies conversational: the recommendation, important differences,
   and any question the other owner must answer. Keep checks and API details
   in linked evidence unless they explain the recommendation.
4. Write design documents directly about the problem and proposed solution.
   Their title and placement establish their purpose. Include concrete limits
   that affect the decision, without repeating workflow status or disclaimers.
   Keep all important design questions and answers.
5. Give the live trial an ordinary product request, with requirements in a file.
   Remove instructions about consultation phases from its opening message.

The requester supplies an initial proposal, not the receiving cell's final
assignment. The receiver still writes and revises that assignment. A meaningful
question should produce another reply; an acknowledgment alone needs no turn.

## Example of the intended exchange

This example is illustrative, not a recorded model response.

**Notebook:** “People sometimes overwrite a note and need the earlier text back.
I'd like you to keep its last three saved versions. I've put the requirements in
`request.md`. Does this fit your API, and what would you change?”

**Storage:** “I can keep the earlier versions. I suggest adding a way to read
them and using our existing save operation to restore one. That avoids a second
way to update a note and keeps the protection against overwriting someone else's
edit. I've written the revised request in `work/handoff.md`.

“One choice affects how much history people get: do you mean three earlier
versions, or three including the current note? I recommend three earlier versions
so users have three restore choices.”

A concrete limitation belongs where it matters: “The current code keeps drafts
in memory, so we need persistent storage to recover them after a restart.”
That explains a consequence. “The deployed persistence layer remains unidentified”
does not orient the reader or say what needs to happen.

## Checks

Native tests check participant/workspace identity, request-file delivery, public
reply attribution, and the unchanged handoff/approval rules. They do not grade
writing. Run a fresh live consultation, retain its actual files separately from
the first trial, and assess whether its recommendation and differences are easy
to understand. Leave prior results unchanged for comparison.

## What changed and what the runs showed

Implemented the five changes above in the adaptive2 prompts. One shared writing
instruction now applies to the working agent, consultants, and reviewers. The
consultation recipe passes the actual speaking and receiving cells into the
initial instructions, and its transcript identifies speakers by cell name.
The response schema describes `reply` as a direct message to the other owner.
Approval, execution, and handoff-identity rules remain unchanged.

The first live revision used first person but still opened with “This fits
storage” and appended a test-pass sentence. I tightened the reply instructions
to lead with what the owner can provide and explain the consequential changes.
Routine validation results belong in the linked evidence.

The [refined conversation and new one-pager](results/2026-11-08-owner-voice/README.md)
both completed successfully with actual Codex calls. The consultation now says
“I can keep earlier versions” and explains why restoring through the existing
save operation protects another tab's edits. The one-pager starts with the lost
note and recommended correction. The important questions remain in the documents.

A further presentation fix uses the assignment's descriptive title when a short
summary has no heading. This avoids a generic “Consultation” title without
requiring every message to follow another template. A native replay of the
recorded live reply verified that change; it did not generate new agent prose.

All **13 native adaptive2 cases pass**, including the added checks within existing
cases for identity, request-file delivery, reply attribution, and descriptive
titles. Reports: `/tmp/adaptive2-human-language-final`,
`/tmp/adaptive2-owner-design-live`, `/tmp/adaptive2-owner-conversation-final`, and
`/tmp/adaptive2-owner-title-replay`. Runtime remains c2j 0.0.124.

These examples are better aligned with the requested conversation. The linked
assignment is still detailed and merits review on its own. No test can establish
that every future reply will be clear; these runs provide concrete examples for
the next review. The original adaptive recipe and previous generated documents
were not changed.

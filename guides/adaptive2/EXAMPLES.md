# Adaptive2: what a human would read

These are **handwritten examples**, not outputs from live jobs and not claims about
existing cells or APIs. The fictional notebook/storage example demonstrates the
proposed reading order. [Live trials](TRIALS.md) must replace these with actual
artifacts before we judge whether the prompts work.

## First review: one-pager.md

**Review title and document heading: Approve 1p for notebook feature: save drafts while typing**

> **Feature request · notebook · Awaiting direction approval**
> Let people leave a note and return without losing their text.

### Problem Description

People lose unfinished notes when they move to another page. They should be able
to return to the most recently saved text without remembering to press Save.

### Non Goals

Offline editing, shared editing, and recovery of text typed before this change.

### What we are planning to do

Save while the person types and show **Saving**, **Saved**, or **Could not save**.
Restore the saved draft when the note opens. If another tab has changed the note,
keep the person's text and explain the conflict rather than overwrite either copy.

Notebook will use storage's existing draft API. The consultation found no need
for the new autosave endpoint we first proposed. A preview attached to the real
review would show saving, failure, and conflict states.

### Compat/Upgrade

Existing notes continue to open. No data migration or new storage endpoint.
Two-tab conflicts will become visible instead of silently replacing newer text.

### Key challenges/design questions & answers

| Question | Answer |
| --- | --- |
| Do we need storage to build an autosave API? | No. Its current draft write supports conditional updates; see the consultation. |
| What if saving fails? | Keep the text on screen, show the failure, and allow a retry. Closing the page can still lose unsaved text. |
| What if two tabs edit the same note? | Keep both versions and ask the person which text to retain. |

This example has three key questions. A real proposal keeps all important questions
and their answers, even when the table becomes the largest section. Grouping by
topic helps with a long table; a page or word target never removes a question.

**Decision:** Approve this scope, request changes, or stop this work.

## Supporting consultation: summary.md

**Title: Storage advice for notebook: reuse the draft API for autosave?**

> **Explanation · notebook asks storage · Answered**
> Parent problem: people lose unfinished notes when leaving the page.

**Asked:** Can storage add an autosave endpoint that preserves the latest draft?

**Answer:** Use the existing draft write with the version returned by the last
read. Storage rejects an outdated version instead of silently replacing newer
text. No storage change is needed for the agreed online scope.

**What changed in our thinking:** Notebook proposed a new endpoint. Storage
pointed to the existing one. Notebook challenged whether it handles two tabs;
the conditional-write example answered that concern. Notebook still needs to
present a conflict without discarding the person's text.

**Still excluded:** This does not save text while offline. The one-pager names
that limit; the human can change the scope if offline work is essential.

**Next:** Notebook implements saving and conflict feedback. Storage has no
implementation assignment. The API example and full exchange are supporting
documents in the real review.

## One level deeper: conversation.md

**Title: Notebook and storage: saving drafts without overwriting another tab**

This illustrates public replies, not hidden reasoning. Real transcripts retain
the actual wording and producer references; they are not rewritten to sound better.

> **Notebook — request:** People lose drafts when moving between pages. Could you
> add an autosave endpoint? We need to restore the latest text when they return.

> **Storage — reply:** The current draft write already stores text. Send the
> version from the last read to avoid replacing a newer write. I'd reuse it;
> another endpoint would duplicate that behavior. It does not provide offline saving.

> **Notebook — reply:** What happens if two tabs start with the same version? We
> must not let the later write silently erase the earlier one.

> **Storage — reply:** The first write advances the version. The second receives
> a conflict. The attached API example demonstrates that case. Keep the user's
> text while they resolve it. No storage implementation is required.

## Intermediate view: progress.md

**Title: Notebook draft saving: checking conflicts and save failures**

> **Feature request · notebook · Implementing the approved plan**
> Draft saving now works in one tab. We are checking two-tab conflicts and how the
> failure message looks. Storage confirmed that its existing API is sufficient.
> No human decision is needed now.

The real document would link the approved one-pager, consultation summary, and
latest test evidence. It would identify its producing task and time.

## Final review: merge-review.md

This example describes a hypothetical completed implementation. Its test results
are illustrative, not evidence from this repository.

**Review title and document heading: Merge notebook feature: save drafts while typing**

> **Feature request · notebook · Merge the draft-saving change?**
> People can return to saved drafts. The agreed checks passed. Recommend merging.

### What changed

Notes save while typing and restore when reopened. Saving, failure, and conflict
messages show whether the text is safe. The implementation matches the approved
one-pager; current UI screenshots accompany the real review.

### What we needed others to do

Storage explained how to use its existing API safely. Its consultation changed
our approach; it did not require a new endpoint or a child implementation job.

### How we tested

| Expectation | Result |
| --- | --- |
| A saved draft returns when the note reopens. | Passed. |
| A failed save preserves the text and offers retry. | Passed. |
| A second tab cannot silently replace newer text. | Passed. |

The real rows link to the relevant test evidence. Current results, not design
intent or a consultant's agreement, establish these outcomes.

### What we did not do

Offline saving remains excluded. Closing the page after a failed save can lose
unsaved text; the UI warns about that. Offline drafts are a possible follow-up.

### Interfaces and upgrade

No new public API or migration. Notebook now uses storage's conditional-write
contract and displays its conflict response.

### Changes from the approved plan

None.

**Read more:** Approved plan; consultation; test results; current screenshots.
Full file accounting and logs are available as supporting/diagnostic evidence.

## The other assignment types

These examples show their opening frames. Features, bugs, and oversight use the
same five one-pager headings; their content changes with the problem.

**Approve 1p for checkout bug: prevent duplicate charges after a timeout**

> A failed payment request can be retried as a new charge. Expected: one charge
> for one purchase. Observed: two charges after a timeout. We plan to reuse the
> same payment key when retrying and add a timeout regression. Refund processing
> is outside this fix. We still need payments to confirm how long it retains keys.

**Storage explanation: why saving from a second tab causes a conflict**

> A second tab gets a conflict because its draft version is old. Reloading gets
> the latest version, but discard nothing until the person has saved or copied
> their current text. The API example shows the conflict response. We have not
> checked whether the current notebook UI handles that response correctly.

No merge question is needed for this answer. A requested investigation of the UI
would have its own explicit scope.

**Approve 1p for root oversight: make payment retries safe across checkout and payments**

> Make payment retries safe across checkout and payments. First confirm the
> payment-key lifetime. Then payments fixes retry handling while checkout adds
> its retry UI. Finally checkout runs the combined timeout scenario.

| Work | Assignment | Owner | Order |
| --- | --- | --- | --- |
| Confirm the payment-key lifetime | Explanation | payments | First |
| Preserve the charge identity across retries | Bug report | payments | After the answer |
| Offer retry without starting a new purchase | Feature request | checkout | After the answer; alongside the fix |
| Check the full timeout/retry journey | Part of the agreed checkout acceptance | checkout | After both changes |

In a real job, each row links its brief, conversation, and actual attempt/result.
The root summary distinguishes work merely agreed from work completed and checked.

## When follow-up work is needed: the receiver's handoff

In this separate fictional example, checkout asks payments to fix retry behavior.
**Payments writes and revises this handoff.** Checkout checks that it addresses
the problem; the coordinator passes the agreed document to the payments child.

### Payments bug report: retry a purchase without charging twice

**Work type:** Bug report (`bug`). **Receiving cell:** payments.
**Requested by:** checkout.

**Parent problem:** A customer may pay twice when checkout retries after a timeout.
Checkout needs a retry of the same purchase to return the original charge.

**Expected / observed:** Reusing the payment key should reuse the charge. In the
reported timeout case, the retry created a second charge. The underlying cause
still needs investigation; the report is not proof of a particular defect.

**Scope:** Fix retry handling for the same payment key. Preserve existing behavior
for different keys. Checkout UI changes and refunds are outside this assignment.

**Completion:** A regression reproduces the reported timeout case and passes
with the fix. Repeated requests with one key produce one charge; different keys
still permit separate purchases. Report any compatibility implications.

**Inputs and open questions:** Include the reported request sequence and selected
logs. Confirm the supported key lifetime from payments' existing contract and
record any constraint checkout must observe. Link the parent problem and agreed
consultation in the real handoff.

This is a bug assignment, not a pasted consultation prompt. A feature, explanation,
or oversight handoff uses its corresponding structure in the [design](DESIGN.md).

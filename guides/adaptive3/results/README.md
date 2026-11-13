# Actual adaptive3 review examples

These files came from live agents using the new recipe activities in disposable
repositories. The generated documents are preserved as written. Human messages
were scripted test inputs; they were not a production user's approvals.

| Trial | Start here | Outcome |
| --- | --- | --- |
| Preserve a notebook draft after closing the browser | [One-pager](notebook/review/durable-local-draft-saving.md), then [human question and answer](notebook/dialogue.md) | Execute, full Validate and human dialogue/acceptance passed. |
| Recover old saves using the storage cell | [Request, receiver response and assignment](storage/dialogue.md), then [receiver's proposal](storage/review/five-version-recovery-proposal.md) | Receiver challenged a redundant API. Execute, full Validate and independent Review passed. |

## What these show

The notebook one-pager keeps the important questions: storage failure, empty and
identical text, multiple tabs, privacy and ownership. The review agent directly
answers whether drafts survive closing the browser and leaves the item pending
until explicit acceptance.

The storage receiver explains that a restore endpoint would duplicate the existing
version-checked update. It also challenges recording identical autosaves and warns
that rapid changed autosaves can evict older versions. The receiver writes the
proposed feature assignment, including the notebook cell's separate UI ownership.

## What still needs judgment

The notebook document is roughly 700 words. Its opening is understandable, but
some operational discovery notes and process commentary could be shorter. The
answer also repeats that the proposal remains pending, which is unnecessary for
the human's question. Those are observations about the actual outputs, not edits
made to make the trial look cleaner.

The storage proposal is more direct and shows useful disagreement. It grounds its
claims in the fixture's code and distinguishes documented HTTP behavior from code
available to inspect. The completed retry passed from Execute through Review. An earlier trial hit
model capacity and correctly returned `stuck` while retaining its proposal.

Neither example establishes UI screenshot relevance, real cross-cell delivery,
or full live implementation and merge. See [test results](../TEST_RESULTS.md) for
the deterministic coverage and remaining live work.

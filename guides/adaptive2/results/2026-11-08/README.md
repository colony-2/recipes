# First adaptive2 documents to review

The later [owner-conversation iteration](../2026-11-08-owner-voice/README.md)
responds to feedback on this first set. These originals are retained unchanged.

These are actual Codex outputs from disposable notebook and storage cells. Start
with the bug one-pager. **The feature trial timed out before submitting its
review; its files are retained drafts.** The HTML is a proposed UI, not an
implemented feature.

| Example                                                       | Start here                                                                                                                                     | Supporting material                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bug:** importing text loses the last note                   | [Direction review](import-last-note/one-pager.md)                                                                                              | [Original request](import-last-note/request.md), [progress](import-last-note/progress.md)                                                                                                                                                                                  |
| **Feature/UI — incomplete run:** save drafts while typing     | [Draft one-pager](draft-saving/one-pager.md)                                                                                                   | [Interactive mockup](draft-saving/mockup.html), [desktop image](draft-saving/evidence/mockup-saved.png), [conflict image](draft-saving/evidence/mockup-conflict.png), [mobile image](draft-saving/evidence/mockup-mobile.png), [original request](draft-saving/request.md) |
| **Receiver-written assignment:** recover earlier saved drafts | [Short consultation summary](receiver-handoff/summary.md), then [storage's feature handoff](receiver-handoff/iter1/consultant/work/handoff.md) | [Full recommendation and alternatives](receiver-handoff/iter1/consultant/summary.md), [actual exchange](receiver-handoff/conversation.md)                                                                                                                                  |

The useful tension in the feature example is concrete: storage found that its
existing API could support autosave, but also found a concurrent-write bug. It
proposed a narrow bug fix instead of simply agreeing to add a new endpoint.

The history example makes different choices visible: whether “three versions”
includes the current draft, whether identical saves consume history slots, and
which cell owns the UI. Storage wrote the assignment itself. Its full summary
and handoff are still lengthy; that is a presentation issue to assess, not a
reason to remove important unresolved questions.

## Feedback that will shape the next iteration

1. Does the title and opening explain the problem and decision quickly enough?
2. Which language or sections can be simplified without losing a necessary choice?
3. Can you follow the original request, the other cell's recommendation, and the
   proposed work without reconstructing the story from logs?

The bug run reached the review in about four minutes. The feature run completed
its consultation and generated a 3,452-word one-pager, mockup, and eleven passing
browser-check groups, then stopped producing events. Its 30-minute deadline
expired without a final response or review form. The cause remains unresolved.
The files are useful for presentation feedback, but this is a failed live trial.
The [check report](draft-saving/evidence/validation.md) distinguishes simulated
UI behavior from unverified service behavior.

No human has approved these directions. A scripted **stop** at the bug review
allowed the native harness to export its packet. The feature never reached that
step. No product implementation or merge followed. The proposed fixes have not
been delivered.

The receiver's live response completed successfully, but its test had an invalid
assertion expression. That expression and the summary-link renderer were fixed
and checked by replaying the **recorded live response** through the native recipe.
The receiver's authored files are byte-identical to the live originals; only the
recipe-rendered summary index and conversation heading changed. This is not a
second live model evaluation.

Each folder's `run-metadata.json` records hashes, native reports, job/task and
artifact references where available, and review forms where present. The feature
drafts came directly from the producing outbox before cleanup; they were not
published task results. These are disposable test
identities, not production jobs available on the remote JobDB. Generated prose
has not been edited. [Earlier attempts](earlier-attempts/README.md) record failures
and incomplete exports rather than hiding them.

See the [implementation assessment](../../IMPLEMENTATION.md) for what is built,
tests, and the remaining work before rollout. The current adaptive entrypoint
remains unchanged.

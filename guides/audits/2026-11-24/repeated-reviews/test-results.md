# Verification of the repeat-review changes

The tests exercise the public build recipe and its production review, consultation and recovery includes. They script agent decisions and human replies. c2j executes the forms, transitions, artifact checks, child handling and merge steps selected by each case.

| Area | Checks exercised |
| --- | --- |
| Reviews | A question becomes the next prompt. A commented attachment reaches the author. Multiple messages share a document version. Revised documents keep the review ID. Each approval records the request and revision the person saw. |
| Delegate | Reuse a covered plan with its earlier receipt and completion choice. Send a formatting repair to the author. Explain a new tradeoff to the human. Preserve the displayed action during a clarification. |
| Consultation | Deliver a paraphrased request from the correct agreement when two agreements have the same owner. Reuse the existing child on retry. Propagate nested agreements. Reject advice, stale offers and unaccepted amendments. Exercise four rounds and ten distinct threads independently. |
| Documents | Embedded templates reach the writer. The 1P opens first. Unchanged stored attachments retain their descriptions. Replacements need a description. A broken supporting link preserves a readable human question. |
| Build | Approval with guidance reaches the author and reviewer. Review before Complete stops at Outcome. Take to Completion can use earlier approval after verification. Short and standard routing have distinct fixtures. |

104 distinct native c2j cases passed across the focused suites and build cases, including the local-provider check below. The publication tests covered delivery in the caller’s published ref and recovery from a recorded child. Three publication cases timed out when run concurrently and passed on serial replay.

The checkout started at `2aa5580`. The tests use the repository’s c2j pin, `source:a6de3eca42509bb9caac1ac2f8af74b37319c192`. Run individual native suites with `c2j test run --file recipe-tests/adaptive3/<suite>.test.yaml`. The main regression suites are `agreement-reference`, `repeat-decision`, `review`, `review-routing`, `limits`, `backstop` and the selected cases in `build`.

Two Chromium checks passed against Cortex checkout `c379635`. Both opened the original and revised attachments, followed two questions and a requested edit, and recorded an approval comment. One restarted the worker and reloaded the page between replies. The native receipt, selected revision and uploaded notes survived.

After removing the title suffix, both browser checks displayed “Saved drafts” on the revised plan and the explanation in the next message. The three repeat-decision cases and the clarification case passed with the original thread and receipt behavior.

The real Codex runner completed two read-only answering turns against a local scripted provider. It resumed the same session and read the original document and the earlier upload on both turns.

All 40 Python validator tests passed. The purpose-document checks and the recipe timeout check passed. The timeout check covered 141 workflow and example files.

The scripted jobs establish what the recipe does with a given decision. To measure how often authors choose the short route and delegates spare the human a repeat approval, sample new jobs using this recipe revision and count both outcomes against the number eligible. The original four jobs retain their captured recipes.

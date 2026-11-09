# Review examples from the implementation trials

Start with the [phone review](phone-review/merge-review.md). Its
[390 × 844 screenshot](phone-review/phone.png) is an actual Chromium capture of
the changed page. The review's local links resolve within the selected packet.
The image and generated documents were exported unchanged from native artifacts;
[run metadata](phone-review/run-metadata.json) records their hashes and producers.

The limit trials retain the actual question body and its choices:

| Situation | Generated brief | Choices and receipt |
| --- | --- | --- |
| Contact import needs more work | [Implementation](limits/live-implementation-choice-brief.md) | [Recorded form](limits/live-implementation-choice-brief.json) |
| Gallery omits an existing screenshot | [Report correction](limits/live-mechanical-report-brief.md) | [Recorded form](limits/live-mechanical-report-brief.json) |
| Request conflicts with keeping existing behavior | [Scope decision](limits/live-scope-choice-brief.md) | [Recorded form](limits/live-scope-choice-brief.json) |

These are isolated local trials from November 9, 2026, using c2j 0.0.124
(`33e2a4de4e99d3a577a38dca4b8de33d43a099ce`) and the changes on top of recipes
`1c7cdc7`. Codex generated the assessment, summaries and decision explanations.
The harness supplied the human choices so the trials could finish. No production
jobs were answered, and no application code was published.

The UI trial starts with an implemented static page and recorded capture. It
exercises live assessment, summary, selection and final attachment validation;
it is not a complete live design-to-merge job. That is why its review says no
separate approved one-pager was supplied. The verification document distinguishes
actual page evidence from unavailable tooling and backend behavior.

The briefs identify practical next steps, but model prose and the deterministic
facts repeat some information. The merge review also spends space on absent
evidence that was outside this trial. These are presentation issues to watch in
the next audit; the original outputs are retained so reviewers can judge them.
The mechanical-report trial's model could not use `c2j job log` through the CLI
available inside its agent environment. The native test engine used the pinned
version, but this trial does not prove that every agent environment has that CLI.

See [test results](../test-results.md) for deterministic coverage and runtime
limitations, and [implementation](../implementation.md) for the assessment against
the plan.

# Build document reviews

Build uses native `input` forms with `kind: review`: documents alongside focused
questions and structured choices. The shared helper is
[`recipes/kernel/review.yaml`](../recipes/kernel/review.yaml).

Plan review presents design, test statements, and expert evidence. The reviewer
can approve, request changes, or cancel. Outcome review adds implementation and
verification evidence; acceptance authorizes squash merge of the tested candidate.
The reviewer can instead request implementation revision, change the design, or
cancel. These are actual decisions, not one-choice acknowledgments of JSON dumps.

Both reviews accept optional text and annotated files. Guidance or uploads require
revision and another review even when the selected decision is approval. A revision
without either repeats the review with an explanation of the missing direction.
Clarification requests use the agent's focused questions and supporting documents,
then resume the same phase. Answers and attachments are delivered as artifacts;
`feedback.json` preserves the exact questions and response. Technical control
artifacts are excluded from the human document list.

Independent assessments run through consultation. The consultant decides agreement
and reports a separate `assessment` verdict. Agreement that a defect exists cannot
pass the build. Iteration exhaustion or deconfliction invokes the consultation's
own synthesis and human direction step before further negotiation.

A successful review is insufficient to merge on its own. The candidate needs a
passing independent outcome assessment, successful executable verification, all
approved prerequisites completed, and explicit outcome acceptance. Changed work
returns through inspection and verification. Changed scope returns through design
and plan approval.

The build exports `reviews` receipts, `artifact_refs`, `verification`, and its latest
session checkpoint. Native review response transport and attachment persistence
remain c2j/Cortex responsibilities; the recipe tests exercise their supported API.

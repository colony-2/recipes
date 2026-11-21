# Ask people a question

Use `ask.yaml` when work needs a human reply, including confirmation of a required
manual package publication, deployment or worker upgrade. It opens the existing
review v2 presentation once and returns the complete reply and native receipt.
It runs no model, deployment or Git publication operation and leaves the caller's
repository unchanged.

If the change you requested is complete but you have a non-Git dependency (such as
a Nix package, c2j library deployment or server update) and do not observe the updated
state, use this recipe to ask a human to inform you when deployment is complete.
If you already observe the required updated state, continue your check. Git-only
dependencies need no extra question. Optional deployment must not delay source
acceptance. A merged c2j change does not establish that workers are running it.

## Submit from Adaptive

Write these inputs to a scratch file, replacing the revision and environment with
the actual values. Preserve literal question text; do not interpolate it into shell
code. This question asks a person to tell you when deployment is complete.

```yaml
title: Confirm c2j worker upgrade
question: |-
  c2j revision <revision> is merged. Please upgrade the workers serving
  <environment>, then confirm they run this revision or a later version
  containing the change. The dependent compatibility check is waiting.
directions:
  - id: available
    label: Available now
    feedback_mode: forbidden
    allow_attachments: false
    continues_review: false
  - id: unavailable
    label: Not available
    feedback_mode: optional
    allow_attachments: true
    continues_review: false
  - id: reply
    label: Other reply
    feedback_mode: required
    allow_attachments: true
    continues_review: false
```

After the entrypoint and its helpers are published together, submit in the caller's
cell using the Recipes Git selector. Do not attach the application candidate or
copy Recipes helpers into its repository.

```sh
c2j submit "Ask about required publication." --self \
  --advanced-recipe 'git+https://github.com/colony-2/recipes.git//ask.yaml@main' \
  --inputs-file /tmp/publication-question.yaml --json
```

Submit once, then end the agent turn. Adaptive records the child and waits through
its existing durable child path. Do not use `--run`, poll in an agent loop or submit
another matching question while the first remains active. Native input can remain
pending until answered or cancelled; this recipe imposes no execution timeout.

## Read the answer

After Adaptive resumes, inspect `c2j job result JOB --json`. Read `request` and the
complete `native` result, including `native.response.direction`, `feedback`,
`attachments`, `settings` and `native.receipt`. For example, `available` with empty
feedback and files confirms the exact condition in the frozen question; `unavailable`
completes the question just as successfully but leaves the dependency unresolved.
The recipe does not interpret choice IDs or return readiness/approval booleans.

The child collector forwards only a short summary, capped at 2,000 characters.
That summary and a successful terminal status establish only that someone replied.
If the final result is absent, inspect tasks with `c2j job log JOB --json`, copy the
exact task occurrence ID and discover pointers with
`c2j job fields JOB --task "$TASK" --json`. Download complete values with
`c2j job log JOB --task "$TASK" --field POINTER --output FILE`; an empty pointer
downloads the full task output. Use scratch outside the checkout and outbox.
Retrieve needed stored files through native artifact inspection/materialization.

Continue the dependent check only after explicit confirmation applicable to the
requested version and environment. An ambiguous reply, a negative reply or an upload
alone provides no such confirmation. Preserve it and explain the remaining
dependency; ask a focused follow-up if clarification is needed. Diagnose failed or
cancelled questions using their actual outcomes and respect cancellation and newer
human direction. Keep successful upstream source delivery separate from deployment.

## Contract

| Input | Meaning |
| --- | --- |
| `title`, `question` | Required nonblank strings, preserved exactly. |
| `prompt` | Optional CLI submission text, unused by the form. `c2j submit` requires a prompt argument. |
| `directions` | Optional nonempty array of review v2 choices; all require `continues_review: false`. |
| `documents` | Optional native `artifact_map` of selected stored evidence; default `{}`. |
| `document_metadata` | Optional review v2 titles, purposes, roles and order for attached evidence; default `{}`. |
| `overview_document_id` | Optional attached ID to open first; omit when unused. |

The default choice is `reply`, labelled **Send reply**, requiring meaningful text
or a permitted new stored upload. Original evidence cannot satisfy required
feedback. Caller-defined choices retain their feedback and upload policies. The
shared [review v2 validator](https://raw.githubusercontent.com/colony-2/recipes/refs/heads/main/guides/REVIEW_V2.md) rejects malformed declarations before
input opens; native input rejects invalid replies. There are no settings or
conversation loops.

| Output | Meaning |
| --- | --- |
| `request` | Exact builder snapshot, including generated review identity and original evidence. |
| `review_id` | Snapshot's review identity. |
| `native` | Complete unchanged input-op result, response, receipt and native references. |
| `summary` | Short navigation message naming the selected direction, not a readiness claim. |
| `artifact_refs` | Original evidence under `originals/ID`; uploads under `feedback/REQUEST/INDEX/BASENAME`. |

Exported names distinguish duplicate basenames while retaining their stored
producer coordinates. The original references in `request` and `native` are
unchanged. Resume the same pending job rather than opening a duplicate question.

Existing review v2 workers and clients are required. An installation too old to
open the question needs an existing operator contact or human-review route for
its upgrade. The shared builder retains its existing source-declared Python
dependency. This adds no installation approval route or deployment automation.

See the [acceptance statements](https://raw.githubusercontent.com/colony-2/recipes/refs/heads/main/recipe-tests/ask-statements.md) and native
question suites for pre-merge checks. Fixture answers do not establish a production
deployment; the consuming assignment still needs its actual dependent check.

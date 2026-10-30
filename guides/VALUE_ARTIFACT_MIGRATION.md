# Value artifact migration and job investigation

## Scope and ownership

This change fits the recipes cell: it replaces recipe-owned JSON/text transport
and diagnoses orchestration behavior. The execution-engine compatibility issues
found during validation belong to c2j; see
[the runtime report](BUG_C2J_VALUE_ARTIFACT_COMPATIBILITY.md).

The implementation uses [c2j's value-artifact API at `66cbded`](https://github.com/colony-2/c2j/blob/66cbded46995627f08c562092d98098f38404b4d/pkg/artifacts/guides/VALUES.md).
A runtime containing that capability is required. The tested current main also
needs the runtime corrections described in the linked report before these
recipes can pass their full validation on an unmodified runtime.

## Ten migrated nodes

| Recipe | Former transport | Replacement |
| --- | --- | --- |
| `recipes/develop/develop.yaml` | `write_build_context`, `CONTEXT` | Named JSON value in the agent's documents map |
| `recipes/light/develop.yaml` | `write_build_context`, `CONTEXT` | Named JSON value in the agent's documents map |
| `recipes/light/develop.yaml` | `write_heavy_handoff`, `HANDOFF` | Named JSON value forwarded into the heavy route |
| `recipes/kernel/consultation.yaml` | `publish_consultation_transcript`, `CONVERSATION` | Value bound into inbox, then copied to outbox for archival |
| `recipes/kernel/review.yaml` | `write_review_feedback`, `FEEDBACK` | Named JSON value containing questions and response |
| `recipes/kernel/repair.yaml` | `write_response_repair_evidence`, `DETAILS`/`ISSUES` | JSON and text values from an empty sequence |
| `recipes/develop/merge-review.yaml` | `CANDIDATE`/`RESULT` environment values | JSON inbox files read by the existing renderer |
| `recipes/light/synopsis.yaml` | `CANDIDATE`/`RESPONSE`/`VERIFICATION` environment values | JSON inbox files read by the existing renderer |
| `create.yaml` | `write_created_cells_manifest`, `CREATED` | Named JSON value used by registration and repair |
| `recipes/build/hooks/settings.yaml` | `write_settings`, `SETTINGS` | Normalized settings exported as a named JSON value |

Seven writer tasks are eliminated. The two Markdown renderers retain their
validation and output behavior. The transcript task deliberately remains: its
stored reference is the public continuation handle. Archiving it prevents the
entire transcript value from being copied recursively into later consultation
inventories.

Document names and JSON structures are preserved. JSON sources receive native
objects, without `json_stringify`; the worker writes JSON and a trailing newline.
Text sources preserve exact text. Settings retain their 16,000-character API
limit and duplicate consultation-key check. No workflow decision, consultation
threshold, approval gate, or retry policy changes in this migration.

Value-backed inbox files are temporary. Human-review attachments and explicitly
exported standalone job results use c2j persistence. A removed writer no longer
has its own downloadable output chapter; the enclosing recipe must export a
document when it should be a job deliverable. Ordinary job-input, declaration,
and op-output limits still apply.

## Job `3LIeAglwSRxG36xoys9kJOwiy19`

The local chapter export contains **162 chapters, ten parent context writes,
and nine parent development-agent turns**. It does not show a hundred parent
agent/context iterations. There are 18 agent responses in this export: nine
parent turns, one plan assessment, and eight recovery-expert turns.
The child jobs' internal histories are not included in that count. A nineteenth
output with a `response` key is the human input op at chapter 76, not an agent turn.

| Context chapter | Parent agent chapter | Phase and requested next action | Context bytes |
| --- | --- | --- | ---: |
| 9 | 10 | Design: consult ten serving cells | 714 |
| 21 | 22 | Design: continue, despite saying independent work was complete | 6,125 |
| 23 | 24 | Design: blocked with an invalid empty key list | 6,047 |
| 26 | 27 | Design: blocked with the ten correct consultation keys after repair | 7,071 |
| 68 | 69 | Design: review the agreements | 75,824 |
| 70 | 71 | Test plan: review | 76,003 |
| 79 | 80 | Implement: submit ten approved prerequisites | 76,537 |
| 101 | 102 | Implement: wait for those ten jobs | 78,019 |
| 143 | 144 | Implement: request six recovery/scope assessments | 107,973 |
| 159 | — | Context writer failed before the next agent turn | 453,842 |

Most intervening chapters perform consultation submission, waiting, result and
artifact retrieval, prerequisite submission, and expert exchanges. The export
records ten serving-consultation child submissions, ten prerequisite child
submissions, and seven transcript writes (one plan assessment and six recovery
assessments). The six recovery assessments took eight agent turns; one required
three responses rather than one.

There is avoidable churn: chapter 22 requested `continue` when it could have
returned `blocked` with the outstanding keys, and chapter 24 required correction
because it supplied no keys. The recorded repair and coordination transitions
then progressed. This evidence does not establish an infinite orchestration
loop. An unbounded series of future `continue` responses remains a separate
liveness concern; this transport migration does not introduce an arbitrary turn
limit.

### Why recovery consultations appeared

The old prerequisite submissions (chapters 82–100) reused a consultant session
and prompts beginning “Agree to a documentation-only prerequisite”. Those are
consultation instructions, despite the new job being an implementation job.
Later assessments identify agreement-only evidence and missing completed work
for several children. This is strong evidence of a consultation-to-execution
handoff defect, rather than successful execution simply being overlooked.
The parent export alone does not prove every child's individual failure cause.

By chapter 143, five children reported `implemented`, three `unchanged`, and two
failed. The parent considered four satisfactory and requested six assessments,
including reconciliation of a recipes-child scope exception. Those assessments
largely agreed that revision/recovery was needed; agreement on findings is not
acceptance of completed implementation.

Current [prerequisite coordination](../recipes/develop/coordinate.yaml) already
addresses the handoff in commit `111d099`: prerequisite
builds explicitly start a fresh execution session, explain that consultation is
complete, and receive the agreed evidence. Commit `4732b8f` also makes up to 40
ordinary serving consultations inline. The recorded job used recipes revision
`21d9c4456296215433f31ed3374624926c9c320a`, before both fixes.

### The terminal failure

Chapter 159 put **453,842 bytes into one `CONTEXT` environment value**. Bash failed
to start with `fork/exec /usr/bin/bash: argument list too long` (exit -1). There
was no subsequent parent agent turn. Chapter 161 recorded the terminal failure.

The `threads` portion alone was about 421 KB, roughly 93% of the final context.
The six additional expert records expanded duplicated state and artifact
inventories; this was not primarily the embedding of document file bodies.
Environment transport made that ordinary state growth fatal before any command
could write `context.json`.

The migrated heavy and light agents receive the context as an inbox value
artifact, so this payload no longer becomes a process environment entry. This
fix does not shrink the context, change the history of an already pinned job,
resume publication, or recover the prerequisite children automatically.

## Validation

Synthetic fixtures avoid committing the private job export. See
[payload transport test statements](../recipe-tests/payload-transport-statements.md).

- Unmodified c2j main: a real command reads and compares 2 MiB JSON/text values,
  including Unicode, quotes, newlines, template syntax, and shell metacharacters.
- With the isolated runtime correction: heavy builds reach their mocked agents
  at 64 KiB, 128 KiB, 512 KiB, and 2 MiB; light builds at 512 KiB.
- Real commands compare 512 KiB repair/synopsis data with the diagnostic runtime.
  A stored 512 KiB consultation transcript also compares exactly on unmodified
  c2j. Review feedback and normalized hook settings are materialized and checked.
- The existing native suites exercise consultation resume, handoff, review,
  repair, registration, validation failures, hooks, and completion routing.

The test runner omits inbox content over 64 KiB from `calls[].artifacts`; the
large-build cases assert successful agent invocation and absence of environment
transport. Separate real-command cases check exact bytes instead of relying on
that truncated observation channel. Full validation reports 277 valid cases. Runtime testing, using the diagnostic
correction where required, yields 276 passing cases and the independently
reproduced `prepare-new-hook` failure. The linked compatibility report records
commands, targeted reruns, and exclusions.

Standalone embedded smoke job `3LOY7mzSGoTL8AukSP3904FZOZB` also completed on the
unmodified runtime with the test statements attached. It used an isolated local
JobDB, preserving the existing database:

```bash
c2j submit 'Validate large value artifacts' \
  --advanced-recipe-file recipe-tests/fixtures/value-artifact-smoke.yaml \
  --inputs-file /tmp/value-smoke-inputs.json \
  --artifact recipe-tests/payload-transport-statements.md \
  --cell /src --run --embed
```

The input file contains `bytes: 2097152` and a short literal marker containing
Unicode, quotes, a newline, shell metacharacters, and `${{ literal }}`. The large
body is computed inside the recipe rather than embedded in the submitted input.

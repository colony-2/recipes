# Adaptive2: work that humans can follow

The default workflow selected by root [`build.yaml`](../../build.yaml), based on adaptive. Start with the
[proposal](../../guides/adaptive2/PROPOSAL.md),
[implementation assessment](../../guides/adaptive2/IMPLEMENTATION.md), and
[actual review packets](../../guides/adaptive2/results/README.md).
See the [rollout assessment](../../guides/adaptive2/ROLLOUT.md) for coverage and remaining gaps.

`build.yaml` accepts the existing adaptive inputs. The first agent identifies a
feature, bug, explanation, or oversight assignment. Delivery work produces
`one-pager.md` and waits for an explicit direction review. Approval leads to
detailed design and test statements, then a fresh implementation session. A
straightforward explanation can finish with `answer.md`.

The first review preserves the exact approved artifact. Important questions have
no length or count limit. The final review explains changes, dependencies, tests,
omissions, interface changes, and differences from the approved plan.

Consultations run inline in the receiving cell's managed workspace. The receiver
checks existing alternatives, summarizes the exchange, and authors any follow-up
`handoff.md` as one of the four assignment types. The requester can challenge it;
the coordinator forwards the receiver's accepted documents for execution.
`conversation.md` preserves public replies and links their selected documents.

The fork changes framing, review transitions, consultation presentation, and
handoff validation. Unchanged helpers are included from `../adaptive/`: package
policy/probes, artifact bindings, child watching, verification, and Git operations
continue to use the existing mechanisms. The revised orchestration and prompt consumers live here; unchanged helpers remain
shared with adaptive.

## Run and inspect the workflow

Use the runtime pinned by [`.c2j-version`](../../.c2j-version) and the
[native testing setup](../../guides/NATIVE_RECIPE_TESTING.md):

```sh
c2j test run --directory recipe-tests/adaptive2 --case-timeout 3m --out-dir /tmp/adaptive2-native
c2j test run --file recipe-tests/adaptive2/live-review.live.yaml \
  --include-live --case-timeout 30m --artifact-mode inline \
  --artifact-max-bytes 262144 --out-dir /tmp/adaptive2-live
c2j test run --file recipe-tests/adaptive2/receiver-handoff.live.yaml \
  --include-live --case-timeout 20m --artifact-mode inline \
  --artifact-max-bytes 262144 --out-dir /tmp/adaptive2-receiver
python3 recipe-tests/adaptive2/export_review_packet.py \
  /tmp/adaptive2-live/cases/import-last-note-direction/result.json \
  /tmp/adaptive2-review/import-last-note
```

Live trials use actual packaged Codex calls, disposable registered cell fixtures,
native workspaces and artifact transport. They need working Codex authentication
and the normal c2ops/Nix environment. Only the stop response at the first direction
review is scripted; it exports the documents without approving or implementing
the proposed work. Native regression cases script agent decisions instead.

The default child selector is `build`, preserving the normal repository-local
recipe resolver and customizations. The shared public entrypoint runs adaptive2.
The default consultation selector names adaptive2 and runs inline. Explicit
`build_recipe` and `consultation_recipe` overrides remain available. Publish this
change before submitting remote jobs that resolve the repository's `main` branch;
existing jobs retain their captured recipes. Creation uses the existing workflow.

Initial live documents are available for review. Reusing a parent's approval for
a child brief, executing approved prerequisites during planning, and a complete
live oversight/recovery/merge trial remain follow-up work in the assessment.

## Human replies and automatic limits

Human questions and review rounds have no recipe turn limit. A new collected
human response renews the automatic allowance; asking the question, presenting
the review, and processing the reply do not spend it. This includes direction,
outcome, consultation, and package decisions. Reusing a saved response or an
automatic package-policy decision does not renew it.

`max_iterations` defaults to zero (disabled). A positive value limits consecutive
automatic implementation work. Response correction still allows two retries;
unchanged operational blockers allow three correction turns. Consultations retain
their per-round automatic limit. New human direction in nested advice also renews
the suspended caller's round. Native Git retries remain bounded, with a new human
response starting a fresh allowance. Runtime execution/time budgets remain separate.

The recipe uses existing input receipts and task history. Custom consultation
recipes that collect human direction should return `review_receipts`, an array of
their native input response receipts, so the calling build can recognize it.
Keep each original receipt's request and submission identifiers; do not generate
replacement identifiers or reconstruct receipts from model output.

Execution forwards the receiver's accepted handoff references. If a parent
republishes a selected file, the recipe compares its bytes with the agreed file.
An identical copy uses the original. A changed copy returns a file-specific error,
restores the agreed inbox document, and preserves the proposed edit under
`error/rejected-handoff/`. Additional recovery and feedback files remain selected
explicitly. Multiple possible agreements require the original consultation's
handoff directory; the recipe does not guess which scope to execute.

See the [incident and plan](../../guides/adaptive2/PROPOSAL_AUTONOMOUS_TURN_LIMITS.md)
and [implementation assessment](../../guides/adaptive2/turn-limits/implementation.md).

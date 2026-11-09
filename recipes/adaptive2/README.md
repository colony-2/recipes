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
the coordinator checks the accepted artifact's identity before execution.
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
c2j test run --directory recipe-tests/adaptive2 --out-dir /tmp/adaptive2-native
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

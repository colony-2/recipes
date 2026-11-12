# Creation helpers

These helpers remain because the root-owned [`create.yaml`](../../create.yaml)
uses them. Adaptive owns its own agent, consultation, recovery, artifact and
review implementation in `recipes/adaptive/`; it does not include this kernel.
The retired heavy/light coordinators and consultation kernel have been removed.

| Helper | Retained responsibility |
| --- | --- |
| `agent-turn.yaml` | Fresh/resumed creation agents, schemas, checkpoints and artifact collection. |
| `artifact-result.yaml` | Resolve declared file references against actual artifacts. |
| `artifact-annotations.yaml` | Collect descriptions and identity-bound source associations. |
| `artifact-namespace.yaml` | Namespace attachments while preserving immutable references. |
| `repair.yaml`, `recovery.yaml` | Correct invalid creation responses with preserved evidence. |
| `review.yaml` | Human clarification, proposal and recovery forms. |
| `review-content.yaml` | Collect evidence and construct a current deterministic brief. |
| `review-presentation.yaml` | Packaged presentation policy for this helper. |
| `review-synthesis.yaml` | Optional model synthesis with validation and deterministic fallback. |

The renderer in [`render/op.yaml`](render/op.yaml) executes the producer program
bound by `review-content.yaml`. It returns typed presentation metadata through
the extension result protocol. Briefs, full evidence and provenance remain artifacts.
A command's stdout preview is not a complete structured result and must not be
parsed as one when it can exceed the preview limit.

Model synthesis remains disabled by the production caller. This was an explicit
choice in commit `1b9846a`, pending evaluation on the original reviews. The approved
“Remove recipe-imposed timeouts” bug fix supersedes its former deadline prerequisite
and all synthesis age cutoffs. Content-quality release gates remain. The opt-in
branch has native contract coverage with scripted model responses, which does not
establish model quality. Runtime defaults, authority bounds and cancellation still apply.
Adaptive agents already author their own review summaries; this extra synthesis
branch belongs to creation's retained review helper.
See [review brief behavior and the activation history](../../guides/REVIEW_BRIEF_PRODUCTION.md).

Tests retain native artifact resolution, review forms, repair, large evidence,
annotation lineage, registration and publication boundaries. See `recipe-tests/`
and [the cleanup assessment](../../guides/ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md).

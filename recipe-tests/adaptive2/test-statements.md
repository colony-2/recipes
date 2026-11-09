# Adaptive2 initial review slice

These statements precede implementation. Native cases script model decisions;
live trials evaluate the actual produced documents separately.

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| A2-1 | Delivery cannot reach detailed planning or implementation before direction approval. | Critical; integration, c2j | `direction-review.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-2 | Requested changes return to framing with feedback; approval retains the exact reviewed one-pager. | Critical; integration, c2j artifacts/input | `direction-review.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-3 | A straightforward explanation returns a sourced answer without implementation or merge review. | High; integration, c2j | `direction-review.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-4 | Consultations expose original questions, public replies, receiver-written typed handoffs, and unresolved issues as readable documents. | High; integration, c2j workspaces/artifacts | `consultation.test.yaml`, `recipes/adaptive2/consultation.yaml` |
| A2-5 | Execution accepts the agreed receiver handoff and rejects a requester-authored replacement. | Critical; integration, c2j | `handoff.test.yaml`, `recipes/adaptive2/coordinate.yaml` |
| A2-6 | Live review packets preserve important design questions and name the cell, work, and decision clearly. | High; live integration, c2j/Codex/human review | `live-review.live.yaml`, `recipes/adaptive2/prompts.yaml` |
| A2-7 | Public build uses adaptive2; the previous adaptive workflow remains available to its own regression tests. | High; integration, c2j | `direction-review.test.yaml`, `recipes/adaptive2/build.yaml`, `build.yaml` |
| A2-8 | Recovery can add selected evidence while preserving the receiver-authored assignment; replacing the assignment requires a new agreement. | Critical; integration, c2j artifacts/children | `handoff.test.yaml`, `recipes/adaptive2/coordinate.yaml` |
| A2-9 | Each consultation participant receives its own cell identity, the other owner, and selected request documents; the transcript attributes replies to the actual speaker. | High; integration, c2j workspaces/artifacts | `consultation.test.yaml`, `recipes/adaptive2/consultation.yaml` |
| A2-10 | Scope-changing feedback reaches a fresh design session with explicit revision instructions; later human direction overrides conflicting original requirements before another one-pager review. | Critical; integration, c2j input/artifacts | `direction-review.test.yaml`, `recipes/adaptive2/prompts.yaml`, `recipes/adaptive2/develop.yaml` |

## Default build rollout

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| A2-R1 | Approved work reaches native merge; verification failures prevent publication and return useful evidence. | Critical; integration, c2j/Git/Nix | `build-delivery.test.yaml`, `build.yaml` |
| A2-R2 | Named child builds resolve the public entrypoint in the destination workspace and require direction approval before implementation. | Critical; integration, c2j/Git/Nix | `default-child.test.yaml`, `build.yaml` |
| A2-R3 | Existing configure and verify hooks work with direction approval; ordinary requests need no audit documents. | High; integration, c2j/Nix | `../self-improvement/build.test.yaml`, `build.yaml` |
| A2-R4 | Invalid public annotations fail before any agent starts. | High; integration, c2j | `build-delivery.test.yaml`, `build.yaml` |

## Automatic limits and accepted assignments

These extend the expectations in [the approved plan](../../guides/adaptive2/PROPOSAL_AUTONOMOUS_TURN_LIMITS.md).

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| A2-T1 | Human questions, answers, and repeated direction or outcome revisions complete with a one-turn automatic allowance. | Critical; integration, c2j input | `human-turns.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-T2 | Continued automatic implementation stops at its configured allowance with a specific reason. | Critical; integration, c2j | `human-turns.test.yaml`, `recipes/adaptive2/autonomous-budget.yaml` |
| A2-T3 | New human consultation or package decisions renew the caller's allowance; replaying a saved decision does not. | Critical; integration, c2j input | `human-turns.test.yaml`, `autonomous-budget.test.yaml` |
| A2-T4 | Human direction renews consultation rounds, including suspended callers of nested advice; automatic debate remains bounded. | High; integration, c2j input/workspaces | `consultation-turns.test.yaml`, `recipes/adaptive2/consultation.yaml` |
| A2-T5 | An unchanged handoff copy starts execution using the receiving owner's original document. | Critical; integration, c2j artifacts/children | `build-handoff-recovery.test.yaml`, `recipes/adaptive2/accepted-handoff.yaml` |
| A2-T6 | Changed assignments cannot execute; correction restores original inbox files and preserves proposed edits separately. | Critical; integration, c2j artifacts | `build-handoff-recovery.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-T7 | Exhausted response correction reports the actual offending file and keeps its evidence. | High; integration, c2j | `build-handoff-recovery.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-T8 | Human feedback renews operational correction; repeated unchanged failures still stop. | High; integration, c2j | `human-turns.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-T9 | Unchanged merge chasing reuses approval and stays bounded; a new human approval starts a fresh retry allowance. | High; integration, c2j/Git | `merge-turns.test.yaml`, `recipes/adaptive2/develop.yaml` |
| A2-T10 | Missing correction checkpoints and exhausted correction retries produce different codes while preserving the unresolved cause. | High; integration, c2j | `response-repair.test.yaml`, `recipes/adaptive2/response-repair.yaml` |

## Approval recovery inspection

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| A2-AR1 | Approved work resumes writable implementation without another direction review when its history exceeds terminal limits and approval appears on a later page. | Critical; integration, c2j/Git/Nix | `approved-recovery.test.yaml`, `approved-source.yaml`, `recipes/adaptive2/recovery-approval.yaml` |
| A2-AR2 | Failed approval inspection stops with its diagnostic before design, implementation, child submission, or another human review. | Critical; integration, c2j/Git/Nix | `approved-recovery.test.yaml`, `recipes/adaptive2/recovery-approval.yaml` |
| A2-AR3 | A successfully inspected revision decision still requires direction review; unreadable approval evidence never grants implementation access. | Critical; integration, c2j artifacts/input | `approved-recovery.test.yaml`, `recipes/adaptive2/recovery-approval.yaml` |
| A2-AR4 | Recovery from an active source stops before starting duplicate work or another design review. | Critical; integration, c2j | `approved-recovery.test.yaml`, `recipes/adaptive2/recovery-approval.yaml` |

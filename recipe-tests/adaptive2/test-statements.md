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

## Default build rollout

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| A2-R1 | Approved work reaches native merge; verification failures prevent publication and return useful evidence. | Critical; integration, c2j/Git/Nix | `build-delivery.test.yaml`, `build.yaml` |
| A2-R2 | Named child builds resolve the public entrypoint in the destination workspace and require direction approval before implementation. | Critical; integration, c2j/Git/Nix | `default-child.test.yaml`, `build.yaml` |
| A2-R3 | Existing configure and verify hooks work with direction approval; ordinary requests need no audit documents. | High; integration, c2j/Nix | `../self-improvement/build.test.yaml`, `build.yaml` |
| A2-R4 | Invalid public annotations fail before any agent starts. | High; integration, c2j | `build-delivery.test.yaml`, `build.yaml` |

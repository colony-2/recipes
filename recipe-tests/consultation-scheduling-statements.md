# Consultation scheduling test statements

These statements define the heavy coordinator's scheduling policy. They qualify
its earlier unconditional parallel-launch expectation: parallel progress applies
to batches above the inline limit and explicit custom recipe selectors.
The light coordinator and same-candidate expert reviews remain inline.

| Importance | Level / dependencies | Files | Statement |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Nix | `recipes/develop/coordinate.yaml` | Up to forty new distinct serving consultations run inline without child consultation jobs. |
| Critical | Integration / c2j, Nix | `recipes/develop/coordinate.yaml` | Forty-one new distinct serving consultations all launch as child jobs before the caller waits. |
| High | Integration / c2j, Nix | `recipes/develop/coordinate.yaml` | Existing threads, repeated keys, and local expert reviews do not inflate the serving consultation batch size. |
| Critical | Integration / c2j, Nix | `recipes/develop/coordinate.yaml`, `recipes/kernel/consultation.yaml` | Sequential consultations retain requester conversation progress and separately preserve each serving cell's agreement documents. |
| Critical | Integration / c2j, Nix | `recipes/develop/coordinate.yaml` | Explicit custom consultation selectors retain child execution regardless of batch size. |
| Critical | Integration / c2j, Nix | `recipes/develop/coordinate.yaml` | Inline consultation failures propagate without manufacturing agreement or launching prerequisite work. |
| High | Integration / c2j, Nix | `recipes/develop/coordinate.yaml` | Root consultations retain project-fit instructions and configured root targeting when included inline. |

The embedded authoring validation attaches this document as a c2 artifact.
Include it in the build's test-plan artifacts when using this change.

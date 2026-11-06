# Legacy retirement and retained coverage

Defined before this cleanup. The user requested removal of unused legacy workflows
without changing adaptive behavior; no compatibility entrypoints are retained.

| ID | Importance | Level / dependencies | Files | Expectation |
| --- | --- | --- | --- | --- |
| LR01 | Critical | Integration / c2j, Git, Nix | `build.yaml`, `recipes/adaptive/` | Adaptive build, consultation, recovery, review, and publication retain their existing behavior after legacy removal. |
| LR02 | High | Static / local recipe sources | `recipes/`, `recipe-tests/` | Retained recipes and tests resolve their dependencies without importing retired workflows. |
| LR03 | Critical | Integration / c2j native registration | `recipes/create/register-cell.yaml` | Root can register a new cell idempotently; conflicting identities and unauthorized callers are rejected. |
| LR04 | Critical | Integration / native Git and child jobs | `create.yaml`, `recipes/create/` | Approved cells publish their exact purposes; registration or publication failure prevents later catalog publication. |
| LR05 | High | Integration / native review artifacts | `recipes/kernel/review-content.yaml` | Large review evidence and annotations remain accessible without truncating the structured result used to construct the review. |
| LR06 | High | Integration / mocked inference, native validation | `recipes/kernel/review-synthesis.yaml` | Enabled synthesis accepts valid citations, retries correctable failures, and falls back for invalid or unavailable results. |
| LR07 | High | Integration / native review artifacts | `recipes/kernel/review.yaml`, `recipes/create/review.yaml` | Clarification includes a current decision brief without requiring the agent to invent supporting documents. |
| LR08 | Critical | Integration / native cell registry and Git | `recipes/create/publish.yaml` | Initialization selects the approved cell and repository; registration rejects conflicting identities before publication begins. |

The retired heavy/light and superpowers expectations are removed with those
workflows. Shared creation, artifact, review, and registration coverage remains.
Model-assisted review stays disabled in the production caller; LR06 tests the
existing opt-in branch and does not certify model quality or enable that branch.

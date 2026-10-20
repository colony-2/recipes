# Build kernel test statements

These statements are published as a test artifact by the lifecycle fixtures.
Native tests use disposable repositories, real review/artifact/session handling,
and mocked Codex responses. Creation handoff uses a stand-in child recipe.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j | `build.yaml` | Builds infer repository purpose when PURPOSE.md is absent; they never bootstrap a mandate or select an evolve mode. |
| Critical | Integration / c2j, c2ops | `recipes/kernel/agent-turn.yaml` | Fresh sessions receive instructions once; resumed build and consultation turns use their exact checkpoints and enforced output schemas. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Implementation begins only after current design and test statements pass independent assessment and human approval. |
| Critical | Integration / c2j artifacts | `recipes/kernel/review.yaml` | Questions are focused fields alongside documents; exact answers and annotations return to the requesting phase as artifacts. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Uploaded edits or requested revisions require a revised proposal and another review before implementation or merge. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Expert agreement with adverse findings cannot authorize implementation or merge; an explicit passing assessment is required. |
| Critical | Integration / c2j, Git | `recipes/develop/develop.yaml` | Passing verification and human acceptance are required to merge the inspected candidate; failures and cancellation never merge. |
| High | Integration / c2j | `recipes/develop/verify.yaml` | Verification reports passed, failed, and skipped checks honestly; missing verification cannot silently count as passing. |
| Critical | Integration / c2j jobs | `recipes/develop/coordinate.yaml` | Independent consultations launch before waiting, and local work can continue while another consultation awaits human direction. |
| Critical | Integration / c2j objects | `recipes/develop/coordinate.yaml` | Submitted prerequisite builds receive the serving consultant's checkpoint and exact agreed artifacts after scope approval. |
| Critical | Integration / c2j jobs | `recipes/develop/coordinate.yaml` | Stable request keys prevent duplicate jobs; blocked routes wait for named known dependencies and preserve failure outcomes. |
| Critical | Integration / c2j, Git | `recipes/develop/coordinate.yaml` | Same-candidate experts inspect unmerged work; foreign consultation never replaces the requester's repository or later session progress. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Only agreed prerequisite keys listed in the approved proposal authorize submission; new external scope requires renewed plan approval. |
| Critical | Integration / c2j | `recipes/develop/coordinate.yaml` | New-cell eligibility consults configured root; feature implementation requires a separate consultation with the created cell. |
| High | Integration / c2j artifacts | `recipes/kernel/artifact-namespace.yaml` | Identically named documents from different consultations and jobs remain separately available without changing their stored identities. |

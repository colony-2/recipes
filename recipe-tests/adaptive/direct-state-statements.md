# Direct recipe state acceptance statements

Defined before implementation. Scope: active adaptive recipes and their private
helpers. This fits the recipes cell. No c2j or c2ops changes are required.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| DS-01 | Critical | Integration / c2j | Helpers receive specific inputs without a replacement workflow context object. | recipes/adaptive/*.yaml |
| DS-02 | Critical | Integration / c2j | Decisions observe producing recipe outputs; configuration and derived status flags are not copied through every transition. | recipes/adaptive/develop.yaml |
| DS-03 | Critical | Integration / c2j | Current failures reach agents through error-directory artifacts without failure objects, path inventories, or error metadata in prompts. | recipes/adaptive/agent.yaml, recipes/adaptive/task-documents.yaml |
| DS-04 | Critical | Integration / c2j | Response repair preserves prior deliverables, uses the latest session, and cannot authorize implementation or child submission. | recipes/adaptive/develop.yaml |
| DS-05 | Critical | Integration / c2j, Git | Consultation, child results, annotations, and sessions survive independent work and repeated coordination without duplicate submissions. | recipes/adaptive/coordinate.yaml |
| DS-06 | Critical | Integration / c2j, Git | Required verification, independent assessment, and human acceptance remain necessary before merging the reviewed candidate. | recipes/adaptive/develop.yaml |
| DS-07 | Critical | Integration / c2j, Git | Rebase recovery preserves changes; upstream advances require fresh checks and retain bounded retries. | recipes/adaptive/rebase-recovery.yaml, recipes/adaptive/develop.yaml |
| DS-08 | High | Integration / c2j | Missing evidence and unchanged blockers request repair or intervention without reusing stale completion decisions. | recipes/adaptive/develop.yaml |

Validation: existing native diagnostics/inbox/coordination fixtures and the adaptive
regression suites, with focused cases for direct input contracts and error-only
handoffs. Retain existing expectations. Published Nix resolution and the shared
embedded database were blocked in the preceding run; report any continuing
limitations separately from native or mocked execution results.

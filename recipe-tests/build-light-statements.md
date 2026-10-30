# Build routing and lightweight workflow test statements

Codex and Jev responses are deterministic fixtures. Native runtime tests exercise
Git, artifact transport, includes, review responses, and child-job completion.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Nix | `build.yaml`, `recipes/build/classify.yaml` | Only a valid Jev answer with at least 90% light probability and usable repository context selects the lightweight workflow. |
| Critical | Integration / c2j | `recipes/build/classify.yaml` | Heavy, uncertain, malformed, unavailable, or context-incomplete classification selects the heavy workflow without silently approving work. |
| High | Integration / c2j, Jev | `recipes/build/classify.yaml` | Jev receives the request, repository purpose, architecture or README context, and the explicitly referenced jev_api_key secret. |
| Critical | Integration / c2j | `recipes/light/develop.yaml`, `recipes/light/agent.yaml` | Light work starts implementation without separate design, test-statement, or plan-approval phases. |
| Critical | Integration / c2j, Git | `recipes/light/develop.yaml` | Local changes require human synopsis approval after available checks; failures or revision feedback repeat implementation and verification before merging. |
| High | Integration / c2j | `recipes/develop/verify.yaml` | A missing target directory fails verification without running checks from the repository root; an existing target without checks reports skipped. |
| High | Integration / c2j, Git | `recipes/light/develop.yaml`, `recipes/light/synopsis.yaml` | An absent optional verify hook permits synopsis review and merge; the synopsis reports skipped verification without claiming tests passed. |
| Critical | Integration / c2j | `recipes/develop/verify.yaml` | Only the configured verify hook runs checks; failures block progress and retain evidence, while an unrelated build.sh is never discovered. |
| Critical | Integration / c2j, Git | `recipes/light/develop.yaml` | No-change jobs without children require human rationale review; delegation-only jobs may bypass local review only after their children succeed. |
| Critical | Integration / c2j jobs | `recipes/light/coordinate.yaml` | Every serving-cell consultation runs inline; agreed child builds launch without human plan approval, using fresh execution sessions and the exact agreed artifacts. |
| Critical | Integration / c2j jobs | `recipes/light/coordinate.yaml` | Stable keys prevent duplicate child submissions; changed requests cannot reuse keys, and child failures retain their original errors. |
| High | Integration / c2j | `recipes/light/develop.yaml` | Clarification and result repair retain the current session and documents without granting merge approval. |
| Critical | Integration / c2j | `build.yaml`, `recipes/develop/develop.yaml` | Heavy builds retain their existing gates and accept successful delegation-only prerequisites without requiring an unnecessary child merge. |
| Critical | Integration / c2j | `build.yaml`, `recipes/light/develop.yaml` | Light work can escalate to heavy after waiting for launched children, retaining its candidate, session, and completed dependency evidence. |

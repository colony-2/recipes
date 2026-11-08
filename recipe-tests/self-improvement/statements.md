# Audit skill and ordinary build expectations

These replace the unpublished extra-entrypoint draft. The existing adaptive
build contract is unchanged.

- S1 [Critical] [integration] [build.yaml] [c2j] Audit requests and selected prior evidence reach normal planning through the existing build input contract.
- S2 [Critical] [integration] [recipes/adaptive/develop.yaml] [c2j] Planning stays read-only, implementation receives the selected audit and plan in a fresh session, and normal outcome review remains required.
- S3 [High] [integration] [build.yaml] [c2j] A completed audit with no justified changes finishes through the existing no-change path.
- S4 [High] [integration] [build.yaml] [c2j] Ordinary recipe changes can complete without audit deliverables, additional classification calls, or child jobs.
- S5 [Critical] [integration] [recipes/adaptive/develop.yaml] [c2j] Essential unavailable evidence can end an audit attempt without an empty successful census or routine human question.
- S6 [High] [integration] [.agents/skills/audit-recipe-jobs/SKILL.md] [c2j] The skill and core backgrounders are available in the managed workspace alongside existing local hooks.

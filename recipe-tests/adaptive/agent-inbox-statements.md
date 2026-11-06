# Standard agent inbox acceptance statements

Defined before implementation. The embedded smoke validation binds this document
as a c2 artifact. Runtime dependency: c2j with execution diagnostics v2 and self
capability discovery (validated against f1a153b898c5).

| ID | Priority | Level | Dependencies | Statement | Files |
| --- | --- | --- | --- | --- | --- |
| I01 | Critical | integration | c2j | Task prompts retain request and phase without leaking workflow configuration or duplicating standing instructions. | recipes/adaptive/agent.yaml |
| I02 | Critical | integration | c2j, Git | Current command and extension failures reach repair as named execution logs in error/, preserving status and provenance. | recipes/adaptive/verify.yaml, recipes/adaptive/hook-verify.yaml |
| I03 | Critical | integration | c2j | Missing logs and required-skipped verification produce actionable error text without implying successful verification. | recipes/adaptive/task-documents.yaml |
| I04 | High | integration | c2j | Human feedback and reviewer findings appear in feedback/ while existing document identities and links remain usable. | recipes/adaptive/task-documents.yaml |
| I05 | Critical | integration | c2j | New attempts replace prior execution errors; historical streams remain readable without invented ordering. | recipes/adaptive/task-documents.yaml |
| I06 | High | integration | c2j | Agents discover effective permissions and availability through self without treating granted capability as unrestricted task authorization. | recipes/adaptive/agent-turn.yaml |
| I07 | Critical | integration | c2j | Authorized implementation validations consume automatic child-job outputs; read-only tasks cannot silently submit work. | recipes/adaptive/develop.yaml |
| I08 | Critical | integration | c2j | Empty-key environment blockers reach intervention rather than invalid prerequisite coordination. | recipes/adaptive/develop.yaml |
| I09 | Critical | integration | c2j | Reviewers receive verification facts and current findings without recursive child results or runtime state dumps. | recipes/adaptive/inspect.yaml |
| I10 | High | integration | c2j | Response repair supplies concrete corrections in files without authorizing implementation. | recipes/adaptive/response-repair.yaml |
| I11 | Critical | integration | c2j | Intervention findings bypass automatic implementation retries; validation plans identify actor, authority, prerequisites, and evidence. | recipes/adaptive/inspect.yaml, recipes/adaptive/agent.yaml |
| I12 | Critical | integration | c2j | Reviewers can return supplied evidence without preventing subsequent agents or candidate inspection from starting. | recipes/adaptive/agent-turn.yaml, recipes/adaptive/git-candidate.yaml |
| I13 | Critical | integration | c2j | Original execution evidence remains authoritative when a reviewer returns a copy; verification files cannot replace approved specifications. | recipes/adaptive/verify.yaml, recipes/adaptive/agent-turn.yaml |

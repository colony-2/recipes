# Acceptance statements for the audit improvements

Defined before implementation. These extend the existing acceptance statements;
limit exhaustion intentionally changes from terminal failure to a human decision.
The limit proposal's LE-01–LE-15 remain part of this assignment.

| Expectation | Importance | Level / dependencies | Files |
| --- | --- | --- | --- |
| Visual changes without adequate actual captures return to validation before merge review. | Critical | Integration / c2j, scripted assessment | `recipes/adaptive2/prompts.yaml`, `recipes/adaptive2/develop.yaml` |
| Every local evidence link in selected review documents resolves to a readable attached artifact. | Critical | Integration / c2j, Markdown parser | `recipes/adaptive2/inspect.yaml`, `recipes/adaptive2/review.yaml` |
| Galleries with omitted images request correction identifying each missing target before human review. | Critical | Integration / c2j artifacts | `recipes/adaptive2/review.yaml` |
| Relative, encoded, reference-style, and supported HTML links resolve consistently within attachment paths. | High | Integration / c2j, Markdown parser | `recipes/adaptive2/review.yaml` |
| External links, anchors, and code examples do not require additional attachments. | High | Integration / c2j | `recipes/adaptive2/review.yaml` |
| Cyclic links terminate; incomplete or unreadable evidence validation cannot pass. | Critical | Integration / c2j | `recipes/adaptive2/inspect.yaml` |
| Unrelated artifacts remain excluded from human review. | High | Integration / c2j | `recipes/adaptive2/review.yaml` |
| Nonvisual changes and explicit visual-evidence exemptions can pass with an explanation. | High | Integration / scripted assessment | `recipes/adaptive2/prompts.yaml` |
| Approved recovery starts writable implementation without repeating the unchanged direction review. | Critical | Integration / c2j input, Git | `build.yaml`, `recipes/adaptive2/develop.yaml` |
| Recovered edits persist into subsequent tasks and undergo current verification. | Critical | Integration / c2j, Git | `recipes/adaptive2/workflow.yaml`, `recipes/adaptive2/agent.yaml` |
| Unsupported approval claims cannot bypass ordinary design review. | Critical | Integration / c2j artifacts | `recipes/adaptive2/develop.yaml` |
| Recovered implementation can execute agreed dependency work. | Critical | Integration / c2j child jobs | `recipes/adaptive2/coordinate.yaml` |
| Configuration checks preserve recovered candidate state and report the actual failure cause. | Critical | Integration / c2j workspaces, Git | `recipes/adaptive2/workflow.yaml`, `recipes/adaptive/hook-configure.yaml` |
| A genuinely mutating read-only hook remains rejected. | Critical | Integration / c2j, Git | `recipes/adaptive/hook-configure.yaml` |
| Exhausted implementation and correction allowances preserve work and ask for direction. | Critical | Integration / c2j input | `recipes/adaptive2/develop.yaml`, `recipes/adaptive2/response-repair.yaml`, `recipes/adaptive2/inspect.yaml` |
| Human grants authorize exactly the displayed new attempts without weakening validation or phase restrictions. | Critical | Integration / c2j input | `recipes/adaptive2/autonomous-budget.yaml` |
| Receipt replay never renews allowances or duplicates child work. | Critical | Integration / c2j receipts | `recipes/adaptive2/autonomous-budget.yaml`, `recipes/adaptive2/consultation.yaml` |
| Failed explanation generation still yields a usable decision from retained facts. | High | Integration / c2j, scripted failure | `recipes/adaptive2/review.yaml` |
| A waiting child remains unfinished; stopping cannot publish or satisfy dependent delivery. | Critical | Integration / c2j lifecycle | `recipes/adaptive2/coordinate.yaml`, `recipes/adaptive/await-child.yaml` |
| Unchanged local edits after unrelated upstream context changes reuse prior approval when verification passes. | Critical | Integration / real Git | `recipes/adaptive/git-candidate.yaml`, `recipes/adaptive2/develop.yaml` |
| Changed behavior, modes, or binary contents still require review; failed verification cannot reuse approval to publish. | Critical | Integration / real Git | `recipes/adaptive/git-candidate.yaml`, `recipes/adaptive2/develop.yaml` |
| Scope exclusions and concrete missing prerequisites survive coordination and recovery. | High | Integration / c2j artifacts | `recipes/adaptive2/prompts.yaml`, `recipes/adaptive2/coordinate.yaml` |

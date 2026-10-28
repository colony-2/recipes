# Build kernel test statements

These statements are published as a test artifact by the lifecycle fixtures.
Native tests use disposable repositories, real review/artifact/session handling,
and mocked Codex responses. Creation handoff uses a stand-in child recipe.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j | `recipes/kernel/agent-turn.yaml`, `recipes/develop/develop.yaml` | Unhandled agent execution failures retain their original message and originating node; build executes no replacement failure command. |
| Critical | Integration / c2j | `recipes/kernel/consultation.yaml`, `recipes/kernel/consultation-report.yaml` | Agent execution failures propagate through build assessments, consultations, and reports; callers can handle them with an ordinary catch. |
| High | Integration / c2j | `recipes/develop/develop.yaml` | Invalid build requests and rejected agent results report specific reasons instead of a generic shell exit message. |
| Critical | Integration / c2j, c2ops | `recipes/kernel/agent-turn.yaml` | Fresh and resumed agents can resolve the explicitly authorized Codex credential; an absent optional credential retains provider fallback. |
| Critical | Integration / c2j | `recipes/kernel/agent-turn.yaml` | A caller's permission ceiling cannot be widened by an agent turn requesting Codex credentials. |
| Critical | Integration / c2j jobs | `recipes/develop/coordinate.yaml` | Dependency waits target the recorded job and preserve its failure without waiting indefinitely for a replacement attempt. |
| Critical | Integration / c2j | `build.yaml` | Builds infer repository purpose when PURPOSE.md is absent; they never bootstrap a mandate or select an evolve mode. |
| Critical | Integration / c2j, c2ops | `recipes/kernel/agent-turn.yaml` | Fresh sessions receive instructions once; resumed build and consultation turns use their exact checkpoints and enforced output schemas. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Implementation begins only after current design and test statements pass independent assessment and human approval. |
| Critical | Integration / c2j artifacts | `recipes/kernel/review.yaml` | Questions use focused fields with optional supporting documents; exact answers and annotations return to the requesting phase as artifacts. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Uploaded edits or requested revisions require a revised proposal and another review before implementation or merge. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Expert agreement with adverse findings cannot authorize implementation or merge; an explicit passing assessment is required. |
| Critical | Integration / c2j, Git | `recipes/develop/develop.yaml` | Available verification checks must pass before human acceptance and merge; skipped absent checks remain visible, and failures or cancellation never merge. |
| Critical | Integration / c2j, Git | `recipes/develop/develop.yaml` | Separate rebase, squash, and merge operations publish one approved commit; verification and file accounting inspect the rebased candidate before human acceptance. |
| Critical | Integration / c2j, Git, Nix | `recipes/develop/merge-review.yaml` | A fresh reviewer accounts for every added, changed, and deleted file; incomplete accounting cannot reach human approval or publication. |
| High | Integration / c2j, Nix | `recipes/develop/merge-review.yaml` | Inventory and review rendering use declared Nix Python without relying on a working host Python executable. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml`, `recipes/develop/merge-review.yaml` | Inappropriate changes return to implementation with review findings and the original build session; revised candidates require fresh accounting and human approval. |
| High | Integration / c2j, Git | `recipes/develop/merge-review.yaml`, `recipes/develop/develop.yaml` | The human reviews the proposed squash subject and explanation; the published commit includes that message and the current tenant's job URL. |
| High | Integration / c2j | `recipes/develop/verify.yaml` | Verification reports passed, failed, and skipped checks honestly; missing verification cannot silently count as passing. |
| Critical | Integration / c2j jobs | `recipes/develop/coordinate.yaml` | Independent consultations launch before waiting, and local work can continue while another consultation awaits human direction. |
| Critical | Integration / c2j objects | `recipes/develop/coordinate.yaml` | Submitted prerequisite builds start fresh execution sessions with exact agreed artifacts after scope approval. |
| Critical | Integration / c2j jobs | `recipes/develop/coordinate.yaml` | Stable request keys prevent duplicate jobs; blocked routes wait for named known dependencies and preserve failure outcomes. |
| Critical | Integration / c2j, Git | `recipes/develop/coordinate.yaml` | Same-candidate experts inspect unmerged work; foreign consultation never replaces the requester's repository or later session progress. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Only agreed prerequisite keys listed in the approved proposal authorize submission; new external scope requires renewed plan approval. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml` | Unknown prerequisite keys are corrected during design; returning an empty corrected list advances to test-plan without stale keys or duplicate jobs. |
| Critical | Integration / c2j | `recipes/develop/agent.yaml` | Parent request identifiers are not treated as the child build's prerequisites; only this build's agreed serving requests belong in design review keys. |
| High | Integration / c2j | `recipes/develop/develop.yaml`, `recipes/develop/verify.yaml` | Missing build.sh is reported as skipped and permits normal review and merge; an existing failing script still requires repair. |
| High | Integration / c2j | `recipes/kernel/agent-turn.yaml`, `recipes/develop/develop.yaml` | Execution errors identify the operation's purpose through explicit descriptive node IDs, preserving the original error message. |
| Critical | Integration / c2j | `recipes/develop/coordinate.yaml` | New-cell eligibility consults configured root; feature implementation requires a separate consultation with the created cell. |
| High | Integration / c2j artifacts | `recipes/kernel/artifact-namespace.yaml` | Identically named documents from different consultations and jobs remain separately available without changing their stored identities. |
| High | Integration / c2j | `recipes/develop/develop.yaml` | Builds discover the root cell and its branch from .c2/config.yaml when callers omit explicit root settings. |
| High | Integration / c2j artifacts | `recipes/kernel/agent-turn.yaml` | Fresh and resumed agents receive current artifact directories and report outbox-relative names; valid design artifacts advance to review. |
| Critical | Integration / c2j path_match | `recipes/kernel/artifact-result.yaml` | Unique approximate references retain the exact stored artifact identity; ambiguous or missing documents require correction before approval. |
| Critical | Integration / c2j | `recipes/kernel/repair.yaml` | Two automatic repairs preserve the latest session and documents; exhausted repairs request human direction or cancellation without approving work. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml`, `recipes/kernel/consultation.yaml`, `recipes/create/review.yaml` | Repairs preserve phase, approvals, participant, and consultation budget; corrected results pass ordinary validation before any dependent action. |
| Critical | Integration / c2j, Git | `recipes/develop/agent.yaml`, `create.yaml` | Result-only repairs cannot alter a built candidate or repeat cell publication or registration edits. |
| High | Integration / c2j | `recipes/kernel/consultation-report.yaml` | Summary corrections preserve the recorded agreement, final artifacts, and participant checkpoints. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml`, `recipes/create/review.yaml` | Clarification reaches the user without deliverables or artifact repair; answers resume the requesting session and phase without approving work. |

# Adaptive build acceptance statements

Agent decisions and human responses are fixtures. These expectations were defined
before implementation; dependencies are recorded per statement.

| ID | Priority | Level | Dependencies | Statement | Files |
| --- | --- | --- | --- | --- | --- |
| A01 | Critical | integration | c2j, Git, Nix | Both design routes establish formal test statements before implementation and require only one normal human outcome review. | recipes/adaptive/build.yaml, recipes/adaptive/develop.yaml |
| A02 | Critical | integration | c2j, Git, Nix | Human redesign feedback restarts design and test statements without duplicating recorded child work. | recipes/adaptive/develop.yaml |
| A03 | Critical | integration | c2j, Git | Failed, malformed, missing-evidence, or required-skipped verification returns to implementation; cancellation remains cancellation. | recipes/adaptive/hook-verify.yaml |
| A04 | Critical | integration | c2j, Git | Hooks return values and evidence directly without extra report-inspection tasks. | recipes/adaptive/hook-verify.yaml |
| A05 | Critical | integration | c2j, Git | Native rebase conflicts preserve complete candidate evidence, establish the target through the rebase op, and repeat implementation, verification, and review. | recipes/adaptive/rebase-recovery.yaml |
| A06 | Critical | unit/integration | c2j, Git | Unsafe, incomplete, cancelled, or exhausted rebase failures cannot authorize automatic repair or publication. | recipes/adaptive/develop.yaml |
| A07 | Critical | integration | c2j, Git, Nix | Upstream advancement triggers bounded native rebases; equivalent changes reuse approval after fresh verification. | recipes/adaptive/develop.yaml |
| A08 | Critical | integration | c2j, Git, Nix | Changed candidates or verification policy invalidate reused approval; ordinary merge errors never trigger an upstream retry. | recipes/adaptive/develop.yaml |
| A09 | Critical | integration | c2j, Git, Nix | Publication failure after merge never reports successful completion or repeats the completed merge. | recipes/adaptive/develop.yaml |
| A10 | Critical | integration | c2j, Git, Nix | Serving agreement precedes child submission; repeated execution references follow recorded jobs; failed prerequisites block completion. | recipes/adaptive/coordinate.yaml |
| A11 | High | integration | c2j, Git, Nix | Required specialists must pass; advisory findings remain visible without blocking the workflow. | recipes/adaptive/specialists.yaml |
| A12 | High | integration | c2j, Git | Review uses defined documents and identity-bound annotations, prioritizing the overview, test expectations, results, and blocking findings. | recipes/adaptive/review.yaml |
| A13 | High | integration | c2j, Git, Nix | Invalid responses receive bounded corrections; agent errors and unauthorized job creation do not silently pass. | recipes/adaptive/develop.yaml |
| A14 | High | integration | c2j, Git, Nix | Small control state uses inputs and outputs; logs, diffs, documents, and transcripts remain artifacts. | recipes/adaptive/agent.yaml, recipes/adaptive/review.yaml |
| A15 | High | integration | c2j, Git, Nix | Iteration exhaustion requests direction; cancellation and no-change completion retain their distinct outcomes. | recipes/adaptive/develop.yaml |
| A16 | Critical | integration | c2j, Git, Nix | New-cell creation preserves root approval and publication requirements and does not satisfy the original feature request by itself. | recipes/adaptive/coordinate.yaml |
| A17 | Critical | integration | c2j, Git, Nix | Implementation cannot replace established test expectations; revised plans preserve expectations or provide a deprecation plan. | recipes/adaptive/develop.yaml |
| A18 | High | integration | c2j, Git | Hook results retain artifact names and immutable references; c2j enforces output contracts without a recipe validation task. | recipes/adaptive/hook-verify.yaml |
| A19 | Critical | integration | c2j, Git, Nix | Adaptive builds and serving consultations run with no kernel recipe files available. | recipes/adaptive/build.yaml, recipes/adaptive/consultation.yaml |
| A20 | High | integration | c2j, Git, Nix | Each verification attempt consumes current evidence; missing evidence or conflicting bindings return to implementation without replacing formal documents. | recipes/adaptive/develop.yaml |
| A21 | Critical | integration | c2j, Git | Reviewing reused or revised documents never produces self-references; valid links to other current documents remain available. | recipes/adaptive/review.yaml |
| A22 | Critical | integration | c2j, Git, Nix | Failed verification provides original command streams and exit details to implementation; later attempts replace earlier evidence without changing cancellation behavior. | recipes/adaptive/hook-verify.yaml, recipes/adaptive/verify.yaml, recipes/adaptive/agent.yaml |

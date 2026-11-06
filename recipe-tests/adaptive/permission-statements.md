# Permission inheritance regression

Recorded before implementation. Integration dependencies: c2j with permission
inheritance, Git, Python, yq, and synthetic tenant secrets. No model service.

| ID | Priority | Statement | Files |
| --- | --- | --- | --- |
| PI01 | Critical | Fresh and resumed read-only tasks resolve configured Git credentials while rejecting child submission before a job is created. | recipes/adaptive/agent-turn.yaml |
| PI02 | Critical | Changing the configured Git-secret name requires no recipe change; unrelated secrets remain unavailable. | recipes/adaptive/agent-turn.yaml |
| PI03 | Critical | A later implementation task retains submission authority and Git access after a restricted task. | recipes/adaptive/agent-turn.yaml |
| PI04 | Critical | Root registration retains Git access and cell-creation authority without granting child submission or leaking creation authority to siblings. | recipes/create/register-cell.yaml |

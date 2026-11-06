# Artifact selection expectations

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| AS-01 | Critical | Integration / c2j | Incidental outbox files remain producer artifacts without expanding repair inputs or human review documents. | recipes/adaptive/artifact-result.yaml, recipes/adaptive/develop.yaml |
| AS-02 | Critical | Integration / c2j | Declared deliverables retain their stored identities across response correction without copying or republishing their contents. | recipes/adaptive/agent-turn.yaml |
| AS-03 | High | Integration / c2j | Missing or ambiguous deliverables produce correction guidance without silently selecting an unrelated file. | recipes/adaptive/artifact-result.yaml |
| AS-04 | High | Integration / prompt fixtures | New and resumed agents receive guidance separating deliverables, individually accessible evidence, and temporary validation files. | recipes/adaptive/prompts.yaml |

---
title: "Rule Gates"
weight: 72
---

Rule gates make deterministic policy checks explicit and testable.

Use `c2ops rule_gate` when a workflow needs to decide based on:

- Boolean assertions.
- Artifact existence.
- Worktree file existence.
- JSON parseability.
- JSON Schema validation.
- Child status.

Example:

{{< example "examples/recipes/rule-gate.yaml" >}}

Policy failures return `ok: false` and list `failed_rule_ids`. That lets the parent recipe route to a replan, user input, or completion state without throwing away context.

Use a failing command when the operation itself failed. Use `rule_gate` when the operation succeeded and the result did not satisfy policy.


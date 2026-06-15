---
title: "Execution Model"
weight: 21
---

A recipe is a durable workflow made from nodes. The node may be an `op`, a `sequence`, a `state` machine, an inline `include`, or a `child_group`.

Each op runs in an isolated operation context, not in your interactive shell. Treat every op as a remote durable step:

- Pass structured data through `inputs`.
- Move files through artifacts.
- Use `context.environment.op.worktree_path`, `context.environment.op.inbox`, and `context.environment.op.outbox` for op-visible paths.
- Export data needed by outer scopes through `outputs`.
- Prefer a real op over ad hoc shell glue when a purpose-built op exists.

The operation context has three important directories:

- `worktree_path`: the current cell checkout for code and repo-relative commands.
- `inbox`: materialized input artifacts for this op.
- `outbox`: files written here become output artifacts for this op.

Git state is also durable. After each mutating op, c2j persists the cell worktree as internal git state and restores it for the next op. Recipe authors normally do not bind or inspect the internal thin-pack artifact directly.

The default local runtime is embedded:

```bash
c2j submit --recipe-file docs/examples/recipes/hello-command.yaml --run --embed
```

Use a remote runtime only when validating scheduler or server-managed behavior:

```bash
c2j submit \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --swf-url http://localhost:9047 \
  --run
```


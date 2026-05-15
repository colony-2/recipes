# Historical Proposal: c2j Op-Visible Path Context

## Status

Superseded by the implemented c2j op-visible path contract. Use the current user guide:

- `../OP_VISIBLE_PATHS_USER_GUIDE.md`

The implemented surface uses:

```text
context.environment.op.workdir
context.environment.op.worktree_path
context.environment.op.inbox
context.environment.op.outbox
context.environment.host.workdir
context.environment.host.worktree_path
context.environment.host.inbox
context.environment.host.outbox
```

The older flat fields remain host-view paths:

```text
context.environment.workdir
context.environment.worktree_path
context.environment.inbox
context.environment.outbox
```

## Difference From The Proposal

The original proposal asked c2j to provide a sandbox-agnostic op-visible path view. c2j implemented that, and also added explicit `sandbox.paths` support so recipes can customize sandbox mount targets:

```yaml
sandbox:
  type: shai
  paths:
    worktree_path:
      sandbox: /workspace/repo
    inbox:
      sandbox: /workspace/inbox
      mode: ro
    outbox:
      sandbox: /workspace/outbox
```

Recipes and extension-op defaults should use `context.environment.op.*` for any path that the running op process must read or write. Use `context.environment.host.*` only when the c2j worker host path is intentionally required.

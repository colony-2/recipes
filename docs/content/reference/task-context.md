---
title: "Task Context"
weight: 42
---

Recipe templates can reference `context`, `inputs`, `sequence`, `states`, `scope`, and local `vars`.

Common task context fields:

```yaml
context.environment.op.worktree_path
context.environment.op.workdir
context.environment.op.inbox
context.environment.op.outbox
context.environment.host.worktree_path
context.environment.host.workdir
context.environment.host.inbox
context.environment.host.outbox
context.git.repo
context.git.ref
context.git.resolved_hash
context.git.hash
context.git.parent_hash
context.invocation.hash
context.artifacts
```

Use op-visible paths in recipe inputs and prompts:

```yaml
inputs:
  working_directory: "{{ context.environment.op.worktree_path }}"
  run: ls "{{ context.environment.op.inbox }}"
```

Use host paths only for extension code that explicitly needs the worker host view.

For selector-backed c2ops agents, pass op-visible paths explicitly when the op schema has path fields:

```yaml
inputs:
  worktree_path: "{{ context.environment.op.worktree_path }}"
  workdir_path: "{{ context.environment.op.workdir }}"
  artifact_inbox_path: "{{ context.environment.op.inbox }}"
  artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

Do not hard-code `/src/inbox` or `/src/outbox`.


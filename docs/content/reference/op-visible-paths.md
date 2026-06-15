---
title: "Op-Visible Paths"
weight: 43
---

Every operation sees a path view that may differ from the host view when sandboxing is enabled.

Author recipes against the op-visible paths:

- `context.environment.op.worktree_path`
- `context.environment.op.workdir`
- `context.environment.op.inbox`
- `context.environment.op.outbox`

Default `command_execution` working directory is `context.environment.op.worktree_path`.

Use outbox to produce artifacts:

```yaml
inputs:
  working_directory: "{{ context.environment.op.outbox }}"
  run: printf ok > result.txt
```

Use inbox to consume bound artifacts:

```yaml
artifacts:
  result.txt: '${{ sequence.produce.artifacts["result.txt"] }}'
inputs:
  working_directory: "{{ context.environment.op.inbox }}"
  run: cat result.txt
```

Extension ops can opt out of sandboxing where appropriate:

```yaml
inputs:
  sandbox:
    type: none
```

Use `sandbox.type: none` for local live smoke tests that should avoid the extension wrapper sandbox. Keep production recipes explicit about the sandbox mode they require.


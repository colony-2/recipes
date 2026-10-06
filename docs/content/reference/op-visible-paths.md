---
title: "Op-Visible Paths"
weight: 43
---

Every operation receives paths for its worktree and artifacts.

Author recipes against the op-visible paths:

- `context.environment.op.worktree_path`
- `context.environment.op.workdir`
- `context.environment.op.inbox`
- `context.environment.op.outbox`

Default `command_execution` working directory is `context.environment.op.worktree_path`.

Omit op sandbox configuration, including explicit `none` settings, as c2j removes that support.

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

## Process Path Examples

Run a command directly on the worker host:

```yaml
- id: direct_check
  op: command_execution
  inputs:
    run: |
      pwd
      ls "{{ context.environment.op.worktree_path }}"
```

Run a command with bound input artifacts:

```yaml
- id: artifact_check
  op: command_execution
  artifacts:
    submitted/: '${{ context.artifacts }}'
  inputs:
    working_directory: "{{ context.environment.op.worktree_path }}"
    run: |
      ls "{{ context.environment.op.inbox }}/submitted"
      mkdir -p "{{ context.environment.op.outbox }}/checks"
      printf '{"ok":true}\n' > "{{ context.environment.op.outbox }}/checks/result.json"
```

Run a selector-backed extension op directly:

```yaml
- id: run_codex
  op: git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572
  inputs:
    prompt: "Review the current cell."
    worktree_path: "{{ context.environment.op.worktree_path }}"
    workdir_path: "{{ context.environment.op.workdir }}"
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

Run an extension op with bound input artifacts:

```yaml
- id: summarize
  op: ./tools/ops/summarize-artifacts
  artifacts:
    submitted/: '${{ context.artifacts }}'
  inputs:
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

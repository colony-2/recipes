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

`inputs.sandbox` is currently an execution option for:

- `command_execution`
- selector-backed and local extension ops, including c2ops selectors such as Codex

It is not a recipe-wide setting. It does not apply to `include`, `child_group`, child recipe ops, `input`, `sleep`, or git integration ops. If a parent starts a child recipe, sandbox behavior is controlled by the ops inside that child recipe.

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

## Sandbox Examples

Run a command directly on the worker host:

```yaml
- id: direct_check
  op: command_execution
  inputs:
    sandbox:
      type: none
    run: |
      pwd
      ls "{{ context.environment.op.worktree_path }}"
```

Run a command in the Shai sandbox:

```yaml
- id: sandboxed_check
  op: command_execution
  artifacts:
    submitted/: '${{ context.artifacts }}'
  inputs:
    sandbox:
      type: shai
    working_directory: "{{ context.environment.op.worktree_path }}"
    run: |
      ls "{{ context.environment.op.inbox }}/submitted"
      mkdir -p "{{ context.environment.op.outbox }}/checks"
      printf '{"ok":true}\n' > "{{ context.environment.op.outbox }}/checks/result.json"
```

Run a selector-backed extension op directly:

```yaml
- id: run_codex
  op: git+https://github.com/colony-2/c2ops.git//codex@main
  inputs:
    sandbox:
      type: none
    prompt: "Review the current cell."
    worktree_path: "{{ context.environment.op.worktree_path }}"
    workdir_path: "{{ context.environment.op.workdir }}"
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

Run an extension op in the Shai sandbox:

```yaml
- id: summarize
  op: ./tools/ops/summarize-artifacts
  artifacts:
    submitted/: '${{ context.artifacts }}'
  inputs:
    sandbox:
      type: shai
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

The reserved `sandbox` input is not delivered to extension op stdin. Keep it out of extension `input_schema`.

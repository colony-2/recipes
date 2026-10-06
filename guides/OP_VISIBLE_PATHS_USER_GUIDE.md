# Using Op-Visible Paths

This guide explains how recipe authors and extension authors should pass file
paths to op processes.

## Short Version

Use `context.environment.op.*` for any path that the op process itself must
read from or write to.

```yaml
run: |
  ls "{{ context.environment.op.inbox }}"
  mkdir -p "{{ context.environment.op.outbox }}/results"
  printf '{"ok":true}\n' > "{{ context.environment.op.outbox }}/results/status.json"
```

Op processes use the paths supplied by c2j for their worktree and artifacts.

Use `context.environment.host.*` only when you intentionally need the path as
seen by the c2j worker host.

Omit op sandbox configuration, including explicit `none` settings: c2j is
removing op sandbox support.

## Available Path Context

| Field | Meaning |
| --- | --- |
| `context.environment.op.workdir` | Operation workspace root as seen by the running op process. |
| `context.environment.op.worktree_path` | Git worktree path as seen by the running op process. |
| `context.environment.op.inbox` | Artifact inbox path as seen by the running op process. |
| `context.environment.op.outbox` | Artifact outbox path as seen by the running op process. |
| `context.environment.host.workdir` | Operation workspace root on the c2j worker host. |
| `context.environment.host.worktree_path` | Git worktree path on the c2j worker host. |
| `context.environment.host.inbox` | Artifact inbox path on the c2j worker host. |
| `context.environment.host.outbox` | Artifact outbox path on the c2j worker host. |

The older flat fields still exist and remain host-view paths:

```text
context.environment.workdir
context.environment.worktree_path
context.environment.inbox
context.environment.outbox
```

For new recipes, prefer the explicit namespace:

- `context.environment.op.*` when a command, agent, or extension process will
  use the path.
- `context.environment.host.*` when a host-side integration needs the path.

## Direct Execution Paths

For direct execution, op-visible paths equal the host paths:

| Field | Value |
| --- | --- |
| `context.environment.op.workdir` | same as `context.environment.host.workdir` |
| `context.environment.op.worktree_path` | same as `context.environment.host.worktree_path` |
| `context.environment.op.inbox` | same as `context.environment.host.inbox` |
| `context.environment.op.outbox` | same as `context.environment.host.outbox` |

## Command Execution

`command_execution` now defaults `working_directory` to:

```yaml
working_directory: "{{ context.environment.op.worktree_path }}"
```

That means most commands do not need to set `working_directory` explicitly.

Direct execution:

```yaml
sequence:
  - id: write_result
    op: command_execution
    inputs:
      run: |
        mkdir -p "{{ context.environment.op.outbox }}/results"
        printf '{"status":"ok"}\n' > "{{ context.environment.op.outbox }}/results/status.json"
```

## Extension Ops

Extension op schema defaults can use op-visible paths. This lets recipe authors
use the invocation's worktree and artifact paths without overriding every input.

Example `op.yaml`:

```yaml
name: summarize_artifacts
run: python3 main.py

input_schema:
  type: object
  properties:
    workdir_path:
      type: string
      default: "{{ context.environment.op.workdir }}"
    worktree_path:
      type: string
      default: "{{ context.environment.op.worktree_path }}"
    artifact_inbox_path:
      type: string
      default: "{{ context.environment.op.inbox }}"
    artifact_outbox_path:
      type: string
      default: "{{ context.environment.op.outbox }}"
```

Recipe authors can then use the extension without overriding those path fields:

```yaml
sequence:
  - id: summarize
    op: ./tools/ops/summarize-artifacts
    inputs: {}
```

## Passing Paths To Prompts Or Agents

When an op receives a prompt or instruction string that mentions filesystem
locations, use op-visible paths:

```yaml
prompt: |
  Read source files from:
  {{ context.environment.op.worktree_path }}

  Read input artifacts from:
  {{ context.environment.op.inbox }}

  Write the final report to:
  {{ context.environment.op.outbox }}/final-report.md
```

Avoid hard-coding `/src`, `/src/git`, `/src/inbox`, or `/src/outbox` in prompts.
Use `context.environment.op.*` so paths follow the current invocation.

## Migration Guide

Switch paths passed to commands, prompts, agents, and extension inputs:

```diff
- "{{ context.environment.inbox }}"
+ "{{ context.environment.op.inbox }}"

- "{{ context.environment.outbox }}"
+ "{{ context.environment.op.outbox }}"
```

Replace hard-coded paths left over from sandboxed execution:

```diff
- /src/git
+ {{ context.environment.op.worktree_path }}

- /src/inbox
+ {{ context.environment.op.inbox }}

- /src/outbox
+ {{ context.environment.op.outbox }}
```

Keep `context.environment.host.*` or the older flat fields only when the host
path is the value you actually want.

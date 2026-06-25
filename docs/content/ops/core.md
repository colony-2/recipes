---
title: "Core c2j Ops"
weight: 51
---

Core c2j ops are registered by the c2j runtime.

## `command_execution`

Runs a bounded shell command.

Inputs:

```yaml
run: npm test
working_directory: "{{ context.environment.op.worktree_path }}"
shell: bash
env:
  CI: "true"
sandbox:
  type: none
continue_on_error: false
timeout: 5m
```

`sandbox` is supported by `command_execution`; see [Op-Visible Paths]({{% relref "/reference/op-visible-paths" %}}) for direct and sandboxed path examples.

Outputs:

```yaml
stdout: string
stderr: string
exit_code: number
success: boolean
timed_out: boolean
error_message: string
```

## `input`

Creates a human input form. Use structured fields rather than unstructured free text when possible.

Autofill example:

{{< example "examples/recipes/input-autofill.yaml" >}}

## `sleep`

Waits for a duration:

```yaml
- id: pause
  op: sleep
  inputs:
    duration: 5s
```

## Recipe Child Ops

Use these when manually composing child recipe orchestration:

- `recipe.run_and_get_result`
- `recipes.run`
- `recipes.run_and_wait`
- `recipe.await_result`
- `recipe.await_result_soft`
- `recipe.get_result`

See [Child Recipe Ops]({{% relref "/ops/child-recipes" %}}) for invocation shapes, output wrapping, and lifecycle examples. Prefer `child_group` for first-class fan-out/fan-in when the shape fits.

## Git Ops

- `thinpackrebase`
- `squashrebasemerge`

Use these for integration phases, not for intermediate validation.

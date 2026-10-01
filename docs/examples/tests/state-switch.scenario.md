# state-switch example

```yaml
recipe: ../recipes/state-switch.yaml
cases:
  - id: state-switch-fast
    type: recipe_case
    inputs:
      route: fast
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: selected
        value: fast path

  - id: state-switch-default
    type: recipe_case
    inputs:
      route: other
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: selected
        value: unknown path
```

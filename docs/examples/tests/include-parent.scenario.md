# include-parent example

```yaml
recipe: ../recipes/include-parent.yaml
cases:
  - id: include-parent
    type: recipe_case
    inputs:
      subject: docs
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: child_message
        value: child handled docs
```

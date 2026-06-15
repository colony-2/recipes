# input-autofill example

```yaml
cases:
  - id: input-autofill
    type: recipe_case
    inputs: {}
    mocks:
      ops:
        - match:
            op: input
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: decision
        value: approve
      - type: output_equals
        path: summary
        value: decision=approve
```

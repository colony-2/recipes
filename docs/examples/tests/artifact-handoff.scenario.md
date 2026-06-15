# artifact-handoff example

```yaml
cases:
  - id: artifact-handoff
    type: recipe_case
    inputs: {}
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
        path: content
        value: artifact handoff ok
```

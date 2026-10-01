# hello-command example

```yaml
recipe: ../recipes/hello-command.yaml
cases:
  - id: hello-command-default
    type: recipe_case
    inputs:
      name: docs
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: greeting
        value: hello docs
```

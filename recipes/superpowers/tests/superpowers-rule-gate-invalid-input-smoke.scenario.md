# superpowers-rule-gate-invalid-input-smoke test suite

```yaml
recipe: superpowers-rule-gate-invalid-input-smoke.yaml
cases:
  - id: ts-048-rule-gate-invalid-input-is-rejected
    type: recipe_case
    expect_error: "missing property 'type'"
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
```

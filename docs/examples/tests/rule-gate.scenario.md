# rule-gate example

```yaml
cases:
  - id: rule-gate
    type: recipe_case
    inputs: {}
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: docs-rule-gate/gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary:
                total: 2
                passed: 2
                failed: 0
              results: {}
    assertions:
      - type: output_equals
        path: ok
        value: true
      - type: output_equals
        path: failed_rule_ids
        value: []
```

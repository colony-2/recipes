# superpowers-rule-gate-schema-smoke test suite

```yaml
recipe: superpowers-rule-gate-schema-smoke.yaml
cases:
  - id: ts-047-rule-gate-validates-plan-and-routeable-policy-failures
    type: recipe_case
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: valid_plan_ok
        value: true
      - type: output_equals
        path: valid_plan_failed_count
        value: 0
      - type: output_equals
        path: schema_policy_ok_false
        value: true
      - type: output_equals
        path: assert_policy_ok_false
        value: true
      - type: output_equals
        path: child_completed_ok
        value: true
      - type: output_equals
        path: child_failed_routeable
        value: true
```

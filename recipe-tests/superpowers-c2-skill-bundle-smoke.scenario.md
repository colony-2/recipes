# superpowers-c2-skill-bundle-smoke test suite

```yaml
cases:
  - id: ts-058-c2-superpowers-skill-bundle-contract
    type: recipe_case
    inputs:
      repo_root: /src
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: ok
        value: true
      - type: output_equals
        path: skill_count
        value: 10
      - type: output_equals
        path: actual_superpowers_skill_count
        value: 10
      - type: output_equals
        path: missing_count
        value: 0
      - type: output_equals
        path: unexpected_count
        value: 0
      - type: output_equals
        path: violation_count
        value: 0
```

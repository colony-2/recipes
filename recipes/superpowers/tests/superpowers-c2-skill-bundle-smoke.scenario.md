# superpowers-c2-skill-bundle-smoke test suite

```yaml
recipe: superpowers-c2-skill-bundle-smoke.yaml
cases:
  - id: ts-058-c2-superpowers-skill-bundle-contract
    type: recipe_case
    runtime:
      cells:
        root:
          file_sources:
            skills-bundle: ../../../skills-bundle
            recipes/superpowers: ..
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

  - id: ts-091-superpowers-run-skill-installs-skill-bundle-ref
    type: recipe_case
    runtime:
      cells:
        root:
          file_sources:
            skills-bundle: ../../../skills-bundle
            recipes/superpowers: ..
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
        path: has_recipe_skill_invocations
        value: true
      - type: output_equals
        path: all_recipe_skill_invocations_wired
        value: true
      - type: output_equals
        path: skill_source_violation_count
        value: 0
```

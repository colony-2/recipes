# superpowers-run-skill-repair-smoke test suite

```yaml
cases:
  - id: ts-057-run-skill-repair-attempt-is-visible-to-recipes
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
            node_path: "superpowers-run-skill-repair-smoke/run_skill/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &run_skill_repair_output
              status: completed
              sessionId: sid-run-skill-repair
              assistantSummary: Repaired output artifact.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: superpowers-ticket-intake
              raw_summary: Repaired output artifact.
              output_source: artifact
              output_path: superpowers/run-skill/result.json
              raw_output: '{"summary":"Repaired result."}'
              parsed_output:
                summary: Repaired result.
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 1
              status_contract_path: superpowers/run-skill/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
              status_contract_errors: []
              diagnostics:
                repaired: true
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs: *run_skill_repair_output
    assertions:
      - type: output_equals
        path: skill
        value: superpowers-ticket-intake
      - type: output_equals
        path: status
        value: completed
      - type: output_equals
        path: parsed_summary
        value: Repaired result.
      - type: output_equals
        path: output_schema_valid
        value: true
      - type: output_equals
        path: output_schema_errors
        value: []
      - type: output_equals
        path: output_repair_attempts
        value: 1
      - type: output_equals
        path: status_contract_present
        value: true
      - type: output_equals
        path: status_contract_valid
        value: true
      - type: output_equals
        path: repaired_in_same_session
        value: true
```

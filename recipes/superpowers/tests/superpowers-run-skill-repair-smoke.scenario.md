# superpowers-run-skill-repair-smoke test suite

```yaml
recipe: superpowers-run-skill-repair-smoke.yaml
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
            node_path: "superpowers-run-skill-repair-smoke/run_skill/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &run_skill_repair_output
              status: completed
              sessionId: sid-run-skill-repair
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "11283f00a77a6a086f86c39483e06411ccfe9e01709dc4da4712323c441de7ec", "artifact": {"jobId": "sid-run-skill-repair", "taskOrdinal": 2, "name": "__c2j_objects__/11283f00a77a6a086f86c39483e06411ccfe9e01709dc4da4712323c441de7ec.tar", "sizeBytes": 100}}
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

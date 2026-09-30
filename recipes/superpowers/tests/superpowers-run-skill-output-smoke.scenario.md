# superpowers-run-skill-output-smoke test suite

```yaml
cases:
  - id: ts-056-run-skill-validates-output-artifact-and-status-contract
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
            node_path: "superpowers-run-skill-output-smoke/run_skill/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &run_skill_output
              status: completed
              sessionId: sid-run-skill
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "d77f1e08c56cac7bef92d44aa03614777d52eae429e1a328c3dfbfb3fef810e5", "artifact": {"jobId": "sid-run-skill", "taskOrdinal": 2, "name": "__c2j_objects__/d77f1e08c56cac7bef92d44aa03614777d52eae429e1a328c3dfbfb3fef810e5.tar", "sizeBytes": 100}}
              assistantSummary: Run skill output artifact validated.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: superpowers-ticket-intake
              raw_summary: Run skill output artifact validated.
              output_source: artifact
              output_path: superpowers/run-skill/result.json
              raw_output: '{"summary":"Selected execute-plan path.","selected_skill":"superpowers-ticket-intake","next_phase":"execute_plan"}'
              parsed_output:
                summary: Selected execute-plan path.
                selected_skill: superpowers-ticket-intake
                next_phase: execute_plan
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/run-skill/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Skill completed.
                  reason: done
              status_contract_errors: []
              diagnostics: {}
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs: *run_skill_output
    assertions:
      - type: output_equals
        path: skill
        value: superpowers-ticket-intake
      - type: output_equals
        path: status
        value: completed
      - type: output_equals
        path: parsed_summary
        value: Selected execute-plan path.
      - type: output_equals
        path: parsed_selected_skill
        value: superpowers-ticket-intake
      - type: output_equals
        path: parsed_next_phase
        value: execute_plan
      - type: output_equals
        path: output_source
        value: artifact
      - type: output_equals
        path: output_path
        value: superpowers/run-skill/result.json
      - type: output_equals
        path: output_schema_valid
        value: true
      - type: output_equals
        path: output_repair_attempts
        value: 0
      - type: output_equals
        path: status_contract_present
        value: true
      - type: output_equals
        path: status_contract_valid
        value: true
      - type: output_equals
        path: status_contract_status
        value: completed
      - type: output_equals
        path: run_skill_contract_valid
        value: true
```

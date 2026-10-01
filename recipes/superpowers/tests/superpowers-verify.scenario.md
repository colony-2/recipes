# superpowers-verify test suite

```yaml
recipe: ../superpowers-verify.yaml
cases:
  - id: ts-069-verify-runs-required-commands-before-success
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-VERIFY-1",
          "summary": "Verify completed task.",
          "tasks": [
            {
              "id": "TASK-1",
              "status": "done",
              "validation_commands": ["printf verified"]
            }
          ],
          "validation_strategy": {"commands": ["printf verified"]}
        }
      execution_result_json: |
        {"task_id":"TASK-1","status":"done","summary":"Task completed."}
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
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-verify/summarize_verification
          behavior:
            mode: return
            outputs: &verify_ok
              status: completed
              sessionId: sid-verify-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "8409e7cfcc67eb6e868e2af6c5a8d5f1d97f910868d6135df3100fbfd07f6732", "artifact": {"jobId": "sid-verify-1", "taskOrdinal": 2, "name": "__c2j_objects__/8409e7cfcc67eb6e868e2af6c5a8d5f1d97f910868d6135df3100fbfd07f6732.tar", "sizeBytes": 100}}
              assistantSummary: Verification passed.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-verify
              raw_summary: Verification passed.
              output_source: artifact
              output_path: superpowers/verify/result.json
              raw_output: '{"ok":true,"commands_required":["printf verified"],"commands_observed":[{"command":"printf verified","exit_code":0}],"evidence_summary":"Required verification command passed.","blocking_issues":[]}'
              parsed_output:
                ok: true
                commands_required:
                  - printf verified
                commands_observed:
                  - command: printf verified
                    exit_code: 0
                evidence_summary: Required verification command passed.
                blocking_issues: []
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/verify/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Verification passed.
                  reason: verified
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers-verify/verification_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: verification gate passed
              results: {}
    assertions:
      - type: output_equals
        path: plan_id
        value: PLAN-VERIFY-1
      - type: output_equals
        path: commands_required_count
        value: 1
      - type: output_equals
        path: validation_exit_code
        value: 0
      - type: output_equals
        path: validation_passed
        value: true
      - type: output_equals
        path: verification_ok
        value: true
      - type: output_equals
        path: verification_gate_ok
        value: true
      - type: node_executed
        node_path: superpowers-verify/run_verification_commands

  - id: ts-070-verify-keeps-failing-command-evidence-as-blocking-data
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-VERIFY-2",
          "summary": "Verify failed task.",
          "tasks": [
            {
              "id": "TASK-FAIL",
              "status": "done",
              "validation_commands": ["printf failing && exit 7"]
            }
          ],
          "validation_strategy": {"commands": ["printf failing && exit 7"]}
        }
      execution_result_json: |
        {"task_id":"TASK-FAIL","status":"done","summary":"Task claims completion."}
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
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-verify/summarize_verification
          behavior:
            mode: return
            outputs:
              <<: *verify_ok
              sessionId: sid-verify-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "09f5ac680d045aa52acc6e9650d96be24d6200aad83603b37d04ea14b3742377", "artifact": {"jobId": "sid-verify-2", "taskOrdinal": 3, "name": "__c2j_objects__/09f5ac680d045aa52acc6e9650d96be24d6200aad83603b37d04ea14b3742377.tar", "sizeBytes": 100}}
              assistantSummary: Verification failed.
              raw_summary: Verification failed.
              raw_output: '{"ok":false,"commands_required":["printf failing && exit 7"],"commands_observed":[{"command":"printf failing && exit 7","exit_code":7}],"evidence_summary":"Required verification command failed.","blocking_issues":["Validation command exited 7."]}'
              parsed_output:
                ok: false
                commands_required:
                  - printf failing && exit 7
                commands_observed:
                  - command: printf failing && exit 7
                    exit_code: 7
                evidence_summary: Required verification command failed.
                blocking_issues:
                  - Validation command exited 7.
        - match:
            node_path: superpowers-verify/verification_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: false
              failed_rule_ids:
                - command_exit_zero
                - verify_ok
              summary: verification gate failed
              results: {}
    assertions:
      - type: output_equals
        path: plan_id
        value: PLAN-VERIFY-2
      - type: output_equals
        path: commands_required_count
        value: 1
      - type: output_equals
        path: validation_exit_code
        value: 7
      - type: output_equals
        path: validation_passed
        value: false
      - type: output_equals
        path: verification_ok
        value: false
      - type: output_equals
        path: verification_gate_ok
        value: false
      - type: output_equals
        path: verification_blocking_issue_count
        value: 1
```

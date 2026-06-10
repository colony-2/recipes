# superpowers-execute-plan test suite

```yaml
cases:
  - id: ts-067-execute-plan-runs-same-job-task-boundary
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-1",
          "summary": "Two dependent tasks.",
          "tasks": [
            {
              "id": "TASK-1",
              "title": "Add export authorization",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "child_job_reason": "",
              "instructions": "Add authorization checks.",
              "validation_commands": ["go test ./..."],
              "review_requirements": ["spec", "quality"]
            }
          ],
          "ready_task_ids": ["TASK-1"],
          "validation_strategy": {"commands": ["go test ./..."]},
          "child_job_boundaries": []
        }
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
            op: sleep
          behavior:
            mode: return
            outputs: {}
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/implement_task"
          behavior:
            mode: return
            outputs: &implement_done
              status: completed
              sessionId: sid-implement-1
              assistantSummary: TASK-1 implemented.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-task-implementer
              raw_summary: TASK-1 implemented.
              output_source: artifact
              output_path: superpowers/tasks/result.json
              raw_output: '{"task_id":"TASK-1","status":"done","summary":"Implemented TASK-1.","validation_commands_run":["go test ./..."]}'
              parsed_output:
                task_id: TASK-1
                status: done
                summary: Implemented TASK-1.
                validation_commands_run:
                  - go test ./...
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/tasks/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: TASK-1 implemented.
                  reason: done
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/spec_review"
          behavior:
            mode: return
            outputs: &spec_ok
              <<: *implement_done
              sessionId: sid-spec-1
              skill: c2-superpowers-spec-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Spec matches.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Spec matches.
                requires_revision: false
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/quality_review"
          behavior:
            mode: return
            outputs: &quality_ok
              <<: *implement_done
              sessionId: sid-quality-1
              skill: c2-superpowers-quality-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Quality acceptable.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Quality acceptable.
                requires_revision: false
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/task_gate"
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: task gate passed
              results: {}
    assertions:
      - type: output_equals
        path: selected_task_id
        value: TASK-1
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: implementation_status
        value: done
      - type: output_equals
        path: spec_review_ok
        value: true
      - type: output_equals
        path: quality_review_ok
        value: true
      - type: output_equals
        path: task_done
        value: true
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/sequence/implement_task"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/sequence/task_gate"

  - id: ts-068-execute-plan-stops-at-required-child-boundary
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-2",
          "summary": "Cross-cell task.",
          "tasks": [
            {
              "id": "TASK-CELL",
              "title": "Delegate reporting update",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": true,
              "child_job_reason": "cross-cell work",
              "instructions": "Run in reporting cell.",
              "validation_commands": [],
              "review_requirements": ["spec"]
            }
          ],
          "ready_task_ids": ["TASK-CELL"],
          "validation_strategy": {"commands": []},
          "child_job_boundaries": [{"task_id":"TASK-CELL","reason":"cross-cell work"}]
        }
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
            op: sleep
          behavior:
            mode: return
            outputs: {}
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/implement_task"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/spec_review"
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/quality_review"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/sequence/task_gate"
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: validation-only mock
              results: {}
    assertions:
      - type: output_equals
        path: selected_task_id
        value: TASK-CELL
      - type: output_equals
        path: child_job_required
        value: true
      - type: output_equals
        path: child_job_reason
        value: cross-cell work
      - type: output_equals
        path: implementer_session_id
        value: ""
      - type: output_equals
        path: task_done
        value: false
      - type: node_executed
        node_path: "superpowers-execute-plan/child_boundary_required/command_execution"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/sequence/implement_task"
```

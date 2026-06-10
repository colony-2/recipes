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

  - id: ts-082-execute-plan-enforces-tdd-red-green-refactor
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-TDD",
          "summary": "TDD task.",
          "tasks": [
            {
              "id": "TASK-TDD",
              "title": "Add behavior with TDD",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "requires_tdd": true,
              "child_job_reason": "",
              "instructions": "Add behavior with a failing test first.",
              "validation_commands": ["printf green"],
              "review_requirements": ["spec", "quality"],
              "tdd": {
                "red_command": "printf 'expected failure' && exit 7",
                "red_expected_failure": "expected failure",
                "green_command": "printf green",
                "refactor_verification_command": "printf refactor"
              }
            }
          ],
          "ready_task_ids": ["TASK-TDD"],
          "validation_strategy": {"commands": ["printf green"]},
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
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: command_execution
          behavior:
            mode: passthrough
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &red_written
              <<: *implement_done
              sessionId: sid-red-1
              raw_output: '{"task_id":"TASK-TDD","status":"red_written","summary":"RED test written.","red_command":"printf expected failure && exit 7"}'
              parsed_output:
                task_id: TASK-TDD
                status: red_written
                summary: RED test written.
                red_command: printf expected failure && exit 7
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_red/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: &tdd_gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: tdd gate passed
              results: {}
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &green_done
              <<: *implement_done
              sessionId: sid-green-1
              raw_output: '{"task_id":"TASK-TDD","status":"done","summary":"GREEN implementation completed.","validation_commands_run":["printf green"]}'
              parsed_output:
                task_id: TASK-TDD
                status: done
                summary: GREEN implementation completed.
                validation_commands_run:
                  - printf green
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &refactor_done
              <<: *green_done
              sessionId: sid-refactor-1
              raw_output: '{"task_id":"TASK-TDD","status":"done","summary":"Refactor kept behavior green.","validation_commands_run":["printf refactor"]}'
              parsed_output:
                task_id: TASK-TDD
                status: done
                summary: Refactor kept behavior green.
                validation_commands_run:
                  - printf refactor
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-tdd-spec-1
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok
              sessionId: sid-tdd-quality-1
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
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
            outputs: *tdd_gate_ok
    assertions:
      - type: output_equals
        path: selected_task_id
        value: TASK-TDD
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: implementation_status
        value: done
      - type: output_equals
        path: tdd_evidence_ok
        value: true
      - type: output_equals
        path: tdd_red_exit_code
        value: 7
      - type: output_equals
        path: tdd_green_exit_code
        value: 0
      - type: output_equals
        path: tdd_refactor_exit_code
        value: 0
      - type: output_equals
        path: task_done
        value: true
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/sequence/implement_task"
```

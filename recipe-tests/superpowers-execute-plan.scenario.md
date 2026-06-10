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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: &task_gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: task gate passed
              results: {}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &revision_done
              <<: *implement_done
              sessionId: sid-revision-1
              raw_output: '{"task_id":"TASK-1","status":"done","summary":"Revised TASK-1.","validation_commands_run":["go test ./..."]}'
              parsed_output:
                task_id: TASK-1
                status: done
                summary: Revised TASK-1.
                validation_commands_run:
                  - go test ./...
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *revision_done
              sessionId: sid-revision-quality-1
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &spec_ok_after_revision
              <<: *spec_ok
              sessionId: sid-spec-after-revision-1
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &quality_ok_after_revision
              <<: *quality_ok
              sessionId: sid-quality-after-revision-1
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"

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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *spec_ok_after_revision
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *quality_ok_after_revision
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-095-execute-plan-stops-when-no-ready-task-exists
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-DONE",
          "summary": "No remaining work.",
          "tasks": [
            {
              "id": "TASK-DONE",
              "title": "Already completed task",
              "status": "done",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "child_job_reason": "",
              "instructions": "No work remains.",
              "validation_commands": [],
              "review_requirements": []
            }
          ],
          "ready_task_ids": [],
          "validation_strategy": {"commands": []},
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
    assertions:
      - type: output_equals
        path: selected_task_id
        value: ""
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: task_done
        value: false
      - type: node_executed
        node_path: "superpowers-execute-plan/no_task_selected/command_execution"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/child_boundary_required/command_execution"

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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *spec_ok_after_revision
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *quality_ok_after_revision
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-083-execute-plan-routes-spec-failure-through-revision
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-REVISION",
          "summary": "Revision task.",
          "tasks": [
            {
              "id": "TASK-REV",
              "title": "Revise after spec review",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "child_job_reason": "",
              "instructions": "Implement behavior and address review feedback.",
              "validation_commands": ["printf verified"],
              "review_requirements": ["spec", "quality"]
            }
          ],
          "ready_task_ids": ["TASK-REV"],
          "validation_strategy": {"commands": ["printf verified"]},
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &spec_needs_revision
              <<: *spec_ok
              sessionId: sid-spec-needs-revision-1
              raw_output: '{"ok":false,"blocking_issues":["Missing required acceptance behavior."],"feedback":"Add the required behavior.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Missing required acceptance behavior.
                feedback: Add the required behavior.
                requires_revision: true
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *revision_done
              sessionId: sid-revision-spec-2
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok_after_revision
              sessionId: sid-spec-after-revision-2
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok_after_revision
              sessionId: sid-quality-after-revision-2
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
    assertions:
      - type: output_equals
        path: selected_task_id
        value: TASK-REV
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: revision_attempted
        value: true
      - type: output_equals
        path: revision_session_id
        value: sid-revision-spec-2
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-084-execute-plan-routes-quality-failure-through-revision
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-QUALITY-REVISION",
          "summary": "Quality revision task.",
          "tasks": [
            {
              "id": "TASK-QUALITY",
              "title": "Revise after quality review",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "child_job_reason": "",
              "instructions": "Implement behavior and address quality review feedback.",
              "validation_commands": ["printf verified"],
              "review_requirements": ["spec", "quality"]
            }
          ],
          "ready_task_ids": ["TASK-QUALITY"],
          "validation_strategy": {"commands": ["printf verified"]},
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *implement_done
              sessionId: sid-implement-quality-1
              raw_output: '{"task_id":"TASK-QUALITY","status":"done","summary":"Implemented TASK-QUALITY.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-QUALITY
                status: done
                summary: Implemented TASK-QUALITY.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-spec-quality-1
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok
              sessionId: sid-quality-needs-revision-1
              raw_output: '{"ok":false,"blocking_issues":["Validation evidence is too weak."],"feedback":"Add stronger validation evidence.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Validation evidence is too weak.
                feedback: Add stronger validation evidence.
                requires_revision: true
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *revision_done
              sessionId: sid-revision-quality-2
              raw_output: '{"task_id":"TASK-QUALITY","status":"done","summary":"Revised TASK-QUALITY.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-QUALITY
                status: done
                summary: Revised TASK-QUALITY.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok_after_revision
              sessionId: sid-spec-after-quality-revision-1
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok_after_revision
              sessionId: sid-quality-after-quality-revision-1
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
    assertions:
      - type: output_equals
        path: selected_task_id
        value: TASK-QUALITY
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: revision_attempted
        value: true
      - type: output_equals
        path: revision_session_id
        value: sid-revision-quality-2
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-087-execute-plan-routes-tdd-spec-failure-through-revision
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "PLAN-TDD-REVISION",
          "summary": "TDD spec revision task.",
          "tasks": [
            {
              "id": "TASK-TDD-REV",
              "title": "Revise TDD task after spec review",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "requires_tdd": true,
              "child_job_reason": "",
              "instructions": "Add behavior with TDD and revise after spec feedback.",
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
          "ready_task_ids": ["TASK-TDD-REV"],
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
            outputs:
              <<: *red_written
              sessionId: sid-tdd-rev-red
              raw_output: '{"task_id":"TASK-TDD-REV","status":"red_written","summary":"RED test written.","red_command":"printf expected failure && exit 7"}'
              parsed_output:
                task_id: TASK-TDD-REV
                status: red_written
                summary: RED test written.
                red_command: printf expected failure && exit 7
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_red/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *green_done
              sessionId: sid-tdd-rev-green
              raw_output: '{"task_id":"TASK-TDD-REV","status":"done","summary":"GREEN implementation completed.","validation_commands_run":["printf green"]}'
              parsed_output:
                task_id: TASK-TDD-REV
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
            outputs:
              <<: *refactor_done
              sessionId: sid-tdd-rev-refactor
              raw_output: '{"task_id":"TASK-TDD-REV","status":"done","summary":"Refactor kept behavior green.","validation_commands_run":["printf refactor"]}'
              parsed_output:
                task_id: TASK-TDD-REV
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
              <<: *spec_needs_revision
              sessionId: sid-tdd-spec-needs-revision
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &tdd_revision_done
              <<: *refactor_done
              sessionId: sid-tdd-revision-spec-1
              raw_output: '{"task_id":"TASK-TDD-REV","status":"done","summary":"Revised TDD task after spec review.","validation_commands_run":["printf green","printf refactor"]}'
              parsed_output:
                task_id: TASK-TDD-REV
                status: done
                summary: Revised TDD task after spec review.
                validation_commands_run:
                  - printf green
                  - printf refactor
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: *tdd_revision_done
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok_after_revision
              sessionId: sid-tdd-spec-after-revision-1
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok_after_revision
              sessionId: sid-tdd-quality-after-revision-1
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
    assertions:
      - type: output_equals
        path: selected_task_id
        value: TASK-TDD-REV
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: revision_attempted
        value: true
      - type: output_equals
        path: revision_session_id
        value: sid-tdd-revision-spec-1
      - type: output_equals
        path: implementer_session_id
        value: sid-tdd-revision-spec-1
      - type: output_equals
        path: spec_reviewer_session_id
        value: sid-tdd-spec-after-revision-1
      - type: output_equals
        path: quality_reviewer_session_id
        value: sid-tdd-quality-after-revision-1
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
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
```

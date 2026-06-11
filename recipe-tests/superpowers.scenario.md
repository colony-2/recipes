# superpowers primary orchestrator test suite

```yaml
cases:
  - id: ts-080-superpowers-orchestrates-same-job-happy-path
    type: recipe_case
    inputs:
      prompt: Add an audit-log export feature for admins.
      completion_action: recommend
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
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers/brainstorm_design/brainstorm_design/superpowers-brainstorm/brainstorm
          behavior:
            mode: return
            outputs: &brainstorm_ok
              status: completed
              sessionId: sid-brainstorm-primary
              assistantSummary: Design approved for planning.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-brainstorm
              raw_summary: Design approved for planning.
              output_source: artifact
              output_path: superpowers/brainstorm/result.json
              raw_output: '{"summary":"Design admin audit-log export.","recommended_approach":"Add scoped export endpoint and status visibility.","alternatives":[],"open_questions":[],"approved_for_planning":true,"plan_inputs":{"required_outcomes":["admin-only authorization","export job","status visibility"]}}'
              parsed_output:
                summary: Design admin audit-log export.
                recommended_approach: Add scoped export endpoint and status visibility.
                alternatives: []
                open_questions: []
                approved_for_planning: true
                plan_inputs:
                  required_outcomes:
                    - admin-only authorization
                    - export job
                    - status visibility
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/brainstorm/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Design approved for planning.
                  reason: approved
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers/write_plan/write_plan/superpowers-write-plan/write_plan
          behavior:
            mode: return
            outputs: &plan_ready
              <<: *brainstorm_ok
              sessionId: sid-write-plan-primary
              skill: c2-superpowers-write-plan
              raw_output: '{"plan_id":"PLAN-PRIMARY-1","summary":"Implement admin audit-log export.","tasks":[{"id":"TASK-1","title":"Add admin export path","status":"pending","dependencies":[],"target_ref":"main","requires_child_job":false,"child_job_reason":"","instructions":"Add admin-only audit-log export behavior.","validation_commands":["printf verified"],"review_requirements":["spec","quality"]}],"ready_task_ids":["TASK-1"],"validation_strategy":{"commands":["printf verified"]},"child_job_boundaries":[]}'
              parsed_output:
                plan_id: PLAN-PRIMARY-1
                summary: Implement admin audit-log export.
                tasks:
                  - id: TASK-1
                    title: Add admin export path
                    status: pending
                    dependencies: []
                    target_ref: main
                    requires_child_job: false
                    child_job_reason: ""
                    instructions: Add admin-only audit-log export behavior.
                    validation_commands:
                      - printf verified
                    review_requirements:
                      - spec
                      - quality
                ready_task_ids:
                  - TASK-1
                validation_strategy:
                  commands:
                    - printf verified
                child_job_boundaries: []
        - match:
            node_path: superpowers/review_plan/review_plan/superpowers-plan-review/review_plan
          behavior:
            mode: return
            outputs: &plan_review_ok
              <<: *brainstorm_ok
              sessionId: sid-plan-review-primary
              skill: c2-superpowers-plan-review
              raw_output: '{"ok":true,"issues":[],"recommendations":["Keep verification scoped."],"blocking_feedback":"","requires_replan":false}'
              parsed_output:
                ok: true
                issues: []
                recommendations:
                  - Keep verification scoped.
                blocking_feedback: ""
                requires_replan: false
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &implement_done
              <<: *brainstorm_ok
              sessionId: sid-implement-primary
              skill: c2-superpowers-task-implementer
              raw_output: '{"task_id":"TASK-1","status":"done","summary":"Implemented TASK-1.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-1
                status: done
                summary: Implemented TASK-1.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &spec_ok
              <<: *brainstorm_ok
              sessionId: sid-spec-primary
              skill: c2-superpowers-spec-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Spec matches.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Spec matches.
                requires_revision: false
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-quality-primary
              skill: c2-superpowers-quality-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Quality acceptable.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Quality acceptable.
                requires_revision: false
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: &gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: gate passed
              results: {}
        - match:
            node_path: superpowers/brainstorm_design/brainstorm_design/superpowers-brainstorm/brainstorm_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/write_plan/write_plan/superpowers-write-plan/plan_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/review_plan/review_plan/superpowers-plan-review/plan_review_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/summarize_verification
          behavior:
            mode: return
            outputs: &verify_ok
              <<: *brainstorm_ok
              sessionId: sid-verify-primary
              skill: c2-superpowers-verify
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
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/verification_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *brainstorm_ok
              sessionId: sid-finish-primary
              skill: c2-superpowers-finish
              raw_output: '{"decision":"merge_ready","summary":"Verified work is ready to merge.","completed_tasks":["TASK-1"],"verification_summary":"Required verification command passed.","remaining_risks":[],"merge_ready":true}'
              parsed_output:
                decision: merge_ready
                summary: Verified work is ready to merge.
                completed_tasks:
                  - TASK-1
                verification_summary: Required verification command passed.
                remaining_risks: []
                merge_ready: true
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs: *gate_ok
    assertions:
      - type: output_equals
        path: route
        value: brainstorm
      - type: output_equals
        path: workflow_status
        value: merge_ready
      - type: output_equals
        path: selected_task_id
        value: TASK-1
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: task_done
        value: true
      - type: output_equals
        path: verification_ok
        value: true
      - type: output_equals
        path: finish_decision
        value: merge_ready
      - type: output_equals
        path: action_taken
        value: recommend
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: superpowers/verify_work/verify_work/superpowers-verify/run_verification_commands

  - id: ts-081-superpowers-stops-at-required-child-boundary
    type: recipe_case
    inputs:
      prompt: Continue this cross-cell plan.
      plan_json: |
        {
          "plan_id": "PLAN-PRIMARY-2",
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
    assertions:
      - type: output_equals
        path: route
        value: execute_plan
      - type: output_equals
        path: workflow_status
        value: child_job_required
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
        path: task_done
        value: false
      - type: node_executed
        node_path: superpowers/child_boundary_required/command_execution
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-085-superpowers-primary-routes-spec-failure-through-revision
    type: recipe_case
    inputs:
      prompt: Continue this plan and revise if review blocks it.
      mode: execute_plan
      completion_action: recommend
      plan_json: |
        {
          "plan_id": "PLAN-PRIMARY-REVISION",
          "summary": "Primary revision task.",
          "tasks": [
            {
              "id": "TASK-PRIMARY-REV",
              "title": "Revise primary task after spec review",
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
          "ready_task_ids": ["TASK-PRIMARY-REV"],
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
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *implement_done
              sessionId: sid-implement-primary-revision
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-spec-primary-needs-revision
              raw_output: '{"ok":false,"blocking_issues":["Missing required acceptance behavior."],"feedback":"Add the required behavior.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Missing required acceptance behavior.
                feedback: Add the required behavior.
                requires_revision: true
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &revision_done
              <<: *implement_done
              sessionId: sid-primary-spec-revision
              raw_output: '{"task_id":"TASK-PRIMARY-REV","status":"done","summary":"Revised TASK-PRIMARY-REV.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-PRIMARY-REV
                status: done
                summary: Revised TASK-PRIMARY-REV.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-spec-after-revision
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-quality-after-revision
              skill: c2-superpowers-quality-reviewer
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/summarize_verification
          behavior:
            mode: return
            outputs: *verify_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/verification_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *brainstorm_ok
              sessionId: sid-finish-primary-revision
              skill: c2-superpowers-finish
              raw_output: '{"decision":"merge_ready","summary":"Verified revised work is ready to merge.","completed_tasks":["TASK-PRIMARY-REV"],"verification_summary":"Required verification command passed.","remaining_risks":[],"merge_ready":true}'
              parsed_output:
                decision: merge_ready
                summary: Verified revised work is ready to merge.
                completed_tasks:
                  - TASK-PRIMARY-REV
                verification_summary: Required verification command passed.
                remaining_risks: []
                merge_ready: true
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs: *gate_ok
    assertions:
      - type: output_equals
        path: route
        value: execute_plan
      - type: output_equals
        path: workflow_status
        value: merge_ready
      - type: output_equals
        path: selected_task_id
        value: TASK-PRIMARY-REV
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: revision_attempted
        value: true
      - type: output_equals
        path: revision_session_id
        value: sid-primary-spec-revision
      - type: output_equals
        path: task_done
        value: true
      - type: output_equals
        path: verification_ok
        value: true
      - type: output_equals
        path: finish_decision
        value: merge_ready
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-086-superpowers-primary-enforces-tdd-red-green-refactor
    type: recipe_case
    inputs:
      prompt: Continue this plan using TDD.
      mode: execute_plan
      completion_action: recommend
      plan_json: |
        {
          "plan_id": "PLAN-PRIMARY-TDD",
          "summary": "Primary TDD task.",
          "tasks": [
            {
              "id": "TASK-PRIMARY-TDD",
              "title": "Add primary behavior with TDD",
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
          "ready_task_ids": ["TASK-PRIMARY-TDD"],
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
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &primary_tdd_red
              <<: *implement_done
              sessionId: sid-primary-tdd-red
              raw_output: '{"task_id":"TASK-PRIMARY-TDD","status":"red_written","summary":"RED test written.","red_command":"printf expected failure && exit 7"}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD
                status: red_written
                summary: RED test written.
                red_command: printf expected failure && exit 7
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_red/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &primary_tdd_green
              <<: *implement_done
              sessionId: sid-primary-tdd-green
              raw_output: '{"task_id":"TASK-PRIMARY-TDD","status":"done","summary":"GREEN implementation completed.","validation_commands_run":["printf green"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD
                status: done
                summary: GREEN implementation completed.
                validation_commands_run:
                  - printf green
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *primary_tdd_green
              sessionId: sid-primary-tdd-refactor
              raw_output: '{"task_id":"TASK-PRIMARY-TDD","status":"done","summary":"Refactor kept behavior green.","validation_commands_run":["printf refactor"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD
                status: done
                summary: Refactor kept behavior green.
                validation_commands_run:
                  - printf refactor
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-spec
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-quality
              skill: c2-superpowers-quality-reviewer
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/summarize_verification
          behavior:
            mode: return
            outputs: *verify_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/verification_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *brainstorm_ok
              sessionId: sid-primary-tdd-finish
              skill: c2-superpowers-finish
              raw_output: '{"decision":"merge_ready","summary":"Verified TDD work is ready to merge.","completed_tasks":["TASK-PRIMARY-TDD"],"verification_summary":"Required verification command passed.","remaining_risks":[],"merge_ready":true}'
              parsed_output:
                decision: merge_ready
                summary: Verified TDD work is ready to merge.
                completed_tasks:
                  - TASK-PRIMARY-TDD
                verification_summary: Required verification command passed.
                remaining_risks: []
                merge_ready: true
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs: *gate_ok
    assertions:
      - type: output_equals
        path: route
        value: execute_plan
      - type: output_equals
        path: workflow_status
        value: merge_ready
      - type: output_equals
        path: selected_task_id
        value: TASK-PRIMARY-TDD
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: task_done
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
        path: implementer_session_id
        value: sid-primary-tdd-refactor
      - type: output_equals
        path: spec_reviewer_session_id
        value: sid-primary-tdd-spec
      - type: output_equals
        path: quality_reviewer_session_id
        value: sid-primary-tdd-quality
      - type: output_equals
        path: verification_ok
        value: true
      - type: output_equals
        path: finish_decision
        value: merge_ready
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"

  - id: ts-088-superpowers-primary-routes-tdd-spec-failure-through-revision
    type: recipe_case
    inputs:
      prompt: Continue this TDD plan and revise after review.
      mode: execute_plan
      completion_action: recommend
      plan_json: |
        {
          "plan_id": "PLAN-PRIMARY-TDD-REVISION",
          "summary": "Primary TDD revision task.",
          "tasks": [
            {
              "id": "TASK-PRIMARY-TDD-REV",
              "title": "Revise primary behavior with TDD",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": false,
              "requires_tdd": true,
              "child_job_reason": "",
              "instructions": "Add behavior with a failing test first and revise after spec feedback.",
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
          "ready_task_ids": ["TASK-PRIMARY-TDD-REV"],
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
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &primary_tdd_revision_red
              <<: *implement_done
              sessionId: sid-primary-tdd-rev-red
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"red_written","summary":"RED test written.","red_command":"printf expected failure && exit 7"}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: red_written
                summary: RED test written.
                red_command: printf expected failure && exit 7
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_red/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &primary_tdd_revision_green
              <<: *implement_done
              sessionId: sid-primary-tdd-rev-green
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"done","summary":"GREEN implementation completed.","validation_commands_run":["printf green"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: done
                summary: GREEN implementation completed.
                validation_commands_run:
                  - printf green
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *primary_tdd_revision_green
              sessionId: sid-primary-tdd-rev-refactor
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"done","summary":"Refactor kept behavior green.","validation_commands_run":["printf refactor"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: done
                summary: Refactor kept behavior green.
                validation_commands_run:
                  - printf refactor
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-spec-needs-revision
              raw_output: '{"ok":false,"blocking_issues":["Missing required TDD acceptance behavior."],"feedback":"Add the required behavior before finishing.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Missing required TDD acceptance behavior.
                feedback: Add the required behavior before finishing.
                requires_revision: true
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &primary_tdd_revision_done
              <<: *implement_done
              sessionId: sid-primary-tdd-revision-spec
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"done","summary":"Revised TDD task after spec review.","validation_commands_run":["printf green","printf refactor"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: done
                summary: Revised TDD task after spec review.
                validation_commands_run:
                  - printf green
                  - printf refactor
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-spec-after-revision
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-quality-after-revision
              skill: c2-superpowers-quality-reviewer
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/summarize_verification
          behavior:
            mode: return
            outputs: *verify_ok
        - match:
            node_path: superpowers/verify_work/verify_work/superpowers-verify/verification_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *brainstorm_ok
              sessionId: sid-primary-tdd-revision-finish
              skill: c2-superpowers-finish
              raw_output: '{"decision":"merge_ready","summary":"Verified revised TDD work is ready to merge.","completed_tasks":["TASK-PRIMARY-TDD-REV"],"verification_summary":"Required verification command passed.","remaining_risks":[],"merge_ready":true}'
              parsed_output:
                decision: merge_ready
                summary: Verified revised TDD work is ready to merge.
                completed_tasks:
                  - TASK-PRIMARY-TDD-REV
                verification_summary: Required verification command passed.
                remaining_risks: []
                merge_ready: true
        - match:
            node_path: superpowers/finish_work/finish_work/superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs: *gate_ok
    assertions:
      - type: output_equals
        path: route
        value: execute_plan
      - type: output_equals
        path: workflow_status
        value: merge_ready
      - type: output_equals
        path: selected_task_id
        value: TASK-PRIMARY-TDD-REV
      - type: output_equals
        path: child_job_required
        value: false
      - type: output_equals
        path: revision_attempted
        value: true
      - type: output_equals
        path: revision_session_id
        value: sid-primary-tdd-revision-spec
      - type: output_equals
        path: implementer_session_id
        value: sid-primary-tdd-revision-spec
      - type: output_equals
        path: spec_reviewer_session_id
        value: sid-primary-tdd-spec-after-revision
      - type: output_equals
        path: quality_reviewer_session_id
        value: sid-primary-tdd-quality-after-revision
      - type: output_equals
        path: task_done
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
        path: verification_ok
        value: true
      - type: output_equals
        path: finish_decision
        value: merge_ready
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
```

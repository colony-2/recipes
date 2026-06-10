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
            node_path: superpowers/brainstorm_design/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
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
            node_path: superpowers/write_plan/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
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
            node_path: superpowers/review_plan/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
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
            node_path: superpowers/run_task_boundary/sequence/implement_task
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
            node_path: superpowers/run_task_boundary/sequence/spec_review
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
            node_path: superpowers/run_task_boundary/sequence/quality_review
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
            node_path: superpowers/run_task_boundary/sequence/task_gate
          behavior:
            mode: return
            outputs: &gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: gate passed
              results: {}
        - match:
            node_path: superpowers/verify_work/sequence/summarize_verification
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
            node_path: superpowers/verify_work/sequence/verification_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/finish_work/sequence/write_finish_summary
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
            node_path: superpowers/finish_work/sequence/finish_gate
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
        node_path: superpowers/run_task_boundary/sequence/implement_task
      - type: node_executed
        node_path: superpowers/verify_work/sequence/run_verification_commands

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
            node_path: superpowers/brainstorm_design/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
          behavior:
            mode: return
            outputs: *brainstorm_ok
        - match:
            node_path: superpowers/write_plan/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
          behavior:
            mode: return
            outputs: *plan_ready
        - match:
            node_path: superpowers/review_plan/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
          behavior:
            mode: return
            outputs: *plan_review_ok
        - match:
            node_path: superpowers/run_task_boundary/sequence/implement_task
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: superpowers/run_task_boundary/sequence/spec_review
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: superpowers/run_task_boundary/sequence/quality_review
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: superpowers/run_task_boundary/sequence/task_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/verify_work/sequence/summarize_verification
          behavior:
            mode: return
            outputs: *verify_ok
        - match:
            node_path: superpowers/verify_work/sequence/verification_gate
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: superpowers/finish_work/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *brainstorm_ok
              sessionId: sid-finish-primary-2
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
            node_path: superpowers/finish_work/sequence/finish_gate
          behavior:
            mode: return
            outputs: *gate_ok
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
        node_path: superpowers/run_task_boundary/sequence/implement_task
```

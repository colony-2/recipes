# superpowers primary orchestrator test suite

```yaml
recipe: ../superpowers.yaml
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "0409713106774b7bb521dd23f79f68cbf60f03de8c08715b3c84192755bce2e8", "artifact": {"jobId": "sid-brainstorm-primary", "taskOrdinal": 2, "name": "__c2j_objects__/0409713106774b7bb521dd23f79f68cbf60f03de8c08715b3c84192755bce2e8.tar", "sizeBytes": 100}}
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "00222beaba3703dda0508f8e8d709e6fa0b502d42b0ea4c6878079e63779cea6", "artifact": {"jobId": "sid-write-plan-primary", "taskOrdinal": 3, "name": "__c2j_objects__/00222beaba3703dda0508f8e8d709e6fa0b502d42b0ea4c6878079e63779cea6.tar", "sizeBytes": 100}}
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "52d5b93b624b5824a0a9bce2fe13c0b45014c46eb25406fe0b5d41d70f8a8f03", "artifact": {"jobId": "sid-plan-review-primary", "taskOrdinal": 4, "name": "__c2j_objects__/52d5b93b624b5824a0a9bce2fe13c0b45014c46eb25406fe0b5d41d70f8a8f03.tar", "sizeBytes": 100}}
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
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &implement_done
              <<: *brainstorm_ok
              sessionId: sid-implement-primary
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "7995c243119f6a6e50d1e7898ae70ce3b6a5ff13abc9918db7f753fdf8648985", "artifact": {"jobId": "sid-implement-primary", "taskOrdinal": 5, "name": "__c2j_objects__/7995c243119f6a6e50d1e7898ae70ce3b6a5ff13abc9918db7f753fdf8648985.tar", "sizeBytes": 100}}
              skill: c2-superpowers-task-implementer
              raw_output: '{"task_id":"TASK-1","status":"done","summary":"Implemented TASK-1.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-1
                status: done
                summary: Implemented TASK-1.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &spec_ok
              <<: *brainstorm_ok
              sessionId: sid-spec-primary
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "f47bbef7b78f73897da72cef47314636425d3c5a6c72c89d77fb73123e077ac3", "artifact": {"jobId": "sid-spec-primary", "taskOrdinal": 6, "name": "__c2j_objects__/f47bbef7b78f73897da72cef47314636425d3c5a6c72c89d77fb73123e077ac3.tar", "sizeBytes": 100}}
              skill: c2-superpowers-spec-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Spec matches.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Spec matches.
                requires_revision: false
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/quality_review/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-quality-primary
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "fb0443f417002cd96d4525ab2f52b25581273b0e3c56f0b00eb32bdc20be46d0", "artifact": {"jobId": "sid-quality-primary", "taskOrdinal": 7, "name": "__c2j_objects__/fb0443f417002cd96d4525ab2f52b25581273b0e3c56f0b00eb32bdc20be46d0.tar", "sizeBytes": 100}}
              skill: c2-superpowers-quality-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Quality acceptable.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Quality acceptable.
                requires_revision: false
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/task_gate/nix:github:colony-2/c2ops/main#rule_gate"
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "36078810f1871367c6cb267905bc4410883b504e7883d9279c0d243088240164", "artifact": {"jobId": "sid-verify-primary", "taskOrdinal": 8, "name": "__c2j_objects__/36078810f1871367c6cb267905bc4410883b504e7883d9279c0d243088240164.tar", "sizeBytes": 100}}
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "fb0445d767b7e220cee00ed7e07ee77f89d25c545344d3118ef4bdca08c0fa72", "artifact": {"jobId": "sid-finish-primary", "taskOrdinal": 9, "name": "__c2j_objects__/fb0445d767b7e220cee00ed7e07ee77f89d25c545344d3118ef4bdca08c0fa72.tar", "sizeBytes": 100}}
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
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/nix:github:colony-2/c2ops/main#skill-run"
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
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/nix:github:colony-2/c2ops/main#skill-run"

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
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *implement_done
              sessionId: sid-implement-primary-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "b305f96d7604ec062718011cea01552e524945ee76ac4ef48e36b4e647e91ce0", "artifact": {"jobId": "sid-implement-primary-revision", "taskOrdinal": 10, "name": "__c2j_objects__/b305f96d7604ec062718011cea01552e524945ee76ac4ef48e36b4e647e91ce0.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-spec-primary-needs-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "1f47accfb8a742f0102282fdc946e6a5edbb5422dde973cd5ee3e8c178fe1d6c", "artifact": {"jobId": "sid-spec-primary-needs-revision", "taskOrdinal": 11, "name": "__c2j_objects__/1f47accfb8a742f0102282fdc946e6a5edbb5422dde973cd5ee3e8c178fe1d6c.tar", "sizeBytes": 100}}
              raw_output: '{"ok":false,"blocking_issues":["Missing required acceptance behavior."],"feedback":"Add the required behavior.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Missing required acceptance behavior.
                feedback: Add the required behavior.
                requires_revision: true
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &revision_done
              <<: *implement_done
              sessionId: sid-primary-spec-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "f7ec03977ea45d36287d5e8245092354307a5721423fc7807c0e8603d784a787", "artifact": {"jobId": "sid-primary-spec-revision", "taskOrdinal": 12, "name": "__c2j_objects__/f7ec03977ea45d36287d5e8245092354307a5721423fc7807c0e8603d784a787.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-REV","status":"done","summary":"Revised TASK-PRIMARY-REV.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-PRIMARY-REV
                status: done
                summary: Revised TASK-PRIMARY-REV.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-spec-after-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "6fd8e740ebeb4d910403d5f49e5f29537f050703bfc79c6f3d20311643bf59b1", "artifact": {"jobId": "sid-primary-spec-after-revision", "taskOrdinal": 13, "name": "__c2j_objects__/6fd8e740ebeb4d910403d5f49e5f29537f050703bfc79c6f3d20311643bf59b1.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-quality-after-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "24044bfa59321fa18d8253e964b8e170dd82a2495fd1ba7d58c382108a8f5e13", "artifact": {"jobId": "sid-primary-quality-after-revision", "taskOrdinal": 14, "name": "__c2j_objects__/24044bfa59321fa18d8253e964b8e170dd82a2495fd1ba7d58c382108a8f5e13.tar", "sizeBytes": 100}}
              skill: c2-superpowers-quality-reviewer
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/nix:github:colony-2/c2ops/main#rule_gate"
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "d9714c3107a1c86c0dd87f88afb216e2aa843b87cd51ce8ea1e41cfe0f8f8bf5", "artifact": {"jobId": "sid-finish-primary-revision", "taskOrdinal": 15, "name": "__c2j_objects__/d9714c3107a1c86c0dd87f88afb216e2aa843b87cd51ce8ea1e41cfe0f8f8bf5.tar", "sizeBytes": 100}}
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
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/quality_review/nix:github:colony-2/c2ops/main#skill-run"

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
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &primary_tdd_red
              <<: *implement_done
              sessionId: sid-primary-tdd-red
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "d87fa292beb946b66910946a4c7c7fad0fa2ba15d95aa8f90d22f2682088e7f3", "artifact": {"jobId": "sid-primary-tdd-red", "taskOrdinal": 16, "name": "__c2j_objects__/d87fa292beb946b66910946a4c7c7fad0fa2ba15d95aa8f90d22f2682088e7f3.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD","status":"red_written","summary":"RED test written.","red_command":"printf expected failure && exit 7"}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD
                status: red_written
                summary: RED test written.
                red_command: printf expected failure && exit 7
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_red/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &primary_tdd_green
              <<: *implement_done
              sessionId: sid-primary-tdd-green
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "96dd1320830ef16ece6ce9a6cba3d48327d76593e49894fe29fefe94f8eedc20", "artifact": {"jobId": "sid-primary-tdd-green", "taskOrdinal": 17, "name": "__c2j_objects__/96dd1320830ef16ece6ce9a6cba3d48327d76593e49894fe29fefe94f8eedc20.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD","status":"done","summary":"GREEN implementation completed.","validation_commands_run":["printf green"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD
                status: done
                summary: GREEN implementation completed.
                validation_commands_run:
                  - printf green
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_green/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *primary_tdd_green
              sessionId: sid-primary-tdd-refactor
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "23d30a57b5e79e3425aee49f951c7fc2133d19b0597a35aedbfab0363a32a9a8", "artifact": {"jobId": "sid-primary-tdd-refactor", "taskOrdinal": 18, "name": "__c2j_objects__/23d30a57b5e79e3425aee49f951c7fc2133d19b0597a35aedbfab0363a32a9a8.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD","status":"done","summary":"Refactor kept behavior green.","validation_commands_run":["printf refactor"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD
                status: done
                summary: Refactor kept behavior green.
                validation_commands_run:
                  - printf refactor
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-spec
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "32d3c150c8d67633a5a8740714c8c429c5d180dc650b6890b58760c06ca31b7c", "artifact": {"jobId": "sid-primary-tdd-spec", "taskOrdinal": 19, "name": "__c2j_objects__/32d3c150c8d67633a5a8740714c8c429c5d180dc650b6890b58760c06ca31b7c.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-quality
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "e4b9a26a95f7f59a40d49c500cb9c05ebb75c608c3975deac9fe4cf5d6d7bd4c", "artifact": {"jobId": "sid-primary-tdd-quality", "taskOrdinal": 20, "name": "__c2j_objects__/e4b9a26a95f7f59a40d49c500cb9c05ebb75c608c3975deac9fe4cf5d6d7bd4c.tar", "sizeBytes": 100}}
              skill: c2-superpowers-quality-reviewer
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/nix:github:colony-2/c2ops/main#rule_gate"
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "c98535cbe619d335279712d52843be2364638400028c384c05203765640c7b7a", "artifact": {"jobId": "sid-primary-tdd-finish", "taskOrdinal": 21, "name": "__c2j_objects__/c98535cbe619d335279712d52843be2364638400028c384c05203765640c7b7a.tar", "sizeBytes": 100}}
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
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/nix:github:colony-2/c2ops/main#skill-run"

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
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &primary_tdd_revision_red
              <<: *implement_done
              sessionId: sid-primary-tdd-rev-red
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "8238295ac74cc446bfeabadaada9235bdd9e20611c44a03c3f2b83b34b46ff97", "artifact": {"jobId": "sid-primary-tdd-rev-red", "taskOrdinal": 22, "name": "__c2j_objects__/8238295ac74cc446bfeabadaada9235bdd9e20611c44a03c3f2b83b34b46ff97.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"red_written","summary":"RED test written.","red_command":"printf expected failure && exit 7"}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: red_written
                summary: RED test written.
                red_command: printf expected failure && exit 7
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_red/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &primary_tdd_revision_green
              <<: *implement_done
              sessionId: sid-primary-tdd-rev-green
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "50adc0b48c9caf2adfb2c0979459c2f6348d842713986289b7a7bf7675b78d5f", "artifact": {"jobId": "sid-primary-tdd-rev-green", "taskOrdinal": 23, "name": "__c2j_objects__/50adc0b48c9caf2adfb2c0979459c2f6348d842713986289b7a7bf7675b78d5f.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"done","summary":"GREEN implementation completed.","validation_commands_run":["printf green"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: done
                summary: GREEN implementation completed.
                validation_commands_run:
                  - printf green
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_green/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *primary_tdd_revision_green
              sessionId: sid-primary-tdd-rev-refactor
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "a5d0a4af3d4831de1809847cfe4b474f5b1abfbd7bc02f2931971629b9bda123", "artifact": {"jobId": "sid-primary-tdd-rev-refactor", "taskOrdinal": 24, "name": "__c2j_objects__/a5d0a4af3d4831de1809847cfe4b474f5b1abfbd7bc02f2931971629b9bda123.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"done","summary":"Refactor kept behavior green.","validation_commands_run":["printf refactor"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: done
                summary: Refactor kept behavior green.
                validation_commands_run:
                  - printf refactor
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-spec-needs-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "9042316dda8bccf161ff17b98f16cf131ea17b5cfde1a78ab7cc736ba3838502", "artifact": {"jobId": "sid-primary-tdd-spec-needs-revision", "taskOrdinal": 25, "name": "__c2j_objects__/9042316dda8bccf161ff17b98f16cf131ea17b5cfde1a78ab7cc736ba3838502.tar", "sizeBytes": 100}}
              raw_output: '{"ok":false,"blocking_issues":["Missing required TDD acceptance behavior."],"feedback":"Add the required behavior before finishing.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Missing required TDD acceptance behavior.
                feedback: Add the required behavior before finishing.
                requires_revision: true
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs: &primary_tdd_revision_done
              <<: *implement_done
              sessionId: sid-primary-tdd-revision-spec
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "8b8c72df181bd8aa20ad33ff843107598e0ae51a883fb116175c40e020feead3", "artifact": {"jobId": "sid-primary-tdd-revision-spec", "taskOrdinal": 26, "name": "__c2j_objects__/8b8c72df181bd8aa20ad33ff843107598e0ae51a883fb116175c40e020feead3.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-PRIMARY-TDD-REV","status":"done","summary":"Revised TDD task after spec review.","validation_commands_run":["printf green","printf refactor"]}'
              parsed_output:
                task_id: TASK-PRIMARY-TDD-REV
                status: done
                summary: Revised TDD task after spec review.
                validation_commands_run:
                  - printf green
                  - printf refactor
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/nix:github:colony-2/c2ops/main#rule_gate"
          behavior:
            mode: return
            outputs: *gate_ok
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-spec-after-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "6044d101de362e59e28fc4d50c6f53df594009b986ff422b1dfbca7ff5db205c", "artifact": {"jobId": "sid-primary-tdd-spec-after-revision", "taskOrdinal": 27, "name": "__c2j_objects__/6044d101de362e59e28fc4d50c6f53df594009b986ff422b1dfbca7ff5db205c.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-primary-tdd-quality-after-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "79d7ae1fb58b387c84e93886366ee7616630ebe14c48b176b8860f5c1ca72d66", "artifact": {"jobId": "sid-primary-tdd-quality-after-revision", "taskOrdinal": 28, "name": "__c2j_objects__/79d7ae1fb58b387c84e93886366ee7616630ebe14c48b176b8860f5c1ca72d66.tar", "sizeBytes": 100}}
              skill: c2-superpowers-quality-reviewer
        - match:
            node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/nix:github:colony-2/c2ops/main#rule_gate"
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "28688dbb968f347cd03e8939d2a3c96bedf97a5911b4955671ab393595285dfc", "artifact": {"jobId": "sid-primary-tdd-revision-finish", "taskOrdinal": 29, "name": "__c2j_objects__/28688dbb968f347cd03e8939d2a3c96bedf97a5911b4955671ab393595285dfc.tar", "sizeBytes": 100}}
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
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/nix:github:colony-2/c2ops/main#rule_gate"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_quality/nix:github:colony-2/c2ops/main#skill-run"
      - type: node_not_executed
        node_path: "superpowers/execute_plan/execute_plan/superpowers-execute-plan/run_task_boundary/state_machine/implement_task/nix:github:colony-2/c2ops/main#skill-run"
```

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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &implement_done
              status: completed
              sessionId: sid-implement-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "0ad0d43e0d110a52ddf503fd81df777bfa071c1d09fdac2f54aabaf49df47a83", "artifact": {"jobId": "sid-implement-1", "taskOrdinal": 2, "name": "__c2j_objects__/0ad0d43e0d110a52ddf503fd81df777bfa071c1d09fdac2f54aabaf49df47a83.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &spec_ok
              <<: *implement_done
              sessionId: sid-spec-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "2c57d37cad1bace31ec89b8f7f24405b883566fcb94c9e7443e3286bab979847", "artifact": {"jobId": "sid-spec-1", "taskOrdinal": 3, "name": "__c2j_objects__/2c57d37cad1bace31ec89b8f7f24405b883566fcb94c9e7443e3286bab979847.tar", "sizeBytes": 100}}
              skill: c2-superpowers-spec-reviewer
              raw_output: '{"ok":true,"blocking_issues":[],"feedback":"Spec matches.","requires_revision":false}'
              parsed_output:
                ok: true
                blocking_issues: []
                feedback: Spec matches.
                requires_revision: false
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &quality_ok
              <<: *implement_done
              sessionId: sid-quality-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "4d29cd312b9b84107eb93af521f712516b0c1b1c9611901a98f5a70647db6028", "artifact": {"jobId": "sid-quality-1", "taskOrdinal": 4, "name": "__c2j_objects__/4d29cd312b9b84107eb93af521f712516b0c1b1c9611901a98f5a70647db6028.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &revision_done
              <<: *implement_done
              sessionId: sid-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "679dbcff3354b0ffee09f88ec7c99a6ed7dedea600155b61aa3cff100f39dae9", "artifact": {"jobId": "sid-revision-1", "taskOrdinal": 5, "name": "__c2j_objects__/679dbcff3354b0ffee09f88ec7c99a6ed7dedea600155b61aa3cff100f39dae9.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-1","status":"done","summary":"Revised TASK-1.","validation_commands_run":["go test ./..."]}'
              parsed_output:
                task_id: TASK-1
                status: done
                summary: Revised TASK-1.
                validation_commands_run:
                  - go test ./...
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *revision_done
              sessionId: sid-revision-quality-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "ea2b04a2e8f28eae286018a33b91f85b64a8daa143261148f43b7806fd99e98f", "artifact": {"jobId": "sid-revision-quality-1", "taskOrdinal": 6, "name": "__c2j_objects__/ea2b04a2e8f28eae286018a33b91f85b64a8daa143261148f43b7806fd99e98f.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &spec_ok_after_revision
              <<: *spec_ok
              sessionId: sid-spec-after-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "5f6c2a9d7aa096d4fe7b2a28a1169f08eb472ec7cd37b3d9d26d456ec3a2b616", "artifact": {"jobId": "sid-spec-after-revision-1", "taskOrdinal": 7, "name": "__c2j_objects__/5f6c2a9d7aa096d4fe7b2a28a1169f08eb472ec7cd37b3d9d26d456ec3a2b616.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &quality_ok_after_revision
              <<: *quality_ok
              sessionId: sid-quality-after-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "ceecd3c6b890db16509c4b1f2ddd8741fd79859c4d2334ff4903c76838aa8828", "artifact": {"jobId": "sid-quality-after-revision-1", "taskOrdinal": 8, "name": "__c2j_objects__/ceecd3c6b890db16509c4b1f2ddd8741fd79859c4d2334ff4903c76838aa8828.tar", "sizeBytes": 100}}
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *spec_ok_after_revision
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"

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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &red_written
              <<: *implement_done
              sessionId: sid-red-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "4c4a9c5d9491f725b589e123d37dc00cda7eef019b1ac27f5cab1ca7e18697e9", "artifact": {"jobId": "sid-red-1", "taskOrdinal": 9, "name": "__c2j_objects__/4c4a9c5d9491f725b589e123d37dc00cda7eef019b1ac27f5cab1ca7e18697e9.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &green_done
              <<: *implement_done
              sessionId: sid-green-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "3f0591a6bba6f5e0c7091a9a872abd4efc2629f21db5ecb8feb17bb0db251c1e", "artifact": {"jobId": "sid-green-1", "taskOrdinal": 10, "name": "__c2j_objects__/3f0591a6bba6f5e0c7091a9a872abd4efc2629f21db5ecb8feb17bb0db251c1e.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &refactor_done
              <<: *green_done
              sessionId: sid-refactor-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "39ea3088de6f35eba1e5abca5859f06add8c9a7bd683b5c74863547adcf79c2d", "artifact": {"jobId": "sid-refactor-1", "taskOrdinal": 11, "name": "__c2j_objects__/39ea3088de6f35eba1e5abca5859f06add8c9a7bd683b5c74863547adcf79c2d.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-tdd-spec-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "50dc8fce5b92db0584c630c742cc27f90d0005401497bc3de04d2d98137c655b", "artifact": {"jobId": "sid-tdd-spec-1", "taskOrdinal": 12, "name": "__c2j_objects__/50dc8fce5b92db0584c630c742cc27f90d0005401497bc3de04d2d98137c655b.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok
              sessionId: sid-tdd-quality-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "58b1f8a2af247352b696cd79ec67930a70fb8f534271d5cb6bed5478667b5b82", "artifact": {"jobId": "sid-tdd-quality-1", "taskOrdinal": 13, "name": "__c2j_objects__/58b1f8a2af247352b696cd79ec67930a70fb8f534271d5cb6bed5478667b5b82.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *spec_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *spec_ok_after_revision
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
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
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"

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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *implement_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &spec_needs_revision
              <<: *spec_ok
              sessionId: sid-spec-needs-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "35cdc485f620294ed66f9fe9d151ad1eea9253700f884c7d10ccc778346f5097", "artifact": {"jobId": "sid-spec-needs-revision-1", "taskOrdinal": 14, "name": "__c2j_objects__/35cdc485f620294ed66f9fe9d151ad1eea9253700f884c7d10ccc778346f5097.tar", "sizeBytes": 100}}
              raw_output: '{"ok":false,"blocking_issues":["Missing required acceptance behavior."],"feedback":"Add the required behavior.","requires_revision":true}'
              parsed_output:
                ok: false
                blocking_issues:
                  - Missing required acceptance behavior.
                feedback: Add the required behavior.
                requires_revision: true
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *task_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *revision_done
              sessionId: sid-revision-spec-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "125d6b3a5c918a2368e7d1f13ac5da9154d9bcd1cc1af236bd66751cfc2e1d1b", "artifact": {"jobId": "sid-revision-spec-2", "taskOrdinal": 15, "name": "__c2j_objects__/125d6b3a5c918a2368e7d1f13ac5da9154d9bcd1cc1af236bd66751cfc2e1d1b.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok_after_revision
              sessionId: sid-spec-after-revision-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "0edad8389b549407ee6e54117c536b429b0d964b24db5ece7e346301f2cbb72b", "artifact": {"jobId": "sid-spec-after-revision-2", "taskOrdinal": 16, "name": "__c2j_objects__/0edad8389b549407ee6e54117c536b429b0d964b24db5ece7e346301f2cbb72b.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok_after_revision
              sessionId: sid-quality-after-revision-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "1ffbc58a1f3bb7bacbaf3894b85342db70ab6f5332ad37d780e13559eb37f87f", "artifact": {"jobId": "sid-quality-after-revision-2", "taskOrdinal": 17, "name": "__c2j_objects__/1ffbc58a1f3bb7bacbaf3894b85342db70ab6f5332ad37d780e13559eb37f87f.tar", "sizeBytes": 100}}
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"

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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *implement_done
              sessionId: sid-implement-quality-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "7593081c5ea36d539cf63c5dc244ef6f08fb5628f762628891c7f50db7e1faa7", "artifact": {"jobId": "sid-implement-quality-1", "taskOrdinal": 18, "name": "__c2j_objects__/7593081c5ea36d539cf63c5dc244ef6f08fb5628f762628891c7f50db7e1faa7.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-QUALITY","status":"done","summary":"Implemented TASK-QUALITY.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-QUALITY
                status: done
                summary: Implemented TASK-QUALITY.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok
              sessionId: sid-spec-quality-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "4cf97afd41dd1b085b1826b00acfd19ae90d82e9c3b886df8579a801ab9a6ccd", "artifact": {"jobId": "sid-spec-quality-1", "taskOrdinal": 19, "name": "__c2j_objects__/4cf97afd41dd1b085b1826b00acfd19ae90d82e9c3b886df8579a801ab9a6ccd.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok
              sessionId: sid-quality-needs-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "9b90a025951c452976fc2da0b80f257139b7e2e58605ac056c80bb9e84b2415f", "artifact": {"jobId": "sid-quality-needs-revision-1", "taskOrdinal": 20, "name": "__c2j_objects__/9b90a025951c452976fc2da0b80f257139b7e2e58605ac056c80bb9e84b2415f.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *revision_done
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *revision_done
              sessionId: sid-revision-quality-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "26924c3a08725740d4b0ef3d033f333534e2a30aab2f5bd8b5b97e77bd0f8d3c", "artifact": {"jobId": "sid-revision-quality-2", "taskOrdinal": 21, "name": "__c2j_objects__/26924c3a08725740d4b0ef3d033f333534e2a30aab2f5bd8b5b97e77bd0f8d3c.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-QUALITY","status":"done","summary":"Revised TASK-QUALITY.","validation_commands_run":["printf verified"]}'
              parsed_output:
                task_id: TASK-QUALITY
                status: done
                summary: Revised TASK-QUALITY.
                validation_commands_run:
                  - printf verified
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok_after_revision
              sessionId: sid-spec-after-quality-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "884bbaef8f9d5a9eb57429e9a7d226288225e36eb2083bd7d2abe43161a28453", "artifact": {"jobId": "sid-spec-after-quality-revision-1", "taskOrdinal": 22, "name": "__c2j_objects__/884bbaef8f9d5a9eb57429e9a7d226288225e36eb2083bd7d2abe43161a28453.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok_after_revision
              sessionId: sid-quality-after-quality-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "126839fe77249f0ed9b6c98d3cce9b08cba7a8e68842876b02d5a37a3eecd086", "artifact": {"jobId": "sid-quality-after-quality-revision-1", "taskOrdinal": 23, "name": "__c2j_objects__/126839fe77249f0ed9b6c98d3cce9b08cba7a8e68842876b02d5a37a3eecd086.tar", "sizeBytes": 100}}
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
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/revise_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"

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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_red_test/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *red_written
              sessionId: sid-tdd-rev-red
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "8623d7366bffea0972521a746917a906af2e292f5579d11017adbcffe8c64c2f", "artifact": {"jobId": "sid-tdd-rev-red", "taskOrdinal": 24, "name": "__c2j_objects__/8623d7366bffea0972521a746917a906af2e292f5579d11017adbcffe8c64c2f.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/write_green_code/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *green_done
              sessionId: sid-tdd-rev-green
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "b92d3c92938a60902648319b9eea6bf00252bbfb5aede21e65e51f2416211635", "artifact": {"jobId": "sid-tdd-rev-green", "taskOrdinal": 25, "name": "__c2j_objects__/b92d3c92938a60902648319b9eea6bf00252bbfb5aede21e65e51f2416211635.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/refactor_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *refactor_done
              sessionId: sid-tdd-rev-refactor
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "6f5b6d199c466bbf5971127fbfc5c1549805374fe533335b20e6d10d5068ef80", "artifact": {"jobId": "sid-tdd-rev-refactor", "taskOrdinal": 26, "name": "__c2j_objects__/6f5b6d199c466bbf5971127fbfc5c1549805374fe533335b20e6d10d5068ef80.tar", "sizeBytes": 100}}
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *spec_needs_revision
              sessionId: sid-tdd-spec-needs-revision
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "f1d6e3d592d8534f7cd1cd0992351a0df75b8c40a3f3a9507d7473375fb0d7e9", "artifact": {"jobId": "sid-tdd-spec-needs-revision", "taskOrdinal": 27, "name": "__c2j_objects__/f1d6e3d592d8534f7cd1cd0992351a0df75b8c40a3f3a9507d7473375fb0d7e9.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *quality_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs: *tdd_gate_ok
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &tdd_revision_done
              <<: *refactor_done
              sessionId: sid-tdd-revision-spec-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "bea0063537872c7a998c12dfecf3359782358b64262fa4e6eb84773d276a7a60", "artifact": {"jobId": "sid-tdd-revision-spec-1", "taskOrdinal": 28, "name": "__c2j_objects__/bea0063537872c7a998c12dfecf3359782358b64262fa4e6eb84773d276a7a60.tar", "sizeBytes": 100}}
              raw_output: '{"task_id":"TASK-TDD-REV","status":"done","summary":"Revised TDD task after spec review.","validation_commands_run":["printf green","printf refactor"]}'
              parsed_output:
                task_id: TASK-TDD-REV
                status: done
                summary: Revised TDD task after spec review.
                validation_commands_run:
                  - printf green
                  - printf refactor
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
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
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *spec_ok_after_revision
              sessionId: sid-tdd-spec-after-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "cc54e0a05c186a726211ad72c4650662bbe318e5771377d95c50a23d0b7e5349", "artifact": {"jobId": "sid-tdd-spec-after-revision-1", "taskOrdinal": 29, "name": "__c2j_objects__/cc54e0a05c186a726211ad72c4650662bbe318e5771377d95c50a23d0b7e5349.tar", "sizeBytes": 100}}
        - match:
            node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *quality_ok_after_revision
              sessionId: sid-tdd-quality-after-revision-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "6ab4773f59c67afd7c8d494993a9d34bdd4c45aef8c7fd8417bece1e90c1771a", "artifact": {"jobId": "sid-tdd-quality-after-revision-1", "taskOrdinal": 30, "name": "__c2j_objects__/6ab4773f59c67afd7c8d494993a9d34bdd4c45aef8c7fd8417bece1e90c1771a.tar", "sizeBytes": 100}}
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
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_spec/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_green/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/assert_revision_refactor/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/spec_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review_after_revision/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate_after_revision/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/quality_review/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/task_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_tdd_task_boundary/state_machine/revise_tdd_after_quality/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
      - type: node_not_executed
        node_path: "superpowers-execute-plan/run_task_boundary/state_machine/implement_task/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
```

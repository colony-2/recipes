# superpowers-adaptive-task-loop-smoke test suite

```yaml
recipe: superpowers-adaptive-task-loop-smoke.yaml
cases:
  - id: ts-055-adaptive-task-loop-updates-plan-before-next-task
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
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: "superpowers-adaptive-task-loop-smoke/task_a_implementer/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-a-implementer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "9f060f838c4ea0182aaf968ee42ec768774cfc820044aee63ef754a8fa5f522d", "artifact": {"jobId": "sid-task-a-implementer", "taskOrdinal": 2, "name": "__c2j_objects__/9f060f838c4ea0182aaf968ee42ec768774cfc820044aee63ef754a8fa5f522d.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 passed; parser now normalizes empty input.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-a-implementer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "29d5b773273e5dcfb6e73c68a022b3aab2d33e42860a9932909390cddf1e0a2f", "artifact": {"jobId": "sid-task-a-implementer", "taskOrdinal": 3, "name": "__c2j_objects__/29d5b773273e5dcfb6e73c68a022b3aab2d33e42860a9932909390cddf1e0a2f.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 passed; parser now normalizes empty input.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-adaptive-task-loop-smoke/task_a_spec_review/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-a-spec
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "01ee2934cc1878e499f8e42347cebf694a8336d3e1035d4bc1fb6ec2b2ee80ff", "artifact": {"jobId": "sid-task-a-spec", "taskOrdinal": 4, "name": "__c2j_objects__/01ee2934cc1878e499f8e42347cebf694a8336d3e1035d4bc1fb6ec2b2ee80ff.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 satisfies the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-a-spec
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "c2c3e912e8ed939403006b5c811f5ab5aa7b4ef38e8b391d297f34f547564de8", "artifact": {"jobId": "sid-task-a-spec", "taskOrdinal": 5, "name": "__c2j_objects__/c2c3e912e8ed939403006b5c811f5ab5aa7b4ef38e8b391d297f34f547564de8.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 satisfies the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-adaptive-task-loop-smoke/planner_update/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-planner
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "21bb5f2b54f072f94d91510e60bc1024ad5d43c822b1a490a01435bcb2f6da0d", "artifact": {"jobId": "sid-planner", "taskOrdinal": 6, "name": "__c2j_objects__/21bb5f2b54f072f94d91510e60bc1024ad5d43c822b1a490a01435bcb2f6da0d.tar", "sizeBytes": 100}}
              assistantSummary: |
                {
                  "plan_id": "superpowers-adaptive-loop-smoke",
                  "tasks": [
                    {
                      "id": "TASK-1",
                      "title": "Add parser coverage",
                      "status": "done",
                      "dependencies": [],
                      "requires_child_job": false,
                      "target_ref": "main",
                      "prompt_delta": "Completed."
                    },
                    {
                      "id": "TASK-2",
                      "title": "Wire parser caller",
                      "status": "pending",
                      "dependencies": [],
                      "requires_child_job": false,
                      "target_ref": "main",
                      "prompt_delta": "Account for TASK-1 parser behavior."
                    }
                  ]
                }
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-planner
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "05529d5d908329292579edfb4a6074015d3c914ff44a2fca56da91449dc72f41", "artifact": {"jobId": "sid-planner", "taskOrdinal": 7, "name": "__c2j_objects__/05529d5d908329292579edfb4a6074015d3c914ff44a2fca56da91449dc72f41.tar", "sizeBytes": 100}}
              assistantSummary: |
                {
                  "plan_id": "superpowers-adaptive-loop-smoke",
                  "tasks": [
                    {
                      "id": "TASK-1",
                      "title": "Add parser coverage",
                      "status": "done",
                      "dependencies": [],
                      "requires_child_job": false,
                      "target_ref": "main",
                      "prompt_delta": "Completed."
                    },
                    {
                      "id": "TASK-2",
                      "title": "Wire parser caller",
                      "status": "pending",
                      "dependencies": [],
                      "requires_child_job": false,
                      "target_ref": "main",
                      "prompt_delta": "Account for TASK-1 parser behavior."
                    }
                  ]
                }
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-adaptive-task-loop-smoke/task_b_boundary/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-b-implementer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "7a9b8052f4603fdfa7620c8b612c854d562c891d1561dc75aff8bb995a538777", "artifact": {"jobId": "sid-task-b-implementer", "taskOrdinal": 8, "name": "__c2j_objects__/7a9b8052f4603fdfa7620c8b612c854d562c891d1561dc75aff8bb995a538777.tar", "sizeBytes": 100}}
              assistantSummary: TASK-2 implemented using updated plan guidance.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-b-implementer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "eac0a6d83b537c615e16581232dbd01c8a97f3003d9383e048766e31182abbbf", "artifact": {"jobId": "sid-task-b-implementer", "taskOrdinal": 9, "name": "__c2j_objects__/eac0a6d83b537c615e16581232dbd01c8a97f3003d9383e048766e31182abbbf.tar", "sizeBytes": 100}}
              assistantSummary: TASK-2 implemented using updated plan guidance.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: first_task_id
        value: TASK-1
      - type: output_equals
        path: first_task_passed
        value: true
      - type: output_equals
        path: first_task_implementer_session_id
        value: sid-task-a-implementer
      - type: output_equals
        path: first_task_spec_reviewer_session_id
        value: sid-task-a-spec
      - type: output_equals
        path: planner_session_id
        value: sid-planner
      - type: output_equals
        path: second_task_id
        value: TASK-2
      - type: output_equals
        path: second_task_session_id
        value: sid-task-b-implementer
      - type: output_equals
        path: adaptive_second_task_selected
        value: true
      - type: output_equals
        path: planner_feedback_carried_forward
        value: true
      - type: output_equals
        path: child_job_used
        value: false
```

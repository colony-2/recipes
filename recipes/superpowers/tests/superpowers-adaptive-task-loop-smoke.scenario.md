# superpowers-adaptive-task-loop-smoke test suite

```yaml
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
            node_path: "superpowers-adaptive-task-loop-smoke/task_a_implementer/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-a-implementer
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
              assistantSummary: TASK-1 passed; parser now normalizes empty input.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-adaptive-task-loop-smoke/task_a_spec_review/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-a-spec
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
              assistantSummary: TASK-1 satisfies the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-adaptive-task-loop-smoke/planner_update/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-planner
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
            node_path: "superpowers-adaptive-task-loop-smoke/task_b_boundary/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-task-b-implementer
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

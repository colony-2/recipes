# superpowers-native-task-selection-smoke test suite

```yaml
cases:
  - id: ts-051-native-task-selection-picks-first-ready-task
    type: recipe_case
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: ready_task_count
        value: 1
      - type: output_equals
        path: selected_task_id
        value: TASK-1
      - type: output_equals
        path: selected_task_target_ref
        value: main
      - type: output_equals
        path: selected_task_requires_child_job
        value: false
      - type: output_equals
        path: no_child_job_required
        value: true

  - id: ts-052-native-task-selection-surfaces-required-child-boundary
    type: recipe_case
    inputs:
      plan_json: |
        {
          "plan_id": "child-boundary-required",
          "tasks": [
            {
              "id": "TASK-CELL",
              "title": "Delegate cross-cell update",
              "status": "pending",
              "dependencies": [],
              "target_ref": "main",
              "requires_child_job": true,
              "child_job_reason": "cross-cell work"
            }
          ]
        }
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: ready_task_count
        value: 1
      - type: output_equals
        path: selected_task_id
        value: TASK-CELL
      - type: output_equals
        path: selected_task_requires_child_job
        value: true
      - type: output_equals
        path: no_child_job_required
        value: false
```

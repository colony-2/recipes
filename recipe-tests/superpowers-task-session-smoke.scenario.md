# superpowers-task-session-smoke test suite

```yaml
cases:
  - id: ts-053-same-job-task-boundary-uses-distinct-role-sessions
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
            node_path: "superpowers-task-session-smoke/implementer_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-implementer
              assistantSummary: TASK-1 implemented and validated.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-implementer
              assistantSummary: TASK-1 implemented and validated.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-task-session-smoke/spec_reviewer_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-spec-reviewer
              assistantSummary: TASK-1 matches the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-spec-reviewer
              assistantSummary: TASK-1 matches the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-task-session-smoke/quality_reviewer_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-quality-reviewer
              assistantSummary: TASK-1 quality review passed.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-quality-reviewer
              assistantSummary: TASK-1 quality review passed.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: task_id
        value: TASK-1
      - type: output_equals
        path: task_requires_child_job
        value: false
      - type: output_equals
        path: child_job_used
        value: false
      - type: output_equals
        path: role_sessions_are_distinct
        value: true
      - type: output_equals
        path: task_boundary_passed
        value: true
```

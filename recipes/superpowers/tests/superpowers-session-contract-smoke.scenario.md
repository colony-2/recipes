# superpowers-session-contract-smoke test suite

```yaml
cases:
  - id: ts-054-session-id-controls-isolation-and-resume
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
            node_path: "superpowers-session-contract-smoke/start_isolated_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              assistantSummary: Started isolated role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              assistantSummary: Started isolated role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-session-contract-smoke/resume_same_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              assistantSummary: Resumed the same role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              assistantSummary: Resumed the same role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: isolated_session_requested_without_session_id
        value: true
      - type: output_equals
        path: isolated_session_id
        value: sid-role
      - type: output_equals
        path: resume_requested_session_id
        value: sid-role
      - type: output_equals
        path: resumed_session_id
        value: sid-role
      - type: output_equals
        path: resume_reused_session_id
        value: true
      - type: output_equals
        path: both_steps_completed
        value: true
```

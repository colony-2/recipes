# job-implement test suite

```yaml
cases:
  - id: ts-011-continue-session-path
    type: recipe_case
    inputs:
      prompt: |
        Continue work

        Resume prior coding session
      session_id: sid-existing
      include_prior_summary: false
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: job-implement/prepare_context/command_execution
          behavior:
            mode: return
            outputs:
              stdout: ""
              stderr: ""
              exit_code: 0
              success: true
            artifacts:
              requirements/plan.json: "{}"
              feedback/validation-feedback.md: ""
              feedback/prior-session-summary.md: ""
              feedback/extra-instructions.md: ""
        - match:
            node_path: "job-implement/continue_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-existing
              assistantSummary: Continued implementation session
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: session_id
        value: sid-existing
      - type: output_equals
        path: status
        value: completed

  - id: ts-012-new-session-path
    type: recipe_case
    inputs:
      prompt: |
        Start fresh

        New implementation session
      include_prior_summary: true
      prior_session_summary: Previous run summary
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: job-implement/prepare_context/command_execution
          behavior:
            mode: return
            outputs:
              stdout: ""
              stderr: ""
              exit_code: 0
              success: true
            artifacts:
              requirements/plan.json: "{}"
              feedback/validation-feedback.md: ""
              feedback/prior-session-summary.md: ""
              feedback/extra-instructions.md: ""
        - match:
            node_path: "job-implement/new_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-new
              assistantSummary: Started new session with provided context
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: session_id
        value: sid-new
      - type: output_equals
        path: status
        value: completed

  - id: ts-013-assistant-summary-output
    type: recipe_case
    inputs:
      prompt: |
        Summary output

        Ensure summary output exists
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: job-implement/prepare_context/command_execution
          behavior:
            mode: return
            outputs:
              stdout: ""
              stderr: ""
              exit_code: 0
              success: true
            artifacts:
              requirements/plan.json: "{}"
              feedback/validation-feedback.md: ""
              feedback/prior-session-summary.md: ""
              feedback/extra-instructions.md: ""
        - match:
            node_path: "job-implement/new_session/git+https://github.com/colony-2/c2ops.git//codex@main"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-summary
              assistantSummary: Non-empty summary for reviewer context
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: assistant_summary
        value: Non-empty summary for reviewer context
```

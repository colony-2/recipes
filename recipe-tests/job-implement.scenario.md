# job-implement test suite

```yaml
recipe: ../recipes/jobs/job-implement.yaml
cases:
- id: ts-011-continue-session-path
  type: recipe_case
  inputs:
    prompt: 'Continue work


      Resume prior coding session

      '
    session:
      $c2j_object: v1
      type: c2ops.codex.session/v1
      tenant_id: test
      sha256: 24d762edfea6056e74ee9841aff4c86e81336d6347ad153586af9037460fa73c
      artifact:
        jobId: sid-existing
        taskOrdinal: 1
        name: __c2j_objects__/24d762edfea6056e74ee9841aff4c86e81336d6347ad153586af9037460fa73c.tar
        sizeBytes: 100
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
          stdout: ''
          stderr: ''
          exit_code: 0
          success: true
        artifacts:
          requirements/plan.json: '{}'
          feedback/validation-feedback.md: ''
          feedback/prior-session-summary.md: ''
          feedback/extra-instructions.md: ''
    - match:
        node_path: job-implement/continue_session/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-existing
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 43e7d0dc6efcac5af48fa5c5dcf99348d510448c02cfcc2587c0da212e9e9d08
            artifact:
              jobId: sid-existing
              taskOrdinal: 2
              name: __c2j_objects__/43e7d0dc6efcac5af48fa5c5dcf99348d510448c02cfcc2587c0da212e9e9d08.tar
              sizeBytes: 100
          assistantSummary: Continued implementation session
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
  assertions:
  - type: output_equals
    path: session_id
    value: sid-existing
  - type: output_equals
    path: status
    value: completed
  options:
    validation_mode: path_only
- id: ts-012-new-session-path
  type: recipe_case
  inputs:
    prompt: 'Start fresh


      New implementation session

      '
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
          stdout: ''
          stderr: ''
          exit_code: 0
          success: true
        artifacts:
          requirements/plan.json: '{}'
          feedback/validation-feedback.md: ''
          feedback/prior-session-summary.md: ''
          feedback/extra-instructions.md: ''
    - match:
        node_path: job-implement/new_session/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-new
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 135b6c6310d317b6d14ae26282e905829ccbe62c882e602eb7c828b3c73c9f4e
            artifact:
              jobId: sid-new
              taskOrdinal: 3
              name: __c2j_objects__/135b6c6310d317b6d14ae26282e905829ccbe62c882e602eb7c828b3c73c9f4e.tar
              sizeBytes: 100
          assistantSummary: Started new session with provided context
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
  assertions:
  - type: output_equals
    path: session_id
    value: sid-new
  - type: output_equals
    path: status
    value: completed
  options:
    validation_mode: path_only
- id: ts-013-assistant-summary-output
  type: recipe_case
  inputs:
    prompt: 'Summary output


      Ensure summary output exists

      '
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
          stdout: ''
          stderr: ''
          exit_code: 0
          success: true
        artifacts:
          requirements/plan.json: '{}'
          feedback/validation-feedback.md: ''
          feedback/prior-session-summary.md: ''
          feedback/extra-instructions.md: ''
    - match:
        node_path: job-implement/new_session/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-summary
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: c0cc9aec155d12f863d5d9f37308656b86bc097831e8b6fce97903b3cf4adc3f
            artifact:
              jobId: sid-summary
              taskOrdinal: 4
              name: __c2j_objects__/c0cc9aec155d12f863d5d9f37308656b86bc097831e8b6fce97903b3cf4adc3f.tar
              sizeBytes: 100
          assistantSummary: Non-empty summary for reviewer context
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
  assertions:
  - type: output_equals
    path: assistant_summary
    value: Non-empty summary for reviewer context
  options:
    validation_mode: path_only
```

# superpowers-write-plan test suite

```yaml
cases:
  - id: ts-063-write-plan-produces-ready-task-chain
    type: recipe_case
    inputs:
      prompt: Add an audit-log export feature for admins.
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "Add a scoped export endpoint and background job."
        }
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-write-plan/write_plan
          behavior:
            mode: return
            outputs: &standard_plan
              status: completed
              sessionId: sid-plan-1
              assistantSummary: Plan is ready.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-write-plan
              raw_summary: Plan is ready.
              output_source: artifact
              output_path: superpowers/plan/plan.json
              raw_output: '{"plan_id":"PLAN-1","summary":"Implement audit-log export in two dependent tasks.","tasks":[{"id":"TASK-1","title":"Add export authorization and tests","status":"pending","dependencies":[],"target_ref":"main","requires_child_job":false,"child_job_reason":"","instructions":"Add authorization checks and coverage for admin-only export.","validation_commands":["go test ./..."],"review_requirements":["spec","quality"]},{"id":"TASK-2","title":"Add background export job","status":"pending","dependencies":["TASK-1"],"target_ref":"main","requires_child_job":false,"child_job_reason":"","instructions":"Implement the export job using the authorized request path.","validation_commands":["go test ./..."],"review_requirements":["spec","quality"]}],"ready_task_ids":["TASK-1"],"validation_strategy":{"commands":["go test ./..."]},"child_job_boundaries":[]}'
              parsed_output:
                plan_id: PLAN-1
                summary: Implement audit-log export in two dependent tasks.
                tasks:
                  - id: TASK-1
                    title: Add export authorization and tests
                    status: pending
                    dependencies: []
                    target_ref: main
                    requires_child_job: false
                    child_job_reason: ""
                    instructions: Add authorization checks and coverage for admin-only export.
                    validation_commands:
                      - go test ./...
                    review_requirements:
                      - spec
                      - quality
                  - id: TASK-2
                    title: Add background export job
                    status: pending
                    dependencies:
                      - TASK-1
                    target_ref: main
                    requires_child_job: false
                    child_job_reason: ""
                    instructions: Implement the export job using the authorized request path.
                    validation_commands:
                      - go test ./...
                    review_requirements:
                      - spec
                      - quality
                ready_task_ids:
                  - TASK-1
                validation_strategy:
                  commands:
                    - go test ./...
                child_job_boundaries: []
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/plan/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Plan is ready.
                  reason: planned
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers-write-plan/plan_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: plan output valid
              results: {}
    assertions:
      - type: output_equals
        path: plan_ok
        value: true
      - type: output_equals
        path: task_count
        value: 2
      - type: output_equals
        path: first_ready_task_id
        value: TASK-1
      - type: output_equals
        path: child_job_boundary_count
        value: 0
      - type: output_equals
        path: output_schema_valid
        value: true

  - id: ts-064-write-plan-surfaces-required-child-boundary
    type: recipe_case
    inputs:
      prompt: Update this cell and a separate reporting cell.
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "Split local and reporting-cell work."
        }
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-write-plan/write_plan
          behavior:
            mode: return
            outputs:
              <<: *standard_plan
              sessionId: sid-plan-2
              raw_output: '{"plan_id":"PLAN-2","summary":"Split cross-cell work at the C2 job boundary.","tasks":[{"id":"TASK-CELL","title":"Delegate reporting-cell update","status":"pending","dependencies":[],"target_ref":"main","requires_child_job":true,"child_job_reason":"cross-cell work","instructions":"Start a child job owned by the reporting cell.","validation_commands":[],"review_requirements":["spec"]}],"ready_task_ids":["TASK-CELL"],"validation_strategy":{"commands":[]},"child_job_boundaries":[{"task_id":"TASK-CELL","reason":"cross-cell work"}]}'
              parsed_output:
                plan_id: PLAN-2
                summary: Split cross-cell work at the C2 job boundary.
                tasks:
                  - id: TASK-CELL
                    title: Delegate reporting-cell update
                    status: pending
                    dependencies: []
                    target_ref: main
                    requires_child_job: true
                    child_job_reason: cross-cell work
                    instructions: Start a child job owned by the reporting cell.
                    validation_commands: []
                    review_requirements:
                      - spec
                ready_task_ids:
                  - TASK-CELL
                validation_strategy:
                  commands: []
                child_job_boundaries:
                  - task_id: TASK-CELL
                    reason: cross-cell work
        - match:
            node_path: superpowers-write-plan/plan_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: plan output valid
              results: {}
    assertions:
      - type: output_equals
        path: plan_ok
        value: true
      - type: output_equals
        path: task_count
        value: 1
      - type: output_equals
        path: first_ready_task_id
        value: TASK-CELL
      - type: output_equals
        path: child_job_boundary_count
        value: 1
```

# superpowers-write-plan test suite

```yaml
recipe: ../superpowers-write-plan.yaml
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "fdb91bae4b31f3982ae0746bf2fb8c1cb3763883195be68426ae31114fb4e5b9", "artifact": {"jobId": "sid-plan-1", "taskOrdinal": 2, "name": "__c2j_objects__/fdb91bae4b31f3982ae0746bf2fb8c1cb3763883195be68426ae31114fb4e5b9.tar", "sizeBytes": 100}}
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
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "f4630877325704a60fc92cb8f9ea97a519b515993c0e60ae1234a4aa3c3df013", "artifact": {"jobId": "sid-plan-2", "taskOrdinal": 3, "name": "__c2j_objects__/f4630877325704a60fc92cb8f9ea97a519b515993c0e60ae1234a4aa3c3df013.tar", "sizeBytes": 100}}
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

  - id: ts-089-write-plan-emits-tdd-task-command-contract
    type: recipe_case
    inputs:
      prompt: Add authorization behavior for audit-log exports.
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "Use TDD for the authorization boundary before export work."
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
              sessionId: sid-plan-3
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "6241a363146aeedc4352238bd5c668302674d2b10a313a05eeafcc0811090198", "artifact": {"jobId": "sid-plan-3", "taskOrdinal": 4, "name": "__c2j_objects__/6241a363146aeedc4352238bd5c668302674d2b10a313a05eeafcc0811090198.tar", "sizeBytes": 100}}
              raw_output: '{"plan_id":"PLAN-3","summary":"Add export authorization with recipe-enforced TDD.","tasks":[{"id":"TASK-TDD-1","title":"Add export authorization behavior","status":"pending","dependencies":[],"target_ref":"main","requires_child_job":false,"requires_tdd":true,"child_job_reason":"","instructions":"Use RED/GREEN/refactor for admin-only export authorization.","validation_commands":["printf green"],"review_requirements":["spec","quality"],"tdd":{"red_command":"printf red && exit 7","red_expected_failure":"authorization test fails before implementation","green_command":"printf green","refactor_verification_command":"printf refactor"}}],"ready_task_ids":["TASK-TDD-1"],"validation_strategy":{"commands":["printf green"]},"child_job_boundaries":[]}'
              parsed_output:
                plan_id: PLAN-3
                summary: Add export authorization with recipe-enforced TDD.
                tasks:
                  - id: TASK-TDD-1
                    title: Add export authorization behavior
                    status: pending
                    dependencies: []
                    target_ref: main
                    requires_child_job: false
                    requires_tdd: true
                    child_job_reason: ""
                    instructions: Use RED/GREEN/refactor for admin-only export authorization.
                    validation_commands:
                      - printf green
                    review_requirements:
                      - spec
                      - quality
                    tdd:
                      red_command: printf red && exit 7
                      red_expected_failure: authorization test fails before implementation
                      green_command: printf green
                      refactor_verification_command: printf refactor
                ready_task_ids:
                  - TASK-TDD-1
                validation_strategy:
                  commands:
                    - printf green
                child_job_boundaries: []
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: plan_ok
        value: true
      - type: output_equals
        path: task_count
        value: 1
      - type: output_equals
        path: first_ready_task_id
        value: TASK-TDD-1
      - type: output_equals
        path: tdd_task_count
        value: 1
      - type: output_equals
        path: first_task_tdd_red_command
        value: printf red && exit 7
      - type: output_equals
        path: first_task_tdd_green_command
        value: printf green
      - type: output_equals
        path: first_task_tdd_refactor_command
        value: printf refactor

  - id: ts-090-write-plan-rejects-missing-child-boundary-entry
    type: recipe_case
    inputs:
      prompt: Split reporting work into a child job.
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "The reporting-cell work requires a child job boundary."
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
              sessionId: sid-plan-4
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "bb87196c131ff0864ecee0cab363615b82504c08f3d0caa3eca74c777060e3fe", "artifact": {"jobId": "sid-plan-4", "taskOrdinal": 5, "name": "__c2j_objects__/bb87196c131ff0864ecee0cab363615b82504c08f3d0caa3eca74c777060e3fe.tar", "sizeBytes": 100}}
              raw_output: '{"plan_id":"PLAN-4","summary":"Invalid child boundary metadata.","tasks":[{"id":"TASK-CHILD-1","title":"Delegate reporting-cell update","status":"pending","dependencies":[],"target_ref":"main","requires_child_job":true,"child_job_reason":"cross-cell work","instructions":"Start a child job owned by the reporting cell.","validation_commands":[],"review_requirements":["spec"]}],"ready_task_ids":["TASK-CHILD-1"],"validation_strategy":{"commands":[]},"child_job_boundaries":[]}'
              parsed_output:
                plan_id: PLAN-4
                summary: Invalid child boundary metadata.
                tasks:
                  - id: TASK-CHILD-1
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
                  - TASK-CHILD-1
                validation_strategy:
                  commands: []
                child_job_boundaries: []
        - match:
            op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
          behavior:
            mode: passthrough
        - match:
            op: extension_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: plan_ok
        value: false
      - type: output_equals
        path: plan_failed_rule_count
        value: 1
      - type: output_equals
        path: child_boundary_coverage_failed
        value: true
      - type: output_equals
        path: child_boundary_orphan_failed
        value: false
```

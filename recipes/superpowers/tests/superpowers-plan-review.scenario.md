# superpowers-plan-review test suite

```yaml
cases:
  - id: ts-078-plan-review-approves-aligned-plan
    type: recipe_case
    inputs:
      prompt: Add an audit-log export feature for admins.
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "Add a scoped export endpoint and background job.",
          "plan_inputs": {"required_outcomes":["admin-only authorization","export job","status visibility"]}
        }
      plan_json: |
        {
          "plan_id":"PLAN-REVIEW-1",
          "summary":"Implement admin audit-log export.",
          "tasks":[
            {
              "id":"TASK-1",
              "title":"Add admin export authorization",
              "status":"pending",
              "dependencies":[],
              "target_ref":"main",
              "requires_child_job":false,
              "child_job_reason":"",
              "instructions":"Add admin-only export authorization and tests.",
              "validation_commands":["go test ./..."],
              "review_requirements":["spec","quality"]
            }
          ],
          "ready_task_ids":["TASK-1"],
          "validation_strategy":{"commands":["go test ./..."]},
          "child_job_boundaries":[]
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
            node_path: superpowers-plan-review/review_plan
          behavior:
            mode: return
            outputs: &plan_review_ok
              status: completed
              sessionId: sid-plan-review-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "a506803576f2640ff6b7b2732f03997fef6446074668664cb2cf52d5fd08840c", "artifact": {"jobId": "sid-plan-review-1", "taskOrdinal": 2, "name": "__c2j_objects__/a506803576f2640ff6b7b2732f03997fef6446074668664cb2cf52d5fd08840c.tar", "sizeBytes": 100}}
              assistantSummary: Plan review approved.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-plan-review
              raw_summary: Plan review approved.
              output_source: artifact
              output_path: superpowers/plan-review/result.json
              raw_output: '{"ok":true,"issues":[],"recommendations":["Keep validation scoped to the changed behavior."],"blocking_feedback":"","requires_replan":false}'
              parsed_output:
                ok: true
                issues: []
                recommendations:
                  - Keep validation scoped to the changed behavior.
                blocking_feedback: ""
                requires_replan: false
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/plan-review/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Plan review approved.
                  reason: approved
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers-plan-review/plan_review_gate
          behavior:
            mode: return
            outputs: &plan_review_gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: plan-review gate passed
              results: {}
    assertions:
      - type: output_equals
        path: review_gate_ok
        value: true
      - type: output_equals
        path: plan_approved
        value: true
      - type: output_equals
        path: requires_replan
        value: false
      - type: output_equals
        path: issue_count
        value: 0
      - type: output_equals
        path: output_schema_valid
        value: true

  - id: ts-079-plan-review-blocks-incomplete-plan-for-replanning
    type: recipe_case
    inputs:
      prompt: Add an audit-log export feature for admins.
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "Add a scoped export endpoint and background job.",
          "plan_inputs": {"required_outcomes":["admin-only authorization","export job","status visibility"]}
        }
      plan_json: |
        {
          "plan_id":"PLAN-REVIEW-2",
          "summary":"Implement export job only.",
          "tasks":[
            {
              "id":"TASK-1",
              "title":"Add export job",
              "status":"pending",
              "dependencies":[],
              "target_ref":"main",
              "requires_child_job":false,
              "child_job_reason":"",
              "instructions":"Add the export job.",
              "validation_commands":[],
              "review_requirements":["spec"]
            }
          ],
          "ready_task_ids":["TASK-1"],
          "validation_strategy":{"commands":[]},
          "child_job_boundaries":[]
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
            node_path: superpowers-plan-review/review_plan
          behavior:
            mode: return
            outputs:
              <<: *plan_review_ok
              sessionId: sid-plan-review-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "fd94e93915781a0d332cb55b80866fd02693035fec415b7b1e64c468baecb1af", "artifact": {"jobId": "sid-plan-review-2", "taskOrdinal": 3, "name": "__c2j_objects__/fd94e93915781a0d332cb55b80866fd02693035fec415b7b1e64c468baecb1af.tar", "sizeBytes": 100}}
              assistantSummary: Plan review blocked.
              raw_summary: Plan review blocked.
              raw_output: '{"ok":false,"issues":["Plan omits admin-only authorization and has no validation command."],"recommendations":["Add an authorization task before the export job."],"blocking_feedback":"Replan to cover admin authorization and validation evidence.","requires_replan":true}'
              parsed_output:
                ok: false
                issues:
                  - Plan omits admin-only authorization and has no validation command.
                recommendations:
                  - Add an authorization task before the export job.
                blocking_feedback: Replan to cover admin authorization and validation evidence.
                requires_replan: true
        - match:
            node_path: superpowers-plan-review/plan_review_gate
          behavior:
            mode: return
            outputs: *plan_review_gate_ok
    assertions:
      - type: output_equals
        path: review_gate_ok
        value: true
      - type: output_equals
        path: plan_approved
        value: false
      - type: output_equals
        path: requires_replan
        value: true
      - type: output_equals
        path: issue_count
        value: 1
      - type: output_equals
        path: blocking_feedback
        value: Replan to cover admin authorization and validation evidence.
```

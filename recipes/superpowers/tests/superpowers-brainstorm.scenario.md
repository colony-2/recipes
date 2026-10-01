# superpowers-brainstorm test suite

```yaml
recipe: ../superpowers-brainstorm.yaml
cases:
  - id: ts-061-brainstorm-produces-plan-ready-design
    type: recipe_case
    inputs:
      prompt: Add an audit-log export feature for admins.
      route_json: |
        {
          "recommended_mode": "brainstorm",
          "selected_skill": "c2-superpowers-brainstorm"
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
            node_path: superpowers-brainstorm/brainstorm
          behavior:
            mode: return
            outputs: &plan_ready_brainstorm
              status: completed
              sessionId: sid-brainstorm-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "97bf7825a65c37e610d5d0c4a6f452a952af8f60e013e32071a4006a5bd43057", "artifact": {"jobId": "sid-brainstorm-1", "taskOrdinal": 2, "name": "__c2j_objects__/97bf7825a65c37e610d5d0c4a6f452a952af8f60e013e32071a4006a5bd43057.tar", "sizeBytes": 100}}
              assistantSummary: Design is ready for planning.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-brainstorm
              raw_summary: Design is ready for planning.
              output_source: artifact
              output_path: superpowers/brainstorm/result.json
              raw_output: '{"summary":"Admins can export audit logs with filters.","recommended_approach":"Add a scoped export endpoint and background job.","alternatives":[{"name":"Synchronous CSV response","tradeoffs":"Simpler but fragile for large exports."},{"name":"Background export job","tradeoffs":"More moving parts but safer for large data."}],"open_questions":[],"approved_for_planning":true,"plan_inputs":{"scope":["export endpoint","job status","authorization"],"validation_commands":["go test ./..."]}}'
              parsed_output:
                summary: Admins can export audit logs with filters.
                recommended_approach: Add a scoped export endpoint and background job.
                alternatives:
                  - name: Synchronous CSV response
                    tradeoffs: Simpler but fragile for large exports.
                  - name: Background export job
                    tradeoffs: More moving parts but safer for large data.
                open_questions: []
                approved_for_planning: true
                plan_inputs:
                  scope:
                    - export endpoint
                    - job status
                    - authorization
                  validation_commands:
                    - go test ./...
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/brainstorm/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Design is ready for planning.
                  reason: approved
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers-brainstorm/brainstorm_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: brainstorm output valid
              results: {}
    assertions:
      - type: output_equals
        path: brainstorm_ok
        value: true
      - type: output_equals
        path: approved_for_planning
        value: true
      - type: output_equals
        path: recommended_approach
        value: Add a scoped export endpoint and background job.
      - type: output_equals
        path: output_schema_valid
        value: true
      - type: output_equals
        path: status_contract_valid
        value: true

  - id: ts-062-brainstorm-stops-for-open-question-before-planning
    type: recipe_case
    inputs:
      prompt: Build the analytics export but use the usual source.
      route_json: |
        {
          "recommended_mode": "brainstorm",
          "selected_skill": "c2-superpowers-brainstorm"
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
            node_path: superpowers-brainstorm/brainstorm
          behavior:
            mode: return
            outputs:
              <<: *plan_ready_brainstorm
              sessionId: sid-brainstorm-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "3b76bc6d3db8ea858bc16ba34591fd1f91c4462b53aee27c2458329367168ed0", "artifact": {"jobId": "sid-brainstorm-2", "taskOrdinal": 3, "name": "__c2j_objects__/3b76bc6d3db8ea858bc16ba34591fd1f91c4462b53aee27c2458329367168ed0.tar", "sizeBytes": 100}}
              raw_output: '{"summary":"Analytics export source is ambiguous.","recommended_approach":"","alternatives":[],"open_questions":["Which analytics source should be exported?"],"approved_for_planning":false,"plan_inputs":{}}'
              parsed_output:
                summary: Analytics export source is ambiguous.
                recommended_approach: ""
                alternatives: []
                open_questions:
                  - Which analytics source should be exported?
                approved_for_planning: false
                plan_inputs: {}
        - match:
            node_path: superpowers-brainstorm/brainstorm_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: brainstorm output valid
              results: {}
    assertions:
      - type: output_equals
        path: brainstorm_ok
        value: true
      - type: output_equals
        path: approved_for_planning
        value: false
      - type: output_equals
        path: open_questions
        value:
          - Which analytics source should be exported?
```

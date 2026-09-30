# superpowers-route test suite

```yaml
cases:
  - id: ts-059-route-feature-request-to-brainstorm
    type: recipe_case
    inputs:
      prompt: Add an audit-log export feature for admins.
      mode: auto
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers-route/heuristic_route/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: &route_brainstorm
              status: completed
              sessionId: sid-route-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "a1bf852b313a78b087ebe9201e01f1a6b37bd4b2232f5b50d384fba53b32f8b1", "artifact": {"jobId": "sid-route-1", "taskOrdinal": 2, "name": "__c2j_objects__/a1bf852b313a78b087ebe9201e01f1a6b37bd4b2232f5b50d384fba53b32f8b1.tar", "sizeBytes": 100}}
              assistantSummary: Route selected brainstorming.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-route
              raw_summary: Route selected brainstorming.
              output_source: artifact
              output_path: superpowers/route/result.json
              raw_output: '{"recommended_mode":"brainstorm","selected_skill":"c2-superpowers-brainstorm","required_skills":["c2-superpowers-brainstorm"],"rationale":"Feature request needs design before planning.","needs_user_input":false,"user_question":"","required_artifacts":[],"human_review_required":true}'
              parsed_output:
                recommended_mode: brainstorm
                selected_skill: c2-superpowers-brainstorm
                required_skills:
                  - c2-superpowers-brainstorm
                rationale: Feature request needs design before planning.
                needs_user_input: false
                user_question: ""
                required_artifacts: []
                human_review_required: true
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/route/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Route selected brainstorming.
                  reason: routed
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: "superpowers-route/heuristic_route_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: route output valid
              results: {}
    assertions:
      - type: output_equals
        path: route_ok
        value: true
      - type: output_equals
        path: route_source
        value: heuristic_skill
      - type: output_equals
        path: recommended_mode
        value: brainstorm
      - type: output_equals
        path: selected_skill
        value: c2-superpowers-brainstorm
      - type: output_equals
        path: needs_user_input
        value: false
      - type: output_equals
        path: human_review_required
        value: true
      - type: output_equals
        path: output_schema_valid
        value: true
      - type: output_equals
        path: status_contract_valid
        value: true

  - id: ts-060-route-user-input-requires-question
    type: recipe_case
    inputs:
      prompt: Do the thing from before.
      mode: auto
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers-route/heuristic_route/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              <<: *route_brainstorm
              sessionId: sid-route-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "7ea7122e54aec89a8bfc078f59448c8aaece81c4fdffd0e24192844aa6b93d1b", "artifact": {"jobId": "sid-route-2", "taskOrdinal": 3, "name": "__c2j_objects__/7ea7122e54aec89a8bfc078f59448c8aaece81c4fdffd0e24192844aa6b93d1b.tar", "sizeBytes": 100}}
              raw_output: '{"recommended_mode":"needs_user_input","selected_skill":"c2-superpowers-route","required_skills":["c2-superpowers-route"],"rationale":"The requested prior work is ambiguous.","needs_user_input":true,"user_question":"Which prior request should this continue?","required_artifacts":[],"human_review_required":false}'
              parsed_output:
                recommended_mode: needs_user_input
                selected_skill: c2-superpowers-route
                required_skills:
                  - c2-superpowers-route
                rationale: The requested prior work is ambiguous.
                needs_user_input: true
                user_question: Which prior request should this continue?
                required_artifacts: []
                human_review_required: false
        - match:
            node_path: "superpowers-route/heuristic_route_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: route output valid
              results: {}
    assertions:
      - type: output_equals
        path: route_ok
        value: true
      - type: output_equals
        path: route_source
        value: heuristic_skill
      - type: output_equals
        path: recommended_mode
        value: needs_user_input
      - type: output_equals
        path: selected_skill
        value: c2-superpowers-route
      - type: output_equals
        path: needs_user_input
        value: true
      - type: output_equals
        path: user_question
        value: Which prior request should this continue?

  - id: ts-065-route-submitted-plan-without-skill
    type: recipe_case
    inputs:
      prompt: Continue this approved task plan.
      mode: auto
      plan_json: |
        {
          "plan_id": "PLAN-1",
          "tasks": [
            {
              "id": "TASK-1",
              "status": "pending",
              "dependencies": []
            }
          ],
          "ready_task_ids": ["TASK-1"]
        }
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers-route/heuristic_route/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *route_brainstorm
        - match:
            node_path: "superpowers-route/heuristic_route_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: route output valid
              results: {}
    assertions:
      - type: output_equals
        path: route_ok
        value: true
      - type: output_equals
        path: route_source
        value: recipe_state
      - type: output_equals
        path: recommended_mode
        value: execute_plan
      - type: output_equals
        path: selected_skill
        value: c2-superpowers-task-implementer
      - type: output_equals
        path: required_artifacts
        value:
          - superpowers/plan/plan.json
      - type: output_equals
        path: output_schema_valid
        value: true
      - type: output_equals
        path: status_contract_valid
        value: true

  - id: ts-066-route-submitted-design-without-skill
    type: recipe_case
    inputs:
      prompt: Turn this approved design into tasks.
      mode: auto
      design_json: |
        {
          "approved_for_planning": true,
          "recommended_approach": "Use the existing export pipeline."
        }
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "superpowers-route/heuristic_route/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs: *route_brainstorm
        - match:
            node_path: "superpowers-route/heuristic_route_gate/git+https://github.com/colony-2/c2ops.git//rule_gate@main"
          behavior:
            mode: return
            outputs:
              version: test
              ok: true
              failed_rule_ids: []
              summary: route output valid
              results: {}
    assertions:
      - type: output_equals
        path: route_ok
        value: true
      - type: output_equals
        path: route_source
        value: recipe_state
      - type: output_equals
        path: recommended_mode
        value: write_plan
      - type: output_equals
        path: selected_skill
        value: c2-superpowers-write-plan
      - type: output_equals
        path: required_artifacts
        value:
          - superpowers/brainstorm/result.json
```

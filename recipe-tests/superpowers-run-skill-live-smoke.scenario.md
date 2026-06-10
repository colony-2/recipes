# superpowers-run-skill-live-smoke test suite

```yaml
cases:
  - id: ts-092-live-run-skill-artifact-status-contract-shape
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
            node_path: superpowers-run-skill-live-smoke/seed_skill
          behavior:
            mode: return
            outputs:
              stdout: ""
              exit_code: 0
        - match:
            node_path: superpowers-run-skill-live-smoke/run_skill
          behavior:
            mode: return
            outputs: &live_run_skill_output
              status: completed
              sessionId: sid-live-run-skill
              assistantSummary: Live run_skill smoke completed.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-run-skill-live-smoke
              raw_summary: Live run_skill smoke completed.
              output_source: artifact
              output_path: superpowers/run-skill-live/result.json
              raw_output: '{"smoke":"run_skill_live_artifact","summary":"run_skill wrote artifact output","selected_skill":"c2-run-skill-live-smoke","next_phase":"validated","input_echo":"run-skill-live"}'
              parsed_output:
                smoke: run_skill_live_artifact
                summary: run_skill wrote artifact output
                selected_skill: c2-run-skill-live-smoke
                next_phase: validated
                input_echo: run-skill-live
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/run-skill-live/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Live run_skill smoke completed.
                  reason: artifact and status contract written
                nextSkillCandidates: []
                checkpoint:
                  status: completed
                  scope: top_level
                  stack: []
              status_contract_errors: []
              diagnostics:
                skill: c2-run-skill-live-smoke
                output_source: artifact
                output_path: superpowers/run-skill-live/result.json
                output_schema_valid: true
                output_schema_errors: []
                output_repair_attempts: 0
                status_contract_path: superpowers/run-skill-live/latest-status.json
                status_contract_present: true
                status_contract_valid: true
                status_contract_errors: []
            artifacts:
              superpowers/run-skill-live/result.json: '{"smoke":"run_skill_live_artifact","summary":"run_skill wrote artifact output","selected_skill":"c2-run-skill-live-smoke","next_phase":"validated","input_echo":"run-skill-live"}'
              superpowers/run-skill-live/latest-status.json: '{"status":"completed","summary":{"human":"Live run_skill smoke completed.","reason":"artifact and status contract written"},"nextSkillCandidates":[],"checkpoint":{"status":"completed","scope":"top_level","stack":[]}}'
              _skill_run/contract.json: '{"skill":"c2-run-skill-live-smoke","artifact_inbox_path":"/tmp/inbox","artifact_outbox_path":"/tmp/outbox","status_contract":{"path":"superpowers/run-skill-live/latest-status.json"},"output":{"from":"artifact","path":"superpowers/run-skill-live/result.json","format":"json"},"input":{"smoke_id":"run-skill-live","expected_skill":"c2-run-skill-live-smoke"}}'
              _skill_run/validation.json: '{"skill":"c2-run-skill-live-smoke","status_contract_path":"superpowers/run-skill-live/latest-status.json","status_contract_present":true,"status_contract_valid":true,"status_contract_errors":[],"output_source":"artifact","output_path":"superpowers/run-skill-live/result.json","output_schema_valid":true,"output_schema_errors":[],"output_repair_attempts":0}'
        - match:
            node_path: superpowers-run-skill-live-smoke/assert_contract
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: live_run_skill_status
        value: completed
      - type: output_equals
        path: live_run_skill_session_nonempty
        value: true
      - type: output_equals
        path: live_run_skill_name
        value: c2-run-skill-live-smoke
      - type: output_equals
        path: live_run_skill_output_schema_valid
        value: true
      - type: output_equals
        path: live_run_skill_status_contract_present
        value: true
      - type: output_equals
        path: live_run_skill_status_contract_valid
        value: true
      - type: output_equals
        path: live_run_skill_artifact_assertions_passed
        value: true

  - id: ts-093-live-run-skill-parsed-artifact-fields-shape
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
            node_path: superpowers-run-skill-live-smoke/seed_skill
          behavior:
            mode: return
            outputs:
              stdout: ""
              exit_code: 0
        - match:
            node_path: superpowers-run-skill-live-smoke/run_skill
          behavior:
            mode: return
            outputs: *live_run_skill_output
            artifacts:
              superpowers/run-skill-live/result.json: '{"smoke":"run_skill_live_artifact","summary":"run_skill wrote artifact output","selected_skill":"c2-run-skill-live-smoke","next_phase":"validated","input_echo":"run-skill-live"}'
              superpowers/run-skill-live/latest-status.json: '{"status":"completed","summary":{"human":"Live run_skill smoke completed.","reason":"artifact and status contract written"},"nextSkillCandidates":[],"checkpoint":{"status":"completed","scope":"top_level","stack":[]}}'
              _skill_run/contract.json: '{"skill":"c2-run-skill-live-smoke","artifact_inbox_path":"/tmp/inbox","artifact_outbox_path":"/tmp/outbox","status_contract":{"path":"superpowers/run-skill-live/latest-status.json"},"output":{"from":"artifact","path":"superpowers/run-skill-live/result.json","format":"json"},"input":{"smoke_id":"run-skill-live","expected_skill":"c2-run-skill-live-smoke"}}'
              _skill_run/validation.json: '{"skill":"c2-run-skill-live-smoke","status_contract_path":"superpowers/run-skill-live/latest-status.json","status_contract_present":true,"status_contract_valid":true,"status_contract_errors":[],"output_source":"artifact","output_path":"superpowers/run-skill-live/result.json","output_schema_valid":true,"output_schema_errors":[],"output_repair_attempts":0}'
        - match:
            node_path: superpowers-run-skill-live-smoke/assert_contract
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: live_run_skill_output_source
        value: artifact
      - type: output_equals
        path: live_run_skill_output_path
        value: superpowers/run-skill-live/result.json
      - type: output_equals
        path: live_run_skill_output_repair_attempts
        value: 0
      - type: output_equals
        path: live_run_skill_status_contract_status
        value: completed
      - type: output_equals
        path: live_run_skill_parsed_smoke
        value: run_skill_live_artifact
      - type: output_equals
        path: live_run_skill_parsed_selected_skill
        value: c2-run-skill-live-smoke
      - type: output_equals
        path: live_run_skill_parsed_next_phase
        value: validated
      - type: output_equals
        path: live_run_skill_parsed_input_echo
        value: run-skill-live
```

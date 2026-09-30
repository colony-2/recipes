# superpowers-debug test suite

```yaml
cases:
  - id: ts-074-debug-routes-reproduced-failure-to-fix-ready
    type: recipe_case
    inputs:
      bug_report: "The CLI exits with an error for a valid request."
      repro_command: "printf 'boom\\n'; exit 7"
      failure_context_json: "{}"
      attempt_count: "1"
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-debug/collect_debug_inputs/command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/investigate/sequence/run_reproduction
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/investigate/sequence/summarize_debug
          behavior:
            mode: return
            outputs: &debug_fix_ready
              status: completed
              sessionId: sid-debug-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "e035e1f5bef9dd39c42479547aeadc4aa148c2d782d29c1b63f55fbecbbfe042", "artifact": {"jobId": "sid-debug-1", "taskOrdinal": 2, "name": "__c2j_objects__/e035e1f5bef9dd39c42479547aeadc4aa148c2d782d29c1b63f55fbecbbfe042.tar", "sizeBytes": 100}}
              assistantSummary: Failure reproduced and root cause identified.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-debug
              raw_summary: Failure reproduced and root cause identified.
              output_source: artifact
              output_path: superpowers/debug/result.json
              raw_output: '{"reproduced":true,"root_cause":"The parser rejects the valid flag before dispatch.","evidence":["Reproduction command exited 7.","Output contains boom."],"recommended_fix":"Adjust flag parsing before dispatch.","requires_plan_update":false,"validation_commands":["printf ok"]}'
              parsed_output:
                reproduced: true
                root_cause: The parser rejects the valid flag before dispatch.
                evidence:
                  - Reproduction command exited 7.
                  - Output contains boom.
                recommended_fix: Adjust flag parsing before dispatch.
                requires_plan_update: false
                validation_commands:
                  - printf ok
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/debug/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Failure reproduced and root cause identified.
                  reason: root_cause_found
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers-debug/investigate/sequence/debug_gate
          behavior:
            mode: return
            outputs: &debug_gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: debug gate passed
              results: {}
    assertions:
      - type: output_equals
        path: debug_status
        value: fix_ready
      - type: output_equals
        path: has_repro_command
        value: true
      - type: output_equals
        path: attempt_count
        value: 1
      - type: output_equals
        path: reproduction_exit_code
        value: 7
      - type: output_equals
        path: reproduced
        value: true
      - type: output_equals
        path: requires_plan_update
        value: false
      - type: output_equals
        path: evidence_count
        value: 2
      - type: output_equals
        path: debug_gate_ok
        value: true
      - type: node_executed
        node_path: superpowers-debug/investigate/sequence/run_reproduction
      - type: node_executed
        node_path: superpowers-debug/investigate/sequence/summarize_debug

  - id: ts-075-debug-stops-before-skill-without-repro-command
    type: recipe_case
    inputs:
      bug_report: "The service behaves unexpectedly."
      failure_context_json: "{}"
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-debug/collect_debug_inputs/command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/needs_repro_command/command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/investigate/sequence/run_reproduction
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/investigate/sequence/summarize_debug
          behavior:
            mode: return
            outputs: *debug_fix_ready
        - match:
            node_path: superpowers-debug/investigate/sequence/debug_gate
          behavior:
            mode: return
            outputs: *debug_gate_ok
    assertions:
      - type: output_equals
        path: debug_status
        value: needs_repro_command
      - type: output_equals
        path: has_repro_command
        value: false
      - type: output_equals
        path: reproduced
        value: false
      - type: output_equals
        path: debug_gate_ok
        value: false
      - type: node_not_executed
        node_path: superpowers-debug/investigate/sequence/summarize_debug

  - id: ts-076-debug-routes-plan-root-cause-to-plan-update
    type: recipe_case
    inputs:
      bug_report: "The selected task cannot satisfy the requested behavior."
      repro_command: "printf 'plan mismatch\\n'; exit 9"
      failure_context_json: '{"plan_id":"PLAN-DEBUG-1"}'
      attempt_count: "1"
    mocks:
      ops:
        - match:
            node_path: superpowers-debug/collect_debug_inputs/command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/investigate/sequence/run_reproduction
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-debug/investigate/sequence/summarize_debug
          behavior:
            mode: return
            outputs:
              <<: *debug_fix_ready
              sessionId: sid-debug-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "15f846a04b4934066208ee784cc80ebd2deebd25dac7198e5e590b2b5282c451", "artifact": {"jobId": "sid-debug-2", "taskOrdinal": 3, "name": "__c2j_objects__/15f846a04b4934066208ee784cc80ebd2deebd25dac7198e5e590b2b5282c451.tar", "sizeBytes": 100}}
              raw_output: '{"reproduced":true,"root_cause":"The plan omits the compatibility requirement.","evidence":["Reproduction command exited 9."],"recommended_fix":"Update the task plan before implementation.","requires_plan_update":true,"validation_commands":[]}'
              parsed_output:
                reproduced: true
                root_cause: The plan omits the compatibility requirement.
                evidence:
                  - Reproduction command exited 9.
                recommended_fix: Update the task plan before implementation.
                requires_plan_update: true
                validation_commands: []
        - match:
            node_path: superpowers-debug/investigate/sequence/debug_gate
          behavior:
            mode: return
            outputs: *debug_gate_ok
    assertions:
      - type: output_equals
        path: debug_status
        value: requires_plan_update
      - type: output_equals
        path: reproduction_exit_code
        value: 9
      - type: output_equals
        path: reproduced
        value: true
      - type: output_equals
        path: requires_plan_update
        value: true
      - type: output_equals
        path: debug_gate_ok
        value: true

  - id: ts-077-debug-requires-architecture-review-after-third-attempt
    type: recipe_case
    inputs:
      bug_report: "The same validation failure persists after repeated fixes."
      repro_command: "printf 'still failing\\n'; exit 8"
      failure_context_json: "{}"
      attempt_count: "3"
    mocks:
      ops:
        - match:
            node_path: superpowers-debug/collect_debug_inputs/command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-debug/investigate/sequence/run_reproduction
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-debug/investigate/sequence/summarize_debug
          behavior:
            mode: return
            outputs:
              <<: *debug_fix_ready
              sessionId: sid-debug-3
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "c1e23c0948c31f6b39defc7183fd5e50f619987aea514f1b26cf4fbfcbae7eb0", "artifact": {"jobId": "sid-debug-3", "taskOrdinal": 4, "name": "__c2j_objects__/c1e23c0948c31f6b39defc7183fd5e50f619987aea514f1b26cf4fbfcbae7eb0.tar", "sizeBytes": 100}}
              raw_output: '{"reproduced":true,"root_cause":"The current architecture cannot preserve both invariants.","evidence":["Reproduction command exited 8."],"recommended_fix":"Discuss architecture before another fix attempt.","requires_plan_update":false,"validation_commands":["printf review"]}'
              parsed_output:
                reproduced: true
                root_cause: The current architecture cannot preserve both invariants.
                evidence:
                  - Reproduction command exited 8.
                recommended_fix: Discuss architecture before another fix attempt.
                requires_plan_update: false
                validation_commands:
                  - printf review
        - match:
            node_path: superpowers-debug/investigate/sequence/debug_gate
          behavior:
            mode: return
            outputs: *debug_gate_ok
    assertions:
      - type: output_equals
        path: debug_status
        value: architecture_review_required
      - type: output_equals
        path: attempt_count
        value: 3
      - type: output_equals
        path: reproduction_exit_code
        value: 8
      - type: output_equals
        path: reproduced
        value: true
      - type: output_equals
        path: debug_gate_ok
        value: true
```

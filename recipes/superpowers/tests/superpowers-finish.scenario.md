# superpowers-finish test suite

```yaml
recipe: ../superpowers-finish.yaml
cases:
  - id: ts-071-finish-recommends-merge-ready-from-verified-evidence
    type: recipe_case
    inputs:
      plan_json: &verified_plan |
        {
          "plan_id": "PLAN-FINISH-1",
          "summary": "Finish verified work.",
          "tasks": [
            {
              "id": "TASK-1",
              "title": "Implement feature",
              "status": "done"
            }
          ]
        }
      verification_result_json: &verified_result |
        {
          "ok": true,
          "commands_required": ["printf verified"],
          "commands_observed": [{"command":"printf verified","exit_code":0}],
          "evidence_summary": "Required verification passed.",
          "blocking_issues": []
        }
      execution_result_json: |
        {"task_id":"TASK-1","status":"done","summary":"Task completed."}
      completion_action: recommend
    mocks:
      ops:
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/collect_finish_inputs
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-finish/recommend/command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs: &finish_merge_ready
              status: completed
              sessionId: sid-finish-1
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "7e2b358eb6930b260bcc2e87317f6a0cbbeffb6a9b1708134a1a72f73040c366", "artifact": {"jobId": "sid-finish-1", "taskOrdinal": 2, "name": "__c2j_objects__/7e2b358eb6930b260bcc2e87317f6a0cbbeffb6a9b1708134a1a72f73040c366.tar", "sizeBytes": 100}}
              assistantSummary: Finish is merge-ready.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: c2-superpowers-finish
              raw_summary: Finish is merge-ready.
              output_source: artifact
              output_path: superpowers/finish/result.json
              raw_output: '{"decision":"merge_ready","summary":"Verified work is ready to merge.","completed_tasks":["TASK-1"],"verification_summary":"Required verification passed.","remaining_risks":[],"merge_ready":true}'
              parsed_output:
                decision: merge_ready
                summary: Verified work is ready to merge.
                completed_tasks:
                  - TASK-1
                verification_summary: Required verification passed.
                remaining_risks: []
                merge_ready: true
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: superpowers/finish/latest-status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
                summary:
                  human: Finish is merge-ready.
                  reason: verified
              status_contract_errors: []
              diagnostics: {}
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs: &finish_gate_ok
              version: test
              ok: true
              failed_rule_ids: []
              summary: finish gate passed
              results: {}
    assertions:
      - type: output_equals
        path: finish_decision
        value: merge_ready
      - type: output_equals
        path: merge_ready
        value: true
      - type: output_equals
        path: finish_gate_ok
        value: true
      - type: output_equals
        path: action_taken
        value: recommend
      - type: output_equals
        path: merged
        value: false

  - id: ts-072-finish-blocks-merge-when-verification-has-issues
    type: recipe_case
    inputs:
      plan_json: *verified_plan
      verification_result_json: |
        {
          "ok": false,
          "commands_required": ["printf failing && exit 7"],
          "commands_observed": [{"command":"printf failing && exit 7","exit_code":7}],
          "evidence_summary": "Required verification failed.",
          "blocking_issues": ["Validation command exited 7."]
        }
      execution_result_json: |
        {"task_id":"TASK-1","status":"done","summary":"Task claimed completion."}
      completion_action: merge
      local_hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
      upstream_repo: git@example.test:org/repo.git
      upstream_branch: main
      commit_message: Finish verified work
    mocks:
      ops:
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/collect_finish_inputs
          behavior:
            mode: passthrough
        - match:
            node_path: superpowers-finish/merge_blocked/command_execution
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *finish_merge_ready
              sessionId: sid-finish-2
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "947675b4085a1d01cb2cdbd94f997f67dc764c5cabd6e1d73d992f7e1b7b2eed", "artifact": {"jobId": "sid-finish-2", "taskOrdinal": 3, "name": "__c2j_objects__/947675b4085a1d01cb2cdbd94f997f67dc764c5cabd6e1d73d992f7e1b7b2eed.tar", "sizeBytes": 100}}
              assistantSummary: Finish needs revision.
              raw_summary: Finish needs revision.
              raw_output: '{"decision":"needs_revision","summary":"Verification failed, so this cannot merge.","completed_tasks":["TASK-1"],"verification_summary":"Required verification failed.","remaining_risks":["Validation command exited 7."],"merge_ready":false}'
              parsed_output:
                decision: needs_revision
                summary: Verification failed, so this cannot merge.
                completed_tasks:
                  - TASK-1
                verification_summary: Required verification failed.
                remaining_risks:
                  - Validation command exited 7.
                merge_ready: false
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs:
              version: test
              ok: false
              failed_rule_ids:
                - merge_ready_requires_verification_ok
              summary: finish gate blocked merge
              results: {}
    assertions:
      - type: output_equals
        path: finish_decision
        value: needs_revision
      - type: output_equals
        path: merge_ready
        value: false
      - type: output_equals
        path: finish_gate_ok
        value: false
      - type: output_equals
        path: action_taken
        value: merge_blocked
      - type: output_equals
        path: merged
        value: false
      - type: output_equals
        path: merge_blocked_reason_count
        value: 3

  - id: ts-073-finish-merges-only-after-gate-and-explicit-action
    type: recipe_case
    inputs:
      plan_json: *verified_plan
      verification_result_json: *verified_result
      execution_result_json: |
        {"task_id":"TASK-1","status":"done","summary":"Task completed."}
      completion_action: merge
      local_hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
      upstream_repo: git@example.test:org/repo.git
      upstream_branch: main
      commit_message: Finish verified work
    mocks:
      ops:
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/collect_finish_inputs
          behavior:
            mode: passthrough
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/write_finish_summary
          behavior:
            mode: return
            outputs:
              <<: *finish_merge_ready
              sessionId: sid-finish-3
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "0a60d681441a490d21f562f0d2bff709f38597742666a4f22cbeef6101377de1", "artifact": {"jobId": "sid-finish-3", "taskOrdinal": 4, "name": "__c2j_objects__/0a60d681441a490d21f562f0d2bff709f38597742666a4f22cbeef6101377de1.tar", "sizeBytes": 100}}
        - match:
            node_path: superpowers-finish/summarize_finish/sequence/finish_gate
          behavior:
            mode: return
            outputs: *finish_gate_ok
        - match:
            node_path: superpowers-finish/merge/squashrebasemerge
          behavior:
            mode: return
            outputs:
              merged_hash: merge456
              target_branch: main
    assertions:
      - type: output_equals
        path: finish_decision
        value: merge_ready
      - type: output_equals
        path: finish_gate_ok
        value: true
      - type: output_equals
        path: action_taken
        value: merge
      - type: output_equals
        path: merged
        value: true
      - type: output_equals
        path: merged_hash
        value: merge456
      - type: output_equals
        path: target_branch
        value: main
      - type: node_executed
        node_path: superpowers-finish/merge/squashrebasemerge
```

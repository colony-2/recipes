# superpowers-session-contract-smoke test suite

```yaml
recipe: superpowers-session-contract-smoke.yaml
cases:
  - id: ts-054-session-id-controls-isolation-and-resume
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
            node_path: "superpowers-session-contract-smoke/start_isolated_session/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "95bfb3d7e8b46f527330dd91782b6d2b9f4b50f595faafaa98a317ae41fb3699", "artifact": {"jobId": "sid-role", "taskOrdinal": 2, "name": "__c2j_objects__/95bfb3d7e8b46f527330dd91782b6d2b9f4b50f595faafaa98a317ae41fb3699.tar", "sizeBytes": 100}}
              assistantSummary: Started isolated role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "e56b7639bf85217a47920cbf2b822db1219c411c4b199208372087f911a7d041", "artifact": {"jobId": "sid-role", "taskOrdinal": 3, "name": "__c2j_objects__/e56b7639bf85217a47920cbf2b822db1219c411c4b199208372087f911a7d041.tar", "sizeBytes": 100}}
              assistantSummary: Started isolated role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-session-contract-smoke/resume_same_session/git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "d2259e8e7fe40d36fdfa7e9dc1bd2c13bde27c5f2d0c9a14c8e9d9899af04c5f", "artifact": {"jobId": "sid-role", "taskOrdinal": 4, "name": "__c2j_objects__/d2259e8e7fe40d36fdfa7e9dc1bd2c13bde27c5f2d0c9a14c8e9d9899af04c5f.tar", "sizeBytes": 100}}
              assistantSummary: Resumed the same role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-role
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "e2c5e113ba150cabe17e14495032804eab783300e73f039a0d80a044d3447da3", "artifact": {"jobId": "sid-role", "taskOrdinal": 5, "name": "__c2j_objects__/e2c5e113ba150cabe17e14495032804eab783300e73f039a0d80a044d3447da3.tar", "sizeBytes": 100}}
              assistantSummary: Resumed the same role session.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: isolated_session_requested_without_session_id
        value: true
      - type: output_equals
        path: isolated_session_id
        value: sid-role
      - type: output_equals
        path: resume_requested_session_id
        value: sid-role
      - type: output_equals
        path: resumed_session_id
        value: sid-role
      - type: output_equals
        path: resume_reused_session_id
        value: true
      - type: output_equals
        path: both_steps_completed
        value: true
```

# superpowers-task-session-smoke test suite

```yaml
recipe: superpowers-task-session-smoke.yaml
cases:
  - id: ts-053-same-job-task-boundary-uses-distinct-role-sessions
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
            op: command_execution
          behavior:
            mode: passthrough
        - match:
            node_path: "superpowers-task-session-smoke/implementer_session/nix:github:colony-2/c2ops/main#codex"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-implementer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "7d98c231a80e9749753a77b653895b3f4eb48f596630b6b077a735deaefd8b9f", "artifact": {"jobId": "sid-implementer", "taskOrdinal": 2, "name": "__c2j_objects__/7d98c231a80e9749753a77b653895b3f4eb48f596630b6b077a735deaefd8b9f.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 implemented and validated.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-implementer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "5491504c438d232f93197482d502712bf9182dade24072ba9ab80d0d700d944b", "artifact": {"jobId": "sid-implementer", "taskOrdinal": 3, "name": "__c2j_objects__/5491504c438d232f93197482d502712bf9182dade24072ba9ab80d0d700d944b.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 implemented and validated.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-task-session-smoke/spec_reviewer_session/nix:github:colony-2/c2ops/main#codex"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-spec-reviewer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "88360c3ec4c0260ae10226709e9ee47e1fdeba1cacbf08e5f8b07d87600866bc", "artifact": {"jobId": "sid-spec-reviewer", "taskOrdinal": 4, "name": "__c2j_objects__/88360c3ec4c0260ae10226709e9ee47e1fdeba1cacbf08e5f8b07d87600866bc.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 matches the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-spec-reviewer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "4a777a7c45e9950488ea7079eb90a35bbcef3479140e97aa228864c27590b81e", "artifact": {"jobId": "sid-spec-reviewer", "taskOrdinal": 5, "name": "__c2j_objects__/4a777a7c45e9950488ea7079eb90a35bbcef3479140e97aa228864c27590b81e.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 matches the selected task.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            node_path: "superpowers-task-session-smoke/quality_reviewer_session/nix:github:colony-2/c2ops/main#codex"
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-quality-reviewer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "ca0aadbeb169e6684bf8cfc7e3d2b62e889a33ade9fc82de8794582247415766", "artifact": {"jobId": "sid-quality-reviewer", "taskOrdinal": 6, "name": "__c2j_objects__/ca0aadbeb169e6684bf8cfc7e3d2b62e889a33ade9fc82de8794582247415766.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 quality review passed.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs:
              status: completed
              sessionId: sid-quality-reviewer
              session: {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "e2bb058b03bda038eca0941c8640c2ec49150c4a67431e7050e498f7ebf7d908", "artifact": {"jobId": "sid-quality-reviewer", "taskOrdinal": 7, "name": "__c2j_objects__/e2bb058b03bda038eca0941c8640c2ec49150c4a67431e7050e498f7ebf7d908.tar", "sizeBytes": 100}}
              assistantSummary: TASK-1 quality review passed.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
    assertions:
      - type: output_equals
        path: task_id
        value: TASK-1
      - type: output_equals
        path: task_requires_child_job
        value: false
      - type: output_equals
        path: child_job_used
        value: false
      - type: output_equals
        path: role_sessions_are_distinct
        value: true
      - type: output_equals
        path: task_boundary_passed
        value: true
```

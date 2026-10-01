# codex-skill-execution-smoke test suite

Requires Codex credentials, its normal sandbox, and access to the authored skill source.

```yaml
recipe: ../recipes/smoke/codex-skill-execution-smoke.yaml
cases:
- id: ts-044-live-codex-skill-executes-and-writes-marker
  type: integration_case
  mocks:
    ops:
    - repeat: true
      match:
        op: command_execution
      behavior:
        mode: passthrough
    - repeat: true
      match:
        op: extension_execution
      behavior:
        mode: passthrough
  assertions:
  - type: output_equals
    path: codex_skill_marker_file_exists
    value: true
  - type: output_equals
    path: codex_skill_marker_file_valid
    value: true
  - type: output_equals
    path: codex_skill_status_artifact_exists
    value: true
  - type: output_equals
    path: codex_skill_status_artifact_ready
    value: true
  runtime:
    cells:
      root:
        files:
          README.md: 'Disposable live test cell.

            '
- id: ts-045-live-codex-skill-contract-artifacts-and-ref
  type: integration_case
  mocks:
    ops:
    - repeat: true
      match:
        op: command_execution
      behavior:
        mode: passthrough
    - repeat: true
      match:
        op: extension_execution
      behavior:
        mode: passthrough
  assertions:
  - type: output_equals
    path: codex_skill_session_nonempty
    value: true
  - type: output_equals
    path: codex_skill_summary_artifact_exists
    value: true
  - type: output_equals
    path: codex_skill_progress_artifact_nonempty
    value: true
  - type: output_equals
    path: codex_skill_ref_resolved
    value: gitl.colony2.com/jnadeau/skills/.agents/skills@1362438426e25c733174ea85f248db11af99a8a7
  runtime:
    cells:
      root:
        files:
          README.md: 'Disposable live test cell.

            '
live: true
```

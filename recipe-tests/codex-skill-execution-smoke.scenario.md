# codex-skill-execution-smoke test suite

```yaml
cases:
  - id: ts-044-live-codex-skill-executes-and-writes-marker
    type: recipe_case
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

  - id: ts-045-live-codex-skill-contract-artifacts-and-ref
    type: recipe_case
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
```

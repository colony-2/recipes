# skill-quality-smoke test suite

Requires Codex credentials, its normal sandbox, and access to the authored skill source.

```yaml
recipe: ../recipes/smoke/skill-quality-smoke.yaml
cases:
- id: ts-042-live-skill-quality-smoke
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
    path: triage_local_ok
    value: true
  - type: output_equals
    path: triage_local_rationale_nonempty
    value: true
  - type: output_equals
    path: triage_frontend_redirect
    value: true
  - type: output_equals
    path: triage_frontend_target
    value: frontend
  - type: output_equals
    path: requirements_count_nonzero
    value: true
  - type: output_equals
    path: requirements_cross_cell_false
    value: true
  - type: output_equals
    path: requirements_targets_valid
    value: true
  - type: output_equals
    path: requirements_acceptance_nonempty
    value: true
  - type: output_equals
    path: requirements_bad_review_rejects
    value: true
  - type: output_equals
    path: requirements_bad_blockers_nonempty
    value: true
  runtime:
    cells:
      root:
        files:
          README.md: 'Disposable live test cell.

            '
live: true
```

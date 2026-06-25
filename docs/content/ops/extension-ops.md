---
title: "Extension Ops"
weight: 53
---

Extension ops package repo-specific or shared behavior behind an `op.yaml` manifest.

Selector forms:

```yaml
op: ./tools/ops/echo
op: ../shared/ops/echo
op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
```

Manifest shape:

```yaml
name: echo
description: Echo input back to the caller
version: 1.0.0
shell: bash
run: python3 main.py
timeout: 30s
env:
  PYTHONUNBUFFERED: "1"
input_schema:
  type: object
  required: [message]
  properties:
    message:
      type: string
output_schema:
  type: object
  properties:
    message:
      type: string
```

Process contract:

- stdin receives one JSON object.
- stdout must be JSON.
- stdout may be either the output object or an envelope with `output` and `artifact_refs`.
- `input_schema` defaults apply before template resolution.
- `output_schema` validates the final output object.

Extension ops do not receive implicit environment metadata. Pass paths and other runtime values through inputs or manifest `env`.

Extension ops support a reserved `sandbox` input field. The runtime consumes this field before building the extension payload, so extension authors should not include `sandbox` in `input_schema`.

Direct execution:

```yaml
- id: summarize
  op: ./tools/ops/summarize
  inputs:
    sandbox:
      type: none
    report_path: "{{ context.environment.op.outbox }}/summary.json"
```

Sandboxed execution:

```yaml
- id: summarize
  op: ./tools/ops/summarize
  artifacts:
    submitted/: '${{ context.artifacts }}'
  inputs:
    sandbox:
      type: shai
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

Use `context.environment.op.*` for paths passed to the extension process. Those values are host paths for direct execution and sandbox-visible paths for `sandbox.type: shai`.

Selector-backed ops are resolved at execution time, so static recipe validation only verifies that `inputs` is an object. Concrete extension input validation happens after the op is resolved.

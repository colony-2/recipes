---
title: "Extension Ops"
weight: 53
---

Extension ops package repo-specific or shared behavior behind a manifest.
Published c2ops use Nix packages; local/Git ops use an `op.yaml` manifest.

Selector forms:

```yaml
op: ./tools/ops/echo
op: ../shared/ops/echo
op: nix:github:colony-2/c2ops/main#rule_gate
```

Nix packages expose metadata as `passthru.c2j` and install the matching manifest
at `share/c2j/op.json`, with a package-relative `command` under `bin/`. c2j
inspects metadata before fetching prebuilt executables. Workers must trust the
publishing cache and cannot build missing outputs. Use the selector directly in
`op:`, without an `extension_execution` wrapper or duplicate dependency entry.
See the [upstream extension guide](https://github.com/colony-2/c2j/blob/main/EXTENSION_OPS.md).

Local/Git manifest shape:

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

Omit op sandbox configuration as c2j removes that support.

```yaml
- id: summarize
  op: ./tools/ops/summarize
  artifacts:
    submitted/: '${{ context.artifacts }}'
  inputs:
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
```

Use `context.environment.op.*` for paths passed to the extension process.

Selector-backed ops are resolved at execution time, so static recipe validation only verifies that `inputs` is an object. Concrete extension input validation happens after the op is resolved.

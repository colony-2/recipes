---
title: "c2ops Catalog"
weight: 53
---

Use `nix:github:colony-2/c2ops/main#<package>` for shared extension ops.
Workers need current c2j `main`, Nix with flakes enabled, and the trusted `colony2`
Cachix cache. c2j records the resolved package output for each invocation;
fresh resolutions can follow updates to `main`. See
[package setup](https://github.com/colony-2/c2ops/blob/main/NIX_PACKAGES.md).

Current catalog from `github.com/colony-2/c2ops`:

| Package attribute | Use |
| --- | --- |
| `codex` | Multi-step Codex coding or review work. |
| `skill-run` | Run one Codex skill with structured output and status validation (manifest name `skill.run`). |
| `llm2` | Single model call with structured output, file context, and tools. |
| `rule_gate` | Deterministic policy rules over booleans, files, JSON, schemas, and child status. |
| `gha` | Run one GitHub Actions workflow. |
| `gha-many` | Run multiple GitHub Actions workflows. |
| `aider` | Aider-backed agentic coding through an extension op. |
| `litellm` | LiteLLM-backed LLM request compatible with the legacy LLM shape. |
| `llm` | Legacy LLM implementation through the extension mechanism. |
| `pydantic` | PydanticAI-backed LLM2-compatible requests. |

Rule gate example:

{{< example "examples/recipes/rule-gate.yaml" >}}

Codex skill pattern:

```yaml
- id: implement
  op: nix:github:colony-2/c2ops/main#skill-run
  inputs:
    skill: c2-superpowers-task-implementer
    skills:
      - "{{ inputs.skill_bundle_ref }}"
    prompt: |
      Complete TASK-1 and write result JSON to the artifact outbox.
    status_contract:
      path: superpowers/task/latest-status.json
    output:
      from: artifact
      path: superpowers/task/result.json
      format: json
      schema:
        type: object
        required: [task_id, status, summary]
        properties:
          task_id:
            type: string
          status:
            type: string
          summary:
            type: string
```

Mock selector-backed ops in `c2j test` by node path when possible. If matching the lowered extension operation, use `extension_execution`.

---
title: "c2ops Catalog"
weight: 53
---

Use `git+https://github.com/colony-2/c2ops.git//<op>@main` for shared extension ops,
except `codex` and `codex/run_skill`: pin both to
`ded76dfbd877d3d0749e509844ecdbc57197b572` for the object-session contract.

Current catalog from `github.com/colony-2/c2ops`:

| Selector Path | Use |
| --- | --- |
| `codex` | Multi-step Codex coding or review work. |
| `codex/run_skill` | Run one Codex skill with structured output and status validation. |
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
  op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572
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

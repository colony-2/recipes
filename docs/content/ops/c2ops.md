---
title: "c2ops Catalog"
weight: 53
---

Use `nix:github:colony-2/c2ops/published#<package>` for shared extension ops.
Workers need current c2j `main`, Nix with flakes enabled, and the trusted `colony2`
Cachix cache. c2j records the resolved package output for each invocation;
fresh resolutions can follow `published`, which advances only after tests,
uploads, and download verification succeed on both architectures. See
[package setup](https://github.com/colony-2/c2ops/blob/published/NIX_PACKAGES.md).

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

For complete agent execution and review examples, inspect the maintained
`recipes/adaptive/agent-turn.yaml` and `recipes/adaptive/inspect.yaml` sources.
The `skill-run` package remains available for projects that supply their own skill
bundle; this repository no longer ships the superpowers workflow family.

Mock selector-backed ops in `c2j test` by node path when possible. If matching the lowered extension operation, use `extension_execution`.

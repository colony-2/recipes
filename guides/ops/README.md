# Ops Guide

Use this guide to choose the right op before you drop into the per-op references.

## Core Rule

Most ops now run as remote durable task steps. Author them as if each step is isolated:

- send structured values through `inputs`
- move files through `artifacts`
- use `context.environment.op.worktree_path`, `context.environment.op.inbox`, and `context.environment.op.outbox` for paths consumed by an op process
- export downstream data through `outputs:`

Do not rely on ambient shell state, ad hoc temp files, or the assumption that one op can see another op's filesystem changes unless those changes are in the managed worktree or emitted as artifacts.

## Which Op To Use

- `command_execution`
  Use for bounded shell commands, light glue, validation commands, or file generation in the worktree/outbox.
  Reference: `OP_COMMAND_EXECUTION.md`

- c2ops `llm2`
  Use for one model call with optional structured output, file context, and tool execution.
  Reference: `OP_LLM_INFERENCE2.md`

- c2ops `codex`
  Use for agentic coding or review work that needs a repo worktree and durable progress.
  Reference: `OP_CODEX_EXEC.md`

- c2ops `gha`, `gha-many`
  Use when the repository already has a workflow you should reuse. These runs are disposable and do not write back into recipe git state.
  Reference: `OP_GITHUB_ACTIONS.md`

- `recipe.run_and_get_result`, `recipes.run`, `recipes.run_and_wait`, `recipe.await_result`, `recipe.await_result_soft`, `recipe.get_result`
  Use to fan work out into child recipes and consume their outputs/artifacts explicitly.
  Reference: `RUN_RECIPE.md`

- `input`
  Use for human approval, structured user answers, or workflow checkpoints that must pause for input.
  Reference: `OP_INPUT.md`

- `sleep`
  Use for explicit waits or retry backoff in orchestration flows.
  Reference: `OP_SLEEP.md`

- `thinpackrebase`, `squashrebasemerge`
  Use when the workflow is ready to integrate git changes back onto the latest upstream state.
  References: `OP_THINPACKREBASE.md`, `OP_SQUASHREBASEMERGE.md`

- selector-based extension ops
  Use when the repo needs custom packaged behavior behind a stable op interface.
  Reference: `EXTENSION_OPS_GUIDE.md`

## Selection Heuristics

- Prefer a purpose-built op over `command_execution` when one exists.
- Prefer c2ops `gha` or `gha-many` over rebuilding an existing workflow in shell.
- Prefer child recipes when a phase is substantial enough to deserve its own durable workflow boundary.
- Prefer c2ops `llm2` for single-turn structured reasoning and c2ops `codex` for multi-step codebase work.
- Prefer artifacts for handoff data instead of parsing free-form summaries.

## Remote c2ops Selectors

Most formerly named ops in this area are now selector-backed extension ops from `/c2ops`.

Use the published Nix selectors in committed recipes:

```yaml
op: nix:github:colony-2/c2ops/main#codex
```

`codex/run_skill` is packaged as `nix:github:colony-2/c2ops/main#skill-run`.
Other attributes retain their op names, including `rule_gate`, `llm2`, `gha`,
and `gha-many`. Use selectors directly in `op:`, without an
`extension_execution` wrapper or a duplicate package dependency.

Use current c2j `main` for packaged-op support. Nix resolves the manifest and
package identity; workers download prebuilt outputs from the trusted `colony2`
Cachix cache. A new resolution can follow an updated `main`, while replay uses
the recorded identity. See [package setup](https://github.com/colony-2/c2ops/blob/main/NIX_PACKAGES.md).
Tests mock model decisions by selector or node path; real schema gates still
need Nix and cache access. `extension_execution` remains the lowered op name
for mock matching, not the recipe authoring syntax.

## Authoring Loop

When you are trying a new op or adjusting inputs, use the local validation loop:

```bash
c2j submit \
  --recipe-file ./recipes/my-recipe.yaml \
  --run \
  --embed
```

That is the fastest way to validate the authored YAML against the runtime behavior of the selected ops.

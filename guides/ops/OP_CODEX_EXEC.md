# c2ops `codex` Op

Runs Codex CLI non-interactively through the selector-backed c2ops extension and returns normalized status/summary.

Use this selector form in recipes:

```yaml
op: git+https://github.com/colony-2/c2ops.git//codex@main
```

This repo uses `@main` for c2ops selectors so recipes automatically pick up c2ops fixes. In deterministic tests, mock `recipe_within_resolution` once per case and mock the Codex node path reported by c2j diagnostics, or by op `extension_execution` when there is no ambiguity.

This op also emits output artifacts:
- `stdout.jsonl`
- `stderr.txt`

## Inputs

Common fields:
- `prompt` (required): prompt sent to Codex.
- `sessionId`: resume an existing Codex session. When omitted, the op starts a
  fully isolated new Codex session. When present, the op continues that session
  and carries conversational context forward for that session ID.
- `model`: Codex model override.
- `env`: extra environment variables.
- `sandbox`: reserved c2j extension sandbox config. Use `sandbox.type: none` to run the extension process without the c2j wrapper sandbox.
- `worktree_path`: defaults to `{{ context.environment.op.worktree_path }}`.
- `workdir_path`: defaults to `{{ context.environment.op.workdir }}`.
- `artifact_inbox_path`: defaults to `{{ context.environment.op.inbox }}`.
- `artifact_outbox_path`: defaults to `{{ context.environment.op.outbox }}`.

These paths are resolved by the extension manifest. Recipes should omit the
inputs unless they need an explicit override. The resolved worktree is required
by the Codex implementation, but callers do not need to supply it themselves.

Skill-related fields:
- `skill`: optional top-level skill to enforce for this invocation.
- `skills`: list of skill source refs in format `<host>/<org>/<repo>/<skills-root-path>@<git-ref>`.
- `skill_mode`: currently supports `enforce`.
- `skill_selection_mode`: `adaptive` or `ordered` (default `adaptive`).
- `return_on`: checkpoint statuses that should cause `incomplete` return.
- `status_contract.path`: outbox-relative status JSON path (for example `implementation/latest-status.json`).

Notes:
- `skills` is for installing skill bundles.
- `skill` is for selecting/enforcing one top-level skill segment.
- `skill_artifacts` and `skill_blobs` are not supported.
- `sandbox.type: none` controls the c2j extension wrapper. Current c2ops `codex@main` invokes the Codex CLI directly and does not create an additional Shai/Docker sandbox.
- Use `context.environment.op.*` for paths passed to Codex prompts or path inputs. c2j maps these to host paths for direct execution and sandbox-visible paths for `sandbox.type: shai`.
- c2j no longer exposes a separate cell path. The current cell is rooted at `context.environment.op.worktree_path`; repo-relative paths in prompts should be relative to that root.
- For the sandbox-agnostic path contract, see `../../OP_VISIBLE_PATHS_USER_GUIDE.md`.

## Skill Source Resolution

When `skills` refs are provided, c2ops `codex`:
1. Resolves each ref to a concrete commit.
2. Fetches/checks out repository content for that commit.
3. Copies all subdirectories under the referenced skills root into the invocation skill staging area.
4. Emits resolved refs in `skills_installed` output.

Merged precedence during execution:
- repo `.c2/skills` overrides configured ref sources
- configured ref sources override codex-home copied from inbox

## Example: Basic

```yaml
- id: run_codex
  op: git+https://github.com/colony-2/c2ops.git//codex@main
  inputs:
    prompt: "Summarize the changes in this repo."
```

## Example: Skill Sources via Git Refs

```yaml
- id: run_codex_skill
  op: git+https://github.com/colony-2/c2ops.git//codex@main
  inputs:
    sandbox:
      type: none
    prompt: "Use my-skill."
    skill: "my-skill"
    skill_mode: "enforce"
    skills:
      - "github.com/acme/codex-platform-skills/.agents/skills@platform-v12"
      - "github.com/acme/payments-cell-skills/.agents/skills@main"
```

## Structured Results

The plain Codex op already enforces its normalized execution envelope
(`status`, `assistantSummary`, and related fields). It does not expose a custom
`response_schema` input for task-specific results. Ask Codex to write a JSON
artifact in the op outbox, include the desired schema in its prompt, and bind
that artifact to c2ops `rule_gate` with a `json_schema` rule before consuming it.
`codex/run_skill` also supports an artifact output contract when running a skill.

## Test Mocks

State-machine selector-backed ops appear in c2j mock diagnostics with the selector in the node path:

```yaml
node_path: "job-implement/new_session/git+https://github.com/colony-2/c2ops.git//codex@main"
```

Sequence selector-backed ops generally use the authored node id, for example `new-ticket-triage/assess_cell`.

When a recipe uses a floating selector such as `@main`, isolated tests also need a selector-resolution mock:

```yaml
- match:
    op: recipe_within_resolution
  behavior:
    mode: return
    outputs:
      resolved_selectors: {}
```

If a test matches by op name instead of node path, the runtime op name is `extension_execution`.

## Outputs

Top-level output:
- `status`: `completed | incomplete | error`
- `sessionId`
- `assistantSummary`
- `incompleteReason`
- `incompleteCategory`
- `pendingDependencies`
- `skills_installed`: resolved refs in input-compatible format (`...@<resolved-commit>`)
- `outcome` (structured checkpoint/skill/routing metadata)

Example:

```json
{
  "status": "incomplete",
  "sessionId": "session-id",
  "assistantSummary": "Need user input",
  "incompleteReason": "needs_user_input",
  "incompleteCategory": "needs_user_input",
  "pendingDependencies": [],
  "skills_installed": [
    "github.com/acme/codex-platform-skills/.agents/skills@9c71eb0d4379a4aa8f4ab94e545e1f53ec94b0b4"
  ],
  "outcome": {
    "summary": {
      "human": "Need user input",
      "reason": "awaiting response"
    },
    "skill": {
      "executed": "my-skill",
      "selectionMode": "adaptive",
      "nextCandidate": ""
    },
    "checkpoint": {
      "status": "needs_user_input",
      "scope": "top_level",
      "blockingSkill": "",
      "stack": [
        {
          "skill": "my-skill",
          "scope": "top_level"
        }
      ],
      "statusArtifact": "implementation/latest-status.json",
      "returnTriggered": true,
      "returnReason": "needs_user_input",
      "contractErrors": []
    },
    "routing": {
      "nextAction": "return_to_recipe_checkpoint"
    }
  }
}
```

## Scoped development recipes

`worktree_path` also selects Codex's starting directory. The shared evolve
workflow intentionally overrides it with the cell worktree plus `.c2j`, while
leaving runtime and artifact paths at their defaults. Build retains all defaults.
Both enable the supported Shai wrapper. The current launcher disables native
Codex sandboxing, and the outer wrapper grants workspace-wide writes: see
[the scoped sandbox report](../BUG_REPORT_SCOPED_CODEX_SANDBOX.md). Do not infer
write isolation from a subdirectory cwd; enforce recipe scope checks as well.

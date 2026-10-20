# c2ops `codex` Op

Runs Codex CLI non-interactively through the selector-backed c2ops extension and returns normalized status/summary.

Use this selector form in recipes:

```yaml
op: nix:github:colony-2/c2ops/published#codex
```

The skill entrypoint is `nix:github:colony-2/c2ops/published#skill-run`.
Both packages retain the object-session contract. See
[the migration guide](../CODEX_OBJECT_SESSION_MIGRATION.md) for worker setup.
In deterministic tests, mock model responses by selector or node path, or match
`extension_execution` when unambiguous. Package metadata still requires Nix.

This op also emits output artifacts:
- `stdout.jsonl`
- `stderr.txt`

## Inputs

Common fields:
- `prompt` (required): prompt sent to Codex.
- `instructions`: additional context for a newly created session; ignored when resuming.
- `output.schema`: JSON Schema enforced by the op for a task-specific response.
- `session`: the complete `c2ops.codex.session/v1` object from a prior invocation.
  Omit it to start fresh; pass a complete `${{ ... }}` value to resume that exact
  checkpoint. Null, legacy `sessionId`, and `resume_context` inputs are rejected.
- `model`: Codex model override.
- `env`: extra environment variables.
- `worktree_path`: defaults to `{{ context.environment.op.worktree_path }}`.
- `workdir_path`: defaults to `{{ context.environment.op.workdir }}`.
- `artifact_inbox_path`: defaults to `{{ context.environment.op.inbox }}`.
- `artifact_outbox_path`: defaults to `{{ context.environment.op.outbox }}`.

These paths are resolved by the extension manifest. Recipes should omit the
inputs unless they need an explicit override. The resolved worktree is required
by the Codex implementation, but callers do not need to supply it themselves.

Skill-related fields:
- `skill`: required only by `codex/run_skill`, selecting the requested skill.
- `skills`: list of skill source refs in format `<host>/<org>/<repo>/<skills-root-path>@<git-ref>`.
- `return_on`: checkpoint statuses that should cause `incomplete` return.
- `status_contract.path`: outbox-relative status JSON path (for example `implementation/latest-status.json`).

Notes:
- `skills` is for installing skill bundles.
- `skill` is for selecting/enforcing one top-level skill segment.
- `skill_artifacts` and `skill_blobs` are not supported.
- Omit op sandbox configuration as c2j removes that support. The packaged c2ops adapter invokes the Codex CLI directly.
- Use `context.environment.op.*` for paths passed to Codex prompts or path inputs.
- c2j no longer exposes a separate cell path. The current cell is rooted at `context.environment.op.worktree_path`; repo-relative paths in prompts should be relative to that root.
- For the path contract, see `../OP_VISIBLE_PATHS_USER_GUIDE.md`.

## Skill Source Resolution

When `skills` refs are provided, c2ops `codex`:
1. Resolves each ref to a concrete commit.
2. Fetches/checks out repository content for that commit.
3. Copies all subdirectories under the referenced skills root into the invocation skill staging area.
4. Emits resolved refs in `skills_installed` output.

Skills and credentials are invocation configuration, not session contents.
Supply needed skill sources on every call. Local skills reside in `.agents/skills`.
Session objects exclude credentials, config.toml, and installed skills.

## Example: Basic

```yaml
- id: run_codex
  op: nix:github:colony-2/c2ops/published#codex
  inputs:
    prompt: "Summarize the changes in this repo."
```

## Example: Skill Sources via Git Refs

```yaml
- id: run_codex_skill
  op: nix:github:colony-2/c2ops/published#skill-run
  inputs:
    prompt: "Use my-skill."
    skill: "my-skill"
    skills:
      - "github.com/acme/codex-platform-skills/.agents/skills@platform-v12"
      - "github.com/acme/payments-cell-skills/.agents/skills@main"
```

## Structured Results

Supply the task's JSON Schema through `output.schema`. On success, consume the
typed `response` and require `output_schema_valid: true`. The execution envelope
(`status`, `session`, and related fields) remains separate. Do not paste the schema
into the prompt or run a second schema validator over a JSON artifact. Recipe-level
checks still enforce routing, artifact existence, and authorization semantics.

The shared kernel pins
`git+https://github.com/colony-2/c2ops.git//codex@5166aec516e5a1958601121d5a3753072acf8dd3`,
which supports `instructions` and `output.schema`; use a revision or published
package containing that contract. See [agent-turn.yaml](../../recipes/kernel/agent-turn.yaml).

## Test Mocks

State-machine selector-backed ops appear in c2j mock diagnostics with the selector in the node path:

```yaml
node_path: "job-implement/new_session/nix:github:colony-2/c2ops/published#codex"
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
- `response`: task-specific structured result when `output.schema` is supplied.
- `output_schema_valid`: whether that response satisfied the supplied schema.
- `session`: immutable continuation object; absent on failed ops.
- `sessionId`: diagnostic conversation ID; never a checkpoint key.
- `assistantSummary`
- `incompleteReason`
- `incompleteCategory`
- `pendingDependencies`
- `skills_installed`: resolved refs in input-compatible format (`...@<resolved-commit>`)
- `outcome` (structured checkpoint/skill/routing metadata)

Execution metadata example (the full op output also includes its opaque `session` object):

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

## Development workspace

Build and consultation use the native managed worktree root. A task's target
directory is supplied as context and does not redefine cell ownership. Consultation
and planning use read-only ops; implementation uses the same helper's mutating
branch. Session checkpoints preserve dialogue, not Git state; native workspaces
and snapshots carry the candidate separately.

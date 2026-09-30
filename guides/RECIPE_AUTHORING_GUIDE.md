# Recipe Authoring Guide

This is the default recipe-authoring workflow for this repo.

Author recipes locally, then validate them by submitting the recipe file directly with `c2j submit --run --embed`. That path exercises the same durable runtime model the real job uses without a separate registry step.

## 1. Keep the Execution Model Straight

Recipes orchestrate ops. Ops do not run inside your interactive shell session just because you authored the YAML locally.

Treat each op as a remote durable step:

- pass structured data through `inputs`
- pass files between steps through `artifacts`
- read/write task-local files through `context.environment.op.worktree_path`, `context.environment.op.inbox`, and `context.environment.op.outbox`
- export anything later nodes need through the enclosing node's `outputs:`

The most common authoring mistake is assuming a later step can read a path written by an earlier step without artifact plumbing. It cannot.

Keep these references open while authoring:

- `NODE_SCOPE_SPEC.md`
- `TEMPLATE_REFERENCE_CHEATSHEET.md`
- `template_resolution.md`
- `RECIPE_ARTIFACTS_REFERENCE.md`
- `TASK_EXECUTION_CONTEXT_REFERENCE.md`

## 2. Pick the Right Op

Start with the smallest op that matches the job:

- `command_execution`: bounded shell commands against the task worktree or inbox/outbox
- c2ops `llm2` selector: schema-constrained model calls and lightweight tool/file reasoning
- c2ops `codex` selector: multi-step agentic coding or review work
- c2ops `gha` / `gha-many` selectors: reuse existing GitHub Actions workflows instead of rebuilding them in shell
- `recipe.run_and_get_result` / `recipes.run*`: delegate work to child recipes
- `input`: explicit human approval or structured user input
- `thinpackrebase` / `squashrebasemerge`: integrate git changes back to the base repo
- extension ops: package repo-specific behavior behind a stable op interface

Use `ops/README.md` as the entrypoint to the per-op guides.

## 3. Default Authoring Loop: `c2j submit --run --embed`

### Confirm cell resolution

`c2j submit` targets the current cell by default. That works when the repo has a usable `.c2j/config.yaml`.

Useful commands:

```bash
c2j self
c2j cells
c2j init --stdout
```

If the current directory does not resolve cleanly as a cell, either:

- create or update `.c2j/config.yaml`, or
- pass `--cell <repo-or-path>` explicitly on submit

### Submit the recipe file directly

For day-to-day authoring, prefer `--recipe-file` over named recipe indirection:

```bash
c2j submit \
  --recipe-file ./recipes/my-recipe.yaml \
  --run \
  --embed
```

If the recipe needs inputs:

```bash
c2j submit \
  --recipe-file ./recipes/my-recipe.yaml \
  --inputs-file ./recipes/test-inputs.yaml \
  --run \
  --embed
```

What this gives you:

- local recipe-file authoring
- submission validation
- immediate execution
- a live job story in the terminal
- no dependency on a separately managed runtime

If the job pauses and you want to continue the same submission later:

```bash
c2j run one --embed --job-id <job-id>
```

To find recent job IDs for the current cell:

```bash
c2j list --self --embed
```

## 4. Author for Remote Ops, Not for Your Laptop

Most of the friction in recipe authoring comes from forgetting that op execution is isolated and durable.

Write recipes with these rules:

- use `context.environment.op.worktree_path` when an op process needs the repo checkout
- use `context.environment.op.inbox` and `context.environment.op.outbox` for paths read or written by an op process
- use `context.environment.host.*` only when you intentionally need the c2j worker host path
- use an `artifacts:` block only on ops that support inbox bindings
- pass the submitted `prompt` input directly in LLM prompts when needed; do not write it to a file just to re-read it
- do not paste file contents into LLM prompts; bind files into the op inbox and tell the LLM the inbox path to read
- use artifact set bindings such as `submitted/: '${{ context.artifacts }}'` when an op needs a whole submitted or node-produced artifact set
- use `${{ ... }}` for raw CEL values when a field expects a list, map, boolean, or number
- use `json_parse(...)` when consuming `llm2` responses produced under `response_schema`
- guard optional values with `has(...)` before indexing or dereferencing

For c2ops `codex`, use `git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572` to use the validated object-session contract. Pin `codex/run_skill` to the same revision. Its manifest supplies these op-visible path defaults automatically; omit them from recipe inputs unless intentionally overriding a path:

- `worktree_path: "{{ context.environment.op.worktree_path }}"`
- `workdir_path: "{{ context.environment.op.workdir }}"`
- `artifact_inbox_path: "{{ context.environment.op.inbox }}"`
- `artifact_outbox_path: "{{ context.environment.op.outbox }}"`

c2j no longer has a separate cell path. The current cell is rooted at `context.environment.op.worktree_path`, so repo-relative prompts and validation commands should resolve from that root.

For live local smoke recipes that should avoid the c2j extension wrapper sandbox, add:

```yaml
sandbox:
  type: none
```

The pinned c2ops Codex adapter invokes Codex directly when the extension sandbox is disabled and uses c2j's op-visible path context when sandboxing is enabled.

Do not hard-code `/src/inbox` or `/src/outbox` in Codex prompts. Recipes should reference:

- `{{ context.environment.op.inbox }}` for input artifacts
- `{{ context.environment.op.outbox }}` for output artifacts

See `../OP_VISIBLE_PATHS_USER_GUIDE.md` for the op-visible and host-visible path contract.

For child-job results, export earlier evidence explicitly through the root recipe's
`outputs.artifact_refs` map. Composite nodes otherwise return their final node's
artifacts; a final merge does not republish earlier verification files. Build and
evolve forward the verification artifact references through their shared
development recipe, preserving the originating job/task keys. The awaiting
parent receives these references in the child result's `artifacts` map and can
bind them into its dependency inbox. Child Git snapshots remain references and
do not replace the parent's working state.

## 5. Validation Levels

Use the fastest tool that answers the question you have:

1. `c2j submit --recipe-file ... --run --embed`
   Use this first. It is the default manual validation path for recipe authoring.
2. `c2j run one --embed --job-id ...`
   Use this when continuing an existing blocked or partially completed run.
3. `c2j test ...`
   Use this only when you need curated suites, mocks, repeated cases, or artifact assertions. See `RECIPE_TESTING_CLI_USER_GUIDE.md`.

## 6. Recommended References

- authoring workflow: `RECIPE_STARTER_GUIDE.md`
- op index: `ops/README.md`
- sequence semantics: `SEQUENCE_GUIDE.md`
- state-machine semantics: `STATE_MACHINE_GUIDE.md`
- template and scope rules: `NODE_SCOPE_SPEC.md`, `TEMPLATE_REFERENCE_CHEATSHEET.md`, `template_resolution.md`
- artifacts and runtime paths: `RECIPE_ARTIFACTS_REFERENCE.md`, `TASK_EXECUTION_CONTEXT_REFERENCE.md`

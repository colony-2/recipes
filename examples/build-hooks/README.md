# Build hooks

Start with the [build hooks user guide](../../guides/BUILD_HOOKS_USER_GUIDE.md)
for setup, configuration, permissions, and testing.

Copy the hooks you need into `.c2/recipes/hooks/build/` in the consuming repository.
The shared build invokes them with `cell://`; these example files are not discovered
by filename alone. Replace example commands with your repository's commands.

- `configure.yaml` adds phase guidance, named values, and required security assessments.
- `before_design.yaml` runs research before each design round. Emit findings in the
  outbox and export their references in `artifact_refs` to supply them to the designer.
- `prepare.yaml` may change checked-in files before assessment and review.
- `verify.yaml` explicitly invokes an existing script. Missing scripts fail this hook.
- `verify-gha.yaml` is an alternative verify hook for an existing dispatchable CI workflow.
- `publish.yaml` runs after merge, using the exact merged commit. It relies on normal
  c2j durability and failure handling. Grant publishing capabilities to this hook only.

Declare tools using `execution_needs` and export named outbox reports explicitly.
Do not assume separate ops share installed tools or temporary files. Scripts are
examples of explicit choices, not a new discovery convention.

For an existing GitHub Actions workflow, replace the verify command with c2ops
`gha` or `gha-many`, wait for completion, and map its result to `passed` or `failed`.
See [the GitHub Actions op guide](../../guides/ops/OP_GITHUB_ACTIONS.md) for the
workflow-dispatch, local execution, credential, and candidate requirements.

The [build hook specification](../../guides/PROPOSAL_BUILD_RECIPE_HOOKS.md) describes
all inputs, results, configuration, checkpoint ordering, and permissions.

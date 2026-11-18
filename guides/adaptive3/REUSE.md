# Reusing adaptive3 activities

Use the normal build submission for a development assignment. Use a consultation
request for another owner's advice. These paths already provide cell workspaces,
validation, human decisions and recovery.

A small diagnostic job can run a specific check. Give it a title describing the
check and return a short explanation of what it found. A diagnostic that records
an import failure has completed its investigation; it has not repaired Python.
An acceptance check must fail when its required behavior fails.

## Including an activity from another repository

c2j trusts explicit secret inputs authored in the root recipe repository. Including
a recipe from another repository requires the caller to authorize its secret
inputs. An optional secret reference still needs authorization.

For example, this call authorizes the model input used by a read-only advice cycle:

```yaml
- id: advice
  include: git+https://github.com/colony-2/recipes.git//recipes/adaptive3/cycle.yaml@main
  perms:
    jobdb:
      secrets:
        resolve: [codex_api_key]
  inputs:
    purpose: advice
    request: Explain how saved drafts survive a restart.
```

The caller must handle the returned `result.status`, including `stuck`, and any
failure at the include boundary. Use the existing containing lifecycle/Backstop
when building a development workflow. `execute.yaml` alone is an internal activity;
it does not supply the surrounding correction and recovery behavior.

This grant authorizes the included recipe's model input. It does not automatically
grant every task permission to fetch the secret by name. It cannot override an
enclosing ceiling. Other capabilities, such as submitting jobs, need an appropriate
caller policy; do not copy this limited advice example as a complete build policy.
Use c2j's [node-permission guide](https://github.com/colony-2/c2j/blob/main/GUIDE-Node-Permissions.md)
for inheritance, ceilings and Git-profile behavior.

The native [reuse tests](../../recipe-tests/adaptive3/reuse-permissions.test.yaml)
create a distinct recipe repository and test trusted-root input resolution,
authorized and denied includes, a denied ceiling and a foreign operation default.
They use synthetic secrets and the actual permission evaluator. No production
secret or runtime implementation is changed.

## Continuing a saved development workspace

Prefer ordinary build submission, retaining the intended target cell and saved
workspace:

```sh
c2j submit 'Continue the accepted implementation.' --cell TARGET --from-workspace
```

When a recovery needs a native preflight or rebase before build, author its
one-off caller beside `build.yaml` in an **isolated Recipes checkout**. Include
build relatively and omit the include's permission override:

```yaml
schema_version: 2
id: continue-work
input_schema:
  prompt:
    type: string
    required: true
inputs:
  prompt: ${{ inputs.prompt }}
sequence:
- id: continue_build
  include: ./build.yaml
  inputs:
    prompt: ${{ inputs.prompt }}
outputs:
  result: ${{ sequence.continue_build.outputs }}
```

Put any necessary native prelude before `continue_build`. For durable execution,
the caller, build and required Recipes helpers must be available together at a
source ref readable by the workers. A saved application snapshot or unpublished
recipe commit does not make that source fetchable. From the task holding the
recovered application workspace, select that source as the root:

```sh
c2j submit 'Continue the accepted implementation.' --cell TARGET \
  --advanced-recipe 'git+https://github.com/colony-2/recipes.git//continue-work.yaml@SOURCE_REF' \
  --from-workspace
```

Use `--from-workspace-now` when the task's current edits, rather than its incoming
snapshot, belong in that continuation. The recipe source checkout and the target
application workspace serve different purposes. Keep the caller and Recipes
sources out of the application candidate; moving the caller must not change its
target cell or recovered workspace. Do not manufacture recipe-source metadata.

For embedded validation, a disposable Git checkout can supply a `git+file://`
source instead. A task-local path is not a durable source for remote workers.
Use normal build submission when no such source ref is available; perform any
necessary preparation in the managed application workspace first.

Do not substitute `--advanced-recipe-file` for the complete-build example on the
current runtime. Its relative includes pass permission validation, but the review
helper's relative operation selector resolves against the application repository,
where `recipes/review-v2/op.yaml` is absent. The complete fixture selects a Git
root so helpers retain the Recipes source without adding them to the candidate.

A local wrapper including a hosted Recipes Git selector crosses a source
boundary, even when submitted by an existing Recipes job. Simply deleting its
`perms` block fails foreign-include validation. Moving the caller beside Recipes
while retaining that hosted selector also fails: switch to the relative include.

Within one source, omission retains trusted model inputs and automatic Git
credentials selected for each task. Ordinary tasks use the configured read
profile; native publication uses the configured write profile unless an enclosing
explicit selection overrides it. A list copied from read-only advice can allow
the model and checkout while excluding a distinct publication credential.
Avoid replacing those defaults with a deployment-specific secret inventory.

Omission cannot clear an earlier explicit grant or an enclosing ceiling. Secret
limits, submission denials and cell scopes still apply; unrelated secrets and
cell creation are not granted by default. Child jobs use their own root policies.
If a foreign include must remain, consult its owner about explicit authority for
its entire lifecycle; the limited advice grant above cannot cover a full build.

A captured recipe retains its declarations. Approval, retry or restart does not
amend its grants. Prepare a corrected fresh submission for a still-affected job,
reusing useful saved work rather than retrying the unchanged restriction.

The reuse suite also runs this relative caller through the real build lifecycle
with scripted model and review decisions, input materialization, saved workspace
persistence and native local publication. A Git pre-push probe executes under a
separate native merge task to check actual read/write helper resolution with
distinct synthetic credentials. Its negative controls cover enclosing denials,
the original incomplete list, unrelated secrets, foreign omission and explicit
profile preservation. Local pushes alone would not establish credential access.

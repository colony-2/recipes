# Recipe CLI Guide

Use `c2j` for day-to-day recipe authoring in this repo.

## Recommended Authoring Loop: `c2j`

### Inspect current cell context

- `c2j self`
- `c2j cells`
- `c2j init --stdout`

`c2j submit` targets the current cell by default. If that does not resolve cleanly, create `.c2/config.yaml` or pass `--cell <registered-name>`.

### Submit and run a local recipe file

```bash
c2j submit "Run the local recipe" \
  --advanced-recipe-file ./recipes/my-recipe.yaml \
  --run \
  --embed
```

With additional inputs (the local recipe must declare the supplied inputs, including
`prompt`):

```bash
c2j submit "Run the local recipe" \
  --advanced-recipe-file ./recipes/my-recipe.yaml \
  --inputs-file ./recipes/test-inputs.yaml \
  --run \
  --embed
```

Useful follow-ups:

- `c2j list --self --embed`
- `c2j run one --embed --job-id <job-id>`

Practical notes:

- `--embed` uses the embedded SWF runtime and is the fastest local feedback loop.
- `--advanced-recipe-file` is the right choice while authoring because it runs the local yaml directly.
- `--advanced-recipe` can target a named recipe or selector when you do want runtime resolution.

## Agent task discovery (c2j main f1a153b898c5)

Run `c2j self` at task start and recheck after a lease or permission failure.
The action table separates permission from availability; follow its routes and
inherited child restrictions. A ready action can still fail for a particular
request. Outside a task, authority is unknown rather than implicitly unrestricted.
See the [current self contract](https://github.com/colony-2/c2j/blob/main/README.md#c2j-self).

A task can authorize job submission, including to another cell. Child identities
are automatically included in task outputs; do not make the agent reconstruct
that list. Recipes still decide whether to await validation children or use the
serving-work coordinator. Discovery does not expand task authorization.

### Recipe source and workspace snapshots

Check `c2j self` and `c2j submit --help` for the installed version's supported
inputs and task route. Within an agent task, use its reported submission route
rather than assuming the embedded route above applies.

Recipe definitions and the workspace being tested are separate inputs. A saved,
unpushed commit is not automatically fetchable from GitHub. A failed Git recipe
selector does not establish that local execution is unsupported.
`--advanced-recipe-file` supplies the actual local recipe definition.
`--from-workspace` selects the task's incoming workspace snapshot;
`--from-workspace-now` selects current commits and file contents. Neither workspace
flag alone packages the recipe definition or its includes. Check local include
resolution separately when the recipe uses includes.

For example, to test a newly authored local recipe against current workspace files
through the task's authorized route:

```bash
c2j submit "Run the local recipe" --advanced-recipe-file ./recipes/my-recipe.yaml --from-workspace-now --run
```

Use `--from-workspace` instead when testing the incoming snapshot, if that snapshot
is available to the task. Validate the
chosen combination with a small unpublished recipe and an observable workspace
change before retrying the larger job. A fixture whose definition is already
published does not test whether newly authored local definitions can be supplied.

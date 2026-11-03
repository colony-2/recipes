# Recipe CLI Guide

Use `c2j` for day-to-day recipe authoring in this repo.

## Recommended Authoring Loop: `c2j`

### Inspect current cell context

- `c2j self`
- `c2j cells`
- `c2j init --stdout`

`c2j submit` targets the current cell by default. If that does not resolve cleanly, create `.c2/config.yaml` or pass `--cell <repo-or-path>`.

### Submit and run a local recipe file

```bash
c2j submit \
  --recipe-file ./recipes/my-recipe.yaml \
  --run \
  --embed
```

With inputs:

```bash
c2j submit \
  --recipe-file ./recipes/my-recipe.yaml \
  --inputs-file ./recipes/test-inputs.yaml \
  --run \
  --embed
```

Useful follow-ups:

- `c2j list --self --embed`
- `c2j run one --embed --job-id <job-id>`

Practical notes:

- `--embed` uses the embedded SWF runtime and is the fastest local feedback loop.
- `--recipe-file` is the right choice while authoring because it runs the local yaml directly.
- `--recipe` can target a named recipe or selector when you do want runtime resolution.

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

The current CLI submits custom local recipes with
`c2j submit --advanced-recipe-file <file> --run --embed`. Check `submit --help`
when using older documentation that spells this flag `--recipe-file`.

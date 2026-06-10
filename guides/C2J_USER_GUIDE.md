# Recipe CLI Guide

Use `c2j` for day-to-day recipe authoring in this repo.

## Recommended Authoring Loop: `c2j`

### Inspect current cell context

- `c2j self`
- `c2j cells`
- `c2j init --stdout`

`c2j submit` targets the current cell by default. If that does not resolve cleanly, create `.c2j/config.yaml` or pass `--cell <repo-or-path>`.

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

---
title: "Quickstart"
weight: 11
---

The default local authoring loop is:

```bash
c2j self
c2j submit --recipe-file docs/examples/recipes/hello-command.yaml --run --embed
```

`c2j submit --recipe-file ... --run --embed` loads the local YAML file, embeds the recipe into the job, starts the embedded SWF runtime, submits the job, and immediately runs it.

Check the exact binary first:

```bash
c2j version
```

Inspect how the current cell resolves:

```bash
c2j self
c2j cells
```

Pass inputs with JSON:

```bash
c2j submit \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --inputs-json '{"name":"C2"}' \
  --run \
  --embed
```

Pass an inputs file:

```bash
c2j submit \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --inputs-file docs/examples/inputs/hello.yaml \
  --run \
  --embed
```

Continue a previously submitted job:

```bash
c2j list --self --embed
c2j run one --job-id <job-id> --embed
```

Use `c2j test` when the recipe needs repeatable assertions, mocks, or artifact checks:

```bash
c2j test validate \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --file docs/examples/tests/hello-command.scenario.md
```


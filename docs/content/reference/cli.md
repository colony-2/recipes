---
title: "CLI"
weight: 41
---

Installed reference version:

```bash
c2j version
# c2j version v0.0.36
```

Current command tree:

```bash
c2j self
c2j cells
c2j init
c2j version
c2j submit
c2j run one
c2j run any
c2j run loop
c2j ready
c2j list
c2j test compile
c2j test validate
c2j test run
c2j test case validate
c2j test case run
```

Submit and run a local recipe file:

```bash
c2j submit --recipe-file docs/examples/recipes/hello-command.yaml --run --embed
```

Submit with inline inputs:

```bash
c2j submit \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --inputs-json '{"name":"C2"}' \
  --run \
  --embed
```

Submit with attached artifacts:

```bash
c2j submit \
  --recipe-file ./recipes/review-docs.yaml \
  --artifact ./brief.md \
  --artifact requirements=./requirements.md \
  --run \
  --embed
```

Useful mutual exclusions:

- `--recipe` and `--recipe-file`
- `--inputs-json` and `--inputs-file`
- `--json` and `--run`
- `--self` and `--cell`

Run or continue:

```bash
c2j run one --job-id <job-id> --embed
c2j run --job-id <job-id> --input-mode fail --embed
c2j run --job-id <job-id> --ci --embed
```

List jobs:

```bash
c2j list --self --embed
c2j list --self --json --embed
```

Embedded runtime:

- `--embed` is shorthand for `--swf-url embed:///`.
- `C2J_EMBED_ROOT` overrides the embedded runtime root.
- The root must be absolute.
- Use separate roots for parallel embedded runtimes.


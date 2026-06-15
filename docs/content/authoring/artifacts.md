---
title: "Artifacts"
weight: 35
---

Artifacts are named files or artifact references that move between durable steps.

There are three common flows:

1. A submitted local file becomes a job artifact with `c2j submit --artifact`.
2. A step writes a file under `context.environment.op.outbox`.
3. A later step binds an artifact into `context.environment.op.inbox`.

Artifact handoff example:

{{< example "examples/recipes/artifact-handoff.yaml" >}}

Submit local artifacts:

```bash
c2j submit \
  --recipe-file docs/examples/recipes/artifact-consumer.yaml \
  --artifact brief=./brief.md \
  --run \
  --embed
```

Bind a submitted artifact:

```yaml
artifacts:
  brief.md: '${{ context.artifacts["brief"] }}'
```

Bind an artifact produced by an earlier sequence node:

```yaml
artifacts:
  report.json: '${{ sequence.generate.artifacts["report.json"] }}'
```

Binding names must be relative paths and cannot contain `..`. If a binding name ends with `/`, c2j appends the artifact's file name.

Use raw CEL expressions for artifact keys so the type is preserved:

```yaml
artifact: '${{ sequence.generate.artifacts["report.json"] }}'
```

Composite scope rule: if a nested sequence or state produces an artifact that an outer node needs, export the artifact key through the nested node's `outputs`.


---
title: "Inline Includes"
weight: 36
---

`include` composes another recipe file into the current job. It does not start a child job.

Use includes when a workflow should be split into reusable files but still execute as one expanded recipe.

Parent:

{{< example "examples/recipes/include-parent.yaml" >}}

Child:

{{< example "examples/recipes/include-child.yaml" >}}

Syntax:

```yaml
- id: verify
  include: ./verify.yaml
  inputs:
    plan: '${{ sequence.plan.outputs.plan }}'
```

```yaml
- id: verify
  include:
    recipe: ./verify.yaml
  inputs:
    plan: '${{ sequence.plan.outputs.plan }}'
```

Rules:

- Relative includes resolve from the including recipe file.
- The included recipe's `input_schema` is enforced at the include boundary.
- Included root recipes should declare explicit `outputs`.
- Current include support is for sequence and state roots; wrap root ops in a sequence if needed.
- The expanded snapshot is what the job executes and replays.

Includes may appear inside state machines. In a transition after an include, `outputs` refers to the included recipe outputs.


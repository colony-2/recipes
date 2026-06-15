---
title: "Sequences"
weight: 32
---

A `sequence` runs child nodes in order. Later children can read earlier sibling outputs through `sequence.<id>.outputs` and artifacts through `sequence.<id>.artifacts`.

Example with artifact handoff:

{{< example "examples/recipes/artifact-handoff.yaml" >}}

Sequence rules:

- Child IDs become keys in the `sequence` scope.
- Sibling references only see completed earlier siblings.
- A nested sequence must export values with its own `outputs` map before an outer node can read them.
- Composite sequence artifacts come from the final child; export specific inner artifacts through outputs when downstream nodes need them.

Use a sequence when the work is a deterministic pipeline. Use a state machine when the next node depends on runtime outputs.


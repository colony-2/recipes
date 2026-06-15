---
title: "Recipe Files"
weight: 31
---

A recipe file has metadata, optional input schema, optional normalized root inputs, and one root node.

The root node can be:

- `op`
- `sequence`
- `state`
- `child_group`

Intermediate nodes can also use `include` and `shared` references after resolution.

Minimal sequence recipe:

{{< example "examples/recipes/hello-command.yaml" >}}

Important fields:

- `id`: stable recipe identifier.
- `version`: author-controlled recipe version.
- `desc`: human-readable description.
- `input_schema`: validates submitted inputs and applies `default_value`.
- `inputs`: normalizes submitted values for the root node.
- `outputs`: exports recipe result values.

Supported `input_schema` types in current `c2j` are `string`, `number`, `boolean`, `artifact`, and `artifact_map`.

Use optional-safe access for inputs that may be absent:

```yaml
inputs:
  mode: '${{ first_nonempty(inputs.?mode, "auto") }}'
```

Use raw CEL expressions when the target field should stay a map, list, boolean, number, or artifact key:

```yaml
inputs:
  parsed: '${{ json_parse(inputs.payload_json) }}'
```

Use Go-style string interpolation for ordinary strings:

```yaml
inputs:
  label: "ticket {{ inputs.ticket_id }}"
```


---
title: "Scope And Templates"
weight: 34
---

c2j supports two template systems in string fields:

- CEL interpolation: `${{ ... }}`
- Go template interpolation: `{{ ... }}`

Use one raw CEL expression when the field needs a non-string value:

```yaml
value: '${{ sequence.fetch.outputs.count }}'
artifact: '${{ sequence.write.artifacts["report.json"] }}'
items: '${{ json_parse(sequence.fetch.outputs.stdout).items }}'
```

Use interpolation inside a larger string for strings:

```yaml
message: "Ticket ${{ inputs.ticket_id }} is ready"
message: "Ticket {{ inputs.ticket_id }} is ready"
```

`when` fields are pure CEL. Do not wrap them:

```yaml
when: sequence.validate.outputs.ok == true
```

Scope rules:

| Container | Reads | Sibling Namespace | Export |
| --- | --- | --- | --- |
| `op` | mapped `inputs` | none | op outputs and artifacts |
| `sequence` | container `inputs` | `sequence.<id>` | `outputs` map |
| `state` | container `inputs` | `states.<id>` | `outputs` map |
| `include` | callsite `inputs` | callsite ID in parent scope | included recipe `outputs` |
| `child_group` | container `inputs` and child specs | group output | group `outputs` |

Common helpers:

- `json_parse(str)`: parse JSON text to a map/list.
- `json_stringify(value)`: JSON encode in CEL.
- `jq(value, expr)`: query structured data with jq.
- `first_nonempty(a, b, ...)`: choose the first non-empty value.
- `nonempty(value)`: true when a value is present and not empty.
- `state_output(id, field, default)`: read a state output safely.
- `state_exists(id)`: true when a state has run.
- Optional access: `inputs.?mode.orValue("auto")`.

Keep jq programs static when possible. Pass dynamic data as the jq input value rather than building jq source strings from recipe inputs.


# jq and JSON Template Helpers

`jq` remains available in the default c2j template function registry. It does not need a recipe-level extension-function import for normal recipe templates.

Use either form:

```yaml
name: "${{ jq(inputs.payload, '.user.name') }}"
tags: "${{ inputs.payload.jq('.tags[]') }}"
```

## Recommended Pattern

Keep jq programs static and pass recipe context as data:

```yaml
recipes: >-
  ${{
    jq(
      json_parse(
        '{"current_cell":' +
        json_stringify(context.workflow.cell) +
        ',"items":' +
        json_stringify(inputs.items) +
        '}'
      ),
      '. as $root | ($root.current_cell // "") as $cell | ($root.items // []) | map(select(.target_cell != $cell))'
    )
  }}
```

That avoids building jq source code with CEL string concatenation and keeps quoting predictable.

## Helper Summary

- `json_parse(str)` turns JSON strings into maps/lists.
- `json_stringify(value)` emits a JSON string from CEL.
- `to_json(value)` emits a JSON string from Go templates.
- `jq(value, expr)` returns `null` for empty output, a scalar for one output, and a list for multiple outputs.

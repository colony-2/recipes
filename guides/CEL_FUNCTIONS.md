# CEL + Template Helper Functions

## `cells()`
- Available in Cortex via the function registry.
- Returns a list of maps, each with keys: `name`, `id`, `path`, `description`.
- CEL example: `cells()[0].name` yields the first cell's name; you can filter with CEL list ops, e.g. `cells().exists(c, c.name == "my-cell")`.
- Go template example: `{{ cells | to_json }}` renders the same value as JSON for prompts/log text.

Notes:
- The function is zero-argument and pulls from the cell service at evaluation time.
- Output items are plain maps for portability; fields are `string`-typed.
- Local `c2j test` does not currently register this runtime provider. For c2j-local recipes, use `command_execution` to run `c2j cells --json` and mock that command node in tests.

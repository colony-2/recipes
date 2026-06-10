# Bug Report: `c2j test validate/run` Cannot Resolve Local Inline Includes

## Summary

`c2j submit --recipe-file ... --run --embed` resolves and executes local
`include` recipe nodes correctly, but local recipe tests do not preserve enough
source context for relative includes.

Observed behavior:

- `c2j test compile` succeeds, but the compiled target recipe content still
  contains unresolved `include: ./child.yaml`.
- `c2j test validate` and `c2j test run` fail before execution with:

```text
target_recipe.content: resolve include "./child.yaml" at root/<node>:
relative include "./child.yaml" has no local recipe directory
```

The inline recipe user guide says recipe tests resolve includes and hash the
expanded snapshot, so local recipe tests should preserve the root recipe file
directory when resolving relative includes.

## Version

Observed with:

```text
c2j version v0.0.29-0.20260610192916-daa785933f7d
/usr/local/bin/c2j sha256 7a21a33b413c65c2bbb4933d45d820b4db2efae1258eb62ca9fd7a791c1ed331
```

## Minimal Reproduction

Create `parent.yaml`:

```yaml
id: parent
version: "1.0"
input_schema:
  prompt:
    type: string
    required: true
inputs:
  prompt: "{{ inputs.prompt }}"
sequence:
  - id: child
    include: ./child.yaml
    inputs:
      prompt: "{{ inputs.prompt }}"
outputs:
  message: "{{ sequence.child.outputs.message }}"
```

Create `child.yaml` in the same directory:

```yaml
id: child
version: "1.0"
input_schema:
  prompt:
    type: string
    required: true
inputs:
  prompt: "{{ inputs.prompt }}"
sequence:
  - id: echo
    op: command_execution
    inputs:
      timeout: 30s
      run: |
        printf '{"message":"%s"}\n' "{{ inputs.prompt }}"
outputs:
  message: '${{ json_parse(sequence.echo.outputs.stdout).message }}'
```

Create `parent.scenario.md`:

````markdown
```yaml
cases:
  - id: parent-inline
    type: recipe_case
    inputs:
      prompt: hello
    mocks:
      ops:
        - match:
            op: command_execution
          behavior:
            mode: passthrough
    assertions:
      - type: output_equals
        path: message
        value: hello
```
````

Run:

```bash
c2j test compile \
  --recipe-file ./parent.yaml \
  --file ./parent.scenario.md \
  --out /tmp/parent.compiled.json \
  --strict

c2j test validate \
  --recipe-file ./parent.yaml \
  --file ./parent.scenario.md \
  --parallelism 1

c2j test run \
  --recipe-file ./parent.yaml \
  --file ./parent.scenario.md \
  --parallelism 1 \
  --artifact-mode inline \
  --out-dir /tmp/parent.run \
  --evaluation-mode enforce
```

## Expected Result

`compile`, `validate`, and `run` should all resolve `./child.yaml` relative to
`parent.yaml`.

Expected command behavior:

- `c2j test compile` should emit canonical IR whose target recipe no longer has
  unresolved local `include` nodes.
- `c2j test validate` should validate the expanded recipe graph.
- `c2j test run` should execute the expanded recipe graph and pass the
  `message == hello` assertion.

## Actual Result

`compile` succeeds, but the compiled target recipe still contains the authored
relative include. `validate` and `run` then fail before execution:

```text
target_recipe.content: resolve include "./child.yaml" at root/child:
relative include "./child.yaml" has no local recipe directory
```

The same failure occurs whether the root recipe file is passed as a relative or
absolute path:

```bash
c2j test run --recipe-file ./parent.yaml ...
c2j test run --recipe-file /absolute/path/to/parent.yaml ...
```

## Control Case

The same root recipe resolves and executes includes through embedded submit:

```bash
c2j submit \
  --recipe-file ./parent.yaml \
  --inputs-json '{"prompt":"hello"}' \
  --run \
  --embed
```

## Impact

Recipes can use local inline includes in normal embedded execution, but local
recipe scenario tests cannot validate or run those recipes directly. This
blocks production-recipe scenario tests for include-based recipes, forcing teams
to rely on phase recipe tests plus an embedded submit smoke until the test
runner preserves local recipe source context.

---
title: "Testing With c2j"
weight: 61
---

`c2j test` compiles, validates, and runs recipe test suites locally.

Commands:

```bash
c2j test compile
c2j test validate
c2j test run
c2j test case validate
c2j test case run
```

Validate one example:

```bash
c2j test validate \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --file docs/examples/tests/hello-command.scenario.md \
  --parallelism 1
```

Run with artifact capture:

```bash
c2j test run \
  --recipe-file docs/examples/recipes/hello-command.yaml \
  --file docs/examples/tests/hello-command.scenario.md \
  --parallelism 1 \
  --artifact-mode inline
```

Scenario Markdown format uses the first fenced YAML or JSON block:

{{< example "examples/tests/hello-command.scenario.md" "markdown" >}}

Mock precedence:

1. `node_path + op`
2. `node_path`
3. `op`
4. declaration order tie-break

Selector-backed op test pattern:

```yaml
mocks:
  ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: docs-rule-gate/gate
      behavior:
        mode: return
        outputs:
          ok: true
          failed_rule_ids: []
```

Supported suite formats:

- `canonical_yaml`
- `canonical_json`
- `compact_yaml`
- `scenario_md`

Run all example tests directly:

```bash
c2j test run --directory docs/examples/tests
```


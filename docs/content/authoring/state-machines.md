---
title: "State Machines"
weight: 33
---

A `state` machine chooses states with transitions. States can be ops, sequences, includes, or child groups.

Example with a switch transition table:

{{< example "examples/recipes/state-switch.yaml" >}}

Initial state forms:

```yaml
state:
  initial: validate
```

```yaml
state:
  initial:
    - to: validate
      when: inputs.enabled
    - to: skipped
      when: true
```

Transition forms:

```yaml
transitions:
  - to: pass
    when: outputs.exit_code == 0
  - to: fail
    when: true
```

```yaml
transitions:
  switch: json_parse(outputs.stdout).status
  cases:
    - value: ready
      to: process
    - value: blocked
      to: wait
  default:
    to: fail
```

Inside a state transition, `outputs` refers to the current state's outputs. Elsewhere, reference completed states with `states.<state-id>.outputs` or helper functions such as `state_output("state_id", "field", default)`.

Switch tables support string, boolean, and number case values. Nested switch tables are intentionally limited; use a command or rule gate to normalize complex decisions before routing.


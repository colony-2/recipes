---
title: "Primary Orchestration"
weight: 71
---

A primary ticket recipe should orchestrate. It should not do all work inline when a phase deserves its own durable boundary.

Recommended shape:

1. Triage the request and confirm the current cell owns it.
2. Produce requirements or a design artifact.
3. Produce test statements and acceptance criteria.
4. Delegate substantial implementation or review phases to child recipes.
5. Collect child outcomes and policy gates.
6. Summarize work and close or route the ticket.

Use `include` for same-job reusable phases:

```yaml
- id: design
  include: ./ticket-design.yaml
  inputs:
    prompt: "{{ inputs.prompt }}"
```

Use `child_group` for durable parallel reviews:

```yaml
- id: reviews
  child_group:
    mode: run_and_get_result
    children:
      - key: spec
        recipe: ticket-spec-review
        required: true
      - key: quality
        recipe: ticket-quality-review
        required: true
    aggregate:
      shape: review_pack
```

Use `rule_gate` to convert policy into routeable data instead of failing early:

```yaml
- id: gate
  op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
  inputs:
    rules:
      - id: review_passed
        type: assert
        value: '${{ sequence.reviews.outputs.ok }}'
        message: Required reviews must pass.
```


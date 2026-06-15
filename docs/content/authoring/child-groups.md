---
title: "Child Groups"
weight: 37
---

`child_group` starts multiple child recipes from one parent node. Use it for fan-out and fan-in across durable recipe jobs.

Basic shape:

```yaml
sequence:
  - id: reviews
    child_group:
      mode: run_and_get_result
      children:
        - key: spec
          recipe: ticket-spec-review
          required: true
          inputs:
            prompt: "{{ inputs.prompt }}"
        - key: quality
          recipe: ticket-quality-review
          required: false
          inputs:
            prompt: "{{ inputs.prompt }}"
      aggregate:
        shape: review_pack
outputs:
  ok: '${{ sequence.reviews.outputs.ok }}'
  blocking_issues: '${{ sequence.reviews.outputs.blocking_issues }}'
```

Child fields:

- `key`: stable child name inside the group.
- `recipe`: recipe ID or selector.
- `cell_name`: optional target cell.
- `git_ref`: optional child ref.
- `required`: failed required children make group `ok` false; optional failures become warnings.
- `when`: optional condition.
- `skip_reason`: recorded when skipped.
- `inputs`: child recipe input map.
- `artifacts`: child-specific artifact refs.

Dynamic fan-out:

```yaml
child_group:
  mode: run_and_get_result
  children_from: '${{ json_parse(inputs.plan_json).tasks }}'
  child:
    key: '${{ item.id }}'
    recipe: task-implementation
    required: true
    inputs:
      task_id: '${{ item.id }}'
      instructions: '${{ item.instructions }}'
```

Modes:

- `run_and_get_result`: start, wait, and aggregate child results.
- `start`: start children and return job IDs.

Use `child_group` for durable job boundaries. Use `include` when the work should stay in the same job.


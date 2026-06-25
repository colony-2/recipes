---
title: "Child Recipe Ops"
weight: 52
---

Child recipe ops start or inspect separate durable recipe jobs. Use them when the parent workflow needs an actual child job boundary: a different cell, an independently resumable phase, a long-running dependency, or a lifecycle decision that should be visible in job history.

Use `include` instead when the work should stay in the same job. Use `child_group` when the parent needs first-class fan-out/fan-in with required and optional child aggregation.

## Choosing An Op

| Op | Use When | Parent Failure Behavior |
| --- | --- | --- |
| `recipe.run_and_get_result` | Start one child, wait for it, and consume outputs. | Child failure fails the parent node. |
| `recipes.run` | Start one or more children and continue immediately with job IDs. | Start failures fail the parent node. Child completion is handled later. |
| `recipes.run_and_wait` | Start multiple children and wait for all terminal states, but do not need outputs. | Child failure fails the parent node. |
| `recipe.await_result` | Wait for one already-started child and consume outputs. | Child failure fails the parent node. |
| `recipe.await_result_soft` | Inspect or wait for one child and route on status as data. | Child failure is returned as structured output. |
| `recipe.get_result` | Fetch one child result that should already be available. | Missing or failed result fails the parent node. |

## Invocation Shape

`recipe.run_and_get_result` starts one child directly:

```yaml
name: child-recipe-name
cell_name: optional-target-cell
git_ref: '${{ has(context.git.hash) && context.git.hash != "" ? context.git.hash : context.git.ref }}'
inputs:
  prompt: "${{ inputs.prompt }}"
artifacts: '${{ context.artifacts.map(k, context.artifacts[k]) }}'
```

`recipes.run` and `recipes.run_and_wait` use shared op-level `git_ref` plus a `recipes` list:

```yaml
git_ref: '${{ has(context.git.hash) && context.git.hash != "" ? context.git.hash : context.git.ref }}'
recipes:
  - name: child-recipe-name
    cell_name: optional-target-cell
    inputs:
      prompt: "${{ inputs.prompt }}"
    artifacts: '${{ context.artifacts.map(k, context.artifacts[k]) }}'
```

`name` selects the child recipe. `inputs` is the child recipe input map. `artifacts` is the artifact set passed to the child job. `cell_name` and git defaults are inherited from the current job when omitted.

Child outputs are wrapped under `outputs.outputs` when consumed by direct child ops:

```yaml
outputs:
  child_summary: "{{ sequence.plan.outputs.outputs.summary }}"
```

Child job result artifacts are attached to the parent node artifacts:

```yaml
artifacts:
  report.md: '${{ sequence.plan.artifacts["report.md"] }}'
```

The parent cannot read arbitrary intermediate node outputs or artifacts from inside the child job. Export values through the child recipe `outputs`, and make parent-needed files part of the child job result artifact contract.

## One Child, Hard Boundary

Use `recipe.run_and_get_result` when the parent cannot continue unless the child succeeds:

```yaml
sequence:
  - id: plan
    op: recipe.run_and_get_result
    inputs:
      name: ticket-plan
      git_ref: '${{ has(context.git.hash) && context.git.hash != "" ? context.git.hash : context.git.ref }}'
      artifacts: '${{ context.artifacts.map(k, context.artifacts[k]) }}'
      inputs:
        prompt: "${{ inputs.prompt }}"

  - id: implement
    op: recipe.run_and_get_result
    inputs:
      name: ticket-implement
      git_ref: '${{ has(context.git.hash) && context.git.hash != "" ? context.git.hash : context.git.ref }}'
      artifacts:
        - '${{ sequence.plan.artifacts["plan.json"] }}'
      inputs:
        plan_summary: "{{ sequence.plan.outputs.outputs.summary }}"

outputs:
  implementation_status: "{{ sequence.implement.outputs.outputs.status }}"
```

## Start Now, Inspect Later

Use `recipes.run` when the parent should start child work and move on. Pair it with `recipe.await_result_soft` when the parent owns the routing decision for failure, timeout, or cancellation:

```yaml
sequence:
  - id: start_dependency
    op: recipes.run
    inputs:
      git_ref: '${{ has(context.git.hash) && context.git.hash != "" ? context.git.hash : context.git.ref }}'
      recipes:
        - name: new-ticket
          cell_name: api
          inputs:
            prompt: "Implement the API dependency for ${{ inputs.ticket_id }}"
          artifacts: []

  - id: inspect_dependency
    op: recipe.await_result_soft
    inputs:
      job_id: '${{ sequence.start_dependency.outputs.job_ids[0] }}'
      return_when: terminal
      timeout: 2h
      poll_interval: 30s

outputs:
  dependency_job_id: '${{ sequence.start_dependency.outputs.job_ids[0] }}'
  dependency_status: "{{ sequence.inspect_dependency.outputs.status }}"
  dependency_terminal: '${{ sequence.inspect_dependency.outputs.terminal }}'
  dependency_failure_kind: "{{ sequence.inspect_dependency.outputs.failure_kind }}"
```

Route on `sequence.inspect_dependency.outputs.status` or `failure_kind` in a state machine when failed child work should trigger replanning instead of failing the parent job.

## Multiple Children Without Aggregation

Use `recipes.run_and_wait` when all children must finish before the parent continues, but the parent does not need their outputs:

```yaml
- id: launch_checks
  op: recipes.run_and_wait
  inputs:
    git_ref: '${{ has(context.git.hash) && context.git.hash != "" ? context.git.hash : context.git.ref }}'
    recipes:
      - name: lint-cell
        cell_name: api
        inputs:
          target: api
        artifacts: []
      - name: lint-cell
        cell_name: web
        inputs:
          target: web
        artifacts: []
```

Prefer `child_group` for review/check fan-out that needs `required: false`, summaries, warnings, blocking issues, or a stable aggregate output shape.

## Result Fetching

`recipe.await_result` waits for a child job and fails if the child failed:

```yaml
- id: wait_for_child
  op: recipe.await_result
  inputs:
    job_id: '${{ sequence.start_child.outputs.job_ids[0] }}'
```

`recipe.get_result` only fetches an already-available result:

```yaml
- id: fetch_child_result
  op: recipe.get_result
  inputs:
    job_id: '${{ inputs.child_job_id }}'
```

Use `get_result` only when another part of the workflow has already established that the child is terminal and has a result.

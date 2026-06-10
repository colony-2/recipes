# Requirements: c2ops `rule_gate`

## Status

Covered by the c2ops `rule_gate` extension op.

Latest c2ops review found this selector:

```yaml
op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
```

## Motivation

Recipes need deterministic policy checks for artifacts, JSON schemas, child
statuses, and simple boolean assertions. Those checks should be separate from
LLM judgment and should emit structured data for recipe transitions.

## Current Surface

Supported rule types:

- `assert`
- `artifact_exists`
- `file_exists`
- `json_parse`
- `json_schema`
- `child_status`

Required inputs:

- `rules`

Defaulted path inputs:

- `artifact_inbox_path`
- `artifact_outbox_path`
- `worktree_path`

Outputs:

- `version`
- `ok`
- `failed_rule_ids`
- `summary`
- `results`

Policy failures return `ok=false` without failing the process. Invalid input or
infrastructure failure exits nonzero.

## Non-Goals

- Do not replace skill-based judgment or reviewer recipes.
- Do not run arbitrary long-lived implementation commands.
- Do not decide route names such as `revise_implementation`.
- Do not implement severity, waivers, warnings, or `next_action` inside the op.

Recipes should map `ok`, `failed_rule_ids`, and `results` to route decisions.

## Rule Examples

### Boolean Assertion

```yaml
- id: final_gate
  op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
  inputs:
    rules:
      - id: validation_passed
        type: assert
        value: "${{ states.validate.outputs.passed }}"
        message: Validation must pass before merge.
```

### Artifact Existence

Use `artifact_exists` when the policy only needs to know whether a previous
node published an artifact.

```yaml
- id: artifact_gate
  op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
  inputs:
    rules:
      - id: review_pack_artifact_exists
        type: artifact_exists
        artifact: "${{ states.review.artifacts['reviews/review-pack.json'] }}"
        message: Review pack artifact is required.
```

### JSON Parse And JSON Schema

Use artifact bindings plus `json_parse` or `json_schema` when the policy needs
to read artifact contents.

```yaml
- id: plan_gate
  op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
  artifacts:
    plan.json: "${{ states.planner.artifacts['plan.json'] }}"
  inputs:
    rules:
      - id: plan_json
        type: json_parse
        inbox_path: plan.json
        message: Plan must be valid JSON.
      - id: plan_schema
        type: json_schema
        inbox_path: plan.json
        schema:
          type: object
          required: [tasks]
          properties:
            tasks:
              type: array
        message: Plan must match the task-plan schema.
```

### Child Status

Use `child_status` for outputs from `recipe.await_result_soft` or
`child_group`.

```yaml
- id: child_gate
  op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
  inputs:
    rules:
      - id: task_child_completed
        type: child_status
        status: "${{ states.await_task.outputs }}"
        allow_statuses: [completed]
        message: Task child must complete before selecting the next task.
```

## Transition Pattern

Route from `ok` and failed rule IDs.

```yaml
transitions:
  - to: repair_plan
    when: '"plan_schema" in states.plan_gate.outputs.failed_rule_ids'
  - to: continue
    when: states.plan_gate.outputs.ok
```

## Acceptance Criteria

- `assert` policy failure returns `ok=false` with zero process failure.
- Invalid rule input fails the node.
- `artifact_exists` can check rendered recipe artifact refs.
- `json_parse` can parse inbox artifacts.
- `json_schema` can validate inbox artifacts against an inline schema.
- `child_status` can consume a soft child-status object.
- Recipe transitions can route using `ok`, `failed_rule_ids`, and `results`.

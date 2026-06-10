# Requirements: c2ops `run_skill`

## Status

Covered by the c2ops `codex/run_skill` extension op.

The latest c2ops checkout reviewed for this document exposes the selector:

```yaml
op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
```

The c2ops manifest name is `skill.run`, but recipe authors should use the
selector above unless c2j later provides a named alias.

## Motivation

Skill-backed recipes repeat a large amount of boilerplate for every c2ops
`codex` invocation:

- selector string;
- worktree, workdir, inbox, and outbox path inputs;
- skill bundle refs;
- `skill_mode: enforce`;
- status contract configuration;
- artifact path instructions;
- assistant summary parsing.

That makes recipes longer than the workflow they are trying to describe. Recipe
authors should be able to express "run this skill with these artifacts and this
contract" directly.

## Goals

- Make common skill execution compact and reviewable.
- Preserve the current c2ops `codex` skill behavior and outputs.
- Keep artifact inputs and output contracts explicit.
- Keep job stories clear about which skill and bundle revision ran.
- Make recipe tests easier to mock with a stable op surface.

## Non-Goals

- Do not add skill-internal subagent management.
- Do not replace recipes as the durable orchestration layer.
- Do not hide submitted artifacts or op-visible path behavior.
- Do not require every c2ops `codex` use to migrate immediately.

## Requirement 1: Compact Skill Invocation

c2ops `run_skill` should run one enforced top-level skill with standard c2 op
paths.

Required surface:

```yaml
- id: intake
  op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
  inputs:
    skill: c2-ticket-intake
    skills:
      - gitl.colony2.com/jnadeau/skills/.agents/skills@main
    prompt: "{{ inputs.prompt }}"
    artifacts:
      submitted/: "${{ context.artifacts }}"
    status_contract:
      path: ticket/latest-status.json
```

The op should default these values from the current op context unless explicitly
overridden:

- `worktree_path`;
- `workdir_path`;
- `artifact_inbox_path`;
- `artifact_outbox_path`.

## Requirement 2: Current Codex Skill Compatibility

`run_skill` should support the current c2ops `codex` skill inputs:

- `skill`;
- `skills`;
- `skill_mode`;
- `skill_selection_mode`;
- `return_on`;
- `status_contract.path`;
- `sessionId`;
- `model`;
- `sandbox`;
- `env`.

If implemented as a wrapper around c2ops `codex`, the wrapper should preserve
the current normalized outputs:

- `status`;
- `sessionId`;
- `assistantSummary`;
- `incompleteReason`;
- `incompleteCategory`;
- `pendingDependencies`;
- `skills_installed`;
- `outcome`.

## Requirement 3: Structured Output Artifact Validation

`run_skill` should parse and validate the skill's primary structured response
from a declared output artifact by default.

Required options:

```yaml
inputs:
  output:
    from: artifact
    path: ticket/result.json
    format: json
    schema:
      type: object
      required: [summary]
```

Outputs should include:

- `output_source`;
- `output_path`;
- `raw_output`;
- `parsed_output`;
- `output_schema_valid`;
- `output_schema_errors`;
- `output_repair_attempts`.

If schema validation fails, the op should either fail or return an incomplete
status based on an explicit policy input.

Compatibility mode may parse `assistantSummary`, but new skills should prefer
artifact output because `assistantSummary` is part of the Codex wrapper result,
not the skill's durable data contract.

## Requirement 4: Status Contract Validation

When `status_contract.path` is set, `run_skill` should validate that the status
artifact exists and is parseable JSON.

The op should expose:

- `status_contract_present`;
- `status_contract_valid`;
- `status_contract_json`;
- `status_contract_errors`.

The job story should identify the status artifact path.

## Requirement 5: Artifact Binding

`run_skill` should accept normal recipe artifact bindings and future artifact
bundle aliases.

Example:

```yaml
artifacts:
  use:
    - submitted
    - ticket-intake
```

The op must not assume that submitted file contents are embedded in the prompt.
It should pass inbox paths to the skill environment and preserve the existing
op-visible path contract.

## Requirement 6: Job Story And Diagnostics

The job story should show:

- requested skill name;
- resolved skill bundle refs;
- status contract path;
- output schema validation result;
- checkpoint status and return reason;
- emitted artifact names.

Errors should explain whether the failure came from skill resolution, Codex
execution, missing artifacts, status contract validation, or output schema
validation.

## Requirement 7: Recipe Testing

Recipe tests should be able to mock `run_skill` by node path or selector without
mocking lower-level Codex behavior.

Mock outputs should support the same normalized shape as c2ops `codex`, plus
`parsed_output` and status contract validation fields.

## Efficiency Examples

### Example 1: Basic Skill Invocation

Before:

```yaml
- id: build_outcome_bundle
  op: git+https://github.com/colony-2/c2ops.git//codex@main
  artifacts:
    submitted/: "${{ context.artifacts }}"
    requirements/plan.json: "${{ states.requirements.artifacts['requirements/plan.json'] }}"
    implementation/plan.json: "${{ states.implementation.artifacts['implementation/plan.json'] }}"
  inputs:
    worktree_path: "{{ context.environment.op.worktree_path }}"
    workdir_path: "{{ context.environment.op.workdir }}"
    artifact_inbox_path: "{{ context.environment.op.inbox }}"
    artifact_outbox_path: "{{ context.environment.op.outbox }}"
    skill: c2-test-statement-curator
    skill_mode: enforce
    skills:
      - gitl.colony2.com/jnadeau/skills/.agents/skills@main
    status_contract:
      path: outcome/latest-status.json
    prompt: |
      Follow the `c2-test-statement-curator` skill contract.
      Ticket prompt: {{ inputs.prompt }}
      Input artifacts are under {{ context.environment.op.inbox }}.
      Write output artifacts under {{ context.environment.op.outbox }}/outcome.
```

After:

```yaml
- id: build_outcome_bundle
  op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
  artifacts:
    use:
      - submitted
      - planning
  inputs:
    skill: c2-test-statement-curator
    skills:
      - gitl.colony2.com/jnadeau/skills/.agents/skills@main
    prompt: "{{ inputs.prompt }}"
    status_contract:
      path: outcome/latest-status.json
```

Efficiency gain: the recipe author removes repeated path plumbing and standard
skill boilerplate. The recipe now shows the workflow intent instead of the
mechanics of invoking Codex.

### Example 2: Parsed JSON Output Artifact

Before:

```yaml
outputs:
  summary: "${{ json_parse(sequence.plan.artifacts['outcome/result.json']).summary }}"
  dependency_order: "${{ json_parse(sequence.plan.artifacts['outcome/result.json']).dependency_order }}"
  requirements: "${{ json_parse(sequence.plan.artifacts['outcome/result.json']).requirements }}"
```

After:

```yaml
outputs:
  summary: "${{ sequence.plan.outputs.parsed_output.summary }}"
  dependency_order: "${{ sequence.plan.outputs.parsed_output.dependency_order }}"
  requirements: "${{ sequence.plan.outputs.parsed_output.requirements }}"
```

Efficiency gain: schema validation and parse errors move into one op output
instead of being repeated across every field projection.

## Acceptance Criteria

- A recipe can run a skill without manually passing op-visible paths.
- A recipe can validate JSON from a declared output artifact without inline
  `json_parse(...)` on every output.
- A recipe test can mock `run_skill` with one node-path mock.
- The job story records resolved skill refs and status contract validation.

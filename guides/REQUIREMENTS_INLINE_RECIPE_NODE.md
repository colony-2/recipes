# Requirements: Inline Recipe Node

## Status

Draft requirements for a c2j core authoring feature.

This is motivated by the Superpowers recipe work, but the feature should be a
general recipe-composition primitive.

## Motivation

Large production recipes benefit from one durable workflow boundary while still
needing readable, independently testable phase definitions. Today authors have
two imperfect choices:

- keep every phase inline in one very large recipe, which makes authoring and
  review harder;
- split phases into separate recipes, which makes testing easier but can imply
  standalone production entrypoints or child-job boundaries that are not
  actually required.

For Superpowers, the desired production shape is one normal ticket lifecycle
recipe. Brainstorming, planning, plan review, task execution, verification,
finish, and debugging should usually run in one job with many recipe-owned Codex
sessions. Separate child jobs should be reserved for real C2 job boundaries such
as cross-cell work, target-ref advancement, reuse, lifecycle isolation, or true
parallelism.

Recipe authors still need a way to keep those phases in separate files without
turning them into runtime child jobs.

## Core Concept

c2j should support a node type that inlines another proper recipe into the
current recipe.

The referenced unit is not a special fragment format. It is a normal recipe file
with the same top-level shape used for direct submission:

- `id`
- `version`
- `input_schema`
- `inputs`
- one root body: `op`, `sequence`, or `state`
- `outputs`

When used as an inline node, that recipe executes inside the parent job. It does
not create a child job, does not create a separate recipe result boundary, and
does not change git or artifact persistence semantics beyond normal same-job
node execution.

## Example Shape

The exact field names are implementation choices, but the authoring surface
should be close to this:

```yaml
state:
  initial: brainstorm
  states:
    brainstorm:
      recipe:
        inline: ./superpowers-brainstorm.yaml
        inputs:
          prompt: "{{ inputs.prompt }}"
          skill_bundle_ref: "{{ inputs.skill_bundle_ref }}"
      transitions:
        - to: write_plan
          when: outputs.approved_for_planning

    write_plan:
      recipe:
        inline: ./superpowers-write-plan.yaml
        inputs:
          prompt: "{{ inputs.prompt }}"
          design_json: "{{ states.brainstorm.outputs.design_json }}"
          skill_bundle_ref: "{{ inputs.skill_bundle_ref }}"
      transitions:
        - to: review_plan
          when: true
```

The parent consumes the inline recipe like any other node:

```yaml
outputs:
  design_json: "{{ states.brainstorm.outputs.design_json }}"
  plan_json: "{{ states.write_plan.outputs.plan_json }}"
```

## Goals

- Let authors keep phase logic in proper recipe files.
- Preserve one production job when no child-job boundary is needed.
- Keep phase recipes independently submittable and testable.
- Let production behavior tests target the production recipe instead of a set of
  phase harnesses.
- Preserve explicit input/output boundaries between parent and inline recipe.
- Preserve normal same-job git persistence, artifact handling, job story, and
  failure behavior.
- Make source locations and expanded node paths clear enough for debugging and
  recipe-test mocks.

## Non-Goals

- Do not create a child job.
- Do not replace `recipes.run`, `recipe.run_and_get_result`,
  `recipe.await_result_soft`, or `child_group`.
- Do not provide parallelism by itself.
- Do not add a separate fragment-only recipe shape.
- Do not make YAML text inclusion or anchors part of the runtime model.
- Do not let an inline recipe implicitly read parent sibling state.
- Do not let the parent implicitly read arbitrary internal node outputs from the
  inline recipe.
- Do not fetch or reinterpret referenced recipes during replay.

## Requirement 1: Proper Recipe Reuse

An inline target must be a valid recipe by itself.

The same file should be usable in both ways:

```bash
c2j submit --recipe-file ./superpowers-write-plan.yaml --run --embed
```

and:

```yaml
- id: write_plan
  recipe:
    inline: ./superpowers-write-plan.yaml
    inputs:
      prompt: "{{ inputs.prompt }}"
      design_json: "{{ sequence.brainstorm.outputs.design_json }}"
```

The inline feature must not require authors to maintain a second fragment file
format for the same phase.

## Requirement 2: Same-Job Execution Semantics

An inline recipe node executes as part of the current job.

Required semantics:

- no child job is created;
- no separate child job ID is produced;
- no separate child result encapsulation is introduced;
- node execution appears in the same parent job story;
- git state flows through the inline recipe's internal ops exactly as it would
  through equivalent inline nodes;
- automatic git persistence after internal ops remains unchanged;
- a mutating inline recipe locks and advances the current job git state the same
  way an inline `op`, `sequence`, or `state` would;
- pausing inside an inlined `input` node pauses the parent job.

If the inline recipe itself contains child-job ops, those child jobs are still
real runtime child jobs. Inline composition only controls the boundary between
the parent recipe and the included recipe.

## Requirement 3: Input Contract

The parent must pass inputs to the inline recipe through an explicit `inputs`
map.

The inline recipe's normal `input_schema` and top-level `inputs` normalization
must still apply. Conceptually:

1. the parent renders the callsite `inputs` map;
2. c2j validates that map against the inline recipe's `input_schema`;
3. the inline recipe evaluates its own top-level `inputs` block from that mapped
   input object;
4. the inline recipe body sees only its normalized recipe inputs, normal
   `context`, and explicitly supplied artifacts.

The inline recipe must not implicitly inherit the parent's `inputs`,
`states.<id>`, or `sequence.<id>` scopes. Authors should pass needed values
explicitly.

## Requirement 4: Output Contract

The parent sees the inline recipe's top-level `outputs` as the inline node's
outputs.

Example:

```yaml
states:
  write_plan:
    recipe:
      inline: ./superpowers-write-plan.yaml
      inputs:
        design_json: "{{ states.brainstorm.outputs.design_json }}"

outputs:
  plan_json: "{{ states.write_plan.outputs.plan_json }}"
```

Internal node outputs of the inline recipe should remain encapsulated for normal
recipe dataflow. Authors should export anything the parent needs through the
inline recipe's top-level `outputs`.

Recipe tests and job-story inspection may still expose expanded internal node
paths for debugging and mocking, but that must not become the normal parent
dataflow contract.

## Requirement 5: Artifact Contract

The parent should be able to pass artifacts to an inline recipe explicitly.

Recommended shape:

```yaml
- id: verify
  recipe:
    inline: ./superpowers-verify.yaml
    inputs:
      plan_json: "{{ sequence.write_plan.outputs.plan_json }}"
    artifacts:
      design.md: "${{ sequence.brainstorm.outputs.design_artifact }}"
```

The inline recipe should receive those artifacts as its submitted artifact set,
using the same rules that apply when the recipe is submitted directly.

Artifacts produced by internal nodes remain same-job artifacts. The parent may
consume artifact handles only when the inline recipe explicitly exports them
through top-level outputs, just as a sequence or state machine exports artifacts
today.

## Requirement 6: Namespacing And Node Paths

c2j must namespace the inline recipe's internal nodes under the callsite node.

Requirements:

- parent and inline recipe node IDs must not collide;
- two callsites may inline the same recipe file with different inputs;
- expanded paths must be deterministic;
- source recipe ID and callsite ID must both be visible in diagnostics;
- recipe tests must be able to mock/assert internal nodes through the expanded
  path when needed.

Example expanded path, exact syntax TBD:

```text
superpowers/write_plan/inline:superpowers-write-plan/write_plan_skill
```

The stable public path for parent dataflow remains the callsite path:

```text
states.write_plan.outputs.plan_json
```

## Requirement 7: Compile-Time Resolution And Durable Replay

Inline recipe references should be resolved at compile/submit time.

Required behavior:

- `c2j submit --recipe-file ... --embed` embeds the resolved inline recipe
  content in the submitted job snapshot;
- replay and resume use the embedded snapshot, not whatever file happens to
  exist later on disk;
- compile diagnostics include both the parent callsite location and the source
  location inside the inline recipe;
- resolution failures fail before the job starts.

Minimum required reference type:

- local relative recipe file path.

Future reference types may include named recipes or git-pinned recipe refs, but
the first version should solve local authoring cleanly.

## Requirement 8: Recursion And Cycle Handling

Inline recipes may themselves inline other recipes if c2j can keep the expanded
graph deterministic and readable.

Requirements:

- direct and indirect include cycles must fail compile with a clear diagnostic;
- the diagnostic should show the include chain;
- c2j may impose a maximum inline depth;
- recursive runtime behavior is not required.

## Requirement 9: Failure And Pause Behavior

An inline recipe failure is a failure of the inline node.

Required behavior:

- parent state transitions can route on the inline node's normal outputs after
  successful completion;
- if the inline recipe fails before producing outputs, normal node failure
  handling applies;
- if the inline recipe pauses for user input, the parent job pauses at that
  nested node and resumes in the same expanded graph;
- failures should include source locations in the parent callsite and in the
  inline recipe.

This feature should not add a soft-failure child-status model. Soft child status
belongs to child jobs and `recipe.await_result_soft`.

## Requirement 10: Recipe Testing

Recipe tests must work against both the standalone recipe and the production
recipe that inlines it.

Tests should support:

- compiling the parent recipe with all inline recipes expanded;
- mocking internal nodes by expanded path;
- asserting parent-visible outputs from the inline callsite;
- asserting that a phase was reached through the production recipe;
- asserting that production tests do not need to submit the phase recipe as a
  separate job;
- showing source locations for failed expectations inside inlined recipes.

This is the key Superpowers use case: phase behavior tests should be able to run
against `recipes/superpowers/superpowers.yaml`, while the phase recipe files
remain independently testable during authoring.

## Requirement 11: Job Story And Diagnostics

The job story should make inline composition visible without treating it as a
child job.

The story should show:

- the parent callsite node ID;
- the referenced recipe ID, version, and source ref/path;
- rendered inline recipe inputs, subject to normal redaction rules;
- expanded internal node execution;
- top-level outputs exported back to the parent;
- source locations for validation and runtime errors.

The story must clearly distinguish:

- inline recipe composition;
- runtime child recipe execution;
- `child_group` fanout.

## Requirement 12: Superpowers Acceptance Criteria

The feature is sufficient for the Superpowers production recipe when:

- `recipes/superpowers/superpowers.yaml` can inline proper recipe files for
  brainstorm, write-plan, plan-review, execute-plan, verify, finish, and debug
  phases;
- the same phase files can still be submitted directly for focused authoring;
- production behavior tests can target `recipes/superpowers/superpowers.yaml`
  rather than separate phase harnesses;
- no child job is created for ordinary same-job Superpowers phases;
- child jobs remain available only for concrete C2 job boundaries;
- the production recipe can consume phase outputs through the inline callsite
  outputs;
- recipe-test mocks can still target internal Codex and rule-gate nodes inside
  an inlined phase.

## Open Design Questions

- Should the node key be `recipe` with `inline`, `inline_recipe`, or `include`?
- Should c2j require an explicit output schema for recipes intended to be
  inlined, or are normal top-level `outputs` sufficient?
- Should artifact bindings on an inline recipe node exactly mirror op artifact
  bindings, or should they mirror submitted job artifacts?
- Should named recipe refs be allowed in the first version, or should the first
  version only support local file paths?
- How should expanded node paths be rendered so they are stable but not too
  verbose for recipe tests?

## Non-Blocking Follow-Ups

- Add optional recipe output schemas if inline reuse shows that untyped outputs
  are hard to maintain.
- Add an authoring command to print the fully expanded recipe graph.
- Add linting that detects phase recipes duplicated inline instead of reused
  through this feature.

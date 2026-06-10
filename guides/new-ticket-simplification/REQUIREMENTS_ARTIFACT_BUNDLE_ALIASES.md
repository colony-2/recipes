# Requirements: Artifact Bundle Aliases

## Status

Draft requirements for c2j recipe authoring.

## Motivation

Recipe nodes repeat long artifact binding lists across planning, review,
implementation, and validation states. The same files are repeatedly mapped:

- submitted artifacts;
- requirements plans;
- implementation plans;
- outcome plans;
- review packs;
- validation outputs.

This makes recipes noisy and increases the chance that one state forgets an
artifact required by a later step.

## Goals

- Let recipes define named artifact bundles once.
- Let nodes bind bundles by name.
- Preserve explicit artifact provenance.
- Keep recipe tests able to assert which artifacts were passed.
- Support migration from current explicit artifact maps.

## Non-Goals

- Do not make artifacts globally visible without binding.
- Do not hide artifact provenance or producing node.
- Do not replace artifact references for one-off bindings.
- Do not introduce implicit filesystem sharing between ops.

## Requirement 1: Bundle Declaration

Recipes should support top-level named artifact bundles.

Example:

```yaml
artifact_bundles:
  ticket-intake:
    artifacts:
      requirements/plan.json: "${{ states.intake.artifacts['requirements/plan.json'] }}"
      requirements/index.md: "${{ states.intake.artifacts['requirements/index.md'] }}"
      implementation/plan.json: "${{ states.intake.artifacts['implementation/plan.json'] }}"
      outcome/plan.json: "${{ states.intake.artifacts['outcome/plan.json'] }}"
  submitted:
    artifacts:
      submitted/: "${{ context.artifacts }}"
```

Bundle names must be unique within the recipe scope.

## Requirement 2: Bundle Use

Any node that accepts artifacts should be able to bind bundles by name.

Example:

```yaml
artifacts:
  use:
    - submitted
    - ticket-intake
  extra:
    feedback/user-feedback.md: "${{ states.review.artifacts['feedback.md'] }}"
```

`use` should expand into normal artifact bindings before execution. Explicit
bindings in `extra` should override bundle bindings only when the recipe author
opts in to override behavior.

## Requirement 3: Scoped Bundles

Bundles should support recipe-level, sequence-level, and state-level scopes.

Children may use bundles visible in their container scope. A nested container
must explicitly export bundle references if outer nodes need them.

This should follow the same encapsulation principles as node outputs.

## Requirement 4: Pattern Bundles

Bundles should support pattern-based artifact grouping when the producing node
emits many files.

Example:

```yaml
artifact_bundles:
  review-pack:
    from: states.counterpoint.artifacts
    include:
      - reviews/**
    exclude:
      - reviews/tmp/**
```

Patterns must apply only to named artifacts, not arbitrary local filesystem
paths.

## Requirement 5: Collision Handling

If two bundles provide the same destination key, c2j should fail validation
unless the node explicitly configures collision behavior.

Supported collision behavior:

- `error` default;
- `first_wins`;
- `last_wins`;
- `explicit_overrides_only`.

The job story should record any non-default collision policy.

## Requirement 6: Job Story And Diagnostics

The job story should show:

- bundle names used by each node;
- expanded artifact bindings;
- producing node or source context for each artifact;
- collision policy and overrides.

Diagnostics should identify missing bundle names at validation time when
possible.

## Requirement 7: Recipe Testing

Recipe tests should be able to assert expanded artifact bindings after bundle
resolution.

Mocking should still work at the node path level; bundle expansion should not
change node identity.

## Efficiency Examples

### Example 1: Repeated Planning Artifacts

Before:

```yaml
artifacts:
  submitted/: "${{ context.artifacts }}"
  requirements/plan.json: "${{ states.requirements.artifacts['requirements/plan.json'] }}"
  requirements/index.md: "${{ states.requirements.artifacts['requirements/index.md'] }}"
  implementation/plan.json: "${{ states.implementation.artifacts['implementation/plan.json'] }}"
  implementation/index.md: "${{ states.implementation.artifacts['implementation/index.md'] }}"
  outcome/plan.json: "${{ states.outcome.artifacts['outcome/plan.json'] }}"
  outcome/tests-index.md: "${{ states.outcome.artifacts['outcome/tests-index.md'] }}"
  outcome/validation-commands.txt: "${{ states.outcome.artifacts['outcome/validation-commands.txt'] }}"
```

After:

```yaml
artifacts:
  use:
    - submitted
    - ticket-intake
```

Efficiency gain: implementation, validation, and reviewer states can all use
the same named bundle instead of repeating fragile artifact maps.

### Example 2: Review Pack Hand-Off

Before:

```yaml
artifacts:
  reviews/review-pack.json: "${{ states.counterpoint.artifacts['reviews/review-pack.json'] }}"
  reviews/requirements.md: "${{ states.counterpoint.artifacts['reviews/requirements.md'] }}"
  reviews/compat.md: "${{ states.counterpoint.artifacts['reviews/compat.md'] }}"
  reviews/outcome.md: "${{ states.counterpoint.artifacts['reviews/outcome.md'] }}"
```

After:

```yaml
artifacts:
  use:
    - review-pack
```

Efficiency gain: adding a new reviewer does not require updating every
downstream artifact binding.

## Acceptance Criteria

- A node can bind `submitted` and `ticket-intake` bundles without listing every
  artifact.
- Missing bundle names fail with a clear validation error.
- Duplicate artifact keys fail unless an explicit collision policy is set.
- The job story shows both the bundle name and expanded artifact list.

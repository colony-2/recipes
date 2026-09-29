---
schema: c2.cell-mandate/v1
---

# Recipes cell mandate

## Purpose

Provide the development workflows that C2 uses to turn requests into scoped,
reviewed, tested, and integrated software changes. Maintain the recipes and
their authoring guidance so projects can use and specialize these workflows.

## Owns

- OWN-01: Shared C2 recipes, including build/evolve entrypoints, phase orchestration,
  human review, dependency coordination, and integration decisions.
- OWN-02: Recipe-owned input/output and artifact contracts, design and test-plan
  requirements, mandate-assessment conventions, and workflow instructions.
- OWN-03: Tests, fixtures, and disposable runtime harnesses that establish recipe
  behavior and integration with supported C2 operations.
- OWN-04: Recipe authoring documentation, examples, and proposals describing
  workflow needs and the contracts required from neighboring components.

## Does not own

- EXCLUDE-01: The c2j execution engine, CLI, JobDB implementation, or their runtime
  persistence, scheduling, and repository-management internals.
- EXCLUDE-02: c2ops operation implementations, including the Codex launcher,
  session import/export, and operation-specific execution behavior.
- EXCLUDE-03: Application features and infrastructure owned by consuming project
  cells. A shared recipe coordinates their work without taking ownership of it.
- EXCLUDE-04: Unilateral changes to another cell's mandate or repository.

## Interfaces

- INTERFACE-01: c2j consumes recipe YAML and provides job execution, templates,
  artifacts, Git state, user input, and child-job lifecycle operations.
- INTERFACE-02: c2ops supplies selector-backed operations used by recipes.
  Missing capabilities or defects are specified and reported to their owners.
- INTERFACE-03: Project cells consume shared defaults or specialize them under
  `.c2j/recipes/`; their own mandates and applicable instructions govern local work.

## Boundary examples

- `fits`: Add a design checkpoint to build/evolve and deterministic tests for it.
- `partial`: Add a cross-cell consultation recipe and a new repository-session
  operation. This cell owns the recipe and contract; c2j/c2ops own runtime changes.
- `outside`: Implement a new persistence backend for JobDB.

## Changing the mandate

The human maintainer responsible for this repository accepts ownership changes
through an explicit review of the proposed boundary and affected neighboring
cells. Agents can propose such changes and gather design feedback. Until a
change is accepted, assess work against the previously accepted mandate; an
edit to this file does not itself authorize broader implementation work.

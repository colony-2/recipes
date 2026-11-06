# Runtime fixture references in mocked outputs

## Problem

`c2j test` creates each runtime cell with a generated portable repository identity.
A mocked creation proposal cannot name that identity: `behavior.outputs` and
`behavior.artifacts` are static, and the suite does not know the generated value.
Using the cell name as `repo` now correctly fails repository validation.

This blocks full creation/publication scenarios after their registration boundary.
The fixture already registers its cells, so these tests mock the registration
command while separately exercising native registration in dedicated cases.
They still need the real registered repository for the empty-workspace selector
and initialization child submission. Removing the explicit repo is not a fix:
empty workspace resolution currently skips registry lookup and requires it.

## Proposed interface

Allow explicit fixture references in mock output values, resolved after seeding
cells and before the mocked operation returns. For example:

```yaml
mocks:
  ops:
  - match:
      selector: nix:github:colony-2/c2ops/published#codex
    behavior:
      mode: return
      outputs:
        response:
          cells:
          - name: alpha
            repo: {fixture: cells.alpha.repo}
            purpose_path: cells/alpha/PURPOSE.md
```

The exact syntax can follow c2j conventions. Expose the registered portable repo,
not the host checkout path. Make unknown cells/fields a fixture-validation error.
Resolve references only in declared fixture data, without evaluating model output
as CEL or changing production template behavior. If artifacts need substitution,
make it explicit and preserve ordinary literal content by default. These creation
cases also need the same references in their proposed `root-config.yaml` artifacts,
so the reviewed configuration and structured proposal name the same repositories.

## Acceptance

- Two parallel cases resolve their own cells without sharing identities.
- Mocked proposals can supply a repository accepted by native empty workspaces
  and child submission for that cell.
- Unknown references fail before the scenario proceeds.
- Literal strings, including template-looking user content, remain literal.
- Test reports show the resolved returned value.

Recipes will consume this feature in the retained full creation suites. Native
registration conflict/permission tests and native publication tests remain.
No production recipe should accept invalid repository locators or skip identity
checks merely to accommodate static test responses.

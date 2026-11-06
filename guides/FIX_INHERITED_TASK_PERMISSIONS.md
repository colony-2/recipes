# Preserve Git access when restricting task permissions

Job `3Li7sIC4c53lVtcIbjkyCiHXIXd` used recipes commit `562ff6a` and failed before
its first Codex task. The read-only node's replacement grant disabled submission
but also removed the Git secret needed for checkout.

## Change

Fresh and resumed read-only tasks now use c2j's explicit inheritance mode:

```yaml
perms:
  inherit: true
  jobdb:
    jobs:
      submit: false
```

Root cell registration has the same correction, plus `cells.create: true`.
Its submission permission remains explicitly disabled. No deployment-specific
secret names are embedded in the recipes, and `const: true` is preserved.

Requires c2j main `eb636a5` or later. See the upstream
[node permission guide](https://github.com/colony-2/c2j/blob/eb636a529263/GUIDE-Node-Permissions.md).
Inheritance overrides individual fields; it is not an irrevocable ceiling.
Existing enclosing limits still apply, and siblings recover their enclosing grant.

## Regression coverage

[permissions.test.yaml](../recipe-tests/adaptive/permissions.test.yaml) uses the
actual production node declarations, replacing only their task bodies with a
native probe. The probe calls Git's credential helper, attempts child submission
through c2j's task broker, and checks cell creation and unrelated-secret denial.
No model or production credentials are used.

- Both read-only node declarations retain Git access with different configured
  secret names and reject submission before creating a child.
- Registration retains Git access and can register a cell, while submission stays denied.
- A subsequent implementation sibling retains Git access and can submit one child;
  it cannot inherit registration's creation authority.
- All three declarations reproduced `secret resolution unavailable` before the fix.

The fixture inspects its specific probe attempt to report deliberate failures;
production dependency waiting continues to target goals. It tests the actual
credential-resolution path used by checkout, without a network Git server or a
live Codex session. Existing agent tests cover session routing separately.

## Validation

Validated with c2j `eb636a5`: **209 cases passed**—203 adaptive cases across
40 suites, plus three native cell-registration cases and three publication cases.
The three new permission cases also passed directly against the original files.
`git diff --check` passed.

The broader adaptive run used the existing temporary test copy that lowers mocked
Nix model selectors to their execution primitive and uses installed Python/yq for
helper commands. The new permission suite and the six creation cases ran without
that adaptation. Credential resolution, task-broker submission, and cell creation
were real native operations using synthetic fixture credentials throughout.

No production job was restarted. Existing captured recipes retain their original
grant; recovery must use an updated recipe and a runtime supporting inheritance.

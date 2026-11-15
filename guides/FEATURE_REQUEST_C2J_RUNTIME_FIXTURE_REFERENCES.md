# Seeded repository identities for creation tests

Native c2j tests register disposable cells with generated portable repository
identities. Creation proposals must use those identities rather than cell names as
repository locators. Seeded fixtures already register their cells, so creation
suites mock only the registration command; the separate registration suite tests
native idempotency, conflicts and denial.

The runtime supports explicit seeded references in mock return values:

```yaml
behavior:
  mode: return
  fixture_refs:
    alpha_repo: {cell: alpha, field: repo}
  outputs_fixture_expr: >-
    {"status": "completed", "output_schema_valid": true,
     "response": {"cells": [{"name": "alpha", "repo": alpha_repo,
       "purpose_path": "cells/alpha/PURPOSE.md"}]}}
```

Declare `alpha` in `runtime.cells`. The expression above illustrates identity
binding; actual creation responses also supply outcome, summary, files and
questions. See [the complete creation suite](../recipe-tests/create.test.yaml).
Computed values are explicit fixture data; ordinary artifact strings stay literal.
No production validation is relaxed for tests.

Creation no longer approves or writes root configuration, so these fixtures need
no computed root-config artifact. The publication tests instead compare root
configuration blobs, complete trees and history before and after creation and
exercise an independent concurrent root writer.

The earlier request for this runtime facility is satisfied by c2j's seeded
reference support. Its complete interface and framework guarantees belong to
[c2j's native testing guide](https://github.com/colony-2/c2j/blob/main/GUIDE-Native-Recipe-Testing.md#seeded-repository-references-in-native-mocks).

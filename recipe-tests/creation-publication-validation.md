# Creation publication failure validation

Validated on 2026-11-01 with
`c2j v0.0.117-0.20261031185936-a501d923f053`.

| Check | Result |
| --- | --- |
| `creation-publication.test.yaml` | All 8 cases passed. |
| `create-handoff.test.yaml` | Passed, including independent initial history, exact contents, author, and committer. |
| `create.test.yaml` | 19 passed; 2 existing clarification cases failed identically on the unchanged revision. |
| Native validation of all three suites | Passed. |
| `bash build.sh`, `git diff --check` | Passed. |

The new integration cases run actual child jobs and Git publication against
disposable repositories. Receive hooks reject initial and catalog pushes; a
catalog hook advances upstream during publication to exercise native
`MERGE_UPSTREAM_ADVANCED` classification. Model decisions are mocked. Additional
operation mocks check unchanged error messages and originating nodes, including
the reported HTTP 403 diagnostic; these mocks do not establish HTTP transport
classification.

The initial-push and catalog-push rejection regressions were also run against
unchanged recipes revision `84a889884fcf78f44de9ab80dcfb99ddf5329d5e` in an
isolated checkout. Both failed their expected-job-error checks: the old recipes
completed normally with `publication_failed` and `registration_failed`.

The pre-existing failures are `clarification-without-artifacts` and
`clarification-with-unresolved-optional-references`. Both fail their third
assertion on the unchanged revision as well as this change. Publication fixes
do not modify clarification behavior or its expectations.

Initial publication retains the composite operation because migrating it to
native `squash` changes the configured committer in this runtime. The existing
handoff assertions were preserved. Correcting native squash committer handling
belongs to c2j.

Reproduce the suites with:

```sh
c2j test run --file recipe-tests/creation-publication.test.yaml --out-dir .c2/test-results/creation-publication
c2j test run --file recipe-tests/create-handoff.test.yaml --out-dir .c2/test-results/create-handoff
c2j test run --file recipe-tests/create.test.yaml --out-dir .c2/test-results/create
```

Local execution used portable Nix with its store exposed to the test process,
rollback SQLite journal mode, and a temporary adapter converting static
`inputDrvs` objects to the equivalent legacy arrays accepted by this c2j build.
The adapter rejects dynamic inputs and does not replace packages, Git, or recipe
operations. This is the already-documented
[local Nix compatibility limitation](../guides/BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md#separate-local-test-prerequisite);
no adapter or runtime code changes are included in this patch.

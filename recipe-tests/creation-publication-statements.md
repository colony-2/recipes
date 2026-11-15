# Creation publication test statements

These replace catalog publication expectations under the approved removal recorded
in [creation expectations](create-statements.md). Each expectation is at most 30 words.

| Priority | Kind / dependencies | Source → test file | Expected outcome |
| --- | --- | --- | --- |
| P0 | Integration / c2j, Git | `recipes/create/initialize.yaml`, `create.yaml` → `creation-publication.test.yaml` | Initial push rejection prevents completion and preserves the original publication diagnostic. |
| P0 | Integration / c2j, Git | `recipes/create/publish.yaml` → `creation-publication.test.yaml` | Later failure preserves earlier registered and published cells, failing child identity and available diagnostics without rollback. |
| P0 | Integration / c2j | `recipes/create/publish.yaml` → `creation-publication.test.yaml` | Required initialization failure, timeout or cancellation prevents readiness and retains registration, pending child identity and completed publications. |
| P1 | Integration / c2j | `recipes/create/initialize.yaml` → `creation-publication.test.yaml` | Permission and preparation failures retain their exact diagnostic and originating operation. |
| P0 | Integration / c2j, Git | `create.yaml` → `creation-publication.test.yaml` | Root push rejection cannot block creation because creation performs no root publication. |
| P0 | Integration / c2j, Git | `create.yaml` → `creation-publication.test.yaml` | Root config bytes, tree and history remain unchanged; independent concurrent advancement survives with absent and legacy dependents. |
| P0 | Integration / c2j | `recipes/create/publish.yaml` → `creation-lifecycle.test.yaml` | A real held child releases only after required wait entry; creation completes only after both released children publish. |
| P0 | Integration / c2j | `recipes/create/publish.yaml` → `creation-lifecycle.test.yaml` | A native child timeout prevents completion and retains pending child identity and the original timeout classification. |
| P0 | Integration / c2j, Git | `create.yaml` → `creation-root-failure.test.yaml` | Initial and later publication failure preserve exact root configuration, tree and history with absent and legacy configuration. |

Push rejection runs real Git receive hooks. Timeout and cancellation propagation
cases inject the required-wait diagnostic after a successful first publication;
router cases script terminal child statuses. A separate isolated fixture exercises
a native child deadline. Controller cancellation of a child lease is not established: the available cancellation control requires
the primary job itself to finish CANCELLED, while required child cancellation
would make this parent fail. Scripted cancellation checks remain explicit. A real
child fixture also returns a typed cancellation failure; it exercises native failure propagation without
claiming controller or lease cancellation. Unexpected case timeouts fail
acceptance rather than satisfying an expected error.

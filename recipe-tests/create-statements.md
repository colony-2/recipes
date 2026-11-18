# Cell creation test statements

These expectations apply the removal approved in root job
`3M4p8iTbAYbweGdvfBfyPjnhNAx`, review
`925ee3e8-1d78-4256-bf6d-aca2c8e9126c` (`accept`, empty feedback).
Registration means the existing JobDB registry operation. Completion requires
initialization as well. The former root catalog application, recovery, verification
and merge expectations are retired by that approved removal.

Each expectation is at most 30 words. Native means c2j's disposable runtime with
seeded repository references, scripted model/review decisions and local Git.

| Priority | Kind / dependencies | Source → test file | Expected outcome |
| --- | --- | --- | --- |
| P0 | Integration / Native | `create.yaml` → `create.test.yaml` | Approved creation registers and initializes every required cell before returning created, merged true and an empty merged_hash. |
| P0 | Integration / Native | `create.yaml` → `create-owner.test.yaml` | Foreign job ownership fails before review or side effects, even when selecting the root workspace. |
| P0 | Integration / Native | `recipes/create/review.yaml` → `create.test.yaml` | Approval reviews names, repository destinations and exact initial purposes without requiring root-config.yaml. |
| P0 | Integration / Native | `recipes/create/review.yaml` → `create.test.yaml` | Missing identities, duplicate destinations and missing or empty purposes require correction before registration or publication. |
| P0 | Integration / Native | `recipes/create/review.yaml` → `create.test.yaml` | Declined, redirected or cancelled proposals and annotated approvals never authorize registration or publication. |
| P1 | Integration / Native | `recipes/create/review.yaml` → `create.test.yaml` | Clarification and revision retain the consultation session, feedback and annotations and require a revised consolidated review. |
| P0 | Integration / Native | `create.yaml` → `create.test.yaml` | Creation invokes no catalog capture, copy, recovery, verification agent, cell-add command or root squash/merge. |
| P1 | Integration / Native | `create.yaml` → `create-handoff.test.yaml` | Completion preserves created identities, initialization results, annotations, review/artifact references and the approved review session. |
| P0 | Integration / Native | `recipes/create/publish.yaml` → `create.test.yaml` | A required initialization without a completed result never sets the completion alias or readiness. |
| P0 | Integration / Native | `create.yaml` → `creation-publication.test.yaml` | Creation preserves root configuration bytes, tree and history with absent dependents, legacy dependents and unrelated settings. |
| P0 | Integration / Native | `create.yaml` → `creation-publication.test.yaml` | An independent concurrent root writer's exact advancement survives creation without root publication, refresh or a publication gate. |
| P0 | Integration / Native, grants | `recipes/create/register-cell.yaml` → `cell-registration.test.yaml` | Same-request retries preserve registration identity; conflicting identities and foreign owners fail without replacing original diagnostics. |
| P0 | Integration / Native, grants | `recipes/create/register-cell.yaml` → `adaptive/permissions.test.yaml` | Creation authority remains confined to registration and unavailable to model operations or sibling commands. |
| P0 | Integration / Native, grants | `recipes/create/publish.yaml` → `creation-permissions.test.yaml` | Registration without submission authority cannot initialize a repository or report readiness. |
| P0 | Integration / Native | `recipes/create/publish.yaml` → `registered-cell-publication.test.yaml` | Repository assertions reject mismatched identities before initialization while retaining registration evidence. |
| P0 | Integration / Native, Git | `recipes/create/initialize.yaml` → `create-handoff.test.yaml` | Initial publication preserves exact approved PURPOSE bytes, independent initial history and configured author and committer. |
| P0 | Integration / Native, Git | `recipes/create/initialize.yaml` → `create.test.yaml` | Existing destination branches fail initialization without overwriting history or reporting readiness. |
| P0 | Integration / Native | `recipes/adaptive/route-target.yaml` → `creation-routing.test.yaml` | The router accepts matching successful publication with merged true and an empty merged_hash and permit continuation. |
| P0 | Integration / Native | `recipes/adaptive/route-target.yaml` → `creation-routing.test.yaml` | The router rejects incomplete, failed, cancelled, timed-out and mismatched results, including targets already present in the registry. |
| P0 | Integration / Native | `recipes/adaptive/route-target.yaml` → `creation-routing.test.yaml` | Creation's empty hash is never passed to thinpackrebase. |
| P1 | Integration / Native | `recipes/adaptive/prompts.yaml` → `creation-routing.test.yaml` | Creation instructions request names, repository identities and exact purposes without promising root configuration approval or catalog edits. |

Publication diagnostics and partial results have additional
[expectations](creation-publication-statements.md).

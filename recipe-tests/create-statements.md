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

## Optional request titles

These expectations supplement the existing creation contract. Native dependencies
include the pinned c2j runtime and the declared Nix tools.

| ID | Priority | Kind / dependencies | Relevant files | Expectation |
| --- | --- | --- | --- | --- |
| T1 | P1 | Integration / c2j, Nix | `create.yaml`, `recipes/create/review.yaml`, `recipe-tests/create.test.yaml` | A supplied title reaches the proposal agent as labeled context alongside the unchanged full prompt. |
| T2 | P1 | Integration / c2j, Nix | `create.yaml`, `recipes/create/review.yaml`, `recipe-tests/create.test.yaml` | Unicode, quotes, newlines and template-like title text remain literal without changing the request details. |
| T3 | P1 | Integration / c2j, Nix, Git | `create.yaml`, `recipe-tests/create.test.yaml`, `recipe-tests/create-handoff.test.yaml` | Omitted and empty titles preserve existing creation outcomes and add no empty title heading. |
| T4 | P1 | Integration / c2j | `create.yaml`, `recipe-tests/create-title-inputs.test.yaml` | Numeric, boolean, list, object and null titles fail validation before any operation or human review. |
| T5 | P0 | Integration / c2j | `create.yaml`, `recipe-tests/create-title-inputs.test.yaml` | A title without the required prompt fails validation before any operation or human review. |
| T6 | P0 | Integration / c2j, Nix, Git | `recipes/create/review.yaml`, `recipe-tests/create.test.yaml` | A titled request creates only the identities and exact purposes approved by the human, even when the title suggests another name. |
| T7 | P0 | Integration / c2j, Nix, Git | `recipes/create/review.yaml`, `recipe-tests/create.test.yaml` | Cancelling or declining a titled request registers no cells and publishes no repositories. |
| T8 | P1 | Integration / c2j, Nix, Git | `recipes/create/review.yaml`, `recipe-tests/create-title-handoff.test.yaml`, `recipe-tests/fixtures/create-title-handoff.yaml` | A supplied consultation session receives the title and full prompt while retaining its documents and session continuity. |
| T9 | P0 | Integration / c2j, Nix | `recipes/create/review.yaml`, `recipe-tests/create.test.yaml` | Feedback on a titled proposal reaches the resumed agent and requires another review before creation. |
| T10 | P1 | Integration / c2j, Nix | `recipes/create/review.yaml`, `recipe-tests/create.test.yaml` | Supplying a title preserves the existing creation and clarification review headings. |

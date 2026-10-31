# Creating cells

[`create.yaml`](../../create.yaml) must run as a job owned by the configured project
root. It accepts `prompt`, optional consultation `session` and `documents`, and
`root_cell`/`root_ref`. Both build paths submit this root-owned child directly for
explicit creation requests or targets that cannot yet serve a consultation.
There is no separate eligibility-only consultation before the creation workflow.

Creation has three publication boundaries:

1. `review.yaml` assesses project fit, existing owners, alternatives, repository
   destinations, technology choices, and initial responsibilities. It prepares
   `proposal.md`, each `cells/<name>/PURPOSE.md`, and `root-config.yaml`, containing
   the exact proposed root configuration. Initial repository contents are limited
   to the approved purpose; application features remain separate work. Human
   approval covers repository identities, initial contents, and catalog changes
   together. Feedback or annotations require another review. Clarification,
   rejection, or cancellation never authorizes publication or root edits.
2. `publish.yaml` resolves an `initial: empty` workspace and submits a separate
   `initialize.yaml` job inheriting that empty workspace. The child is owned by
   the destination cell, receives the exact approved purpose and approval artifact,
   and publishes `main` through `squashrebasemerge`. It does not fetch an absent
   target or discover a recipe from that target. `initialize_recipe` defaults to
   the shared initialization selector; override it to test an unpublished revision.
   The root job never pushes the new repository itself.
3. After all initializations succeed, root checks that its catalog has not changed
   since proposal preparation, validates the proposed configuration, and copies
   the approved bytes into `.c2/config.yaml`. Existing settings, dependent entries,
   and discovery configuration must be preserved. The root agent verifies registration
   read-only and supplies `completion.md`; it cannot silently rewrite approved
   contents. Root publishes its catalog change separately.

The native runtime preserves the parent repository while each child publishes
independent initial history. Gitvend may create an authorized missing repository
on this ordinary push. Other Git servers require a provisioned destination.
Recipes do not issue Git bootstrap commands or repository-creation API calls.

## Results and recovery

Successful output has `disposition: created`, `merged: true`, `created_cells`
with actual repository/ref/revision, the root `merged_hash`, and review/artifact
references. `initializations` retains child-job identities and errors, including
partial publication. Callers require the domain outcome and matching published
identity; a completed child job alone does not mean a cell is ready.

An existing destination branch is never overwritten. Initialization failures
return `publication_failed`, without starting registration. Catalog application
failures enter a human recovery loop; retry only reapplies the approved catalog,
never publication. Cancellation retains published cells and reports
`registration_failed`. If root changed during review, reconcile that change
before retrying; do not overwrite newer configuration.

Incomplete registration evidence resumes the same read-only session. Two automatic
response corrections are followed by human direction or cancellation. Declared
registration failure (`completed: false`) or a rejected catalog merge returns
`registration_failed` with publication evidence retained. Multiple repositories
are not an atomic transaction. Do not restart the entire creation request or
remove successful repositories to recover a later failure. Lost push acknowledgements
and task replay use c2j's publication reconciliation rather than a fresh child.

## Routing and light work

`kernel/resolve-target.yaml` probes identity/ref availability without a target
checkout. Local absence, empty repositories, missing refs, and unresolved access
remain distinct. Remote private-404, authorization, and transport errors are
unknown, not proof of absence. Root must resolve eligibility and obtain approval
before initializing; a readable existing branch is never initialized over.

`kernel/route-target.yaml` retains the original request and creation job. Stable
keys and matching recorded destinations reuse creation outcomes within the parent
workflow. Distributed deduplication across independent parents is not provided;
Git publication still refuses an existing destination branch.

Delegation-only creation can stay light: root performs architecture and human
review. For a feature request, successful creation is followed by serving-cell
consultation and its own build. Creation does not satisfy the feature request.
Failed or unrelated creation outcomes cannot authorize serving consultation.

Native suites use disposable repositories, real child jobs, artifacts, reviews,
and Git publication with mocked model decisions. Live gateway authorization and
remote repository provisioning remain deployment integration checks. See
[recovery and creation expectations](../../recipe-tests/recovery-creation-statements.md).

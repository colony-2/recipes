# Creating cells

[`create.yaml`](../../create.yaml) runs as a job owned by `root` in an explicit
root workspace. Its ownership guard runs before review or registration and does
not read or capture root configuration. The inputs remain `prompt`, optional
consultation `session`, `documents`, `annotations`, `root_cell`/`root_ref`, and an
optional `initialize_recipe` selector.

Creation has two boundaries:

1. [`review.yaml`](review.yaml) assesses project fit, existing owners, alternatives,
   technology choices, cell names and repository destinations. It prepares
   `proposal.md` and each exact `cells/<name>/PURPOSE.md`. Missing identities,
   missing purposes and empty purposes require correction before review or
   registration. Human approval binds identities and exact initial purposes.
   Feedback or annotations require another review. Clarification, rejection and
   cancellation authorize no registration or publication.
2. [`publish.yaml`](publish.yaml) registers each approved cell, then submits and
   awaits its destination-owned [`initialize.yaml`](initialize.yaml) job. Every
   required registration and initialization must succeed before creation completes.
   Initial repository contents consist exclusively of the approved purpose, on
   `main`, with independent history. Creation does not complete product features.

[`register-cell.yaml`](register-cell.yaml) gives `perms.jobdb.cells.create: true`
only to the `c2j cell create` command. The owning job ID and cell name form its
stable request ID. Conflicts fail without initialization; a retry within the same
job reconciles the original registration. The deployment must separately authorize
submission to the destination cell. Registration grants no submission authority.
The cell name selects the workspace; the repository locator is an assertion against
its registered identity.

The initialization child receives the exact approved purpose and approval artifact.
It publishes through `squashrebasemerge` in empty-workspace mode, preserving the
existing configured Git identity and runtime fallback behavior. This operation is
retained because separate squash changed the configured committer in earlier
runtime validation. Gitvend may create an authorized missing repository through
this ordinary push; other Git servers need a provisioned destination. An existing
branch is never overwritten. Use `initialize_recipe` to test an unpublished child
revision without discovering a recipe in an empty destination repository.

## Completion and partial results

Successful output has `disposition: created`, `merged: true`, and
`merged_hash: ""`. The boolean is the legacy alias for completed creation; it
identifies no root commit. Root configuration, tree and history are untouched by
creation, including legacy dependents and unrelated settings. Concurrent root
writers can advance independently.

Results retain `created_cells` with actual repository/ref/revision,
`initializations` with child identities and errors, annotations, review and artifact
references, and the approved review session. Both retained adaptive routers require
successful creation and matching published identity before returning a ready target.
They accept the empty root hash and do not pass it to `thinpackrebase`.

Required child waits propagate publication failures, timeouts and cancellation
without reporting readiness or replacing original diagnostics. Registration evidence
remains in each registration operation's `registration.json`. Before each wait and
after each completed initialization, [`publication-record.yaml`](publication-record.yaml)
persists `created.json` and `initializations.json`. These retain earlier publications
and the failing child identity even when final outputs are unavailable. A pending
record describes the checkpoint before waiting, not the child's eventual status.
Inspect that child for its terminal diagnostics.

Multiple repositories are not an atomic transaction. Later failure preserves earlier
registrations and publications; it does not roll them back. Do not restart an entire
request or remove successful repositories to recover a later failure. Lost push
acknowledgements use the runtime's existing publication reconciliation.

There is no root-config proposal, copying, recovery, final catalog-verification
agent, root squash or root merge. Root coordinates rollout for older jobs that
captured catalog-writing recipes and for pinned callers. Publish this recipes
change through the managed adaptive3 lifecycle before root cleanup is published.

Native acceptance uses seeded disposable repository references, real registration
and permission probes, child jobs, reviews, artifacts and Git publication with
scripted model responses. See [creation expectations](../../recipe-tests/create-statements.md),
[publication expectations](../../recipe-tests/creation-publication-statements.md),
and [historical validation](../../recipe-tests/creation-publication-validation.md).

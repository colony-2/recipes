# Creating cells

[`create.yaml`](../../create.yaml) runs in the project root and accepts `prompt`,
an optional serving consultation `session`, and `documents`. Optional
`root_cell`/`root_ref` select the root explicitly; otherwise it uses the current
cell. Build submits it after a root consultation agrees that new cells are
appropriate.

The recipe composes three steps:

1. `review.yaml` continues the serving session, inspects project fit and existing
   owners, and writes a consolidated proposal plus each initial purpose. Review
   covers purposes, excluded alternatives, technology choices, repository URLs,
   and root catalog changes. New cells always start on `main`; the model does
   not select a branch. Questions and annotations use the shared
   review kernel. Clarification can precede any proposal: questions are required,
   documents are optional, and unresolved optional references do not trigger repair.
   Answers continue proposal preparation without authorizing creation.
   Changes require another review; cancellation or redirection
   publishes nothing.
2. `publish.yaml` opens one `initial: empty` workspace per approved cell, copies
   its approved purpose artifact to `PURPOSE.md`, and calls `squashrebasemerge`.
   Gitvend creates missing repositories during the normal authorized push.
3. The root session resumes with `created.json` containing actual publication
   results. It updates the existing `.c2/config.yaml` dependents catalog and
   applicable descriptions. A separate merge publishes those root changes.

The initial purpose files are reviewed assets, not generated again at publication.
Creation does not implement application features. The requester starts a new
consultation in each created cell before submitting its feature build.

Successful output has `disposition: created`, `created_cells` with names, URLs,
branches, and revisions, the root's `merged_hash`, the final `session`, and
`artifact_refs` containing the proposal, purposes, publication records, and
completion summary. Declined, redirected, or cancelled proposals have no created
cells and `merged: false`. Artifact references are resolved with `path_match` before
semantic checks. Missing or ambiguous documents and other correctable responses
resume the same session, preserving produced documents. After two corrections,
a human review requests direction or cancellation; it does not approve creation.
An operation failure returns `disposition: invalid` without publishing.

## Runtime and failures

Requires the c2j revision in [native testing](../../guides/NATIVE_RECIPE_TESTING.md)
for `.c2/` configuration and empty workspaces; see the
[empty-workspace guide](../../guides/GUIDE-Empty-Workspaces.md).
c2j manages initialization, commits, default identity, and first publication.
Recipes do not issue Git bootstrap commands or make repository creation API calls.

An existing destination branch fails publication without overwriting it.
Publication errors return `publication_failed` before registration; incomplete
registration or a rejected root merge returns `registration_failed`. Both have
`merged: false`; callers must check the disposition before accepting the prerequisite.
The output includes the error and any cells already published successfully.
Incomplete registration evidence is corrected in the same session with read-only
Git access. That loop never repeats publication or registration edits. A declared
registration failure (`completed: false`) returns for deliberate follow-up.
Multiple repositories are not an atomic transaction:
earlier successful publications remain if a later operation fails. Inspect the
job's recorded publication results and finish the remaining work deliberately;
do not restart the entire creation request or delete successful repositories.

c2j currently defers reconciliation when a push succeeds but its task outcome
is lost. Retrying that task can encounter the already-created branch. This
recipe has no automatic retry or workaround for that runtime limitation.

The native suites use real empty workspaces, artifact persistence, reviews,
and Git publication with mocked model decisions. Disposable local repositories
exercise first publication on an absent branch; live gitvend authorization and
GitHub repository creation are separate deployment integration checks. Test
fixtures supply an explicit Git identity and verify it is honored; bot fallback
and worker-recovery guarantees belong to c2j's runtime tests.

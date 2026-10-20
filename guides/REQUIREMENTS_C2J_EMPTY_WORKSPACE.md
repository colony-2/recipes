# c2j requirements: empty workspaces and first publication

Status: implemented in c2j main `a058abe015e556ee7264ded665c47efe95959235`,
except lost-push-outcome reconciliation, which c2j explicitly defers.
See [the usage guide](GUIDE-Empty-Workspaces.md) for the supported contract.
The requirements below retain the original request; the current-gap section
describes the earlier v0.0.83 inspection.
Requested by: recipes cell. Implementation owner: c2j.
Date: 2026-10-20.

## Outcome

A recipe can start with an empty repository, write its initial contents, and
publish through the normal Git persistence and merge/push workflow. When the
remote is served by gitvend, that ordinary push creates the repository if
authorized. The recipe does not need a separate repository-creation operation
or custom Git bootstrap script.

c2j must also supply the default Git identity used in this repository:

```text
colony2.com <col2bot@colony2.com>
```

This name and email were verified from local Git configuration and recent
commits. They are the intended defaults, rather than the tentative name `c2bot`.

## Current gap

Inspection of c2j commit
[`a3a330212958723c1ab9cb2a867b2147a27883c8`](https://github.com/colony-2/c2j/tree/a3a330212958723c1ab9cb2a867b2147a27883c8)
(v0.0.83) found three assumptions that prevent this workflow:

- `pkg/worker/compiler/workspace.go` resolves a remote ref to an existing commit
  before preparing a workspace.
- `pkg/git/gitcommit/persist.go` requires an existing root commit and `HEAD`,
  and constructs persistence artifacts relative to existing history.
- `pkg/git/squashrebasemerge/operation.go` fetches the target branch and resolves
  its tip before publication.

`pkg/git/common/author.go` currently supplies `c2j <c2j@colony2>` or an identity
derived from the cell name. Those automatic fallbacks should use the verified
bot identity above.

## Required behavior

### 1. Explicit empty starting state

Provide an explicit way to select an empty initial Git state for a workspace,
including one used by a child job. Repository destination and target branch
remain ordinary workspace inputs.

Illustrative syntax only; c2j owns the final API:

```yaml
workspace:
  cell: ${{ inputs.repository }}
  ref: ${{ inputs.branch }}
  initial: empty
```

An empty-base sentinel is an acceptable internal representation. It must be
distinct from an unresolved or missing value and must never be passed to Git
as though it names a commit. Do not manufacture a placeholder commit.

Preparing this workspace must initialize a local repository on the requested
branch without requiring a successful remote fetch or an existing remote
repository. Preparation must not create or modify anything remotely.

Empty mode is explicitly requested. A failed fetch, missing ref, authentication
failure, or network error in an ordinary workspace must not silently select it.

### 2. Normal persistence from the first change

Operations see the ordinary worktree, inbox, and outbox layout. The first
operation that changes repository contents is persisted as a real root commit
with no parent. An operation that makes no changes leaves the repository empty.

Native persistence must support both the unborn repository and its first commit.
Artifacts for the first commit must be restorable without a nonexistent parent
or base prerequisite. Later operations, worker changes, job resumption, and child
workspace handoffs must retain the correct state through the normal mechanisms.

Once a real commit exists, expose its actual hash through normal Git context.
Represent the absent initial base explicitly; do not expose a fabricated commit
hash. Preserve that distinction until first publication has completed.

This state belongs to the selected workspace. Creating another cell must not
replace the requesting or root cell's Git state.

### 3. First publication through the existing merge/push operation

Extend the ordinary publication operation to handle an explicitly empty base.
It must publish the persisted initial commit without requiring the destination
branch to exist or calculating a merge base against nonexistent history.

Use the configured repository URL, branch, credentials, and Git transport.
gitvend performs repository creation during receive-pack discovery on an
authorized push; no separate provisioning API is required. See
[gitvend's first-push behavior](https://github.com/colony-2/gitvend/blob/3850cc249964a1457b88d810a76f293143798e90/README.md).

Publication must require the destination branch to remain absent, with that
condition enforced at the push itself. A concurrently created branch must not
be overwritten or silently adopted as the base of unrelated history. An
existing repository with an absent target branch can use the same first-branch
publication behavior.

The usual successful publication outputs must identify the published commit
and branch. Subsequent ordinary jobs must resolve that repository normally.
Permission and transport failures must remain failures, with enough context
to diagnose the failing stage.

Keep publication at the recipe's existing approved merge/push boundary.
Workspace initialization and read-only operations must not trigger receive-pack
discovery, including a dry-run push: gitvend can create a repository during
that discovery even if no commits are pushed.

### 4. Durable retries

Persisted commits must survive retries and resumption without regenerating
unrelated initial history. If a push succeeds but its response is lost, c2j
must reconcile the already-published result using its normal durable execution
mechanisms. An exact previously published result may count as success; different
remote history must not be overwritten.

An empty remote repository left by an interrupted first push must remain
retryable. Neither case should require recipe-owned receipts, bundles, or a
separate recovery workflow.

### 5. Automatic Git identity

Use `colony2.com <col2bot@colony2.com>` as the default committer for automated
commits when no identity is explicitly configured. Apply the same fallback
author identity when c2j creates a new commit without an explicit author.
Replace synthesized cell-name identities as automatic defaults.

Honor explicit operation identity and configured Git identity overrides under
the normal precedence rules. Preserve original authors where an operation's
existing semantics preserve authorship; author and committer are distinct.

The defaults must work without host-global Git configuration, including in
new empty workspaces, restored workspaces, persistence, and merge/rebase
operations that create commits. Set identity within the operation or workspace;
do not modify the user's global Git configuration. Ordinary existing-repository
jobs receive the same fallback.

## Recipe integration

The creation recipe carries the approved purpose document into the new empty
workspace, writes `PURPOSE.md`, and uses the normal publication step. It returns
the new cell identity and published revision for subsequent consultation/build.
Purpose review, overlap assessment, and technology guidance remain recipe
responsibilities. Application feature implementation follows the normal build
workflow after creation.

This request covers Git initialization, persistence, publication, and identity.
gitvend remains responsible for remote creation authorization and upstream
credentials. No additional repository provisioning service is required.

## Acceptance tests

These are proposed c2j test statements, not tests executed by this document.
File references identify implementation areas; c2j should place tests alongside
the relevant implementations.

| Test statement | Priority | Type / dependencies | Relevant files |
| --- | --- | --- | --- |
| Explicit empty initialization succeeds without a remote repository and performs no remote writes. | Critical | Integration / Git | `pkg/worker/compiler/workspace.go` |
| Failed ordinary workspace resolution never silently initializes empty history. | Critical | Integration / Git | `pkg/worker/compiler/workspace.go` |
| A read-only operation leaves an empty workspace without commits or remote side effects. | High | Integration / Git | `pkg/git/gitcommit/persist.go` |
| Writing PURPOSE.md produces a restorable root commit with no parent. | Critical | Integration / Git | `pkg/git/gitcommit/persist.go`, `pkg/git/gitstate/workspace_controller.go` |
| Resumption on another worker preserves empty state or the previously persisted first commit, as appropriate. | Critical | Integration / Git, worker persistence | `pkg/git/gitstate/workspace_controller.go` |
| Creating a child workspace preserves the parent cell's repository and revision. | Critical | Integration / Git, child jobs | `pkg/worker/compiler/workspace.go` |
| Ordinary publication creates an authorized missing gitvend repository and publishes the expected branch and files. | Critical | Integration / Git, gitvend, disposable upstream | `pkg/git/squashrebasemerge/operation.go` |
| First publication succeeds when the repository exists but the destination branch is absent. | High | Integration / Git | `pkg/git/squashrebasemerge/operation.go` |
| A concurrently created destination branch is preserved and publication reports a conflict. | Critical | Integration / Git | `pkg/git/squashrebasemerge/operation.go` |
| Denied repository creation reports failure without claiming successful publication. | Critical | Integration / Git, gitvend | `pkg/git/squashrebasemerge/operation.go` |
| Retrying after a lost push response recognizes the published result without creating replacement history. | Critical | Integration / Git, failure injection | `pkg/git/squashrebasemerge/operation.go` |
| Retrying after remote creation without branch publication completes the original first push. | High | Integration / Git, gitvend, failure injection | `pkg/git/squashrebasemerge/operation.go` |
| Without configured identity, automated commits use the specified bot author and committer, including after workspace restoration. | Critical | Integration / Git, isolated configuration | `pkg/git/common/author.go`, `pkg/git/gitstate/workspace_controller.go` |
| Explicit identities override defaults; operations preserving authorship retain the original author. | High | Integration / Git | `pkg/git/gitcommit/persist.go`, `pkg/git/squashrebasemerge/operation.go` |
| Existing-repository persistence and publication retain normal history behavior without modifying global Git configuration. | High | Integration / Git | `pkg/git/gitcommit/persist.go`, `pkg/git/squashrebasemerge/operation.go` |

## Delivery

c2j should document the supported empty-workspace syntax, its context/output
representation, and first-publication behavior, with native tests demonstrating
the lifecycle above. The recipes cell can then wire `create` to that contract
without adding a custom bootstrap/push path.

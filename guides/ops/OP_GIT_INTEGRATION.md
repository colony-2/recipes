# Separate Git integration ops

Use c2j's native `rebase`, `squash`, and `merge` operations when the recipe needs
explicit preparation, review, and publication boundaries. These ops are available
in c2j v0.0.104 and later. They operate on the managed task worktree and must not
be marked `const`.

| Op | Inputs | Result |
| --- | --- | --- |
| `rebase` | Required `target_base_hash`; execution base and HEAD default automatically | Replays local work onto the target and updates the persisted workspace base; returns `new_base_hash` and `new_persist_hash`. |
| `squash` | `commit_message`, optional `author` and `base_hash` | Replaces local commits after the execution base with one commit, preserving the tree; returns `squashed_hash`. |
| `merge` | Optional `upstream_repo` and `upstream_branch`, defaulting to the current repository and ref | Publishes the prepared HEAD by fast-forward; returns `merged_hash` and `target_branch`. |

`rebase` shares the [thinpackrebase contract](OP_THINPACKREBASE.md), including
ancestry checks and fetching missing history. Its target must descend from the
workspace base and initial commit. The recipe can resolve the current branch tip
with `git ls-remote --exit-code` before supplying `target_base_hash`.

Build orders these operations around its existing gates:

1. Rebase the implementation onto the current target tip.
2. Independently inspect and verify the rebased candidate, then account for every file change.
3. Ask the human to accept the accounting, outcome, and proposed commit message.
4. Squash using that message, then merge the resulting commit.

Squashing after review changes commit history but preserves the reviewed tree.
After rebasing, repeat verification and review any changed local candidate. `merge`
does not rewrite the candidate or force-update existing history. Retrying `merge` reuses the saved
candidate and succeeds if that commit is already published, including when it
is an ancestor of the current target.

When `merge` reports `MERGE_UPSTREAM_ADVANCED`, both build paths return to
rebase and resolve the latest upstream tip. Verification always runs again.
If the local changes are identical, the existing approval and commit message
are reused without another assessment, accounting session, or human review.
If rebasing eliminates all local changes, successful verification completes
the job without another review or merge. If the local changes differ, the
normal review gates run again. Up to **three chases** are
allowed after the initial merge attempt; a fourth stale failure propagates from
the merge op. Revisions and light-to-heavy escalation retain the consumed budget.
Squash failures, unrelated merge errors, and rebase conflicts propagate normally.

Approval reuse compares a digest of the local Git changes: paths, before/after
blob IDs, and file modes, with renames represented as deletion/addition. Commit
IDs and unrelated upstream files do not affect it. Changes to reviewed files,
including binary content, symlink targets, or executable bits, require renewed
review. This exception applies only after an approved merge enters the chase
loop; initial no-change outcomes and implementation repairs keep their normal
review requirements.

This requires c2j's structured advancement contract, documented in its
`GUIDE-Git-Ops.md`. The contract exists in c2j revision
`db32d4246b20df452e283cf0de4657fb6462fb11`; npm release `0.0.107` still returns an
unclassified divergence error and therefore cannot activate the chase loop.
Use a c2j build/release containing that contract. Keep enclosing and job retry
policies at one attempt so they do not restart the development workflow after
its chase budget is exhausted. See the
[contract and acceptance requirements](../REQUIREMENTS_MERGE_UPSTREAM_ADVANCED.md).

These operations require clean, committed workspaces; ordinary preceding writing
ops persist their changes automatically. For an empty workspace, use `squash`
then `merge` without `rebase`; initial publication requires an absent destination
or recognition of the already-published candidate.

The composite [squashrebasemerge op](OP_SQUASHREBASEMERGE.md) remains available
to other recipes. Build deliberately uses the separate operations.

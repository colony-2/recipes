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
Do not rebase after approval without repeating verification and review. `merge`
does not rewrite the candidate or force-update existing history. If the target
advances incompatibly, the error propagates. Retrying `merge` reuses the saved
candidate and succeeds if that commit is already published, including when it
is an ancestor of the current target.

These operations require clean, committed workspaces; ordinary preceding writing
ops persist their changes automatically. For an empty workspace, use `squash`
then `merge` without `rebase`; initial publication requires an absent destination
or recognition of the already-published candidate.

The composite [squashrebasemerge op](OP_SQUASHREBASEMERGE.md) remains available
to other recipes. Build deliberately uses the separate operations.

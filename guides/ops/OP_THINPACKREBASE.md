# thinpackrebase Op

Rebases a thin-pack backed workspace onto a new base commit and returns updated git metadata for downstream ops.

For the managed workspace, supply only the target commit:

```yaml
- id: refresh
  op: thinpackrebase
  inputs:
    target_base_hash: '${{ sequence.child.outputs.outputs.merged_hash }}'
```

Use c2j commit `ee1420b12dee` or later. `base_hash` defaults to
`{{ context.git.execution.base_hash }}` and `persist_hash` to
`{{ context.git.execution.head_hash }}`. These resolve after workspace restoration:
the base is beneath pending local commits, while HEAD includes them. Do not use
`context.git.resolved_hash` as a substitute; it can intentionally remain empty
before a job commits to a hash. Execution references are for op inputs, not routing.

The op obtains enough shallow history to establish ancestry, preserves pending
commits, and records the updated persistence base for later tasks. Divergent
history, unavailable ancestry, uncommitted changes, and conflicts remain errors.
The `git_context_patch` output is descriptive; the native op applies an explicit
workspace persistence update. Arbitrary outputs with that name do not update it.

## Input Structure

```json
{
  "repo_path": "/path/to/repo",
  "target_base_hash": "abc1234",
  "upstream_remote": "origin",
  "preserve_author": true,
  "update_refs": "refs/heads/main",
  "base_hash": "def5678",
  "persist_hash": "fedcba9",
  "base_repo": "git@example.com:org/repo.git",
  "git_author": "Jane Doe <jane@example.com>",
  "cell_name": "api"
}
```

## Output Structure

```json
{
  "target_base_hash": "abc1234",
  "new_base_hash": "0123abc",
  "new_persist_hash": "4567def",
  "updated_ref": "refs/heads/main",
  "rebased_from": {
    "base_hash": "def5678",
    "persist_hash": "fedcba9"
  },
  "git_context_patch": {}
}
```

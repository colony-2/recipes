# Bug Report: `c2j test` Rejects Built-In Ops Inside Inline Included Recipes

## Summary

`c2j test compile`, `c2j test validate`, and `c2j test run` fail while
resolving a local inline recipe when the included recipe contains the built-in
`squashrebasemerge` op.

The same included recipe compiles successfully when tested directly as the
top-level recipe. Embedded runtime execution also resolves and runs the
production inline recipe successfully. This suggests the test inline resolver is
parsing included recipe files with a different op registry or validation path
than top-level recipe parsing.

## Version

Observed with:

```text
c2j version v0.0.30-0.20260610211650-78765e1505de
/usr/local/bin/c2j sha256 557f643bfbc931e6da8a3b134b06f7b05c247f401ea9ea137b59cf6aac9c6ee3
```

## Minimal Reproduction

Create `child.yaml`:

```yaml
id: child-with-merge-op
version: "1.0"
desc: Child recipe that uses a built-in merge op
state:
  initial: merge
  states:
    merge:
      op: squashrebasemerge
      transitions: []
      inputs:
        repo_path: "{{ context.environment.op.worktree_path }}"
        local_hash: "0000000000000000000000000000000000000000"
        upstream_repo: "git@example.com:org/repo.git"
        upstream_branch: "main"
        rebase: true
        author: ""
        commit_message: "test merge"
outputs:
  merged_hash: "${{ state_output('merge', 'merged_hash', '') }}"
```

Create `child.scenario.md`:

````markdown
```yaml
cases:
  - id: child-merge-op-direct
    type: recipe_case
    inputs: {}
    mocks:
      ops:
        - match:
            op: squashrebasemerge
          behavior:
            mode: return
            outputs:
              target_branch: main
              remote_ref: refs/heads/main
              merged_hash: abc123
              squashed_commits:
                base_hash: base123
                persist_hash: persist123
              git_context_patch: {}
              fast_forward: true
    assertions:
      - type: output_equals
        path: merged_hash
        value: abc123
```
````

Create `parent.yaml`:

```yaml
id: parent-inline-child-with-merge-op
version: "1.0"
desc: Parent recipe that inlines a child recipe using a built-in merge op
state:
  initial: child
  states:
    child:
      include: ./child.yaml
      transitions: []
      inputs: {}
outputs:
  child_merged_hash: "${{ state_output('child', 'merged_hash', '') }}"
```

Create `parent.scenario.md`:

````markdown
```yaml
cases:
  - id: parent-inline-child-merge-op
    type: recipe_case
    inputs: {}
    mocks:
      ops:
        - match:
            op: squashrebasemerge
          behavior:
            mode: return
            outputs:
              target_branch: main
              remote_ref: refs/heads/main
              merged_hash: abc123
              squashed_commits:
                base_hash: base123
                persist_hash: persist123
              git_context_patch: {}
              fast_forward: true
    assertions:
      - type: output_equals
        path: child_merged_hash
        value: abc123
```
````

Run the direct child control:

```bash
c2j test compile \
  --recipe-file ./child.yaml \
  --file ./child.scenario.md \
  --out /tmp/child.compiled.json \
  --strict
```

Run the inline parent case:

```bash
c2j test compile \
  --recipe-file ./parent.yaml \
  --file ./parent.scenario.md \
  --out /tmp/parent.compiled.json \
  --strict
```

The same failure also occurs with:

```bash
c2j test validate \
  --recipe-file ./parent.yaml \
  --file ./parent.scenario.md \
  --parallelism 1

c2j test run \
  --recipe-file ./parent.yaml \
  --file ./parent.scenario.md \
  --parallelism 1 \
  --artifact-mode inline \
  --out-dir /tmp/parent.run \
  --evaluation-mode enforce
```

## Expected Result

The parent recipe should resolve `./child.yaml` and accept `squashrebasemerge`
inside the included recipe, just as `c2j test compile` accepts it when
`child.yaml` is compiled directly.

Expected command behavior:

- direct child `compile` succeeds;
- inline parent `compile` succeeds;
- inline parent `validate` succeeds;
- inline parent `run` executes the mocked `squashrebasemerge` op and passes the
  `child_merged_hash == abc123` assertion.

## Actual Result

The direct child compile succeeds, but the inline parent test commands fail
before execution:

```text
Error: resolve inline recipes: resolve include "./child.yaml" at root/child:
parse local recipe "<path>/child.yaml": unknown op: [squashrebasemerge] at [0:0]
```

## Production Recipe Observation

The same issue is visible in the Superpowers production recipe:

```bash
c2j test compile \
  --recipe-file recipes/superpowers/superpowers.yaml \
  --file recipes/superpowers/tests/superpowers.scenario.md \
  --out /tmp/superpowers.inline-test.compiled.json \
  --strict
```

Actual result:

```text
Error: resolve inline recipes: resolve include "./superpowers-finish.yaml" at root/finish_work:
parse local recipe "/src/recipes/superpowers/superpowers-finish.yaml": unknown op: [squashrebasemerge] at [0:0]
```

The included recipe compiles successfully on its own:

```bash
c2j test compile \
  --recipe-file recipes/superpowers/superpowers-finish.yaml \
  --file recipes/superpowers/tests/superpowers-finish.scenario.md \
  --out /tmp/superpowers-finish.standalone.compiled.json \
  --strict
```

Result:

```text
compiled 3 case(s) to /tmp/superpowers-finish.standalone.compiled.json
```

Embedded runtime execution of the production inline recipe also succeeds:

```bash
recipe-tests/verify-superpowers-inline-primary-live.sh
```

Result:

```text
TS-094 passed
```

## Impact

Production recipes can use local inline includes in embedded execution, but
local `c2j test` coverage cannot compile, validate, or run an inline recipe
graph if an included phase recipe uses `squashrebasemerge`. This prevents the
production Superpowers recipe from replacing its temporary primary
compile-only test workaround with full `c2j test validate/run` coverage.

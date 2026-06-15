---
title: "Git State"
weight: 44
---

c2j maintains git state between recipe ops for the current cell.

Author-facing rules:

- Work in `context.environment.op.worktree_path`.
- Do not manually pass the internal thin-pack artifact.
- Changes made by an op are persisted for later ops.
- If no changes are made, the previous git state passes through.
- Merge/rebase ops should be used only when the workflow is ready to integrate.

Useful context:

```yaml
context.git.repo
context.git.ref
context.git.resolved_hash
context.git.hash
context.git.parent_hash
context.invocation.hash
```

Integration ops:

- `thinpackrebase`: rebase recipe git state onto an upstream ref.
- `squashrebasemerge`: squash and merge recipe git state back to the base repo/ref.

GitHub Actions ops from `c2ops` run validation workflows but do not automatically write back into recipe git state. Use them for checks, not as a replacement for c2j git persistence.


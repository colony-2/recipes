# Scoped Codex directory does not imply a scoped writable sandbox

Owners: c2j process sandbox and c2ops Codex launcher.

## Expected behavior

A recipe should be able to run Codex in a cell subdirectory, allow writes only
there plus operation scratch/output storage, and preserve the complete cell's
git persistence. For evolve, application files outside `.c2j` should be readable
when necessary but not writable.

## Source-confirmed current behavior

In the checkouts inspected on 2026-09-27:

1. `/c2ops/codex/pkg/codex/command.go` always passes
   `--dangerously-bypass-approvals-and-sandbox`. There is no recipe input for
   selecting Codex's native sandbox.
2. `/c2ops/codex/pkg/codex/execute.go` uses `Options.WorktreeRoot` as `cmd.Dir`.
   Overriding `worktree_path` therefore changes the starting directory, as
   confirmed by a disposable launcher probe using a stub Codex executable.
3. `/c2j/pkg/ops/process/runtime.go`, `executeInShai`, configures
   `ReadWritePaths: []string{"."}` for the operation workspace. The extension
   runner uses the host operation workdir as that workspace.
4. `filterWorkspaceCoveredMounts` drops mappings covered by the workspace
   mapping without checking whether the requested mode is more restrictive.
   A covered read-only mapping cannot be assumed to narrow that writable mount.

Consequently this recipe input changes cwd and enables the outer sandbox, but
does not establish a `.c2j`-only write boundary:

```yaml
worktree_path: '{{ context.environment.op.worktree_path }}/.c2j'
sandbox:
  type: shai
```

This is a source-level finding, not a completed live container reproduction.
The authoring environment has no Docker runtime. Do not report subdirectory
write isolation as tested based on the launcher probe alone.

## Requested fix and regression coverage

Expose a supported write-scope configuration independent of cwd and git root,
and honor restrictive mount modes without broader writable aliases. Either
support a correctly configured native Codex sandbox or enforce the scope in the
outer sandbox. Preserve inbox reads, outbox/scratch writes, and session resume.

The integration test should run in `.c2j`, successfully create a recipe there,
fail to write a sibling application file through any mounted alias, and preserve
both scoped changes and session artifacts through c2j checkpoints. Include
symlink escapes, covered read-only mounts, and resumed sessions.

The shared development recipes enable Shai and enforce changed-file scope gates
after agents and before merge. Those gates detect violations; they do not claim
to prevent the original write.

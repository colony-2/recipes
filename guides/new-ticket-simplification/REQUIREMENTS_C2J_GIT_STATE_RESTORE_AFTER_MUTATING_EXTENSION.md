# Requirements: Restore Git State After Mutating Extension Ops

## Status

Fixed/validated for the focused Codex mutation-to-command path on 2026-06-09
UTC. Keep this document as the regression contract for future c2j changes.

Bug report:

- `guides/BUG_REPORT_C2J_THIN_PACK_RESTORE_MISSING_PREREQUISITE_COMMITS.md`

## Problem

Recipes depend on C2 git persistence after every mutating op. A Codex task that
changes the worktree must produce git state that the next op can restore and
continue from.

During the original validation, `recipe-tests/verify-codex-skill-execution-live.sh`
ran a live c2ops Codex step that created the expected marker file. The following
`command_execution` probe failed before it could run because c2j could not
restore the prior git state:

```text
restore git state: failed to apply thin pack ... Repository lacks these prerequisite commits
```

This blocks the core Superpowers/C2 pattern: implement with Codex, then run a
deterministic recipe gate against the changed worktree.

The focused rerun on 2026-06-09 UTC passed. The post-Codex command probes
restored git state and did not reproduce the missing prerequisite commit
signature.

## Goals

- A mutating extension op must produce connected git state that later ops can
  restore.
- The next op must see the code changes produced by the previous op without
  explicit recipe-authored thinpack or commit handoff.
- Restore failures must be deterministic, diagnosable, and recoverable.
- The behavior must work in embedded local runs and server-managed jobs.

## Non-Goals

- Do not require recipes to pass commits or thinpacks between normal sequential
  ops.
- Do not add a parent-owned git adoption protocol for the common sequential
  recipe case.
- Do not change the target-ref child-job model.
- Do not make Codex responsible for manual git commits.

## Requirements

### Requirement 1: Connected Git Persistence

After a mutating op completes, c2j must persist enough git object data for any
later op in the same job to restore the resulting worktree.

Acceptance criteria:

- A command op immediately after a mutating extension op can read files changed
  by that extension op.
- Restoring the persisted state never fails with missing prerequisite commits
  when the previous op completed successfully.
- Thin packs or equivalent artifacts include the full commit/object chain needed
  by later restore operations.

### Requirement 2: Retry-Safe Restore

If a later op is retried, c2j must restore the same prior git state each time.

Acceptance criteria:

- Retrying a failed post-Codex command op does not create a new incompatible git
  base.
- Repeated restore attempts do not mutate the persisted predecessor state.
- The job story remains coherent after retries.

### Requirement 3: Job Story Diagnostics

When git persistence or restore fails, diagnostics must identify the relevant
git state.

Diagnostics should include:

- previous op node path;
- base commit;
- produced commit;
- persisted pack or change artifact identifier;
- missing prerequisite commit IDs, when known;
- target ref and cell repository.

### Requirement 4: Minimal Regression Smoke

Add a deterministic live smoke that does not require Codex:

1. An extension or command-like mutating op writes a small repo file.
2. c2j persists git state.
3. A following command op reads the file.
4. The recipe completes in embedded runtime.

Then keep the Codex live smoke as an integration test once the deterministic
smoke passes.

## Superpowers Impact

Before the fix, this requirement was a blocker for:

- task jobs that implement code and then validate in later states;
- TDD RED/GREEN/refactor gates where Codex writes code and command ops prove
  behavior;
- parent recipes that trust child task jobs to advance target refs;
- any recipe loop that alternates Codex edits with deterministic validation.

## Validation Command

The regression command is:

```bash
recipe-tests/verify-codex-skill-execution-live.sh
```

Failure observed on 2026-06-09 UTC after updating the live script to use
`c2j run one`. The same focused command passed later on 2026-06-09 UTC after
the thin-pack restore fix.

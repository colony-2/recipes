# Bug Report: c2j Thin-Pack Restore Missing Prerequisite Commits After Mutating Codex Op

## Status

Fixed/validated. Originally reproduced in live embedded validation on
2026-06-09 UTC; validated fixed with the focused live smoke later on
2026-06-09 UTC.

## Summary

A live recipe that runs a mutating c2ops Codex op could fail on the following
op because c2j could not restore the persisted git state. The restore error
reported that the thin pack was missing prerequisite commits.

The focused regression now passes, so git state is propagating through the
tested mutating Codex-op to command-op path.

## Impact

This blocks recipe patterns that alternate agentic edits and deterministic
validation:

- Codex writes code, then `command_execution` runs tests.
- Codex writes a marker/status file in the repo, then a probe verifies it.
- TDD RED/GREEN/refactor loops persist changes between states.
- Child task jobs make changes that later states validate before completion.

It is especially relevant to the Superpowers recipe port because that port
depends on recipe-enforced gates after Codex implementation steps.

## Reproduction

Run:

```bash
recipe-tests/verify-codex-skill-execution-live.sh
```

The script:

1. Creates a temporary cell repository.
2. Submits `codex-skill-execution-smoke.yaml` through embedded c2j.
3. Runs the submitted job with `c2j run one`.
4. The recipe seeds artifacts, runs a live c2ops Codex implementation step, and
   then runs a `command_execution` probe.

## Expected Behavior

After the Codex op completes successfully, c2j persists connected git state.
The following `command_execution` op restores that state and sees the files
created by Codex.

The probe should run and validate:

- `.c2/live-codex-skill-execution/result.json`
- `implementation/latest-status.json`
- `implementation/summary.md`
- `implementation/progress.ndjson`

## Actual Behavior

The Codex op completed, but the following `command_execution` op failed during
git restore before its probe command could run.

Observed error shape:

```text
restore git state: failed to apply thin pack ... git command failed: exit status 1
error: Repository lacks these prerequisite commits:
error: <commit-id>
```

The failure repeated across retries with different missing prerequisite commit
IDs.

## Evidence From Validation Run

Fixed validation:

- Command: `recipe-tests/verify-codex-skill-execution-live.sh`
- Result: `TS-044 and TS-045 passed`
- The following post-Codex command ops restored git state and completed.
- The live log did not contain `Repository lacks these prerequisite commits`,
  `restore git state`, `failed to apply thin pack`, `workflow state conflict`,
  or chapter ordinal conflict signatures.

Original failing validation:

Representative missing prerequisite commit IDs from the run:

- `22e1b8a1016d4cfa34fe8566937b40e2f72e1b0f`
- `e0d6c3a694cbcaf6de50b1c352052bb78b79f8b1`
- `3bdedf8400795ee397cd3f6ba8a05d8da43f192d`

Representative failing pack paths:

- `/tmp/thin-pack-restore-2184699909/d69e557-22e1b8a-9d38518.pack`
- `/tmp/thin-pack-restore-2783298864/034da23-3bdedf8-9d38518.pack`

## Suspected Area

The persisted git change artifact produced after the mutating Codex extension
op appears not to include the full object chain needed by later restore
operations, or the restore target repository is missing a base object that c2j
expects to be present.

This may involve:

- thin-pack generation after extension ops;
- commit/base selection for post-op persistence;
- restore repository initialization;
- retry behavior after failed restore attempts.

## Acceptance Criteria For Fix

- A deterministic non-Codex smoke can write a repo file in one op and read it in
  the next op through restored git state.
- `recipe-tests/verify-codex-skill-execution-live.sh` passes.
- Retries of the post-Codex probe restore the same prior git state and do not
  create new missing-prerequisite failures.
- The job story exposes enough git metadata to diagnose future restore failures:
  previous op node path, base commit, produced commit, pack/change artifact, and
  target ref.

## Related Docs

- `guides/new-ticket-simplification/REQUIREMENTS_C2J_GIT_STATE_RESTORE_AFTER_MUTATING_EXTENSION.md`
- `guides/SUPERPOWERS_RECIPE_GAPS.md`
- `guides/SUPERPOWERS_RECIPE_VALIDATION_TEST_PLAN.md`

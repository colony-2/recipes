# Build does not capture structured rebase failures for conflict recovery

Date: 2026-11-01 UTC

Status: implemented; validation recorded in `recipe-tests/rebase-recovery-validation.md`

Owner: recipes

Purpose assessment: fits; catch predicates, recovery handoff, budgets, and review gates belong to this cell.

## Problem and evidence

Heavy and light development resolve upstream and call `rebase_candidate`, but
their `rebase` states have no conflict catch or recovery handoff. A conflict ends
the job without giving the implementation workflow structured evidence it can
use to repair the candidate.

In [job 3LTTo4JDx3ZNA1q5esqVeqCkLK2](https://jobs.colony2.com/c2/jobs/3LTTo4JDx3ZNA1q5esqVeqCkLK2),
chapter 37 failed rebasing new candidate `24900ea…` from `aa17c20…` onto
`924e012…`, conflicting in `web/app/src/components/ReviewDocuments.tsx`.
The job ended `failed_app`. Restarting at approval repeated implementation on
the retained old base and did not provide a conflict-aware repair path.

Current guidance explicitly says rebase conflicts propagate normally in
`guides/ops/OP_GIT_INTEGRATION.md`. This report requests a deliberate extension:
capture classified, safely restored conflicts and give them a bounded repair
path, while preserving failure for unhandled or unsuccessful recovery.

## Dependency and capture contract

Requires [c2j structured rebase failures](../thinpackrebase-op-spec.md), available
in c2j `e7e2184f843500db9d6fe3dd2b6149a25de26aba` (operation 1.1.0, payload 1).
Its fields are `failure.kind`, `failure.code`, `failure.node`, and
`failure.attrs.rebase`, containing a schema version, input hashes, conflict
paths, restoration status, and durable diagnostic references. These fields
are now native guarantees for `rebase` and `thinpackrebase`. The implementation
uses no message-parsing fallback.

The intended catch matches all of:

- `kind == task_error` and `code == REBASE_CONFLICT`;
- the expected `rebase_candidate` node, `op == rebase`, and intended origin path;
- supported structured payload version and required recovery evidence;
- confirmed `workspace_restored == true`;
- remaining durable conflict-repair allowance.

Guard optional fields before dereferencing them. A failure from
`resolve_upstream_head`, a different nested operation, or an unsupported schema
must retain its original propagation. Do not read `sequence.rebase_candidate.outputs`
as if the failed operation completed successfully.

## Required recipe behavior

1. Apply equivalent handling to `recipes/develop/develop.yaml` and
   `recipes/light/develop.yaml`. Capture the failure at the rebase state and
   explicitly pass it through `transition.failure` or a declared payload to the
   recovery state. Export evidence needed beyond that scope.
2. Preserve the request, accepted planning documents, implementation session,
   candidate snapshot, target hash, failure origin, and diagnostic artifact map.
   Bind diagnostics into the repair operation's inbox through normal artifact
   plumbing. Keep bulky diagnostic content out of transition values and prompts.
3. Use the existing implementation/repair workflow to reconcile the candidate
   with the supplied target using c2j's documented repair handoff. It must work
   after worker replacement. Do not assume an active conflicted index survived
   abort, or instruct an agent to run `git rebase --continue` on a clean restore.
4. Allow at most two automatic conflict-repair rounds for a build. Persist a
   separate `rebase_repairs` count in flow; increment only when entering repair.
   Preserve it through resume, revisions, light-to-heavy handoff, and merge
   chases. Existing merge-chase limits remain independently enforced.
5. After repair, resolve upstream again and perform native rebase. A changed
   target may produce another conflict and consume the remaining allowance.
   Recovery cannot jump directly to squash, merge, or successful completion.
6. Clear candidate-dependent verification and approval reuse after a conflict
   repair. Re-run independent assessment, verification, accounting, and required
   human approval for the repaired candidate before publication.
7. Unclassified errors, cancellation, timeout, missing evidence, unsuccessful
   cleanup, and exhausted allowances propagate as failures. If repair itself
   fails, retain both that error and the originating rebase evidence. Do not
   convert failure into a successful result saying recovery or publication failed.
8. Preserve failed origin and recovery in the story and final diagnostics. If
   recovery succeeds, report the conflict resolution and subsequent validation.
   Prevent enclosing retries or replacement jobs from silently resetting limits.

This adds a distinct rebase-conflict policy. It does not broaden the existing
`MERGE_UPSTREAM_ADVANCED` publication catch, classify authorization failures as
advancement, or change empty-workspace initial publication to use rebase.
Update guidance that currently says all rebase conflicts propagate, while
retaining propagation for conflicts outside this bounded policy.

## Acceptance statements and validation

| Importance | Level / dependencies | Files | Statement |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Git | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | A classified, safely restored conflict reaches repair with the original candidate, target, conflicting paths, and diagnostics. |
| Critical | Integration / c2j, Git | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | A repaired candidate passes fresh integration, verification, assessment, accounting, and required approval before publication. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | Unclassified errors, unsupported payloads, and failures from unrelated nodes propagate without entering conflict repair. |
| Critical | Integration / c2j | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | A third conflict propagates after two automatic repairs; resume and escalation never reset the allowance. |
| Critical | Integration / c2j, Git | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | Failed cleanup or failed repair never produces a successful build or publishes an unverified candidate. |
| High | Integration / c2j, Git, JobDB | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | A replacement worker can read conflict evidence and resume recovery without the failed worker's worktree. |
| High | Integration / c2j, Git | `recipe-tests/merge-chase.test.yaml` | Conflict repair preserves the existing merge-chase allowance and cannot reuse approval of the earlier candidate. |

Publish statements and evidence as c2 artifacts during implementation. Use
mocked structured failures for focused routing coverage and a real conflicting
Git history for the end-to-end native contract. Mock only agent decisions and
human input as necessary. Validate ordinary successful builds and negative
propagation cases alongside recovery, including restart during the repair path.

The [build workspace cleanup](BUG_REPORT_BUILD_EXPLICIT_WORKSPACE_PINNING.md)
and [c2j pinning correction](BUG_REPORT_C2J_PREMATURE_WORKSPACE_HASH_PINNING.md)
reduce stale-base exposure but do not eliminate concurrent rebase conflicts.

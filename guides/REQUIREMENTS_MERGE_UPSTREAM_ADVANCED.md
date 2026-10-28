# Requirements: Detect upstream advancement and bound merge chases

Status: c2j implemented the contract in its Git ops guide; the recipes now use
it for bounded recovery. npm release `0.0.107` predates that behavior. Use a
c2j build/release containing the implementation (present at revision
`db32d4246b20df452e283cf0de4657fb6462fb11`). The original gap below describes the
source inspected when these requirements were written.

## Outcome and ownership

When another job publishes while a build is being reviewed, the build should
rebase onto the new upstream tip, repeat verification, and try to merge again.
Repeat review only if the local candidate changes. Allow at most **three chases after the initial merge attempt**:
four merge attempts total when each failure is caused by upstream advancement.

c2j owns reliable classification and durable delivery of the merge failure.
This recipes cell owns the chase count, routing, verification, and approval
policy. This request fits the recipes cell with an external dependency on c2j.

## Current behavior and gap

Both `recipes/develop/develop.yaml` and `recipes/light/develop.yaml` rebase
before verification and final review. Their final `merge` state runs `squash`
then `merge`. A merge failure currently propagates without recovery.

Source inspected: c2j commit
`392509ed7dd33db631420549c66af373c4d0d06e`.

- `pkg/git/squashrebasemerge/merge_ancestry.go` checks ancestry before publication
  and returns `common.NotFastForwardError` on divergence.
- `pkg/git/common/errors.go` carries the branch, candidate hash, and upstream
  hash in that Go error. Divergence alone does not establish that upstream
  advanced normally from the candidate's prepared base.
- `pkg/git/squashrebasemerge/separate.go` uses a non-forced push. A race after
  the ancestry check returns a generic wrapped Git error, unless reconciliation
  proves the candidate was already published.
- `pkg/worker/compiler/failure.go` reads recipe-facing codes from structured
  application errors. There is no mapping here from `NotFastForwardError` to a
  dedicated code that recipes can match consistently across both paths.

Matching text such as `rejected` or `not a fast-forward` is insufficient:
authentication, branch protection, transport errors, and history rewrites must
not enter the chase loop. Recipe-side Git checks also duplicate the op's
publication and race-handling responsibilities.

## Required merge failure contract

Keep the existing successful `merged_hash` and `target_branch` outputs and the
default behavior of failing when publication cannot complete. Use existing
recipe `catch`; no soft-result mode or additional error-capture op is needed.

Expose the following stable failure when the candidate needs a new rebase
because upstream advanced normally:

```yaml
failure:
  kind: task_error
  code: MERGE_UPSTREAM_ADVANCED
  message: "Target branch advanced beyond the prepared base; rebase and review again."
  node:
    id: merge_reviewed_candidate
    op: merge
    # Preserve the actual originating node path and type as usual.
  attrs:
    candidate_hash: <full candidate commit hash>
    prepared_base_hash: <full base hash used to prepare this candidate>
    upstream_hash: <full observed upstream commit hash>
    target_branch: refs/heads/main
    phase: preflight # or push
```

The code is the routing API; message wording is diagnostic. Required attributes
must survive task persistence, enclosing nodes, job stories, and resume. The
failure must remain attributable to the original merge op.

Use the managed workspace's execution base as the prepared base. If standalone
merge calls lack that context, provide an optional `prepared_base_hash` input
or document another explicit source. Without a trustworthy base, do not claim
normal advancement. Recipe callers with managed workspaces should not need to
repeat Git inspection in shell commands.

### Classification rules

1. Preserve existing already-published reconciliation first. If upstream equals
   or contains the saved candidate, report success, including after a lost push
   response. Do not consume a chase.
2. If upstream is an ancestor of the candidate, allow ordinary fast-forward
   publication.
3. Emit `MERGE_UPSTREAM_ADVANCED` only when the prepared base is an ancestor of
   both candidate and upstream, upstream differs from that base, and neither
   candidate nor upstream contains the other. Fetch sufficient history to prove
   these facts; incomplete history is not proof of advancement.
4. Cover both advancement visible during preflight and advancement racing the
   push. Use structured Git push rejection information and a fresh ancestry
   check for a non-fast-forward/ref-update race. A generic rejection or a
   transport failure followed by observation of a new tip is not sufficient to
   attribute that rejection to advancement.
5. Authentication, authorization, branch protection, hooks, invalid refs,
   dirty worktrees, transport failures, timeouts, cancellations, and failures
   to fetch or establish ancestry retain their actual failure classification.
6. Upstream history rewritten away from the prepared base is not eligible.
   Initial publication colliding with an existing unrelated branch is not
   eligible. Neither case should receive the new code.

A classified failure must leave the candidate, workspace base, and snapshots
available for a subsequent native `rebase`. It must not force-push, silently
rebase, or mark the candidate as published. Retrying the identical candidate is
not the recovery mechanism: deliver the failure to `catch` before scheduling
any recipe retry, using the existing catch ordering.

## Recipe policy

Apply the same policy to heavy and light development:

- Carry a durable `merge_chases` counter in workflow `flow`, initially zero.
  Increment only when a classified failed merge routes to rebase. Initial
  preparation, ordinary implementation revisions, and replay do not increment it.
- Keep the counter across verification failures, implementation fixes, review
  revisions, and any light-to-heavy handoff. Do not reset it on each merge entry.
- Catch only `MERGE_UPSTREAM_ADVANCED` originating from the final merge op.
  Squash and unrelated merge failures continue to propagate.
- When the count is below three, preserve the development session, documents,
  and dependency state, increment the count, and route to the existing `rebase`
  state. Resolve the current upstream tip again; the failure's observed hash
  may already be stale.
- Compare the rebased local changes against the approved changes, including
  paths, before/after blob IDs, and file modes. Unrelated upstream files and
  commit IDs do not change this comparison. Always repeat verification.
- If local changes are identical, reuse the existing final approval and commit
  message; skip repeated assessment, accounting, synopsis, and human review.
  If no local changes remain, complete after verification without another
  review or merge. This exception applies only to an already approved chase.
- If local changes differ, repeat the existing downstream review gates. Heavy
  builds repeat independent assessment, file accounting, and human acceptance;
  light builds regenerate the synopsis and request human acceptance.
- Missing optional checks remain explicitly skipped. Failing checks send the
  candidate back to implementation and invalidate the approval-reuse shortcut.
  Subsequent implementation changes and initial no-change outcomes still need
  their normal reviews.
- After three chases, a fourth stale merge failure propagates unchanged from
  the merge op. No fifth attempt, replacement command failure, or endless loop.
  Preserve enough workflow state and story information to see all three chases.
- A rebase conflict follows existing failure behavior; this policy does not
  introduce an automatic conflict-resolution agent.

Illustrative catch on the enclosing `merge` state (production recipes also mark
the chase for candidate comparison and clear the previous verification state):

```yaml
catch:
  - id: chase_advanced_upstream
    when: >-
      failure.kind == 'task_error' &&
      failure.code == 'MERGE_UPSTREAM_ADVANCED' &&
      failure.node.op == 'merge' &&
      failure.node.id == 'merge_reviewed_candidate' &&
      transition.payload.flow.?merge_chases.orValue(0) < 3
    to: rebase
    payload:
      flow: >-
        ${{ jq([transition.payload.flow, {
          'merge_chases': int(transition.payload.flow.?merge_chases.orValue(0)) + 1
        }], 'add') }}
```

There is deliberately no fallback catch. Exhaustion and other failures retain
their original diagnostics. The recipe changes must also preserve the counter
at handoff and regenerate final evidence as described above.

## Acceptance tests

Each statement below is at most 30 words. Filenames identify implementation or
recipe targets; the c2j owner may choose the corresponding test filenames.

| Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- |
| Critical | Integration / Git | Upstream advancement before publication exposes the stable code and exact candidate, base, branch, and upstream hashes. | c2j: `pkg/git/squashrebasemerge/merge_ancestry.go`, `separate.go` |
| Critical | Integration / Git | Advancement between ancestry inspection and push yields the same classified failure without publishing or modifying the candidate. | c2j: `pkg/git/squashrebasemerge/separate.go` |
| Critical | Integration / Git | An already-published candidate succeeds after a lost response, even when upstream contains additional commits. | c2j: `pkg/git/squashrebasemerge/separate.go` |
| Critical | Integration / Git | Permission, protection, hook, transport, and timeout failures never produce the upstream-advanced code, including when the branch concurrently moves. | c2j: `pkg/git/squashrebasemerge/separate.go` |
| Critical | Integration / Git | Rewritten history, initial-publication collisions, and unprovable ancestry do not trigger ordinary advancement recovery. | c2j: `pkg/git/squashrebasemerge/merge_ancestry.go`, `separate.go` |
| Critical | Integration / durable runtime | Structured merge failures preserve code, attributes, and originating node through nested recipes and resume; existing catch can route them. | c2j: `pkg/worker/compiler/failure.go` |
| Critical | Integration / Git, native recipe runner, mocked agents | A stale merge rebases onto concurrent changes and repeats verification; unchanged local changes reuse approval, while changed local changes require fresh approval. | `recipe-tests/merge-chase.test.yaml` |
| Critical | Integration / native recipe runner, mocked agents | Three stale attempts can recover; a fourth stale failure propagates from merge without another rebase or a replacement failure task. | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` |
| Critical | Integration / durable runtime, mocked agents | Resume, implementation revisions, and light-to-heavy handoff preserve the chase budget without double-counting completed catch routes. | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` |
| Critical | Integration / native recipe runner, mocked agents | Verification failure after a chase blocks publication until corrected; implementation repairs require renewed review. | `recipe-tests/merge-chase.test.yaml` |
| Critical | Integration / native recipe runner, mocked agents | An empty local diff after an approved chase completes after verification without another review or merge. | `recipe-tests/merge-chase.test.yaml` |
| High | Integration / native recipe runner, mocked agents | Unrelated merge errors and squash failures preserve their original diagnostics and never consume a chase. | `recipe-tests/build-merge.test.yaml`, `recipe-tests/build-light.test.yaml` |

Use real Git repositories and native merge/rebase ops for the advancement and
push-race cases. Mocking a future error code tests recipe routing only; it does
not establish that a released c2j produces the required contract.

## Delivery

1. Implemented in c2j source: code, classification, persistence, and Git ops guide.
2. Release dependency: identify the first published c2j version providing this
   contract; `0.0.107` does not provide it.
3. Implemented in both recipes: the three-chase loop, preserved handoff budget,
   and native Git regression cases in `recipe-tests/merge-chase.test.yaml`.

Older c2j versions continue to propagate unclassified merge errors. There is no
text-matching compatibility fallback. CI's latest-release installation needs a
release containing this contract to pass the native advancement tests.

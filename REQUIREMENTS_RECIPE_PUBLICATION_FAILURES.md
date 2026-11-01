# Requirements: Recover only classified upstream advancement

Status: proposed recipe correction; requirements only.

## Intended policy and current deviation

The existing [upstream advancement requirements](REQUIREMENTS_MERGE_UPSTREAM_ADVANCED.md)
specify that heavy/light development catches only `MERGE_UPSTREAM_ADVANCED`
from the final merge operation. Squash failures and unrelated merge failures
propagate. The current [Git operations guide](GUIDE-Git-Ops.md#when-merge-fails-because-upstream-advanced)
documents the implemented structured classification contract for the separate
`merge` operation.

The recorded recipe for job `TExEUTN3c5GbGIpKrwicPeukpYM` does something broader:
at recipes commit `5274e14e7d82ea777cebadcbf009a435268eb545`, both the new-cell
`publish_new_cell` state and root-catalog `publish_cell_catalog` state catch all
failures from `squashrebasemerge` and continue with `outputs.error`.

The observed new-cell push failed with HTTP 403 and `no discoverable writable
refs`. The job nevertheless returned successfully with
`disposition: publication_failed`, `created_cells: []`, and `merged: false`.
Its history records no classified upstream advancement. This is an initial
publication from an empty workspace, not evidence of a stale prepared base.

These observations establish behavior of the recorded revision, not the latest
recipes branch. Implementation must audit the current recipes checkout too.

## Required publication policy

1. Audit publication catches in create, root-catalog registration, heavy/light
   development, and shared publication helpers. Remove catch-all handling that
   converts an unsuccessful publication into normal recipe completion.
2. Recovery is eligible only for a structured failure matching all of:
   - `failure.kind == 'task_error'`;
   - `failure.code == 'MERGE_UPSTREAM_ADVANCED'`;
   - the intended publication node's `failure.node.op == 'merge'` and exact ID;
   - remaining durable recovery budget.
3. Other failures must propagate with their original kind, code, origin,
   diagnostics, and artifacts. Do not replace them with a generic failure command
   or turn them into successful `publication_failed`/`registration_failed` output.
   A parent recipe must not silently undo this policy by swallowing the failure.
4. Do not identify advancement by message text, HTTP status, branch rejection
   wording, generic non-fast-forward errors, or a recipe-side Git probe. Trust
   the native operation's structured, ancestry-verified classification.
5. The classification describes repository state. A permission, hook, or
   transport error can coincide with proven advancement and still carry the
   code. Preserve the original push diagnostics; without that classification,
   such failures must propagate and must not consume a chase.
6. Cancellation, timeout, failed ancestry probes, unknown prepared bases,
   rewritten history, and initial-publication collisions must not be treated
   as ordinary upstream advancement. Squash/rebase failures do not qualify.
7. Already-published reconciliation remains success when the native operation
   proves the target contains the candidate. It consumes no recovery budget.

This policy concerns Git publication errors. It does not prohibit intentional
catches for unrelated recipe contracts or normal outcomes such as a user
declining approval. Audit those independently rather than removing all catches.

## Operation choice and recovery

Implementation note: the failure-propagation correction retains the initial
composite operation to preserve configured Git identity until the
[native squash committer defect](guides/BUG_REPORT_C2J_INITIAL_SQUASH_COMMITTER.md)
is corrected. Its errors now propagate; no initial-publication recovery is
enabled. The separate initial-operation migration below remains a follow-up.

- Do not assume the combined `squashrebasemerge` operation emits
  `MERGE_UPSTREAM_ADVANCED`; that guarantee belongs to separate `merge`.
- Where advancement recovery is needed, use separate preparation/publication
  operations and match the failure from the intended `merge` node. Preserve
  verification and approval gates between preparing and publishing a candidate.
- New-cell publication from `workspace.initial: empty` uses `squash` followed
  by `merge`, without `rebase`, as documented in the Git guide. Authentication
  failures and collisions must fail that publication. Do not invent a base or
  route initial publication into an established-branch rebase loop.
- For existing-branch recovery, resolve the current upstream again, rebase,
  and repeat required verification. Approval reuse is allowed when the reviewed
  local changes and hook identities are unchanged, following the existing
  heavy/light policy. Changed local candidates require fresh approval. Never
  force-push.
- Preserve the existing heavy/light budget: at most three advancement chases
  after the initial attempt. Increment only when routing a classified failure
  into recovery; persist the count through resume, revisions, and handoff.
- Any new existing-branch recovery path, including catalog publication, must
  define equivalent verification/approval gates and a durable bound before
  enabling a catch. Until then, let its merge failures propagate.
- Exhaustion propagates the original merge failure. Enclosing retries, whole-job
  retries, or child-job replacement must not reset or bypass the recovery bound.

## Outcomes, evidence, and ownership

An unrecovered publication error must result in a failed job. Successful recipe
execution must not be used to report that a required publication failed.
Retain partial-publication evidence and diagnostic artifacts on failure; avoid
implying that a repository already published earlier in a batch was rolled back.
Do not register a cell whose publication failed. If catalog publication fails
after cell publication, fail the job while preserving the already-created cell
identities for inspection and safe recovery.

The recipes repository owns catch predicates, control flow, budgets, and gates.
c2j owns native merge classification and preservation of structured failures.
JobDB records the resulting success/failure. Cortex must present that outcome;
it must not reinterpret arbitrary recipe output strings to repair recipe policy.
The separate [caught-failure story requirements](REQUIREMENTS_STORY_CAUGHT_FAILURE.md)
explain legitimately handled failures without changing job outcomes.

Do not retroactively change historical outcomes: the example job really did
return successfully under its recorded recipe. Apply corrected policy to runs
using the corrected recipes and document the required c2j contract/version.

## Acceptance criteria

Use native recipe execution with real Git repositories and durable JobDB
history; mock agents/review input where appropriate. A mocked error code alone
is sufficient for routing unit tests, not for the end-to-end classification test.

| Scenario | Required result |
| --- | --- |
| New-cell initial push rejected with 403, without advancement code | Job fails with original error; no catalog registration; diagnostic artifacts survive. |
| Catalog publication rejected after cells were published | Job fails; published-cell evidence remains available; no false completion result. |
| Squash failure, rebase conflict, ordinary merge failure | Original failure propagates; no advancement recovery or budget consumption. |
| Proven advancement in preflight or racing a push | Only the intended merge catch routes to rebase; repeat verification and obtain fresh approval when the reviewed changes or hook identities differ. |
| Classified advancement with coincident push error | Bounded recovery preserves original push diagnostics. |
| Unknown base, failed probe, rewritten history, or unrelated initial branch | Failure propagates without advancement recovery. |
| Target already contains candidate after lost push response | Native reconciliation succeeds; no unnecessary chase. |
| Three chases followed by a fourth stale merge | Fourth failure propagates; no fifth attempt or replacement failure task. |
| Resume, revisions, handoff, enclosing retry | Recovery count persists and cannot be bypassed or double-counted. |
| Parent waits for failed publication child | Required child failure is surfaced, not silently converted into parent success. |
| Story inspection of a successful advancement catch | Catching node is caught_failure once supported; failed origin and recovery remain visible. |

Include a regression matching the reported create recipe's failed initial push.
It must fail against the old catch-all recipe and pass after failure propagation
is corrected. Keep ordinary successful creation and publication coverage.

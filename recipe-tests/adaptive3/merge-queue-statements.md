# Adaptive3 merge queue test statements

These expectations are defined before implementation. None is a passing test result. Existing adaptive3 statements remain in force. Each numbered expectation is at most 30 words; annotations identify files, priority, level and dependencies.

Production filenames below are relative to `recipes/adaptive3/`, except `./adaptive3.yaml` at repository root. Each section names its planned suite under `recipe-tests/adaptive3/`; that suite applies to every row in the section. Proposed filenames do not imply delivered code.

Use a compatible c2j runtime and disposable repositories with real Git bundles and artifact storage. Nix is required for packaged agent ops, and uv with a compatible interpreter is required for the queue's Python op. Script agent decisions only. Integration cases run native workspaces, children, waits, the packaged Python op and merges. A negative case must reach its intended failure with unrelated prerequisites satisfied and have a passing control.

## Build defaults

Suite: `recipe-tests/adaptive3/default-build.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-69 | A build that omits the queue setting verifies and merges through the queue and publishes its confirmed commit. | `./build.yaml`, `./adaptive3.yaml`, `merge-queue-submit.yaml` | Critical | Integration / grouped c2j, Git, uv |
| MQ-70 | A build with `merge_queue: false` merges directly without submitting to the queue. | `./build.yaml`, `./adaptive3.yaml`, `integration.yaml` | High | Integration / c2j, Git |

## Python op boundary

Run the unit tests with `python3 -B -m unittest discover -s recipe-tests -p test_merge_queue.py`. The native replay, caller and selection suites also execute the extension.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-65 | Native queue tasks exchange structured results and bundle artifacts through the packaged Python op. | `recipes/merge-queue/op.yaml`, `merge-queue-replay.yaml`, `merge-queue-install.yaml` | Critical | Integration / c2j, uv, Git |
| MQ-66 | Missing, duplicate, stale or mismatched check results cannot establish passing subset evidence. | `recipes/merge-queue/policy.py`, `merge-queue-select.yaml` | Critical | Unit / Python |
| MQ-67 | Subset planning prioritizes older compatible work within its probe budget and surfaces exhaustion as an operational failure. | `recipes/merge-queue/policy.py` | High | Unit / Python |
| MQ-68 | A caller accepts only its own uniquely identified result in a complete receipt for the expected branch. | `recipes/merge-queue/policy.py`, `merge-queue-submit.yaml` | Critical | Unit and integration / Python, c2j |

## Candidate preparation

Suite: `recipe-tests/adaptive3/merge-queue-caller.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-01 | Implementation starts with retained work refreshed against the latest published branch. | `execute.yaml`, `integration.yaml` | Critical | Integration / c2j, Git |
| MQ-02 | Preparation-hook edits are included in the refreshed single-commit candidate before verification. | `execute.yaml`, `validate.yaml` | Critical | Integration / c2j, writing hook |
| MQ-03 | Each verified candidate carries one durable random KSUID change ID without losing its approved commit message. | `integration.yaml` | Critical | Integration / c2j, Git |
| MQ-04 | Refresh conflicts and failed verification return diagnostics to repair without queue admission. | `execute.yaml`, `validate.yaml` | Critical | Integration / c2j, conflict and verifier fixtures |
| MQ-05 | Post-verification writes invalidate checks; changed approved content requires renewed outcome review before admission. | `validate.yaml`, `cycle.yaml` | Critical | Integration / c2j, scripted review |
| MQ-06 | Unchanged rebased changes retain approval only after renewed verification, including binary contents and file modes. | `tools.yaml`, `cycle.yaml` | Critical | Integration / c2j, Git |
| MQ-07 | A queued pack, base and source HEAD describe the same prepared candidate. | `integration.yaml` | Critical | Integration / c2j, real artifact storage |
| MQ-08 | Accepted no-change work completes without queue admission or an empty source contribution. | `execute.yaml`, `cycle.yaml` | High | Integration / c2j, no-change fixture |

## Admission and retry age

Suite: `recipe-tests/adaptive3/merge-queue-admission.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-09 | Canonical branch aliases share one cell queue; different cells, branches and tenants remain separate. | `integration.yaml`, `merge-batch.yaml` | Critical | Integration / grouped c2j, tenant fixtures |
| MQ-10 | Every caller supplies limit 50; overflow enters a successor that waits for its predecessor. | `integration.yaml` | Critical | Integration / grouped c2j, serial generations |
| MQ-11 | The first worker chapter seals contributions; a crash before that write preserves appendable admission. | `merge-batch.yaml` | High | Integration / grouped c2j, restart fixture |
| MQ-12 | Matching policies permit admission; incompatible protocol, target or verification policies receive validation rejection without changing the creator’s checks. | `integration.yaml`, `merge-batch.yaml` | Critical | Integration / grouped c2j, mixed-policy fixtures |
| MQ-13 | Unavailable grouping fails visibly without falling back to caller direct merge. | `integration.yaml` | Critical | Integration / c2j, unsupported-feature fixture |
| MQ-14 | Lost responses, restarts and successor admission retain the original ID, timestamp and exact batch handle. | `integration.yaml`, `lifecycle.yaml` | Critical | Integration / grouped c2j, durable recovery |
| MQ-15 | Repair after definitive rejection changes the content ID while preserving the requested change’s first submission time. | `execute.yaml`, `lifecycle.yaml` | Critical | Integration / c2j, scripted repair |
| MQ-16 | Missing original timestamps require recovery; malformed or contradictory timestamps cannot authorize success. | `integration.yaml`, `merge-batch.yaml` | Critical | Integration / c2j, invalid contributions |

For MQ-12, use the ordinary-input policy and each append’s explicit copy. Include a matching control with reordered object keys; creator `require_verification: false` followed by append `true`; creator `true` followed by append `false`; changed settings or directory; and missing, malformed or unsupported policy. For usable IDs, assert `fail-validation` plus a readable policy log, no replay/publication for that ID, unchanged creator policy and successful processing of an independent compatible contribution. Include an already-landed mismatching ID and contradictory duplicate policies so neither history nor deduplication bypasses comparison. Malformed authoritative ordinary policy must prevent a complete batch success.

## Contribution integrity and history

Suite: `recipe-tests/adaptive3/merge-queue-intake.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-17 | Receiver assembly starts from the pinned published tip, independent of the first caller’s unpublished workspace. | `merge-batch.yaml` | Critical | Integration / c2j, distinct snapshot fixtures |
| MQ-18 | Contributions with identical bundle filenames retain distinct readable bytes throughout replay. | `merge-batch.yaml` | Critical | Integration / c2j, real artifacts |
| MQ-19 | Equivalent duplicate contributions produce one outcome even when job IDs or artifact storage locations differ. | `merge-batch.yaml` | Critical | Integration / c2j, duplicate envelopes |
| MQ-20 | Contradictory content under one ID cannot succeed and retains a readable validation diagnostic. | `merge-batch.yaml` | Critical | Integration / c2j, conflicting duplicates |
| MQ-21 | Wrong repository, branch, source HEAD, parent base or ID trailer prevents contribution replay. | `merge-batch.yaml` | Critical | Integration / c2j, Python replay, malformed bundles |
| MQ-22 | Unreadable packs and missing prerequisite history remain operational failures rather than conflicts or candidate rejections. | `merge-batch.yaml` | Critical | Integration / c2j, Python replay, storage faults |
| MQ-23 | Already-landed IDs return their original reachable hashes without replay, including beyond the recent-history window. | `merge-batch.yaml` | Critical | Integration / c2j, deep Git history |
| MQ-24 | Conflicting retained source evidence or multiple upstream occurrences of one ID require reconciliation rather than arbitrary success. | `merge-batch.yaml` | Critical | Integration / c2j, history fixtures |

## Ordered application and conflict repair

Suite: `recipe-tests/adaptive3/merge-queue-replay.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-25 | Older initial submission times lead regardless of append arrival; equal times use deterministic change-ID order. | `merge-batch.yaml` | Critical | Integration / c2j, ordered Git fixtures |
| MQ-26 | A replay conflict leaves no residual edits and does not prevent clean neighboring contributions from proceeding. | `merge-batch.yaml` | Critical | Integration / c2j, Python replay, Git |
| MQ-27 | Nominal approved-intent conflict repairs retain identity, repair evidence and fresh verification before landing. | `merge-batch.yaml`, `merge-check.yaml` | Critical | Integration / c2j, scripted repair |
| MQ-28 | Uncertain or behavior-changing repairs return conflict rejection without publication or repeated automatic repair attempts. | `merge-batch.yaml` | Critical | Integration / c2j, scripted repair |
| MQ-29 | Older repairs are evaluated against older accepted work and reinserted before younger additions. | `merge-batch.yaml` | High | Integration / c2j, ordered repair fixtures |
| MQ-30 | Empty replay preserves the original change ID in a reachable commit with an individual success hash. | `merge-batch.yaml` | High | Integration / c2j, Python replay, Git |
| MQ-76 | If reconstructing the preceding changes produces a different commit, the batch stops before asking for a repair or publishing. | `merge-queue-repair.yaml` | Critical | Integration / c2j, Git, missing predecessor |

## Combined verification and subset selection

Suite: `recipe-tests/adaptive3/merge-queue-selection.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-71 | Consecutive conflicts see each earlier accepted repair and land in order with their original change IDs. | `merge-queue-resolve.yaml`, `merge-queue-repair.yaml` | Critical | Integration / c2j, Git, scripted repair |
| MQ-72 | A declined repair is attempted once, even when a younger repair succeeds and causes the batch to be rebuilt. | `merge-queue-resolve.yaml` | Critical | Integration / c2j, Git, scripted repair |
| MQ-73 | A later repair that touches an unauthorized path leaves earlier repairs publishable and returns a conflict diagnostic for the rejected change. | `merge-queue-resolve.yaml`, `merge-queue-repair.yaml` | High | Integration / c2j, Git, scripted repair |
| MQ-74 | After combined verification fails, subset checks and final verification retain a repair when its predecessors are unchanged. | `merge-queue-resolve.yaml`, `merge-queue-land.yaml`, `merge-queue-select.yaml` | Critical | Integration / c2j, Git, verification hook |
| MQ-75 | A subset that excludes a repair’s predecessor verifies and lands the original contribution on its new base. | `merge-queue-replay.yaml`, `merge-queue-land.yaml` | High | Integration / c2j, Git, verification hook |
| MQ-31 | A passing complete sequence lands all eligible contributions without subset-search publication. | `merge-batch.yaml`, `merge-check.yaml` | Critical | Integration / c2j, controlled verifier |
| MQ-32 | A failing sequence launches isolated parallel subset checks with no more than four concurrent probes. | `merge-batch.yaml` | High | Integration / c2j, parallel child fixtures |
| MQ-33 | Subset checks preserve the same published base and relative order while naming their exact persisted candidate HEADs. | `merge-check.yaml` | Critical | Integration / c2j, real snapshots |
| MQ-34 | Check-child writes cannot change the parent or another child’s candidate. | `merge-check.yaml` | Critical | Integration / c2j, independent workspaces |
| MQ-35 | Independently passing subsets with a failing union cannot land together without a passing combined check. | `merge-batch.yaml` | Critical | Integration / c2j, interacting verifier |
| MQ-36 | An older passing large contribution wins over more numerous incompatible younger contributions. | `merge-batch.yaml` | Critical | Integration / c2j, priority fixture |
| MQ-37 | Faster younger checks cannot evict verified older work or bypass unresolved older probes. | `merge-batch.yaml` | Critical | Integration / c2j, delayed child results |
| MQ-38 | A demonstrably failing older contribution permits compatible younger work to land with retained rejection evidence. | `merge-batch.yaml` | Critical | Integration / c2j, healthy baseline |
| MQ-39 | Compatible excluded contributions found during oldest-first add-back join the final verified set. | `merge-batch.yaml` | High | Integration / c2j, add-back fixture |
| MQ-40 | Discovered passing combinations containing older dependent work retain priority over younger alternatives. | `merge-batch.yaml` | High | Integration / c2j, non-monotonic verifier |
| MQ-41 | Search exhaustion preserves partial evidence without inventing rejection or claiming exact optimality for untested work. | `merge-batch.yaml` | Critical | Integration / c2j, incomplete-search fixture |
| MQ-42 | Restarted search retains original ages, protected passing work and deterministic ordering. | `merge-batch.yaml` | Critical | Integration / c2j, durable restart |
| MQ-43 | An older retry leads its next appendable batch without preempting sealed predecessors. | `merge-batch.yaml` | High | Integration / grouped c2j, serial generations |

## Verification policy and evidence

Suite: `recipe-tests/adaptive3/merge-queue-check.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-44 | The saved authoritative policy requires passing hooks when verification is required and rejects failed or skipped checks. | `merge-check.yaml`, `hooks.yaml` | Critical | Integration / c2j, explicit policy and hook fixtures |
| MQ-45 | Optional verification skips remain visible and retain the existing cell policy. | `merge-check.yaml`, `hooks.yaml` | High | Integration / c2j, optional hook |
| MQ-46 | Broken baselines, unavailable credentials and infrastructure failures cannot become candidate validation rejections. | `merge-batch.yaml`, `merge-check.yaml` | Critical | Integration / c2j, operational faults |
| MQ-47 | Changed base, HEAD, ordered content or verification configuration prevents reuse of prior passing evidence. | `merge-batch.yaml` | Critical | Integration / c2j, candidate variants |
| MQ-48 | Check roots invoke authorized cell hooks without target-write grants; caller-bound grants cannot authorize a combined commit. | `merge-check.yaml`, `hooks.yaml` | Critical | Integration / c2j, permission fixtures |
| MQ-49 | Candidate hook changes are verified against their exact candidate; unavailable selector sources fail visibly. | `merge-check.yaml` | High | Integration / c2j, hook and selector fixtures |
| MQ-50 | Final merge uses the exact verified sequence with no intervening squash, rebase or unverified write. | `merge-batch.yaml` | Critical | Integration / c2j, Git |

For MQ-44, observe baseline, subset and final child inputs and results: all must retain the authoritative requirement flag, directory and settings. For MQ-45, use matching explicit optional policies as the skip control. For MQ-47, vary policy settings, directory and requirement separately and assert that prior success is not reused; a returned check policy differing from the authoritative object cannot authorize merge.

## Merge races and per-change results

Suite: `recipe-tests/adaptive3/merge-queue-results.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-51 | Upstream advancement rebuilds and reverifies remaining work without force push; exhausted chases retain recovery evidence. | `merge-batch.yaml` | Critical | Integration / c2j, advancing remote |
| MQ-52 | A lost push response recovers saved mappings and landed hashes without duplicate commits. | `merge-batch.yaml` | Critical | Integration / c2j, push-response fault |
| MQ-53 | Partial landing preserves confirmed outcomes and reverifies remaining work rather than certifying the old whole sequence. | `merge-batch.yaml` | Critical | Integration / c2j, partial-history fixture |
| MQ-54 | Complete results contain exactly one outcome for every unique requested ID, including duplicates and already-landed contributions. | `merge-batch.yaml`, `integration.yaml` | Critical | Integration / c2j, mixed batch |
| MQ-55 | Each success identifies its own reachable target commit and matching change-ID trailer. | `merge-batch.yaml`, `integration.yaml` | Critical | Integration / c2j, real Git remote |
| MQ-56 | Validation rejections retain readable original failure-log references after the batch completes. | `merge-batch.yaml` | Critical | Integration / c2j, artifact materialization |
| MQ-57 | Batch success, foreign IDs, missing entries, duplicate entries, invalid hashes and unknown statuses cannot release publication. | `integration.yaml` | Critical | Integration / c2j, malformed receipts |
| MQ-58 | Mixed success, validation rejection and conflict rejection route each caller according to its own outcome. | `integration.yaml`, `lifecycle.yaml` | Critical | Integration / grouped c2j, three callers |

## Publication and cancellation

Suite: `recipe-tests/adaptive3/merge-queue-recovery.test.yaml`.

| ID | Expectation | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| MQ-59 | Publication reads the caller’s landed commit and receives that hash even when source HEAD and batch tip differ. | `execute.yaml`, `hooks.yaml` | Critical | Integration / c2j, publication hook |
| MQ-60 | Failed publication resumes from the confirmed receipt without queue resubmission or another merge. | `execute.yaml`, `lifecycle.yaml` | Critical | Integration / c2j, failing publish hook |
| MQ-61 | Rejected callers receive original diagnostics, reprepare changed work and satisfy verification and approval before resubmission. | `execute.yaml`, `cycle.yaml` | Critical | Integration / c2j, scripted repair and review |
| MQ-62 | Cancelling one caller neither cancels the shared batch nor withdraws its accepted contribution. | `integration.yaml` | Critical | Integration / grouped c2j, cancellation fixture |
| MQ-63 | Failed or cancelled batches reconcile known outcomes and branch history before replacement admission. | `integration.yaml`, `lifecycle.yaml` | Critical | Integration / c2j, durable recovery |
| MQ-64 | Malformed input without a usable ID produces protocol failure while preserving known outcomes for recovery. | `merge-batch.yaml` | Critical | Integration / c2j, mixed malformed intake |

## Running and interpreting acceptance

Implement these cases in the named native suites, then run `c2j test validate --directory recipe-tests/adaptive3` and the focused new suites with `c2j test run --file <suite>`. Retain existing `integration.test.yaml`, `publication-ref.test.yaml`, `renewal.test.yaml`, `resume.test.yaml` and `cancellation.test.yaml` coverage, adapting only their integration path assumptions. Run shared `recipe-tests/adaptive/parent-recovery.test.yaml` and `required-jobs.test.yaml` when changing child orchestration, plus the repository timeout-policy check when executable recipes change.

Finish with a real grouped receiving flow on the selected supported local backend: multiple appends, a serial successor, actual bundles, interrupted/restarted waiting, a passing item beside validation/conflict rejections, and publication observing its own hash. Do not mock those boundaries. Record runtime identity, native reports and selected failure evidence. A selected acceptance check that cannot run is incomplete or failed, never a feature pass. No production deployment, additional backend repair or all-backend certification is part of this validation.

Scripted repair choices verify routing and rollback, not Codex confidence or semantic equivalence. Exact optimum, global oldest-first scheduling and starvation freedom across sealed generations are not asserted. If exact optimization is selected, add acceptance for discovering feasible older-dependent combinations before claiming that stronger guarantee.

The replay helper runs through the Recipes-owned Python extension op. The
statements describe acceptance requirements for the queue.

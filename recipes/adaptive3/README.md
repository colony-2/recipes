# Adaptive3

The delegate chooses one operation at a time and receives its result. One author plans, another implements, and an independent reviewer checks the work. The delegate can answer an explanation, send a repair to its author, gather preferences or take verified work through integration. [Operations and handoffs](../../guides/adaptive3/DELEGATE_ORCHESTRATION.md)

Implementation writes the Git title and body from the finished change. The recipe
adds the originating job URL as the final `Job` trailer. Queued candidates also
carry a `Change-Id` immediately above it. The queue receives the complete commit.

Use root `build.yaml` for the default entrypoint, or `adaptive3.yaml` explicitly.
See the [rollout notes](../../guides/adaptive3/ROLLOUT.md) for the public contract.

```sh
# Run the local adaptive3 source against the current cell.
c2j submit --recipe-file ./adaptive3.yaml --inputs-file request.yaml --run --embed
```

Example `request.yaml`:

```yaml
title: Keep unsent drafts after closing the tab
prompt: Preserve a draft until it is sent or explicitly discarded.
target_directory: .
require_verification: true
```

Optional inputs are `documents` (selected artifact references), `resume_from`
(a previous job to inspect) and `max_iterations` (the exchange limit and basis for the job dispatch budget). A new job starts fresh sessions.

## Reading a job

Start with the delegate’s last message and the receipt for any decision it references. The job story records what it chose, the assignment it sent and what came back. The planning 1P, Design and Tests are available as source material. A review of a specific document includes the selected text. An ordinary question is self-contained. [Job inspection](../../guides/JOB_INSPECTION_PLAYBOOK.md)

A job requested through negotiation receives the reason, the parent request and the exchange. The requester can consult, open negotiation for a needed change and ask the receiving cell to deliver the agreed work. [Consultation and cell responsibilities](../../guides/adaptive3/PRINCIPLES.md#consultation-negotiation-and-delivery)

## Dependency publication

When a change depends on another cell, the delegate can arrange the handoff. It asks the requester only about a decision or access grant the team needs from them.

Consumer-initiated work: B is updating its feature and discovers it needs an API
change in A. B can keep its work, ask A to implement and publish that change, wait,
then update its dependency and finish locally. B is the workflow parent of A’s
delivery job, but B depends on A’s API. B needs no additional coordinator or local
implementation job for this reason alone.

Provider-initiated adoption: A needs B to adopt A’s new API as part of A’s request. A
can submit a distinct same-cell implementation assignment directly through review
and publication, then
request B’s delivery against the published API. That implementation job handles the
prerequisite; A retains the adoption request. If a new data format is involved,
publish and, where required, deploy compatible reader support before activating
new-format output. If the reader can implement from the agreed format contract
without new producer code, A can keep preparation local, request reader delivery,
and resume activation when that support is available. API discussion and isolated
candidate checks can happen earlier.

If adoption can happen after A’s original request finishes, A can publish normally
and arrange later adoption instead. Saved commits, snapshots and recovered diffs
preserve work; they do not publish a dependency. Use the target cell’s configured
published ref and ordinary dependency route, including any release or deployment
the consumer needs. A new child does not clear or refresh its caller’s candidate.

Independent consultation delivery selects a fresh target workspace and submits its
symbolic published ref explicitly, avoiding the caller's candidate-hash default.
Advice starts from the selected target's native published default as well. With
no workspace ref override, c2j uses captured self/root ref settings and defaults
other targets to `main`; it does not discover an arbitrary target repository's
configuration. Ask the owner when its publication route is unknown. Consultation
and public build input schemas do not expose a ref override. Intentional candidate
validation continues to use explicit workspace submission.

## Merge queue

Adaptive3 builds use grouped integration by default. Set `merge_queue: false`
to merge directly. Grouped integration requires workers and a JobDB that support
grouped recipe submission. Publish `build.yaml`, `adaptive3.yaml`,
`merge-batch.yaml`, `merge-check.yaml`, their includes, and the
[queue extension](../merge-queue/op.yaml) together. The op
requires Git, uv, and Python 3.10 or newer on the worker. Its manifest declares
an isolated Python environment with an empty library set. Git-backed jobs
resolve the extension from the recipe's source revision.
[Extension Python environments](https://github.com/colony-2/c2j/blob/main/EXTENSION_OPS.md#python-libraries) ·
[Grouping contract](https://github.com/colony-2/c2j/blob/12cee9e70f04826adf073ba4b5e34deb388df691/GUIDE-Recipe-Grouping.md)

The caller refreshes retained work before implementation. After rebase and the
prepare hook, a candidate touching both publisher and product paths returns to
implementation for splitting, including in direct-merge mode. Eligible queued
changes are squashed into one commit with a durable KSUID Change-Id. The caller
verifies the candidate before entering the queue. Entry requires Outcome approval or
confirmed coverage under full Preparation acceptance. The
same change retains its initial submission time on retry. The queue groups by
cell and canonical branch ref, with up to 50 contributions per serial batch.
Each batch uses the creator's verification policy.

New batches have titles such as `Merge queue: recipes/refs/heads/main (2024-04-01 12:25:00 UTC)`.
The caller captures UTC submission time immediately before grouped submission;
this includes any later wait for a predecessor. Completed capture and submission
checkpoints survive same-job resumption. Joining callers keep the creator's
title; a successor uses its own creating submission's time, independently of
contribution age. Fixed-width, 24-hour timestamps sort chronologically within
one destination, subject to clock skew and ties within a second. Job IDs still
distinguish generations. Existing jobs keep their titles, and custom receivers
need no new inputs.

A change confined to `.c2/recipes/hooks/build/publish.yaml` or its sibling
`publish/` directory runs the same merge recipe inline with one contribution.
It can land ahead of queued product changes. If another change lands during
verification, the merge recipe replays and verifies against the updated branch.
Integration checks the reviewed diff again when choosing the merge path.
If its hook fails, Integration retains the confirmed merge, original hook inputs
and diagnostics in bound internal `merge_state`. Retry validates that state and
invokes only publication at the original commit, even after branch advancement or
disabling the queue. It does not submit, verify, squash or merge again. Repeated
failure remains stuck; completed or skipped publication is not invoked again.
Retain the original Integration state rather than resubmitting a landed change.

The Python op screens contributions, replays bundles in a disposable Git
checkout, plans subset probes, and produces per-change receipts. Replay retains
the original commit metadata and Change-Id. The receiver can try one narrow
conflict repair against the older accepted prefix. It verifies the complete
stack and, if needed, tests subsets in groups of up to four using isolated
check jobs. Selection prefers older verified work within the batch. Search
exhaustion returns an operational failure with evidence for recovery.

Queue submissions optionally carry `verification`: the originating `job_id`
and the saved verifier's `identity`, `result`, and `artifacts` (without its
`contribution`). The queue reuses this evidence only when an applied supplied
commit, its checked candidate, and the installed publication head are identical,
the clean workspace can fast-forward from the pinned target, and the original
base, directory, settings and verification requirement match. There is no
batch-size gate. Rebase, repair or reconstruction that changes the hash needs
fresh verification, even with the same tree. Missing, malformed, foreign or
contradictory evidence falls back to ordinary verification. Duplicate receipts
are checked against their own producers before deduplication.

Qualifying full, subset and final checks retain the original receipt and status,
identify the reused job and commit in the summary, and preserve log identities
under `verification/<producer>/`. An optional skip remains skipped. Older callers
without receipts still work. Custom hooks do not receive a separate queue-context
invocation on qualifying paths: the original candidate check is authoritative.
The general verifier's receipt cache and publication guards are unchanged.

The batch installs its checked commit sequence through the native merge operation,
then runs the publish hook once at the final assembled tip. The caller confirms
its individual receipt and the receiver-owned publication against target-branch
history, without invoking a hook. Recover failed publication in that receiver
at the same source. Candidate rejections return diagnostics to implementation.
The [merge queue test statements](../../recipe-tests/adaptive3/merge-queue-statements.md)
describe the existing acceptance checks; [exact-commit reuse expectations](../../recipe-tests/adaptive3/exact-commit-fast-forward-statements.md) cover verification reuse.

## Recovery and local hooks

A failure returns to the delegate with its diagnostic. It can repair, retry a specific operation, investigate a different approach or ask the requester. A cancelled job stops. A previously landed change carries its native receipt through publication recovery.

The delegate presents questions and decisions through the native review form. **Revise** carries a question, guidance, an annotated document or a requested change. **Review before Complete** requests a final decision. **Take to Completion** permits a covered result to land after verification. A planning interview sends actual choices back to the planner. [Decision and interview handoffs](../../guides/adaptive3/DELEGATE_ORCHESTRATION.md#when-a-person-is-needed)

Configure, before-design, prepare, verify and publish retain the existing
[build hook API](../../guides/BUILD_HOOKS_USER_GUIDE.md). Hook settings artifacts
stay at that boundary. Agent prompts do not receive `build-settings.json`.
Native workspace, permission and Git operations remain responsible for isolation
and publication. Integration keeps `merge_state` independently of agent feedback.
A completed native merge or the queue caller's confirmed landing establishes it
before the publication include runs. The receipt supplied to the hook is also the
final merge output. Returned hook failures and thrown resolution/collection errors
retain that record for the delegate and subsequent retries.
Retries reuse it while the target and accepted Outcome/patch remain unchanged.
New accepted work uses normal Integration; older evidence stays at its producer.

General `feedback.publication` never selects publication, including dependency,
null, malformed and copied receipts. An explicit cross-job Integration recovery
may propose that field as a producer lookup hint. `merge-receipt.yaml` checks the
exact successful native merge task, source cell/repository/branch and native human
acceptance. For full Preparation acceptance, it also checks the original coverage task
and the Preparation receipt recorded for that candidate. It binds the approved patch to the acceptance workspace, then checks
the full landed edit and reachability in a fresh fetch of the target branch. Batch
recovery can select an accepted contribution behind the native published tip with
its original Change-Id and complete patch equivalence. Unavailable or contradictory
evidence stops recovery before publication or a guessed second merge. No public
build input or agent trust flag can establish the internal record.

Queued publication belongs to the merge receiver at the final assembled tip;
callers consume the shared result and retain their individual merge hashes.
Resume the original receiver at its saved publication step. If c2j assigns the repair
a new job ID, supply it in `queue_recovery.repair_job`. The caller checks the retained
assembly, original merge, and its own contribution before consuming the result. [Receipt, recovery and drain-first upgrade details](../../guides/BUILD_HOOKS_USER_GUIDE.md#queue-receipt-and-upgrade)
cover the v2 paired caller/receiver contract. Product hooks still own branch
eligibility, durable release identity and ancestry-aware ordering.

Package requests contain a `reference`, an argument-array `check`, and a reason.
The package service validates a proposed configuration and retains its original baseline,
artifact identity and exact requests/checks in native outputs. After applicable approval,
a bounded operation compares and writes it in a separate validation job. Only the following
fresh task prepares and probes those additions. After child success, the same operation
compares the parent's current configuration again before adoption. Conflicts, substituted
proposals and extra packages fail without writing; an exact unchanged retry preserves bytes.
Older callers without the retained binding fail safely before writing.
For direct CLI submission and recovery of a retained approval against the actual
target baseline, see [Submit an approved package check](package-probe.md).

Private pnpm authorization includes direct, transitive and selected optional dependency
builds, mutable transitive resolutions and repeated preparation after failure, worker changes
or cache loss. Exact requested references and checks stay exact. Changed requests or scope
need applicable authority; questions never approve, and withdrawal, cancellation and newer
human scope take precedence. Completed durable operations remain completed. Legacy pnpm
reference/check policy matches alone use the existing package review; uv/Nix matching is
unchanged. Baseline recipe, repository, extension and early-hook dependencies derive authority
from their source and applicable standing cell policy, independently of personal job approval.
This guarantee covers service-managed staging/adoption; out-of-service edits remain outside it.

## Source map

- [Delegate](delegate.yaml) chooses the next action. [Dispatch](dispatch.yaml) runs it and stores its result.
- [Presentation](delegate-present.yaml) sends the selected message and records the submission. [Interview preparation](prepare-interview.yaml) supplies batch questions.
- [Validation](validate.yaml), [execution](execute.yaml), [consultation](consultation.yaml) and [package requests](packages.yaml) own their work.
- Direct callers of the reusable cycle and lifecycle recipes can use their own review and recovery flows.
- `agent.yaml` owns session start/resume and native Codex calls.
- `hooks.yaml`, `integration.yaml`, `specialists.yaml` call existing extension points.
- `prompts/` and `schemas.yaml` are empty includes; they create no worker tasks.
- `tools.yaml` embeds review-file and approved-edit validators plus bounded package comparison/writing.

See the [design](../../guides/adaptive3/DESIGN.md),
[implementation assessment](../../guides/adaptive3/IMPLEMENTATION.md), and
[tests](../../recipe-tests/adaptive3/README.md) before widening use.

For foreign includes and diagnostic jobs, see [the reuse guide](../../guides/adaptive3/REUSE.md).
The [supported-worker check](../../guides/adaptive3/VALIDATOR_WORKER_CHECK.md) covers the
validator dependency boundary separately from local routing tests.

The shared [review/v2 form contract](../../guides/REVIEW_V2.md) describes declarations,
source resolution, native responses and compatibility for custom includes.

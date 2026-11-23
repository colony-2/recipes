# Adaptive3

Adaptive3 uses two author sessions and one independent assessor for the standard
build. Direction and Preparation share a planning author. Implementation and
Outcome share a core implementer. Standard deliveries pause at Preparation with the one-pager, detailed design and
promised behaviors and suggested checks. “Show me the result” requests a final review.
“Finish if verified” permits completion or merge once independent assessment confirms the
verified candidate meets the promise and any explicitly required checks. An equivalent
check can replace an author’s example. A short local assignment goes
directly from Direction to Implementation and requires human Outcome acceptance.
Review questions resume the author in a read-only turn. Autonomous acceptance
uses the independent assessment result.

Check outputs before verification or assessment. Rebase and prepare the
candidate before managed verification. Send failed checks to the implementer
with original diagnostics. A merge retry after upstream advancement can reuse
human approval when the prepared change matches the approved patch and fresh
verification passes. Successful integration completes from merge and any
configured publication work.

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
(a previous job to inspect), and `max_iterations` (automatic passes before
Backstop; zero uses the finite default of four). Human discussion does not consume
these passes. A new job starts fresh agent sessions and uses inspection to
recover useful previous work.

## Reading a job

Start with the current stage's primary review document. Direction provides a
one-pager: problem, non-goals, approach, compatibility, and important questions
and answers. Outcome explains the change, other owners' work, tests, omissions,
public API changes and differences from the approved direction.

The producing agent owns its current review documents. The recipe also attaches the original negotiation reports and transcripts. Validation checks
those files; human input receives the same references. No recipe step builds a
second review packet or overlays older files. Documents worth retaining belong
in the agent's current work; other material remains accessible through native
job inspection. Diagnostics stay in files, with concise findings in responses.

For more detail, use the [job inspection playbook](../../guides/JOB_INSPECTION_PLAYBOOK.md).
Each cross-cell negotiation has a report with the parent objective, original request,
decision and linked transcript. A child receives the report with the agreed
assignment. Its Preparation review includes it immediately after the three planning
documents. Outcome and Backstop retain the same context. A direct assignment
identifies its parent and the initiating task. Owners can ask for evidence or
suggest an existing capability or a smaller enhancement. The requester confirms
changed terms before delivery. The receiver writes any delivery assignment. Consultation advice is
inline between different cells. Delivery uses a child adaptive3 job and a native
wait. A request addressed to the current cell returns to the existing worker.

## Dependency publication

For required manual publication, deployment or worker upgrades, use the standalone
[question recipe](../../guides/ASK_RECIPE.md). Submit it once, let Adaptive wait for
the child and inspect its complete reply before continuing the dependent check.

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

An ordinary caught failure reports `stuck` and enters Backstop in the same
job. Backstop first diagnoses the intended outcome, completed effects, remaining
work and failing boundaries, using retained results and earlier attempts. It
explains realistic options, owners, uncertainty and prerequisites. Authorized
read-only investigation needs no extra approval.

Backstop can return to Configure, Direction, Preparation, Implementation, Outcome or
Integration when the destination has its native entry prerequisites. An earlier
failure does not restrict the destination vocabulary. The accepted Preparation packet, or the current Direction on the short path,
establishes the basis for Implementation. A changed plan or candidate makes historical verification and acceptance ineligible.
Configure retains the intended destination. Prior-job restoration retains its
existing inspected approval/publication recovery contract.

Both recovery responses require nullable `action`, `stage`, `instruction`,
`destination` and `report` fields. A concrete available action and an eligible
stage gate automatic resume and Apply. A destination alone supplies no missing
plan, route, credentials or publication authority. Automatic correction defaults
to one extra pass; explicit integer allowances remain 1–20. Every phase visit starts with fresh counters. An explicit allowance can grant
a larger visit for the paused loop. Backstop spends one of two returns on dispatch.
Newly accepted phases and newly passing verification checks replenish those two
returns once per requirement per instruction. The progress step records the
evidence and resulting count. A fresh human instruction at any review resets
phase and merge retries and restores both returns before the next decision.

When help is needed, the primary report explains requester/rationale, completed
work and effects, the blocker and failed approaches, options with prerequisites,
a recommendation and useful research. Unknowns are explicit. A native report
remains readable after diagnosis or supporting-file validation failure; invalid
supporting files still disable Apply. `review/backstop-report.md` is reserved for
this report. Selected agent files remain supporting evidence.

**Give instructions** supplies native human authority for the precise request.
A clear instruction can also arrive through Ask a question; informational and
hypothetical questions remain discussion. Preserve original words, notes and
receipts. Requirement changes return to Direction and update the affected plan.
After validation confirms exactly that amendment, reuse its native receipt
and present the revised design and acceptance criteria at Preparation. Outcome and merge reviews
remain separate. Ambiguity, conflicting destinations or additional consequential
choices need clarification. Forward the original human receipt when a review hands an instruction to Backstop.
After answering a question, reassess the blocker under the existing authority.

Cancellation stays manual under the latest human scope. Prefer a return within
this job; an
exceptional explicit separate-job request can be routed to execution using the
existing create-job operation. Creating a job does not cancel this source.

Human checkpoints use Cortex `review/v2`. Ask a question keeps the original
documents and logical review identity, saves the exact contribution and native
receipt, appends the actual answer, and waits for another contribution. The
answering session receives the complete discussion and all retained files.
Approval requires exactly empty feedback and no new uploads.

Review doc comments appears when originals are attached. It sends the comments
through the documents' complete producer and validation cycle and requests fresh
approval. Request changes can select Auto or an applicable correction destination
under Review settings. The selection applies once; later reviews return to Auto.
Scope changes require Direction, and conflicting instructions stay in discussion.
Package-review destinations pass through the containing lifecycle.

Backstop no longer offers model/reasoning edits or settings reconsideration.
Existing launch inputs and worker defaults retain their current behavior.

Configure, before-design, prepare, verify and publish retain the existing
[build hook API](../../guides/BUILD_HOOKS_USER_GUIDE.md). Hook settings artifacts
stay at that boundary. Agent prompts do not receive `build-settings.json`.
Native workspace, permission and Git operations remain responsible for isolation
and publication. Integration keeps `merge_state` independently of agent feedback.
A completed native merge or the queue caller's confirmed landing establishes it
before the publication include runs. The receipt supplied to the hook is also the
final merge output. Returned hook failures and thrown resolution/collection errors
retain that record through Cycle, Lifecycle, Backstop and human discussion.
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

- `lifecycle.yaml` handles corrections, consultations and package interruptions.
- `cycle.yaml` defines a single Execute/Validate/Review pass, shared with consultation.
- `execute.yaml`, `validate.yaml`, `review.yaml` define those activities once.
- `discussion.yaml` retains human turns, actual answers, receipts and distinct uploads.
- `review-policy.yaml` declares correction destinations; [the shared builder](../review-v2.yaml)
  validates declarations and generates closed native schemas through its local source operation.
- `backstop.yaml`, `consultation.yaml`, `packages.yaml` provide their services.
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

# Adaptive3

Adaptive3 uses two author sessions and one independent assessor for the standard
build. Direction and Preparation share a planning author. Implementation and
Outcome share a core implementer. Direction and Outcome retain human approval.
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

The producing agent owns the current `review/` collection. Validation checks
those files; human input receives the same references. No recipe step builds a
second review packet or overlays older files. Documents worth retaining belong
in the agent's current work; other material remains accessible through native
job inspection. Diagnostics stay in files, with concise findings in responses.

For more detail, use the [job inspection playbook](../../guides/JOB_INSPECTION_PLAYBOOK.md).
Owner questions and replies appear as task responses in the receiving cell's
workspace. The receiver writes any delivery assignment. Consultation advice is
inline between different cells. Delivery uses a child adaptive3 job and a native
wait. A request addressed to the current cell returns to the existing worker.

## Dependency publication

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

The caller refreshes retained work before implementation. After preparation it
squashes changes into one commit with a durable KSUID Change-Id, verifies the
candidate, and waits for its outcome approval before entering the queue. The
same change retains its initial submission time on retry. The queue groups by
cell and canonical branch ref, with up to 50 contributions per serial batch.
Each batch uses the creator's verification policy.

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

The batch publishes only its verified commit sequence through the native merge
operation. The caller confirms its individual receipt against target-branch
history, then runs the publish hook at that commit. A failed publish retries at
the same commit. Candidate rejections return their diagnostics to implementation.
The [merge queue test statements](../../recipe-tests/adaptive3/merge-queue-statements.md)
describe the existing acceptance checks; [exact-commit reuse expectations](../../recipe-tests/adaptive3/exact-commit-fast-forward-statements.md) cover verification reuse.

## Recovery and local hooks

An ordinary caught failure reports `stuck` and enters Backstop in the same
job. Backstop first diagnoses the intended outcome, completed effects, remaining
work and failing boundaries, using retained results and earlier attempts. It
explains realistic options, owners, uncertainty and prerequisites. Authorized
read-only investigation needs no extra approval.

Both recovery responses require nullable `action` and `stage` fields. A nonblank
available action and an allowed destination gate automatic resume and Apply;
a destination alone grants no work. Apply also requires readable presentation.
Automatic corrections retain existing authority and finite limits. Diagnosis or
externally blocked repairs stay open for discussion without Apply or extra
attempts. Human approval cannot supply missing routes, credentials or deployment.
Questions and correction-destination edits grant no stage work or attempts.
Apply accepts the displayed correction with no new feedback or uploads. Request
changes reopens the diagnosis; a replaced action needs a fresh decision. Human
cancellation remains terminal.

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
acceptance. It binds the approved patch to the acceptance workspace, then checks
the full landed edit and reachability in a fresh fetch of the target branch. Batch
recovery can select an accepted contribution behind the native published tip with
its original Change-Id and complete patch equivalence. Unavailable or contradictory
evidence stops recovery before publication or a guessed second merge. No public
build input or agent trust flag can establish the internal record.

Package requests contain a `reference`, an argument-array `check`, and a reason.
The package service prepares a proposed configuration, obtains policy or human
approval, validates it in a separate job, and checks the adopted configuration.

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
- `tools.yaml` embeds three validators: review files, approved edits and package configuration.

See the [design](../../guides/adaptive3/DESIGN.md),
[implementation assessment](../../guides/adaptive3/IMPLEMENTATION.md), and
[tests](../../recipe-tests/adaptive3/README.md) before widening use.

For foreign includes and diagnostic jobs, see [the reuse guide](../../guides/adaptive3/REUSE.md).
The [supported-worker check](../../guides/adaptive3/VALIDATOR_WORKER_CHECK.md) covers the
validator dependency boundary separately from local routing tests.

The shared [review/v2 form contract](../../guides/REVIEW_V2.md) describes declarations,
source resolution, native responses and compatibility for custom includes.

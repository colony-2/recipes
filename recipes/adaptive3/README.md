# Adaptive3

The default development recipe, built around one cycle:
**Execute → full Validate → Review**. Corrections repeat the whole cycle.
Questions stay in Review. Accepted work advances directly to the next stage.

The five stages are Direction, Preparation, Implementation, Outcome acceptance,
and Integration/publication. Direction and Outcome have human review. The other
stages use independent agent review. An accepted explanation can finish at Direction.

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
inline; delivery uses a child adaptive3 job and a native wait.

## Dependency publication

Consumer-initiated work: B is updating its feature and discovers it needs an API
change in A. B can keep its work, ask A to implement and publish that change, wait,
then update its dependency and finish locally. B is the workflow parent of A’s
delivery job, but B depends on A’s API. B needs no additional coordinator or local
implementation job for this reason alone.

Provider-initiated adoption: A needs B to adopt A’s new API as part of A’s request. A
can coordinate a same-cell implementation job through review and publication, then
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
and publication. Publication recovery carries the completed merge forward.

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

# Cross-cell repository sessions within one job

Status: proposed implementation. This document defines the desired behavior;
the op and input names below are illustrative, not existing c2j APIs.

## Objective

A job executing for cell A can create and continue a conversation grounded in
cell B's repository, mandate, and instructions without starting a job in B.
Use this for ownership assessment, requirements discussion, design feedback,
and deciding whether an existing cell or a proposed new cell should own work.

The central requirement is **no repository changes carried forward**, not
read-only filesystem enforcement. The B checkout can be writable: the agent
may experiment, generate files, or run checks. Each turn discards that checkout.
Only conversation state and explicitly selected consultation artifacts persist.

Actual implementation for B still runs through a job targeting B. A consultation
can recommend that work, but does not create it implicitly.

## Identity and state

| Concept | Value during a consultation |
|---|---|
| Owning job and runtime cell | A's existing job and cell |
| Consulted cell | B, resolved through normal cell configuration |
| Repository context | An independent checkout of B at an immutable commit |
| Instructions | B's applicable `AGENTS.md` files and `.c2j/mandate.md` |
| Session | A separate conversational thread for this consultation |
| Git persistence | None for B; A's incoming Git state passes through unchanged |
| Durable outputs | Replies, transcript, session checkpoint, brief, selected evidence |

Do not replace A's `context.git` or injected current-job identity with B's.
Expose the consulted identity separately in the prompt and structured metadata.
In particular, `c2j self` is not the source of truth for the conversation's
perspective: checkout-based resolution and owning-job identity are distinct.

Do not place B beneath A's managed worktree. Otherwise ordinary op checkpointing
could accidentally commit the auxiliary checkout into A. Do not share a writable
clone, index, or working tree between sessions. Repository fetch caches can be
shared if each turn materializes its own independent checkout.

## Proposed capability

Introduce one logical operation, `cell_session.turn`, with open-or-resume
semantics. Expose it first as an op that recipes can include in A's job. An
agent-facing tool can later invoke the same durable contract; a separate
long-running agent service is unnecessary.

Proposed inputs:

| Field | Meaning |
|---|---|
| `cell` | B's canonical repository identity; required for a new session |
| `ref` | Optional initial ref; defaults through B's normal configuration |
| `purpose` | For example `mandate_assessment`, `requirements`, or `design_review` |
| `message` | The current question or feedback |
| `session_ref` | Prior session-checkpoint artifact; absent on the first turn |
| `turn_id` | Stable request identity within this session for replay handling |
| `context_artifacts` | Explicit request/design evidence shared with the consultant |

The launcher resolves all runtime directories. Callers should not supply
worktree, workdir, inbox, or outbox paths. On continuation, the session manifest
supplies B and the pinned commit; conflicting cell/ref inputs are rejected.

Proposed output contract:

```json
{
  "version": "c2.cell-session.turn/v1",
  "session_ref": "<new checkpoint artifact reference>",
  "turn_id": "design-2",
  "status": "answered",
  "consulted_cell": "github.com/example/server",
  "snapshot_commit": "<resolved commit>",
  "mandate": {
    "path": ".c2j/mandate.md",
    "sha256": "<hash of mandate bytes>",
    "state": "present"
  },
  "answer": "The server owns token generation; the client owns iteration.",
  "questions": [],
  "suggested_work": [],
  "assessment_artifact": "<optional mandate-assessment.json reference>",
  "brief_artifact": "<consultation-brief.md reference>"
}
```

`status` is `answered`, `needs_input`, or `error`; it describes the turn, not
whether the work fits B. Ownership assessments use the separate
[mandate contract](CELL_MANDATE_SPEC.md). Runtime failure and an unfavorable
answer are different: a well-supported `outside` verdict is a successful turn.

## Execution of a turn

1. Resolve B and pin its ref to a commit on the first turn. Record the mandate
   and instruction revisions. Subsequent turns use that same commit.
2. Materialize a clean B checkout in op scratch outside A's managed Git root.
3. Restore only this session's conversational state into an isolated session
   directory. Keep session storage separate from the B checkout.
4. Run Codex with B as its repository context. Supply B's instructions, the
   question, selected artifacts, and an explicit consultation-mode instruction.
5. Explain that local experiments are disposable: no publishing, merge, deployment,
   or child submission is part of a consultation. The requesting session decides
   whether to request actual work. Do not forward child-submission capability
   into the consultant merely because the owning op has a broker.
6. Validate the structured answer and any mandate assessment with the normal
   schema-gate mechanism. Record available evidence and errors honestly.
7. Persist the response, transcript, brief, and session checkpoint as artifacts.
   Exclude the B checkout, local commits, thin packs, patches for automatic
   application, build caches, and arbitrary scratch contents from checkpointing.
8. Return A's incoming Git state unchanged and discard the B checkout. Do this
   on successful, failed, cancelled, and interrupted execution; recovery cleanup
   handles abandoned scratch directories after worker loss.

The session can remember an experiment and retain an explicitly exported log
or explanatory code example. This does not turn those files into either cell's
code or into the next turn's repository state. Each new turn tells the model
that its previous uncommitted changes are absent; experiments must be recreated
if later reasoning depends on them.

Changing `worktree_path` alone is insufficient: it changes where Codex runs but
does not establish the checkout lifecycle or the Git-persistence contract. An
OS read-only mount can be optional defense, but is not a delivery prerequisite.
Ordinary sandbox/resource policies still apply. No special write-isolation
feature is required merely to permit disposable local edits.

## Durable conversation and replay

The checkpoint manifest identifies the owning job, consulted cell, pinned
commit, mandate hash, runtime session ID, transcript/checkpoint artifacts, and
last completed turn. A session ID alone is insufficient across workers.

Have one active turn per session. Identical retries of a completed `turn_id`
return its recorded response; different content with that ID is rejected.
Commit the reply and next checkpoint together. A crash before completion may
rerun the unfinished model turn from the last committed checkpoint; exactly-once
model execution is not promised. Never publish two competing next checkpoints.

An explicit refresh creates a new checkpoint revision with the new commit and
a recorded context refresh. It retains the transcript but forces reassessment
of affected conclusions. Moving branches must not silently change an existing
conversation's repository context.

For an initial op implementation, each turn is a durable task in A's job, with
artifacts passed between invocations. No B job is submitted or awaited. A later
tool interface must use the same durable turn/checkpoint storage; launching an
untracked subprocess with a machine-local session directory is not equivalent.

## Handoff to actual work

At the end of consultation, A can continue locally, consult another candidate,
submit work to B, or propose a new cell to the root workflow. The consultant's
suggested work is data, not a submission action. Keep normal dependency creation
and waiting in A's existing build/evolve workflow.

When submitting to B, attach the brief, transcript, mandate assessment, consulted
revision, and optionally the session checkpoint. Never attach a consultation
worktree or silently apply its experimental edits.

B's job rechecks its current mandate and relevant source changes, then adopts
the requirements context through its normal design gates. Prefer continuing
the existing conversation when native import works; otherwise create a fresh
session from the brief and transcript. Supply fresh B-job paths, execution
instructions, and capabilities rather than inheriting A's runtime configuration.

Native adoption requires exclusive session transfer or a supported fork; A and
B must not concurrently mutate the same checkpoint. The consultation author
does not become the independent reviewer of its own design. A new-cell proposal
includes the consulted candidates and reasons their existing mandates do not
cover the proposed responsibility.

## Implementation responsibilities

| Owner | Work |
|---|---|
| c2j | Resolve auxiliary repository context, isolate it from the owning Git chain, define turn/artifact durability, preserve job identity |
| c2ops Codex | Run against the supplied checkout, import/export isolated conversational state, return structured outcomes without publishing repo changes |
| recipes | Provide consultation prompts and includes, consume mandate assessments, decide routing and actual child work |

The boundary can be implemented as a c2j operation composed with the Codex
extension or as an extension using supported runtime repository/session services.
Choose the smallest implementation that proves the persistence invariant; do not
add a general job-wide repository switch or a persistent cell-agent daemon.

Source inspected on 2026-09-29 already provides Codex `sessionId`, a worktree
override, and `codex-home-state` artifacts. c2j consumes operation Git results
into the owning job's Git state. Those are building blocks, not an existing
auxiliary-repository session API. Validate explicit checkpoint import on a fresh
worker instead of assuming machine-local session caches supply portability.

Deliver first: one same-job consultation turn, then continuation and replay,
then portable handoff. Reuse the existing ephemeral JobDB integration harness.
Native cross-job session adoption can follow the portable brief without blocking
the initial consultation capability.

## Acceptance test statements

These are proposed implementation tests, not claims that the capability exists.
Each statement is at most 30 words; file entries identify implementation areas.

| ID | Statement | Files / areas | Importance | Level / dependencies |
|---|---|---|---|---|
| CS-01 | A's job consults B without creating any B job. | c2j session op; consultation recipe | Critical | Integration; ephemeral JobDB, two temporary repositories |
| CS-02 | The consultant reads B's pinned source, mandate, and instructions while the owning job remains A's. | c2j session op; c2ops Codex launcher | Critical | Integration; deterministic agent |
| CS-03 | Local B edits and commits never change A's checkpoint, B's upstream, or the next consultation checkout. | c2j Git persistence; session op | Critical | Integration; disposable Git repositories |
| CS-04 | A resumed conversation remembers its discussion after worker replacement while starting with a clean B checkout. | c2ops session import/export | Critical | Integration; separate workers, ephemeral JobDB |
| CS-05 | Replaying a completed turn returns its recorded reply without advancing the conversation twice. | c2j session checkpoint store | Critical | Integration; worker interruption |
| CS-06 | Conflicting turn content and concurrent session writers cannot publish competing checkpoints. | c2j session checkpoint store | Critical | Integration; concurrent workers |
| CS-07 | Failed and cancelled consultations leave the owning job's Git state unchanged and no resumable dirty checkout. | c2j session op | Critical | Integration; injected failure/cancellation |
| CS-08 | Missing mandates request clarification; unfavorable fit assessments remain valid consultation answers. | consultation recipe; mandate assessment gate | High | Integration; deterministic agent, schema gate |
| CS-09 | Actual B work can consume the consultation brief without importing experimental repository changes. | build/evolve handoff | Critical | Integration; ephemeral JobDB |
| CS-10 | Explicit snapshot refresh records changed assumptions instead of silently accepting stale design conclusions. | session manifest; design review | High | Integration; changed repository and mandate |

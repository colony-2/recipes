# Adaptive2: implementation and initial review

**Current status:** `build.yaml` now selects adaptive2 for new submissions.
See [the rollout assessment](ROLLOUT.md). The plan and initial trial results below
record the earlier opt-in milestone; pending capabilities remain identified.

**2026-11-08. Experimental; root `build.yaml` still uses adaptive.**

The subsequent [plain-language iteration](PLAIN_LANGUAGE_ITERATION.md) changes
how agents speak as owners and includes fresh live examples. This assessment
records the initial implementation and its first trials.

Start with the [real review packets](results/2026-11-08/README.md).
This implements the first runnable milestone from [TRIALS.md](TRIALS.md): let a
human judge the actual framing documents before completing and deploying the
whole variant. The [proposal](PROPOSAL.md) remains the target for subsequent work.

## What changed against the plan

| Planned behavior | Implemented behavior |
| --- | --- |
| Four understandable work types | The first agent returns `feature`, `bug`, `explanation`, or `oversight`. Consultation receivers use the same types for their assignments. No extra model classification task. |
| Direction approval before detailed planning | A real `input` checkpoint follows the one-pager. Approval advances; feedback returns to framing; cancellation stops. An unanswered review cannot start implementation. |
| Preserve important design questions | The framing prompt specifies the five requested sections and explicitly forbids a page, word, or question-count cap. UI work requests a mockup. |
| Orient a reviewer quickly | Prompts ask for the original problem, owning cell, work type, proposed outcome, and a descriptive review title. `request.md` remains available. Review metadata identifies the primary document and selected sources. |
| Keep the accepted direction | The recipe retains the exact approved artifact as `approved-direction/one-pager.md`. Later agent output cannot replace it. Reframing returns to direction review. |
| Detailed planning, then implementation | Detailed design, test statements, and the local execution handoff follow approval. Implementation uses the existing fresh, writable session path. |
| Receiver writes the assignment | A receiving consultant returns a typed `handoff.md`. The coordinator checks its stored identity against an accepted consultation before dispatch; a requester-written replacement fails validation. |
| Readable consultations | Each terminal consultant reply supplies a summary. The recipe renders public replies into `conversation.md` and retains the documents linked from earlier replies. No private model reasoning is requested or displayed. |
| Challenge unnecessary work | The consultant checks existing interfaces and explains alternatives. Completed advice can return `answered` with no delivery child. Disagreement is useful when supported by evidence, not mandatory ceremony. |
| Readable final review | The outcome prompt covers changes, others' work, tests, omissions, interface/upgrade implications, and changes from the approved plan. Native tests exercise reaching the outcome review after initial approval. A complete live delivery cycle is still pending. |
| Preserve recovery and package handling | Existing helpers and mechanisms are reused. Recovery can add selected evidence alongside the receiver's unchanged handoff. Changing the assignment requires the receiving cell to revise it. |
| Keep adaptive available | All changed orchestration and prompts are under `recipes/adaptive2/`. Existing adaptive sources and the root entrypoint were not changed. |

The implementation copies the orchestration and helpers that select the new
prompts/schema, and includes unchanged helpers directly from adaptive. This keeps
the trial isolated. It does create maintenance duplication; shared abstractions
should follow demonstrated needs after reviewing the variant, rather than
reorganizing the working adaptive implementation during this experiment.

## What the tests establish

Native tests run actual c2j state transitions, artifact storage, workspace
selection, review forms, and child operations. They script the model decisions.
They do not establish that prose is understandable.

- Direction: stop, unanswered review, requested revision, direct explanation,
  approved planning followed by fresh implementation and outcome review.
- Approval identity: a later forged copy of the approved document does not replace
  the original seen by assessment.
- Consultation: an objection and receiver revision, an existing-API answer with
  no child, directory spelling normalization, and accurate repair diagnostics.
- Handoff: the child receives the receiver's actual stored document; a rewritten
  assignment is rejected before submission. Selected recovery evidence can accompany
  the original handoff.
- Evidence export: the native live-trial wrapper retains selected evidence bytes
  before the disposable runtime is cleaned up.

The first complete pass covered 9 cases. Live trials then exposed a directory
validation problem: an otherwise valid handoff directory without a trailing `/`
was rejected, and the generic correction text incorrectly suggested a missing
session. The recipe now normalizes that spelling and reports the actual failed
conditions. New regressions cover both. A scope error in the first diagnostic
rewrite was caught and fixed by native execution before the final live rerun. A later presentation check replaced a broken relative-link
summary alias with a short index pointing to the original summary. Conversation
headings now use the descriptive summary heading instead of repeating the whole
request; native consumers verify the rendered links.

The current initial suite has **13 passing native cases** across four files.
The unchanged adaptive suites also passed **58 cases**: flow (39), consultation
(15), review (1), and parent recovery (3). This is a selected regression set, not
a claim that every repository test or every adaptive2 recovery path was run.

Commands, with `c2j` resolved to the pinned runtime and its normal package environment:

```sh
c2j test run --directory recipe-tests/adaptive2 --out-dir /tmp/adaptive2-final-verified
c2j test run --file recipe-tests/adaptive/flow.test.yaml --out-dir /tmp/adaptive2-original-flow
c2j test run --file recipe-tests/adaptive/consultation.test.yaml --out-dir /tmp/adaptive2-original-consultation
c2j test run --file recipe-tests/adaptive/review.test.yaml --out-dir /tmp/adaptive2-original-review
c2j test run --file recipe-tests/adaptive/parent-recovery.test.yaml --out-dir /tmp/adaptive2-original-parent-recovery
```

The final combined adaptive2 run passed all 13 cases. It includes the recovery
evidence case, corrected consultation links, and centralized direction-review
prompts. Native replay of the recorded receiver response also passed.

Runtime: c2j **0.0.124**, source `33e2a4de4e99d3a577a38dca4b8de33d43a099ce`.
The local environment required the existing Nix/proot wrapper to resolve packaged
operations. Tests used actual packaged operations; no replacement Git scripts or
fake package executables were introduced.

## Live evidence and limits

The [packet index](results/2026-11-08/README.md) records actual outcomes and links
the untouched model documents. These are small disposable notebook/storage
repositories, not production jobs. Normal packaged Codex calls, separate cell
workspaces, session checkpoints, artifacts, and review operations are real.

The native harness cannot leave a review pending and export an arbitrary set of
artifact bodies after teardown. Direction trials therefore supply a **scripted
cancel** at the first review, then materialize the selected files for export.
This is a stop control, not human approval. No implementation or merge follows.
Native tests separately verify that an unanswered review cannot advance.

The final bug trial reached its review and passed in 233 seconds. The final
feature/UI trial **failed at the 30-minute deadline**. Its consultation completed;
the resumed notebook agent generated the one-pager, mockup, screenshots, and
eleven passing browser-check groups, but never returned its structured response.
No direction form was created. The last recorded event was a file change at
21:46:47 UTC; the native deadline expired at 21:56:52 UTC. No explanatory error
was present in the captured Codex stderr, and the retained session log also had
no final assistant response. The cause is unresolved; passing native
state tests does not resolve this live completion failure.

The feature files are retained **draft producer outputs**, not a successful
checkpoint packet. They can inform the presentation review while this completion
problem is investigated. Do not promote the variant on the strength of them.

Earlier runs are recorded honestly: the first feature trial timed out after a
useful consultation; the first receiver trial hit the handoff validation bug;
a receiver assertion used a recipe helper unavailable in test expressions;
early bug runs retained the one-pager but lost supporting artifact bodies during
test cleanup. The final capture wrapper prevents that evidence loss. The receiver document
packet uses a native replay of its recorded live response to verify the corrected
assertion and rendered links; its authored documents are byte-identical to the
original live files. Neither a
timeout nor a partial artifact export counts as a successful complete packet.

The fixture environment also limits what these examples prove. Its repositories
model the notebook UI and storage contract, not a running HTTP service. The agents'
`c2j self`/`cells` attempts reported missing local configuration; one reported that
its CLI lacked job inspection. The recipe runtime itself was pinned, but these
trials do not establish that every tool visible inside a Codex session has the
production task context. Keep that distinction explicit when evaluating recovery
or deployment claims. Tool setup details that do not affect the direction should
move out of the primary human document in the next wording iteration.

Native call traces also omit files above 64 KiB and encode captured bodies as
text. The export helper checks every selected artifact against its recorded byte
size, using retained observations or untouched producer files when needed. Feature
screenshots were retained from the producing outbox for this reason; a missing or
invalid-sized body causes export to fail instead of producing a partial packet.
The incomplete feature run required a separate, explicitly labeled copy of its
unpublished outbox drafts; their metadata records that different provenance.

## Follow-up after reviewing these documents

These are planned features beyond the first-checkpoint milestone, not delivered
capabilities:

Before further live delivery trials, investigate why the feature agent stopped
emitting events after writing its documents. Inspect the retained session/operation
diagnostics and reproduce with a smaller UI framing request; do not assume that
raising the time limit or changing the approval gate fixes it.

1. **Reuse approval for delegated work.** Children currently take their own
   direction review. Carry an explicit parent's approval of an unchanged receiver
   brief and test missing, changed, and forged approvals before enabling reuse.
2. **Approved prerequisites during planning.** The existing execution dispatch
   restriction remains. Add a deliberate path for approved prerequisite delivery
   without making the planning workspace writable.
3. **A full oversight trial.** Exercise multiple owners, nested consultation,
   selected partial recovery, and combined completion in adaptive2. Existing
   adaptive recovery passes are useful evidence, not a substitute for this trial.
4. **Live final review.** Continue accepted examples through implementation,
   verification, and merge review after feedback on the initial documents. Test
   material scope changes and unchanged-rebase approval reuse in this variant.
5. **Pinned child routing and rollout.** Publish the variant, explicitly pin its
   child recipe selector to the tested revision, then verify remote resolution.
   The current `@main` default names adaptive2 but does not pin the parent's exact
   captured revision. No production default was switched.
6. **Comparison and wording.** Compare a matched existing-adaptive live packet and
   tune confusing phrases using concrete human feedback. Keep substantive Q&A;
   shorten setup narration and internal runtime details where they obscure the
   decision. This is not a test of whether Codex is generally a capable agent.

The present recommendation is to review the initial packets, revise their
presentation, and then complete these remaining trials before promotion.

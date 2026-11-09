# Human reviews must not consume automatic retry budgets

Approved proposal, 2026-11-09. Implementation and validation are recorded in
[the implementation assessment](turn-limits/implementation.md).
The incident evidence below describes the recipe before this change.
This fits the recipes cell's responsibility for review, coordination, and recovery.

There are two problems: a real handoff failure hidden behind a misleading limit
message, and an optional implementation counter that can stop work after human
feedback. Fix both. Increasing the limit would only delay the handoff failure.

## What happened in the reported job

Job `7f7199c5c7c08380f4a5fc1e809c476d`, cell `cortex`, on
`http://192.168.1.195:9047/c2` ran the shared build from commit
`610a59bba9eb707b96f84972b929958dff1c6dcb`. It started at 01:04:04 UTC and
failed at 02:23:13 UTC on 2026-11-09. The requested work was a contextual chat
panel backed by durable assistant sessions.

| Stage | Recorded behavior |
| --- | --- |
| Initial design and consultation | Cortex consulted the relevant owners and prepared a one-pager. |
| First human direction review | The human requested changes: use c2j operation resolution and recipe-declared configuration inputs. |
| Revised consultation and design | Cortex-assistant supplied an agreed feature handoff. Cortex revised the proposal. |
| Second human direction review | The human approved the revised direction. |
| Detailed planning | Cortex produced the design, 23 test statements, and its local execution handoff. |
| First implementation turn, `work#6` | The agent requested execution by cortex-assistant and copied its agreed handoff into the outbox. |
| First correction, `work#7` | The agent adjusted document metadata and source links, keeping the handoff contents unchanged. The coordinator rejected it again. |
| Second correction, `work#8` | The agent selected the existing filename without producing another copy. The recipe still resolved the retained copy and rejected it. |
| Failure | The response-correction allowance was exhausted. The coordinator submitted no prerequisite execution. |

The final retained diagnostic, `error/summary/response-corrections.md`, says:

> Execution requires the agreed receiving cell's typed handoff and original selected artifact references. Ask that cell to write or revise the assignment; do not substitute requester-authored files.

This was **not a human-review cap**. The human revision and approval both worked.
The three final responses were all `next: coordinate`, which the implementation
counter excludes. The failure came from `repair.attempts > 2`: the original
rejected response followed by two automatic correction attempts.

The terminal message instead says that an implementation-turn cap **or** a
response-correction limit was reached. That makes two different failures look
like one and hides the actionable explanation from the human or parent.

### The handoff contents were unchanged

I retrieved the receiver's original handoff, both Cortex-produced copies, and the
copy retained on failure. All four are 10,702 bytes with SHA-256:

```text
1d83874e2de03e53b03af03559898eba1f4b475de65934a656c4af0abb3531e4
```

The receiver returned `outcome: agreed`, `work_kind: feature`, and a handoff
under `iter1/consultant/work/`. The requested execution owner was the same cell,
`cortex-assistant`. This was an unchanged document with a new storage occurrence,
not an unauthorized change to the agreed scope.

## Bugs and related limits

| Location | Finding | Proposed treatment |
| --- | --- | --- |
| [`coordinate.yaml`, execution](../../recipes/adaptive2/coordinate.yaml) | Agreement validation compares complete artifact references after removing only `name`. An unchanged outbox copy has a different producer task and fails. | Recover the accepted receiver document from consultation history and forward its original reference. Accept an unchanged copy; reject a changed assignment with a precise reason. |
| [`agent-turn.yaml`, normalize](../../recipes/adaptive2/agent-turn.yaml), [`artifact-result.yaml`](../../recipes/adaptive/artifact-result.yaml), and [`develop.yaml`, record/repair](../../recipes/adaptive2/develop.yaml) | New outputs replace inbox references. Repair retains those outputs and overlays them again on subsequent turns. Removing the new copy from a later outbox cannot restore the accepted receiver reference. | Restore authoritative receiver bindings from the existing consultation result before dispatch and during correction. Keep erroneous copies separate from those bindings. |
| [`develop.yaml`, iteration_limit](../../recipes/adaptive2/develop.yaml) | Different exhaustion paths share one vague failure message and code. | Separate the causes and include the actual unresolved diagnostic in the terminal failure. |
| [`develop.yaml`, dispatch](../../recipes/adaptive2/develop.yaml), and the previous adaptive implementation | When `max_iterations` is positive, it counts qualifying implementation turns over the whole job. `ask_user` and `review` qualify. Human answers do not reset it. The guard also runs before dispatching other phases. | Count consecutive autonomous work, exclude human interactions, and start a fresh allowance after a real human response. Never block the human's answer from reaching the agent. |
| [`consultation.yaml`, record/expert_record](../../recipes/adaptive2/consultation.yaml), [`consultation-start.yaml`](../../recipes/adaptive/consultation-start.yaml) | Consultation already counts agent exchanges within a round and resets `round_iterations` after human direction. No lifetime human-round cap was found. | Preserve this behavior. Add repeated-human-round and nested-consultation coverage. Keep the automatic debate bound. |
| [`develop.yaml`, recover_work/assessment](../../recipes/adaptive2/develop.yaml) | Recovery counts consecutive failed working turns against the same Git candidate. Intervening successful work can reset it. Human progress is not represented explicitly, so reset behavior depends on the route taken. | Make the human-response boundary explicit and test it. This is a robustness gap, not a confirmed cause of this job's failure. |
| [`inspect.yaml`](../../recipes/adaptive2/inspect.yaml), consultation response repair, creation review repair | These bounds apply to automatic response correction. Creation's ordinary human review loop has no turn cap. | Retain bounded automatic repair and prove human feedback starts a new attempt. Do not remove these bounds indiscriminately. |
| Native merge chasing and conflict recovery | These bound automatic Git retries, not human conversations. | Keep these safeguards and unchanged-diff approval reuse. A newly reviewed work attempt should not inherit unrelated exhausted retry history. |

## Proposed changes

### 1. Make the recipe carry the agreed handoff

Use the consultation records we already retain. The agent selects the receiving
cell and handoff directory; it should not have to preserve storage identities by
managing outbox copies or annotation metadata.

For execution:

1. Find the selected accepted assignment in the existing consultation history.
   Check its owner and work type, and identify the original selected documents.
2. Bind the original receiver references directly. Preserve the existing focused
   directory selection and separate `recovery/` or `feedback/` additions; do not
   send every consultation document to the child.
3. If the agent supplied a different storage reference for the same selected
   document, compare those two files. Identical contents use the receiver's
   original reference. Different contents require the receiver to revise the
   assignment; never silently execute the replacement or silently ignore edits.
   Use an ordinary artifact-bound file comparison only when necessary, not a new
   persistent hash registry or an LLM judgment of byte equality.
4. On correction, rebuild those bindings from consultation history. A previous
   rejected copy must not win because it remains in `retained_artifacts` or the
   current document map. Preserve a changed proposal separately as useful evidence.
5. Explain a rejection specifically: which assignment or file is missing, which
   owner disagrees, or which file changed. Do not ask for a new consultation when
   the recorded agreement already exists and its contents are unchanged.

This preserves the receiver-authorship requirement while removing storage
bookkeeping from the agent's job. Document roles and source links remain
presentation metadata; changing them cannot repair a storage-reference mismatch.

### 2. Make human interaction unlimited by recipe turn counters

Use the following rule consistently:

**A budget limits an uninterrupted automatic loop. A human response starts a new
allowance; requesting or processing that response does not consume the allowance.**

Keep `max_iterations: 0` as the default. For an explicitly configured positive
value, change it from a lifetime implementation count to a consecutive automatic
work allowance, and update the input description accordingly.

- Exclude human questions, human review requests, and the response to human
  feedback. Review or clarification loops can repeat as often as the human needs.
- Reset only after an actual collected human response: one-pager revision or
  approval, outcome feedback, clarification answers, consultation direction, or
  a package decision. Merely creating a form, waiting, or reaching a state does
  not reset anything. An automatic package-policy decision is not human input.
- Count continued autonomous work and agent disagreements until they complete,
  make the relevant progress, exhaust their local allowance, or reach a human
  response. Keep response repair and consultation debate budgets separate.
- Check a general automatic-work allowance only before another autonomous work
  turn. Do not use it to prevent a human-directed framing or planning turn.
- For nested advice, propagate the fact that a new human response occurred to
  the suspended caller when returning that advice. Use existing review receipts
  and consultation transcript entries; do not let repeated reads of the same
  saved response manufacture fresh allowances.

Implement this in transitions and existing state outputs, not just prompts.
Where an explicit scalar counter/reset is necessary, keep it local to the loop.
Do not add another compound workflow object or a parallel job-event registry.
Use existing review results to distinguish genuine human responses from automatic
progress and reused historical advice.

Exhaustion must not manufacture a human question just to renew the allowance.
Human input is for a concrete decision or correction, not retry-budget management.

The agent-only guards still matter: two agents should not argue forever, invalid
responses should not retry forever, and an unchanged operational failure should
return to the parent with its evidence. Explicit execution/time budgets remain
separate runtime controls; they are not a reason to charge a human review round
against a recipe turn counter.

### 3. Report the actual reason for stopping

Split response repair, autonomous-work exhaustion, consultation debate, and
operational recovery into distinguishable failure paths. Preserve the original
validation or execution cause in the terminal message and selected diagnostics.

For this incident, an informative failure would have said:

> I could not start the cortex-assistant work because the recipe rejected the
> handoff's artifact reference. The agreed document is retained. Two automatic
> correction attempts did not resolve the reference mismatch.

It should not say that the human used too many turns, suggest that agreement was
missing when it existed, or recommend restarting from scratch as the only option.
The parent can use the existing inspection and selective recovery mechanisms.
No additional human approval is needed just to repair recipe bookkeeping.

## Tests to add before implementation is considered complete

All cases should use native c2j transitions, artifacts, reviews, and child
submission. Script model decisions; do not substitute a prompt-text assertion
for execution. Exercise the public adaptive2 build, not only the old adaptive
regression fixture.

| Expectation | Importance; level/dependencies | Coverage to add |
| --- | --- | --- |
| Repeated human questions and replies complete with a one-turn automatic allowance. | Critical; integration, c2j | `recipe-tests/adaptive2/human-turns.test.yaml`, `develop.yaml` |
| Repeated one-pager and outcome revisions remain possible after substantive work. | Critical; integration, c2j | `human-turns.test.yaml`, `direction-review.test.yaml` |
| Automatic continuation without human input exhausts its allowance and reports that exact cause. | Critical; integration, c2j | `human-turns.test.yaml`, `develop.yaml` |
| Human consultation direction renews the debate allowance; agent-only disagreement remains bounded. | High; integration, c2j | `consultation.test.yaml`, including nested advice |
| An unchanged republished handoff starts the child with the receiver's original artifact identity. | Critical; integration, c2j/artifacts | `handoff.test.yaml`, `build-handoff-recovery.test.yaml` |
| Changed handoff contents cannot execute without receiver agreement. | Critical; integration, c2j/artifacts | `handoff.test.yaml` |
| Selecting the original after a rejected copy recovers despite retained retry artifacts. | Critical; integration, c2j/artifacts | `build-handoff-recovery.test.yaml`, `agent-turn.yaml` |
| Exhausted response repair preserves its actual diagnostic and reports two correction attempts. | High; integration, c2j | `build-handoff-recovery.test.yaml`, `develop.yaml` |
| Saved human feedback cannot repeatedly reset a resumed automatic loop. | High; integration, c2j persistence | `human-turns.test.yaml` |

The test filenames above that do not yet exist are proposed additions.

### Why the existing tests missed it

The handoff fixture passes the receiver's stored reference directly into the
coordinator. It proves that the original works and a replacement fails, but skips
the parent agent's real output normalization and repair path. It does not model
an unchanged outbox copy followed by selection from retained artifacts.

The direction tests cover one revision and approval using the default disabled
implementation cap. The explicit cap test is in the previous adaptive suite and
checks planning exclusions, not repeated human questions or outcome revisions.
Passing those tests therefore did not establish the policy requested here.

## Scope and evidence

Implement the active adaptive2 fixes first, plus any genuinely shared helper
changes and their regression coverage. The previous adaptive implementation has
the same lifetime implementation predicate; avoid documenting it as having the
new semantics unless it is updated too. No c2j API addition is needed for the
identified recipe bugs. Runtime budget policy is a separate concern.

Inspection covered this one job, its 51 recorded task occurrences, both collected
human direction responses, relevant agent outputs, terminal diagnostics, and the
four handoff artifacts compared above. The recorded recipe revision matches the
local source inspected. There was no final job result; earlier outputs and the
failure artifacts remain available. No jobs were changed or submitted, and no
production recipes or tests were edited during this investigation.

To retrieve the evidence with an inspection-capable c2j, use the stated JobDB,
then `job log JOB --limit 100 --output FILE`. Select exact task occurrence IDs
from that inventory, not only node names. The relevant occurrences are:

- Receiver revision: the consultation under `coordinate#2`, task list index 37
  in the captured inventory; artifact `iter1/consultant/work/handoff.md`.
- Human responses: `direction#1` and `direction#2`, `input:collect_user_input`.
- Execution and corrections: `work#6`, `work#7`, `work#8`; the first two export
  `coordination/request-2-0/artifacts/iter1/consultant/work/handoff.md`.
- Final failure: `iteration_limit/stop_attempt`; retrieve
  `error/summary/response-corrections.md` and the same handoff path with
  `job artifact JOB --task TASK --name NAME --output FILE`.

Raw inspection downloads are in scratch under `/tmp/turn-cap-*`; the identifiers,
source references, key diagnostic, and equality evidence above make the finding
reviewable without attaching the entire job history.

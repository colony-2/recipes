# Adaptive3 follow-ups: requester-led recovery and clearer reviews

Status: implementation in progress, 2026-11-13. This records the feedback on the
[adaptive2 history audit](AUDIT_ADAPTIVE2_HISTORY.md). See [the implementation record](FOLLOWUP_IMPLEMENTATION.md) for delivered changes and tests.
The work is tracked in [TODO.md](TODO.md), alongside the three previously agreed items.

The main rule is simple: give the working agent the result and let it decide what
to do. Use the resolver when that agent is stuck, cannot run, or needs an exhausted
automatic allowance renewed. A child failure alone is not a reason to invoke it.

These changes fit the recipes cell. Native artifact storage, durable waits and
inspection belong to c2j; review rendering belongs to its consuming application.
Any missing capability at those boundaries should be identified by a focused test,
not replaced with recipe-owned document or job-management machinery.

## 1. Return child outcomes to the agent that requested the work

**Bug fix and behavior adjustment.** The requester should receive successful,
failed and cancelled outcomes in the same way: the actual job ID, terminal status,
original outcome/cancellation message, and references to useful results and errors.
The native result remains available for inspection; do not inline its whole body.

A return prompt should look like this:

> You asked storage to keep the last three saved versions. Job JOB has finished
> with status failed. Its message is: “The verification command could not find
> sqlite3.” Read its results and the errors supplied in inbox/work/children/JOB/.
> Decide what to do next. You can recover useful work, correct the request and try
> again, use a successful replacement, or continue if this dependency is no longer
> needed. Explain your choice. Respect an instruction to stop; do not repeat an
> unchanged attempt or submit work that is already running.

The recipe transports the outcome and resumes the requesting agent's session and
assignment. It does not decide that every failure needs a retry, human review or
resolver. A successful process also needs the requester's judgment about whether
it delivered the requested outcome. Retain the distinction between a corrective
cancellation and an instruction to stop the broader work.

Concrete changes:

- In `agent.yaml`, preserve c2j's recorded child identities even when the model's
  final report is invalid. Correcting a report must not forget its side effects.
- In `consultation.yaml` and `lifecycle.yaml`, deliver terminal child outcomes back
  to the requester instead of converting every failed/cancelled child to parent
  `stuck`. Preserve the requester across nested consultations as well.
- Use the same return behavior for small jobs submitted through agent tools and
  for recipe-submitted delivery. Use native job outputs/history; do not add a
  parallel child ledger or recipe-generated IDs.
- Keep submissions and native waits as separate durable operations. Ordinary
  re-entry follows the recorded submission. A replacement is a new explicit
  requester decision. If the requester identifies an existing active/successful
  job, wait on or consume that exact job instead of submitting again.
- Preserve the current stage's permissions and session separation. A result
  arriving during planning does not turn that session into implementation.

The requester enters the normal full validation cycle after acting on the result.
Only its own unresolved `stuck` response, an unavailable requester, or a local
allowance pause needs resolution. Parent notification while a child is still open
remains a separate [runtime requirement](RUNTIME_REQUIREMENTS.md).

**Checks:** real children that succeed, fail and are cancelled all return to the
requester before any resolver call; a corrected retry and a no-retry choice both
work; a successful replacement is reused; an active replacement is awaited; an
invalid report after submission cannot duplicate the child. Verify messages,
identities and useful artifacts, not just the final status.

## 2. Start `resume_from` in the resolver

**Enhancement.** Treat `resume_from` as an instruction to inspect previous work
and choose where to continue. Do not automatically start another Direction review.
This is a new job using the selected recipe, not an implicit replay of the old job.

The initial resolver prompt should say:

> Continue this request using job PRIOR as context. Read the latest human direction,
> current status, useful outputs and any existing child attempts. Work out what is
> already complete and what remains. Choose the stage that should run next and
> explain why. Recover only what that work needs. Preserve real approvals and
> completed effects; ask only for a decision that is still missing.

Concrete changes:

- Route a supplied `resume_from` directly to a recovery entry of `resolver.yaml`,
  with the current request, prior job ID and any submitted artifacts.
- Let the resolver inspect exact task outputs, approvals, current child/goal
  status and snapshots using c2j. Distinguish an unavailable record from evidence
  that a decision was never made. Later human guidance wins over older plans.
- Return a chosen stage, concise continuation instructions and selected native
  references. No generated recovery/handoff manifest or copied job history.
- Initialize the selected stage from these supplied values. The current entrypoint
  assumes earlier stages ran in this job; remove that assumption for recovery
  without manufacturing completed stage outputs.
- Configure the new job before its selected work needs repository hooks/settings.
  Configuration must preserve the resolver's chosen destination and context.
- Recover actual prior approval and its document when it still covers the work.
  A copied agent statement that something was approved is insufficient. Changed
  direction returns to Direction; unchanged approved work need not be reapproved.
- Restore unfinished code through the managed workspace in Implementation and run
  the complete validation cycle. Previous tests are useful context, not current
  verification. If a merge already completed, preserve its native result and
  continue the remaining publication work without merging again.

Stage selection is the resolver's judgment about remaining work. It does not add
a set of selective validation routes: the destination stage runs its full cycle,
and subsequent stages follow the ordinary order.

**Checks:** approved unfinished work reaches Implementation without another
one-pager approval; changed scope reaches Direction; missing inspection access
keeps a specific recovery question open; an existing successful child is adopted;
a merged change resumes publication once. Include a paginated prior history and
assert that the selected stage never reads nonexistent earlier-stage outputs.

## 3. Preserve diagnostics as separate directories

**Bug fix.** Put each producer's diagnostics in its own subtree and preserve the
paths beneath it. Use native directory references where available.

An illustrative inbox layout is:

```text
work/
  review/                         current human-facing documents
  children/JOB/results/           selected child result directory
  children/JOB/errors/TASK/       that task's original diagnostic subtree
  errors/verify/TASK/             a local verification failure
```

`JOB` and `TASK` stand for existing native identities, including the attempt where
needed. They are not new identifiers to be maintained by agents. Different
wrapped causes receive distinct subdirectories within their producer's errors.
Keep native command logs intact, including command, relative directory and streams.

Concrete changes:

- Stop flattening diagnostic paths to their basename in `hooks.yaml` and
  `cycle.yaml`. Two `check.log` files must remain two distinct files.
- Follow original failure/cause references and select the relevant diagnostic
  subtrees. Do not synthesize a fake directory reference by renaming one file.
- Forward before-design, prepare, verify and publish failure directories to the
  next working agent. If the agent is stuck, pass the same references to resolution.
- Bind hook output and child results separately from `review/`, so neither can
  replace a human document with the same filename.
- Prompts identify the directory and problem. They need no list of all filenames.
  If bytes are unavailable, preserve the original source reference and exact
  retrieval error so the agent can decide whether it matters.

**Checks:** two children with same-named logs, multiple wrapped causes, a failed
prepare/publish hook and a hook file named like the current review. Assert exact
bytes at distinct paths, original producer identity, and no overwritten review.

## 4. Make repository-required reviews actually reach validation

**Proposed cleanup.** A configured specialist is an additional validation agent.
It does not own another workflow, approval checkpoint or repair loop. The shared
Validate activity owns its invocation and combines its findings with the other
checks into one result.

The current bug is concrete: a required pre-design specialist can report a problem,
but its result is only shown to the writer. It does not constrain Direction
acceptance. Some configured assessment instructions also never reach the assessor.

### One place to define validation

Keep the five repository hooks and the existing configure contract. Research from
`before_design.yaml` still reaches Execute before framing. Move the configured
specialist calls out of Execute and into Validate, where they assess actual work.
The similarly named research hook and specialist checkpoint have different jobs:
research informs the proposal; validation checks the proposal after it exists.

Define the mapping once in `validate.yaml`:

| Stage | Configured specialists in its full validation | Assessment prompt addition |
| --- | --- | --- |
| Direction | `before_design` | `plan_assessment`, applied to the one-pager's level of detail |
| Preparation | `plan_assessment` | `plan_assessment`, applied to detailed design and test expectations |
| Implementation | `outcome_assessment` | `outcome_assessment`, applied to the implemented behavior and checks |
| Outcome | No additional specialist invocation; validate the complete human review against the actual work and recorded findings | `outcome_assessment`, applied to the accuracy and completeness of that review |
| Integration | No configured specialist invocation; validate native merge/publication results | No assessment addition |

This is a fixed definition of each stage's full validation, not a decision about
which checks to rerun after a particular edit. Every correction repeats all checks
for its destination stage. A behavioral correction found during Outcome returns
to Implementation and therefore reruns its specialists and verification too.

Execution guidance stays with Execute: `design` for Direction, `test_plan` for
Preparation and `implementation` for Implementation. Remove the substitution of
assessment instructions into the outcome writer's prompt as their only consumer.
Both the general assessor and configured specialists receive the corresponding
assessment guidance, current assignment, latest human direction, relevant work
and diagnostic references. Their task is bounded by the stage being validated.

### One result and one correction path

`specialists.yaml` becomes a small iterator over configured requests. Each request
uses the existing read-only agent wrapper, common validation prompt and validation
response schema. Add its role and question as ordinary prompt context. Do not
call the human Review activity or introduce a specialist-specific response protocol.
Keep the original result and source references in native task outputs.

The general assessor receives these findings alongside native checks. Validate
returns one combined result:

- Pass when the required native checks, required specialists and general assessment
  pass for the current assignment.
- Otherwise return concrete findings and diagnostic references to Execute. Include
  all current findings, rather than hiding everything behind the first failure.
  A missing or unusable required assessment is incomplete validation, not success.
- Optional advice has no independent veto. The general assessor can still identify
  a real defect supported by that advice and request a correction on its merits.

The existing recipe condition enforces required results; an agent cannot turn a
failed required check into a pass by writing a more favorable summary. The working
agent decides how to address the findings. It can fix the work, obtain owner advice,
or explain why a reviewer used a mistaken premise. The next complete validation
assesses that response. It need not change correct code merely to satisfy an
unsupported suggestion.

For example, if the human explicitly excluded deployment, a specialist must assess
the agreed source change rather than demand deployment. The next pass includes
that original human direction. Human feedback has greater weight than agent advice;
reviewers do not gain authority to redefine the assignment.

A failed specialist operation also returns its concrete error to the working
agent. Enter the resolver only if that agent is stuck/unavailable or the enclosing
correction allowance needs renewal. There is no specialist retry counter: its
finite request list is traversed once per full validation pass. Repeating the pass
uses the existing stage correction loop.

### Implementation scope

| File | Planned change |
| --- | --- |
| `execute.yaml` | Keep research hook delivery; remove specialist invocation and the separate owner-findings prompt construction. |
| `validate.yaml` | Own the single stage mapping, supply assessment guidance, collect specialist findings and produce one complete validation result. |
| `specialists.yaml` | Reuse the agent/validation contract; return current results and references without its own workflow or persisted obligations. |
| `prompts/validate.yaml` | Explain specialist role/question, stage scope, current human direction and how to report actionable findings. |
| `prompts/execute.yaml` | Keep correction guidance ordinary: address the current findings, including disputed assumptions. |
| Hook guide and native tests | Document the mapping and verify both rejection and correction through the existing lifecycle. |

Keep changes inside these building blocks. No new public settings object,
per-stage wrapper recipes, checklist files, approval certificates, or generated
code to assemble findings. Use native values and references; substantive documents
remain for people and actual work.

### Validation before accepting the cleanup

Use scripted agent responses to test orchestration, without claiming to test
whether a model is a good specialist:

1. A required Direction specialist rejects the one-pager. The working agent gets
   its actual finding; no human acceptance form opens yet. After correction, the
   full validation runs again and the normal human review opens.
2. Multiple findings survive aggregation. A file-check failure does not erase a
   specialist finding or the original diagnostics.
3. A small document correction still repeats every check in that stage. No route
   skips a specialist because the edit appears unrelated to its subject.
4. Optional advice alone does not veto progress; required missing/invalid output
   cannot silently pass. A native specialist failure reaches the working agent
   before resolver escalation.
5. Configure a local hook with distinct assessment instructions. Assert that the
   actual general and specialist calls receive the correct stage guidance, current
   human wording and document references. Writer-only delivery does not pass.
6. A specialist initially applies an excluded requirement, receives the human
   correction on the next full pass, and withdraws it. No extra human approval or
   scope-reconciliation file is introduced.
7. A job with no configured specialists retains its ordinary lifecycle. Repeated
   unsuccessful correction reaches the stage's local allowance, not a new nested
   specialist recovery loop.

This plan preserves required validation while leaving the substance of diagnosis
and correction to the agents. This mapping is implemented; see the implementation record.

## 5. Bound each automatic loop independently

**Behavior adjustment.** Every automatic loop gets a positive finite allowance.
Reaching it pauses that loop; it does not fail the job. A resolver or human can
renew it with a finite allowance when the next approach or continuing progress
justifies more work. Human conversation has no turn cap.

Keep counters at the scope that owns the repetition:

| Loop | What it counts | Proposed starting allowance |
| --- | --- | ---: |
| Stage correction | Another complete Execute → Validate → Review pass after automatic correction | 4 passes |
| Owner conversation | Replies in that owner exchange; nested advice has its own allowance | 4 rounds |
| Child replacement | New attempts for the same requested outcome after terminal results | 3 attempts |
| Package recovery | Another proposal/probe attempt for the current unmet requirement | 3 attempts |
| Merge chase | Another merge attempt after upstream movement or conflict correction | 3 attempts |
| Resolver correction | An automatic correction followed by another unresolved return | 2 attempts |

These are proposed initial values to tune, not elapsed-time limits. Keep defaults
with their owning loops; do not add a large public configuration object. Give the
existing `max_iterations` a finite default and require a positive value for that
allowance instead of using zero to disable all limits.

A suspended outer loop does not spend attempts while a child loop runs. For
example, three storage retries consume three storage attempts, not three parent
validation passes. A completed outer pass counts once when it actually repeats.
A merge chase retains its own count across returns through Implementation and
Outcome; entering another stage does not reset that chase. Completion or a real
new assignment starts a new loop; relabeling the same failed work does not.

At exhaustion, return the local loop, attempted work, progress and unresolved
problem to the resolver. The resolver may propose a correction or grant that
loop additional attempts. Preserve the grant in native state. It must not
silently reset unrelated counters or grant itself an endless series of renewals:
its own automatic correction allowance ends in a human decision. A human can
renew or increase either allowance. A question-only response grants nothing.

Repeated unanswered/invalid model responses in Review also need a finite local
recovery path. Count automatic response failures, never human question/answer
rounds. New explicit human direction can start a new allowance for the affected
work; replaying an old receipt cannot do so.

**Checks:** each loop exhausts and pauses; nested work leaves the outer counter
unchanged; repeated upstream movement cannot escape its merge allowance; resolver
renewal permits slow progress; repeated resolver failures reach a usable human
form; human questions remain uncapped and do not renew automatic work.

## 6. Add a short inspection guide to new-session context

**Prompt clarification.** Restore the few operational details that prevent
unproductive guessing. Keep the normal context short:

> Inspect status and task history with `c2j job show JOB --json` and
> `c2j job log JOB --json`. Use the returned task ID. Discover field paths with
> `c2j job fields JOB --task TASK --json`; copy a returned pointer rather than
> guessing one. Download its complete value with `c2j job log JOB --task TASK
> --field POINTER --output ./scratch/value.json`; previews can be truncated.
> List that task's artifacts and retrieve the needed files. Final job results
> may be absent even when earlier tasks have useful output. Follow `next_cursor`
> with `--cursor` when needed. Use command `--help` for attempt selection and
> `c2j restart --help`, `c2j job restart-points --help` and
> `c2j job restart-context --help` for recovery options. Report an actual access
> error; do not treat a failed read as a failed child or poll unchanged work.

Put downloaded inspection data in scratch outside the managed checkout and
outbox. Keep permissions/availability discovery through `c2j self`. Retain the
existing snapshot guidance. The longer [inspection playbook](../JOB_INSPECTION_PLAYBOOK.md)
is an authoring reference; do not assume that path exists in another cell.

**Checks:** an inspection fixture whose useful field differs from the example,
a paginated task inventory and an output larger than the preview. Native retrieval
must return exact content. A small live trial can assess whether the short wording
is sufficient; mocked prompt assertions cannot establish agent judgment.

## 7. Pass directories while keeping human presentation small

**Enhancement.** Use native directory references for selected result/review/error
subtrees. This removes per-file handoff accounting and preserves relative links.
It must not become a reason to carry the entire outbox or all previous attempts.
A producer selects a coherent directory; older versions stay at their source.

For titles and purpose, use the level a human actually needs:

| Item | How to describe it |
| --- | --- |
| Review | One descriptive decision title, using the existing title field |
| Selected directory | A short purpose for the collection, using native group metadata if supported |
| Primary document | One selected relative path; its heading and opening paragraph explain the decision |
| Important supporting material | Descriptive filenames and ordinary labeled links in the primary document |
| Bulk logs/screenshots | Browsable directory contents; individual files need no mandatory annotation record |

For example, a review titled **“Merge notebook: recover earlier saves”** can open
`review/save-recovery.md`. That document links **“Phone recovery screen”** to
`screenshots/phone-recovery.png` and **“Storage owner's recommendation”** to
`consultation/storage.md`. The directory is attached once. Those labels already
explain the purpose of the files without a separate per-file metadata ledger.
Use the existing review document; do not require another README/index solely for
recipe plumbing. A human-oriented gallery/index is useful when the material needs it.

Concrete changes:

- Carry selected directory references through agent outputs, consultation,
  child inputs, diagnostics and review. Preserve original native identity.
- Keep the existing review title/primary selection. Presentation belongs to the
  current review and should not accumulate across stages or redefine scope.
- Let file/link/image validation inspect the materialized directory. The recipe
  does not need to serialize its contents back into state just to validate it.
- Reusing an unchanged directory reuses its reference. A newly authored collection
  is a new snapshot; its author must keep required linked material available.
  Directory references do not themselves merge old and new collections.
- Apply metadata only at the review boundary. If the UI supports group metadata,
  use one title/purpose per attached directory. Otherwise put the purpose in the
  primary document and retain the directory; do not recreate per-file annotation
  machinery to simulate group presentation.

**Runtime/consumer check before implementation:** the checked-in
[artifact set binding guide](../C2J_ARTIFACT_SET_BINDINGS_USER_GUIDE.md) describes
expanding an artifact map into individual bindings. That is not by itself evidence
of a compact stored directory reference. Confirm the current c2j directory-reference
contract the user identified, and its behavior through child results and review.
Use the native representation rather than inventing YAML syntax here. A local
`file://` directory or an archive is not a substitute for a durable reference that
works on another machine. If a compact reference is expanded into a large chapter
or the UI cannot open its primary document, record the specific c2j/consumer gap.

**Checks:** a directory with thousands of files crosses a real child boundary;
serialized parent state/chapter size does not grow by repeatedly embedding its
file inventory; a renamed directory preserves relative links; the human review
opens its primary document and nested images/logs; unrelated outbox files stay
out. Measure chapter size, not only validator stdout. Check title/purpose display
in the actual review UI.

## 8. Restore usable feedback entry in human reviews

**Confirmed consumer contract mismatch.** The user selected “Ask a
question or change the direction” in adaptive3 and received no feedback box.
Adaptive3 declares `message` and `notes`; adaptive2 uses `feedback` and
`annotations` for the corresponding fields, and normal reviews use `revise` as
the non-approval value. This difference is a plausible consumer-contract mismatch.
c2j's review guide says decision names have no built-in workflow meaning; native
recipe tests alone cannot establish how the consuming UI renders them.

Plan:

- Reproduce the generated adaptive3 form in the actual review consumer and compare
  its field handling with a working adaptive2 form.
- Use the working `feedback` paragraph field and `annotations` upload field in
  adaptive3 Review and Resolver. Use the consumer's established action value
  where required, with a human label such as “Discuss or request changes.” Update
  all prompt readers, acceptance conditions and reply paths together.
- Keep the meaning of discussion: the agent interprets the feedback as a question
  or a change request. A UI action value must not automatically route a question
  into implementation. Approval with text or an upload must still be interpreted
  before work proceeds.
- On a discussion action with neither text nor an upload, leave the form pending
  with visible feedback entry. Do not send an empty turn to the agent or accept it.
- Keep the conversation and current proposal available across repeated resolver
  questions through the native session/state. Do not add a discussion JSON file.

**Checks:** click the discussion/change control, enter text and submit it in the
actual UI; repeat with an upload and with an empty submission. Verify that exact
text/attachments reach the answering agent, questions stay in Review, changes
reach Execute and approval stays explicit. Cover Direction, Outcome, package
approval and Resolver. Native tests that inject a response object bypass the
missing textbox, so they need this consumer-level complement.

If the UI ignores arbitrary valid paragraph fields, record that separately for
the consumer owner. No external ticket or recipe fix is part of this planning task.

## Order and boundaries

The feedback-entry bug comes first because it prevents useful human oversight.
Then establish the directory transport boundary, use it for diagnostics and child
returns, and add resolver-first recovery. Bound each affected automatic loop as
it is changed. Hook assessment wiring and inspection wording are independent.

Keep all correction paths on the same Execute → full Validate → Review cycle.
Use native state and references; no new internal handoff files, conversation
manifests, retry dashboards or per-file ledgers. Existing todo items for model
selection, complete titles and change reports remain open. Implementation is tracked in the todo list and implementation record.

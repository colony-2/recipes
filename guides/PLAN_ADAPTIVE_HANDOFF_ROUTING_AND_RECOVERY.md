# Plan: execution handoffs, sessions, routing, and recovery

Status: implemented and validated, November 7, 2026; all 289 adaptive cases pass with c2j v0.0.122. This follows the [non-archived job audit](AUDIT_NON_ARCHIVED_JOBS_2026-11-07.md). The sections below preserve the proposal and its motivating behavior; see [the implementation assessment](ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) for the delivered changes, regression evidence, and remaining runtime limits. Running production jobs are not modified.

The main correction is to hand off **the outcome of planning**, then run a fresh execution session against that handoff. A consultation request is not an implementation assignment. A consultation checkpoint is not the working agent's checkpoint. Each recipient gets a focused assignment and the files necessary to carry it out. Retaining an artifact in job history does not make it an input to subsequent tasks.

This fits the recipes cell's ownership. Recipes owns the changes below to prompts, sessions, orchestration, artifact delivery, and tests. Gitvend owns the gateway route repair; its operator owns deployment. c2j owns any additional durable wait or runtime diagnostic capabilities. The core recipe corrections can use the existing native operations.

**1. Generate an execution handoff; stop copying the consultation prompt**

Today, [coordinate.yaml](../recipes/adaptive/coordinate.yaml) builds the child prompt from `agreement.request.request`: the original question sent to a consultant. It then adds a sentence saying that consultation-only instructions no longer apply and appends execution guidance. That is why the c2j child receives both “implement” and “design consultation only; do not implement.” Its normal build entrypoint may subsequently append another design assignment.

Replace this with a small, current execution handoff authored by the agent that has the design and consultation results. The consultant provides its conclusions and implementation brief; the parent reconciles those with the final design, test plan, and any later decisions before submission. This should normally happen in the parent's existing progression turn, without adding a mandatory separate summarization task.

Apply the same boundary within a job: the final planning turn publishes `handoff.md` alongside `test-statements.md`, and the first implementation turn reads those files in a fresh session. When design is unnecessary, test planning derives the handoff from the user's request and repository findings. A child that already receives a complete execution handoff uses it directly.

The handoff should explain:

- The requested outcome and the cell doing the work.
- Settled design decisions, contracts, and constraints that affect implementation.
- The work this child must finish and how to validate it.
- Relevant current documents, with working relative links.
- External prerequisites and follow-up work, distinguished from this child's completion criteria.
- What the parent needs returned, such as a published API reference or validation result.

Use ordinary Markdown and files. The handoff should stand on its own for the decisions it conveys. Attach a source document when the recipient needs its exact contract, fixture, acceptance statements, or evidence; summarize decisions in the handoff when their history is unnecessary. Do not introduce another workflow-context JSON document or copy the entire transcript into the task. Earlier dialogue remains in job history and is attached only when it answers a specific need.

For multiple assignments, the parent can prepare descriptive directories:

```text
outbox/
  work/
    input-history/
      handoff.md
      test-statements.md
      supporting/
        api-agreement.md
    gateway-routing/
      handoff.md
      test-statements.md
      supporting/
        failing-fetch.log
```

A proposed execution request is deliberately small:

```yaml
next: coordinate
requests:
  - action: execute
    cell: c2j
    ref: main
    handoff: work/input-history/
```

`handoff` is a recipe field, not a c2j CLI flag. It identifies a directory of actual exported artifacts, not an opaque agreement key. The coordinator binds only that directory's contents at the child's inbox root, with no automatic additions from parent or consultation history. The current artifact map and ordinary file descriptors provide the inventory; the prompt does not enumerate files. Internal durable submission records still provide replay/idempotency and track replacements.

An execution prompt should look like this:

```text
Implement the assignment in inbox/handoff.md in this cell's managed workspace.
Read the supplied design, acceptance statements, and supporting files as needed.
Continue from the settled decisions. Inspect the repository, implement the work,
and run the checks needed to establish the requested outcome.

If implementation reveals a material design problem, explain it and request a
design revision. Use job inspection when additional saved context would help;
report required inputs that remain unavailable. The recipe manages verification,
merge review, and publication.

Return implementation.md and test-results.md with the result and useful evidence.
```

For the history-service child, `handoff.md` would start with “Implement the agreed historical input service for Cortex,” describe the three agreed API operations, and include the actual HISTORY/STORE acceptance statements. It would not contain the old instruction to perform consultation only.

Add an execution-handoff entry to the shared build contract. A complete handoff containing settled design and formal test statements enters implementation directly, with the normal verification and review gates intact. If only acceptance outcomes are settled, perform a bounded test-plan step first. Honor explicit cell policy requiring additional planning, and reopen design for a substantive conflict; do not restart design merely because this is a new child job. These are recipe inputs/transitions, not phase files in the inbox.

**2. Restore separate consultation and progression sessions**

The current code does share sessions. `coordinate.yaml` passes the working checkpoint as `requester_session`; `consultation-start.yaml` initializes the consultation requester from it; the coordinator subsequently copies the consultation's requester checkpoint back into progression. Design, test-plan, and implementation transitions also normally retain the same progression checkpoint.

That mixes roles. It is especially problematic because the Codex adapter applies additional instructions only when creating a session; supplying different instructions on a resume does not replace the original instructions.

Use these boundaries:

| Activity | Session rule | Workspace behavior |
| --- | --- | --- |
| Design | Fresh design session; resume within design | Const; preserve documents |
| Test planning | Fresh test-plan session; resume within planning | Const; preserve documents |
| Implementation | Fresh session receiving the execution handoff; resume for ordinary work and implementation recovery | Persist managed candidate changes |
| Consultation | Fresh requester and consultant sessions for that consultation; resume them only inside that exchange | Const; preserve advice and experiment evidence |
| Independent assessment | Separate assessment session | Const |
| Response correction | Continue the relevant session with an explicitly response-only assignment | Const; preserve corrected output files |

Pause the progression session while consultation runs, then resume that original checkpoint with the consultation's returned documents. Do not replace it with the consultation requester checkpoint. A new implementation child receives no consultation session at all.

Session separation does not require separate consultation jobs. Keep consultations inline, including foreign cell workspaces. A fresh requester session can inspect the parent's current managed candidate without inheriting its chat history; preserve the existing unpublished-candidate workspace behavior.

**3. Why implementation ran under `const: true`, and the correction**

The c2j child `SVYbGlC2gSzO0r8bUo1bEkBx1tT` was still in **design** when it reported missing documents. The following sequence occurred:

```text
phase = design
  → agent returns blocked
  → recover_work sets assignment = recovery, but leaves phase = design
  → agent.yaml selects the recovery prompt instead of the design prompt
  → agent.yaml still selects read_only from phase != implement
  → resume_read_only_session executes with const: true
```

The recovery prompt told the agent to diagnose and correct the problem. Combined with the child's overall implementation assignment, that led it to implement. The recipe discarded the worktree changes from the managed snapshot because the task was const. Its 115,158-byte patch artifact survived, but the recorded candidate hash did not advance.

This was a recipe mismatch, not an agent choosing its own persistence mode, and not a c2j failure to honor a writable task. The generic recovery assignment was added in `5c6a6fb`; it replaced the phase prompt without changing the phase used for persistence.

Fix it by keeping the phase's assignment present on every turn. Recovery is additional guidance about a failure, not a replacement phase. Use the same actual phase to select the prompt and whether repository changes persist:

- Design recovery repairs the design, obtains missing context, or returns a concrete unmet input. It does not ask for implementation.
- Implementation recovery repairs code and runs checks in a task that persists the candidate.
- Response correction explicitly changes only the answer/documents and remains const.
- Promotion from planning to implementation is an explicit state transition with a fresh implementation session and a complete handoff.

Do not fix this by making every recovery task writable or by globally removing `const`. Consultation experiments and independent review should still leave the candidate untouched. Do not accept an implementation claim from a planning/const task as completed source work. If such a task returns a useful patch, keep it as evidence and have an actual implementation task inspect/apply/test it.

**4. Route execution to the requested owner, not the consultant**

In the audited chain, Gitvend consulted root. Root correctly answered that recipes owned the consumer check and returned an execution request naming recipes. The coordinator recorded that information, but launch used `agreement.target.cell`, which was still **root**. It used the consultation's identity as the execution destination. Root then had to submit the recipes child itself.

Make the execution request's registered `cell` the authoritative destination. Resolve that cell and its requested/default ref through the existing target resolver, select its native workspace, and launch the child there. The handoff describes the agreed assignment; its source consultation does not determine the destination.

Require an explicit destination for execution. A missing or conflicting destination goes back to the producing agent for correction; it must not silently fall back to root or to the last consultant. A referral does not require a second consultation just to acknowledge dispatch. The receiving owner can resolve a real scope question after reading the assignment.

Return execution requests consistently from top-level, nested, and custom consultations. The parent incorporates them into current handoffs instead of exposing implementation requests only as text in `status.md`. One consultation can identify several owners; each gets its own assignment and handoff.

Keep native submission IDs and durable invocation records for monitoring and duplicate prevention. Do not require agents to invent or interpret `request-3-0/advice-1` agreement keys. A retry can refer to the prior native job it replaces; a Git `ref` must never be used as a job handle.

For this incident, the intended route is Gitvend → recipes. c2j becomes a separate dependency only if recipes identifies a necessary runtime capability or defect, not simply because root was asked for ownership advice.

**5. Replace agent polling with an explicit durable wait**

The agent response schema currently has no `wait` choice. `continue` returns directly to another agent turn. Known coordinator children are automatically awaited only on `review`, `outside`, or `blocked`. This explains the 17 Gitvend turns saying that the same child was still pending. The lower-level coordinator has an internal `await` operation, but the agent-facing schema does not expose that as a normal decision.

Add `next: wait` with this meaning: “I have no useful local work to do until the outstanding children return.” The recipe already knows the submitted job IDs; the agent should not list or poll them again.

```text
Continue useful local work while dependencies run. When their results are the
only thing you need next, return wait with a short explanation. The recipe waits
for those jobs and resumes you with their results. Do not spend turns polling.
```

Implement the transition as follows:

1. Collect known children from both coordinator submissions and automatic direct-submission outputs. Preserve native IDs and actual results; do not create a parallel agent-maintained status map.
2. Inspect their statuses once. Deliver already-available failures/results before blocking on a running sibling.
3. When none is ready, use `recipe.await_result_soft` with `return_when: terminal`. This durably suspends the workflow. It is not a shell sleep or another agent invocation.
4. On completion, bind status, errors, and exported artifacts into the standard result directories, then resume progression once.
5. Treat failed attempts as results the parent can repair, even if the associated goal remains open. Preserve cancellation semantics and fresh-job retry behavior.

Keep `continue` for concrete independent work; do not automatically block every parent as soon as it has a child. For an ambiguous `continue` whose summary only describes waiting, a small Jev classification can choose between useful local continuation and durable waiting. Give it the current response and child statuses, not entire histories. This is one general intent classification, not keyword matching or a rule per error message. The explicit `wait` path needs no classification. An unavailable classifier must not invent a completed result; return a focused choice correction to the agent through the existing response-repair path.

Unify this scheduling decision for direct and coordinator children. Today direct-child collection can wait immediately while coordinator children can repeatedly poll; neither difference should control whether independent work continues.

The existing implementation can inspect all children, then wait for one. Prompt wakeup when *any* of several running children changes still depends on a native durable wait-any capability; confirm current c2j support before implementation. If unavailable, retain one native terminal wait and rescan after it returns. That may delay a sibling's result, but it does not spend LLM turns polling. Do not claim wait-any behavior without testing it.

**6. Deliver a focused handoff for each recipient**

The missing files have a precise cause: `coordinate.yaml` launches with `agreement.result.final_artifacts` plus the conversation. That set contains the consultant's final reply, not the parent's final design/test plan. In the twelve-cell configuration batch, documents such as `package-matrix.json` and `validation-plan.md` were created later and therefore could never be in that earlier consultation result.

Fix the selection and delivery boundary, rather than expanding the collection forwarded to every task. The producing agent uses its current knowledge to write a self-contained handoff and selects the few attachments the recipient needs. The recipe delivers precisely that selection. A document being recent, returned by a consultant, or retained in the parent is not sufficient reason to include it.

For example, a c2j history-service assignment needs the agreed API contract and relevant HISTORY/STORE acceptance statements. It does not need Cortex UI drafts or the whole consultation transcript. A configuration child needs that cell's exact package requirements, applicable common constraints, and relevant checks. It does not need the thirteen-cell package matrix and every other cell's test plan. Preserve the meaning and identifiers of selected acceptance statements; extracting a recipient's scope must not silently change requirements.

Use the existing handoff directory as the selection mechanism. Its actual exported files are the delivery set; no second manifest or dependency graph is needed. The coordinator removes the directory prefix for the child's inbox and preserves original artifact identities when rebinding. A reference inside a transcript is not delivery of the referenced bytes.

Apply the same principle between steps in a job:

| Recipient | Inputs appropriate to its assignment |
| --- | --- |
| Consultant | The focused question and selected contracts or evidence needed to answer it |
| Implementer | The execution handoff, scoped acceptance statements, and necessary supporting files; repository source comes from its workspace |
| Recovery turn | The current assignment plus the relevant failure/result and current corrective feedback |
| Response correction | The response being corrected, validation errors, and files needed to correct that response |
| Reviewer | The current candidate's summary, acceptance statements, results, and relevant evidence |

This also requires correcting the local accumulation path: `develop.yaml` currently unions prior documents with new ones, and `task-documents.yaml` binds almost that entire collection. Preserve historical artifacts at their producing nodes, but pass an explicitly selected set as the next task's `documents`. An unchanged file can remain selected across turns; a superseded report or unrelated child's output should not appear merely because it was once received. Bind the selected files on each invocation so execution remains portable across workers. Session memory is not a substitute for file delivery.

Concrete rules:

- Require `handoff.md` and a valid artifact set before launching. Direct implementation additionally requires scoped formal test statements; otherwise explicitly enter test planning. A complete parent design document is not a mandatory attachment.
- Select the current version of needed files, including files produced after consultation. Reuse stored producer references when rebinding; preserve source annotations when a document is revised or copied.
- Deliver only the requested handoff directory. Do not merge the parent's document collection or every consultant output into it. Reject ambiguous filename collisions rather than silently overwriting files.
- Use `handoff.md`, scoped `test-statements.md` when applicable, and optional `supporting/`. Add `design.md` only when its detail is actually needed beyond the handoff.
- Validate paths and artifact existence deterministically. Let the receiving agent assess semantic completeness. Do not build a Markdown-reference parser or another metadata schema to decide whether a design is sufficient.
- If more context would help, the agent can inspect its own saved tasks or direct children and retrieve selected files using the supported commands in item 9. Known required inputs still belong in the handoff. A child cannot assume it can read its parent or siblings; report required material that remains unavailable.

When the unmet input can only be supplied by the parent, finish the unsuccessful child attempt with an actionable report through the existing failure/result path. The parent corrects its handoff and submits a fresh attempt from the normal starting ref. This general rule also covers other parent-supplied prerequisites. Do not make the child consult the parent's *cell* as a way to reach the parent's active agent, or repeatedly tell a consultant to inject files into an existing job. Neither is a supported message-delivery operation.

Do not create an automatic duplicate while the original child remains active. Recover running incidents separately after inspecting their current state. Selected earlier outputs can now be retrieved through documented job inspection and supplied in a corrected handoff; the concrete recovery flow is described in item 9 and [the recovery proposal](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md). Start again without salvaged work when it is unavailable or not worth reusing. Neither path needs chapter scraping.

**7. Keep acceptance aligned with the requested outcome**

The `.git` gateway bug needs a real Gitvend fix. The source repair and its regression tests can complete before operational adoption. The current child was told not to deploy, yet its generated plan made deployed-artifact inventory and fresh Cortex verification prerequisites for accepting the source fix.

The handoff and review prompts should distinguish three outcomes:

| Outcome | Completion evidence | Owner |
| --- | --- | --- |
| Repair the gateway source | Correct route behavior and relevant regression checks on the candidate | Gitvend |
| Adopt the repaired service | Successful deployment and bounded checks against the actual service | Gateway operator/deployment workflow |
| Complete the original Cortex verification | Original failing verification succeeds after adoption | Cortex parent |

The parent remains incomplete until its original outcome is satisfied. Finishing the source child does not falsely complete Cortex; it enables the deployment/adoption step and then the retry. Ask for an operator or deployment decision only when that is the actual next prerequisite, with a review explaining what is fixed and what remains. Preserve existing human merge decisions; do not add a new approval for every handoff.

Apply the same principle to the hook-consumer chain. Establish the requested failed-status behavior with existing native tests where possible. `verification.test.yaml` already exercises failed status with a successful helper operation and asserts `allowed: false`; it does not by itself prove every later publication transition. Add the smallest missing end-to-end assertion if needed. Do not make visibility of every internal composite value a product acceptance requirement when observed behavior can establish the result.

Reviewers should flag an acceptance plan that expands beyond the requested outcome. Correct that plan explicitly while preserving the user's actual requirements; do not silently mark an unmet requirement as passed. An unnecessary observation requirement is a planning error, not automatically a c2j implementation dependency. A necessary runtime improvement can still be requested with a concrete failing case.

**8. Keep useful repository context when classification input is large**

`classify.yaml` replaces all context with empty strings when serialized context exceeds 8,000 bytes, then requires design because context is unusable. A large README therefore becomes an accidental design gate.

Bound fields independently: preserve usable purpose and architecture context first, then a bounded README excerpt. Record omitted/truncated context honestly, without equating truncation with total absence. Keep the full artifact available for later inspection. A genuine lack of enough information can still require design; the number of bytes alone should not.

Execution handoffs also need their explicit entry path from item 1. They should not be reclassified as arbitrary fresh requests solely because they arrive in another job.

**9. Explain job inspection at session start and use it for selective recovery**

[GUIDE-Job-Inspection.md](../GUIDE-Job-Inspection.md) documents the newly available `c2j job` commands. This removes the earlier inspection/API blocker in the intermediate-results proposal. Recipe adoption now uses c2j v0.0.122; the implementation assessment records native tests. This is not evidence that every deployed worker has already been upgraded.

Add a compact capability explanation to the shared initial context in `prompts.yaml` → `turn.instructions`, delivered at session creation through `agent-turn.yaml`. All agent roles should know inspection exists, including consultation and review sessions that cannot submit jobs: the read capability is independent of submission permission. Keep the main instructions short and point to command help for detailed flags.

Proposed initial context:

```text
You can inspect saved work when you need more context. c2j self describes this
task's environment and advertises jobs.inspect. c2j job list --json lists your
direct children; c2j job log self shows this job's recorded tasks. Use c2j job
show JOB, log JOB, or story JOB --json to understand an execution. These reads
do not run or replay it and also work when submission is disabled.

Use c2j job fields and artifacts to discover available outputs, then read only
what helps your assignment. For a task, copy its exact occurrence ID from log
and pass it as --task "..."; select --attempt N when a specific retry matters.
Use job log/result --field with a JSON Pointer for an exact value, or job artifact
to download one file. Paginate discovery with the returned cursor and save large
values with --output FILE. Use c2j job <command> --help for the full syntax.

Job inspection covers your current job and direct children, including completed
or failed children. It does not imply access to parents, siblings, or arbitrary
jobs. Running work may not have recorded its outputs yet. If needed material
cannot be read, report the specific missing input and continue useful work.

For code recovery, c2j job snapshot can export a saved cumulative workspace into
a new scratch directory. Inspect its provenance and changes before reuse. Keep
the export in scratch; select useful files or a patch for a fresh execution
handoff. Attaching a patch does not install it in the new job's worktree. The
recipe still handles submission, durable waiting, and normal completion.
```

This is an optional tool capability, not a mandatory inspection task or an instruction to poll jobs. Preserve focused inboxes: inspect when a concrete question requires more context, and retrieve individual files by default. Use the task's supplied connection; selecting another `--jobdb` does not bypass its access scope.

For selective recovery, the parent receives the failed child's result, inspects its retained task outputs, and chooses useful work. It writes a corrected handoff explaining the selected sources, what failed, and what must be revalidated. It then supplies only those files through the existing artifact binding path to an ordinary new execution. No old session, execution prefix, or automatic Git-state adoption is needed.

If unpublished code is worth recovering, use a snapshot of the relevant task/attempt and workspace in scratch, inspect the cumulative changes, and prepare a portable patch or selected files. A snapshot contains cumulative state and retained artifacts through its boundary; it is not merely that task's changes. Default latest export uses successful state, while an explicitly selected failed attempt may expose diagnostic state labelled `failed_attempt`. Consult `snapshot.json` for the actual cell, repository, base, target, and workspace. Exporting all that history does not make it the next job's input.

Use exact stored artifact references when available, or download and republish selected bytes. Native submissions still need to bind the selected `documents` into the intended task inbox. Do not forward the entire exported directory, assume a commit hash transfers unpublished code, or substitute the current branch tip for an unavailable saved snapshot. A const task's discarded edits do not become durable through inspection; an explicitly published patch can still be recovered.

The implementation subsequently built and tested c2j v0.0.122 with its task helper, including native artifact retrieval and snapshot recovery. Upgrade deployed workers before relying on these commands. See [the updated recovery proposal](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md) for exact examples, access boundaries, and adoption tests.

**Implementation order and affected code**

| Step | Change | Main files |
| --- | --- | --- |
| 1 | Align phase prompts and persistence; separate progression/consultation sessions | `agent.yaml`, `agent-turn.yaml`, `develop.yaml`, `consultation-start.yaml`, `consultation.yaml`, `coordinate.yaml` |
| 2 | Add focused execution handoffs and direct owner routing; replace accumulated inbox forwarding with recipient selection | `prompts.yaml`, `response-schemas.yaml`, `coordinate.yaml`, `develop.yaml`, `task-documents.yaml`, `build.yaml`, `recipes/adaptive/build.yaml`, document-binding helpers |
| 3 | Add explicit waiting and unify child scheduling | `response-schemas.yaml`, `develop.yaml`, `child-results.yaml`, `await-child.yaml`, `coordinate.yaml` |
| 4 | Correct acceptance guidance and bounded classification | `prompts.yaml`, `classify.yaml`, relevant planning/review tests |
| 5 | Add initial inspection context and selected-output recovery using the documented c2j commands | `prompts.yaml`, `agent-turn.yaml`, `coordinate.yaml`, recovery tests, verified c2j runtime pin |
| 6 | Document the final contracts and assess the implementation against this plan | Adaptive process guide, authoring guide, implementation assessment |

All abbreviated recipe paths above are under `recipes/adaptive/`, except the shared `recipes/response-schemas.yaml` and root `build.yaml`. Change tests alongside each step and run the relevant suites before broadening. Keep existing native workspaces, Git operations, package policy, inline consultation, and fresh-attempt recovery.

**Behavioral test statements to establish before implementation**

Each statement below is at most 30 words. These test recipe behavior and actual transported/persisted state, not whether a mocked agent can write good prose.

| ID | Priority / level / dependencies | Relevant files | Statement |
| --- | --- | --- | --- |
| HR-01 | Critical / integration / c2j | `coordinate.yaml`, `prompts.yaml` | An execution child receives its generated assignment without inherited consultation prohibitions. |
| HR-02 | Critical / integration / c2j | `consultation.yaml`, `coordinate.yaml` | Consultation uses separate checkpoints while progression resumes its original session and unpublished candidate. |
| HR-03 | Critical / integration / c2j | `develop.yaml`, `agent.yaml` | Implementation starts a fresh session using the settled handoff and preserves its changes in the next task's checkout. |
| HR-04 | Critical / integration / c2j | `develop.yaml`, `agent-turn.yaml` | Planning recovery preserves planning instructions; implementation recovery persists a real repository edit. |
| HR-05 | High / integration / c2j | `agent-turn.yaml`, `consultation.yaml` | Consultation and response-correction experiments leave the managed candidate unchanged while preserving their output documents. |
| HR-06 | Critical / integration / c2j | `coordinate.yaml`, `route-target.yaml` | A root consultation referring work to recipes launches one recipes child and no root implementation child. |
| HR-07 | High / integration / c2j | `coordinate.yaml`, `consultation.yaml` | Nested and custom consultation referrals reach their explicit execution owners without another dispatch consultation. |
| HR-08 | Critical / integration / c2j | `coordinate.yaml`, document-binding helpers | Selected documents created after consultation arrive byte-for-byte in the execution child's materialized inbox. |
| HR-09 | High / integration / c2j | `coordinate.yaml`, document-binding helpers | Each child receives exactly its selected handoff files; unrelated parent documents, sibling outputs, and consultation history are absent. |
| HR-10 | High / integration / c2j | `coordinate.yaml`, `develop.yaml` | Missing handoff artifacts prevent submission and return a useful correction without asking the human. |
| HR-11 | Critical / integration / c2j | `develop.yaml`, `child-results.yaml` | A waiting parent suspends durably without another agent turn and receives the child's completed result. |
| HR-12 | High / integration / c2j | `develop.yaml`, `child-results.yaml` | Concrete independent parent work continues while children run; status-only continuation routes to waiting. |
| HR-13 | Critical / integration / c2j | `await-child.yaml`, `coordinate.yaml` | Child failure reaches the parent despite an open goal; a corrected attempt starts fresh and cancellation does not trigger resubmission. |
| HR-14 | High / integration / c2j | `classify.yaml`, `build.yaml` | A long README retains useful classification context; a complete execution handoff does not restart design. |
| HR-15 | Critical / integration / c2j | `verify.yaml`, `develop.yaml` | Failed hook status blocks merge and publication even when the helper operation succeeds. |
| HR-16 | High / integration / c2j | `develop.yaml`, `task-documents.yaml` | Subsequent tasks receive selected current files without accumulating superseded reports; earlier artifacts remain retained by their producers. |
| HR-17 | High / integration / inspection-capable c2j | `prompts.yaml`, `agent-turn.yaml` | New working, consultation, and review sessions receive inspection guidance even when job submission is disabled. |
| HR-18 | Critical / integration / task helper and failed child | `coordinate.yaml`, recovery tests | A parent retrieves selected failed-child outputs into a fresh handoff without forwarding unrelated artifacts or session state. |
| HR-19 | Critical / integration / task helper and scoped tokens | `agent-turn.yaml`, recovery tests | Inspection reads current-job and direct-child artifacts; unavailable parent or sibling inputs produce a specific unmet-input report. |
| HR-20 | Critical / integration / snapshot-capable c2j and Git | `coordinate.yaml`, recovery tests | Recovered changes are reviewed and applied in a writable task; unavailable snapshots preserve the option to start again. |

Extend the existing coordination, consultation-candidate, parent-recovery, job-monitoring, verification, and flow suites. Use real child submission, artifact materialization, suspension, and workspace edits wherever those are the behavior under test. Mock model decisions only to drive the relevant branch. Check persistence by reading the next task's worktree, not by trusting an agent's summary or patch artifact. Test the changed response schema through the existing native schema smoke after deterministic checks pass.

Acceptance-plan quality also needs a review of rendered prompts and the two incident examples. Do not claim deterministic mocks prove that future generated plans will always be proportionate. After rollout, inspect a small number of real executions for unnecessary consultations, missing inputs, polling turns, and premature deployment questions.

**Handling the already-running incidents after the recipe correction**

Resolved recipes in existing jobs do not change just because a new recipe commit is published. Inspect the then-current job state before intervening; this plan authorizes no cancellation or restart by itself.

- For the history-service chain, determine whether subsequent writable work already recovered the patch. If not, preserve the known patch and reconstruct a complete handoff before deciding how to replace the attempt. Do not assume the const task committed it.
- For the Gitvend routing repair, preserve the tested candidate and correct the source job's acceptance scope. Then arrange actual gateway adoption and the Cortex retry as their own remaining work.
- For the hook-consumer chain, reassess the required observable result before continuing the instrumentation dependency. Avoid another root intermediary.
- For the configuration batch, inspect children before replacing anything. Supply each recipient's current package requirements, applicable common constraints, and relevant formal statements. Children that already completed correctly do not need to be rerun merely for uniformity.

Record the implementation assessment against the numbered items and HR statements, including runtime versions and remaining limitations. Use c2j's existing task inspection capability; no broad parent-job access, chapter-scraping recovery system, or wholesale workflow replacement is required.

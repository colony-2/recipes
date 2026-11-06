# Next steps: simpler adaptive coordination and understandable reviews

Historical baseline, superseded by the [gap-closure plan](PLAN_ADAPTIVE_GAP_CLOSURE.md)
and [assessment](ASSESSMENT_ADAPTIVE_GAP_CLOSURE.md). The compatibility paths and
remaining gaps described below have since been removed or addressed.

Status: implemented locally, 2026-11-05. See the
[implementation report](IMPLEMENTATION_ADAPTIVE_COORDINATION_AND_REVIEWS.md)
for changes, validation, deliberate differences, and remaining follow-ups. The
proposal below is retained for comparison; use the report and recipe README for
the implemented request shapes.

The subsequent monitoring requirement supersedes attempt-based waiting and custom
replacement reconciliation below: monitor **goal success**, consume its successful
attempt, and allow authorized humans or agents to repair failed attempts within
that goal. Separate goals remain separate obligations.

The plan builds on the [job audit](AUDIT_JOB_PROMPTS_2026-11-05.md), including its
follow-up covering 27 jobs and 923 chapters.

## Direction

Let Codex investigate, interpret agreements, decide useful next work, and explain
results. Let the recipe enforce permissions, perform durable operations, wait for
goals, preserve evidence, and obtain explicit human decisions when needed. Use
small structured outputs at those boundaries; stop asking agents to maintain a
parallel model of workflow state.

Three recommendations drive the plan:

1. Remove unnecessary agent bookkeeping while preserving reliable execution.
   Replace the agent-facing key protocol where it causes ambiguity; retain native
   execution identities and existing durable submission/wait mechanisms.
2. Use one pattern for requesting help, receiving a result, and continuing the
   requesting task. Consulting another owner, waiting for their implementation,
   and correcting a response should not automatically become human questions or
   redesigns.
3. Every human review opens with **one current decision brief**. Explain what
   happened, what the person must decide, and what their answer causes. Organize
   evidence around that decision instead of presenting accumulated workflow files.

This fits the recipes cell's purpose. Recipe contracts, prompts, transitions,
review assembly, and tests belong here. Runtime suspension, task permissions,
credential resolution, and replay guarantees belong to c2j/c2ops and their
execution providers. Cortex owns how review metadata is rendered. We can improve
review content now without waiting for a new UI or runtime API.

The optional-title and selected-artifact fixes described in the audit are already
implemented locally. Preserve those changes. This plan addresses the remaining
problems; it does not claim those problems are already fixed.

## Delivery approach: justify replacement, regardless of change size

This is not a requirement that every change be incremental. Several earlier
redesigns make it especially important to establish what works before replacing
it again. A coordinated redesign is appropriate when it removes the underlying
problem more cleanly than accumulating exceptions. Small patches are not inherently
safer or simpler; a smaller final conceptual model matters more than a small diff.

| Treatment | Mechanisms | Reason |
| --- | --- | --- |
| Keep and reuse | Native child submission/results/waiting, managed Git persistence, artifact bindings, shared prompt include, independent assessment, native input forms. | The audit does not show that these mechanisms need replacements. Their composition and content often need correction. |
| Repair directly | Existing-job wait ordering, contradictory execution briefs, unchanged-baseline rejection, vague review wording. | Concrete faults with identifiable corrections, without another architecture. |
| Change coherently | Agent-facing key bookkeeping, downstream consultation handoff, change-request routing, review information hierarchy. | These contracts make agents or humans maintain state or choose implementation details that the workflow should handle. Changing producer and consumer together can be simpler than special cases. |
| Add a missing capability | Package request, authorization, validation, and adoption. | Missing tools cannot be solved by clearer wording or more work attempts. Reuse existing config and child execution. |

For each proposed replacement, identify the failing invariant, the existing code
we can reuse, the old behavior/code it eliminates, and the audit case that proves
the improvement. Include migration of in-flight/custom consumers in that decision.
Do not add a parallel framework while retaining the old one indefinitely. Temporary
compatibility is acceptable when it has an explicit removal point.

The sequence below organizes delivery and testing, not a ban on combining related
steps. If downstream requests and removal of agent-maintained keys need to land
as one contract change, do that. A universal new workflow engine or classification
service still needs evidence that the existing mechanisms cannot meet the need.

## 1. Simplify agent bookkeeping

### What identity is actually needed?

Today `agent.yaml` requires `keys` and keyed `consultations`; `develop.yaml`
maintains `plan_keys`; `coordinate.yaml` indexes separate thread and job maps by
those strings. Agents must invent names, repeat them in later phases, distinguish
incoming assignment keys from local keys, and clear obligations correctly.
The audit shows failures at each of those boundaries.

We need durable identity for an actual request or execution. We do not need the
agent to invent `review_input_story_contract_v2` and carry it through every reply.
A consultation's existence also does not mean implementation is required.

**Proposed ownership:**

| Information | Source and use |
| --- | --- |
| Work requested and why | Codex writes a concise request to the owning cell. |
| Agreement and accepted scope | Serving consultation outputs and its accepted documents. |
| Whether implementation is needed | Requester and serving agent establish this in the agreement; clarification alone creates no build obligation. |
| Request occurrence | Recorded recipe operation/run identity, assigned by the runtime or recipe. |
| Submitted child and current status | Native submission outputs and refreshed JobDB results. |
| Whether a failed attempt was replaced | Explicit reconciliation referencing the actual old and new jobs. |

Do not replace `keys` with another agent-authored slug, a title hash, or a required
`work_id` in every phase response. Titles are labels. Two requests to the same
cell may be different work; similar wording is not proof of duplication.

### Proposed request contract

Keep phase results and selected files. Replace the parallel agent-authored
`consultations`/`keys` bookkeeping with optional requests for external work. For
example, an illustrative proposed response is:

```yaml
next: coordinate
summary: The history view needs JobDB to define its continuation contract.
requests:
  - action: consult
    cell: jobdb
    request: >-
      Agree the pagination and continuation contract for input history.
      Establish whether existing APIs suffice or implementation is needed.
files:
  - path: design.md
    description: History view behavior and unresolved backend interface.
```

Use `consult` and `execute` for the external actions. Execution consumes a
reference to a recorded agreement plus a fresh execution brief. It cannot create
an agreement by asserting one exists. A consultation-only agreement needs no
execution request. Omit unused optional collections; do not require empty fields
at every phase. Keep other phase outputs unless changing them removes an observed
problem.

Agents may refer to an existing agreement or job using the native reference
supplied in context, but must not repeat it just to preserve state across phases.
The recipe consumes recorded request/results directly. An incoming assignment is
not an outbound prerequisite. Consultation alone does not imply implementation.

Prove how existing runtime identity handles replay, retries, inline consultations,
and resumed turns before replacing internal maps. Prefer recorded node invocation
identity plus request position within that immutable output. A fresh submission
with the same prose is not inherently idempotent. If necessary, retain an internal
recipe-assigned handle while removing the agent burden; this is not a reason to
make agents keep inventing keys. Preserve working execution machinery, and remove
`plan_keys` obligations and the correction loops made obsolete by the new contract.

### One owner for each submission

For coordinated project work, the recipe submits an agreed request using native
ops. Codex decides the requested work; the recipe executes and records it. Both
must not independently submit the same request. Agents may still directly submit
bounded validation jobs where their task explicitly permits it; those jobs are
already reported through automatic child-job outputs and need no manual ID list.

Consultation agents can return downstream requests through the same contract.
The coordinator performs the allowed consultation, returns the result, and resumes
the original negotiation. They do not need permission to launch implementation
jobs simply to ask another owner for advice. Enforce task submission restrictions
before effects; `const: true` alone is insufficient. Check the available permission
contract with c2j rather than inventing a YAML deny field.

### Classify requested work, not every runtime step

Describe each new work request as a **bug report**, **enhancement**, or
**clarification**. These categories help the receiving Codex understand intent;
they do not require three workflows or labels on every command and wait operation.

| Category | Request should explain | Expected result |
| --- | --- | --- |
| Bug report | Expected versus observed behavior, reproduction/evidence, affected scope. | Diagnosis and a fix with regression evidence, or a precise owner handoff. |
| Enhancement | Desired outcome, motivation, constraints, and acceptance expectations. | Agreed work and evidence that the outcome was achieved. |
| Clarification | The exact question and what the answer enables. | An answer with sources or a small bounded experiment; no implied implementation obligation. |

For the first version, put the category in the existing title/request text, such
as “Bug report: continuation drops the final history entry.” Keep one build and
consultation mechanism. If machine routing later needs a field, add an optional
`request_type` without overloading the existing `kind` used for feature/creation
routing. Classification belongs to the proposing Codex; it is descriptive and
can be corrected by the recipient without a human review. A clarification that
uncovers a defect can lead to a separately scoped bug report.

### Explain the job capability without encouraging delegation by default

The shared new-session instructions now identify the actual job, explain tasks
and automatic persistence, and describe direct child-job use as exceptional:

> You are a task in c2j job <actual job id>. A recipe defines the workflow;
> a job is its durable execution, and tasks perform individual steps in cell
> workspaces. c2j persists repository changes between steps and records published
> outbox files and child jobs.
>
> Where your assignment and token permit it, you can start, monitor, and read
> results of additional jobs. Use direct submissions rarely, for small
> clarification or validation exercises such as checking a new hook or an API
> usage example. Prefer existing documentation and local checks when sufficient.
> For most cross-cell work, return consultation and execution requests through
> the supplied response schema; the recipe coordinates them.

This wording uses the current schema; it does not announce an unimplemented
`requests` field. No-submission phases remain prohibited. A small exercise must
have a specific question, bounded invocation, and observed result. It must not
become a general build delegated to a child to evade the task's scope. Direct
submission never gains authority from being labeled “clarification.”

The implementation adds this context to `prompts.yaml`'s existing system
instructions, inserted only on new sessions through `agent-turn.yaml`. It leaves
session resumption and phase permissions unchanged. Shared-prompt tests check the
actual job identity, coordination guidance, and retained restrictions.

## 2. Use a common continuation pattern

The generalized flow is: **work → request help or return a result → fulfill the
request → resume with the result**. Preserve the original task's scope, session
policy, and exact human feedback. Do not start design over because a reference,
artifact declaration, or output field needed correction.

| Observation | Recipe action | Codex responsibility |
| --- | --- | --- |
| Known required child is running | Refresh and durably wait when no independent work remains. | Continue useful independent work when available. |
| Child has completed | Bind its current result and evidence. | Decide what that result means for the original request. |
| Child has failed | Return its failure and actual identity once. | Diagnose, repair, or explain a justified replacement. |
| Response has an invalid reference | Correct the response in the same logical task. | Fix the reference without redoing a sound plan. |
| Another cell must act | Resolve the agreed request through the coordinator. | State owner, requested outcome, and why it is needed. |
| Missing capability | Use an authorized requirements path or report the actual runtime owner. | Explain the capability needed and why. |
| Product choice or authority increase is unresolved | Ask a specific human question with a brief. | Explain alternatives and recommend a course of action. |

Do not infer human responsibility from `blocked` plus an empty list. Conversely,
a running child does not prove every blocker is resolved by waiting: Codex must
relate the blocker to that dependency. Unrelated product questions may still need
an answer while children run.

### Concrete scheduling corrections first

In `coordinate.pick`, an existing submission must refresh/wait rather than take
an unchanged `skip` route back to another implementation turn. In
`develop.record`, handle known relevant dependencies before generic intervention.
Refresh referenced jobs before describing them as reusable coordinators; accepted
submission is not successful startup.

Durable waits and response-only repairs must not consume the implementation
attempt allowance. Retain finite limits for actual autonomous work and separate,
small limits for response correction. Repeated failure should produce a diagnostic
about the unresolved operation, not a request to change valid requirements.
Start with native invocation counts and outcomes; do not build a second progress
ledger or hash all workflow state. The broader
[loop-guard proposal](PROPOSAL_BUILD_LOOP_GUARDS.md) remains useful background,
but its additional tracking is not a prerequisite for these fixes.

For validation children, replace “any historical failure permanently poisons the
result” with explicit reconciliation of a failed attempt and its replacement.
Keep both in history. A replacement only satisfies the obligation after its own
required checks succeed against the appropriate candidate. Codex proposes the
relationship; the recipe checks real identities, scope/candidate evidence, and
terminal outcomes. Unexplained or unrelated failures remain unresolved.

### Fresh execution instructions

Have the existing consultation/requester agent write the accepted execution brief
when work is agreed. Avoid adding a separate summarization task. Pass that brief
as the child request; bind the original consultation as historical evidence.
An illustrative child prompt is:

> You are implementing the agreed JobDB history API work within this cell's c2j
> job. Read the accepted execution brief and supporting agreement in inbox.
> Implement its scope and validate the stated outcomes. The consultation is
> complete; its earlier instruction to only discuss the work does not apply to
> this execution task. Scope and permission limits still apply.
>
> Run c2j self for your current context and permissions. c2j records repository
> changes and child submissions automatically. Continue independent work while
> dependencies run. Return requests for other owners through the coordinator.
> Put deliverables and relevant evidence in outbox; keep scratch work elsewhere.

The actual task adds its current scope and authorization explicitly. Do not append
an old consultation request as live instructions, or strip arbitrary prohibitions
with string substitutions. Agreement does not authorize every possible action.

### Preserve unchanged expectations

Remove the `test-statements.md` filename-presence rule in `develop.record`.
Returning an existing baseline is valid. Use existing immutable artifact identity
for the common case; if the agent republishes it under a new reference, compare
content before declaring a change. A changed reference alone is not a changed
expectation. Actual modifications still need the required redesign/deprecation
process. Artifact selection and reference repair remain independent of that rule.

## 3. Use Jev for narrow interpretation, not execution authority

**Recommendation:** let the working Codex node propose the next action first.
Experiment with Jev immediately before an otherwise ambiguous human escalation,
using those base outputs and current observed facts. Do not add a classifier to
every turn or ask it to rediscover facts that native outputs already contain.

The first useful question is: **“Does the described next step require a decision
or action from this human, rather than work available to the agent, coordinator,
or execution provider?”** Its output is advisory. Another useful experiment is classifying returned change requests as
implementation work or design revision after Codex has explained their impact.
This is internal routing, never a question the user must answer. A later experiment
can assess whether a review clearly states the decision and material limitations.

Use the existing Jev question mechanism in `classify.yaml` as the integration
reference, not a fictional new classifier API. Supply a concise Codex summary,
proposed request/question, current child outcomes, and relevant permission facts.
Do not dump the full history or truncate arbitrary JSON/document bodies into its
input. If judging the case requires reading files or investigation, return it to
Codex with the files instead.

A Jev disagreement goes back to the existing Codex session for one targeted
reconciliation. An unknown answer or provider failure does not itself cause a
human prompt. Use the explicit request and deterministic gates; unresolved semantic
ambiguity returns to Codex within the normal bound. Neither model may waive a
permission check, turn failed tests into passing tests, or reinterpret an explicit
human acceptance/rejection.

Pilot this against audit fixtures with labeled expected outcomes before enabling
it. Compare unnecessary human prompts, missed necessary decisions, extra turns,
and latency. Keep Jev only if it improves these results. It is not needed to fix
known waiting, key, baseline, or credential bugs.

## 4. Make every review understandable on its own

### What currently causes confusion

`review.yaml` recognizes only `merge-review.md` as an overview. It forces that
file, test statements, test results, and assessment all to `primary`. Other callers
can pass accumulated documents with a generic title and no current overview.
Generic titles such as “Clarify the current build” do not name the decision.
The intervention form puts the blocker explanation inside the decision question.
The merge-summary prompt also mixes outcome explanation with exhaustive file
accounting. A person must reconstruct what matters and what they are approving.

Older kernel brief/presentation documents describe a different implementation.
Reuse their useful review principles, not their large context blobs, parallel
provenance machinery, or deterministic paragraph-copying renderer. The active
adaptive recipes already have Codex nodes capable of writing a clear brief.

### Specific wording, with simple actions

Use the actual subject for the title: “Choose the history retention period,”
“Approve Go for backend validation,” or “Review the job-history change.” Avoid
“Clarify the build,” “Resolve a blocker,” and similarly generic requests. Standard
phrases are fine when their meaning is clear: “Merge these changes” and “Request
changes” name real actions. Do not use a long internal status explanation as the
question; put that explanation in the brief.

### One brief, authored by the node that understands the decision

For final acceptance, improve the existing `merge-review.md` produced by the
summary node. For clarification or intervention, the requesting Codex node writes
`review.md` as part of its current turn. Consultation deconfliction follows the
same convention. For a recipe-only interruption with no adequate brief, resume
the existing responsible node once to explain the stall; if unavailable, show a
short factual fallback naming the failed operation and required owner action.
Do not fabricate a recommendation or launch another work loop just to render it.

The brief should usually fit on one screen before supporting links. This is an
authoring target, not a truncation rule. Include these sections when applicable:

1. **Decision:** the exact question and what the answer causes.
2. **Summary:** requested behavior, achieved/proposed outcome, and what remains.
3. **Evidence and limitations:** meaningful checks, failed/skipped/not-run checks,
   unresolved findings, and important risks.
4. **Recommendation:** suggested choice and its consequence.
5. **Read more:** selected links with one sentence explaining when each is useful.

For a revised review, lead with what changed since the last answer and how that
feedback was addressed. Never silently re-ask an already answered requirement.
Keep detailed file accounting in `implementation.md` or a linked appendix; the
brief groups changes by their user-visible purpose. Preserve every material caveat
in the brief even when its underlying evidence is diagnostic.

### Concrete review presentation

Change `review.yaml` to accept an explicit overview document reference chosen by
the caller and validate that it is attached. Keep `merge-review.md` as the final
acceptance default; other reviews use their current `review.md`. This is a
recipe-include input mapped to the existing `form.overview_document_id`, not a
new c2j form field.

Use existing `document_metadata` and annotations:

| Placement | Contents | Example label |
| --- | --- | --- |
| Primary, first | Exactly one current decision brief. | Start here — accept the history view |
| Supporting | Current evidence needed to assess this decision. | Validation — tested behavior and remaining gaps |
| Supporting, when relevant | Design, expectations, independent findings, screenshots. | Screenshots — inspect scrolling and navigation |
| Diagnostic | Selected command logs or technical detail. | Diagnostics — failed backend validation |

Select the review bundle explicitly from current outputs. Do not pass the entire
accumulated working-document map to every review. Files retained in job history
remain available; important supporting files should be directly accessible without
an archive or a scavenger hunt. Historical negotiations and superseded drafts are
not default review attachments. Preserve identity checks and evidence links.

For visual changes, require current screenshots or comparable visual evidence
where feasible. If unavailable, say what was not assessed and why before asking
for acceptance. A renderer that ignores metadata must still present an
understandable brief with usable relative links. Test actual Cortex rendering;
if it fails to honor the existing overview/order/roles, report that separately to
Cortex rather than adding recipe-specific UI fields.

### Example: outcome acceptance

Illustrative content, not a claim about the audited implementation:

> **Title:** Review the job-history view
>
> **Decision:** Accept this candidate and merge it into `main`?
>
> **Summary:** The history view now shows the question, submitted answer, and
> timing. Wide documents scroll horizontally. Your previous scrolling feedback
> has been addressed.
>
> **Evidence and limitations:** UI checks passed; screenshots show narrow and
> wide layouts. Live backend integration was not run because the test environment
> was unavailable. That behavior remains unverified.
>
> **Recommendation:** Request the missing integration evidence before merging.
>
> **Read more:** Screenshots — inspect the visible behavior. Test results — see
> exactly what ran and what did not. Implementation — detailed changes.

If the missing check is mandatory, the recipe must obtain it before offering an
acceptance action; this example is an acceptance form only where policy permits
that limitation. The summary cannot authorize bypassing verification.

Use a short decision field: **“Merge these changes?”** Offer **Merge these
changes**, **Request changes**, and **Cancel**. For an unchanged outcome, use
**Accept this outcome** instead of merge. Feedback is optional for acceptance and
required for changes unless an annotation supplies the direction. Do not make the
user choose an implementation phase or approve “file accounting.”

### The recipe routes requested changes

Replace separate human choices for implementation revision and redesign with one
**Request changes** action. Pass the exact feedback and annotated files to the
existing working Codex node. Ask it to determine whether the request can be met
within the recorded scope and expectations or requires revisiting them. Route its
ordinary next output to implementation or design, retaining verification and
independent assessment. This is an internal decision, not another approval form.

A bug fix or presentation adjustment within the agreed behavior usually returns
to implementation. A different product outcome, interface contract, or expectation
requires design revision and any applicable deprecation process. An unclear request
gets one specific question only after the agent has considered existing context.
Routine classification does not need a new Jev node; test Jev only if Codex routing
proves unreliable. Old captured reviews with `redesign` answers keep their original
meaning, while newly generated forms offer the simpler choices.

### Example: a genuine capability decision

> **Title:** Approve Docker access for integration tests
>
> **Decision:** Allow this job to run the integration tests with Docker access?
>
> **Summary:** The tests require a disposable database container. Current task
> permissions do not allow Docker; changing the implementation would not resolve
> this blocker.
>
> **Impact:** This grants the specified runner access for this job. It does not
> change the cell's persistent configuration.
>
> **Recommendation:** Approve if that access fits your execution policy.
>
> **After your answer:** Approval requests the capability, validates it, and
> resumes testing. Denial leaves the required validation incomplete.

The actual brief must name the real requested access, duration, policy boundary,
and responsible provider; never imply job-scoped access when the mechanism edits
persistent `.c2/config`. If policy already permits the capability, route it without
a human question. Ask the authorized approver, not an arbitrary product reviewer.

## 5. Package requests: a defined first version

Implement **additive cell tooling requests** first, using existing portable
package references and `.c2/config.yaml`'s `packages` field. This directly addresses
the missing-Go jobs. It is not a general environment-management redesign.
Docker access, memory, credentials, images, and temporary requirement scopes remain
separate follow-ups. Project libraries still use the project's dependency manifest;
`uv`/`pnpm` tool packages are not a substitute for Python/Node application dependencies.

### Request and scope

Add one optional `packages` array of package-reference strings to the existing
agent response. Keep the reason in `summary` and detailed evidence in normal files.
Use the existing `blocked` outcome to request fulfillment; a package-bearing
blocker enters package handling before generic intervention. The remaining
current response fields are unchanged. Illustrative response excerpt:

```yaml
next: blocked
summary: Go is missing; the backend regression checks cannot start. Add the approved Go toolchain and resume these checks.
packages:
  - nix:github:NixOS/nixpkgs/<pinned-revision>#go
```

The placeholder must be replaced with a real approved reference. Agents discover
existing tools and config with `c2j self` before requesting additions. They return
the request and preserve completed work; they do not edit the active config or
install the requested tool speculatively. Duplicate existing declarations are a
no-op; an existing package that failed preparation is a runtime problem rather
than a request to add it again.

V1 scope is deliberate: adopting a package updates the current job's managed
workspace and makes it a proposed default for future work in this cell. Future
jobs receive it only after normal merge. The request survives new agent sessions
through recorded recipe outputs and then the actual config, not session memory.
For a one-off experiment, prefer an already permitted bounded validation job with
its own package declaration rather than adding a cell-wide default.

### Authorization without a review for every package

Use a small trusted policy supplied by the recipe deployment/operator: exact
approved package references and permitted validation probes. Reuse an existing
policy mechanism if available; do not create a policy service. The agent cannot
expand this list through its own proposed config. Exact approved additions proceed
automatically. Other additions need one review of the package set, reason, config
diff, persistence, and intended validation. Group related additions in one request.
Explicitly denied requests return a reason and permitted alternatives to Codex.

No policy match means approval is needed, not that arbitrary packages from a whole
registry are trusted. Pin versions/revisions where supported. V1 allows additions
only: package replacement/removal, permission changes, and unrelated config edits
use the existing design/change process. Approval of a tool does not approve Docker
access, credentials, or arbitrary code execution beyond the existing task scope.

### Fulfillment using existing workspace behavior

The inspected c2j checkout (`d6553a2`, `EXECUTION_TOOLS.md`) already reads repository
packages before each task and observes config edits on the next task. It records
setup diagnostics. Its package lists in `execution_needs` are literal. Use those
existing behaviors rather than assume dynamic package-list interpolation or invent
a new suspension API for this first version.

1. **Prepare without activating.** Build an additive candidate config from the
   current workspace config, preserving other settings. Retain its exact bytes and
   the pre-adoption workspace identity as normal artifacts/runtime references.
   Static parsing and policy evaluation do not install anything.
2. **Authorize.** Apply the trusted allowlist or collect the specific approval
   above. Bind authorization to this proposal; a changed proposal is reevaluated.
3. **Validate in a child.** Add a small recipe-owned `package-check.yaml` with two
   operations. Starting from the current workspace snapshot, the first copies the
   approved config artifact into the child's `.c2/config.yaml`; the next executes
   the approved bounded tool probes. c2j prepares packages before that second
   operation. The child never merges or publishes repository changes. Keep the
   parent's active config untouched throughout validation.
4. **Observe the result.** Consume native child outputs and setup/error artifacts.
   Reaching the probe proves preparation completed, but a tool's version check
   does not establish that application tests pass. Record actual probe results and
   package/config identity. Setup failure or an unsatisfied executor requirement
   is a failed/pending validation, not success. Preserve one request while waiting;
   do not spawn replacement probes on every turn.
5. **Adopt and continue.** On success, copy the exact validated config into the
   parent workspace in a normal operation and resume the unfinished assignment.
   Check that the parent config still matches the proposal's base; if changed,
   rebuild and reevaluate rather than overwrite concurrent edits. The next task
   loads the packages normally. Codex reruns the originally blocked checks and
   includes the config change in the ordinary outcome review.

The validation recipe is recipe-owned and pinned by the submission, not supplied
as executable recipe content by the requesting agent. Probes come from trusted
policy or are explicitly included in the approval. Launch through the coordinator
using native child operations and the exact current workspace state; no agent
needs broader general submission rights to request a package. Verify snapshot
selection and failure propagation in a focused native fixture before wiring the
parent flow. A plain echo alone is insufficient to establish the requested tool
works.

### Failures and recovery

A failed validation leaves the parent config and prior work intact. Return setup
errors under `error/` for the agent to choose another permitted package or report
the executor problem. A declined request resumes with that decision and available
alternatives; it does not repeatedly ask the same approval. Required validation
cannot silently become optional because a package was declined.

Even a validated config can encounter a later provider outage. Preserve the
validated candidate and earlier working snapshot; do not loop through Codex when
package preparation prevents Codex from starting. Restoration, if needed, must
select the pre-adoption workspace before package preparation and preserve all
pre-adoption code changes. Verify that runtime path in the fixture. If unsupported,
report the runtime-owner intervention explicitly; do not claim an agent can repair
an environment it cannot start in. Never use a Git reset to discard user work.

V1 acceptance cases: allowlisted addition with no human prompt; an unlisted
addition approved or declined once; no installation before authorization; child
preparation/probe failure with unchanged parent config; adoption after success;
changed base config; resumed session seeing the tool; no duplicate child on replay;
and real blocked checks rerun before the job can claim completion. Mocked package
setup is insufficient for the central install/adopt behavior: run a small actual
package fixture on a worker with the required package manager.

### Other capability and runtime issues

Use the existing requirements/suspension mechanism for approved memory or Docker
needs once its recipe interface is confirmed, as discussed in the
[requirements brainstorm](BRAINSTORM_ADAPTIVE_ENVIRONMENT_REQUIREMENTS.md). It is
not a prerequisite for the package-only increment above. Missing runtime routes
and credential failures remain execution-owner issues, not package requests.

Do not add a merge-credential preflight. If merge encounters a credential failure,
report it to the runtime owner and retain the accepted candidate and decision for
recovery. Reuse acceptance when content, verification, and approval conditions
remain valid. Do not turn that runtime failure into redesign or ask the user to
accept unchanged work again.

## 6. Concrete implementation sequence

Implement in small changes, with test statements written first and native recipe
tests for each behavioral change. Validate coherent changes together and observe the resulting behavior.
Job-context instructions are the first completed prompt-only change.

| Step | Concrete edits | Acceptance evidence |
| --- | --- | --- |
| 1. Review clarity and feedback routing | Update `prompts.yaml`; add overview selection and one-primary policy in `review.yaml`; select current attachments; offer one change-request action and let the existing Codex node choose implementation/design in `develop.yaml`. | Specific titles, self-contained brief, relevant evidence, no user phase selection; old feedback remains usable. Inspect forms in Cortex. |
| 2. Correct continuations | Fix existing-job refresh/wait ordering in `coordinate.yaml` and `develop.yaml`; exclude waits from work attempts; preserve human feedback. | Repeated submit launches once and waits without an attempt-limit form; unrelated real questions still reach the human. |
| 3. Fix handoffs and baseline repair | Produce an accepted execution brief in `consultation.yaml`; consume it in `coordinate.yaml`/`prompts.yaml`; replace filename-based baseline rejection in `develop.yaml` with identity/content checking. | Coherent child instructions; unchanged expectations and document corrections do not restart design; actual expectation changes remain gated. |
| 4. Package requests v1 | Add optional `packages` to `agent.yaml`; route package blockers through policy and a small `package-check.yaml`; validate, adopt, and resume using native outputs and workspace config. | The package cases above pass, including real setup, failure isolation, approval ordering, persistence, and replay. No general environment rewrite. |
| 5. Coordination contract and work intent | Update `agent.yaml` and `consultation.yaml` together for downstream requests; remove agent-maintained keys/`plan_keys` obligations in `develop.yaml`; reuse native submission/waiting and recipe-owned identity in `coordinate.yaml`; describe work intent in existing title/request. | Cortex → c2j → JobDB handoff needs no human scheduling; advisory agreements imply no implementation; replay and multiple requests to one cell remain correct. Replace the failing contract, not the execution engine. |
| 6. Reconcile child execution and recovery | Consume automatic outputs in `validation-jobs.yaml`; ask Codex for targeted reconciliation of failed/replacement children; preserve valid acceptance on runtime recovery. | A successful appropriate replacement resolves the obligation; unrelated failures stay blocking; credential recovery does not ask for repeated acceptance. |
| 7. Tune from new evidence | Re-audit recent jobs. Trial Jev for feedback/escalation classification if Codex needs help; assess remaining failures before proposing another redesign. | Measurable reduction in unnecessary prompts/turns without missed decisions, duplicate jobs, or a larger mandatory protocol. |

All recipe paths above are under `recipes/adaptive/`. Update its README and
`ADAPTIVE_BUILD_PROCESS.md` with the final behavior as each increment lands.

### Migration and validation boundaries

Keep old captured recipes understandable and resumable. Removing agent-authored `keys` is an
internal contract change for coordinated recipes and may affect custom wrappers.
Introduce the new request contract additively first, update shared producers and
consumers together, identify external consumers, and remove the deprecated form in
a separate release/ticket with the required deprecation plan. Do not rewrite live
job histories or run old jobs against silently incompatible state.

Use deterministic fixtures derived from the audit rather than contacting or
resubmitting production jobs. Native tests establish transitions, durable waits,
artifact binding, permissions, and approval behavior. Replay tests must cover
resumption after submission, distinct requests to the same cell, failed startup,
and a completed replacement. Test human forms for actual title, brief, question,
ordered evidence, and answer consequences, not merely that an input op occurred.

Mocked model tests do not establish that a prompt is understandable or that an
agent will reason well. Add a small sandboxed Codex exercise for the contradictory
handoff and nested consultation cases, and manually read the generated review
briefs in Cortex. Keep these checks bounded and separate from deterministic CI.

### Audit coverage

| Audited problem | Planned resolution |
| --- | --- |
| Missing downstream work in consultation | Shared requests and coordinator continuation, step 5. |
| Repeated submit / empty-key human intervention | Native status refresh and waiting, step 2; remove agent-maintained key obligations, step 5. |
| Phantom prerequisites / incoming-key confusion | Change the agent-facing coordination contract while retaining native execution, step 5. |
| Contradictory child instructions | Accepted execution brief, step 3. |
| Unchanged baseline forces redesign | Identity/content-aware correction, step 3. |
| Failed coordinator reused / failed attempts linger | Status refresh and explicit replacement, steps 2 and 6. |
| Runtime tools/routes/credentials become product questions | Package requests, step 4; runtime-owner recovery, step 6; broader capabilities remain follow-up. |
| Read-only task submits before being rejected | Retained task restrictions and coordinated handoff, step 5; runtime permissions checked before widening access. |
| Feedback repeated / missing screenshots / unclear document relevance | Current decision brief, evidence selection, exact feedback preservation, steps 1 and 2. |
| Oversized artifact inventory / title rejection | Preserve already implemented local fixes and their tests. |

Success means a person is asked for a real decision with a clear explanation,
while agents and the runtime handle the work and coordination they already have
authority to perform. Measure unnecessary interruptions, repeated unchanged turns,
duplicate submissions, and review comprehension on these same audit scenarios.

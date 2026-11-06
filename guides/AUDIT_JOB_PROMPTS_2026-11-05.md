# Job coordination and unnecessary human prompts

Read-only audit of `http://192.168.1.195:9047/c2`, captured on 2026-11-05 around
06:13–06:17 UTC. No jobs, answers, permissions, or remote repositories were changed.
The [follow-up audit](#follow-up-audit) below covers subsequent progress and the
locally implemented optional-title fix.

The [next-steps plan](PLAN_ADAPTIVE_COORDINATION_AND_REVIEWS.md) translates these
findings into concrete changes, with simpler agent coordination and clearer human
reviews. Its keyless request proposal refines the keyed handoff suggested below.

## Coverage

Queried the JobDB jobs endpoint without cell/status restrictions and with
`includeHidden: true`, covering active and archived jobs. It returned 21 jobs,
including eight omitted from the ordinary listing. Read all 714 returned chapters,
including the retained histories of hidden/deleted jobs. There were 17 recorded
form-generation events. Several histories inherit the same earlier prompts through
restarts; these are not 17 independent incidents. There was no next-page token.
Active jobs can have advanced since this snapshot. Physically purged data, if any,
is not recoverable through this listing.

## Main finding: agents describe work, but consultation cannot return it as work

For `a1756523-517b-40f4-aea0-f994ec1b2fd1` (Cortex):

- Chapter 16 returns a proper structured consultation to c2j under
  `review_input_story_v1`.
- Chapters 20–24 establish that c2j needs a downstream JobDB consultation.
  The agents prepare the request and explicitly describe a coordinator handoff.
- Chapter 24 returns `needs_review` while saying this is a coordination handoff,
  not a human approval request.
- Chapter 26 asks the human for “Consultation needs expert direction.”
- Chapter 28 records the human directing the agent to return a workflow-creation
  request.
- Chapters 30–33 produce more request documents, identify c2j ownership and the
  JobDB first step, and say no further semantic approval is needed.
- Chapter 35 generates the same kind of human prompt again. Chapter 36 is waiting
  for its answer in this snapshot.

The agents are returning the intended work **in prose and files**. The consultation
response schema only allows `outcome`, `thinking`, `files`, and `assessment`.
There is no structured list of downstream consultations or prerequisite work for
the coordinator to consume. `needs_review` is mapped directly to a human form;
there is no automatic handoff branch. Human direction is fed into another round
of the same conversation rather than routed as work.

Code: [consultation response schema](../recipes/adaptive/consultation.yaml),
`turn` / `exchange` / `schema`; `report` and `request_consultation_direction` states.
The top-level build agent already has structured `consultations` and `keys`, but
that contract is absent from consultation turns.

**Recommended correction:** give consultation a structured coordination outcome
and a list of requests using the existing cell/key/ref/request/role contract.
Return that to the parent coordinator, which routes the requested owner consultation
and resumes the original conversation with its result. Reserve human direction
for a specific unresolved decision. Distinguish agreement on scope from completion
of the resulting prerequisite; don't require implemented dependency evidence just
to agree that work should be commissioned. Keep serving-owner agreement and actual
submission permissions intact. Do not interpret a Markdown filename as executable
workflow instructions.

## Other recurring patterns

### 1. Running prerequisites become human blockers or repeated no-op submissions

Job `3Lft1kkjaAm8EEBGXhu0KS2kVhl` successfully returns structured work:

- Chapter 29: `next: submit`, `keys: [c2j_resolution_restart]`.
- Chapter 32: continues independent work while the prerequisite runs.
- Chapter 33: `blocked` with empty keys, though its summary names the running
  prerequisite. Chapter 34 asks the human to supply its result.
- Human direction at chapter 36 asks the agent to return a job request.
- Chapters 38–43 repeatedly return `submit` for the same key. Chapter 44 asks for
  direction after bounded attempts.

There are two independent recipe problems:

1. In `develop.record`, `blocked` with empty keys enters human intervention
   **before** the later branch that waits for known running dependencies.
2. In `coordinate.pick`, `submit` for an existing job goes to `skip` before the
   running-job wait branch. Deduplication prevents duplicate jobs, but this path
   neither waits nor refreshes the recorded outcome. Each trip back to the agent
   consumes another work attempt.

The submitted c2j job `Aexe3DV6IC4oHXTLGr8Ocm4U36g` is actually failed in this
snapshot, while the parent conversation still describes its cached state as
running. Its child `3LfwF9bruXEprqjwTVmB5I6XpIZ` failed schema validation.

**Recommended correction:** consult native job state before escalating a dependency
blocker. Repeated submission of an existing key should reuse its identity and
refresh/wait for its result. Waiting must not consume agent-attempt budget. A real
failed child should return its identity, failure, and evidence for targeted
reconciliation, not a generic missing-capability question. Empty keys alone are
not evidence that a human is the responsible actor.

Code: [coordinator](../recipes/adaptive/coordinate.yaml), `pick`;
[development loop](../recipes/adaptive/develop.yaml), `record` transition ordering.

### 2. Consultation keys become phantom implementation obligations

In `32c627c5-8b8d-4de8-94d0-bf77a5bd4460`, the agent consults c2j, follows its
redirect to recipes, and receives the verification contract. Design and test-plan
responses include `verify_workflow_contract` in `keys`. No implementation child
was requested. After implementation, the controller reports that required child
work has not succeeded. The agent checks, finds no child jobs, returns empty keys,
and is still bounced into repair. Chapter 34 asks the human to reconcile the
missing record.

`record.plan_keys` unions earlier keys with later responses, so empty keys cannot
remove a mistakenly retained obligation. The implementation completion gate
requires every plan key to have a successful child job. The schema does not
explicitly distinguish consultation-only agreements from agreements requiring
implementation.

**Recommended correction:** record whether an agreement requires external work,
plus the actual required work keys. Do not turn all consulted/accepted keys into
child-job requirements. Reconcile the work plan against the agreement before
implementation. If required work has not been launched, route it to the coordinator
rather than asking the agent to repair a completion report. Explain which key is
missing and why; “Required child work has not succeeded” hides the actionable cause.

### 3. Runtime discovery and authority failures go to the product reviewer

The Gitvend lineage `6f4aa8aa…` → `3LfpdJcr…` → `3Lft2gSc…` carries a prompt asking
the human to configure JobDB/managed validation. The answer is simply the JobDB
URL already used to run these jobs. `8337b154…` similarly asks for controller-record
access; the human suggests exercising the verification path instead.

Hidden jobs `54b46e81…`, `3LfhRsw…`, and `817facda…` report verifier clone failures
because credential/secret resolution was unavailable. These are genuine runtime
failure reports, not evidence that application code needs human interpretation.
The human in `817facda…` explains that automatic verification already exists and
that a bounded workspace-derived test job can be submitted.

The implementation prompt explicitly tells agents to return empty-key `blocked`
for missing tools, permissions, or environments. The recipe routes that outcome to
a generic human intervention form. This collapses discoverable context, existing
workflow capabilities, runtime faults, and actual approval requirements into one
question type.

**Recommended correction:** provide/discover the current runtime route and expected
verification lifecycle; attempt authorized existing recipe paths first. Route
verified infrastructure failures to the responsible owner with diagnostics. Ask a
human only when an actual approval or unavailable external action is required.
A URL alone is not authorization, and genuine secret-access failures must not be
worked around by exposing credentials. This audit did not independently verify
whether each historical worker had the expected broker/discovery configuration.

### 4. Human direction is treated as requiring another requirement decision

In `811e64e3-13ab-47c1-8965-311d97fad53a`, chapter 44 requests before/after screenshots
and confirmation that horizontal scrolling still works. The assessment at chapter
56 identifies that scrolling was removed, then asks for an “authoritative requirement
decision.” Chapter 59 repeats the requirement: horizontal scrolling is required.

The formal-plan rules preserve earlier expectations but make it easy to treat later
explicit feedback as an unresolved conflict rather than authorized direction.

**Recommended correction:** use explicit human feedback to enter redesign/test-plan
revision automatically, preserving superseded expectations and the required
migration explanation. Ask again only if the feedback leaves a genuine choice
unresolved. The audit cannot infer a universal rule that every apparent conflict
is already settled; this example contains specific direction to preserve behavior.

### 5. Outcome reviews lack the evidence a human needs

`e7dbfe06-c753-4e23-b66e-55dd4496097f` reaches outcome review, then the user asks for
screenshots. The scrolling job also requires a second request for device/tree-size
coverage. The outcome approval itself is intentional, but the evidence package is
not sufficient for evaluating a visible UI change.

**Recommended correction:** the test plan for visual changes should specify
representative screenshots or equivalent visible evidence up front, including
relevant viewport and content extremes. Return that evidence with the first
outcome review. Do not remove outcome approval to hide an incomplete evidence set.

### 6. Read-only job submission is detected after the side effect

In `Aexe3DV6IC4oHXTLGr8Ocm4U36g`, c2j correctly consults JobDB about a runtime defect
and receives an agreement. On a resumed **read-only** task the agent directly
submits the JobDB build, instead of returning a coordinator request. The recipe
then fails the parent for submitting from a prohibited phase. The child itself
fails because it supplied `title`, which the selected build input schema rejects.
A hidden earlier validation child `3LfnyjcDhT4dPOyulwGrZQ1uqDJ` similarly supplied an
unsupported `prompt` field to its recipe.

**Recommended correction:** explicitly deny job submission in read-only tasks,
and make the structured handoff available there. The coordinator should submit
against the actual recipe input contract. `const: true` protects Git state; it is
not a substitute for a submission permission boundary. The audit identifies the
recorded side effect and rejection; it did not inspect the live server's policy
configuration.

The `title` rejection is also a missing build capability, not merely a caller
mistake: titles are useful request context. Optional title support is implemented
in the follow-up below. Unsupported fields on other recipes still require checking
those recipes' contracts.

## Artifact fix completed separately

The oversized review inventory in `3Lft2gSc…` is addressed locally by separating
selected documents from the complete artifact inventory. See
[implementation and tests](FIX_REVIEW_ARTIFACT_SELECTION.md). It does not repair
the coordination/routing problems above. No coordination change was silently
included in this audit.

## Proposed order

1. Add structured downstream work handoff to consultations; cover the exact
   Cortex → c2j → JobDB sequence without a human prompt.
2. Wait/refresh existing prerequisite jobs and prioritize known dependencies
   before empty-key intervention. Test repeated submit and failed-child refresh.
3. Separate consultation-only agreements from required implementation work; test
   that explicit contract clarification does not create a phantom child obligation.
4. Enforce read-only submission permissions before effects and validate launch
   inputs. Return actionable child failures rather than generic response repair.
5. Separate runtime-owner intervention from product questions; reuse explicit
   user direction and collect visible review evidence before asking for approval.

Human checkpoints should remain for outcome acceptance, real ambiguity,
authority increases that require approval, and genuinely unavailable external
actions—not routine scheduling, state refresh, schema repair, or handing a known
request to its owning cell.

## Complete job inventory

Chapter counts and status are the audit snapshot, not a claim about later progress.

| Job | Cell | Hidden | Status | Chapters | Recorded forms | Finding |
| --- | --- | --- | --- | ---: | ---: | --- |
| `3LfwF9bruXEprqjwTVmB5I6XpIZ` | jobdb | no | COMPLETED | 8 | 0 | Child rejected unsupported title input. |
| `3LfuSA5YSUxSVGOQgLsetFRFaS9` | gitvend | no | COMPLETED | 7 | 0 | Successful managed validation child; no human form. |
| `Aexe3DV6IC4oHXTLGr8Ocm4U36g` | c2j | no | COMPLETED | 26 | 0 | Read-only task submitted child; parent rejected effect. |
| `32c627c5-8b8d-4de8-94d0-bf77a5bd4460` | cortex | no | CANCELLED | 36 | 1 | Phantom prerequisite obligation; generic blocker prompt. |
| `a1756523-517b-40f4-aea0-f994ec1b2fd1` | cortex | no | READY | 37 | 2 | Downstream consultation handoff repeatedly becomes human direction. |
| `3Lft2gScFyph0OzbvTooal1tMmv` | gitvend | no | COMPLETED | 61 | 1 | Inherited runtime-context prompt; later oversized review inventory. |
| `3Lft1kkjaAm8EEBGXhu0KS2kVhl` | cortex | no | READY | 46 | 2 | Running prerequisite, repeated submit no-op, attempt-limit prompt. |
| `8337b154-a69d-4fbb-8d94-fec48f8bea12` | gitvend | no | ACTIVE | 88 | 2 | Runtime evidence blocker; legitimate outcome revision requests task-based checks. |
| `dc736ae6-6e3a-406d-aa4b-76843bab40d7` | cortex | no | COMPLETED | 21 | 0 | Root cell unavailable; creation routing failed before a human form. |
| `e7dbfe06-c753-4e23-b66e-55dd4496097f` | cortex | no | ACTIVE | 60 | 2 | Outcome review revised to request missing screenshots. |
| `811e64e3-13ab-47c1-8965-311d97fad53a` | cortex | no | ACTIVE | 65 | 2 | Outcome evidence request followed by repeated scrolling requirement decision. |
| `3LfpdJcrPi0541AQ2z938222370` | gitvend | no | COMPLETED | 46 | 1 | Inherited runtime-context prompt; root cell unavailable. |
| `1fa7464c-774d-4061-8da1-04d77f91d637` | cortex | yes | COMPLETED | 15 | 0 | Classifier stdout truncation; no human form. |
| `3LfoYF0fjKhLyMPbGOo8DmX4Ak2` | gitvend | yes | COMPLETED | 7 | 0 | Successful validation child; no human form. |
| `3LfnyjcDhT4dPOyulwGrZQ1uqDJ` | gitvend | yes | COMPLETED | 6 | 0 | Validation child rejected unsupported prompt input. |
| `6f4aa8aa-61ae-4a15-bc3e-d786de17d3ff` | gitvend | no | COMPLETED | 44 | 1 | Runtime-context prompt; root cell unavailable. |
| `54b46e81-b7fd-41fb-a444-b9f030fb77a1` | gitvend | yes | CANCELLED | 32 | 1 | Deleted job retains history: verification credential blocker. |
| `3LfiiiUCmLEQKFgzYgcagQXi7Ev` | gitvend | yes | CANCELLED | 31 | 0 | Cancelled before a recorded human form; verification lineage. |
| `3LfhRswJgaa4KQQFel76nuBqn6m` | gitvend | yes | CANCELLED | 34 | 1 | Verification credential blocker; cancelled. |
| `817facda-6a08-4756-ba2b-7e2e141b17a8` | gitvend | yes | CANCELLED | 34 | 1 | Credential blocker; human explains automatic/workspace validation. |
| `6111daac-1a8c-43eb-b3a2-6aebd518967e` | gitvend | yes | COMPLETED | 10 | 0 | Repository used as cell name; no human form. |

## Follow-up audit

Captured later on 2026-11-05, reviewed through approximately 19:00 UTC, against the
same JobDB. The unrestricted listing, including hidden jobs, returned **27 jobs,
eight hidden**, with no next-page token. Read all **923 chapters**, an increase of
209. Six jobs are new and five existing jobs have additional history. The other
16 jobs have unchanged chapter counts; their earlier findings remain applicable.
These are snapshots, including terminal jobs whose recorded outcome is failure;
`COMPLETED` alone does not mean success. No remote state was changed.

### Optional title support: implemented locally

Two new c2j child jobs, `3LhBEkefJps2Ltln4fesyzyaQpZ` and
`3LhBQXhsut7oXPZnlPW77sOfv12`, fail before work starts because the public build
schema rejects `title`. The titles are useful labels such as
`review_input_story_v1: coordinate JobDB history contract` and
`c2j_resolution_restart`. This repeats the earlier JobDB child failure.

[build.yaml](../build.yaml) now accepts an optional string `title`, defaulting to
empty, forwards it to the adaptive build, and retains it in the build output.
When present, the adaptive request starts with `Title: <title>`, a blank line, and
the original prompt. Classification and working agents receive that context.
The required `prompt` remains the detailed request; omitting `title` preserves
existing request text. This does not change JobDB display metadata.

Both full-flow cases `direct-no-change` and `design-single-review` passed in the
native c2j test runner, using the local execution adapter and mocked model/hook
responses. Assertions cover acceptance and preservation of a title containing
Unicode and percent signs, its inclusion in classifier and agent inputs, and
unchanged untitled behavior. Test statements are in
[title-statements.md](../recipe-tests/adaptive/title-statements.md); assertions are
in [flow.test.yaml](../recipe-tests/adaptive/flow.test.yaml). Historical jobs still
contain their captured recipes; none were restarted by this change.

### Execution handoffs carry contradictory consultation instructions

The new c2j, JobDB, and pgjobdb implementation jobs all begin with the prerequisite
execution prompt: consultation is complete, this is a fresh execution session,
and the agent should implement the agreed work. The same prompt then appends the
original consultation request verbatim. In these jobs that request says **“Do not
implement or submit jobs.”** The c2j variant also prohibits repeating backend
consultations.

This comes from `children.prerequisite` in
[prompts.yaml](../recipes/adaptive/prompts.yaml), which embeds `inputs.request`
after “Original consultation request.” In `OqTDQnNop6ZHU38thtkvGhDbtKV`, chapter
16 explicitly cites the no-implementation phase constraint among its blockers;
chapter 19 asks the human to resolve a build blocker. This contradiction exists
in the new task text, independently of session inheritance.

**Proposed correction:** submit an execution brief derived from the accepted
agreement, with the owning cell, requested work, acceptance expectations, and
remaining dependencies. Preserve original consultation material as labeled
historical evidence. Explicitly supersede consultation-only phase restrictions
while retaining actual scope and authority limits. Do not indiscriminately strip
prohibitions from requests.

### Incoming assignment keys are mistaken for new prerequisites

`ZTj36Ivv1iPuewgp9qdYHtGNPuL` and `Ox7iAaAi5bZ72vrBC7HLWconMMA` return their
incoming agreement keys in chapter 16. Those keys are not locally requested
serving agreements. Chapter 17 changes the response to redesign with empty keys,
although the underlying technical plan is unchanged. `3LhBYCtYRK43K9OVJTnRcHHrOK8`
shows the same incoming-key correction around chapters 16–17.

**Proposed correction:** distinguish the parent assignment/agreement identity
from this job's outbound prerequisites. Repair invalid response bookkeeping in
place; reserve redesign for a real plan change. Include an explicit explanation
of these two roles in child context and output-field instructions.

### Returning an unchanged baseline triggers redesign

In pgjobdb job `Ox7iAaAi5bZ72vrBC7HLWconMMA`, chapter 22 returns a blocker and
lists `test-statements.md` as “Formal expectations preserved unchanged.” Chapter
23 changes to redesign and describes that file as preserved byte-for-byte;
chapter 24 removes it from the returned file list. Chapters 27–28 repeat design
and test planning with the same 27 expectations. Chapter 29 reaches the same
blocker, followed by the human form at chapter 30.

The `record.vars.issues` expression in
[develop.yaml](../recipes/adaptive/develop.yaml) flags **any** implementation
response listing `test-statements.md`. It does not distinguish referencing or
republishing the unchanged baseline from editing expectations. The directory
entry `evidence` also needed correction to individual files, but that packaging
repair is independent of whether design should restart.

**Proposed correction:** preserve the baseline artifact identity and compare a
proposed replacement before treating it as a change. Referencing unchanged
expectations should be valid. Actual expectation changes must still follow the
existing redesign/deprecation rules; correcting document references should not
consume a design cycle.

### Missing tools and runtime routes become product-facing blocker forms

JobDB job `ZTj36Ivv1iPuewgp9qdYHtGNPuL` reports two validation commands exiting
127 because Go is unavailable, alongside a missing JobDB runtime URL and pending
pgjobdb evidence. The pgjobdb job reports the same missing tool and runtime-route
conditions. These are agent-reported execution findings, not independently
reproduced worker-environment probes. Both jobs reach generic human blocker forms;
the pgjobdb redesign cycle does not resolve its environment.

**Proposed correction:** route declared tool needs through task requirements and
policy-controlled provisioning/suspension; obtain runtime routes from the execution
context and refresh known dependencies through the coordinator. Ask a human when
policy or a genuinely unavailable external action requires one, with the specific
owner/action identified. Do not ask the product reviewer to revise a sound plan
because an executor lacks its toolchain. See the existing
[environment requirements brainstorm](BRAINSTORM_ADAPTIVE_ENVIRONMENT_REQUIREMENTS.md).

### Failed coordinator references outlive submission

In `a1756523-517b-40f4-aea0-f994ec1b2fd1`, chapter 39 reports submitting and
observing coordinator job `3LhBEkefJps2Ltln4fesyzyaQpZ` as active. That job then
fails input validation on `title`. Nevertheless, the later child requests still
instruct their agents to reuse it as an existing coordinator.

The parent subsequently obtains agreements from JobDB, pgjobdb, and c2j, returns
three work keys in chapters 69–71, and launches all three corresponding jobs.
Thus the newer history **does contain the work list and owning cells, and the
recipe does launch them**. The remaining problems include the contradictory
execution briefs and scheduling: chapter 78 observes running jobs, chapter 80
requests the same jobs again, and chapter 81 generates the attempt-limit form.
This confirms the earlier repeated-submit/wait issue with additional evidence.

**Proposed correction:** refresh referenced job status before reuse. Submission
acceptance is not successful startup or completion. Reconcile failed/replaced
coordination jobs explicitly, then wait for existing running prerequisites without
counting a repeated request as another implementation attempt.

A related prospective issue appears in `3Lft1kkjaAm8EEBGXhu0KS2kVhl`: chapter 48
records both title-rejected attempt `3LhBQXhsut7oXPZnlPW77sOfv12` and corrected
child `3LhBYCtYRK43K9OVJTnRcHHrOK8`. Automatic child-job outputs retain both. The
parent currently waits in `PENDING_JOBS`. Because
[validation helper (now validation-goals.yaml)](../recipes/adaptive/validation-goals.yaml) aggregates failures
across children, a superseded failed attempt may still fail validation after the
replacement finishes. This is a code-based risk, **not an observed final outcome**.
Reconciliation should identify the replacement while retaining the failed attempt
as history, rather than silently ignoring arbitrary failed children.

### Human acceptance is followed by a merge credential failure

Three older jobs now fail at `merge_reviewed_candidate` after a human accepts the
outcome: gitvend `8337b154-a69d-4fbb-8d94-fec48f8bea12`, and Cortex
`e7dbfe06-c753-4e23-b66e-55dd4496097f` and
`811e64e3-13ab-47c1-8965-311d97fad53a`. All report a failed workspace clone with
`Error: secret resolution unavailable`; the c2j Git credential helper quits.

This is an execution/credential-path failure, not evidence that the user rejected
the result or that implementation needs redesign. Credential availability belongs
to c2j and its execution provider. The recipe should preserve the reviewed
candidate and approval across runtime restoration, without adding a credential
preflight before review. Changed candidate
content or other material approval conditions must still trigger appropriate
review. This audit did not inspect or change secrets or diagnose the provider's
underlying configuration.

### Changed-job inventory

All eleven jobs below are visible. The eight hidden jobs remain included in the
27-job coverage and have no additional chapters relative to the initial snapshot.

| Job | Cell | Chapters: initial → follow-up | Follow-up status | Finding |
| --- | --- | --- | --- | --- |
| `3LhBEkefJps2Ltln4fesyzyaQpZ` | c2j | new → 8 | COMPLETED, failed_app | Coordinator rejected title; later requests still refer to it. |
| `3LhBQXhsut7oXPZnlPW77sOfv12` | c2j | new → 8 | COMPLETED, failed_app | Title-rejected attempt retained alongside replacement. |
| `3LhBYCtYRK43K9OVJTnRcHHrOK8` | c2j | new → 25 | READY | Incoming key correction; blocked validation and runtime routing. |
| `OqTDQnNop6ZHU38thtkvGhDbtKV` | c2j | new → 21 | READY | Execution prompt also prohibits implementation. |
| `ZTj36Ivv1iPuewgp9qdYHtGNPuL` | jobdb | new → 25 | READY | Incoming key correction, missing Go/runtime route, dependency evidence. |
| `Ox7iAaAi5bZ72vrBC7HLWconMMA` | pgjobdb | new → 32 | READY | Incoming key and unchanged-baseline redesigns; same environment blocker. |
| `a1756523-517b-40f4-aea0-f994ec1b2fd1` | cortex | 37 → 83 | READY | Three children launched; repeated submit reaches attempt-limit form. |
| `3Lft1kkjaAm8EEBGXhu0KS2kVhl` | cortex | 46 → 54 | PENDING_JOBS | Failed submission and corrected child both recorded. |
| `8337b154-a69d-4fbb-8d94-fec48f8bea12` | gitvend | 88 → 98 | COMPLETED, failed_app | Accepted outcome; merge clone cannot resolve Git credentials. |
| `e7dbfe06-c753-4e23-b66e-55dd4496097f` | cortex | 60 → 66 | COMPLETED, failed_app | Accepted outcome; same merge credential failure. |
| `811e64e3-13ab-47c1-8965-311d97fad53a` | cortex | 65 → 85 | COMPLETED, failed_app | Scrolling change accepted; same merge credential failure. |

### Follow-up priorities and implementation boundary

Optional title support is implemented and tested locally. Artifact selection is
also implemented as described above. The remaining findings are proposals, not
claimed fixes. Prioritize coherent execution handoffs and existing-job waiting,
then distinguish incoming assignments from outbound prerequisites and repair
unchanged-document responses without redesign. Runtime requirement/route handling
and merge credential availability need coordination with c2j/provider owners.

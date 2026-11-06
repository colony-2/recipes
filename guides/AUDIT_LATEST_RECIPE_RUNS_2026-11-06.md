# Latest recipe runs: failures, tuning, and missing recovery

Audited on 2026-11-06 against `http://192.168.1.195:9047/c2`.
Census captured from 18:31 UTC; final refresh before 18:46 UTC found no new
attempts or changed statuses, and confirmed the goal counts below.
Recipe revision: `538ff7cf6394b4fd6610d7dbd16d31a6c69c0301`.
This is an investigation and proposed work plan; no recipes or production runs were changed.

## Findings that determine the next work

The failures are real, but `stop_attempt` combines several different causes. We
deliberately fail that command when the recipe gives up. Renaming it or increasing
retries would leave the underlying problems intact.

The most important findings are:

1. **Recovery has no effective owner in these executions.** Thirteen failed
   attempts have OPEN goals with zero nonterminal candidates. Three parents are
   waiting for goals to finish. The recipe correctly waits for goal outcomes,
   but that does not arrange for anyone to repair a failed attempt.
2. **Our structured output schema is rejected before useful agent work.** All
   187 recorded model results use `schema_mode: prompt` and report one output
   repair attempt. A captured provider error identifies the untyped `order`
   property. This is a recipe/adapter contract defect, not evidence that the
   underlying agent needs more elaborate instructions.
3. **Consultation cannot reliably hand accepted prerequisite work back to an
   executor.** Advice recurses into more advice, and a recovery agreement can
   produce a different goal instead of continuing the existing one.
4. **The configuration rollout acquired excessive and inconsistent validation
   obligations.** Several cells passed configuration and tool checks but stopped
   on missing worker-image provenance. Other cells completed comparable changes
   while explicitly disclosing that limitation.
5. **There are concrete implementation defects to fix:** lost repair inbox
   evidence, an unpublished workspace SHA treated as an upstream ref, an invalid
   package probe, and invalid-ref errors hidden by subsequent allowance failures.
6. **The private Git problem is a distinct routing failure.** Normal private Go
   dependency fetches reach a gateway URL that returns `unsupported Git route`.
   That needs a gitvend/Git-profile fix or configuration correction; prompt tuning
   cannot make the route work.

I recommend targeted recipe fixes plus an explicit goal-recovery mechanism. The
sample does not justify replacing the whole adaptive workflow again.

## Scope and counts

The census included 81 retained attempts across ACTIVE and ARCHIVED storage with
`includeHidden: true`; the ordinary visible query returned 31. The current-recipe
sample is the 24 attempts created after the latest recipe commit at
2026-11-06 03:16:19 UTC. I inspected their 1,027 chapters, goal records, and selected
command logs, agent outputs, agreements, and validation documents.

Every sampled root-source record resolves to `538ff7cf`: 22 use `build.yaml`, and
two use `recipes/adaptive/package-check.yaml`. This verifies the captured source,
rather than assuming a submission used whatever `main` contains now.

| Recorded outcome | Attempts | Meaning |
| --- | ---: | --- |
| Failed application execution | 13 | Ten end through `stop_attempt`; three fail elsewhere |
| Successful | 7 | Six build outcomes and one package-validation outcome |
| Waiting for goals | 3 | Root rollout, pgjobdb package adoption, and c2j prerequisite delivery |
| Waiting for human input | 1 | The separate recipes audit/owner-investigation run |

That is 65% failure among the 20 terminal attempts, or 54% of the full sample.
These are correlated attempts: one rollout accounts for 15 rows, and one
cross-cell feature accounts for four. They are not 24 independent projects.

All 24 headers report c2j
`v0.0.120-0.20261106011904-eb636a529263+dirty`. The source commit is recorded, but
the dirty suffix does not identify the exact deployed executable. Recipe source
identity is much stronger than runtime build identity in this evidence.

This investigation fits the recipes cell's purpose. Runtime workspace restoration,
goal scheduling, Git transport, and tool preparation have external owners identified
below. Application implementation remains with its owning cell.

## Catalog

Goal IDs identify the outcomes to monitor. Attempt links open the captured
chapters; they are evidence coordinates. `cN` means chapter ordinal N.
All times below are creation times on November 6, UTC.

| Time | Cell | Goal | Attempt evidence | Outcome / immediate cause |
| --- | --- | --- | --- | --- |
| 03:23:15 | cortex | `3LiSSbpvlXm7Xh79RU3iY9k5KTQ` | [fe4a6d1b…](http://192.168.1.195:9047/v1/tenants/c2/jobs/fe4a6d1b-4389-4278-98f8-a61387602a9a/chapters?startOrdinal=0) | Succeeded; visual change validated and reviewed. |
| 03:24:04 | cortex | `3LiSYlhPFFfJA8n4rMupxjpiguH` | [8e71e9cb…](http://192.168.1.195:9047/v1/tenants/c2/jobs/8e71e9cb-7466-4226-ac86-9cea288b4090/chapters?startOrdinal=0) | Failed; private Go modules rejected by gateway (c44–48). |
| 03:24:16 | root | `3LiSaEG29BdS92LhNzaK9Rpgobh` | [ae23c91d…](http://192.168.1.195:9047/v1/tenants/c2/jobs/ae23c91d-0acc-45dc-8e58-889d6036ec3a/chapters?startOrdinal=0) | Waiting; twelve owner goals; missing worker identity also reported (c142–148). |
| 03:24:42 | cortex | `3LftOyquYC8gRetIh4KeTmKxDk4` | [3LiSdVig…](http://192.168.1.195:9047/v1/tenants/c2/jobs/3LiSdVigxW1urTFF2amWnSZVIHp/chapters?startOrdinal=0) | Failed; work allowance after prerequisite/recovery coordination (c59–62). |
| 03:25:27 | cortex | `3LiSj8ddycGtpqxiiQcPe4rDlXo` | [73fc96ba…](http://192.168.1.195:9047/v1/tenants/c2/jobs/73fc96ba-5936-4a1a-901a-5f047392b4e2/chapters?startOrdinal=0) | Succeeded; hidden from ordinary listing; reviewed candidate. |
| 03:42:48 | c2j | `3LiUpzjeHN55PE9EkBmA0ro35Ko` | [PAitP6Wz…](http://192.168.1.195:9047/v1/tenants/c2/jobs/PAitP6WzcK3e8QDuKK80eDX0JGt/chapters?startOrdinal=0) | Failed; implementation dispatch recurses through advisory tasks (c22–33). |
| 03:46:15 | cortex | `3LiVFzZQVYah5tl7XXv3aE9hfYX` | [b2851039…](http://192.168.1.195:9047/v1/tenants/c2/jobs/b2851039-cdad-4e35-b479-f3327b4e4495/chapters?startOrdinal=0) | Succeeded; reviewed 14-file candidate with validation and screenshots. |
| 04:11:18 | c2j | `3LiYIwU4iJf3XPcWp2RvLWkFFnz` | [4Y4rYZl3…](http://192.168.1.195:9047/v1/tenants/c2/jobs/4Y4rYZl36QmtEg6JONXNyuW3LOn/chapters?startOrdinal=0) | Succeeded; bounded configuration change and tool checks. |
| 04:11:21 | base | `3LiYJE8FimgCRFpLR17h0SYdGPq` | [AkRXogr6…](http://192.168.1.195:9047/v1/tenants/c2/jobs/AkRXogr6i6B1Eu3CmxcVxenq2BG/chapters?startOrdinal=0) | Failed; correction lacks original evidence; identity/worker checks also blocked (c18–23). |
| 04:11:24 | cortex | `3LiYJdFkUDWebJ5sFne2wBDV2jc` | [R7fjxwCg…](http://192.168.1.195:9047/v1/tenants/c2/jobs/R7fjxwCgtmhys0H62CUeQJedRer/chapters?startOrdinal=0) | Failed; unchanged config passes checks; Chromium sandbox launch fails as root (c18). |
| 04:11:28 | pulse | `3LiYK8AbfKSW4TuwOVltaD2jmt5` | [R6EZtMyl…](http://192.168.1.195:9047/v1/tenants/c2/jobs/R6EZtMylP2IX05ezXPAplSEztbo/chapters?startOrdinal=0) | Failed; loaders pass; effective identity and worker provenance remain unmet (c23). |
| 04:11:31 | jobdb | `3LiYKYMB3SxUctzAVB0KM8HG4YQ` | [JpIHRBqW…](http://192.168.1.195:9047/v1/tenants/c2/jobs/JpIHRBqWfDQ0GCvcZZzEkrwpGii/chapters?startOrdinal=0) | Succeeded; config migration; conditional operational checks disclosed as skipped. |
| 04:11:34 | pgjobdb | `3LiYKv6bUwMRVHDJ6m6raw4AEtw` | [Ujlj0dEa…](http://192.168.1.195:9047/v1/tenants/c2/jobs/Ujlj0dEaZhcqZ3RGeAyWga1Q0hJ/chapters?startOrdinal=0) | Waiting; approved package child failed but its goal remains OPEN (c25). |
| 04:11:37 | shai | `3LiYLIITT1hMRr8wLRzR3DEMbkT` | [0nnvY07G…](http://192.168.1.195:9047/v1/tenants/c2/jobs/0nnvY07GCXU19YtQfT7EviJYsbJ/chapters?startOrdinal=0) | Failed; consultation return fetches unpublished candidate from upstream (c27). |
| 04:11:40 | c2ops | `3LiYLfy6Xw90tYxDewy9Ag4v00u` | [C0Q7rQtn…](http://192.168.1.195:9047/v1/tenants/c2/jobs/C0Q7rQtnZYQnjotTmg95NLqC5QX/chapters?startOrdinal=0) | Failed; config/tool checks pass; immutable worker image identity unavailable (c26). |
| 04:11:43 | recipes | `3LiYM2cRQsj14JgBDSFjMnz4tju` | [0UQZP18b…](http://192.168.1.195:9047/v1/tenants/c2/jobs/0UQZP18bPPAw2bUZhAR4K6wpG6C/chapters?startOrdinal=0) | Failed; candidate pnpm package preparation refuses install scripts (c19). |
| 04:11:46 | gitvend | `3LiYMOPwg9BtKGBKjMs9VNeCV38` | [SlZJxbky…](http://192.168.1.195:9047/v1/tenants/c2/jobs/SlZJxbkygTVHMXCRB4paT5DZiOZ/chapters?startOrdinal=0) | Failed; reported build/tests pass; c2j source/identity and worker provenance unmet (c21). |
| 04:11:49 | cortex-assistant | `3LiYMmVL0IDxMDuOBQBU44b9BjS` | [4OgjGQMU…](http://192.168.1.195:9047/v1/tenants/c2/jobs/4OgjGQMUPjg02hMl7I80gsgdhl4/chapters?startOrdinal=0) | Failed; config/tool checks pass, including package child; required worker identity absent (c30). |
| 04:11:52 | pulse-tart | `3LiYND2oYodWDlH8rPvRRPfAZxT` | [J6tgp9FI…](http://192.168.1.195:9047/v1/tenants/c2/jobs/J6tgp9FIsLGf3g0QgXTIh3J170D/chapters?startOrdinal=0) | Succeeded; config and tool checks; live integration/provenance limits disclosed. |
| 04:23:33 | c2j | `3LiZnDQ2S0Gz2waFlpwTkY72BtZ` | [5yImDlgN…](http://192.168.1.195:9047/v1/tenants/c2/jobs/5yImDlgNg8WszaA2aNzw0OqTx2U/chapters?startOrdinal=0) | Waiting; JobDB prerequisite candidate failed; its goal remains OPEN (c40). |
| 04:42:12 | jobdb | `3Lic3qv6M0MhkCyPzKAV5kWWTtv` | [4iuE5Ded…](http://192.168.1.195:9047/v1/tenants/c2/jobs/4iuE5DedNGPLKOqHbPxSJaR7T1u/chapters?startOrdinal=0) | Failed; substantial unfinished work, invalid consultation ref, then allowance stop (c34–39). |
| 04:46:39 | cortex-assistant | `3LicbTPrvHoHRTxNEJ1ZJtW7cX0` | [R5dd9nC0…](http://192.168.1.195:9047/v1/tenants/c2/jobs/R5dd9nC05lXBVIm3xF9sgGVNP9i/chapters?startOrdinal=0) | Succeeded; cortex-assistant package-validation child. |
| 04:47:44 | pgjobdb | `3LicjZy0AHheEPMZQSIIJdT8q6v` | [BAjlUdQ7…](http://192.168.1.195:9047/v1/tenants/c2/jobs/BAjlUdQ7rosP292F5ghTLAztYaV/chapters?startOrdinal=0) | Failed; Go prepared, but requested go --version is invalid (c6). |
| 07:17:43 | recipes | `3LiuyUYEYCbWXJ15qtunPuviShE` | [cf14ca98…](http://192.168.1.195:9047/v1/tenants/c2/jobs/cf14ca98fda8c44e7e4f8bf51cc9a51b/chapters?startOrdinal=0) | Human input pending; asks for historical deployment operator/archive (c68–71). |

The configuration rollout consists of root `ae23…`, its twelve direct owner
attempts, and two package checks. Three owner builds succeeded, eight failed,
and pgjobdb remains waiting. Root is waiting on the next owner goal after
consuming the successful c2j result.

The bounded-history feature consists of Cortex `3LiSd…`, two c2j attempts, and
JobDB `4iu…`. It combines useful implementation progress with a consultation
loop, a recovery handoff to a new goal, and a remaining prerequisite wait.

## Detailed causes and proposed adjustments

### 1. OPEN goals without a running candidate are not being recovered

`await-goal.yaml` waits for success or a terminal **goal**. A failed candidate does
not make its OPEN goal terminal. Consequently:

- pgjobdb `Ujlj…` remains waiting after its package probe `BAjl…` failed.
- c2j `5yIm…` remains waiting after JobDB `4iu…` failed.
- root `ae23…` remains waiting while multiple owner attempts have failed.

At the audit snapshot all thirteen failed sample attempts belong to OPEN goals
with no nonterminal candidate. Nothing in the recorded executions establishes
an active recovery actor for those goals. The current recipes describe an
external controller doing recovery, but describing it does not supply it.

**More than tuning:** establish responsibility for every OPEN goal. When its last
candidate fails, its owner must receive the original errors, saved work, current
authority, and the supported continuation boundary. That owner can repair a
bounded operational problem, obtain an external fix, or explicitly report what
is needed. Continue within the same goal. Parent success still requires the goal's
accepted outcome; an attempt failure must neither imply success nor silently
strand the goal.

Prefer existing c2j goal/restart facilities. If the deployed runtime lacks the
notification or continuation contract needed by a supervisor, specify that exact
gap to c2j/JobDB. This audit proves missing recovery in the observed flow, not
that every necessary engine primitive is absent.

**Recipe tuning alongside it:** after independent work, route an actionable
external blocker through existing consultation/execution coordination. Reserve
terminal operational stops for cases where the permitted local or coordinated
actions are exhausted. The original failure and responsible owner should lead
the outcome; `stop_attempt` should not be the useful part of the diagnosis.

### 2. Native output schemas fail on every recorded model result

Cortex `8e71…`, c16, `stdout.jsonl` records:

> Invalid schema for response_format 'codex_output_schema': In context=('properties', 'files', 'items', 'properties', 'order'), schema must have a 'type' key.

The result succeeds only after prompt-mode fallback. Every sampled model result
reports that fallback and one repair attempt: 187 result records in total.
This does not mean 187 terminal job failures, but it is a pervasive failed first
attempt and a weaker output contract.

**Concrete fix:** give `title`, `role`, `order`, and `source_paths` their actual
supported types in `agent.yaml`, `consultation.yaml`, and other schema producers.
Check the entire schema against the provider's supported subset, including
optional-field rules. Confirm the complete contract with c2ops; fixing only the
first rejected property may reveal another rejection.

The acceptance check is actual native schema acceptance and valid annotations,
not a fixture returning `output_schema_valid: true`. This is interface testing,
not a test of whether Codex is intelligent.

### 3. Advice, acceptance, execution, and recovery are getting confused

In c2j `PAit…`, c22–30, consultants repeatedly request implementation dispatch
from other consultants. Those tasks are correctly prohibited from submitting or
implementing. Each request becomes another inline advice exchange until depth
four is exhausted. Raising the depth would extend the same loop.

The later c2j `5yIm…` run also spends exchanges obtaining a direct serving record:
a nested JobDB acceptance under a root consultation is insufficient for the
outer coordinator's execution lookup. It consults JobDB again merely to register
the already settled acceptance.

There is a second concrete failure: Cortex c59 launches `5yIm…` into goal
`3LiZnDQ2S0Gz2waFlpwTkY72BtZ` after consulting about recovery of
`3LiUpzjeHN55PE9EkBmA0ro35Ko`. The original goal remains OPEN. Neither attempt
lists the other goal in `otherGoalIds`. `coordinate.yaml` reuses execution by
agreement reference, so a newly negotiated recovery agreement can create a new
goal despite the prose saying to continue the old one.

**Concrete orchestration change:** consultations should finish with the answer,
accepted scope, actual serving cell, and any prerequisite execution still needed.
Return those needs to the implementation coordinator; do not ask another advisory
turn to dispatch work. Preserve nested serving acceptance so the coordinator can
use it directly. Recovery needs an explicit existing-goal continuation path,
rather than passing a recovery document to the ordinary new-build path.

Use the agent to distinguish advice from execution needs. A small shared handoff
contract is preferable to routing on special words, a new user-facing key system,
or permissively allowing consultants to submit arbitrary work.

### 4. Response repair loses evidence and can reopen settled consultation

Base `AkRX…`, c18, publishes individual implementation evidence files but lists
`evidence/` as one response descriptor. The normalizer rejects the directory.
The c19 correction inbox contains selected summaries and earlier consultation
evidence, but omits the implementation evidence files. The agent accurately
reports that it cannot republish originals it did not receive.

This is a verified selection/binding problem. The files have stored references
on c18; storage loss is not established. `agent-turn.yaml` retains the inventory
for normalization but binds only `documents` and `evidence_documents` into the
next agent inbox. Retaining a reference for later matching is not the same as
making its content available to the correction task.

Root's JobDB consultation exhibits the related semantic problem: c52 says
`agreed`; after a file correction, c54 says `continue`, followed by acknowledgement
rounds. At c60 it asks a human to end a consultation that explicitly has no
remaining question. The human replies, "your comment is unclear."

**Concrete fix:** preserve original file identities and make the relevant
referenced files available during repair. For a directory descriptor, use the
stored inventory to expose the intended subtree's individual files. Keep
incidental scratch output out of ordinary inboxes and review bundles. File-only
correction should preserve the substantive agreement unless a material change is
actually made; it must not require another round of acceptance bookkeeping.

The next regression must inspect the correction agent's real inbox and the
post-correction outcome, not just the normalizer's artifact map.

### 5. Private Git has three different failure classes

**Gateway routing:** Cortex `8e71…`, c44,
`_c2j/execution/go-module-tidiness.log` runs
`bash scripts/go.sh -C server mod tidy -diff`. Go tries c2j v0.0.120 and JobDB
v0.0.71. Git receives `unsupported Git route` for rewritten addresses such as
`http://192.168.1.195:8082/github/colony-2/jobdb/`. The failure happens before
project tests. Public modules begin downloading normally.

The concrete spelling lacks `.git`; suffix/trailing-slash handling is a plausible
route mismatch, not yet a proven root cause. The client log does not establish
which gateway parser or profile setting is responsible. It does not justify
treating this as a generic missing-token problem.

**Owner action:** gitvend and the c2j Git-profile owner should compare the actual
Go-generated URL with the supported gateway route contract. Test the real module
fetch shape and exact versions, as well as canonical `.git` URLs and denied
access. Fix the responsible route or rewrite configuration while retaining the
scoped credential model. No global token fallback or verification bypass.

**Unpublished candidate fetched upstream:** Shai `0nnv…`, c18, creates candidate
`35e323b5dc140934634b3f77199f024b30d5b838`. C21 restores that candidate using its
retained thin pack. After the foreign c2j advice, c27 enters a new local workspace
with that candidate SHA as its `ref` and no restore artifact; GitHub replies
`upload-pack: not our ref`.

This is stronger evidence than a generic missing-commit report: the recipe's
`consultation.yaml` captures `context.git.hash` as `requester_ref`, then selects
a fresh workspace by that ref. **Recipes owns correcting that selection** to
reuse the exact requester candidate and its managed persistence. c2j owns any
missing capability for restoring that snapshot across scopes. Do not substitute
`main`, which would lose the candidate being discussed.

**Nonexistent requested branch:** JobDB `4iu…`, c34, asks to consult ref
`jobdb/bounded-execution-reader/v1`; c36 reports `ref not found`. This is separate
from both gateway routing and candidate restoration. Return the actual target
resolution error for correction, and default to the registered ref unless a
verified different ref is required. Do not silently change a deliberately pinned
ref. The current generic repair path can instead run into the global limit,
leaving only the allowance failure as the final headline.

Older visible merge failures `8337…` and `3LiGB…` report secret-resolution errors,
but their root-source chapters capture **531599a**, not the current recipe.
They remain relevant operational history; they are not evidence of the same
current-recipe Git failure.

### 6. Package preparation needs a usable correction path

pgjobdb's package child `BAjl…`, c6, has successful preparation metadata for the
pinned Go package. Its command then runs `go --version` and receives
`flag provided but not defined: -version`. The correct probe is `go version`.
The parent cannot correct that small error while it waits for the OPEN goal.

**Tuning:** tell the agent to choose a tool's actual supported probe, with both
Go and conventional `--version` examples. **Behavioral fix:** return probe
diagnostics to the recovery owner and allow correction within the same goal.
Separate probe correction from package-source failure. An explicit tooling policy
can authorize bounded probe-only corrections without asking the human to approve
the same package repeatedly; expanded package or execution authority still follows
the existing approval policy. Successful preparation alone must not adopt a
configuration whose required probe has not passed.

Recipes `0UQ…` is different. C18 writes the accepted
`pnpm:@colony2/c2j@0.0.120` declaration and requests Go for remaining checks.
C19 cannot even prepare that Go proposal: the newly active repository package
fails with `ERR_PNPM_IGNORED_BUILDS`. The candidate configuration is already
affecting subsequent management tasks.

**Beyond prompt tuning:** c2j's tool owner must establish whether the package is
supported under its lifecycle-script policy, or supply a supported reference.
Recipes also needs a management/recovery scope that remains usable when the
candidate's package configuration cannot prepare. Generalize the existing
propose → authorize → validate → adopt flow to configuration-edit tasks; writing
a proposed dependency must not make its own repair machinery unusable. Use a
supported runtime boundary, not an ad hoc bypass of preparation or script policy.

### 7. Validation plans are turning small changes into infrastructure certification

The rollout request was to configure the JobDB URL, root URL, and appropriate
base packages. Root's final plan has 36 statements; per-cell plans add their own
requirements. Required loader harnesses, immutable image admission records,
compiler provenance, and runtime readiness checks appear in the accepted work.

Five failed owner attempts name missing identity/provenance/harness evidence:
base, pulse, c2ops, gitvend, and cortex-assistant. Root also reports missing actual
immutable worker identity. Cortex separately fails a real Chromium sandbox
launch as root. These are reported validation blockers; this audit has not
reproduced the provisioner's behavior.

Some validation is appropriate: a package declaration should be usable, and a
required browser check must actually run in a supported environment. The problem
is making every diagnostic limitation a new acceptance requirement. Successful
c2j, JobDB, and pulse-tart owner runs demonstrate a narrower pattern: verify the
configuration and relevant tools, disclose conditional integrations and image
provenance limits, and complete the agreed configuration scope.

**Tuning:** anchor each required check to the requested outcome or an existing
project requirement. Separate required checks from useful diagnostics and
conditional integrations. A config edit should not automatically re-prove the
c2j parser, all negative configuration fixtures, or the entire worker platform.
Consultation supplies usable interface advice, not an ever-expanding certification
contract. Document evidence that is unavailable without claiming a pass.

Review inflated plans before locking them in. For existing goals, explicitly
reconcile the recorded requirements through the scope-change process; do not
silently mark an unmet requirement passed. If immutable worker identity is truly
required, the provisioner/c2j must expose invocation-bound evidence. If Chromium
is required, the worker owner must provide a supported sandbox-capable environment.
Those capabilities cannot be supplied by a better prompt.

### 8. One global turn limit conflates work, coordination, and lack of progress

JobDB `4iu…` uses two turns for design/test planning and ten for implementation.
Its recorded progress grows from an API and five focused tests to durable
indexes, remote operations, recovery handling, and 2,480 passing test events.
Acceptance is still incomplete. Its final invalid-ref request then meets the
same exhausted allowance.

Cortex `3LiSd…` similarly consumes work turns on coordination and recovery. It
launches another c2j child at c59, then immediately stops on its own allowance.

**Tuning plus small control-flow changes:** distinguish actual work, response
correction, dependency waiting, and repeated no-progress advice. Have the agent
provide a brief progress/remaining-work explanation at the bound; permit a
policy-bounded continuation or hand it to the goal owner. Retain overall limits
and stop unproductive loops. Do not universally increase `max_iterations` or
judge progress solely by a growing test count. Newly launched required goals
must remain supervised even if the current parent attempt exhausts its allowance.

### 9. Human questions still include internal process and missing-evidence decisions

There are twelve generated forms in this sample, including legitimate merge
and package approvals. Two cases need attention:

- Root's c62 asks for acknowledgement that consultation is complete, while
  saying no clarification remains. This should have returned automatically.
- The separate audit `cf14…` reaches a human question about locating a historical
  deployment operator/archive or accepting missing records. Its human had asked
  for deeper analysis and module reports. The investigation traverses several
  owners before stopping for historical provenance.

The latter has a real information gap, but a report can ordinarily say what is
proven, what is unknown, and which owner should investigate without first
certifying the historical deployment. Ask for an operator contact only if it
materially blocks an action the user requested. Do not make delivery of the
audit depend on an invented completeness requirement.

**Tuning:** complete advisory exchanges when their question is answered. Before
asking the human, explain the unresolved decision and why the permitted agent or
owner cannot resolve it. Use a lightweight judgment step where needed; do not
add a collection of phrase-specific filters or a routine extra review task.

## Proposed implementation order

| Priority | Concrete work | Primary owner / files | Completion evidence |
| --- | --- | --- | --- |
| P0 | Correct provider-facing schemas | recipes `agent.yaml`, `consultation.yaml`, other schema producers; c2ops adapter contract | Complete native schema accepted; normal turn has no rejection-driven fallback |
| P0 | Preserve requester candidate during inline consultation | recipes `consultation.yaml`; c2j workspace restoration if needed | Changed local candidate survives foreign advice and requester return without upstream SHA fetch |
| P0 | Carry original evidence into response correction | recipes `agent-turn.yaml`, `artifact-result.yaml`, repair callers | Correction reads original relevant bytes and retains their producing identities |
| P0 | Repair the private-module route | gitvend and c2j Git-profile/deployment owner | Exact Go module fetch succeeds through the intended scoped gateway; denied access remains denied |
| P0 | Assign and connect goal recovery | recipes coordination plus c2j/JobDB and the serving controller | Failed candidate → bounded same-goal repair → successful candidate → waiting parent resumes |
| P1 | Return accepted prerequisites from consultation to execution | recipes `consultation.yaml`, `coordinate.yaml`, `prompts.yaml` | Nested acceptance dispatches once to its actual owner; no advice/submission recursion or re-registration round |
| P1 | Correct package probe and failed-config recovery | recipes `packages.yaml`, `package-check.yaml`, `package-tools.yaml`; c2j tool preparation | Probe errors are repairable; invalid proposed packages cannot disable management; adoption still requires validation |
| P1 | Preserve target-resolution errors and improve work-budget handling | recipes `resolve-target.yaml`, `coordinate.yaml`, `develop.yaml` | Missing ref receives specific correction; progress and waiting do not masquerade as no-progress loops |
| P1 | Narrow validation and human-question instructions | recipes `prompts.yaml`, consultation/review handling | Config acceptance stays tied to its outcome; completed advice returns without a human acknowledgement |
| P2 | Expose required runtime identity/capabilities consistently | provisioner, c2j, affected application owners | Only genuinely required checks receive actual invocation-bound identity and supported environment |

For recovery of the existing sample, start with the small pgjobdb probe error,
base's c18 evidence, and Shai's persisted candidate; resolve the gateway and
package-manager failures with their owners. Resume JobDB's unfinished implementation
from its retained candidate with a real consultation target. Reconcile the
rollout's required-versus-conditional evidence before launching further validation.
Keep monitoring the existing goals and dependencies; a newly submitted build is
not proof of recovery.

## Why recent tests missed this, and the tests to add

The previous tests improved native diagnostics, artifact identity, inline advice,
permissions, and scope coverage. Those improvements are visible here: Cortex's
verification failure reaches the implementation agent as the original command
log, and ordinary consultations and several merge paths complete. The remaining
gaps are at boundaries the fixtures do not exercise.

| Boundary | Current blind spot | Regression needed |
| --- | --- | --- |
| Provider schema | Mocked responses declare successful schema validation | Validate the complete real schema against the adapter/provider contract; reject unsupported annotation definitions |
| Artifact correction | Tests retain/match identities without making the original evidence necessary in the next agent inbox | Produce evidence, return a directory descriptor, correct it, and read the original files in the actual correction task |
| Consultation workspace | Read-only/unchanged fixture workspaces do not reproduce an unpublished requester candidate | Modify requester repository, persist it, consult another cell, return to the exact candidate; assert no branch-tip substitution |
| Consultation semantics | Fixture consultants generally agree or request genuine advice | Return a settled prerequisite needing execution; assert one handoff to the owner, preserved acceptance, no recursive dispatch advice |
| Goal lifecycle | `goal-monitoring.test.yaml` mocks eventual success or explicit goal failure | Real failed candidate while goal stays OPEN; recovery owner continues the same goal; waiting parent consumes the successful replacement |
| Package probe | Parent tests mock probe outcomes and normally use a valid Ruff example | Successful preparation followed by invalid argv, bounded correction, successful probe and adoption; separately fail preparation before the management task starts |
| Git transport | Local fixture repositories bypass production gateway URL rewriting | Gateway/profile owner tests Git URLs generated by Go and scoped auth, plus exact retained candidate restoration |
| Budget/error routing | Tests establish that exhaustion fails without a human review | Progressing work, exhausted parent with a live dependency, and invalid target at the last allowance preserve useful state and the actual error |

Where c2j's fixture API cannot model a lifecycle boundary, describe that specific
test limitation and use a supported native integration case with the owning cell.
Do not replace missing behavior with a mock and call the recovery loop tested.
No broad model-quality evaluation is required for these defects.

## Evidence access and limits

The catalog links the original chapter records. Individual artifacts can be read
at `/v1/tenants/c2/jobs/<attempt>/chapters/<ordinal>/artifacts/<URL-encoded-name>`
on the same host. Particularly useful evidence:

- `8e71…` c16 `stdout.jsonl`: native provider schema rejection; c44
  `_c2j/execution/go-module-tidiness.log`: original gateway failure.
- `BAjl…` c6 `_c2j/preparation.json` and
  `_c2j/execution/probe_approved_packages.log`: Go prepared, probe argv invalid.
- `0UQ…` c18–19: candidate config activates pnpm package before the next proposal
  can prepare; original setup failure remains in c19.
- `0nnv…` c18, c21, c27: candidate creation, successful thin-pack restoration,
  then new workspace selection by unpublished SHA.
- `AkRX…` c18–19: producer inventory, correction input bindings, and
  `response-correction.md` identifying the omitted originals.
- Root `ae23…` c52–69: agreement, artifact correction, acknowledgement loop,
  unnecessary human question, and eventual agreement.
- JobDB `4iu…` c18–34: implementation progression; c36 invalid ref; c39 final
  allowance failure. Cortex `3LiSd…` c59 records the new recovery goal.
- Successful rollout controls: c2j c30, JobDB c33, and pulse-tart c32
  `merge-review.md` explain required checks and disclosed limitations.

I also read the separate production audit's retained report drafts and compared
its claims with these records. Its broader historical counts include older recipe
versions; they are not mixed into this current-recipe sample. Its pending owner
investigations are not treated as confirmed external implementation defects.

This audit establishes captured behavior and source-level causes where identified.
It does not establish that gateway or worker configuration is unchanged since
the failing commands, and it does not certify a deployed fix. Runtime/environment
remediation needs the focused checks above, followed by successful continuation
of the affected goals.

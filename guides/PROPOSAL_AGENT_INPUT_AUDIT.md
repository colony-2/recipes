# Proposal: deliberate agent instructions and task inputs

Status: historical field audit of the pre-change implementation. The active adaptive
path now implements the [standard inbox plan](IMPLEMENTATION_STANDARD_AGENT_INBOX.md).
The source observations below describe the audited baseline, not current behavior.
Date: 2026-11-02.

## Decision

Stop serializing internal workflow state into agent prompts. Do not relocate the
same state dump into context.json. Select information according to the decision
the receiving agent must make. Put standing rules in additional instructions at
session creation, current assignments in prompts, and substantial evidence in
explicitly named inbox files. Omit inapplicable sections entirely.

The user accepts new-session-only insertion of standing instructions. This
proposal does not require instruction refreshes on resumed sessions or extra
setup text to compensate for inherited sessions.

This work **fits** the recipes cell's purpose: recipes own their prompts,
artifact contracts, and workflow guidance. c2ops owns the implementation of the
`instructions` channel; this audit establishes recipe usage, not whether that
channel becomes a system or developer message internally. c2j owns artifact
materialization and runtime persistence. No ownership changes are proposed.

## Evidence and audit boundary

The active root [build.yaml](../build.yaml) selects
[adaptive/build.yaml](../recipes/adaptive/build.yaml), which selects
[adaptive/develop.yaml](../recipes/adaptive/develop.yaml).
Its `start` state constructs `flow`; subsequent states and helper recipes add
fields. [adaptive/agent.yaml](../recipes/adaptive/agent.yaml) passes:

1. `vars.instructions` directly inside the prompt.
2. The current phase assignment.
3. `json_stringify(flow)` excluding only session, documents, result,
   repair_artifacts, and repair_base_documents.
4. The repository's current phase prompt addition.
5. The same `vars.instructions` through the op's `instructions` input.

[adaptive/agent-turn.yaml](../recipes/adaptive/agent-turn.yaml) binds documents
and verification evidence and adds actual inbox/outbox paths to every prompt.
It supplies `instructions` only to new sessions. This is already the desired
session insertion behavior.

The tables below cover every top-level flow field constructed or subsequently
added along this active path, including currently excluded fields and fields
normally removed before agent dispatch. Nested records are audited separately.
They also cover the adjacent reviewer and consultation prompts. This is a
source audit, not a measurement of every live job or an exhaustive audit of
unrelated new-ticket, superpowers, or creation-only agent prompts.

Related proposals: [initial instructions](PROPOSAL_AGENT_INSTRUCTIONS_AND_SKILLS.md)
and [payload transport](PROPOSAL_RECIPE_PAYLOAD_TRANSPORT.md). The latter records
historical growth from nested consultation results. Moving data to artifacts
addresses transport; selecting relevant data addresses this proposal's problem.
The older develop/light recipes already read context.json, but that placement
alone is not the proposed contract.

## Each top-level flow field

“Internal” means retain in recipe state and job history, not discard from the
system. “File” means bind a real artifact and name its resolved inbox path;
never send a runtime artifact reference object as a substitute for its contents.

### Task and human input

| Field | Current origin/use | Proposed agent use |
| --- | --- | --- |
| request | Original build prompt; reused by hooks, reviewers, and child coordination. | Include the original request in the task prompt. Preserve it when recovery or continuation messages change. |
| message | Initially duplicates request; later continuation or specialist revision text. | Use only as the current action/direction, avoiding an initial duplicate of request. Make its purpose explicit. |
| target_directory | Validated repository-relative task scope. | Include in task prompt; explain in standing rules that it does not redefine ownership. |
| phase | design, test-plan, or implement. Selects task and write permissions. | Include as a clear assignment with permitted actions and required deliverables. |
| last_phase | Previous successful turn's phase. | Internal; used for orchestration, not task reasoning. |
| event | Machine labels such as start, verification, assessment, coordination, response_invalid, and rebase_conflict. | Translate into a specific current action and evidence paths. Do not expose an unexplained enum. |
| feedback | Human answer/review/direction fields, added after human interaction. | Supply actual answers and requested changes, with question labels and relevant file paths. Keep short answers in prompt; substantial feedback in a file. Do not dump form metadata. |
| annotations | Accumulated input, agent, specialist, child, and human annotations. | Supply applicable unresolved feedback anchored to documents. Preserve source and resolution history in evidence, but avoid repeating all historical annotations each turn. |
| issues | Response/gate validation errors, added during repair. | Include the precise correction list only on a repair turn. Clearly distinguish invalid output from failed implementation. |
| plan_keys | Recorded prerequisite keys from reviewed design/test plan. | Include the current prerequisite key list when external work exists, with agreement references. Omit the section when there are none; the schema can still require keys: []. |

### Coordination and dependencies

| Field | Current origin/use | Proposed agent use |
| --- | --- | --- |
| threads | Consultation records keyed by stable request key. | Provide a compact coordination index only when nonempty; see nested audit below. Name final agreement/evidence files. |
| jobs | Submitted prerequisite records keyed by stable request key. | Combine with the coordination index: key, target, status, outcome, relevant evidence. Needed to avoid duplicate requests and premature completion. |
| root_cell | Explicit input or c2j self root_repo; routes creation work. | Internal routing. If an agent must reason about a particular root's ownership, supply its identity for that task only. |
| root_ref | Explicit input or discovered root_ref/main. | Internal routing; expose a revision only for a concrete compatibility or ownership question. |
| consultation_recipe | Selector used to execute serving consultations. | Internal. Agent requests consultation through typed output, not recipe selection. |
| build_recipe | Selector used to launch prerequisite builds. | Internal. |
| create_recipe | Selector used to launch cell creation. | Internal. |
| pending_outside | Remembers outside disposition while running external work is settled. | Internal; orchestrator controls lifecycle. |

### Hook configuration and specialist work

| Field | Current origin/use | Proposed agent use |
| --- | --- | --- |
| hook_settings | Normalized require_design, prompt_additions, variables, consultations. | Do not expose entire configuration. Route selected guidance and relevant values as described below. |
| settings_artifact | Runtime artifact reference for build-settings.json, supplied to hooks. | Internal reference. Bind selected agent-relevant settings as a file only when needed. |
| require_verification | Controls whether skipped verification is acceptable. | Keep gate internal. Tell the agent required verification expectations in its assignment; report skipped checks accurately. |
| design_context | before_design hook result; corresponding artifacts also bound. | Point design agent to research/design-context documents. Include substantive summary if useful; exclude status envelope and artifact refs. |
| preparation | prepare hook result; artifacts merged into documents. | On failure give summary, diagnostics, and repair assignment. On success expose only information that affects the work or outcome report. |
| hook_digest | Serialized preparation/specialist evidence used to determine approval reuse. | Internal. |
| specialist_reviews | Keyed specialist checkpoint/verdict records. | Provide current findings file paths and whether revisions are required. Keep scheduling and historical rounds internal. |
| specialist_round | Counter used to distinguish specialist runs. | Internal. |
| design_round | Counter for design-context runs. | Internal. |
| validation_round | Counter for prepare/validation runs. | Internal. |

### Verification, recovery, and output repair

| Field | Current origin/use | Proposed agent use |
| --- | --- | --- |
| verification | Verification hook evidence or synthesized failure evidence. | Give actual status, what ran, summary, and evidence paths when relevant. Never collapse skipped/failed into passed. See nested audit. |
| verification_artifacts | Runtime diagnostic artifact map, separately bound to inbox. | Bind files and list useful paths. Do not serialize reference map. This field is currently not excluded from the blob. |
| verification_allowed | Gate result for passed or permitted skipped verification. | Internal. Agent receives verification facts, not a gate boolean suggesting success. |
| rebase_recovery | Native failure with rebase metadata/diagnostics. | Only on recovery, supply required base/candidate/target identity and diagnostic paths in a recovery brief; preserve full failure as optional evidence. |
| rebase_recovery_pending | Prior recovery input carried into initial flow; removed after successful rebase. | Internal marker. Derive explicit recovery assignment when applicable, not a freestanding flag. |
| rebase_repairs | Bounded recovery attempt counter. | Internal. |
| repair_attempts | Bounded response repair counter. | Internal. |
| repair_artifacts | Artifacts from invalid response retained for reuse; already excluded from prompt dump. | Continue retaining/binding internally. Tell repairing agent which existing files are eligible when relevant. |
| repair_base_documents | Original document snapshot used to isolate response repair; already excluded. | Internal snapshot. Keep read-only mode and allowed repair scope explicit in task. |
| iterations | Agent turn budget accounting. | Internal. |
| max_iterations | Configured turn limit; triggers human direction. | Internal; communicate a concrete request for direction when necessary rather than exposing counters. |

### Candidate review, merge, and terminal state

| Field | Current origin/use | Proposed agent use |
| --- | --- | --- |
| candidate | Git inventory, identities, job URL, and change digest from git-candidate.yaml. | Reviewers read merge-candidate.json and merge-candidate.diff. Implementation agent receives only a relevant repair/accounting request and file paths. |
| candidate_changed | Whether candidate file inventory is nonempty. | Internal gate; an outcome reviewer can inspect inventory and explain no-change rationale. |
| assessment | Independent approve/revise result. | On revise, provide findings and repair action. On approve, retain internally unless relevant to outcome preparation. |
| reviews | Human outcome receipt map; starts empty. | Internal receipts. Provide actual requested changes or approved scope where relevant, not receipt structures. |
| reviewed_change_digest | Candidate digest associated with reviewed outcome. | Internal approval binding. |
| reviewed_hook_digest | Hook evidence associated with reviewed outcome. | Internal approval binding. |
| commit_message | Reviewer subject/summary plus job URL, consumed by merge. | Keep merge payload internal. Summary agent proposes subject through its schema; expose specific correction only if necessary. |
| merge_chases | Attempts to catch an advancing target branch. | Internal. |
| chase_pending | Routes post-rebase validation/review reuse; removed in dispatch. | Internal; normally not agent-visible. |
| reuse_merge_approval | Cleared defensively in several paths; no writer found in audited adaptive path. | Internal; do not revive as agent input. |
| review_hint | Human form hint; removed in dispatch. | Internal UI wording; normally not agent-visible. |
| publication | Hook result after successful merge, normally terminal rather than redispatched. | Internal lifecycle; include substantive outcome in final user report. A future publication-repair agent should get a scoped task and evidence. |
| disposition | Terminal implemented/delegated/unchanged/outside/cancelled classification. | Internal lifecycle; reflect meaningful outcome in final user report. |
| session | Runtime checkpoint, already excluded. | Internal op input only. Never include checkpoint/export data in task context. |
| documents | Artifact map, already excluded. | Bind through artifacts. Provide a curated list of required/current evidence paths, not the whole map. |
| result | Previous structured agent response, already excluded. | Internal routing. On response repair expose only relevant invalid fields or the previous response as a named file. |

## Nested records: what survives selection

### Consultation threads and child jobs

Sources: [coordinate.yaml](../recipes/adaptive/coordinate.yaml) and
[consultation.yaml](../recipes/adaptive/consultation.yaml).

| Nested information | Proposed use |
| --- | --- |
| Map key / request.key | Preserve stable coordination key; use in returned keys and duplicate detection. |
| request.kind | Preserve meaningful distinction between feature, create, and expert when applicable. |
| request.cell, request.ref | Show requested target when useful; distinguish from resolved target. |
| request.request, request.role | Keep scope and responsibility in agreement/request document. Brief index can name the outcome without repeating long text. |
| target.repo, target.ref | Preserve resolved serving target in coordination index, especially redirects. |
| status | Show factual consultation/build progress; a completed conversation does not itself mean agreed work or completed implementation. |
| job_id | Keep internal for awaiting; expose a diagnostic link only when useful. Agent should not manage child jobs directly. |
| result.outcome and agreement text | Preserve agreed/declined/redirected disposition and accepted scope with final agreement file paths. |
| result.final_artifacts, artifact_refs | Materialize files and publish paths; omit runtime descriptors. |
| result.continuation | Keep runtime handoff internal; retain conversation file for scope provenance when needed. |
| result requester/consultant sessions, state, transcript inventories | Do not recursively expose. Keep full conversation as optional evidence; default to current agreement and unresolved questions. |
| result.annotations | Route actionable feedback once with source identity; avoid duplicate accumulation in index and documents. |
| Child result merged/disposition | Preserve exact execution outcome; delegated/unchanged is not equivalent to a local merge. |
| Child result created_cells[].repo/ref/revision | Include created identities and pinned revisions when subsequent feature consultation depends on them. |
| ready | Internal computed creation gate; derive an accurate outcome summary, preserving missing/invalid creation evidence. |
| failure | Provide concise cause and diagnostic paths on failure; full runtime failure envelope remains optional evidence. |
| Other child result fields | Default internal. Add a selected field only for a documented receiving-agent decision. Never recursively serialize arbitrary outputs. |

Suggested conditional index file: `coordination.md`, containing key, kind,
resolved target, consultation disposition, execution status/outcome, and paths
to agreements/results. These are separate facts, not one “done” flag. Omit the
file and prompt section when no external work exists. Include known active keys
even when their evidence is not needed this turn to prevent duplicate requests.

### Hook settings and specialist records

| Nested information | Proposed use |
| --- | --- |
| require_design | Internal phase selection; agent receives actual assigned phase. |
| prompt_additions.design/test_plan/implementation | Include selected addition as labeled current repository phase guidance. Keep phase-varying material out of permanent session rules. |
| prompt_additions.plan_assessment/outcome_assessment | Route only to matching reviewers. Current inspect.yaml does not explicitly select these additions; resolve this gap during implementation. |
| variables | Supply only values the agent needs, preferably as a named settings document with their meaning. Arbitrary hook configuration is not automatically agent context. |
| consultations[].key/checkpoint/required | Internal scheduling/gating. Report a current required revision explicitly, and identify the findings source. |
| consultations[].role/request | Assignment for that specialist, not every implementation turn. |
| specialist_reviews.*.key/checkpoint/required/outcome/assessment | Summarize current relevant verdict and evidence paths. Internal round-based map keys and historical successful verdicts need not recur. |
| Hook result api_version/status/summary/failure/artifact_refs | Keep version/envelope internal; expose factual status and actionable summary, bind diagnostics. Preserve required failures rather than silently dropping absent artifacts. |

### Verification and recovery evidence

| Nested information | Proposed use |
| --- | --- |
| Verification status/ok/summary | Status and substantive summary are useful. Avoid redundant ok boolean when status conveys it. |
| failure.kind/code/message | Include when needed to distinguish failed checks from infrastructure or missing-evidence failures. |
| failure.attrs.command | On native command failures preserve command/exit details that actually exist and name stdout/stderr diagnostics under _c2j/command/. Do not require invented fields. |
| Diagnostic reference maps | Bind diagnostic files and give paths; do not stringify descriptors. Missing diagnostics must remain an explicit limitation. |
| Rebase attrs.rebase.base_hash/candidate_hash/target_base_hash | Include on recovery to identify saved local work and adopted target. |
| Rebase diagnostic metadata | Bind conflict evidence; preserve full metadata as optional file if needed for debugging. |
| candidate.diff and commits.log | Required recovery evidence. Tell agent to reconcile the entire saved change with the target already adopted by the recipe. |
| Candidate base/head/files | Required for exact-candidate review and file accounting; read from inventory file. |
| Candidate change_digest | Internal approval reuse; human/agent reviewers need inventory and diff, not digest arithmetic. |
| Candidate job_url | Useful provenance in outcome report; not required for implementation reasoning. |

Recovery instructions must match the active adaptive behavior: the recipe saves
the whole candidate delta, resets the known clean candidate to its base, then
adopts the recorded target. The agent reconciles saved work there; it must not
be instructed to continue an active rebase. Older develop-path instructions
have different recovery semantics and should not be copied into this path.

## Instruction and prompt content beyond the blob

| Current content | Proposed destination/use |
| --- | --- |
| Cell is whole repository; read purpose/infer ownership; local versus external work | New-session instructions only. Include reading applicable AGENTS.md explicitly, consistent with repository conventions. |
| Consult before external changes; stable keys; new-cell proposals; independent progress before blocked | New-session instructions only. Current key/status facts stay conditional task evidence. |
| Recipe owns commits/rebase/merge/publication/job submission | New-session instructions only. Recovery tasks clarify permitted local reconciliation without duplicating all workflow rules. |
| Output file description/title/role/order/source_paths conventions | New-session instructions; enforce structure through output schema. Explain evidence/source-path meaning once. |
| Artifact inbox/outbox resolved paths | Per-turn prompt because directories belong to the current op. Keep relative output-path requirement adjacent. |
| Design assignment and design.md requirement | Current design task prompt. Research paths only when supplied. |
| Test-plan assignment and test-statements.md requirement | Current test-plan prompt, including required statement constraints. |
| Implementation assignment and implementation.md/test-results.md requirements | Current implementation prompt. Preserve expectations and exact verification facts. |
| response_invalid handling | Explicit repair task with issue list, missing file paths, eligible existing artifacts, and no-code-edit scope. Do not rely on event enum alone. |
| rebase_conflict handling | Explicit recovery task plus selected evidence; only on recovery. |
| “Use typed workflow state below” | Remove when replacing the dump; point to actual selected task evidence instead. |
| Output schema | Continue using op output.schema. Do not duplicate complete JSON Schema in prose. |
| Empty placeholders | Omit prompt labels/sections for empty assignments, evidence, corrections, feedback, and coordination. Required response schema fields are a separate concern. |

## Adjacent agent calls

[inspect.yaml](../recipes/adaptive/inspect.yaml) already selects a narrower
`evidence` object, but stringifies it. Assessment receives verification and
full child job records; summary also receives candidate. Replace recursive
child/verification envelopes with selected summaries and file paths. Keep
original request, reviewer role, actual specialist assignment, concrete repair
issues, exact candidate files, and evidence. Do not include empty Assignment,
Evidence, or Response corrections lines. Keep assessment and summary permissions
in their task prompts; the shared standing instructions should not imply these
read-only agents can themselves request consultation through an unsupported
response schema.

[consultation.yaml](../recipes/adaptive/consultation.yaml) is closer to the
proposed separation: stable cell/setup instructions, current dialogue message,
human direction, latest file paths, and output directory. Keep participant,
thread identity, purpose, and assignment available at session creation. On each
turn supply the new message, applicable human direction, and current evidence
paths. Remove setup reinsertion used only for inherited-session concerns under
the user's accepted policy. Runtime rounds, seen counters, sessions, and
conversation envelopes remain internal. A full transcript can remain optional
evidence for disputed scope, without being embedded every turn.

[response-repair.yaml](../recipes/adaptive/response-repair.yaml) stringifies
issues, the previous response, and human direction. Short concrete issue lists
and actual direction belong in the repair prompt. Put a large previous response
in a named file, or quote only invalid fields. Retain a clear repair-only task
and eligible document paths. Do not emit empty Human direction JSON.

The older [develop agent](../recipes/develop/agent.yaml) and
[light agent](../recipes/light/agent.yaml) show file-based context transport.
Apply the same semantic selection if these paths remain supported; copying their
context.json contract wholesale would preserve the current information problem.

## Proposed turn examples

Initial test-plan task, with no external dependencies or feedback:

```text
Phase: test-plan
Request: <original request>
Target directory: <repository-relative directory>

Write test-statements.md before implementation. <test-statement requirements>
<selected repository phase guidance, only if present>

Inbox: <resolved inbox directory>
Outbox: <resolved outbox directory>
Return deliverable paths relative to this outbox.
```

Verification repair, only when it occurs:

```text
Phase: implement
Request: <original request>
Target directory: <directory>

Repair the failed verification described in <inbox>/verification.md.
Read <inbox>/_c2j/command/<actual diagnostic paths>.
Preserve the agreed design and test statements at <actual paths>.
Update implementation.md and test-results.md with accurate results.
<coordination index path only when external work exists>

Inbox: <resolved inbox directory>
Outbox: <resolved outbox directory>
Return deliverable paths relative to this outbox.
```

The proposed names verification.md and coordination.md are new contracts, not
claims that these files currently exist. Reuse useful existing reports instead
of creating redundant summaries. A manifest is justified only when selecting
among many files materially helps the task. There is no mandatory context.json.
Moving evidence to files does not guarantee fewer tokens if all files are read;
selection and removal of duplicated envelopes provide the main benefit.

## Implementation proposal and acceptance statements

1. Replace the flow denylist with explicit prompt construction and selected
   evidence bindings. Unknown future flow fields must stay internal by default.
2. Remove duplicate standing instructions from adaptive prompts; retain their
   existing new-session instructions input. Do not add resume refresh machinery.
3. Route original request, phase assignment, target, and applicable phase guidance
   directly. Emit conditional tasks for feedback, response repair, verification,
   consultation changes, specialist revision, and rebase recovery.
4. Build compact coordination evidence from stable keys and authoritative outcomes;
   bind scope agreements and child results without recursive runtime state.
5. Keep approval receipts, gating, counters, selectors, and transport references
   inside recipes. Preserve durable job evidence and human outcome reporting.
6. Apply the same selection to reviewer and response-repair prompts. Resolve
   reviewer phase-guidance routing explicitly. Evaluate supported older paths
   separately against these rules.
7. Validate deterministically first; use bounded embedded recipe runs only where
   needed to verify materialized evidence paths. Never launch real builds merely
   to review this proposal.

These statements are defined before implementation. For a future implementation
job, persist them as c2 test-plan artifacts; this repository proposal does not
claim to have created runtime artifacts.

| ID | Test statement (each at most 30 words) | Files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| AI-01 | New sessions receive standing cell rules once through additional instructions. | recipes/adaptive/agent.yaml, recipes/adaptive/agent-turn.yaml | Critical | Integration / c2j fixture runner |
| AI-02 | Resumed turns do not duplicate standing cell rules in task prompts. | recipes/adaptive/agent.yaml, recipes/adaptive/agent-turn.yaml | High | Integration / c2j fixture runner |
| AI-03 | Initial tasks retain original request, target directory, phase requirements, and applicable repository guidance. | recipes/adaptive/agent.yaml | Critical | Integration / c2j fixture runner |
| AI-04 | Empty coordination, feedback, recovery, and correction sections are absent from initial task prompts. | recipes/adaptive/agent.yaml | High | Integration / c2j fixture runner |
| AI-05 | New internal workflow fields never appear automatically in agent inputs. | recipes/adaptive/agent.yaml | Critical | Integration / c2j fixture runner |
| AI-06 | Agents see stable consultation keys, agreed scope, execution status, and outcome evidence without nested runtime state. | recipes/adaptive/coordinate.yaml, recipes/adaptive/agent.yaml | Critical | Integration / c2j fixture runner |
| AI-07 | Failed, declined, redirected, running, and incomplete external work cannot appear as successfully completed prerequisites. | recipes/adaptive/coordinate.yaml | Critical | Integration / c2j fixture runner |
| AI-08 | Verification repair identifies failed checks and available diagnostics; missing evidence remains explicit. | recipes/adaptive/verify.yaml, recipes/adaptive/agent.yaml | Critical | Integration / c2j fixture runner |
| AI-09 | Response repair names corrections and eligible documents without authorizing code changes. | recipes/adaptive/agent.yaml, recipes/adaptive/response-repair.yaml | Critical | Integration / c2j fixture runner |
| AI-10 | Recovery tasks identify saved local work and the adopted target without requesting continuation of an inactive rebase. | recipes/adaptive/rebase-recovery.yaml, recipes/adaptive/agent.yaml | Critical | Integration / c2j fixture runner |
| AI-11 | Human answers and unresolved specialist findings reach the responsible agent with their evidence paths. | recipes/adaptive/develop.yaml, recipes/adaptive/specialists.yaml | High | Integration / c2j fixture runner |
| AI-12 | Reviewers receive exact candidate evidence, applicable assignment guidance, and accurate verification and dependency outcomes. | recipes/adaptive/inspect.yaml | Critical | Integration / c2j fixture runner |
| AI-13 | Referenced evidence files exist in the current operation inbox, including after session resume. | recipes/adaptive/agent-turn.yaml | Critical | Integration / embedded c2j artifact materialization |
| AI-14 | Approval reuse, bounded retries, dependency gates, and terminal lifecycle decisions retain their existing behavior. | recipes/adaptive/develop.yaml | Critical | Integration / existing adaptive fixture suite |

## Limits and follow-up decisions

No recipes, schemas, or runtime contracts were changed for this audit. No model
runs were needed to establish the source-level findings. The proposal preserves
existing output schemas; optionality of required empty response fields is a
separate decision. Exact instruction message roles require c2ops implementation
inspection if that distinction becomes relevant. Evidence summaries must be
mechanically faithful and must not replace authoritative outcome gates.

# Adaptive coordination, goal monitoring, reviews, and package requests

Historical baseline, superseded by the [gap-closure plan](PLAN_ADAPTIVE_GAP_CLOSURE.md)
and [assessment](ASSESSMENT_ADAPTIVE_GAP_CLOSURE.md). The compatibility paths and
remaining gaps described below have since been removed or addressed.

Implementation report, 2026-11-05. Changes are local and uncommitted. This compares
the implementation with the [accepted plan](PLAN_ADAPTIVE_COORDINATION_AND_REVIEWS.md)
and the subsequent instruction to monitor **goals**, not individual job attempts.
No production goals, jobs, answers, permissions, or remote repositories were changed.

## Outcome

The adaptive workflow now uses goal success as its dependency boundary. Codex can
request cross-cell work without inventing prerequisite keys, consultations can
obtain downstream advice, and a working agent can request development tools using
an explicit response contract. Human outcome reviews have one primary brief and a
single change-request action; Codex determines whether changes require design or
implementation work.

The existing development phases, hooks, native child execution, Git persistence,
artifact identities, independent assessment, and review protocol remain in use.
There is no new workflow engine, parallel goal ledger, or mandatory classifier.

## Changes compared with the plan

| Plan area | Implemented | Differences and boundaries |
| --- | --- | --- |
| Clear human reviews | One current overview is primary; other documents are supporting or diagnostic. Outcome bundles select current required summaries, explicit sources, and current verification evidence. Summary instructions explain the decision, outcome, evidence, limitations, recommendation, and reading order. | Uses existing native review metadata. Cortex itself was not changed or visually tested. |
| Specific questions | Outcome reviews use the actual candidate subject and “Merge these changes?”; clarification titles use the agent's question/title. Blocker briefs explain the current reason. | Compatibility fallbacks remain when an older response lacks a dedicated title or brief. A useful agent-authored brief is preserved; otherwise the recipe builds a factual brief from the current explanation/questions. |
| One change-request action | Outcome and blocker reviews offer “Request changes.” Exact feedback goes to the existing working Codex session, which chooses implementation or redesign. | Old `redesign` continuation handling remains for compatibility; new forms do not require the user to select a phase. |
| Existing dependency waiting | Repeating an execution request refreshes/waits for its existing goal. A known running dependency is handled before an empty-list blocker becomes intervention. | Truly unrelated questions can still reach the human. Durable waiting itself does not invoke another Codex turn. |
| Goal monitoring | Prerequisite, consultation, creation, package-validation, and agent-submitted validation waits use goal success. Goal IDs and successful attempt identities are retained where supplied. Automatic validation records are deduplicated by goal. | Job IDs remain historical/compatibility lookup handles. Waiting through such a handle still resolves the goal; it does not wait for that particular attempt to succeed. |
| Replace agent-authored keys | Agents return `requests` describing consultation or execution. Recipe-generated references identify agreements, and `plan_keys` obligations are removed. | Internal coordinator maps and legacy explicit consult/submit fields remain supported. They are not a second model-maintained work ledger. Full removal of legacy fields needs a separate compatibility cleanup. |
| Downstream consultation | A consultation can return requests to other owning cells. Native child execution waits for their goals and resumes the participant that requested advice with the results. | Nested consultation is bounded at four levels. This is advice and scope agreement, not authority to implement. |
| Execution handoffs | Child instructions explicitly authorize implementation of accepted scope and supersede consultation-only discussion restrictions. | The original conversation is retained as historical evidence; it is no longer appended as live instructions. The consultation agent authors the execution brief with the accepted documents. |
| Baseline corrections | Reusing a baseline artifact or republishing identical bytes is valid. Different content is detected before ordinary implementation can accept it. | Actual expectation changes retain the redesign/deprecation requirement. Comparison uses native artifacts and a bounded command, not filename-presence rules. |
| Package requests | Authorize the proposal, validate it in a child goal, adopt the exact matching config, and resume the blocked work. Failed validation leaves the parent config intact. | V1 supports additive persistent cell tooling. It does not implement Docker/memory allocation, temporary environment scopes, or automatic package replacement/removal. |
| Work classification | Instructions describe bug reports, enhancements, and clarifications in the existing request text. | No required new `request_type` field and no separate workflow for each category. |
| Task context | New-session instructions explain recipes, jobs, tasks, goals, persistence, child results, rare direct validation/clarification jobs, and package-request syntax. | Resumed sessions retain the existing instruction-insertion policy. Direct submission remains subject to both task scope and token authority. |
| Submission restrictions | Read-only Codex operations explicitly deny delegated submission before effects occur. | Explicit restricted grants also withhold additional delegated secret resolution. Caller-supplied model credentials remain inputs; these nodes do not receive a general secret-fetch grant. |
| Merge/runtime recovery | No credential preflight was added. Existing candidate/approval handling remains; recoverable attempts can be repaired within their existing goal. | The recipe does not repair executor credentials, deploy a monitoring agent, or automatically restart arbitrary failures. Those actions belong to authorized operators/agents and c2j/providers. |
| Jev | Existing initial design classification remains. Feedback interpretation uses the working Codex node. | No new per-turn Jev gate was added. The plan made additional classification an evidence-driven experiment, not a prerequisite; live evaluation remains future tuning. |

## Goal semantics

The dependency contract is now:

```yaml
wait:
  on: goal
  condition: success
```

When a goal ID is available, it is the target. Older records containing only a
job ID remain usable: c2j resolves that attempt's goal. A failed attempt does not
make an open goal terminal. An authorized human or agent can correct a minor
failure and continue the same goal; the parent consumes the result from the
attempt that eventually satisfies it.

An explicitly failed goal remains a failure. The recipe also checks business
results: for example, required creation readiness, a failed validation status,
or a mismatched package config cannot be hidden by infrastructure completion.
A successful replacement goal result is not permission to skip required tests.

Monitoring entry points, confirmed against c2j main `0252e9b`:

```bash
c2j goals get GOAL --jobdb JOBDB
c2j goals candidates GOAL --jobdb JOBDB
c2j goals waits --target-goal GOAL --jobdb JOBDB
```

`c2j restart JOB --goal continue --scope SCOPE` continues the same goal using a
recorded restart scope. Recovery still requires appropriate authority and a
suitable scope; the recipe does not blindly restart an arbitrary attempt. Failed
attempt diagnostics remain useful evidence even after goal success.

Existing public field names such as `dependencies` and internal `jobs` maps are
retained to avoid an unrelated API rename. Their status records now identify the
goal and successful attempt. Validation evidence keeps the established inbox
folder convention, with `jobs/validation-<goal-id>/` for current goal results.

This replaces the proposed custom failed-attempt/replacement reconciliation ledger
for attempts belonging to the same goal. c2j already owns that relationship. Two
independently created goals are still two obligations; the recipe does not guess
that one supersedes another just because their descriptions look similar.

## What agents now return

### Consultation and execution

```yaml
next: coordinate
summary: JobDB must clarify the pagination contract before implementation.
requests:
  - action: consult
    cell: jobdb
    request: Clarification — define cursor ordering and continuation semantics.
files: []
```

After an agreement is recorded:

```yaml
next: coordinate
summary: Execute the agreed history API change.
requests:
  - action: execute
    agreement: request-2-0
files: []
```

The agreement reference comes from the supplied consultation status; the agent
does not invent it or repeat it in ordinary design/test/review responses. Request
occurrence and position produce internal references. Two requests to the same
cell remain distinct. Repeated execution of an existing reference reuses its goal.
Consult and execute requests are returned in separate turns so execution consumes
an actual recorded agreement. Legacy explicit `consultations`/`keys` remain
accepted for existing callers.

A consultation has a smaller advice-only form:

```yaml
outcome: continue
thinking: Need the storage owner to confirm the retention contract.
requests:
  - cell: pgjobdb
    request: Clarification — what retention behavior does the existing API guarantee?
files: []
assessment: not_applicable
```

Its coordinator performs the downstream consultation and resumes the original
participant. Asking for advice does not submit an implementation build.

### Packages

The working agent's system instructions contain this actual shape:

```yaml
next: blocked
summary: The required lint check cannot run because Ruff is unavailable.
packages:
  - reference: uv:ruff==0.11.2
    check: [ruff, --version]
files: []
```

The version illustrates syntax. Agents should inspect current tooling with
`c2j self`, use portable pinned `nix:`, `uv:`, or `pnpm:` references, and provide a
bounded probe as an argument array. They must not install requested tooling or
edit active package configuration before authorization.

The plan initially illustrated an array of reference strings. Implementation
uses a `reference` and `check` per entry so the exact validation command is part of
the authorization, without another parallel list or command-name guessing.
Application libraries still belong in project dependency manifests.

## Package lifecycle and policy

1. Prepare an additive candidate from the current `.c2/config.yaml`. Preserve
   comments and unrelated settings, record the original digest, and publish the
   candidate and requested checks as ordinary artifacts. Preparation does not
   install the proposed tools.
2. Consult the trusted `approved` map in
   [package-tools.yaml](../recipes/adaptive/package-tools.yaml). The map defaults
   to empty. Exact reference/probe matches are auto-approved; anything else gets
   one specific review showing requested packages, checks, and persistence.
3. Run the recipe-owned
   [package-check.yaml](../recipes/adaptive/package-check.yaml) in a child goal
   based on the current workspace. One operation adopts the authorized config in
   that child; the next runs the probes after native package preparation.
4. Wait for goal success and require its reported config digest to match the
   approved proposal. A child attempt may be repaired within that same goal.
5. Recheck the parent's original config digest, copy the exact validated candidate,
   and resume the working agent with feedback to rerun the originally blocked
   checks. A probe passing is not a claim that application validation passed.

The policy is captured with the trusted recipe, not taken from the requesting
agent's output. Operators can configure exact pairs such as:

```yaml
approved:
  uv:ruff==0.11.2: [ruff, --version]
```

A different probe for that package still needs approval. Declining a request does
not install tools; the agent receives that decision and any supplied alternatives.
A failed validation or changed parent config does not overwrite the parent config.

A package adopted in the job survives session changes through the managed config.
It becomes a default for future cell work only after the normal merge. An existing
package declaration is not added again. If an already-declared tool failed setup,
the problem belongs to runtime recovery, not repeated package approval.

c2j main now supports extension execution negotiation for resources/capabilities,
but its contract explicitly rejects `packages` in an `execution_required` request.
This implementation therefore uses existing repository package preparation rather
than claiming that negotiation can install these additions.

## Review behavior

- Final reviews use the candidate subject as the title and a direct merge/accept
  question. “Request changes” returns the exact feedback for Codex to interpret.
- `merge-review.md` is the sole primary document for acceptance. Current formal
  expectations, results, findings, and implementation detail are supporting.
- The summary author selects further evidence through identity-checked source
  annotations, including screenshots where relevant. Current verification evidence
  remains attached. Historical working documents are not automatically the final
  review bundle.
- Clarifications and interventions use the current `review.md`, or a factual
  fallback from the current explanation and actual questions. The brief tells the
  reader why they were interrupted. An existing current brief is preserved.
- Detailed file accounting belongs in implementation detail or an appendix rather
  than crowding the opening summary. Material limitations must still be visible.

These changes establish the content contract and native presentation metadata.
They do not prove that every future model-generated brief will be clear. The tests
validate routing, selection, identities, and form structure; live Codex quality
and Cortex rendering need observation after rollout.

## Validation

- **185 cases passed** across the adaptive recipe suites using c2j main `0252e9b`.
- **Two additional adoption-guard cases passed**: a changed parent config and a
  result for a different validated config are both rejected without overwriting
  the parent.
- **One additional already-declared-package case passed**: no second approval or
  child validation is launched; feedback explicitly says no new probe occurred.
  All four package lifecycle cases passed again after that feedback change.
- After the final review-title, blocker-choice, and instruction changes, the
  affected outcome/redesign, intervention, and shared-prompt cases passed again.
- Package tests exercised real native child execution and preparation of
  `uv:ruff==0.11.2`, including the probe, config adoption, comment preservation,
  and parent continuation. Separate cases cover refusal, explicit goal failure,
  exact policy matching, and changed probes requiring approval.
- Goal tests verify deduplication of two attempts for one goal and consumption of
  the successful replacement's evidence. Existing native child tests exercise
  goal waiting; an actual production failure/restart was not induced.
- The upstream c2j tests `TestSoftGoalCurrentStatusAndResultLookup` and
  `TestSoftGoalWaitPropagatesControlAndStorageErrors` also passed against the
  unchanged main checkout.
- Consultation tests cover downstream advice followed by resumption without a
  human scheduling prompt. Expectations tests compare actual artifact contents.
- New expectations are recorded in
  [coordination-review-statements.md](../recipe-tests/adaptive/coordination-review-statements.md)
  and retained as an artifact by the shared-prompt fixture.

Test setup uses the native c2j runtime with model responses mocked. A temporary
local adapter expands packaged selectors to their underlying extension op and
supplies installed Python/yq helpers instead of resolving their Nix declarations.
Requested repository packages still use c2j's real package preparation. These runs
do not claim live Codex-provider coverage or production Nix worker provisioning.
No production goal was restarted or resubmitted for testing.

Local test records: `/tmp/adaptive-implementation-final`,
`/tmp/adaptive-adoption-guards`, `/tmp/adaptive-review-final`,
`/tmp/adaptive-intervention-final`, `/tmp/adaptive-prompts-final`, and
`/tmp/adaptive-packages-final`.

## Remaining boundaries and rollout

- Publish these recipes together before consuming the new package-check recipe
  from the shared `main` selector. Historical jobs retain their captured recipes;
  changing files here does not modify those executions.
- Memory, Docker access, broader requirements policy, and temporary capability
  scopes remain outside the additive-package v1. No automatic persistent authority
  increase was introduced.
- If package preparation later fails before the parent agent can start, native
  goal monitoring must involve the execution owner. This version preserves the
  recorded proposal/work but does not implement an automatic pre-preparation
  workspace rollback or provisioning service.
- Existing bounded operator intervention for repeatedly invalid responses remains.
  The common false triggers—unchanged baselines, repeated dependency submissions,
  incoming keys, and downstream advice—are addressed directly. This does not
  promise that all operator questions disappear.
- Jev escalation/readability experiments and a live Cortex/Codex review evaluation
  remain tuning work. No new mandatory classifier was added without evidence.
- Legacy coordination fields are retained during migration. Removing them is a
  separate release in this historical plan. The later gap-closure instruction
  superseded that migration; the legacy contract has now been removed.

The implementation keeps the runtime as the authority for goals, attempts, Git,
and artifacts. Codex interprets requested outcomes and feedback; the recipe handles
execution boundaries and asks humans for concrete decisions.

# Adaptive gap closure: implementation versus plan

Implementation assessment, 2026-11-05. This follows the four plans recorded in
[PLAN_ADAPTIVE_GAP_CLOSURE.md](PLAN_ADAPTIVE_GAP_CLOSURE.md), after the instruction
to remove compatibility paths and finish the remaining recipe gaps. It supersedes
the earlier [implementation report](IMPLEMENTATION_ADAPTIVE_COORDINATION_AND_REVIEWS.md).

Follow-up, 2026-11-06: authenticated checkout exposed an incomplete permission
grant on read-only tasks. The [inheritance fix](FIX_INHERITED_TASK_PERMISSIONS.md)
records the correction and new native credential-helper regression coverage.

The four recipe changes are implemented. Coordination uses direct requests and
native history; execution failures no longer become product-review questions;
all review callers select current evidence; package decisions and failure evidence
survive subsequent turns. No live-agent quality evaluation was added.

This assessment covers the local recipe implementation. No production goals,
jobs, review answers, permissions, or remote repositories were changed. Existing
unrelated working-tree changes were preserved.

## 1. Coordination without a second protocol or state ledger

**Plan:** consume `requests` directly; remove old response fields, translation,
carried maps, and job-target fallbacks; allow independent requests in one batch;
reuse goals and prevent completion before required work succeeds.

**Implemented:**

- Removed the adaptive `requests.yaml` translation include. The agent schema no
  longer accepts `keys`, `consultations`, `next: consult`, or `next: submit`.
  Removed the consultation-only `assessment` field that existed for compatibility.
- Reworked [coordinate.yaml](../recipes/adaptive/coordinate.yaml) to process the
  requests list directly. Consultation and execution of an existing agreement can
  appear in the same response. Two requests to one cell retain separate agreements.
- Removed `threads`/`jobs` coordinator maps and prior-dependency/prior-consultation
  inputs. The parent reads completed coordinator invocations from native state
  history. The public output is now `coordination`, an array of those records.
  It is a projection of completed operations, not a separately updated status map.
- Agreement references are assigned by the recipe. Execution must reference an
  actual accepted agreement and is permitted only during implementation. Repeated
  execution uses the existing goal, including repeated references within a batch.
- A new submission returns control for independent local work. Before completion,
  outside-cell disposition, or an otherwise unexplained blocker, the parent awaits
  outstanding required goals. Consultation alone creates no execution obligation.
- Renamed the validation helper to `validation-goals.yaml`. Native `goal_ids` are
  required. There is no fallback from old job-only submission outputs. Validation
  evidence is under `goals/validation-<goal-id>/`; agreement evidence is under
  `coordination/`.
- Added [await-goal.yaml](../recipes/adaptive/await-goal.yaml), shared by dependency,
  creation, and package waits. A failed attempt can be repaired while its goal
  remains open. A successful replacement supplies the result. An explicitly failed
  goal remains blocking.

**Assessment:** matches the plan. The implementation retains the existing serving
agreement, phase, ownership, and root-creation gates. It does not replace c2j's
execution machinery. An additional correction makes creation explicit: an
inaccessible workspace returns for investigation instead of silently becoming a
root-cell creation request. A permission or transport error is not proof that a
new cell should be created.

Two native properties still mention jobs because they describe real executions:
`task.jobs` is c2j's automatic child-submission output; failed-goal
`terminalJobIds` identifies attempts whose diagnostics should be retrieved.
The diagnostic helper reads those exact attempts with `current_status` **after**
the goal is explicitly failed. Neither is a compatibility target, completion gate,
or agent-maintained list. Similarly, root build `type` remains a current CLI input:
c2j `0252e9b` injects it when submitting a workflow. Its unused inner pass-through
was removed.

## 2. Operational recovery without product-review repair questions

**Plan:** retain bounded automatic correction; turn exhausted limits and technical
blockers into recoverable attempt failures; reserve human review for explicit
product decisions and required authorization; preserve failure evidence.

**Implemented:**

- [response-repair.yaml](../recipes/adaptive/response-repair.yaml) still permits
  two automatic corrections when a safe checkpoint exists. Exhaustion or absence
  of a safe checkpoint stops the attempt with `ADAPTIVE_RECOVERY_REQUIRED`.
  It no longer offers a human retry/cancel form.
- Development iteration bounds, repeated unchanged assessment findings,
  unexplained blockers, and consultation depth/round bounds take the operational
  failure path. These conditions no longer manufacture a product question.
- The first actionable assessment finding returns to the working agent. It can
  request packages, consult an owner, revise the implementation, or name a real
  human decision. A repeated unchanged finding does not loop indefinitely.
- [operational-failure.yaml](../recipes/adaptive/operational-failure.yaml) retains
  selected documents and recovery instructions as failure artifacts. Its minimal
  reporting command runs in an empty workspace of the same registered cell so a
  broken repository package config does not prevent publishing the failure.
- Agent execution and package-check failures preserve the native cause, including
  preparation failures before the agent can start. The wrappers identify
  `AGENT_EXECUTION_RECOVERY_REQUIRED` and `PACKAGE_VALIDATION_RECOVERY_REQUIRED`.
  Cancellation remains cancellation.
- Shared recovery instructions tell an authorized operator or agent to inspect
  the goal, its candidates, actual diagnostics, and recorded scopes, repair the
  execution problem, then use `c2j restart ATTEMPT --goal continue --scope SCOPE`.
  For exhausted bounds, restart the affected work scope before the limit handler;
  restarting the stop handler merely repeats the same failure.

**Assessment:** matches the plan's native recovery approach. These paths fail the
attempt; they do not mark its goal failed, claim successful completion, or grant
new permissions. Review remains available for specific user decisions and package
approval. Exact change-request feedback goes to the working agent, which chooses
implementation versus design.

Recovery is performed by authorized humans or agents using c2j. This change does
not deploy another monitoring service or automatically repair executor credentials,
provisioning, or arbitrary provider failures. Those remain execution-owner actions;
the recipe now exposes them as operational failures with preserved evidence.

## 3. Current decision briefs and selected evidence for every review

**Plan:** require a current overview identity; create a factual current brief if
one was not supplied; attach relevant sources and mandatory evidence; remove
stale-brief selection and generic title fallbacks.

**Implemented:**

- [review.yaml](../recipes/adaptive/review.yaml) takes an explicit `overview`,
  optional current `brief`, and decision-specific `required_documents`. Its
  selection step is an empty sequence, so it creates no additional worker task.
- Without an authored brief, it generates a fresh Markdown brief from the actual
  title, questions, and current explanation. It never chooses an accumulated
  `review.md` or `merge-review.md` merely because the filename exists.
- The bundle contains that brief, its explicitly cited sources whose artifact
  identities still match, and the documents required for the decision. Unrelated
  accumulated files remain available in the story rather than being attached.
- Applied the same selection to direct questions, serving consultations, package
  approval, and final acceptance. Consultations identify briefs from the current
  response. Final acceptance retains formal expectations, results, assessment,
  implementation, and current verification evidence.
- Human questions and consultation requests must provide a title naming the
  decision. Missing titles are corrected before review. Old human `redesign`
  answers and generic fallback labels were removed. Internal agent-directed
  redesign remains a valid development transition.
- Review output contains the selected bundle plus returned user uploads. Metadata
  gives exactly one brief the primary role; other files are supporting evidence
  or diagnostics. Prompts explain the summary, recommendation, evidence, and
  reading order expected from an authored brief.

**Assessment:** matches the plan across all adaptive review callers, rather than
only final acceptance. Artifact identity checks and existing c2j review metadata
remain the mechanism. There is no additional language-model classifier or test of
whether Codex writes convincing prose. Deterministic tests establish selection,
roles, current titles, source binding, and feedback routing. Cortex rendering is
outside this recipe change.

## 4. Package decisions, diagnostics, and setup recovery

**Plan:** reuse prior decisions and validation goals; authorize changed probes;
bind actual failure evidence; adopt only the exact validated config; retain the
pre-adoption state and provide recovery if later preparation prevents agent start.

**Implemented:**

- Working-agent instructions give the concrete request shape: `next: blocked`,
  an explanation, and `packages` entries containing `reference` plus bounded
  `check` argv. Application libraries remain normal project dependencies.
- Extracted the exact reference/probe allowlist into the trusted, empty-sequence
  [package-policy.yaml](../recipes/adaptive/package-policy.yaml). The default is
  empty; an operator can configure exact approved pairs without editing the
  implementation program. Unlisted proposals require authorization before setup
  or probe execution.
- Native prior package-state outputs retain decisions. A canonical request identity
  includes the references and probes; proposal identity also includes the exact
  candidate config. An identical refusal reuses the original feedback without
  another question. An identical approved proposal reuses authorization and its
  validation goal. A changed probe or candidate requires a fresh decision unless
  explicitly covered by policy.
- Already declared tools produce a clear response that no new install or probe was
  performed. The agent is directed to inspect PATH/setup diagnostics and rerun the
  blocked check instead of repeatedly requesting the same addition.
- Validation occurs in a child goal from the recorded base. Parent adoption checks
  both the validated candidate digest and unchanged parent config. Validation
  failure leaves the parent config untouched; concurrent edits are not overwritten.
- Failed goals bind actual runtime-provided attempt artifacts under `error/`.
  Adoption failure reads native `failure.attrs.command.diagnostics`, replacing
  the ineffective `failure.artifacts` lookup. These files survive the next
  development dispatch as evidence.
- Proposal artifacts retain `previous-config.yaml`, the base identity, candidate,
  probes, and review brief. Fixed newline/NUL handling in the helper, including
  creation of a valid config when no config previously existed.
- If package preparation later prevents the parent agent from starting, the
  original failure reaches the operational recovery path. Repair the executor and
  restart the failing scope within the goal. A revised package proposal can resume
  from the recorded pre-adoption boundary with appropriate authorization.

**Assessment:** implements the planned package v1. Decisions persist through
native recipe execution history; there is no new policy database or custom retry
ledger. The pre-adoption artifact and native restart boundary preserve a recovery
path without trying to execute rollback inside the broken environment.

There is deliberately no automatic rollback, package removal/replacement,
Docker/memory provisioning, or unchecked requirement escalation. Package additions
persist in the job workspace and become cell defaults through the normal merge.
Changing the approved proposal requires authorization; a repair that leaves it
unchanged does not ask the product reviewer to approve the same work again.

## Validation

The behavioral statements were recorded before implementation in
[gap-closure-statements.md](../recipe-tests/adaptive/gap-closure-statements.md)
and are retained as an artifact by the shared-prompts fixture.

Final result: **200 distinct cases across 39 suites pass**, combining the full
regression run with focused reruns after the final consultation and goal-result
edits. No failing case remains. `git diff --check` passes.

| Plan | Principal deterministic checks |
| --- | --- |
| Coordination | Mixed actions, separate agreements for one owner, repeat execution without another submission, actual required-goal completion gates, explicit root creation, rejection of removed response fields and job-only targets. |
| Recovery | Missing/exhausted checkpoints, consultation failure, iteration limit, repeated assessment, unexplained blocker, and preparation failure produce no product review. |
| Reviews | Stale brief excluded, current cited evidence included, current files materialized, missing decision title corrected, final validation evidence retained, exact feedback returned. |
| Packages | Identical decline reused, changed probe reauthorized, approved proposal reuses its goal, actual failed-attempt diagnostics materialize, validation failure leaves parent unchanged, changed config/digest blocks adoption, real approved probe precedes adoption. |

The current-case summary and detailed runner output are retained locally under
`/tmp/gap-suite-current-summary.json` and the run directories listed there.

The checks use c2j `0252e9b` and its embedded native recipe test runner. Agent
responses and human answers are deterministic fixtures. Native orchestration,
Git operations, command diagnostics, artifact materialization, and package helper
commands execute; the approved-package case also performs actual uv/Ruff setup
and a probe before parent adoption.

For this environment, a temporary test copy expands Nix selector operations to
`extension_execution`, the same primitive used by compilation, removes live model
credentials, and uses installed Python/yq for helper commands instead of resolving
those Nix packages. Repository-declared package setup remains active. These tests
validate recipe behavior, not live Nix selector resolution or a live Codex service.
The original recipe files retain their native selectors and package requirements.

The preparation-failure regression injects a native failure to prove propagation
and absence of a review. Separate command/goal tests prove diagnostic artifact
binding. It does not claim to have reproduced every real executor failure after
adoption. No live-agent quality benchmark or Cortex visual exercise was performed,
as requested.

Run the authored suites with a configured c2j environment:

```sh
c2j test run --directory recipe-tests/adaptive --parallelism 4 --case-timeout 30s
```

No compatibility rollout or migration release remains necessary for these recipe
contracts. Existing captured executions are not rewritten; new submissions use
the updated recipes when these local changes are published.

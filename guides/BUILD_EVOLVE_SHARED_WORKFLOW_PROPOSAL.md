# Shared build and evolve workflow proposal

Status: implemented in the root entrypoints and `recipes/develop/`; see the README for invocation and runtime limitations.

## Decision

Use one development workflow, with two thin entrypoints. Both separate design,
test-plan authoring, independent test-plan review, implementation, implementation
review, verification, and human acceptance. Directory instructions supply domain
knowledge; recipes enforce the process and its gates.

| Entrypoint | Default target directory, relative to the cell root | Domain instructions |
|---|---|---|
| `build.yaml` | `.` | Applicable root and nested `AGENTS.md` files |
| `evolve.yaml` | `.c2j` | Applicable root instructions plus `.c2j/AGENTS.md` |

The target directory is resolved once per run and passed to every phase. Evolve
explains automatically that it changes the development workflows, not application
features. A missing local specialization means creating one in the target cell;
it does not mean silently switching repositories to edit the shared defaults.

c2j resolves committed `.c2j/recipes/build.yaml` and `evolve.yaml` at the target
cell's configured ref. Missing files fall back to root `build.yaml` and
`evolve.yaml` in `github.com/colony-2/recipes`. Errors do not trigger fallback.
See `/c2j/README.md`, “build and evolve”. The shared recipes repository is a
deliberate exception to the `.c2j` default: its workflow sources live at the root
and under `recipes/`. Work on those defaults uses an explicitly configured scope
in that cell.

## Recipe set

Phase files live under `recipes/develop/`:

| Recipe | Responsibility | Durable result |
|---|---|---|
| `develop.yaml` | Own lifecycle, phase routing, revision loops, and human checkpoints | Current phase, artifact revisions, session identifiers, completion status |
| `design.yaml`, `review-design.yaml` | Inspect scope, clarify requirements, author and independently review the design | `design.md`, requirements with stable IDs, scope and unresolved questions |
| `test-plan.yaml` | Define observable outcomes before implementation | `test-statements.md`, structured statement index, commands and acceptance mapping |
| `review-test-plan.yaml` | Independently assess coverage and whether tests establish the requested outcomes | Structured verdict, uncovered requirement IDs, blocking feedback |
| `implement.yaml` | Implement the approved design and tests, continuing the same implementation session on revision | Changes, statement-to-test mapping, implementation session ID |
| `review-specification.yaml`, `review-quality.yaml` | Separate specification review from quality review | Two independent structured verdicts with actionable issues |
| `verify.yaml` | Execute approved checks against the candidate revision and validate change scope | Command logs, exit codes, per-statement evidence, candidate hash |
| `finish.yaml` | Check acceptance, scope and candidate freshness, then squash merge upstream | Merge hash; human review and feedback are owned by `develop.yaml` |

Use includes for normal same-job phase composition, keeping git state and session
continuation explicit. Use child jobs for actual cross-cell or lifecycle
boundaries. Local entrypoint specializations reference the shared workflow by
selector; they should not need copies of every phase. Shared relative includes
must resolve from their source repository and pinned commit.

## Review and revision flow

1. Establish the target scope and read applicable instructions. Clarifications
   feed back into design; waiting for an answer does not complete the job.
2. Write the design, including requirements, boundaries, compatibility, and any
   deprecation plan. An independent design review returns issues to the author.
3. Author test statements and the executable test plan from that design.
4. Independently review the test plan. Rejected planning results return to the design/test-plan cycle with the prior
   results and feedback. No implementation starts through a failed gate.
5. Present the design and reviewed test statements together for human approval.
   This is one pre-implementation checkpoint, with approve/revise choices.
6. Implement and run implementation-time checks. Keep the implementation Codex
   session across review fixes and user feedback; reviewers use separate sessions.
7. Run specification and quality reviews, then independently execute verification.
   Failures return actionable evidence to implementation and trigger re-review
   and re-verification after changes. A durable human feedback step controls each retry, avoiding an unbounded
   automatic revision loop.
8. Present an outcome summary and statement-by-statement evidence. Satisfaction
   authorizes squash merge into the cell's upstream branch. Rejection collects
   feedback and continues the loop.

Feedback that changes requirements returns to design and invalidates dependent
plan approval and verification. An implementation defect continues the same
implementation session without rewriting the agreed expectations. Changed
design/test-plan revisions require renewed plan review and human approval.
Changed code invalidates evidence for the prior candidate. The merge op disables automatic rebasing; upstream advancement stops
integration so a resulting candidate cannot bypass verification.
Cancellation propagates through active work; a blocked job cannot report success.

## Test statements and contracts

Test statements are Markdown artifacts, with stable IDs and requirement links.
Each statement is at most 30 words, uses outcome language, and records relevant
filenames, importance, unit/integration level, and dependencies. Critical behavior
needs positive and negative cases. The structured index references the same
statements rather than providing independently editable duplicate expectations.

Example statement:

> TS-01: Rejecting the outcome resumes the existing implementation conversation
> without merging changes.

Annotations: critical; integration; dependencies: c2j and mocked Codex/input;
files: `recipes/develop/develop.yaml`, `recipes/develop/finish.yaml`.

The test-plan reviewer checks requirement coverage, negative cases, meaningful
assertions, feasible commands, and required environments. The implementation
cannot weaken statements merely to make checks pass. Changes to existing
behavioral expectations follow the repository's deprecation policy.

Every phase emits a schema-validated structured result plus human-readable
artifacts. Use Codex artifact output contracts and `rule_gate` for schema checks;
command checks enforce cross-reference and scope consistency. Parent transitions must require the gate
result as well as the phase verdict. Missing, malformed, contradictory, or stale
results cannot advance the workflow. An absent verification command is not a
passing test; uncovered or unverified requirements remain explicit blockers.

## Directory constraints

Keep c2j's cell worktree and git integration rooted at the cell. Build uses the
Codex op's default paths. Evolve intentionally overrides only:

```yaml
worktree_path: '{{ context.environment.op.worktree_path }}/.c2j'
```

All other Codex paths retain their extension defaults. The current c2ops code
maps this input to `Options.WorktreeRoot`, which becomes the Codex process cwd.
A disposable launcher probe passed for both `.` and `.c2j`, including default
inbox/outbox placement. It used a stub Codex executable; live instruction loading,
session resume, sandbox behavior, and c2j git persistence still need integration
coverage.

Changing cwd is a scope aid, not filesystem isolation. Resolve the target within
the cell, reject traversal and symlink escapes, and check the changed paths after
mutating phases and before merge. Include additions, deletions, and rename source
and destination paths. Out-of-scope changes block progression. Scope expansion
returns to design rather than silently broadening access.

Root `AGENTS.md` supplies common project rules; `.c2j/AGENTS.md` supplies workflow
authoring rules, standard paths, op references, test commands, and ephemeral
runtime requirements. c2j pins the expanded recipe snapshot for the run; design reads the applicable
instructions. Editing them does not relax that run's gates or change
its approved scope. Local role skills must be available from the scoped directory
or installed explicitly; changing the Codex root also changes its default skill
discovery location.

## Acceptance tests for implementation

The deterministic suite in `recipe-tests/verify-default-recipes.py` covers phase
routing, contracts, scope, evidence, and integration. Live instruction discovery,
session persistence, runtime cancellation and sandbox isolation are not claimed by
these mocked-agent tests. The sandbox limitation has a separate bug report.
All are integration tests. c2j runtime tests use disposable databases and git
repositories; none submit against a home-sourced embedded database.

| ID | Statement | Files | Importance | Dependencies / case |
|---|---|---|---|---|
| SD-01 | Build and evolve execute identical development phases with their configured target directories. | `build.yaml`, `evolve.yaml`, `recipes/develop/develop.yaml` | Critical | c2j, mocked agents; positive |
| SD-02 | Evolve starts Codex in the local workflow directory while preserving normal artifact paths and cell git persistence. | `evolve.yaml`, `recipes/develop/implement.yaml` | Critical | c2j, Codex launcher, temporary git repository; positive |
| SD-03 | Invalid artifacts or rejected design and test-plan reviews prevent implementation. | `recipes/develop/develop.yaml`, `recipes/develop/review-test-plan.yaml` | Critical | c2j, rule_gate, mocked agents; negative |
| SD-04 | Approved test statements cover requirements and precede implementation. | `recipes/develop/test-plan.yaml`, `recipes/develop/review-test-plan.yaml` | Critical | c2j, mocked agents/input; positive |
| SD-05 | Failed, missing, or stale verification evidence prevents merge despite a favorable agent summary. | `recipes/develop/verify.yaml`, `recipes/develop/finish.yaml` | Critical | c2j, real command execution; negative |
| SD-06 | Implementation feedback resumes the existing conversation and reruns review and verification. | `recipes/develop/develop.yaml`, `recipes/develop/implement.yaml` | Critical | c2j, mocked agents/input; positive |
| SD-07 | Requirement changes return to design and invalidate dependent approvals. | `recipes/develop/develop.yaml` | Critical | c2j, mocked agents/input; negative |
| SD-08 | Changes outside the approved target, including renamed files, prevent progression and merge. | `recipes/develop/verify.yaml`, `recipes/develop/develop.yaml` | Critical | c2j, temporary git repository; negative |
| SD-09 | Human satisfaction and passing gates produce one squash merge into upstream. | `recipes/develop/finish.yaml` | Critical | c2j, temporary upstream repository; positive |
| SD-10 | Editing workflow instructions cannot bypass gates already governing the running job. | `evolve.yaml`, `recipes/develop/develop.yaml` | Critical | c2j, pinned recipe fixtures; negative |
| SD-11 | Local entrypoints resolve shared phase recipes without requiring local copies. | `build.yaml`, `evolve.yaml`, `recipes/develop/develop.yaml` | High | c2j selector/include resolution; positive |
| SD-12 | Cancellation and unresolved clarification cannot be reported as successful completion. | `recipes/develop/develop.yaml` | High | c2j, mocked input and cancellation; negative |

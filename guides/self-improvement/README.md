# Improving recipes from observed jobs

Use the existing [build entrypoint](../../build.yaml) and repository skill
[audit-recipe-jobs](../../.agents/skills/audit-recipe-jobs/SKILL.md). The skill
supplies the specialized investigation method; adaptive build keeps responsibility
for phase transitions, workspaces, verification, review, and publication.
There is no separate improvement recipe or document-selection classifier.

## Choose the guidance for the task

| Work | Guidance |
| --- | --- |
| Any recipe bug fix, enhancement, or clarification | [General improvement guide](../RECIPE_IMPROVEMENT_GUIDE.md) and the [documentation map](../README.md). |
| Investigating a cohort of jobs or recurring behavior | [Audit skill](../../.agents/skills/audit-recipe-jobs/SKILL.md) and [audit method](AUDITING.md). |
| Turning observed gaps into selected changes | [Findings to implementation](IMPROVING.md). |
| Understanding why earlier choices were made | [Historical background](BACKGROUND.md), then the relevant linked audit and assessment. |

General recipe work does not require an audit. Read detailed procedures or historical
reports when they help answer the current question. The documentation map points to
existing authoring, scope, artifacts, operations, hooks, testing, review, coordination,
and recovery guides rather than duplicating their contracts here.

## Discovery and phases

The skill lives in `.agents/skills/audit-recipe-jobs`. The c2ops Codex adapter
includes the managed worktree's `.agents/skills` in its skill sources; no remote
skill installation, extra operation, or worker configuration change is needed.
Normal automatic skill selection remains enabled. [AGENTS.md](../../AGENTS.md)
provides an explicit pointer, and requests may name `$audit-recipe-jobs` directly.
See [Codex skill sources](../ops/OP_CODEX_EXEC.md#skill-source-resolution).

The adapter can install a copy outside the checkout. The skill therefore identifies
its documentation paths as repository-relative: read them from the managed worktree,
not relative to the installed copy. It is a repository skill that uses this cell's
guides, not a standalone portable bundle for unrelated projects.

During design or test planning, inspect jobs and produce the audit and plan before
implementation. The normal handoff carries selected evidence to a fresh implementation
session. That session applies the requested fixes and runs tests; assessment and human
review evaluate the result. An audit-only request stops at its findings, and a valid
no-change conclusion does not require invented implementation work. One request covers
one bounded cycle; a subsequent requested cycle can evaluate later jobs.

## Submit an ordinary build

The target JobDB, selection window, cells, visibility, constraints, and requested
outcome belong in the normal request. For example, write `audit-request.md` outside
the repository:

```markdown
Use $audit-recipe-jobs to audit job behavior and implement justified recipe improvements.

JobDB: http://192.168.1.195:9047/c2
Scope: jobs created in the 24 hours before this audit starts, across visible cells.
Include completed, failed, cancelled, active, and waiting jobs. Follow relevant
ancestors and children outside that window as supporting context.

Focus on avoidable human questions, failed child recovery, and missing evidence.
Implement recipe-owned changes with meaningful regression tests. Record c2j/c2ops
needs for their owners. Prefer existing mechanisms when sufficient; justify a
larger redesign with evidence. Do not operate on the audited jobs.

Publish the audit, selected improvement plan, and implementation-versus-plan results.
```

Then submit normally:

```sh
c2j submit --cell recipes --jobdb http://192.168.1.195:9047/c2 \
  --title 'Improve recipes from recent jobs' --prompt-file audit-request.md
```

Use `--artifact NAME=PATH` to attach a previous audit, authorized inventory, or
constraints document when useful. See [artifact submission](../C2J_SUBMIT_ARTIFACTS_USER_GUIDE.md).
Give prior reports names such as `previous-audit.md`; `handoff.md` plus
`test-statements.md` mean a complete current execution handoff to adaptive build.

The request's JobDB text does not redirect task credentials. Submit on the instance
being inspected and confirm the actual connection with `c2j self`. The skill and
guides must be present in the worker's recipes checkout; normal remote use requires
the repository changes to be published, or a supported workspace snapshot for an
unpublished candidate. Keep credentials out of prompts and documents.

## Hooks retain their existing roles

The skill and AGENTS pointer provide document discovery. Existing hooks still apply:

- `configure` can supply standing phase guidance or require design when that is a
  cell policy. It affects other builds too; this change does not force every recipe
  edit through an audit or add a classifier to recognize audit requests.
- `before_design` can collect deterministic research if a reusable collector is
  later justified. It runs again on redesign, so preserve the identified observation
  window rather than silently selecting a new cohort each time.
- `verify` runs the cell's automated checks. The current hook invokes `build.sh`,
  which checks purpose-document structure and evidence paths. It does **not** run
  native recipe suites; implementation must run and report the affected cases and
  relevant regressions. [Native testing](../NATIVE_RECIPE_TESTING.md) describes that flow.
- `prepare` and `publish` retain their normal build meanings.

See [hook authoring](../BUILD_HOOKS_USER_GUIDE.md) and
[examples](../../examples/build-hooks/README.md). No new hook is needed merely to
select reading material, and no additional audit-plan approval gate is introduced.

## Deliverables and limits

`audit.md` is the short overview; `inventory.md` supports its census and evidence.
When changes are requested, `improvement-plan.md` selects fixes, owners, tests,
deferred work, and expected effects. The existing `test-statements.md` and
`handoff.md` carry that assignment into implementation. `implementation.md` and
`test-results.md` assess changes against the plan, and the normal `merge-review.md`
presents the outcome decision. The [audit method](AUDITING.md) and
[improvement method](IMPROVING.md) provide details.

Use artifacts for cycle-specific reports; keep raw histories and downloads in scratch.
Record durable new lessons in repository guidance when warranted. The skill is
methodology, not a guarantee of model judgment. Hidden/archive discovery has
[documented coverage limits](AUDITING.md#coverage-constraints); unavailable records
must not become an invented complete census. Running jobs retain captured recipes
and sessions; merging a fix does not restart or repair their earlier handoffs.

## Validation

[Native cases](../../recipe-tests/self-improvement/build.test.yaml) exercise ordinary
build with selected audit evidence, fresh phase sessions, existing local hooks,
no-change outcomes, ordinary non-audit work, and explicit failure for essential
missing coverage. They script agent decisions; they do not test model intelligence
or access a production JobDB. The [test statements](../../recipe-tests/self-improvement/statements.md)
record the contract. Skill structure and documentation references are checked separately.

```sh
c2j test run --directory recipe-tests/self-improvement --parallelism 2 --case-timeout 180s
```

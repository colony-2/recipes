# Requirements: Live Codex Timeout Policy

## Status

Required test/recipe authoring policy. This is not currently a confirmed c2ops
product gap. The default skill-quality live smoke has been narrowed and is now
required from `recipe-tests/run-all.sh`; missing live resources or failure
signatures hard-fail the suite.

## Problem

The original broad `recipe-tests/verify-skill-quality-live.sh` failed with:

```text
job total timed out after 30m0s
```

That result did **not** mean one Codex op should take 30 minutes. The original
`skill-quality-smoke.yaml` recipe was a large live integration smoke with 17
top-level nodes, most of which invoked Codex. Logs showed many Codex ops
successfully completing and the job continuing through the recipe before the
overall run hit the 30-minute limit.

The validation conclusion is that live skill-quality coverage must stay focused,
must set explicit timeouts, and must be split into smaller required jobs when it
gets broad. It must not be skipped or hidden behind an environment gate.

## Root Cause Analysis

The original authored recipe was not an infinite loop. It was a straight
sequence with 17 top-level nodes:

- 11 live c2ops Codex calls;
- 6 `command_execution` setup/probe/assertion calls.

The Codex calls cover several unrelated skill contracts in one run:

- triage, local-cell happy path;
- triage, redirect happy path;
- requirements authoring;
- requirements good-plan review;
- requirements bad-plan review;
- implementation-plan authoring;
- implementation-plan good review;
- implementation-plan bad review;
- outcome/test-statement authoring;
- outcome good review;
- outcome bad review.

That was excessive for a smoke test. It was closer to a broad live integration
suite. The prior validation log also showed story/chapter write conflicts such
as `workflow state conflict: chapter ordinal ... already exists`. That is
separate from the thin-pack git restore bug: it is job-story persistence/replay
behavior, not git state propagation, and it now has its own bug report.

The fix is not to accept 30-minute smokes as normal. The current
`skill-quality-smoke.yaml` is focused on triage, requirements-author, and
bad-requirements contrarian-review contracts: seven top-level nodes, four live
Codex calls, and deterministic assertions. It uses explicit `c2j run one`
lease/wait timeouts and scans live logs for c2j failure signatures. It passed
TS-042/TS-043 as part of `recipe-tests/run-all.sh` on 2026-06-09 UTC. Future
implementation-planning or outcome-determination coverage should be added as
separate required phase smokes, not by expanding this smoke back into an
all-phase job.

## Goals

- Keep live Codex smokes bounded, diagnosable, and cheap enough to run.
- Set explicit timeout policy instead of relying on hidden defaults.
- Split large multi-skill smokes into smaller durable jobs where practical.
- Treat a single Codex op approaching 30 minutes as suspicious unless the recipe
  intentionally configured that behavior.

## Non-Goals

- Do not classify the observed skill-quality timeout as proof of a missing
  c2ops timeout primitive.
- Do not normalize very large single Codex prompts.
- Do not run the whole Superpowers methodology inside one Codex invocation.

## Requirements

### Requirement 1: Explicit Live Timeout Configuration

Live Codex smoke tests must declare the timeout policy they depend on.

Acceptance criteria:

- Long live jobs use `c2j run one` with explicit `--lease-duration` and
  `--wait-timeout`.
- Recipe-authored Codex nodes set the supported timeout controls available to
  the op/runtime.
- If an expected timeout control is ignored or unsupported, file a focused bug
  with a minimal reproduction.

### Requirement 2: Split Large Multi-Skill Smokes

Large smoke recipes should be split by workflow phase or contract.

Acceptance criteria:

- Triage, requirements, implementation planning, outcome determination, and
  review-contract smokes can run independently.
- Each smoke has a small number of live Codex invocations.
- A failure identifies the specific skill/phase contract that broke.

### Requirement 2a: Keep Primitive Regression Tests Focused

Default regression tests should validate one runtime contract at a time where
possible, while still running required live skill-quality coverage.

Acceptance criteria:

- Git-state restore is validated by a focused Codex mutation followed by
  deterministic command probes.
- Child artifact forwarding is validated by a focused child-job smoke.
- Story/chapter conflicts are diagnosed from focused logs before filing a bug.
- Focused skill-quality validation runs by default and hard-fails on missing
  resources, timeout, or c2j failure signatures.
- Broader multi-skill quality validation is added only as smaller
  phase-specific required smokes.

### Requirement 3: Bound Individual Codex Work

Individual Codex invocations should stay task-sized.

Acceptance criteria:

- One Codex op should usually cover one authoring task, review, repair, or
  implementation slice.
- A Codex op nearing 30 minutes is treated as a prompt/task-sizing issue or a
  possible Codex progress bug.
- Recipes preserve partial progress through artifacts and gates between Codex
  invocations.

## Superpowers Impact

This reinforces the planned Superpowers/C2 architecture:

- task jobs should remain small;
- TDD, validation, review, and planner updates should be separate states;
- long methodology validation should run as multiple smokes, not one large live
  Codex recipe.

## Validation Command

The command that exposed the issue was:

```bash
recipe-tests/verify-skill-quality-live.sh
```

Observed on 2026-06-09 UTC after the script was changed to submit first and run
with a longer c2j lease.

Current required validation:

```bash
recipe-tests/verify-skill-quality-live.sh
```

The current smoke passed TS-042/TS-043 on 2026-06-09 UTC after being narrowed to
focused triage and requirements coverage.

The focused git-state regression command is:

```bash
recipe-tests/verify-codex-skill-execution-live.sh
```

On 2026-06-09 UTC this focused command passed and did not reproduce the
thin-pack restore issue or the separate story/chapter conflict signature.

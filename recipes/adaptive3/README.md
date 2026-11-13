# Adaptive3

An opt-in development recipe built around one cycle:
**Execute → full Validate → Review**. Corrections repeat the whole cycle.
Questions stay in Review. Accepted work advances directly to the next stage.

The five stages are Direction, Preparation, Implementation, Outcome acceptance,
and Integration/publication. Direction and Outcome have human review. The other
stages use independent agent review. An accepted explanation can finish at Direction.

Use the root `adaptive3.yaml` entrypoint. `build.yaml` still uses adaptive2.

```sh
# Run the local adaptive3 source against the current cell.
c2j submit --recipe-file ./adaptive3.yaml --inputs-file request.yaml --run --embed
```

Example `request.yaml`:

```yaml
title: Keep unsent drafts after closing the tab
prompt: Preserve a draft until it is sent or explicitly discarded.
target_directory: .
require_verification: true
```

Optional inputs are `documents` (selected artifact references), `resume_from`
(a previous job to inspect), and `max_iterations` (automatic passes before
resolution; zero disables that allowance). Human discussion does not consume
these passes. A new job starts fresh agent sessions and uses inspection to
recover useful previous work.

## Reading a job

Start with the current stage's primary review document. Direction provides a
one-pager: problem, non-goals, approach, compatibility, and important questions
and answers. Outcome explains the change, other owners' work, tests, omissions,
public API changes and differences from the approved direction.

The producing agent owns the current `review/` collection. Validation checks
those files; human input receives the same references. No recipe step builds a
second review packet or overlays older files. Documents worth retaining belong
in the agent's current work; other material remains accessible through native
job inspection. Diagnostics stay in files, with concise findings in responses.

For more detail, use the [job inspection playbook](../../guides/JOB_INSPECTION_PLAYBOOK.md).
Owner questions and replies appear as task responses in the receiving cell's
workspace. The receiver writes any delivery assignment. Consultation advice is
inline; delivery uses a child adaptive3 job and a native wait.

## Recovery and local hooks

An ordinary caught failure reports `stuck` and enters the resolver in the same
job. The resolver investigates and directs a correction back to a stage's
Execute. If that correction also gets stuck, the resolver asks for human direction
before another attempt. Human cancellation remains terminal.

Configure, before-design, prepare, verify and publish retain the existing
[build hook API](../../guides/BUILD_HOOKS_USER_GUIDE.md). Hook settings artifacts
stay at that boundary. Agent prompts do not receive `build-settings.json`.
Native workspace, permission and Git operations remain responsible for isolation
and publication. Publication recovery carries the completed merge forward.

Package requests contain a `reference`, an argument-array `check`, and a reason.
The package service prepares a proposed configuration, obtains policy or human
approval, validates it in a separate job, and checks the adopted configuration.

## Source map

- `lifecycle.yaml` handles corrections, consultations and package interruptions.
- `cycle.yaml` defines a single Execute/Validate/Review pass, shared with consultation.
- `execute.yaml`, `validate.yaml`, `review.yaml` define those activities once.
- `resolver.yaml`, `consultation.yaml`, `packages.yaml` provide their services.
- `agent.yaml` owns session start/resume and native Codex calls.
- `hooks.yaml`, `integration.yaml`, `specialists.yaml` call existing extension points.
- `prompts/` and `schemas.yaml` are empty includes; they create no worker tasks.
- `tools.yaml` embeds three validators: review files, approved edits and package configuration.

See the [design](../../guides/adaptive3/DESIGN.md),
[implementation assessment](../../guides/adaptive3/IMPLEMENTATION.md), and
[tests](../../recipe-tests/adaptive3/README.md) before widening use.

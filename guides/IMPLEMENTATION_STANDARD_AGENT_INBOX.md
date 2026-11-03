# Standard agent inbox implementation

Runtime baseline: c2j main f1a153b898c57e93e9b01477d08cc02c1509ee4b (2026-11-03).
This work fits the recipes cell. Runtime log collection and capability discovery
are now implemented by c2j, and will be consumed rather than reimplemented here.

Status: implemented for the active adaptive build path. This document supersedes
the runtime feature sketches in the original proposal. The runtime baseline was
built locally as `/tmp/c2j-agent-inbox-bin`; the system-installed binary was older.

Follow-up: [direct recipe state](IMPLEMENTATION_DIRECT_RECIPE_STATE.md) removes
the internal `flow` object and moves error-file preparation to producing steps.
That report supersedes this document's internal helper descriptions; the standard
inbox and new-session instruction contracts remain in place.

Sources reviewed:

- [Execution diagnostics](https://github.com/colony-2/c2j/blob/f1a153b898c57e93e9b01477d08cc02c1509ee4b/GUIDE-Command-Failure-Diagnostics.md).
- [c2j self](https://github.com/colony-2/c2j/blob/f1a153b898c57e93e9b01477d08cc02c1509ee4b/README.md#c2j-self).
- [Recipe design feedback](RECIPE_DESIGN_IMPROVEMENTS.md).

## Contract changes from the proposal

- Forward version-2 `_c2j/execution/<node-id>.log` artifacts from command and
  extension failures. New executions do not have separate stdout/stderr files.
  Preserve readable historical version-1 references without inventing interleaving.
- Treat command outputs as bounded previews; retain successful validation evidence
  using `capture_diagnostics: always` where the recipe owns the command.
- Tell agents to run `c2j self` at task start. Permission and availability are
  separate; follow reported routes, inherited child restrictions, and task scope.
  `self` reports last-known authority, not a guarantee that an action succeeds.
- Consume automatic child-job output fields. No agent-maintained job registry.
- Keep the current hook settings-artifact contract for hook compatibility while
  removing automatic settings exposure from agent prompts and inboxes.

## Implementation sequence

1. Define integration expectations before changing recipes.
2. Introduce ordinary text artifacts for current failures, feedback, and relevant
   coordination facts. Bind current execution logs under error/. Remove flow JSON
   and repeated standing rules from prompts; use phase and repair assignments.
3. Apply the same task/context separation to reviewers and consultation repair.
4. Forward both command and extension failure logs. Preserve original hook output
   contracts; apply directory aliases only at agent consumption.
5. Authorize bounded implementation validation and consume automatic child results;
   keep no-submission restrictions for read-only reviews and serving negotiation.
6. Route empty-key blockers and actionable assessment findings to a specific
   intervention. Retain validation authority and feasibility in test-plan prompts.
   Reuse evidence only when its verified inputs are demonstrably unchanged.
7. Exercise native diagnostics and actual inbox bindings, then run the adaptive
   flow and hook/coordination regression suites. Run a bounded embedded smoke recipe
   with retained test statements and execution evidence.

## Implemented behavior

| Information | How it is used |
| --- | --- |
| Cell ownership, artifact conventions, c2j discovery | Additional instructions on new sessions; resumed sessions receive only their current task and current directories. |
| Request, target directory, phase | Ordinary task prose. No phase or last-phase file. Response repair and rebase repair select their own assignments. |
| Internal flow, counters, gates, selectors, configuration | Recipe state and CEL expressions. No workflow JSON or replacement context blob. |
| Configure-hook outputs | Selected phase prompt additions only; the existing settings artifact remains supported for hooks, excluded from default agent inboxes. |
| Current verification failures | `error/<node-id>.log` plus `error/verification.md`. Original immutable producer references remain intact. |
| Preparation failures | `error/prepare/` reports and `error/preparation.md`. |
| Successful verification logs | `verification/<node-id>.log`, with `verification.md` describing the result. |
| Historical command streams | Separate `error/legacy/` files; no invented timestamps or cross-stream ordering. |
| Missing diagnostics or required skipped checks | Readable failure text; absent logs never imply success. Cancellation still propagates. |
| Human comments and files | `feedback/human-answers.md` and `feedback/human/`; original documents remain usable for links. |
| Assessment and specialist findings | Aliases under `feedback/`, retaining originals and document identities. |
| Consultation and prerequisite facts | Small per-key Markdown summaries in `consultations/` and `jobs/`; existing agreement and outcome documents remain available. Recursive state is omitted. |
| Response corrections | `error/response-corrections.md`; consultation repair also includes the previous response as a file. |
| Rebase failure evidence | `error/rebase/` includes recovery context, saved changes, and native conflict diagnostics. |
| Direct validation children | Consume runtime `jobs.job_ids`, await completion, retain status and reported artifacts under `jobs/validation-<job-id>/`. No manual job registry or resubmission. |

The implementation assignment authorizes bounded validation from the test plan,
including c2j submissions. Runtime capability is an additional constraint, not a
substitute for that assignment. Prerequisite feature builds continue through the
existing agreement/coordinator path. Read-only review, planning, negotiation, and
response-repair tasks do not gain submission authority.

Reviewers identify a finding's owner, next action, and closure condition. Their
`next` result distinguishes implementation, validation, intervention, and completion.
Missing-evidence returns explicitly request validation while preserving code and
formal expectations. Empty-key blockers and assessment interventions request
specific human direction, with continue/redesign/cancel choices. A repeated
assessment summary against the same candidate also triggers intervention; human
direction can explicitly authorize a fresh attempt. This guard is deliberately
simple, not a semantic comparison of every finding and environmental condition.

## What the prompts look like

These are representative excerpts from the implemented templates. The wrapper
appends the actual inbox and outbox locations for each invocation. Those current
locations may be absolute; persisted log working directories are portable.

New-session additional instructions include:

```text
Run c2j self at task start for execution context, permissions, availability, routes,
and inherited child restrictions. Recheck after lease or permission failures.
Follow the task's authorization as well as runtime restrictions; ready is not a guarantee.
c2j cells lists dependent cells. Child submissions are automatically recorded in task outputs.
```

A design task from the prompt fixture renders as:

```text
Request: Preserve filters in CSV export
Target directory: services/orders

Develop design.md: behavior, responsibility, alternatives, interfaces, compatibility,
acceptance outcomes, and external prerequisites. Consult serving cells as needed. Preserve the
original request after cell creation. Return review with agreed prerequisite keys when ready.
Do not submit jobs or implement in this phase. Ask for human input only for a specific unresolved decision;
there is no routine human design approval. Use redesign for material changes in scope.

Preserve CSV API
```

An implementation return retains its implementation assignment, then adds only
applicable directions:

```text
Review the errors in the error directory and address the problems for this task.
Read the feedback directory and address the current comments.
```

A missing-validation return additionally says:

```text
This return is for missing validation evidence. Read feedback/assessment.md,
execute the assigned bounded validation, and update implementation.md and
test-results.md with results. Preserve repository code and formal expectations.
Return blocked with keys: [] if the required authority or environment is unavailable.
```

Response repair replaces the phase assignment:

```text
Correct the response using the errors in the error directory and the supplied schema.
Write missing deliverables. Do not edit repository code or change the plan.
```

## Validation results

Acceptance statements were written before implementation in
[agent-inbox-statements.md](../recipe-tests/adaptive/agent-inbox-statements.md).
The native smoke binds them between operations and retains them with its results.

- **Native runtime:** inbox materialization (9 cases), command diagnostics (4),
  extension protocol failure (1), automatic validation children (2), verification
  contracts (16), and smoke (1). All passed using the unmodified c2j binary and
  native operations, including timeout, missing evidence, required skip, and a
  process exiting zero while its extension operation fails.
- **Adaptive regression:** 140 cases across 21 suites passed in an isolated copy
  using the existing mocked agent responses and real native Git/hook/child ops.
  After the final preparation-log adjustment, the inbox cases and the 33-case
  flow suite were checked again. Two additional focused cases verify recovery
  when a missing log is bound under its success or failure alias. Prompt cases cover instruction separation,
  configuration omission, response repair, and the validation assignment.
- **Validation:** `c2j test validate --directory recipe-tests/adaptive` and
  `git diff --check` passed.
- **Self discovery:** the latest binary reported this checkout as standalone,
  with unknown submission permission and unavailable incoming-task workspace.
  No grant was inferred from that result.

The full agent-mocked suites could not resolve their published Nix packages on
this host: serial resolution stalled and parallel resolution hit an existing
tool-cache link collision. To test orchestration, a temporary copy expanded the
Nix selectors into their `extension_execution` primitive, omitted unused synthetic
secret inputs, and used installed tools in place of package resolution. This
validates recipe flow and bindings, **not** published package resolution or a real
model session. No such transport changes were made to repository recipes.

The requested direct submission was attempted with current CLI syntax:

```sh
c2j submit 'Exercise native error inbox bindings' \
  --advanced-recipe-file recipe-tests/adaptive/inbox-smoke.yaml \
  --cell <isolated-fixture-repository> \
  --artifact test-statements.md=recipe-tests/adaptive/agent-inbox-statements.md \
  --run --embed
```

It stopped before submission because the existing embedded database requires
the upstream chapter-artifact migration. The shared database was not migrated.
The same smoke recipe passed through c2j's isolated native test runtime instead:

```sh
c2j test run --file recipe-tests/adaptive/inbox-smoke.test.yaml
```

Native smoke job `3LaAOZhx6vwUQN6tWSlBQE8MAcW` captured an intentional exit-7
command and successfully materialized `error/exercise_failure.log`. Its retained
log recorded a working directory relative to worktree, the submitted script,
timestamped stdout/stderr observations, and separate process/operation outcomes.
The successful check retained `test-statements.md`, `results.md`, the failure log,
and its own execution log. Fixture reports are under `/tmp/inbox-smoke-native`;
the full regression reports are under `/tmp/inbox-regression-final`.

## Explicit boundaries

- **Verification reuse:** conservative reruns remain. Hooks do not declare all
  relevant inputs and execution conditions, so there is no safe generic identity
  for reuse. The proposal's optimization remains future work; no check is skipped
  merely because only documentation changed or a commit hash stayed the same.
- **Hook compatibility:** `build-settings.json` remains a supported hook input.
  Removing that public contract needs a separate staged deprecation. Agent exposure
  is removed now.
- **Older recipe families:** this change covers the active adaptive path and its
  helpers; legacy kernel/new-ticket families retain their existing interfaces.
- **Operational validation remaining:** rerun the standard suites with working
  published Nix packages and direct embedded submission after the existing JobDB
  migration. Runtime/package ownership belongs to c2j/c2ops and the environment.

# Recovery using selected intermediate results

Status: recipe implementation, updated 2026-11-07 against
[GUIDE-Job-Inspection.md](../GUIDE-Job-Inspection.md). c2j now documents the
inspection, artifact retrieval, and snapshot export needed for this approach.
The earlier request for a new inspection API is superseded. Recipe instructions and focused handoffs now support this path. See the
[implementation assessment](ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) for native
task-token inspection, snapshot export, and fresh-child recovery tests.

The [handoff and recovery plan](PLAN_ADAPTIVE_HANDOFF_ROUTING_AND_RECOVERY.md)
now includes initial inspection guidance and selected-output recovery. The
implemented start-again flow remains a useful fallback. Here, the parent can
preserve useful work by selecting outputs from the failed job and supplying them
to an ordinary new submission. This is selective recovery:
reuse selected work in a new execution, without restarting the old execution.

This specification fits the recipes cell's purpose. Recipes owns selection,
handoff instructions, and the recovery flow. c2j owns the inspection APIs, CLI,
task-token access, and supported artifact/change retrieval.

## 1. Intended workflow

1. The parent receives the child's terminal result through exact-job soft waiting.
2. It inspects a compact job log: which tasks ran, what failed, and which output
   fields and artifacts each task produced. Failed jobs remain inspectable even
   when they never exported final recipe outputs.
3. It reads the relevant fields and files. For example, it might select a design
   document, a patch containing unfinished implementation, and the failed check's
   command log. Selection belongs to the agent; the recipe does not need rules
   for every possible failure.
4. It submits a new job with the corrected assignment and only the selected files
   or typed inputs. The request explains what has already been done, what failed,
   and what the new job should accomplish.
5. The new job uses its normal workflow to inspect the supplied work, finish it,
   validate it, and make any required publication decisions. The parent follows
   its new native job ID and consumes its result.

The old job remains unchanged. Carry only deliberately selected files and
instructions, not the whole outbox, execution prefix, or session. A goal
relationship can describe the shared outcome without determining which execution
the parent waits for. Inspection is also useful independently of recovery when an
agent needs a specific piece of saved context.

## 2. Available capabilities and adoption work

The supplied job-inspection guide documents:

- `c2j job list`, `show`, `log`, and `story` for persisted jobs, tasks, and scopes.
- `fields`, `artifacts`, selected `log`/`result` fields, and `artifact` downloads
  for choosing and reading exact outputs.
- `snapshot` for exporting cumulative Git state and retained artifacts into a
  fresh directory, including selected task/attempt/workspace boundaries.
- `jobs.inspect` through the task helper following existing JobDB read permissions,
  including producer jobs outside the direct child chain, independently of submission.
- `recipe.await_result_soft` supplies an exact job's terminal status and available
  final outputs/artifacts. Those final outputs may be absent when execution fails
  before the recipe exports them; task inspection can still recover retained work.
- `c2j submit --artifact name=path` already attaches local files. Native recipe
  submission also accepts stored artifact references. Neither requires inventing
  a new transport format.

Use `pkg/jobinspect.API` (`Inspect` and `Download`) and its `Export` workflow for
programmatic integration. They read native persisted execution records without
recipe replay or a live worker. The documented wire/result schema is version 1.
No additional JobDB API is required for this implementation.

Recipe integration now teaches these commands, prepares focused recovery handoffs,
and binds selected attachments into the recipient inbox. The implementation was
initially validated with a locally built c2j v0.0.122 CLI/task helper. The current
pin is v0.0.124, which extends inspection to existing JobDB read permissions.
Native inspection and snapshot recovery tests passed;
[the assessment](ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) records the evidence.
This does not imply that every deployed worker has already been upgraded.

## 3. Documented CLI usage

These commands follow the supplied guide. `JOB`, `TASK`, and `CURSOR` represent
values discovered from the runtime; copy native task IDs exactly and quote them.

```sh
# In a task, list visible jobs and inspect your own saved history.
c2j self
c2j job list --json
c2j job list --parent JOB --json
c2j job log self

# Compact history and recorded scope structure for a selected job.
c2j job show JOB
c2j job log JOB
c2j job log JOB --json --limit 25 --cursor CURSOR
c2j job story JOB --json

# One task occurrence, including its output-field and artifact inventory.
c2j job log JOB --task "$TASK" --json
c2j job fields JOB --task "$TASK" --limit 25 --json
c2j job artifacts JOB --task "$TASK" --json

# Read a discovered field or the complete task output to a local file.
c2j job log JOB --task "$TASK" --field /response/summary --output summary.json
c2j job log JOB --task "$TASK" --field '' --output task-output.json

# Job-level outcome and exported-output inventory, distinct from task outputs.
c2j job result JOB --json
c2j job fields JOB --json
c2j job result JOB --field /assistant_summary --output result.json

# Download one artifact, preserving its bytes.
c2j job artifact JOB --task "$TASK" --name check.log --output ./check.log
```

`TASK` is a native occurrence ID returned by the log, not a node name or chapter
ordinal. Repeated node executions have different IDs. Use the task's `attempts`
list and `--attempt N` to select a retry; otherwise the latest attempt is used.
Omit `--task` for job-result artifacts. An exact `reference.stored.key` can be
passed as JSON with `--ref` instead of `--name`.

Field paths are examples: discover the actual output first. `--field` uses JSON
Pointer; escape `/` inside a key as `~1` and `~` as `~0`. Empty `--field ''`
selects the whole output. Missing is distinct from null, false, zero, or an empty
string. These reads preserve original types rather than using truncated previews.

An illustrative default view:

```text
Job child-123: failed — cell example
Failure: verification exited with status 1
Final recipe result: not produced

Task    Step             Status      Available outputs
task-a  implement        succeeded   response; implementation.md; changes.patch
task-b  verify           failed      exit_code=1; check.log

Use --task to inspect an occurrence, then read a field or download an artifact.
```

The task inventory should provide:

| Information | Use |
| --- | --- |
| Native occurrence handle, node path/title, task type, cell, attempt | Identify the operation and distinguish repeated executions. |
| Status, available start/finish times, failure code/message | Explain what happened, including setup failures before an operation ran. |
| Output field names, types, sizes where known, bounded previews | Let the agent choose what to read without receiving large bodies. |
| Artifact name, type, size where known, producer, native reference | Locate exact files and pass references through existing submission APIs. |
| Availability and pagination information | Distinguish missing results from partial inventory, withheld data, or an unfinished task. |

Omit inapplicable optional fields. Do not return a large object of empty context
fields. Keep full inputs, rendered variables, resolved recipe YAML, credentials,
and internal session objects out of the default view. Ordinary output fields must
retain their original types; a missing field is different from `false`, `0`, an
empty string, or an explicit `null`.

## 4. Retrieval behavior to preserve when integrating

**Bounded discovery, exact selected reads.** Discovery defaults to 25 entries and
allows at most 100 per page. Continue with the returned cursor. Summaries cap
inventories; use `fields` and `artifacts` for paginated discovery. Terminal JSON is
limited to 256 KiB; save large exact values with `--output FILE`. Output files are
created exclusively, and failed downloads remove their partial files. Prefer
scratch files over dumping complete outputs or binary artifacts into the prompt.

**Useful failure coverage.** Include completed and failed task occurrences when
the enclosing job fails or is cancelled. Report preparation failures even if no
application output exists. Support running-job inspection, distinguishing pending
outputs from absent outputs. Stable handles must survive subsequent task updates.
Do not assume an old, hidden, deleted, or archived job is readable merely from its
ID; access and retention determine what inspection can actually return.

**No dependency on replaying the workflow.** Reading persisted task outputs must
not execute commands, require a live worker, or resolve a newer recipe revision.
If full story reconstruction is unavailable, expose the stored task information
that can be decoded and identify the incomplete portion.

**Faithful files and diagnostics.** Downloads preserve bytes, filename information,
and provenance. Command diagnostics retain c2j's command, repository-relative
working directory, timestamps, and stdout/stderr representation. Do not replace
the original command log with a generated summary. Default retrieval is individual
files; no archive or extraction step should be required.

**Clear failures.** Distinguish unavailable, not yet produced, expired, and denied
data as far as the access policy allows. Prevent accidental local overwrite and
unsafe filename traversal. A reported artifact reference whose bytes cannot be
retrieved must not appear as a successful download.

`story` is a persisted scope view, not a replayed or reconstructed UI story.
`completion_not_recorded` does not mean a scope is still running, and a running
task may have no recorded result yet. Inspection pagination bounds returned
inventories; the documented backend still loads history before projection and
buffers remote artifacts internally. Keep inspection targeted rather than using
it as a continuous polling mechanism.

## 5. Access from an ordinary agent task

The documented task helper allows inspection of the **current job and direct
children**, including terminal children, for the lifetime of the task. Reads are
independent of submission permission. `c2j self` advertises `jobs.inspect`; the
CLI uses the task's authenticated connection. Standalone `--jobdb` or `--embed`
selection does not bypass task access scope.

This lets a parent recover its failed child's work and lets an agent retrieve its
own earlier outputs. It does not promise access from a child to its parent, a
sibling, or a grandchild. A nested coordinator should retrieve its own children's
work and return selected artifacts through the normal handoff. Changing to a
different cell workspace does not make another job's session available.

Include the compact initial-context wording in item 9 of the
[main plan](PLAN_ADAPTIVE_HANDOFF_ROUTING_AND_RECOVERY.md), including for advisory
and review sessions. Inspection is optional and does not require an approval
exchange. Required files should still be deliberately delivered. If a specific
read is denied or unavailable, report the missing input and continue useful work.
Do not implement a recipe-owned chapter parser or broaden access just to make
implicit document dependencies work.

## 6. Supplying selected work to the new job

The first version can download chosen files and use the existing submit flags:

```sh
# The preceding inspection commands saved these selected files locally.
c2j submit --cell example --recipe-file ./repair.yaml \
  --inputs-file ./request.json \
  --artifact design.md=./design.md \
  --artifact error/check.log=./check.log \
  --artifact changes.patch=./changes.patch
```

This illustrates the existing submission mechanism, not a new generic repair
recipe. The chosen recipe must explicitly bind the submitted artifacts from
`context.artifacts` into the task's inbox or use its existing typed document inputs;
an attachment does not automatically appear in every operation's inbox.

Where the caller already has a native stored reference, reuse the existing typed
artifact submission path. A CLI convenience for attaching such references can
avoid a download/upload round trip later, but it is not required for the initial
feature. Do not introduce a separate artifact manifest protocol.

Prefer the normal execution request and coordinator for actual recipe recovery.
Prepare `work/<assignment>/handoff.md` and only the selected supporting files.
Explain their source job/task/attempt and what was verified in concise Markdown;
do not create a second machine-readable recovery manifest. Preserve native
references when rebinding existing artifacts. The coordinator uses the existing
`documents` binding path, records the replacement job, and durably waits for it.

**Unpublished code has a documented snapshot export.** A commit ID alone cannot
transfer unpublished changes. `--from-workspace` refers to the submitter's
workspace, not the failed child's. Use c2j's exporter when code recovery is useful:

```sh
c2j job snapshot JOB --task "$TASK" --json
c2j job snapshot JOB --task "$TASK" --workspace SCOPE_ID --dir ./recovered
git -C ./recovered/worktree diff --binary refs/c2j/base HEAD > changes.patch
```

Select the relevant workspace from snapshot metadata. A single-workspace export
has `snapshot.json`, `worktree/`, `artifacts/<producer>/attempt-N/<name>`, and Git
bundles. Multiple workspaces use paths under `workspaces/`; read the returned
paths instead of assuming `worktree/`. Keep the export in scratch outside outbox.
The last command illustrates a single-workspace export with a recorded base.

Snapshots contain **cumulative** state and retained task artifacts through the
selected boundary, not only the selected task's changes. `after` is the default;
`--boundary before` requires a task. Without a task selector, export uses the
latest successful task state in each workspace. Explicitly selecting a failed
attempt can expose saved diagnostic Git state labelled `failed_attempt`; it is
not an accepted candidate. Inspect the repository, cell, workspace, base/target
hashes, and provenance recorded in `snapshot.json` before choosing what to reuse.

The exporter verifies the saved bundle and obtains exact prerequisites through
existing Git credentials. It creates a new directory and never updates an
existing checkout or substitutes today's branch tip for unavailable saved state.
An empty-base export has no `refs/c2j/base`; use its exported files/checkout as
appropriate rather than blindly running the diff example. A required missing or
external artifact can make a complete directory export fail; individual artifact
reads and snapshot metadata remain available. A useful published patch can be
retrieved even when no usable Git export is available.

Select the useful patch, files, and diagnostic logs from scratch into the new
handoff. Do not attach the whole snapshot directory, every historical output, or
internal session objects. In the const-task incident, discarded worktree edits
are not recoverable as committed Git state merely because inspection exists;
the explicitly published implementation patch is the useful saved work.

The new job reads the supplied changes, applies or adapts them in its own managed
checkout, and validates the result. Receiving an artifact does not automatically
restore Git state or certify that prior work is correct. If no usable code export
is available, say so and use the current fresh-start path.

Example recovery handoff prompt:

```text
Complete the original assignment. Relevant work from an earlier failed job is
in inbox: design.md describes the intended behavior, changes.patch contains
unfinished implementation, and error/ contains the failed verification output.
Inspect and reuse the supplied work where useful, address the failure, and run
the required checks. The patch is input to review and apply; it is not already
installed in your checkout. This is a new job with its normal completion process.
```

The exact filenames in this example describe a selected handoff. General shared
prompts should continue directing agents to standard inbox directories, without
generating a list of every diagnostic file.

## 7. Acceptance and adoption

These are adoption checks, not claims that this recipe integration has passed.
Paths identify the documented c2j inspection service or recipe boundary. Each
expectation is at most 30 words.

| ID | Importance | Level / dependencies | Files / area | Expectation |
| --- | --- | --- | --- | --- |
| IR-01 | Critical | Integration / failed native job | c2j `pkg/jobinspect/` | A failed job without final recipe outputs exposes completed task outputs and available failure diagnostics. |
| IR-02 | High | Integration / repeated tasks and retries | c2j `pkg/jobinspect/` | Repeated node executions have stable distinguishable handles, and paginated discovery does not silently omit occurrences. |
| IR-03 | Critical | Integration / large outputs | c2j CLI and `pkg/jobinspect/` | Discovery stays bounded; an explicitly selected field can be exported exactly with its original type. |
| IR-04 | Critical | Integration / artifacts and native submission | c2j artifact service; recipes `coordinate.yaml` | Selected artifact bytes reach the new job unchanged; unselected files and session state are not carried forward. |
| IR-05 | Critical | Integration / ordinary task token | c2j task permissions and CLI | A parent task reads its child's results and artifacts without administrative access; unrelated restricted jobs remain inaccessible. |
| IR-06 | High | Integration / preparation failure and unavailable recipe source | c2j `pkg/jobinspect/` | Stored failure information remains inspectable without executing tasks or requiring the original worker and recipe source to remain available. |
| IR-07 | Critical | Integration / unpublished changes | c2j change export; recipes `coordinate.yaml` | A new job can recover selected unpublished changes without fetching an unavailable commit or inheriting the parent's unrelated workspace. |
| IR-08 | High | Integration / cancellation and missing artifacts | c2j `pkg/jobinspect/`; recipes `coordinate.yaml` | Inspection leaves the source job unchanged and reports unavailable bytes accurately; cancellation never initiates recovery by itself. |
| IR-09 | Critical | Integration / multiple workspaces and Git | c2j snapshot exporter; recipes recovery tests | Recovery selects the intended workspace and cumulative boundary without mixing repositories or assuming a failed attempt was accepted. |

Validate the documented c2j capabilities with a current worker CLI/task helper,
then exercise the recipe boundary with real failed jobs and selected outputs.
Update the recipe's fresh-submission path to accept the focused handoff and add
an end-to-end failed-child-to-new-job test. Include multi-workspace snapshots,
an explicitly selected failed attempt, missing bytes, and unavailable parent or
sibling access. A later writable task must observe the applied code; an attached
patch or a successful inspection response is not sufficient.

Keep ordinary new submission and exact-job waiting as the control flow. Failed
retrieval does not force recovery to stop: start again from the corrected handoff
when that remains useful. Do not duplicate an active execution or treat explicit
cancellation as an automatic recovery request. Before enabling the feature,
record which tested c2j release and worker helper provide these commands; do not
leave a requirement for an inspection API that the supplied guide already provides.

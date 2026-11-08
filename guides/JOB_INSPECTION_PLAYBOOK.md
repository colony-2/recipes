# Inspect a job without guessing its outputs

Use inspection to answer a specific question: what failed, what a task produced,
or which saved work is useful. These commands read persisted records; they do not
execute or replay the job. Routine inspection does not require a human decision.
The adaptive recipe includes this guidance in each new agent session.

## Find the job and task

Inside a task, `self` selects the current job. `c2j job list --json` lists
backend-visible jobs in the selected tenant; `--parent JOB` selects direct
children. `c2j self` reports `jobs.inspect`. Reads follow existing JobDB read
permissions for the task, independently of submission permission, including
parent, sibling, unrelated, and terminal jobs. Use the supplied task connection.
Do not infer a denial from a job's relationship to the current job.

For a missing input, follow producer job/task/artifact references in the handoff
first. Discover the task and select the required file; do not copy every document
or ask the human to locate something already retained. If access is actually
denied or bytes expired, preserve that exact result. A report can record specific
unavailability when its assignment permits it; a required unresolved input goes
back to the coordinator. Neither case proves the underlying product works.

```sh
JOB=self                         # Or a known producer job ID.
c2j job show "$JOB" --json
c2j job log "$JOB" --json
```

Read task paths, statuses, errors, and attempts. Set `TASK` to the exact `id` of
the relevant entry. Node names and chapter numbers are not task selectors.
Quote the ID; repeated executions of a node have distinct IDs. If needed,
`c2j job story "$JOB" --json` gives the recorded execution scopes.

## Discover fields, then retrieve values

```sh
c2j job log "$JOB" --task "$TASK" --json
c2j job fields "$JOB" --task "$TASK" --limit 25 --json
```

These return details and bounded previews. The field inventory gives top-level
`pointer`, `type`, `bytes`, and `preview` values. Set `FIELD` to the returned
pointer you need, then retrieve the exact value into an unused scratch path:

```sh
c2j job log "$JOB" --task "$TASK" --field "$FIELD" --output selected-value.json
```

Pointers address the task's output, not the inspection envelope. There is no
universal `/response/summary` field. If the inventory shows `/response` as an
object, retrieve that object to discover its members. If it is a string containing
JSON, retrieve `/response` and parse the string locally; JSON Pointer cannot
traverse inside a string. A missing path is a query to correct, not a reason to
ask the user how the recipe works.

For a complete task output when needed:

```sh
c2j job log "$JOB" --task "$TASK" --field '' --output task-output.json
```

`--field ''` selects the root value. JSON Pointer escapes `/` in a key as `~1`
and `~` as `~0`. Missing output differs from valid `null`, `false`, `0`, or `""`.

## Retrieve the relevant file

```sh
c2j job artifacts "$JOB" --task "$TASK" --json
# Set NAME to the exact returned artifact name, including any directory prefix.
c2j job artifact "$JOB" --task "$TASK" --name "$NAME" --output check.log
```

The local filename need not match the stored name. Inspect the failed task's
error and available command diagnostics; inspect earlier tasks for useful work
that completed before the failure. Select files for the question at hand.
Without `--task`, artifact commands address final-result artifacts, not the
combined artifacts of every task.

## Inspect final results when available

```sh
c2j job result "$JOB" --json
c2j job fields "$JOB" --json
# Set FIELD to a pointer discovered in this final-result inventory.
c2j job result "$JOB" --field "$FIELD" --output result-value.json
```

The first two commands show availability and inventories; the last retrieves
an exact value. Final recipe outputs have their own shape, distinct from task
outputs. `/summary` is an example, not a required field. Running or failed jobs
may have no final output. Inspect recorded tasks instead; absence is neither
success nor proof that no useful work was saved.

## Keep inspection focused

- Follow `next_cursor` with `--cursor` on the same inventory command when needed.
  Pages default to 25 entries, with a maximum of 100.
- Use `--attempt N` consistently across task details, fields, artifacts, and
  downloads when selecting a retry. Otherwise the latest attempt is used.
- Download to scratch outside the managed checkout and outbox. Output paths must
  not exist. Large exact values require `--output`; previews can be truncated.
- If access is denied or bytes are unavailable, report the exact missing evidence
  and continue independent work. Ask the human only for a necessary decision they
  can resolve. A working agent with an essential unmet need and no useful correction
  returns `next: fail` to end the attempt; an investigation may instead finish with
  documented unavailability if its acceptance permits that result.
- If the only remaining work is child completion, return `next: wait`. Repeatedly
  inspecting unchanged history does not advance the work.

For recovered code, use the [selective recovery workflow](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md):
export a snapshot into scratch, select useful artifacts or an explicit patch,
and supply a corrected handoff to a fresh job. Downloading or attaching a patch
does not apply it; the next writable task reviews, applies, and retests it.

Validated with the repository's pinned c2j v0.0.124. The native
`recipe-tests/adaptive/inspection-recovery.test.yaml` exercises task discovery,
exact fields, missing-field handling, failed-task diagnostics, artifact downloads,
snapshot recovery, parent artifact retrieval without submission permission,
selective file delivery, and final outputs using task credentials.

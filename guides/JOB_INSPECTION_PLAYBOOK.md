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

## Choose a restart point

The command contract below was reviewed at c2j source commit
`11574b555465d1558754b436f68ef5c7ac0912ff`; it is not a claim that newer commands
are deployed on your route. The pinned-version validation above covers task
inspection and snapshot recovery.

Use native restart when rerunning an eligible scope with its recorded execution
prefix addresses the problem. Use selective snapshot salvage (above) to recover
saved files into a fresh execution, reviewing and retesting the selected patch.
Recipes `resume_from` carries prior approval and scope after the recipe checks
the actual decision and original assignment; it restores neither history nor
files automatically. Preserve those checks and the receiver's handoff.

The prior approval and receiver-authored handoff may belong to an earlier parent.
Inspect that attempt's latest status and human feedback before selecting files.
Use `replaces` for the unsuccessful attempt and `resume_from` for the job holding
approval when they differ. The coordinator waits for active work and reuses a
successful result; it does not import the earlier parent's coordination history.
Consult when the assignment changes or agreement is unclear, rather than merely
to recreate records. The receiving build still checks approval against the current
assignment. See [adaptive2 recovery guidance](../recipes/adaptive2/README.md).

Check `c2j self`, actual command help, and matching task helper capability on the
supplied route. Parent help or a successful exit alone does not establish support:
older CLIs may print parent help for an unknown command. Check that help actually
describes the requested command and flags. Source support does not prove that
the CLI/helper is deployed. On supported versions:

```sh
c2j job restart-points "$JOB" --json
```

This returns the complete `restart_scopes` list, without pagination. Keep the
source job with an exact returned `scope_id` lacking `unavailable_reason`.
Use chapter, path, title and time to distinguish repeated visits and choose the
smallest suitable eligible enclosing scope. Task IDs, node names, statuses,
timestamps and guessed ordinals are not selectors. Eligibility comes from
recorded restart boundaries, not successful completion. Discovery does not
guarantee retained bytes, replay compatibility or submission authority.

If discovery is unsupported, record precise unavailability. `c2j job story
"$JOB" --limit 100 --json` can inspect history; follow `next_cursor` with
`--cursor` on the same query. Its paginated inventory cannot certify restart
eligibility; `completion_not_recorded` is not a restartability flag. When
necessary, request a matching supported CLI/helper route through the coordinator
or operator. Otherwise choose a separately suitable recovery mechanism. Never
guess selectors or bypass the helper.

When context matters, enter scratch outside checkout/outbox and choose an unused
output path (downloads do not overwrite files):

```sh
c2j job restart-context "$JOB" --scope "$SCOPE" --output before.json
```

Missing retained recipe/history bytes can prevent reconstruction even after
successful discovery. Respect `redacted_paths`. Artifact, object and configuration
references remain references; neither a context snapshot nor redaction
placeholders are reusable patches. Detailed typed patch authoring belongs in
c2j's [restart context guide](https://github.com/colony-2/c2j/blob/main/GUIDE-Restart-Context.md).

Discovery permission and submission authority are separate. Inside tasks, use
the authenticated helper even with explicit connection options; do not fall back
to direct credentials. Submission requires suitable `jobs.submit` authority,
source-cell access, a valid controller owner lease and compatible hook policy.
Inherited hook policy may block restart to preserve its ceiling. Route denial to
the authorized coordinator/operator without credential workarounds. Routine
reads need no new approval ritual.

Only with authority and compatible command/helper support:

```sh
c2j restart "$JOB" --scope "$SCOPE" --request-id "$REQUEST" --goal continue
```

Save the complete returned continuation identity and follow its status/result;
submission alone is not recovery. It is an independent job: discover its own
restart points before selecting a further restart. `continue` is the default
and shares the source goal; `--goal new` creates a new goal. Neither cancels nor
rewinds the source. Identical retries, including after a lost response, reuse
one request ID for the same source, selection, goal and payload. A changed source,
selection, goal or payload requires a fresh request ID; retries do not edit an
existing continuation.

Explicit `--chapter ORDINAL` selection is version dependent: check actual help
first. Where supported, select exactly one scope or chapter; chapter zero is
submission. Multiple scopes in one chapter require an exact returned scope ID.
Never substitute a task ordinal, subtract from an ordinal or construct scope IDs.

A recipe-scope restart retains the recorded prefix before the selected scope,
including preceding setup/resolution and durable state. Later work and current
live edits are not automatically retained; tasks and external effects may repeat.
Submission restart retains original submission inputs/artifacts and the owning
cell snapshot, discards later execution and patches, and reruns setup, recipe
resolution and hooks. Floating references may resolve newer content; pinned or
embedded recipes remain as submitted. Intentional recipe changes favor fresh
execution with explicit source selection rather than assuming restart loads edits.

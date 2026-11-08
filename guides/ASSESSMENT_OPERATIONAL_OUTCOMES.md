# Operational outcomes: implementation versus plan

Implements [PLAN_OPERATIONAL_OUTCOMES.md](PLAN_OPERATIONAL_OUTCOMES.md), based on the
[November 7 audit](AUDIT_ALL_JOBS_2026-11-07.md). This is a targeted adjustment to
adaptive build, its shared prompts, and its regression tests.

## Changes against each planned outcome

| Plan | Implementation | Validation |
| --- | --- | --- |
| Finish the assigned investigation | Planning defines acceptance for the child's deliverable. Execution and assessment distinguish a completed report of findings/unavailability from successful product behavior or parent recovery. Parent-wide expectations belong in supporting context. | A full build with scripted investigation outputs completes as `unchanged`, with its normal outcome review and no operational question. Its report explicitly leaves parent recovery unresolved. |
| Retrieve existing evidence | Initial context and the inspection playbook follow recorded producer job/task/artifact references. Removed the obsolete parent/sibling prohibition. `.c2j-version` advances from 0.0.122 to released 0.0.124, whose task inspection follows existing JobDB read permissions. | A real child task with job submission disabled finds and downloads one required parent output absent from its inbox. An unrelated parent artifact remains unselected. Native task/output discovery and download checks still run. |
| Distinguish saved code from published dependencies | Handoffs identify producer references and publication state. Prompts explain selected snapshot patches for bounded validation and source-publication ordering for ordinary Git/module consumers. | The existing native recovery case exports a failed child's unpublished snapshot, selects a patch and one useful file, and applies them in a fresh child's managed workspace. Parent checkout isolation and replacement tracking remain checked. |
| End unsuccessful attempts | The response schema accepts `next: fail`. After normal response validation, this routes directly to operational failure, before child recovery, package handling, or human questions. Summary and selected files survive. Reworded blocker summaries no longer reset the consecutive correction counter, and reworded negative assessments of the same candidate enter recovery. Changed candidates and intervening successful work still permit progress. | Schema validation accepts failure. Full builds stop on explicit failure both before and during recovery. Four differently worded blockers exhaust three correction turns; a separate case covers repeated reworded assessments. Five candidate-changing corrections can continue. Existing recovery-progress tests remain regression coverage. |
| Avoid failure export collisions | Removed the generic generated `recovery.md` and its unused prompt. Failure export has one document binding and preserves the supplied documents; the failure itself carries the explanation. | A real failed command's retained `recovery.md` and nested evidence log are retrieved through job inspection and compared byte-for-byte. The original failure code/reason remain intact. |
| Keep environments and reviews scoped | Planning, execution, and assessment follow latest human scope decisions, distinguish product deprecation from correcting a generated validation plan, defer excluded checks, and prefer compatible installed tools. Existing package policy/probes remain the path for required packages. Prompts direct exhausted operational needs to the parent and prohibit repeating an already answered question. Review overviews explain outcome, decision needed now, and changes since approval. | Existing package, feedback, review, expectation-protection, and shared-prompt rendering suites cover the supported routes. These are prompt guidance changes rather than new heuristic classifiers or extra human gates. |

## Test evidence

The new acceptance statements are in
[operational-outcomes-statements.md](../recipe-tests/adaptive/operational-outcomes-statements.md).
The principal additions are
[operational-outcomes.test.yaml](../recipe-tests/adaptive/operational-outcomes.test.yaml)
and [failure-export.test.yaml](../recipe-tests/adaptive/failure-export.test.yaml).
The existing intervention, schema, and native inspection/recovery tests were extended.

Validation uses a locally built CLI and task helper from **c2j v0.0.124**, commit
`33e2a4de4e99d3a577a38dca4b8de33d43a099ce`. No c2j source changes were made.
The environment's Nix store is exposed through the existing local test wrapper;
agent/Jev decisions are scripted, while command execution, artifacts, Git state,
child jobs, and job inspection use the real embedded runtime.

**Full adaptive regression: 296 cases passed across 61 suites; zero failures.**
The final run exited successfully on November 8, 2026. Seven cases were added;
existing intervention and native inspection cases were extended. This includes
full build lifecycle, expectation protection, review revisions, native Git/merge,
consultation, packages, failure diagnostics, and durable child waiting.

```sh
c2j test run --directory recipe-tests/adaptive --parallelism 2 \
  --case-timeout 180s --out-dir /tmp/operational-adaptive-final
```

Local run reports are in `/tmp/operational-adaptive-final`; the command log is
`/tmp/operational-adaptive-final.log`. `git diff --check` also passed. The published
npm release's `gitHead` matches the source commit recorded above. This is the
adaptive regression suite, not a claim that unrelated creation/live-service
suites were rerun. No live model or production job was exercised.

## Practical limits

The mechanical fixes are deterministic: failure routing, counter behavior, artifact
preservation, and the exercised inspection paths. Acceptance scoping, necessary
environment choices, review clarity, and whether a retry has a useful correction
remain agent judgments guided by the revised prompts. The tests establish that
the recipe handles those decisions; they do not measure model judgment quality.

No new automatic provisioning, publication, review bypass, global recovery budget,
or document accumulation was introduced. Package policies still decide their own
approval rules. The parent still decides whether corrected inputs, code, environment,
or evidence of a transient failure justify a fresh attempt.

Existing live jobs keep their captured recipes and session instructions. This
change does not repair already omitted handoffs or resume, resubmit, or answer
those jobs. New sessions using this recipe receive the updated context. The
inspection behavior requires workers with the supporting c2j version; an actual
denial or expired artifact remains a concrete unmet input to report.

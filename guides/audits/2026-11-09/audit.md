# Recent recipe audit: missing screenshots and avoidable recovery work

The clearest remaining recipe bug is **review assembly dropping existing
screenshots**. Asking the implementation agent to take them again does not fix
the selector that later leaves them out. The existing assessment should check
visual evidence, and the assembled review needs a check that its linked images
are actually attached.

This is an audit and proposal only. No recipes, tests, or observed jobs were
changed. See the [concrete plan](improvement-plan.md), [job inventory](inventory.md),
and [selected evidence](evidence.md).

A separately requested follow-up found an additional current-recipe bug:
**approved recovery assignments restart in read-only design**. Job `0NUMMlLN…`
was created after the frozen window and is recorded below without changing the
44-job cohort or its counts.

The recommendations also incorporate the
[screenshot proposal](../../screenshot-improvement-plan.md) and
[limit-escalation proposal](../../adaptive2/PROPOSAL_LIMIT_ESCALATION.md).
Their proposed behavior is distinguished from the observed job findings below.

## What was inspected

- JobDB: `http://192.168.1.195:9047/c2`.
- Jobs **created** from **2026-11-08 19:11:11 UTC through 2026-11-09
  19:11:11 UTC**. This window stayed fixed during inspection.
- All 44 jobs in that window, including 11 Cortex jobs and 13 hidden jobs.
  The census included both active and archived stores. Six older parents were
  supporting context, outside the denominator.
- The initial census contained 14 successful, 18 failed, one cancelled, and
  11 unfinished jobs. Unfinished meant six ACTIVE, four READY, and one
  PENDING_JOBS; it did not mean failed. One READY job resumed during inspection.
- Read all 44 task inventories, selected task outputs, human replies, review
  forms and their documents. Retrieved screenshot bytes and visually inspected
  representative execution-tree, timeline, and goals-filter captures.

The failures are not a useful delivery rate by themselves: the cohort mixes
feature work, investigations, package checks, and helper probes. One helper
completed successfully while correctly reporting a failed hosted check.

### Most jobs did not capture the latest fixes

| Captured recipes revision | Jobs | Meaning |
| --- | ---: | --- |
| `1c7cdc74` | 2 | Latest human-turn budgets and accepted-handoff recovery fixes |
| `610a59bb` | 36 | Adaptive2 before those fixes |
| `33f64742` | 3 | Older adaptive |
| `a3fea1fc` | 1 | Older adaptive |
| Inline helper recipe | 2 | Verification probes |

The latest JobDB recovery, `3LsmdOIA…`, succeeded by verifying that replacement
work was already published, avoiding duplicate implementation. The latest
Cortex recovery, `3LsmZNU…`, was still recovering its inputs and consulting
owners. There is not enough production evidence yet to judge the new fixes.

Three older failures belong to the already-addressed handoff/turn-limit family:
`7f7199c5…`, `BA8QGnX…`, and `6d44f0e7…`. Their retained corrections demand
original receiving-cell artifact identities; agents repeatedly tried to supply
the accepted assignments. The first two exhausted their old iteration limits.
The third eventually returned failure after concluding the delivery contract
could not express the required references. Do not count these as regressions
of `1c7cdc74`. The [implementation assessment](../../adaptive2/turn-limits/implementation.md)
describes that fix.

## Screenshots: produced, described, then omitted

Four clearly visual Cortex changes reached merge review in this cohort. Of
their seven review forms, **five contained no PNGs**. The latest packet for
three of the four changes omitted screenshots.

| Change / job | Merge reviews | What happened |
| --- | --- | --- |
| [Execution tree](https://jobs.colony2.com/c2/jobs/1f72f9d9e783e9a9722c0c861a1af01b) | Both missing images | Human asked for attachments. Agent recovered four screenshots and said they were attached. The revised form still contained none. |
| [Lease timeline](https://jobs.colony2.com/c2/jobs/WZ9xJfKBfxGFhnNadct9jb3IQSX) | Both missing images | Human said “Need screenshots before merge.” Agent produced four captures and a gallery. Assessment said screenshot evidence was complete. The open form attached the gallery, but none of its images. |
| [Root-goals filter](https://jobs.colony2.com/c2/jobs/6a70318940363160d26f63d5323b8fb2) | First had images; second did not | The first form attached two phone captures. A later summary dropped them from the selected sources while continuing to link them. |
| [Review-panel scrolling](https://jobs.colony2.com/c2/jobs/7ca74bfa70249331df08ea6b8330fb49) | Images attached | The primary brief directly selected two PNGs, and both reached the form. |

The inspected images show implemented browser UI, not mockups. The timeline
captures use HTTP fixtures and explicitly do not establish live deployment or
authentication. The execution-tree review identifies older captures and their
limits after subsequent repairs. Those distinctions should remain visible.

The compact-job-ID change is a useful exception: its report explains that the
change affects submission payloads, not appearance. Requiring screenshots for
every Cortex change would create unnecessary work.

### Why repeated prompting failed

1. Agents can publish PNGs, declare them in `files`, and link them in Markdown.
2. The [review selector](../../../recipes/adaptive2/review.yaml) only includes
   the primary brief, required documents, and the primary brief's **direct**
   annotated sources. It neither follows sources transitively nor examines
   Markdown image links.
3. In the timeline case, the primary brief selects `screenshots.md`; that
   gallery selects four PNGs. The second hop is lost. In the execution-tree
   case, the brief and evidence index link PNGs that are not selected directly.
4. [Artifact validation](../../../recipes/adaptive/artifact-result.yaml) checks
   declared `files.*.path`. It does not check whether a review's links will
   resolve in the final form. Unresolved `source_paths` also do not cause repair.
5. [Assessment and summary validation](../../../recipes/adaptive2/inspect.yaml)
   checks response shape and required documents, not the final attachments.
   An assessor can truthfully see images in its inbox that the human never gets.

These paths are unchanged in the current checkout at `1c7cdc74`. The evidence
supports a recipe defect independently of any possible Cortex rendering bug.
I did not test the deployed browser's rendering of a correctly assembled form.

The current summary prompt already asks for actual UI screenshots. Adding that
sentence again would not repair the delivery boundary. There is also a smaller
prompt gap: implementation and assessment do not clearly make visual evidence
part of UI acceptance, so a missing gallery can pass without a focused request
to capture one.

The incorporated screenshot proposal makes the check broader: **every local
file link in every selected review document must resolve to a retrievable
attachment**, including nested galleries, supporting documents, and logs. Keep
selection explicit and return omissions for correction; do not automatically
copy arbitrary files or excuse broken links because the target exists in an
earlier task. Judge required visual evidence from the actual change, even when
the brief omits any mention of screenshots. Missing capture capability needs
concrete recovery feedback, not approval merely because the absence is disclosed.

## Other remaining issues

### Approved recovery restarts in design and cannot proceed

Follow-up job
[0NUMMlLN6YlOv34xXc4sQcW2AKo](https://jobs.colony2.com/c2/jobs/0NUMMlLN6YlOv34xXc4sQcW2AKo)
was created at **2026-11-09 19:46:37 UTC** in cortex-assistant, under parent
`18f1949f…`. It used **`1c7cdc74`**, including the latest fixes. It failed after
two agent turns, not because of a turn cap.

The receiving-cell handoff supplied approved design/test documents and explicitly
said not to repeat direction review. However,
[build's start transition](../../../recipes/adaptive2/develop.yaml) always enters
design. Its prompt demanded a one-pager and approval, and its agent operation
used `const: true`. The agent reported applying a recovery patch and then asked
to execute the already-agreed c2ops dependency. The coordination validator
rejected execution because the current phase was not `implement`.

The agent could neither advance to implementation through its response schema
nor honor the handoff by reopening approval. It returned `next: fail`, and the
recipe recorded `ADAPTIVE_RECOVERY_REQUIRED`. The patch application did not
persist in managed Git: the following task saw the original clean base. The
8,302-byte recovery patch and supporting evidence survived as artifacts; no code
was merged.

This is a recipe routing and approval-carryover gap, separate from the repaired
artifact-identity and human-turn-budget bugs. An accepted recovery assignment
needs an explicit route into a fresh writable implementation session, carrying
the prior approval and acceptance documents. Prose saying “continue implementation”
cannot change phase, permissions, or Git persistence. See the
[proposed route and regression checks](improvement-plan.md#resume-approved-work-in-implementation)
and [recorded evidence](evidence.md#follow-up-approved-recovery-starts-in-read-only-design).

### Recovered candidates can fail configuration before an agent starts

Two c2j recovery attempts, `3LquN99…` and `3LquYc2…`, restore the old child's
candidate at `ff47456e…`. Their explicitly declared configure workspace resolves
`main` at `4a07de54…`. There is no configure hook in that resolved tree, yet the
shared guard compares the two hashes and reports “Read-only hook changed the
candidate.” The outer gate replaces that cause with “Configuration hook failed.”

This is supported by the recorded workspace resolutions, absent-hook result,
and current recipe code; it has not been independently reproduced in a new
native test during this audit. The same-cell workspace is being reselected at
the wrong boundary. This also risks checking a different checkout from the one
being recovered. Fix inherited workspace handling and preserve the real error.
The existing [workspace-pinning report](../../BUG_REPORT_BUILD_EXPLICIT_WORKSPACE_PINNING.md)
describes a related problem; intentionally separate workspaces still matter.

### Approval reuse misses unchanged edits within a changed upstream file

The goals-filter job was approved, rebased, and approved again. I downloaded
both candidate diffs. Their path-scoped additions and removals are identical;
the only textual differences are blob hashes and nearby unchanged context where
an upstream test was renamed. Assessment also reported no additional feature
changes.

[Candidate comparison](../../../recipes/adaptive/git-candidate.yaml) hashes
whole before/after blob identities. That survives changes to unrelated files,
but not unrelated upstream edits inside a file this candidate also edits. The
fallback assessment has no route to reuse the existing approval. Keep the exact
digest fast path, and handle this narrower equivalence case explicitly. Matching
added/removed lines alone is not a general proof of semantic equivalence.

### Scope still grows before existing capabilities are checked

Human corrections repeatedly reduce work the agents introduced:

- Goals filter: “We don't need new jobdb storage”; parent relationships already
  exist.
- Compact IDs: wrong backend assumptions, then a browser-ID proposal, before
  the actual submission path was established.
- Lease timeline: human removes identity work from the assignment.
- Cortex assistant: six direction reviews; the human asks for a simple recipe
  conversation loop without c2j changes, then explicitly defers permissions.
  The last correction had just arrived; this audit does not claim it was ignored
  in a subsequent response.
- vz-macos API work: repeated review of additional placement abstractions that
  the human wanted removed from the public API.

Use the existing one-pager and receiver consultation to establish the smallest
missing behavior from actual code/API evidence. Carry human exclusions into
revised receiving-cell assignments. These are judgment/prompt improvements,
not a reason for another workflow redesign or a new classification model.

### Environment failures need a changed prerequisite

Nine failed jobs fall into related environment/dependency groups: three
macOS-executor failures, two missing developer-local Apple dependency failures,
one uncached c2ops Nix-output failure, and three failed package probes. These
are correlated parent/child outcomes, not nine independent root causes.

- Several macOS requests execute on Linux ARM64 without the Apple SDK or
  signing tools. Editing configuration does not by itself move the current
  task to a different executor. Requiring successful native execution before
  permitting the configuration that selects it creates a bootstrap problem.
- `/Users/tmc/go/src/github.com/tmc/apple` is a missing machine-local dependency.
  Its owner needs to make the intended source consumable.
- Two package probes try `flake:go_1_25` / `flake:go_1_26`; corrected probes later
  succeed. These are invalid package references, not unavailable Go versions.
- c2ops verification reports required Nix outputs are uncached while builds are
  disabled on the executor. That needs an environment/provider change.

The recipe should distinguish a correctable package spelling from a missing
executor or unpublished dependency, and return that concrete need to its parent.
Several jobs already do this honestly and avoid unchanged retries; preserve it.

### Some recovery assignments ask the child to operate the controller

`UmjkVQ…` and `3LqtNo…` ask ordinary build tasks to fence or recover another
parent's continuation. They stop because the required interface is not exposed
and their current task cannot submit the demanded job. That is different from
ordinary source implementation.

The parent should retain orchestration and submit a fresh, concrete owner
assignment with selected recovered evidence. Do not fix an impossible controller
assignment by broadly granting permissions to read-only design tasks. Several
of these parents captured older recipes, so repair the handoff as well as using
a new recipe revision.

### Checks worth following separately

- Cortex verification encountered browser failures in five cohort jobs. Several
  recovered or reached review; reports retain flaky cases and skips. Do not
  turn every failed check into a failed-job count or silently bless flakes.
  The repeated browser assertions belong with Cortex's test owners.
- The recipes verification child reached GitHub and received an actual 401.
  Its report also identifies 18 creation-test failures under retained harness
  constraints. Those claims need credential/test-owner follow-up; they are not
  evidence that screenshots could not be produced.
- `3LsSrj…` reports a verification scope “timed out after 0s” even though recorded
  command tasks succeeded. The retained report and task sequence establish a
  suspicious scope-level failure, not its cause. Capture the runtime scope
  failure before assigning it to a recipe timeout or changing source tests.
- A consultation in `6d44f0e7…` used `iter1/consultant/work/handoff.md` as a Git
  `ref`, causing a real workspace-resolution failure. Clarify Git-ref versus
  handoff-directory fields and keep the original resolution error in repair
  feedback; a ref cannot be validated with a rule banning slashes.

## Additional proposed policy: limits should pause for direction

The [limit-escalation proposal](../../adaptive2/PROPOSAL_LIMIT_ESCALATION.md)
addresses current terminal behavior at automatic implementation and
response-correction limits. It is based on source review, not additional jobs
in this cohort. It covers development, consultation response correction, and
review preparation, including equivalent retained adaptive paths.

Instead of failing solely because an allowance was exhausted, preserve work and
ask the human what to do next. Explain the goal, attempts, unresolved issue,
tradeoffs, and saved work in ordinary language. Offer concrete supported choices,
including a larger bounded allowance when another attempt is possible. A waiting
child should remain waiting, not trigger replacement work. Failed brief synthesis
must still produce a usable deterministic decision from retained facts.

This does not change which turns count as autonomous work, authorize invalid
reports, extend runtime deadlines, or soften unrelated operational failures.
It also does not fix `0NUMMlLN…`: that job was in the wrong phase, and another
allowance would leave the phase mismatch intact. The
[integrated plan](improvement-plan.md#ask-for-direction-when-an-automatic-allowance-is-exhausted)
keeps the two changes separate and describes their regression coverage.

## What is working and should stay

Native merge and rebase recovery completed useful deliveries, including the
execution-tree and scrolling changes. Selected partial-output recovery let a
replacement JobDB job finish work from a capped child. Explanation-only requests
can finish without a merge review. Package probes can reveal a bad selection
before another implementation attempt. Human design review caught real scope
errors, even though it currently makes the human do too much diagnosis.

The proposed work strengthens evidence delivery, workspace continuity, and those
existing review/recovery loops. It does not need a new adaptive recipe generation.

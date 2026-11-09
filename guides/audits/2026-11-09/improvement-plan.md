# Proposed fixes after the November 9 audit

Implementation is recorded in [implementation.md](implementation.md) and
[test-results.md](test-results.md). This document preserves the agreed plan.
The [audit](audit.md) explains observed behavior and limits. Start with screenshot
delivery, approved-recovery routing, and recovered workspaces, then approval reuse.
Add a human decision when an automatic allowance is exhausted, using the limit
proposal below. Keep normal assessment and review in their existing phases.
The recovery-routing recommendation comes from a separately requested post-window
job, `0NUMMlLN…`, running the latest recipe.

## Incorporated proposals and decisions

This plan incorporates two complementary proposals requested after the audit:

- [Screenshot improvement plan](../../screenshot-improvement-plan.md): judge
  visual evidence from the actual change, preserve explicit artifact selection,
  and recursively validate **all local file links in selected review documents**.
  This replaces this plan's earlier suggestion to automatically add images or
  expand the source graph. Missing attachments go through existing correction;
  a gallery alone is insufficient under the current direct-source selector.
- [Limit escalation](../../adaptive2/PROPOSAL_LIMIT_ESCALATION.md): exhausted
  automatic work or response correction should preserve work and ask for a
  concrete decision, including a bounded larger allowance when retry is possible.
  This is a source-based policy proposal, not an additional observed failure in
  the frozen job cohort. The linked document retains the detailed examples and
  acceptance statements.

The proposals meet at review repair: missing screenshots or broken links trigger
normal correction first; exhausted corrections trigger a comprehensible decision,
not a broken review or an automatic terminal failure. A grant of more attempts
does not waive evidence, approval, phase, or publication requirements.

## Make UI evidence part of the existing assessment

**Bug fix and clarification — recipes.** Change
[adaptive2 prompts](../../../recipes/adaptive2/prompts.yaml), using the existing
[assessment → validation route](../../../recipes/adaptive2/develop.yaml).

Suggested implementation guidance:

> For a visible UI change, capture the implemented screens and important states
> at the relevant desktop or phone sizes. Put the images in outbox and link them
> from a short screenshot section or gallery. Say what each image demonstrates
> and identify fixture data. Inspect the images before calling them evidence.

Suggested assessment guidance:

> If this changes what a user sees or how they interact with the UI, check the
> actual screenshots against the changed behavior. Check that the review links
> to them. If images are missing, unreadable, or do not demonstrate the change,
> request a specific correction through validation. Reuse existing captures when
> they still apply; do not require new images merely because the commit changed.

Use the agent's understanding of the diff and requested outcome, not a filename
heuristic, a README's mention of screenshots, or a new mandatory `is_ui_change`
field. A nonvisual change or explicit human exemption can pass with an explanation.
Design mockups and unrelated test-failure screenshots do not establish implemented
behavior. Preserve enough capture context to judge applicability to the candidate.

If capture needs a missing browser/package, use the existing package or recovery
path. Record the attempted command and concrete environment failure; merely
disclosing missing required evidence does not make the change ready for approval.
Retrieve applicable retained captures before rerunning the application. Do not
require production deployment or all browsers unless the assignment calls for it.
A screenshot request is not a new feature or another routine human approval.

**Regression checks:** a scripted assessment rejects a missing visual example
and reaches writable validation; its returned PNG reaches the eventual form.
A nonvisual change can pass without screenshots. Scripts verify routing, not
the quality of an LLM's visual judgment. After implementation, run a small real UI
example and inspect the resulting human review.

## Validate every local link in the selected review packet

**Bug fix — recipes; Cortex only if a correct packet still fails to render.**
The timeline case is an exact reproduction fixture:

```text
merge-review.md → screenshots.md → four PNGs
```

1. Keep [review selection](../../../recipes/adaptive2/review.yaml) explicit.
   Under the current selector, the summary declares each selected image and
   lists it directly in `merge-review.md`'s `source_paths`, even when the prose
   reaches it through a gallery. Keep current artifact identity checks and
   required documents. Do not silently attach files found in the repository,
   an earlier task, or the output directory.
2. During existing summary/accounting validation, evaluate the **same selection**
   that will reach the form. Check every selected review document and follow its
   local links transitively through supporting documents, galleries, images, and
   logs. Each referenced local file must be present and retrievable in that final
   document map. Metadata, file declarations, and producer inventories alone
   cannot establish this.
3. Parse supported Markdown links, reference-style links/images, and supported
   embedded HTML link/image markup. Ignore examples inside code. Resolve targets
   relative to the referring document's attachment path, normalize `.`/`..` and
   encoded filenames consistently with the viewer, and separate query/fragment
   suffixes from artifact lookup. Fragment-only links need no new attachment;
   external URLs are outside this check. Never read arbitrary filesystem paths
   to satisfy an attachment link.
4. For a missing, unreadable, or ambiguous target, report the referring document,
   original link, resolved path, and useful link chain. For example:
   `merge-review.md → screenshots.md → evidence/desktop.png: missing from review attachments`.
   Feed this through existing bounded inspection repair. Select the exact retained
   artifact, retrieve missing evidence by producer reference, or correct the link.
   Use the existing writable validation task when a new capture is needed. Do not
   remove required evidence merely to make the checker pass.
5. Keep selection and checking together: summary validation and final form
   construction must use the same selector, so later filtering cannot invalidate
   a successful check. A shared selection helper can prevent divergent preview
   and publication behavior. Reuse the existing accounting agent with a
   deterministic attachment check; no new routine model or human review.

This needs code as well as prompts. CEL metadata selection alone cannot read a
stored Markdown document. Use a small read-only native check over the selected
bound artifacts, integrated with the current inspection repair, for link/content
validation. Do not add a new parallel manifest for the agent to maintain.

Every local evidence link is a promise that its target will be attached. This
includes links in supporting documents and to optional diagnostics: optional
reading does not excuse a broken published link. A repository/scratch path or
earlier producer artifact is not an attachment. Where the intended citation is
external source code, use a real external source link or plain path notation;
do not reinterpret a broken local link as a source citation to pass validation.

Use a visited set for cycles. Reject escapes from the attachment namespace.
If a resource limit prevents a complete check, report incomplete validation
instead of silently passing. Preserve meaningful links and applicable screenshots
through revised and rebased reviews; regenerate images only when their visual
evidence is stale. Do not attach whole evidence trees or every historical image.

If automatic correction exhausts its allowance, use the
[limit decision](#ask-for-direction-when-an-automatic-allowance-is-exhausted).
The decision concerns how to obtain a usable review; it cannot approve broken
attachments or silently waive required screenshots. Stable browser/font
provisioning can be investigated by Cortex/c2ops if it recurs, independently of
fixing the confirmed selection defect.

**Native regression checks, using actual stored artifacts and final input forms:**

| Case | Required result |
| --- | --- |
| Overview directly references a PNG | Image is attached and resolves under the referenced name. |
| Overview selects a gallery but its four PNGs are omitted | Correction identifies the missing images; revised selection includes all four. |
| Markdown references an available image without selecting it | Correction selects its exact retained reference before the form is shown. |
| Screenshots are present but a local document or log is omitted | Publication waits for correction of that link too. |
| Final summary is rewritten after rebase | Still-referenced images survive review assembly. |
| Human requests missing screenshots | The revised form actually contains the recovered/generated images. |
| Referenced artifact is unavailable or unreadable | Repair runs before the merge review; no unsupported success claim. |
| Nested relative, encoded, reference-style, or supported HTML links | Targets resolve exactly as attachment paths in the viewer. |
| External URLs, fragment-only links, and code examples | Create no additional attachment requirement. |
| Duplicate basename, stale reference, or cyclic links | No incorrect attachment or infinite traversal; useful repair when needed. |
| Validation exceeds its resource allowance | Reports incomplete validation rather than passing the packet. |
| Ordinary review with unrelated logs/images in inventory | Unrelated artifacts stay out. |

Extend [adaptive2 native cases](../../../recipe-tests/adaptive2/README.md) and
the review/artifact suites. Assert both attachment identities and document-link
resolution. Existing “required overview exists” assertions do not exercise this
failure. A Cortex rendering test can then consume the assembled gallery and
verify visible images, rather than testing only a hand-built fixture.

## Resume approved work in implementation

**Bug fix — recipes.** Job
[0NUMMlLN6YlOv34xXc4sQcW2AKo](https://jobs.colony2.com/c2/jobs/0NUMMlLN6YlOv34xXc4sQcW2AKo)
received an approved execution assignment but entered read-only design, lost a
patch application from managed Git, and was blocked from executing its agreed
dependency. It used `1c7cdc74`; another fresh submission alone would repeat the
same route. See the [evidence](evidence.md#follow-up-approved-recovery-starts-in-read-only-design).

1. Add an explicit approved-recovery entry mode to the build input contract and
   [workflow routing](../../../recipes/adaptive2/workflow.yaml). The coordinating
   recipe supplies it with selected references to the prior approval, receiving
   assignment, design, acceptance statements, and useful recovery artifacts.
   Carry workflow state deliberately; do not infer approval from words in a prompt
   or let an arbitrary agent statement bypass design review.
2. In [develop's start transition](../../../recipes/adaptive2/develop.yaml), check
   that the approval and required acceptance documents are available and apply
   to the selected assignment. For unchanged approved scope, enter implementation
   with a fresh session. Recover missing records by producer reference first.
   If approval cannot be established, retain the ordinary design path; if scope
   materially changed, use the existing direction-review path for that change.
3. Supply implementation instructions only on that route. Reuse the existing
   writable agent operation, package handling, dependency execution, verification,
   assessment, and merge review. Apply the selected patch normally and rerun
   checks in the actual candidate. Do not reuse old test results as proof of the
   recovered checkout, force-reset Git, or disable read-only behavior for design.
4. Update the coordinating submission path to pass the entry mode and approval
   references when it sends this kind of recovery assignment. Inspect ordinary
   accepted execution handoffs for the same mismatch; do not assume every
   consultation agreement is also a human design approval.
5. If these inputs are incomplete, return the specific missing approval/document
   through existing repair/recovery. Do not send the agent through a loop that
   simultaneously forbids another approval and requires one to advance.

This needs recipe contract and transition changes, not only prompt tuning or a
new c2j restart API. Keep source recovery, approval carryover, and writable
execution aligned; all three must survive the new-job boundary.

**Native regression checks:**

| Case | Required result |
| --- | --- |
| Approved assignment with design, tests, and saved patch | Starts writable implementation without another direction review. |
| Implementation applies the recovered patch | A subsequent real managed-workspace task sees the changes. |
| Recovered implementation requests its agreed dependency | Coordination accepts execution in the implementation phase. |
| Agent reports prior tests passed | Current verification still runs before publication. |
| Approval is missing, unrelated, or claimed only in prose | Cannot silently bypass the ordinary design path. |
| Recovery introduces a material scope change | Existing direction review addresses the changed scope. |
| Ordinary new feature or read-only consultation | Retains its existing phase and read-only persistence rules. |

Extend the native build/handoff-recovery cases with the parent submission and
child phase transition. Use real artifact references, approval records, and Git
persistence; mock only model decisions and human responses. A test that checks
the handoff text or patch availability alone would miss this incident.

## Ask for direction when an automatic allowance is exhausted

**Behavior change — recipes.** Incorporate
[PROPOSAL_LIMIT_ESCALATION.md](../../adaptive2/PROPOSAL_LIMIT_ESCALATION.md),
including its acceptance statements LE-01–LE-15. A limit means automatic work
must pause, not that the requested outcome is impossible or complete.

Replace terminal exhaustion in adaptive2's `autonomous_limit`,
`response_repair_exhausted`, consultation response correction, and inspection
correction with a focused shared escalation helper. Apply the same policy to
equivalent **retained** adaptive paths, without reviving removed workflows.
Keep continuation with the owning loop. Do not globally replace operational
failure handling or extend consultation debate/depth, unchanged-blocker, Git,
creation-review, or runtime time/execution limits in this change.

**What the human sees:** a descriptive title such as “Importing contacts needs
your direction,” and a primary brief explaining the goal, progress, materially
different attempts, why work paused, the unresolved issue, concrete choices
with tradeoffs and a recommendation, and what work is saved or still running.
Describe attempts as work passes or report corrections, not time estimates.
Distinguish a product disagreement from a mechanical reporting problem. Never
ask the human to repair JSON or interpret an internal state name.

Offer only supported, task-specific choices: continue for another bounded round;
increase the allowance with old and new counts shown; try a named different
approach; change a stated scope/constraint through normal planning and owner
agreement; or stop and retain the unfinished work. Include a larger allowance
when more attempts are possible. Missing continuation context or uncertain side
effects may make direct retry unavailable; a larger number does not repair them.

Use native review input with a required single choice and optional feedback.
There is no timeout approval or automatically submitted recommendation. Invalid
or contradictory answers require clarification before further work. If a custom
allowance needs another field, use a supported follow-up form rather than assuming
the input operation provides conditional or numeric widgets.

**Concrete state and allowance rules:**

- Retain the current phase/assignment, approved scope, session, managed Git state,
  selected original artifact references, rejected responses, issues, attempt
  history, and active child identifiers in normal inputs/outputs. Do not rebuild
  continuation from an invalid report or synthesized brief.
- A bounded read-only synthesis step prepares the brief. Authoritative counts,
  supported actions, and continuation stay with the recipe. If synthesis fails,
  show a deterministic brief from retained facts and valid choices; do not enter
  another correction loop just to explain the exhausted one.
- “Continue with five” grants five new eligible passes. “Increase from five to
  ten” grants ten new passes for the next round, not five extra or ten lifetime
  passes. An increase must be a finite positive integer above the current
  allowance. Do not offer unlimited retry; configured `max_iterations: 0` keeps
  its existing disabled meaning.
- Response correction defaults to two retries. An increase from two to four
  grants four further corrections of that unresolved response. Count completed
  corrections, excluding the original invalid response. It grants no permission
  to implement, weaken acceptance, or accept an invalid report.
- An override is for one round: it expires at the next genuine human decision
  or completion of the affected correction episode. Later unrelated episodes
  use their defaults. Preserve lifetime attempt history separately from the
  current-round count. Asking, preparing the brief, and processing the answer
  consume no granted attempts.
- Persist the displayed choices, selected action, allowance, feedback, and native
  receipt. Replay must not grant another allowance or duplicate child work.
  Propagate receipts from inline consultation and inspection to their callers
  wherever human-response accounting occurs. Merely displaying a form or seeing
  the same receipt again does not renew a budget.
- A child awaiting direction remains unfinished; its parent waits rather than
  replacing it. Inline helpers propagate the decision through the caller without
  duplicate questions. Already-running siblings are not implicitly paused or
  resubmitted. Stopping follows existing child-cancellation policy and preserves
  results without merging or presenting incomplete work as successful delivery.

Verify actual runtime waiting, cancellation/ticket outcomes, and deadline
behavior. A recipe output labelled `cancelled` is not proof of runtime
cancellation, and a larger recipe allowance does not extend runtime deadlines.
Missing support belongs to c2j/c2ops; do not simulate it with polling or scripts.
The fallback brief should attach only known readable evidence, so broken review
links cannot send escalation back into the exhausted repair loop.

This complements the approved-recovery fix; it does not replace it. `0NUMMlLN…`
failed on its second agent turn in the wrong phase. More attempts would not make
that session writable. Fix phase routing independently, and retain ordinary
validation, verification, and merge approval after every continuation decision.

**Regression checks:** use the detailed LE-01–LE-15 expectations from the linked
proposal, covering exact grant counts and expiry, repeated exhaustion, all three
correction contexts, malformed answers, synthesis failure, receipt replay,
parent/child waiting, stopped outcomes, preserved phase restrictions, and healthy
work below its allowance. Use real native input, artifacts, Git, and lifecycle
behavior with scripted model decisions. Include screenshot-link correction
exhaustion as an integration case; increasing corrections must not bypass the
attachment check. Document the changed terminal-behavior expectations explicitly.

Inspect real decision packets for converging work, a genuine scope conflict,
and a purely mechanical report failure. Scripted tests do not establish whether
the explanation is useful. Changes apply to newly captured recipes; they do not
migrate or revive existing jobs automatically. No new public correction-limit
configuration is needed for one-round human grants.

## Keep a recovered candidate in the same owner workspace

**Bug fix — recipes, with a native c2j boundary test.** In
[adaptive2 workflow](../../../recipes/adaptive2/workflow.yaml), ordinary
`configure` and `run` should inherit the current owner-cell workspace instead of
resolving the symbolic ref again. Audit equivalent shared-build declarations.
Preserve deliberate foreign-cell consultations, upstream inspection, and
publication at an exact merged commit.

Keep the read-only hook guard, but compare before/after within the same managed
candidate. Propagate the actual configure failure and its diagnostics through
`configuration_gate` instead of replacing everything with “Configuration hook
failed.” Do not remove the guard to make the two observed failures disappear.

**Regression checks:** restore a candidate different from upstream, enter build
with an absent configure hook, and preserve that candidate through first
implementation. Repeat with a successful read-only hook. A hook that genuinely
mutates the candidate must still fail. Test normal fresh-workspace refresh and
intentional cross-cell isolation as controls. Git and workspace operations must
be real, not mocked hash strings. See the earlier
[workspace report](../../BUG_REPORT_BUILD_EXPLICIT_WORKSPACE_PINNING.md).

## Reuse approval when only upstream context changed

**Bug fix — recipes.** Keep the existing exact digest fast path in
[candidate inspection](../../../recipes/adaptive/git-candidate.yaml). Add a
comparison path for a digest mismatch caused by upstream changes in the same
file, using the existing prior approved candidate and diff.

The observed case has identical local edits and a renamed neighboring upstream
test. Compare file-scoped change hunks and relevant context, retain mode/binary/
rename significance, and let the existing assessment identify conflict repair
or behavioral changes. When equivalence is established and verification passes,
the develop state machine should reuse the prior human approval. If the change
is materially different or equivalence is uncertain, retain the focused change
review referencing the approved brief.

Do not use an agent's unstructured “same scope” sentence as sufficient proof,
and do not equate identical added/removed lines with universal semantic equality.
Do not add hook fingerprints to the approval decision.

**Regression checks:** same local patch plus changed neighboring upstream text
does not ask again; a conflict repair changing behavior does; mode/binary changes
still count; failed verification cannot use approval to bypass repair. Reproduce
the goals-filter pair from [the evidence](evidence.md) with real Git history.

## Reduce invented prerequisites in design and consultation

**Clarification — recipes.** Adjust the existing one-pager, consultation, and
assessment prompts to establish:

- What the cell already provides, based on inspected code or APIs.
- The smallest missing behavior needed for this request.
- The human's explicit exclusions, carried into any revised receiver-authored
  assignment.

For example: “Parent relationships are already stored; expose and use that data
for the filter,” rather than proposing another storage project. Keep source
acceptance distinct from future deployment hardening when the human excludes it.
Challenge a proposed dependency with concrete evidence before spawning its job.

Clarify that request `ref` is a Git branch/tag/commit, while `handoff` names
artifact content. Keep real ref-resolution errors in repair feedback; support
valid branch names containing slashes.

**Validation:** preserve exclusions and corrected receiving-cell assignments
through native handoff tests. For prompt effectiveness, review a few actual
resulting one-pagers; text assertions or scripted “good agent” replies do not
prove reasoning quality. Do not add a special new classifier or machine taxonomy.

## Make environment and recovery needs actionable

**Targeted enhancement — recipes plus the owning runtime/application cells.**

- Package requests: show resolvable package-reference examples. A bad reference
  should return its exact setup error for correction. Preserve the current
  approval-before-execution policy; parsing a reference is not authorization to
  execute an arbitrary new package.
- Base/capability requests: confirm the deployed c2j requirements/suspension and
  workspace-submission behavior, then use that mechanism for a fresh probe after
  approved configuration changes. Separate source/configuration validation from
  execution checks that require the proposed environment. Do not assume editing
  `.c2/config` changes the running task's machine.
- Missing local dependencies and unavailable Nix realizations: return the exact
  source or realization needed to its owner. Avoid another identical child
  until a prerequisite changes.
- Recovery assignments: keep parent orchestration in the parent. Ask owner cells
  for source work, explanation, or validation they can actually deliver. Carry
  selected recovered artifacts into a fresh job; do not require ordinary build
  tasks to fence/restart another parent's internal continuation.

**Regression checks:** malformed package selection repairs without losing the
approved intent; incompatible executor reports a concrete unmet need; unchanged
prerequisites do not produce replacement loops; configuration-only work can be
validated without claiming native runtime acceptance. Runtime capability tests
need the corresponding c2j/executor support and cannot be proven by recipe mocks.

Keep the GitHub 401, missing Apple source, repeated Cortex browser failures, and
reported zero-second scope timeout as separate owner investigations. The timeout
needs a retained runtime failure before assigning a cause. These should not be
folded into a screenshot fix or used to justify broader task permissions.

## Order and completion criteria

1. Fix screenshot capture expectations and final attachment delivery together.
2. Add approved-recovery routing into writable implementation, carrying prior
   approval and acceptance documents across the parent/child boundary.
3. Fix inherited workspace handling and configure diagnostics.
4. Add bounded limit decisions for implementation and response correction,
   including inspection/consultation callers and retained adaptive equivalents.
5. Extend approval reuse for the confirmed same-file upstream-context case.
6. Tune existing design/consultation prompts and package/recovery feedback;
   consult runtime owners only for missing environment capabilities.

Run focused native regressions, then the affected adaptive2 and shared artifact,
review, workspace, approval, and retained adaptive suites. Generate a real UI
review packet and representative limit-decision packets; inspect them as a human
would. Report implemented versus deferred work explicitly.

The next audit should look for complete screenshot packets without human
reminders, approved recoveries that reach writable implementation without renewed
design approval, no false configure mutation failures on recovered work, useful
limit decisions that retain work without bypassing validation, fewer repeat
approvals of unchanged edits, and fewer invented prerequisites. Measure final
review packets, not counts of producer PNGs. Judge jobs that captured the new
recipe separately from older parents and children.

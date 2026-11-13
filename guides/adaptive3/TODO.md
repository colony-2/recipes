# Adaptive3 follow-ups

- [x] **Allow human-directed model and reasoning changes.** Add optional job inputs
  `model` and `reasoning_effort`. For each field, use the latest human-directed
  override, then the job input, then the c2ops config default (`codex_model` or
  `codex_reasoning_effort`), otherwise leave it unspecified. Omit unset operation
  inputs so c2ops can apply its defaults. Retain overrides in normal recipe state
  for later agent calls. The resolver applies human guidance; it does not choose
  replacements autonomously. If the new settings fail, show the attempted settings
  and error and ask again. The native fallback form must accept overrides even
  when the resolver's model cannot run. Test precedence, persistence, human direction
  and repeated failure.

- [x] **Return incomplete results to their producing agent.** Use the existing
  Execute → full Validate → Review cycle to request missing content. Remove the
  child-title fallback “Complete the agreed owner request”; require the receiver
  to supply a descriptive title before submission. Audit similar substitutions.
  Make package-probe and resolver titles describe their specific work or blocker.
  Test that incomplete advice returns for correction before child submission and
  that the corrected title reaches the child.

- [x] **Show qualitative scope in the one-pager and measured changes in the final review.**
  Remove numerical code-change estimates and estimate-versus-actual arithmetic.
  In the delivery one-pager, include a table with columns `Cell`, `Core code`,
  `Tests`, and `Docs`. Give each affected cell a row; mark each category `none`,
  `small`, `medium`, or `large` to show whether changes are expected and their
  rough size. Do not require line-count estimates or fixed numeric size thresholds.
  In the merge review, report actual measured additions/removals for core code,
  tests and docs, separately by cell, supported by per-file accounting for the
  actual candidate. Test code includes test frameworks, harnesses, fixtures and
  test implementations. Identify binary/uncountable changes without inventing
  counts, and distinguish completed delegated work from pending work. Have agent
  validation return missing or incomplete reports to Execute, followed by full
  validation. Keep these as human review content using the existing cycle.
  Test missing-report correction, measured counts, per-cell separation and the
  classification of test frameworks as test code.

- [ ] **Return child outcomes to the requester before escalating.** Deliver the
  actual job ID, success/failure/cancellation message and selected result/error
  directories to the requesting agent, including after an invalid model report.
  Let it retry, recover, adopt existing work or continue as appropriate. Enter
  resolution only when the requester is stuck/unavailable or its local allowance
  needs renewal. Test all outcomes, existing-child adoption and no duplicate
  submission during report correction. [Plan 1](PLAN_AUDIT_FOLLOWUPS.md#1-return-child-outcomes-to-the-agent-that-requested-the-work).

- [ ] **Enter the resolver first for `resume_from`.** Inspect previous work and
  current human direction, recover useful references and actual approvals, then
  enter the stage that has remaining work. Preserve completed effects and run the
  destination's full cycle. Avoid assuming earlier stages ran in the new job.
  Test approved implementation recovery, changed scope, unreadable history and
  publication after a completed merge. [Plan 2](PLAN_AUDIT_FOLLOWUPS.md#2-start-resume_from-in-the-resolver).

- [ ] **Preserve diagnostic directories and isolate producers.** Keep each
  child's/task's failure in its own subtree, including wrapped causes and original
  relative paths. Forward all hook failures without flattening names or replacing
  review documents. Prefer native directory references. Test same-named logs,
  nested failures and prepare/publish failure delivery.
  [Plan 3](PLAN_AUDIT_FOLLOWUPS.md#3-preserve-diagnostics-as-separate-directories).

- [x] **Unify configured specialists with the shared Validate activity.** Move
  specialist invocation out of Execute; keep the research hook there. Define the
  fixed stage mapping once, use the common validation prompt/schema, and pass
  configured assessment guidance to general and specialist assessors. Return all
  current findings in one validation result. Required failures return to Execute;
  optional advice has no independent veto. Rerun the full stage cycle, respect
  current human scope, and use its existing correction allowance. No new sign-off
  files or specialist recovery workflow. Test rejection/correction, complete
  findings, native failure delivery and actual hook-guidance consumers.
  [Detailed plan 4](PLAN_AUDIT_FOLLOWUPS.md#4-make-repository-required-reviews-actually-reach-validation).

- [ ] **Bound every automatic loop locally and allow explicit renewal.** Use
  positive finite defaults; count only repetitions owned by that loop. Inner
  consultation/child work must not spend the outer loop's allowance. Preserve the
  merge-chase count across stages. A resolver or human can grant more attempts;
  the resolver cannot renew itself indefinitely. Human discussion has no cap and
  does not grant attempts. Test exhaustion, isolation, slow progress and renewal.
  [Plan 5](PLAN_AUDIT_FOLLOWUPS.md#5-bound-each-automatic-loop-independently).

- [x] **Restore concise inspection guidance.** Explain actual task/field
  discovery, exact downloads, pagination, intermediate versus final results,
  restart-help discovery and access errors. Keep detailed data in scratch.
  Test exact retrieval beyond previews and the first inventory page.
  [Plan 6](PLAN_AUDIT_FOLLOWUPS.md#6-add-a-short-inspection-guide-to-new-session-context).

- [ ] **Use native directory references for selected artifact collections.**
  Confirm compact transport through child results and human reviews. Carry one
  coherent selected subtree, with a review title, primary document and optional
  collection purpose. Use descriptive filenames/links instead of mandatory
  per-file metadata. Test chapter growth and actual UI navigation for large
  directories; set-binding expansion alone does not prove compact transport.
  [Plan 7](PLAN_AUDIT_FOLLOWUPS.md#7-pass-directories-while-keeping-human-presentation-small).

- [x] **Fix missing feedback entry in adaptive3 reviews.** Compare actual UI
  behavior with adaptive2; align feedback/upload field names and supported action
  values, updating all readers together. Keep questions in Review, reject empty
  discussion submissions without an agent call, and preserve repeated resolver
  dialogue. Test real click/type/upload behavior as well as native response
  routing. Highest priority among these follow-ups.
  [Plan 8](PLAN_AUDIT_FOLLOWUPS.md#8-restore-usable-feedback-entry-in-human-reviews).

See [the implementation assessment](IMPLEMENTATION.md) and the separate
[runtime requirements](RUNTIME_REQUIREMENTS.md).

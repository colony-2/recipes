# Adaptive3 follow-ups

## Open findings from 2026-11-13

Scope: the [review-options audit](AUDIT_REVIEW_OPTIONS.md), Python preparation,
and the two jobs below on `http://192.168.1.195:9047/c2`. Implementation and test results are in the [assessment](IMPLEMENTATION_REVIEW_AND_BACKSTOP.md).
The earlier completed checklist remains below as history.

- [x] **Restore reader-friendly documents.** Compare adaptive2's owner-voice and
  human-language instructions with adaptive3. Explain the user problem and proposed
  change first; use familiar words, direct commitments and short connected prose.
  Keep workflow bookkeeping out of documents. Preserve the one-pager sections and
  every consequential design question. Put the shared guidance in one place and
  have existing validation request clearer writing when needed.

- [x] **Rename Backstop to Backstop.** Rename the activity, prompts, state paths,
  current documentation and tests together. Keep the same recovery responsibilities
  and boundaries. Preserve historical audit names and descriptions as history.

- [x] **Restore clear approval choices.** Use **Approve direction**, **Accept
  answer**, **Accept and merge**, and **Accept outcome** as appropriate. Package
  requests need **Add tools and run checks** and **Do not add these tools**.
  Derive the decision from the existing stage, work kind and validated candidate;
  retain one shared review activity. Test the generated native forms and their
  resulting paths for each case. Declining tools must neither launch a probe nor
  adopt configuration; the requester should receive the decision.

- [x] **Separate questions from change requests.** Show **Ask a question** and
  **Request changes**, using the existing review conversation agent. Preserve
  `feedback` and `annotations` field IDs. Test both buttons through Cortex's real
  adapter/renderer, including typing, uploading, returning to choices, empty
  submissions and repeated questions. Asking a question must not start execution
  or grant more automatic attempts.

- [x] **Make the stage or Backstop the visible requester.** Prefix descriptive
  titles with **Direction**, **Outcome review**, the actual stage requesting
  tools, or **Backstop**. Keep the full title within its limit. Backstop should
  describe the immediate blocker and proposed action; name the interrupted stage
  separately when useful. Show the actual allowance when asking for more attempts.
  Keep model controls usable when the agent cannot start, without unrelated JSON
  in every question. Test titles in the review queue and detail view, including
  reopened reviews, long subjects and native fallback forms.

- [x] **Reconsider new feedback before Backstop continues.** Currently, Continue
  can forward text/uploads while returning its previously selected stage and
  correction. Match ordinary review: plain approval can resume; new feedback goes
  through the conversation agent first. Test conflicting scope, an annotated
  document and a question accompanying Continue. Verify the actual interpreted
  correction and destination, not merely that notes were forwarded. The selected
  stage still runs its complete activity cycle.

- [x] **Make recovery requests readable without missing documents.** Keep a
  simple correction in the question itself. Attach any supporting document actually
  referenced, use working review links, and select an existing relevant overview
  when useful. The original Cortex request linked to an unattached worker-local
  correction file while displaying an old design. Test that situation and reject
  local-only links through existing validation. Do not add mandatory recovery
  documents, handoff files or a document-management activity.

- [x] **Cover permission failures at foreign recipe includes and preserve recovery.**
  Job `3M2pIhgSrgP6tJKgGrzM2WoqNHW` failed before its first agent started:
  `input secret "codex_api_key" exceeds the enclosing limit: lease permission denied`.
  Its custom `python-preparation-recipes-advice` wrapper calls adaptive3 Execute
  directly; its recorded path has no surrounding lifecycle/Backstop to recover.
  The earlier attempt `3M2pAXYfy6BnQvXl3GH37kk74oZ` failed identically. A later
  alternative, `3M2pYAOdgBC6lUbJSTT4ZUiWrkL`, also failed resolving the foreign
  operation's secret default. Retrying unchanged permissions cannot address this.

  Inspect the submitted wrapper and effective ceiling to identify the precise
  missing authorization. c2j's documented contract requires caller authorization
  for secret references from a foreign recipe; an optional secret expression does
  not waive it. Document a supported reuse example with the correct include grant
  and the existing recovery boundary. Prefer the normal build/consultation path
  when it satisfies the assignment. Keep necessary input-secret authorization
  separate from delegated secret-reading capability; do not broadly grant secrets
  to every agent or work around a denied ceiling.

  Test trusted-root and foreign-include cases with actual source identity and
  native permission evaluation: authorized input, missing grant, denied enclosing
  ceiling and foreign operation default. Use fixture secrets, never real keys.
  Mocks must not bypass input-secret resolution. Test that the supported containing
  workflow receives a launch failure, preserves its diagnostic, and offers local
  recovery/native human input when the agent cannot run. Owner: recipes for reuse
  guidance, containing workflow and coverage; c2j if its documented authorization
  contract is violated. The current error establishes a denial, not why the
  submitted authorization was insufficient.

- [ ] **Verify the shipped Python dependencies in real task environments.**
  Track [the c2j bug](../BUG_REPORT_C2J_PYTHON_DEPENDENCY_ENVIRONMENT.md), goal
  `3M2nxdy26CqBg7b2FzRob6uoeMN`. Confirm the supported interpreter/library contract
  before changing the recipe declaration. Run the unmodified validator through
  real fresh preparation and cache reuse on a supported worker, checking Pillow
  imports/image decoding and Markdown parsing. Unsupported dependencies must fail
  preparation clearly before the command runs. Local tests with preinstalled
  dependencies cover validator logic, not this boundary. Keep that distinction
  explicit in test results and release checks. The [real-worker check](VALIDATOR_WORKER_CHECK.md)
  still fails in both tasks with `No module named PIL`; this remains a c2j blocker.

- [x] **Make diagnostic completion distinguishable from a successful repair.**
  Job `3M2oINy9BiYRlbhD6YhRoX2Ebrk` was a diagnostic child of the c2j bug-fix job
  `3M2nxf25SYsee0HnOxsaw94fLpG`. It ran two probes (`first`, `reuse`); both returned
  `import_ok: false` and `No module named 'PIL'`. The script caught `ImportError`
  and exited zero, so the job and its diagnostic goal completed successfully.
  It collected useful evidence; it did not implement a repair. The parent repair
  job was still active when inspected.

  Give diagnostic jobs titles and concise results that say what they checked and
  found. A collection-only probe may succeed after recording a negative finding;
  an acceptance check must signal failed acceptance. Teach the requesting agent
  to read the result before concluding the dependency or original goal is fixed.
  Use ordinary result text/fields and existing requester recovery, not a new
  evidence schema. Test a successful diagnostic job containing a negative finding,
  a failed acceptance probe, and a successful acceptance probe. Verify the negative
  finding returns to the requester for action instead of being treated as repair
  completion solely because the child job succeeded.

Evidence: native `job show`, `job log`, `job story`, `job result` and the second
job's `_c2j/execution/reuse.log`, inspected 2026-11-13. The first failure is an
input-permission error; the second is a completed diagnostic with a negative
finding. Neither establishes that the Python bug was repaired. No observed jobs
were changed during this audit.

## Earlier implementation checklist

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

- [x] **Return child outcomes to the requester before escalating.** Deliver the
  actual job ID, success/failure/cancellation message and selected result/error
  directories to the requesting agent, including after an invalid model report.
  Let it retry, recover, adopt existing work or continue as appropriate. Enter
  resolution only when the requester is stuck/unavailable or its local allowance
  needs renewal. Test all outcomes, existing-child adoption and no duplicate
  submission during report correction. [Plan 1](PLAN_AUDIT_FOLLOWUPS.md#1-return-child-outcomes-to-the-agent-that-requested-the-work).

- [x] **Enter the resolver first for `resume_from`.** Inspect previous work and
  current human direction, recover useful references and actual approvals, then
  enter the stage that has remaining work. Preserve completed effects and run the
  destination's full cycle. Avoid assuming earlier stages ran in the new job.
  Test approved implementation recovery, changed scope, unreadable history and
  publication after a completed merge. [Plan 2](PLAN_AUDIT_FOLLOWUPS.md#2-start-resume_from-in-the-resolver).

- [x] **Preserve diagnostic directories and isolate producers.** Keep each
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

- [x] **Bound every automatic loop locally and allow explicit renewal.** Use
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

- [ ] **Use native directory references for selected artifact collections — blocked on c2j/Cortex.**
  The pinned runtime has no compact directory-reference contract. Native tests
  deliver 1,024 files but expand them into 202,940 bytes of reference metadata.
  See [the concrete runtime requirement](RUNTIME_REQUIREMENTS.md#4-transport-a-selected-directory-as-one-native-reference).
  Confirm compact transport through child results and human reviews once supported. Carry one
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

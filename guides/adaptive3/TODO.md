# Adaptive3 follow-ups

- [ ] **Allow human-directed model and reasoning changes.** Add optional job inputs
  `model` and `reasoning_effort`. For each field, use the latest human-directed
  override, then the job input, then the c2ops config default (`codex_model` or
  `codex_reasoning_effort`), otherwise leave it unspecified. Omit unset operation
  inputs so c2ops can apply its defaults. Retain overrides in normal recipe state
  for later agent calls. The resolver applies human guidance; it does not choose
  replacements autonomously. If the new settings fail, show the attempted settings
  and error and ask again. The native fallback form must accept overrides even
  when the resolver's model cannot run. Test precedence, persistence, human direction
  and repeated failure.

- [ ] **Return incomplete results to their producing agent.** Use the existing
  Execute → full Validate → Review cycle to request missing content. Remove the
  child-title fallback “Complete the agreed owner request”; require the receiver
  to supply a descriptive title before submission. Audit similar substitutions.
  Make package-probe and resolver titles describe their specific work or blocker.
  Test that incomplete advice returns for correction before child submission and
  that the corrected title reaches the child.

- [ ] **Show qualitative scope in the one-pager and measured changes in the final review.**
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

See [the implementation assessment](IMPLEMENTATION.md) and the separate
[runtime requirements](RUNTIME_REQUIREMENTS.md).

# Review decision briefs

The shared `recipes/kernel/review.yaml` now attaches a generated decision brief and supporting provenance before publishing a human review. Existing documents, form fields, decision values, receipts, routing, and annotation handling retain their contracts. Feedback and uploads still require revision and another review. Briefs cannot approve work.

The review include accepts optional `checkpoint` context. Development callers supply current phase, request, plan keys, approvals, jobs, consultation threads, assessment, verification, and candidate information through this context. Existing callers may omit it; their actual form questions and available documents still produce a useful review without invented phases. Do not supply historical brief text as evidence. Prior brief/provenance attachments remain available but are excluded from current source selection.

`review-content.yaml` owns source collection, immutable material evidence, deterministic rendering, namespacing, and provenance. Its helper source is held in `vars.program` and bound as a text artifact to isolated command steps. Source documents travel through artifact bindings; source bodies are not shell interpolations. Generated documents live under collision-safe `review-briefs/<digest>/` IDs. Existing stored references retain their identities.

The deterministic brief presents the actual question, attributed current evidence, exact authoritative facts and material limits, consultation outcomes, and coverage/source references. Optional-hook absence and empty sections are omitted. Original reports remain attached; failed or skipped mandatory checks, missing evidence, adverse assessments, and verification limits remain visible. Unclassified current evidence is retained paragraph-for-paragraph in the evidence ledger and rendered in the brief; there is no keyword filter or word cutoff. This conservative fallback can exceed the normal length target. Recognized absence-only reports may be omitted; mixed reports lose only exact recognized absence notices and retain their status and every unrelated paragraph. Required verification absence remains visible. Configuration and design-hook reports receive the same treatment rather than being excluded by filename. Known structured consultation outcomes retain their readable summary instead of a raw JSON dump; candidate inventory remains available through its original attachment. These are source-specific coverage distinctions, not claims of semantic understanding or newly performed verification.

Consultation summaries use current recorded outcomes and final references, distinguishing scope agreement, expert assessment, and delivery. Supplied final references supersede historical iteration files; unresolved or missing final documents are identified rather than linked as though attached. Per-conversation advisory reporting and human deconfliction in `consultation-report.yaml` are unchanged.

## Model synthesis is inactive

The production include passes `activation: false` to `review-synthesis.yaml`. No provider credentials are read and no inference call occurs in that default path. Activation is a reviewed release change, not an instruction accepted from evidence documents.

The optional synthesis recipe uses `nix:github:colony-2/c2ops/published#llm` with a closed response schema, at most two attempts, a 60-second invocation timeout per attempt, a source/serialized-request guard, and independent consistency checks. It rejects unknown citations, missing mandatory fact references, oversized output, and model-authored critical assertions. Retry is restricted to invalid output or recognized transient errors, with a conservative remaining-budget check; otherwise the original artifact bundle reaches deterministic rendering. No Codex synthesis, tools, fanout, or recursive summaries are introduced.

Before activation, confirm the deployed package/worker bounds include setup and provider retries within the 130-second total budget. The inspected c2ops published revision `f30202d13d197beaed7ba0bd0b120b04443728eb` supports the selected provider/model/response_schema interface, but its `EXTENSION_OPS.md` explicitly places package setup outside invocation timeout. Catalog/schema support does not establish enforceable end-to-end timing. This inspection is not runtime validation and does not authorize activation.

Run both original review examples and adverse, contradictory, injected, incomplete, and overflow cases three times each with the deployment provider/model. Preserve every fixture-marked caveat, finding, current key/status, and valid source reference. No invented verification or approval is allowed. Record corpus, requested/returned configuration, provenance, per-run results, and limitations; obtain human readability assessment. Any violation or unavailable evidence blocks model-default activation. Passing mocked scenarios is not this gate.

The original example bodies were not available in this build's inbox; no substitute fixtures establish those evaluations. Deterministic production remains available independently of activation. c2j metadata and Cortex presentation integration are separate work.

## Checks

Run the native suites with `c2j test run --file <suite>`:

- `recipe-tests/review-brief.test.yaml`: real evidence/artifact/form integration, limits, consultations, injection, overflow, and feedback.
- `recipe-tests/review-synthesis.test.yaml`: exact-selector mocks for valid output, corrective retry, invalid/citation failures, transport errors and timeout fallback.
- `recipe-tests/review-validation.test.yaml`: production helper validation, UTF-8 and schema bounds, mandatory references, missing evidence, collisions, repeat rendering, revisions, and exhausted budgets.

Also retain existing affected completion-review, hook, stale-accounting, and consultation scenarios. The approved statements are preserved in `recipe-tests/review-brief-statements.md`; missing live/runtime evidence must be reported rather than marked passed.

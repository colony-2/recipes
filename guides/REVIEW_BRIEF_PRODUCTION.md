# Review decision briefs

This document describes the retained **creation** review helper. Adaptive uses its
own agent-authored summaries and review presentation, unchanged by this cleanup.

The shared `recipes/kernel/review.yaml` attaches a generated decision brief and supporting provenance before publishing a human review. Existing documents, form fields, decision values, receipts, routing, and annotation handling retain their contracts. Feedback and uploads still require revision and another review. Briefs cannot approve work.

The review include accepts optional `checkpoint` context. Callers may supply the current decision and its authoritative facts through this context. Existing callers may omit it; their actual form questions and available documents still produce a useful review without invented phases. Do not supply historical brief text as evidence. Prior brief/provenance attachments remain available but are excluded from current source selection.

`review-content.yaml` owns source collection, immutable material evidence, deterministic rendering, namespacing, and provenance. Its helper source is held in `vars.program` and bound as a text artifact to isolated steps. The final renderer uses
`recipes/kernel/render/op.yaml` to return structured metadata directly; command
stdout previews can truncate and are not a transport for the complete result. Source documents travel through artifact bindings; source bodies are not shell interpolations. Generated documents live under collision-safe `review-briefs/<digest>/` IDs. Existing stored references retain their identities.

The deterministic brief presents the actual question, attributed current evidence, exact authoritative facts and material limits, consultation outcomes, and coverage/source references. Optional-hook absence and empty sections are omitted. Original reports remain attached; failed or skipped mandatory checks, missing evidence, adverse assessments, and verification limits remain visible. Unclassified current evidence is retained paragraph-for-paragraph in the evidence ledger and rendered in the brief; there is no keyword filter or word cutoff. This conservative fallback can exceed the normal length target. Recognized absence-only reports may be omitted; mixed reports lose only exact recognized absence notices and retain their status and every unrelated paragraph. Required verification absence remains visible. Configuration and design-hook reports receive the same treatment rather than being excluded by filename. Known structured consultation outcomes retain their readable summary instead of a raw JSON dump; candidate inventory remains available through its original attachment. These are source-specific coverage distinctions, not claims of semantic understanding or newly performed verification.

Consultation summaries use current recorded outcomes and final references, distinguishing scope agreement, expert assessment, and delivery. Supplied final references supersede historical iteration files; unresolved or missing final documents are identified rather than linked as though attached. The retired consultation-report helper is no longer shipped.

## Model synthesis is inactive

Commit `1b9846a` introduced the explicit activation gate described below. It was
never completed; disabling this optional extra call is not a c2j restriction.
The production include passes `activation: false` to `review-synthesis.yaml`. No provider credentials are read and no inference call occurs in that default path. Activation is a reviewed release change, not an instruction accepted from evidence documents.

The optional synthesis recipe uses `nix:github:colony-2/c2ops/published#llm` with a closed response schema, at most two attempts, a source/serialized-request guard, and independent consistency checks. It rejects unknown citations, missing mandatory fact references, oversized output, and model-authored critical assertions. Retry is restricted to invalid output or recognized transient errors; otherwise the original artifact bundle reaches deterministic rendering. No Codex synthesis, tools, fanout, or recursive summaries are introduced.

The approved “Remove recipe-imposed timeouts” bug fix supersedes the earlier
60-second attempt, 130-second total, five-second eligibility and 55-second retry
requirements, including B01's deadline prerequisite and B07 in
[the original statements](../recipe-tests/review-brief-statements.md). Evidence age
does not determine eligibility, retry or validity. Timestamps remain provenance.
Production synthesis remains inactive; activation still requires the content-quality
evaluation below. Supported timeout omission preserves runtime defaults, authority
bounds and cancellation; it does not certify unlimited execution or provider behavior.

Run both original review examples and adverse, contradictory, injected, incomplete, and overflow cases three times each with the deployment provider/model. Preserve every fixture-marked caveat, finding, current key/status, and valid source reference. No invented verification or approval is allowed. Record corpus, requested/returned configuration, provenance, per-run results, and limitations; obtain human readability assessment. Any violation or unavailable evidence blocks model-default activation. Passing mocked scenarios is not this gate.

The original example bodies were not available in this build's inbox; no substitute fixtures establish those evaluations. Deterministic production remains available independently of activation. c2j metadata and Cortex presentation integration are separate work.

## Checks

Run the native suites with `c2j test run --file <suite>`:

- `recipe-tests/review-brief.test.yaml`: real evidence/artifact/form integration, limits, consultations, injection, overflow, and feedback.
- `recipe-tests/review-synthesis.test.yaml`: exact-selector mocks for valid output, corrective retry, invalid/citation failures, transport errors and timeout fallback.
- `recipe-tests/review-validation.test.yaml`: production helper validation, UTF-8 and schema bounds, mandatory references, missing evidence, collisions, repeat rendering, revisions, and age-independent validation.

Retain creation, shared-artifact and adaptive regression coverage. Retired
heavy/light completion, stale-accounting and consultation suites are removed. The approved statements are preserved in `recipe-tests/review-brief-statements.md`; missing live/runtime evidence must be reported rather than marked passed.

# Decision brief acceptance statements

Defined before implementation against `inbox/design.md` and the final accepted production contract. This work fits recipes ownership. External prerequisite keys: **[]**. No implementation or test execution is claimed.

## Compatibility and execution conventions

These statements supplement `recipe-tests/build-kernel-statements.md`, `recipe-tests/completion-review-statements.md`, and existing consultation, annotation, coordination, accounting, and hook scenarios. They do not replace or relax existing expectations. No feature is deprecated and no deprecation plan is required.

The visible change is additive decision briefs and provenance. Original hook reports remain available: omitting irrelevant optional-hook boilerplate from a brief does not remove evidence, conceal mandatory checks, or change skipped checks into passes. Existing agent-report failure propagation remains unchanged; only the new optional synthesis path has bounded fallback behavior.

Each table row is one test statement; its expected-outcome text has at most 30 words. Filenames identify production boundaries under test. New helper and scenario filenames will be established during implementation without changing these outcomes.

Dependency codes:

- **N**: native c2j declarative runner, disposable Git repository, declared Nix helper packages; exact `nix:github:colony-2/c2ops/published#llm` selector mocked, helper and form/artifact path real.
- **R**: N plus actual selected c2ops package, configured non-Codex provider/model, authorized credentials and worker deadline enforcement; required for runtime/model activation evidence.
- **H**: R plus original evaluation corpus and human readability assessment.

Do not substitute mocked model cases for real deadline or factual evaluation evidence. Native tests exercise production includes, exported artifact references, and resulting forms/routes, rather than a separate illustrative renderer.

## Checkpoint content and evidence

| ID | Priority | Level / dependencies | Filenames | Expected outcome |
| --- | --- | --- | --- | --- |
| C01 | Critical | Integration / N | `recipes/develop/develop.yaml`, `recipes/kernel/review.yaml` | Triage briefs state the requested outcome, ownership, constraints, and actual scope decision without inventing later phases. |
| C02 | Critical | Integration / N | `recipes/develop/develop.yaml`, `recipes/kernel/review.yaml` | Design and test-plan briefs explain behavior, consequential alternatives, compatibility, acceptance expectations, and exact prerequisites. |
| C03 | Critical | Integration / N | `recipes/develop/merge-review.yaml`, `recipes/kernel/review.yaml` | Outcome briefs state delivered behavior, candidate identity, verification performed, material limits, unresolved findings, and the precise decision requested. |
| C04 | Critical | Integration / N | `recipes/develop/merge-review.yaml`, `recipes/develop/accounting.yaml` | No-change briefs retain evidence-backed fulfillment rationale; missing work cannot become approval merely because the candidate inventory is empty. |
| C05 | High | Integration / N | `recipes/develop/develop.yaml`, `recipes/kernel/review.yaml` | Revision and clarification briefs identify changed evidence and the remaining question without repeating irrelevant phase history. |
| C06 | High | Integration / N | `recipes/kernel/review.yaml` | Briefs omit empty sections, serialized phase dumps, repeated setup, and irrelevant optional-hook absence while retaining original documents. |
| C07 | Critical | Integration / N | `recipes/develop/verify.yaml`, `recipes/kernel/review.yaml` | Failed checks, skipped mandatory checks, missing expected evidence, contradictions, and unresolved adverse findings remain visible despite positive recommendations. |
| C08 | Critical | Integration / N | `recipes/develop/verify.yaml`, `recipes/kernel/review.yaml` | Absent optional verification remains skipped in evidence; briefs never claim it passed or automatically block otherwise valid review. |
| C09 | Critical | Integration / N | `recipes/kernel/review.yaml` | Unknown or ambiguous evidence remains explicitly uncertain, with attributed excerpts or fallback rather than invented completeness. |
| C10 | High | Integration / N | `recipes/kernel/review.yaml` | Briefs normally target 300–600 words; necessary material findings survive even when they require a longer review. |
| C11 | Critical | Integration / N | `recipes/kernel/review.yaml` | Source references identify exact attached documents and available sections; unsupported links or fabricated URLs never appear as evidence. |

## Consultation synthesis

| ID | Priority | Level / dependencies | Filenames | Expected outcome |
| --- | --- | --- | --- | --- |
| S01 | High | Integration / N | `recipes/kernel/review.yaml`, `recipes/kernel/consultation-report.yaml` | Multiple consultations yield one readable summary covering accepted scope, contracts, disagreements, assessments, and approval or delivery dependencies with final-document references. |
| S02 | Critical | Integration / N | `recipes/kernel/review.yaml`, `recipes/kernel/consultation-report.yaml` | Later accepted revisions supersede earlier proposals; summaries never revive rejected scope or historical prerequisite identifiers. |
| S03 | Critical | Integration / N | `recipes/kernel/consultation-report.yaml`, `recipes/develop/develop.yaml` | Serving agreement remains distinct from delivered implementation; adverse expert findings remain adverse regardless of agreement. |
| S04 | Critical | Integration / N | `recipes/kernel/review.yaml`, `recipes/develop/develop.yaml` | Parent requests and expert assessments create no prerequisite keys; only authoritative current serving prerequisites and statuses are reported. |
| S05 | High | Integration / N | `recipes/kernel/review.yaml` | Reviews without consultations omit the consultation section and do not invent consensus. |
| S06 | Critical | Integration / N | `recipes/kernel/consultation-report.yaml` | Human deconfliction retains both positions, evidence, focused questions, and existing needs-review routing despite the added summary. |
| S07 | Critical | Integration / N | `recipes/kernel/review.yaml` | Unstructured consultation evidence receives attributed excerpts, final-document references, and coverage warnings rather than manufactured agreement. |

## Bounded synthesis and fallback

| ID | Priority | Level / dependencies | Filenames | Expected outcome |
| --- | --- | --- | --- | --- |
| B01 | Critical | Integration / N | `recipes/kernel/review.yaml` | Deterministic briefs remain available by default; missing credentials, provider configuration, or enforceable deadlines bypass inference immediately. |
| B02 | Critical | Integration / R | `recipes/kernel/review.yaml`, `docs/data/op-catalog.yaml` | Enabled synthesis uses the existing published llm selector with configured non-Codex provider/model and response schema, without agent sessions or tool execution. |
| B03 | Critical | Integration / N | `recipes/kernel/review.yaml` | Valid cited synthesis produces visibly generated prose while preserving immutable critical facts, exact keys, statuses, and candidate identity. |
| B04 | Critical | Integration / N | `recipes/kernel/review.yaml` | Malformed JSON, missing required fields, extra fields, incorrect types, unknown citations, or missing mandatory references cannot become rendered model prose. |
| B05 | Critical | Integration / N | `recipes/kernel/review.yaml` | Invented prerequisites, altered statuses, contradictory candidate identities, and uncited substantive claims trigger rejection and bounded recovery. |
| B06 | Critical | Integration / N | `recipes/kernel/review.yaml` | Transport failures and invalid responses receive at most one corrective retry; nontransient errors immediately produce useful fallback. |
| B07 | Critical | Integration / R | `recipes/kernel/review.yaml` | Each attempt ends within 60 seconds; total synthesis ends within 130 seconds including backoff and provider retries, then fallback reaches review. |
| B08 | Critical | Integration / N | `recipes/kernel/review.yaml` | Synthesis uses one selected source set without fanout, recursive summaries, nested retries, or agent repair loops. |
| B09 | Critical | Integration / N | `recipes/kernel/review.yaml` | Source text exceeding 128 KiB UTF-8 bypasses inference, discloses omitted inference coverage, and preserves original attachments without silent truncation. |
| B10 | Critical | Integration / N | `recipes/kernel/review.yaml` | Responses exceeding 32 KiB decoded, prose exceeding 8 KiB, arrays exceeding 32 entries, or item prose exceeding 2 KiB are rejected. |
| B11 | High | Integration / N | `recipes/kernel/review.yaml` | Inputs exactly at resource limits remain eligible when all other conditions pass; multibyte text is measured in UTF-8 bytes. |
| B12 | Critical | Integration / N | `recipes/kernel/review.yaml` | Exhausted retries produce the actual question, change description, material findings, verification limits, exact prerequisite statuses, evidence links, and an explicit fallback reason. |
| B13 | Critical | Integration / N | `recipes/kernel/review.yaml`, `recipes/develop/develop.yaml` | Instructions injected into logs, contracts, or generated prose cannot change fields, choices, approval, prerequisite keys, source authority, or routing. |
| B14 | Critical | Integration / N | `recipes/kernel/review.yaml` | The source manifest and mandatory evidence ledger exist before inference; model output cannot rewrite authoritative facts or claim unsupported coverage. |

## Artifact lifecycle and preserved review semantics

| ID | Priority | Level / dependencies | Filenames | Expected outcome |
| --- | --- | --- | --- | --- |
| L01 | Critical | Integration / N | `recipes/kernel/review.yaml` | New brief and provenance IDs avoid collisions, preserve original bytes and references, and remain available to subsequent review occurrences. |
| L02 | High | Integration / N | `recipes/kernel/review.yaml` | Internal context, feedback, and conversation documents remain filtered from the form while permitted original evidence stays reachable. |
| L03 | Critical | Integration / N | `recipes/kernel/review.yaml` | Provenance records producer, prompt/schema versions, requested/returned provider/model when known, attempts, elapsed time, fallback reason, source identities/digests, candidate, and coverage. |
| L04 | Critical | Integration / N | `recipes/kernel/review.yaml` | Frozen form replay reuses identical brief and provenance references without additional inference. |
| L05 | Critical | Integration / N | `recipes/develop/develop.yaml`, `recipes/kernel/review.yaml` | Changed candidate, source set, feedback, or annotations produce a fresh evidence-bound brief through the existing review-occurrence flow. |
| L06 | Critical | Integration / N | `recipes/develop/develop.yaml`, `recipes/kernel/review.yaml` | Uploaded annotations and requested changes return to revision and another review; they never count as approval. |
| L07 | Critical | Integration / N | `recipes/kernel/review.yaml`, `recipes/develop/develop.yaml` | Legacy callers preserve field names, choices, exact responses, receipts, routing, and approval gates without requiring new metadata fields. |
| L08 | Critical | Integration / N | `recipes/develop/accounting.yaml`, `recipes/develop/merge-review.yaml` | Brief generation neither bypasses complete file accounting nor authorizes stale candidates; revised candidates still require fresh accounting and human approval. |
| L09 | High | Integration / N | `recipes/kernel/review.yaml` | Isolated operations receive evidence through declared inputs and artifact bindings; exported documents resolve without ambient shared files or repository mutations. |

## Real examples and activation gate

| ID | Priority | Level / dependencies | Filenames | Expected outcome |
| --- | --- | --- | --- | --- |
| E01 | Critical | Integration / H | `recipes/kernel/review.yaml`, `recipes/develop/merge-review.yaml` | The original deletion-filter example retains two-mode scope, no active prerequisite keys, and Postgres, older-server, and purge limits; historical three-mode scope stays superseded. |
| E02 | Critical | Integration / H | `recipes/kernel/review.yaml`, `recipes/develop/merge-review.yaml` | The original story-prompt example retains tests not rerun at merge, unverified production cause and deployed freshness, and correctly attributed earlier test evidence. |
| E03 | Critical | Integration / H | `recipes/kernel/review.yaml` | Three runs per real, adverse, contradictory, injection, incomplete, and overflow case retain all marked caveats, findings, keys/statuses, and valid citations without invented verification or approval. |
| E04 | Critical | Integration / H | `recipes/kernel/review.yaml` | Any evaluation violation or unavailable required evidence blocks model-default activation while deterministic reviews remain available. |
| E05 | High | Integration / H | `recipes/kernel/review.yaml` | Evaluation records identify corpus, deployment model/configuration, per-run results, provenance, and limitations without claiming general factual correctness. |
| E06 | High | Integration / H | `recipes/kernel/review.yaml` | Human reviewers understand the decision, change, and uncertainty without opening every attachment; material limits remain understandable and visible. |

## Evidence limits and completion criteria

The inbox supplies design, final agreement, and accepted production contract, but not the bodies of `mockups/examples.json` or the real source reviews. Retrieve those originals through artifact plumbing before E01–E03; synthetic stand-ins cannot establish those outcomes. No real-example evaluation or model activation is claimed now. Build settings add no consultations or specialist prompt requirements; no separate advisory findings were supplied.

Implementation acceptance requires passing native production-path cases and existing affected lifecycle regressions, plus documented real runtime enforcement before enabling inference. Model-default activation additionally requires the complete H evaluation gate. A mock-only timeout test cannot establish worker enforcement. Missing model evaluation leaves deterministic production usable and explicitly records synthesis as unactivated.

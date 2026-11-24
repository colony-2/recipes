# Test continuous discussion and correction behavior

These expectations were approved before implementation in Recipes job
`3M8JPi6Jy6P6K494QYf2h6hKIza`, native request
`010b7735-1d81-498e-9e49-b00dfa9fb11c` (2026-11-15). Their expectation text is
unchanged; filename annotations now name the implementing checks. Each expectation is at most 30 words; filenames, priority, kind and
dependencies are separate annotations. See the [current contract](../../guides/REVIEW_V2.md)
and [test instructions](../adaptive3/README.md) for implementation and execution.

Critical statements gate acceptance. High statements establish the shared contract and compatibility promised by the direction and also require passing results. A failed or unavailable required check is unmet acceptance. Existing Cortex results, capability probes and a hand-authored consumer fixture do not establish migrated-producer acceptance.

## Form declarations and native contributions

| ID | Priority | Kind | Dependencies | Filenames | Expectation |
| --- | --- | --- | --- | --- | --- |
| V01 | Critical | Integration | c2j | `recipes/review-v2.yaml`, `recipe-tests/review-v2/forms.test.yaml` | Generated forms open structured reviews with complete request and response schemas and no ordinary fields or native review kind. |
| V02 | Critical | Integration | c2j | `recipes/review-v2.yaml`, `recipe-tests/review-v2/forms.test.yaml` | New forms use final direction rules; legacy, mixed, partial, null and forbidden-with-uploads declarations fail before opening input. |
| V03 | High | Unit | Python | `recipes/review-v2.py`, `recipe-tests/review-v2/test_contract.py` | Duplicate identifiers and metadata naming unattached documents are rejected; valid original references retain producer coordinates. |
| V04 | High | Unit | Python | `recipes/review-v2.py`, `recipe-tests/review-v2/test_contract.py` | Generic text, choice, boolean and number settings accept valid declarations and reject incompatible controls, unsupported keywords and contradictory bounds. |
| V05 | High | Unit | Python | `recipes/review-v2.py`, `recipe-tests/review-v2/test_contract.py` | Choice validation distinguishes false, zero, null and strings, rejects numerically duplicate choices, and counts string lengths by Unicode code points. |
| V06 | High | Unit | Python | `recipes/review-v2.py`, `recipe-tests/review-v2/test_contract.py` | Declared nullable resets succeed; incomplete reset pairs and invalid current or default values fail without filling response defaults. |
| V07 | High | Unit | Python | `recipes/review-v2.py`, `recipe-tests/review-v2/contract-vectors.json` | Portable patterns accept supported Unicode search cases and reject unsupported syntax, leading-zero repeat bounds and excessive repeats. |
| V08 | Critical | Integration | c2j native structured submission | `recipes/review-v2.yaml`, `recipe-tests/review-v2/native.test.yaml`, `recipe-tests/adaptive3/consumer/native_test.go` | A direction configured to forbid feedback accepts empty text and rejects nonempty text, whitespace and uploads. |
| V09 | Critical | Integration | c2j native structured submission | `recipes/review-v2.yaml`, `recipe-tests/review-v2/native.test.yaml` | Required contributions reject every declared whitespace-only case, including U+FEFF; meaningful Unicode text succeeds and remains byte-for-byte unchanged. |
| V10 | Critical | Integration | c2j, artifact storage | `recipes/review-v2.yaml`, `recipe-tests/adaptive3/consumer/native_test.go` | Required contributions accept permitted upload-only responses; settings, originals and earlier discussion never satisfy the new contribution requirement. |
| V11 | Critical | Integration | c2j native structured submission | `recipes/review-v2.yaml`, `recipe-tests/review-v2/native.test.yaml` | Missing contribution fields, unknown properties, undeclared or inapplicable settings and incorrectly typed edits fail; valid sparse edits preserve omitted values. |
| V12 | High | Integration | c2j, published Cortex validators | `recipe-tests/review-v2/contract-vectors.json`, `recipe-tests/adaptive3/consumer/feedback.test.tsx` | Producer and consumer agree on identical declaration, contribution, whitespace, scalar, reset, Unicode-length and portable-pattern vectors. |

## Checkpoint effects, discussion and corrections

| ID | Priority | Kind | Dependencies | Filenames | Expectation |
| --- | --- | --- | --- | --- | --- |
| V13 | Critical | Integration | c2j | `recipes/adaptive3/prompts/review.yaml`, `recipes/adaptive3/backstop.yaml`, `recipe-tests/adaptive3/review.test.yaml` | Reviewers can approve with or without a text comment. Approval records the exact comment and proceeds with the selected action. |
| V14 | Critical | Integration | c2j, artifact storage | `recipes/adaptive3/review.yaml`, `recipe-tests/adaptive3/review.test.yaml` | Two questions retain exact human turns, actual answers, receipts, originals and one logical identity, with fresh native requests and another contribution pending. |
| V15 | Critical | Integration | c2j | `recipes/adaptive3/review.yaml`, `recipe-tests/adaptive3/backstop.test.yaml` | Every question continues review; even an answer suggesting changes cannot approve work, revise documents, move stages or grant attempts. |
| V16 | Critical | Integration | real Codex CLI, scripted local provider, c2ops | `recipes/adaptive3/agent.yaml`, `recipe-tests/adaptive3/discussion-context.test.yaml` | Successive answering calls receive complete ordered discussion and original/upload bytes; answering-session continuation preserves context while remaining read-only. |
| V17 | Critical | Integration | persisted c2j, artifact storage | `recipes/adaptive3/discussion.yaml`, `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Restart after accepted question or saved answer retains each turn once, exact receipts, original references and pending status without inventing an answer. |
| V18 | Critical | Integration | c2j, artifact storage | `recipes/adaptive3/discussion.yaml`, `recipe-tests/adaptive3/consumer/native_test.go`, `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Same-named uploads from one or successive contributions remain distinct and readable; discussion attachments never replace original documents. |
| V19 | Critical | Integration | c2j | `recipes/adaptive3/review.yaml`, `recipe-tests/adaptive3/review.test.yaml` | Document comments appear only with originals; otherwise the review explains Request changes without offering document comments. |
| V20 | Critical | Integration | c2j, artifact storage | `recipes/adaptive3/cycle.yaml`, `recipe-tests/adaptive3/review-comments.test.yaml` | Revised documents keep their review ID and discussion. Approval identifies the current revision, its native request and its exact documents. |
| V21 | Critical | Integration | c2j | `recipes/adaptive3/packages.yaml`, `recipe-tests/adaptive3/packages.test.yaml` | Package document comments regenerate the proposal, validate configuration and documents, and require fresh approval before probing. |
| V22 | Critical | Integration | c2j | `recipes/adaptive3/backstop.yaml`, `recipe-tests/adaptive3/backstop-actions.test.yaml` | Backstop document comments rerun read-only investigation and readability checks; revised diagnosis requires a fresh decision before correction. |
| V23 | Critical | Integration | c2j | `adaptive3.yaml`, `recipe-tests/adaptive3/review-routing.test.yaml`, `recipe-tests/adaptive3/lifecycle.test.yaml` | Explicit current or earlier correction destinations run the selected complete cycle; scope changes return to Direction and conflicting instructions await clarification. |
| V24 | Critical | Integration | c2j | `recipes/adaptive3/lifecycle.yaml`, `recipe-tests/adaptive3/review-routing.test.yaml` | Auto retains reviewer routing; explicit destinations apply once and reset to Auto, while questions and approvals reject routing edits. |
| V25 | Critical | Integration | c2j | `recipes/adaptive3/packages.yaml`, `recipe-tests/adaptive3/package-routing.test.yaml` | Package-review corrections preserve their destination through containing lifecycles instead of silently resuming the interrupted agent or bypassing approval. |
| V26 | High | Integration | c2j | `recipe-tests/review-v2/forms.test.yaml`, `recipe-tests/review-v2/forms.yaml` | An unfamiliar fixture setting changes fixture output; omission preserves its value, applicable sparse edits work, and declared reset restores its default. |
| V27 | Critical | Integration | c2j | `recipes/adaptive3/backstop.yaml`, `recipe-tests/adaptive3/backstop-actions.test.yaml`, `recipe-tests/adaptive3/backstop.test.yaml` | New reviews offer no model, reasoning or settings-reconsideration controls; undeclared edits and human prose cannot mutate invocation configuration. |
| V28 | High | Integration | c2j, c2ops | `build.yaml`, `recipe-tests/adaptive3/models.test.yaml` | Launch overrides remain independent; omitted settings retain worker defaults and unset operation arguments remain omitted after review-control removal. |
| V29 | Critical | Integration | c2j | `recipes/adaptive3/backstop.yaml`, `recipe-tests/adaptive3/backstop-actions.test.yaml` | Readable available corrections permit bounded continuation; unreadable evidence, unavailable actions, questions and routing edits cannot grant work or replenish attempts. |
| V30 | Critical | Integration | c2j | `recipes/adaptive3/packages.yaml`, `recipe-tests/adaptive3/packages.test.yaml` | Package refusal, with optional feedback or uploads, runs no probe; failed checks prevent adoption, while successful approved checks permit adoption. |
| V31 | Critical | Integration | c2j, Git | `recipes/adaptive3/integration.yaml`, `recipe-tests/adaptive3/integration.test.yaml` | Equivalent rebases retain native approval; changed edits require fresh review, and publication recovery never repeats a completed merge. |
| V32 | High | Integration | c2j, c2ops, artifact storage | `recipes/adaptive3/consultation.yaml`, `recipe-tests/adaptive3/nested-adoption.test.yaml`, `recipe-tests/adaptive3/package-restore.test.yaml` | Nested consultation and ordinary session restoration retain current instructions, original documents and accepted feedback without introducing model-change session policy. |

## Local Cortex integration using real generated forms

All cases and launchers below live in Recipes. Cortex remains an unchanged published dependency. These are controlled local checks; no serving endpoint, deployment or operator evidence is required.

| ID | Priority | Kind | Dependencies | Filenames | Expectation |
| --- | --- | --- | --- | --- | --- |
| V33 | Critical | Integration | native reports, Cortex, pnpm | `recipe-tests/adaptive3/consumer/run.py`, `recipe-tests/adaptive3/consumer/feedback.test.tsx` | Actual helper-produced checkpoint forms reach real v2 presentation dispatch with unchanged schemas and documents; missing or empty requested fixture input fails. |
| V34 | High | Integration | Cortex, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Desktop and phone reviews render generated labels, originals and ordered discussion; generic settings render without model-specific knowledge, and absent settings hide the gear. |
| V35 | Critical | Integration | Cortex, HTTP JobDB, pinned worker, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Two questions and actual answers remain visible in order under one logical identity, with unchanged originals and another contribution pending. |
| V36 | Critical | Integration | Cortex, HTTP JobDB, browser, artifact storage | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Original and cross-job document references resolve through retained manifests; same-named uploaded files retain distinct bindings and exact bytes after reload. |
| V37 | Critical | Integration | Cortex, HTTP JobDB, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Adaptive3 accepts a blank or commented approval on the displayed revision. A direction configured to forbid feedback rejects text and uploads. |
| V38 | High | Integration | Cortex, HTTP JobDB, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Gear edits send nothing until confirmation; only changed applicable settings submit, while invalid drafts block confirmation and inapplicable edits remain local. |
| V39 | Critical | Integration | Cortex, HTTP JobDB, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Structured multipart contributions return native receipts; forged artifact keys, receipt/actor fields and replacement conversations fail without accepting a contribution. |
| V40 | Critical | Integration | persisted HTTP JobDB, Cortex, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Reload during an input gap preserves saved discussion and originals, shows waiting accurately, and resumes only against the matching successor occurrence. |
| V41 | Critical | Integration | Cortex, HTTP JobDB, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Stale native requests cannot submit; terminal jobs stop waiting, and unavailable history preserves readable saved material while disabling uncertain actions. |
| V42 | Critical | Integration | Cortex, HTTP JobDB, browser, controlled response interruption | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | Ambiguous submission reconciles accepted history without automatic repost, duplicate contribution, revision or work approval. |
| V43 | High | Integration | Cortex, browser | `recipe-tests/adaptive3/consumer/review-v2.spec.ts` | A reviewer can read both plan versions and their submitted discussion after revision. Unsent drafts stay out of history. Frozen legacy forms remain readable. |
| V44 | Critical | Integration | recorded c2j restart, Cortex, browser, artifact storage | `recipe-tests/adaptive3/consumer/review-v2.spec.ts`, `recipe-tests/adaptive3/resume.test.yaml` | Recorded restart matches an uninterrupted control for identity, discussion, receipts, correction choice, artifacts and pending actions; no question produces approval or publication. |

## How to establish the expectations

Start with declaration and schema cases, then migrate each checkpoint with its focused native tests. Native negative submissions must satisfy unrelated guards, identify the expected rejection and retain a valid control. For rejected contributions, assert no accepted receipt, answering call or downstream effect. Use actual generated schemas for direct native submission; browser-disabled checks must not be the only defense.

Use one Recipes-owned `contract-vectors.json` corpus with explicit expected outcomes for producer validation, direct native submissions where applicable, and exported Cortex validators. Include each whitespace character and mixtures, meaningful Unicode, scalar distinctions, numeric equality, supported patterns and prohibited patterns. Positive controls accompany each failure family. Load the exact vector bytes; do not rewrite values through string coercion.

For repeated questions, hold the successor input pending while asserting both question/answer pairs, then submit an explicit final contribution to finish the test. Check after each accepted human turn and actual answer. Preserve the same logical identity and original producer coordinates while native request IDs change. An agent response containing a hypothetical change must not trigger a revision. Assert no stage work, attempt grant, acceptance receipt for the work or publication during discussion.

Use scripted agent choices for routing and real native artifacts, Git and child waits for effects. Verify actual answering-session requests and attachment bytes separately with the real Codex CLI and a scripted local provider. A mock prompt assertion does not replace that check. Retain ordinary session and nested consultation restoration without adding removed model-change policies.

Record workflow restarts after the first accepted question, after its answer and after an accepted correction choice before its effect. Compare against an uninterrupted control, including artifact contents, native receipt identities, selected routing and absence of duplicate effects. A direct c2ops restore, serialized state round trip or second fresh job is insufficient.

The [Recipes-owned harness](../adaptive3/README.md) extracts complete generated forms and exercises unchanged published Cortex. DOM/component checks establish dispatch and interaction; actual production Cortex plus local HTTP JobDB/worker checks establish multipart submission, persisted history, manifests, receipts and file bytes. Keep producer schemas and original documents intact. The independent Cortex fixture remains a control only.

Run the focused additions, affected adaptive3 suites, native authoring validation and existing policy checks. Standard commands once the planned files exist:

```sh
c2j test validate --directory recipe-tests/review-v2
c2j test run --directory recipe-tests/review-v2
c2j test validate --directory recipe-tests/adaptive3
c2j test run --directory recipe-tests/adaptive3
python3 recipe-tests/checks/recipe_timeout_policy.py .
```

The harness uses compatible published Cortex and the repository's supported pinned runtime/worker and locked dependencies. Record their exact identities with test results. Request missing packages before installation; this plan requests no installation or worker configuration. Do not patch Cortex or substitute mocks for required real boundaries. An isolated retry pass does not erase a failed combined run. No production deployment is part of acceptance.

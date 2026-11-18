# Adaptive3 test statements

All integration cases use the pinned c2j runtime and disposable cell repositories.
Agent decisions are scripted unless a case is explicitly marked live.

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| A3-01 | Each accepted delivery stage advances directly after Execute, complete validation and Review. | Critical | Integration / c2j, Nix | adaptive3.yaml, lifecycle.yaml, cycle.yaml |
| A3-02 | A correction rechecks affected work and reuses passing verification only when its inputs remain current. | Critical | Integration / c2j, Nix | lifecycle.yaml, validate.yaml |
| A3-03 | Human questions retain the pending item without executing work or consuming automatic attempts. | Critical | Integration / c2j, Nix | review.yaml |
| A3-04 | Human changes reach Execute with original wording and supersede conflicting generated plans. | Critical | Integration / c2j, Nix | review.yaml, prompts/execute.yaml |
| A3-05 | Validation and human review receive the same corrected artifact identities without historical overlays. | Critical | Integration / c2j, Nix | cycle.yaml, tools.yaml, review.yaml |
| A3-06 | Large diagnostics remain available without corrupting bounded control outputs. | Critical | Integration / c2j, Python | tools.yaml |
| A3-07 | Planning, validation and review cannot persist repository edits; implementation can. | Critical | Integration / c2j, Nix | agent.yaml, execute.yaml |
| A3-08 | Caught execution failures enter same-job resolution and can resume successfully. | Critical | Integration / c2j, Nix | adaptive3.yaml, backstop.yaml |
| A3-09 | Consultation runs in the receiving cell and sends its agreed assignment directly to child execution. | Critical | Integration / c2j, Nix | consultation.yaml |
| A3-10 | Nested owner advice retains the suspended conversation without creating an advice job. | High | Integration / c2j, Nix | consultation.yaml |
| A3-11 | Package probes cannot run before policy or human approval, and adoption preserves unrelated configuration. | Critical | Integration / c2j, Nix | packages.yaml, package-probe.yaml, tools.yaml |
| A3-12 | Missing required verification and failed publication remain correctable rather than silently succeeding. | Critical | Integration / c2j, Nix | hooks.yaml, validate.yaml, execute.yaml |
| A3-13 | Unchanged rebases reuse approval after full validation; changed edits require review. | Critical | Integration / c2j, Git | tools.yaml, review.yaml, integration.yaml |
| A3-14 | New sessions receive instructions; resumed sessions receive current tasks without another instruction insertion. | High | Integration / c2j, Nix | agent.yaml, prompts/ |
| A3-15 | Prompt includes create no worker tasks and preserve literal caller text. | High | Integration / c2j | prompts/ |
| A3-16 | Cancellation retains its meaning and never silently recreates cancelled work. | Critical | Integration / c2j | lifecycle.yaml, consultation.yaml |
| A3-17 | Real UI reviews contain readable captures linked from the selected human document. | High | Live integration / Codex, browser | validate.yaml, tools.yaml |
| A3-18 | Default build uses Adaptive3 for explanations, delivery, and repository improvements. | Critical | Integration / c2j | build.yaml, adaptive3.yaml, default-build.test.yaml |
| A3-19 | A failed backstop correction asks for human direction before another automatic attempt, even when the error message changes. | Critical | Integration / c2j, Nix | backstop.yaml, adaptive3.yaml |
| A3-20 | Review actions expose feedback entry and preserve questions, changes and uploads through submission. | Critical | Integration / c2j, Cortex renderer | review.yaml, backstop.yaml |
| A3-21 | Required specialist findings prevent acceptance until full validation passes; optional advice has no independent veto. | Critical | Integration / c2j, Nix | validate.yaml, specialists.yaml |
| A3-22 | Configured assessment guidance reaches general and specialist assessors with current human scope and original diagnostic references. | High | Integration / c2j, Nix | validate.yaml, prompts/validate.yaml |
| A3-23 | Repeated backstop discussion preserves the previous proposal and human context without executing work before explicit continuation. | High | Integration / c2j, Nix | backstop.yaml |

| A3-24 | Incomplete receiver titles return to the author before independent assessment or child submission. | consultation.test.yaml | critical | integration, c2j |
| A3-25 | Missing change measurements return to the writer; final reviews separate cells and include test frameworks. | reporting.test.yaml | high | integration, c2j |
| A3-26 | Candidate measurements preserve per-file additions/removals and mark binaries uncountable. | test_tools.py | high | unit, Git |
| A3-27 | Job inspection follows pagination and retrieves exact output beyond previews. | inspection.test.yaml | high | integration, c2j |

| A3-28 | Explicit model settings override worker defaults independently; absent settings stay omitted. | models.test.yaml | high | integration, c2j |
| A3-29 | Unavailable models reopen native human input; corrected settings persist into subsequent work and validation. | models.test.yaml | critical | integration, c2j |

| A3-30 | Successful and failed child outcomes reach their requester before resolution, including after invalid reports. | child-recovery.test.yaml | critical | integration, c2j |
| A3-31 | Wrapped failures retain same-named logs with distinct producer paths and exact bytes. | diagnostics.test.yaml | critical | integration, c2j |
| A3-32 | Prepare failure diagnostics reach the working agent without replacing the current review documents. | hook-recovery.test.yaml | high | integration, c2j |

| A3-33 | Existing active or successful attempts are awaited without another delivery submission. | adoption.test.yaml | critical | integration, c2j |
| A3-34 | Corrective cancellation text reaches the requester without cancelling its parent or automatically replacing the child. | child-recovery.test.yaml | critical | integration, scripted terminal result |

- **A3-35 · critical · integration · c2j:** Resume approved implementation without repeating direction review; changed scope returns to Direction. (`resume.test.yaml`)
- **A3-36 · critical · integration · c2j:** Preserve recorded publication state and avoid another merge when only publication remains. (`resume.test.yaml`)
- **A3-37 · critical · integration · c2j:** Bound each automatic loop independently; discussion grants no attempts, and explicit renewal remains finite. (`limits.test.yaml`, `renewal.test.yaml`)
- **A3-38 · high · integration · c2j:** Deliver selected directories intact and measure current reference-map growth honestly. (`collections.test.yaml`)
- **A3-39 · critical · integration · c2j:** A failed child returns to its requester for a corrected retry without escalating or duplicating prior submissions. (`child-recovery.test.yaml`)

- **A3-40 · high · integration · c2j/Cortex:** Review titles identify the stage; approval buttons describe the authorized action. (`review.test.yaml`, `consumer/feedback.test.tsx`)
- **A3-41 · critical · integration · c2j:** Continue with text or annotations is reconsidered before Backstop resumes a stage. (`backstop.test.yaml`)
- **A3-42 · high · integration · c2j/Cortex:** Questions keep review pending and expose working feedback and attachment controls. (`review.test.yaml`, `backstop.test.yaml`, `consumer/feedback.test.tsx`)
- **A3-43 · critical · integration · c2j:** Declining tools launches no probe and returns the original human notes to the requester. (`packages.test.yaml`)
- **A3-44 · high · unit/integration · Python/cmark:** Missing correction links cannot become an actionable approval; useful attached corrections can open first. (`test_tools.py`, `backstop.test.yaml`)
- **A3-45 · critical · integration · c2j/Git/Nix:** Foreign includes require explicit input-secret authorization and cannot exceed the caller's ceiling. (`reuse-permissions.test.yaml`)
- **A3-46 · high · integration · c2j:** Successful diagnostic collection returns negative findings to the requester; required acceptance probes fail on negative results. (`child-recovery.test.yaml`, `diagnostic-child.test.yaml`)
- **A3-47 · critical · worker integration · Nix/Python/cmark:** The shipped validator imports its declared libraries, parses Markdown and decodes images in separate task environments. (`guides/repros/validator-environment-check.yaml`)

- **A3-48 · critical · integration · c2j:** Invalid or failed Backstop reports retain native human input and accept a corrected continuation. (`backstop.test.yaml`)

- **A3-49 · critical · worker integration · uv/Python/Nix:** Review checks reuse prepared Python libraries across tasks and report missing or corrupt screenshots as corrections. (`tools.test.yaml`, `guides/repros/validator-environment-check.yaml`)

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| A3-50 | Unfixed validation with distinct native candidate and proposal restore packs fails preparation with the workspace collision before validator execution. | Critical | Integration / c2j, Git, Nix | `recipes/adaptive3/tools.yaml`, `recipe-tests/adaptive3/package-restore.yaml`, `recipe-tests/adaptive3/package-restore.test.yaml` |
| A3-51 | Corrected validation executes against the committed candidate, retaining its configuration, marker and revision without persisting validator changes. | Critical | Integration / c2j, Git, Nix | `recipes/adaptive3/tools.yaml`, `recipe-tests/adaptive3/package-restore.test.yaml` |
| A3-52 | Review documents retain their original names, references and contents while other proposal artifacts cannot enter the validator document mount. | Critical | Integration / c2j, Git, Nix | `recipes/adaptive3/tools.yaml`, `recipe-tests/adaptive3/package-restore.test.yaml` |
| A3-53 | Review-only input remains valid and preserves the candidate through native restoration. | High | Integration / c2j, Git, Nix | `recipe-tests/adaptive3/package-restore.test.yaml`, `recipe-tests/adaptive3/tools.test.yaml` |
| A3-54 | Requested nix, uv and pnpm additions pass validation while retaining existing packages and unrelated configuration. | Critical | Integration / c2j, Git, Nix | `recipe-tests/adaptive3/tools.test.yaml`, `recipe-tests/adaptive3/packages.test.yaml` |
| A3-55 | Unsupported apt requests receive the portable-reference finding before any approval, probe or adoption. | Critical | Integration / c2j, Nix | `recipe-tests/adaptive3/tools.test.yaml`, `recipe-tests/adaptive3/packages.test.yaml` |
| A3-56 | Unrelated configuration edits receive the unrelated-configuration finding and cannot advance to probing or adoption. | Critical | Integration / c2j, Nix | `recipe-tests/adaptive3/tools.test.yaml`, `recipe-tests/adaptive3/packages.test.yaml` |
| A3-57 | Removed existing packages, unrequested additions and duplicate packages receive the package-additions finding. | High | Integration / c2j, Nix | `recipe-tests/adaptive3/tools.test.yaml` |
| A3-58 | Adoption succeeds when the current parsed configuration equals the approved proposal and retains existing settings. | Critical | Integration / c2j, Git, Nix | `recipe-tests/adaptive3/tools.test.yaml`, `recipe-tests/adaptive3/packages.test.yaml` |
| A3-59 | Adoption differing from the approved proposal receives the adoption-mismatch finding, including changed unrelated settings or missing approved additions. | Critical | Integration / c2j, Git, Nix | `recipe-tests/adaptive3/tools.test.yaml`, `recipe-tests/adaptive3/packages.test.yaml` |
| A3-60 | Exact policy approval precedes probe launch without requiring human approval. | Critical | Integration / c2j, Nix | `recipe-tests/adaptive3/packages.test.yaml` |
| A3-61 | Requests lacking an exact policy reference and check match require human approval before probe launch. | Critical | Integration / c2j, Nix | `recipe-tests/adaptive3/packages.test.yaml` |
| A3-62 | Human denial preserves feedback and leaves both probing and adoption unexecuted. | Critical | Integration / c2j, Nix | `recipe-tests/adaptive3/packages.test.yaml` |
| A3-63 | A failed probe job or non-passing probe finding prevents adoption and returns a non-passing result. | Critical | Integration / c2j, Nix | `recipe-tests/adaptive3/packages.test.yaml`, `recipe-tests/adaptive3/package-probe.test.yaml` |
| A3-64 | Successful approved probing completes before exact adoption, which passes the real configuration validator. | Critical | Integration / c2j, Git, Nix | `recipe-tests/adaptive3/packages.test.yaml`, `recipe-tests/adaptive3/package-probe.test.yaml` |
| A3-65 | Proposal validation executes against the retained candidate even when the proposal workspace and upstream configuration would produce different findings. | Critical | Integration / c2j, Git, Nix | `recipe-tests/adaptive3/package-restore.test.yaml` |
| A3-66 | Independent and specialist assessors receive exact v2 human corrections; absent human feedback remains valid. | High | Integration / c2j, Nix | `recipes/adaptive3/prompts/validate.yaml`, `recipe-tests/adaptive3/validation-feedback.test.yaml` |
| A3-67 | Preparation reviewers receive exact human choices and messages, including Unicode, whitespace and line breaks. | Critical | Integration / pinned c2j, scripted Codex | `recipes/adaptive3/prompts/review.yaml`, `recipe-tests/adaptive3/review.test.yaml` |
| A3-68 | Implementation reviewers receive exact human choices and messages from the current correction envelope. | Critical | Integration / pinned c2j, scripted Codex | `recipes/adaptive3/prompts/review.yaml`, `recipe-tests/adaptive3/review.test.yaml` |
| A3-69 | Stale direct feedback cannot replace a human correction supplied through the current envelope. | Critical | Integration / pinned c2j, scripted Codex | `recipes/adaptive3/prompts/review.yaml`, `recipe-tests/adaptive3/review.test.yaml` |
| A3-70 | Reviews without human feedback remain valid and do not invent instructions. | High | Integration / pinned c2j, scripted Codex | `recipes/adaptive3/prompts/review.yaml`, `recipe-tests/adaptive3/review.test.yaml` |

## Document details

| Expectation | Files | Priority | Level; dependencies |
| --- | --- | --- | --- |
| Producer reports require complete typed document details, including exact IDs and reading priority. | `test_schemas.py`, `../../recipes/adaptive3/schemas.yaml` | critical | unit; PyYAML, jsonschema |
| Invalid coverage, text, primary agreement or native presentation size returns correction findings before human review. | `test_tools.py`, `tools.test.yaml` | critical | unit/integration; Pillow, cmark, c2j |
| Corrected metadata receives full validation and reaches exactly one human review. | `lifecycle.test.yaml`, `cycle.test.yaml` | critical | integration; c2j |
| Replacement, reuse and question replies retain only the selected documents and their current descriptions. | `cycle.test.yaml`, `review.test.yaml` | critical | integration; c2j |
| Tool and recovery reviews require checked details; failed preparation remains a document-free question. | `packages.test.yaml`, `backstop.test.yaml`, `resume.test.yaml` | critical | integration; c2j |
| Generated forms display explicit titles, purposes and roles through the real reader while preserving drafts. | `consumer/feedback.test.tsx` | critical | integration; Cortex, locked UI tools |
| Independent validation rejects misleading titles and irrelevant purposes with concrete rewrites, then accepts corrected descriptions. | `../../guides/repros/misleading-document-details-check.yaml` | critical | live worker integration; c2j, Codex |


## Outcome-only change-count validation

Defined in the approved preparation before implementation. Scripted assessments test routing, not live model judgment.

| Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- |
| Non-Outcome general and specialist assessors receive no requirement to supply the Outcome change-count report. | Critical | Integration / c2j, Nix | `recipes/adaptive3/prompts/validate.yaml`; `recipe-tests/adaptive3/change-count-scope.test.yaml` |
| Outcome assessors require measured per-file totals, cell/category classification, honest binary entries and verified delegated results. | Critical | Integration / c2j, Nix | `recipes/adaptive3/prompts/validate.yaml`; `recipe-tests/adaptive3/change-count-scope.test.yaml` |
| Outcome's general assessor receives native measurements matching the candidate's text changes and binary entries. | Critical | Integration / c2j, Git, Nix | `recipes/adaptive3/validate.yaml`; `recipes/adaptive3/tools.yaml`; `recipe-tests/adaptive3/reporting.test.yaml` |
| Missing, invented or inconsistent Outcome reports require concrete correction before acceptance. | Critical | Integration / c2j, Nix; scripted assessment | `recipes/adaptive3/prompts/validate.yaml`; `recipe-tests/adaptive3/reporting.test.yaml` |
| Implementation with passing required checks can advance without an Outcome change-count artifact. | Critical | Integration / c2j, Git, Nix; scripted assessment | `recipes/adaptive3/validate.yaml`; `recipe-tests/adaptive3/change-count-scope.test.yaml` |
| Genuine Implementation findings repeat all required checks after correction. | Critical | Integration / c2j, Git, Nix; scripted assessment | `recipes/adaptive3/lifecycle.yaml`; `recipe-tests/adaptive3/lifecycle.test.yaml` |
| Failed required verification prevents acceptance even when the assessor reports success. | Critical | Integration / c2j, Git, Nix | `recipes/adaptive3/validate.yaml`; `recipe-tests/adaptive3/lifecycle.test.yaml` |
| Every phase retains factual, behavioral, dependency and required-check validation in its generated assessor instructions. | Critical | Integration / c2j, Nix | `recipes/adaptive3/prompts/validate.yaml`; `recipe-tests/adaptive3/change-count-scope.test.yaml` |
| Direction continues requiring its per-cell scope table without requiring Outcome measurements. | High | Integration / c2j, Nix | `recipes/adaptive3/prompts/validate.yaml`; `recipe-tests/adaptive3/change-count-scope.test.yaml` |
| A complete, consistent Outcome report reaches human review without a reporting correction. | Critical | Integration / c2j, Git, Nix; scripted assessment | `recipes/adaptive3/validate.yaml`; `recipe-tests/adaptive3/reporting.test.yaml` |
| Corrected Outcome reports are assessed against freshly delivered candidate measurements before acceptance. | Critical | Integration / c2j, Git, Nix; scripted assessment | `recipes/adaptive3/validate.yaml`; `recipe-tests/adaptive3/reporting.test.yaml` |
| Candidate measurements preserve exact text additions and removals while leaving binary line counts uncountable. | High | Unit / Python, PyYAML, Git | `recipes/adaptive3/tools.yaml`; `recipe-tests/adaptive3/test_tools.py` |

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| A3-75 | Delivery reuses two author sessions and one independent assessor across phases, questions, and corrections. | Critical | Integration / c2j | default-build.test.yaml, discussion-context.test.yaml |
| A3-76 | Invalid review output returns to its author before rebase, verification, or assessment. | Critical | Integration / c2j | reporting.test.yaml, lifecycle.test.yaml |
| A3-77 | Failed verification reaches the implementer with the original evidence before independent assessment. | Critical | Integration / c2j | hook-recovery.test.yaml |
| A3-78 | Verification starts from the prepared latest upstream candidate and retains matching passing evidence after a report correction. | Critical | Integration / c2j, Git | candidate-flow.test.yaml, candidate-conflict.test.yaml |
| A3-79 | After upstream advancement, an equivalent rebased change with fresh passing verification merges under the original approval. | Critical | Integration / c2j, Git | integration.test.yaml |
| A3-80 | A same-cell consultation returns to the requester without launching an owner session. | Critical | Integration / c2j | publication-ref.test.yaml |
| A3-81 | Successful merge and skipped publication complete from native results without further assessment. | Critical | Integration / c2j, Git | default-build.test.yaml |

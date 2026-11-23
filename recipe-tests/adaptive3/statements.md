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
- **A3-44 · high · unit/integration · Python/cmark:** Missing correction links cannot authorize work; the native diagnosis opens before useful supporting corrections. (`test_tools.py`, `backstop.test.yaml`)
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
| Tool reviews require checked details; Backstop retains a readable native report when supporting-file preparation fails. | `packages.test.yaml`, `backstop.test.yaml`, `resume.test.yaml` | critical | integration; c2j |
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
| A3-82 | Candidate verify-hook edits run before merge, with failures and diagnostics returned to the implementer for repair. | Critical | Integration / c2j, Git, Nix | `recipes/adaptive3/verify-candidate.yaml`, `recipe-tests/adaptive3/lifecycle.test.yaml` |
| A3-83 | Recipes verification runs the repository-wide CI checks for a change in any target directory and reports failed checks to the agent. | Critical | Integration / c2j, Git, Nix, Python | `.c2/recipes/hooks/build/verify.yaml`, `.github/workflows/recipes.yml`, `scripts/test-recipes.sh` |
| A3-84 | A Git consumer proceeds after upstream delivery succeeds. A consumer awaiting a manual package release requests human confirmation after delivery succeeds. | High | Integration / sampled Adaptive3 jobs | `recipes/adaptive3/prompts/context.yaml` |
| A3-85 | Plans and assessments use candidate evidence before merge and evaluate requested releases after publication. | High | Integration / sampled Adaptive3 jobs | `recipes/adaptive3/prompts/execute.yaml`, `recipes/adaptive3/prompts/validate.yaml` |
| A3-86 | A local dependency update proceeds from passing focused compatibility checks without routine owner confirmation. | High | Integration / sampled Adaptive3 jobs | `recipes/adaptive3/prompts/context.yaml`, `recipes/adaptive3/prompts/execute.yaml` |
| A3-87 | Owner consultations identify a concrete issue, a question that could change the plan, or required external work, and carry relevant evidence. | High | Integration / sampled Adaptive3 jobs | `recipes/adaptive3/prompts/context.yaml`, `recipes/adaptive3/prompts/execute.yaml` |

The accepted pnpm correction replaces the former late-adoption checks in A3-57–61
with comparison before writing. Duplicate references have a specific finding;
automatic legacy policy matching remains applicable to uv/Nix. The original
34 saved-candidate R/G/H/D expectations remain separate review artifacts.

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| A3-88 | Approved bindings retain the original baseline, proposal artifact and exact references/checks through isolated validation and parent adoption. | Critical | Integration / pinned c2j | `packages.test.yaml`, `package-probe-binding.test.yaml`, `package-binding-child.test.yaml` |
| A3-89 | Altered approved inputs, substituted artifacts and unexpected additions leave configuration unchanged and never reach a fresh probe. | Critical | Integration / pinned c2j | `package-probe-binding.test.yaml` |
| A3-90 | A fresh probe prepares accepted packages after bounded staging; failed setup prevents its body from running. | Critical | Integration / pinned c2j, uv | `package-probe.test.yaml`, `package-preparation-failure.test.yaml` |
| A3-91 | Concurrent configuration changes cause parent adoption conflicts after successful child validation, preserving current bytes. | Critical | Integration / pinned c2j | `packages.test.yaml`, `test_tools.py` |
| A3-92 | Unchanged authorized retries probe successfully without rewriting configuration; changed requests cannot reuse the prior binding. | Critical | Integration / pinned c2j, uv | `package-retry.test.yaml`, `test_tools.py` |
| A3-93 | Legacy pnpm policy matches still require review; questions and withdrawal prevent installation, and newer human scope returns to direction. | Critical | Integration / pinned c2j | `packages.test.yaml` |
| A3-94 | Symlinks, malformed packages and mid-comparison configuration changes fail before replacement and preserve unrelated files. | Critical | Unit / Python, yq | `test_tools.py` |

Preparation-order checks use a real failing uv setup and a following native task
for rejected additions; command-entry order alone is insufficient. These fixtures
do not establish private pnpm dependency-build behavior, worker/cache replacement,
or a real interrupted durable continuation. Existing scripted `resume.test.yaml`
cases exercise routing and remain distinct from that missing continuation coverage.

A corrected Backstop resume fixture must supply valid retained review descriptions
before offering Continue; invalid earlier collections remain blocked. This exercises
existing review safeguards, not a worker restart. (`backstop-resume.test.yaml`;
critical, integration, pinned c2j.)

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| A3-95 | Direction framing explains applicable private pnpm authority before scheduling scoped tool consumption. | Critical | Integration / pinned c2j | `build.test.yaml` |
| A3-96 | Boolean and numeric settings remain distinct in approved proposals, concurrent conflicts and already-applied retries; rejected changes preserve current configuration. | Critical | Unit and integration / Python, yq, pinned c2j | `test_tools.py`, `package-types.test.yaml` |
| A3-97 | Native setup records show approved additions only after staging, and exclude child-warmed additions from parent preparation following rejected adoption. | Critical | Integration / pinned c2j, uv | `package-preparation.test.yaml`, `../checks/package_preparation.py` |
| A3-98 | Symlinks, unsafe configuration parents and rejected inputs preserve configuration and targets without cold-installing or probing proposed additions; paired healthy controls install and probe. | Critical | Integration / pinned c2j, synthetic uv | `package-negative-preparation.cases.yaml`, `../checks/package_negative_preparation.py` |
| A3-99 | Bounded adoption preserves the proposal or latest review session without starting another author task. | High | Integration / pinned c2j | `packages.test.yaml`, `packages.yaml` |
| A3-100 | Verification records candidate and runtime identities, runs shared checks and retains failure reports. | High | Integration / c2j, Go, Python, Nix | `.c2/recipes/hooks/build/verify.yaml`, `scripts/test-recipes.sh`, `../repository-verify.test.yaml` |
| A3-101 | Verification collects orphaned fixture processes before they exhaust worker capacity, preserving successful results and failure diagnostics. | High | Integration / Python, pinned c2j, tini, Linux procfs | `.c2/recipes/hooks/build/verify.yaml`, `../repository-verify.test.yaml`, `../fixtures/check-orphan-reaping.py` |
| A3-102 | Shared verification executes configuration-validator and response-schema tests; a failing test stops verification and preserves its diagnostic log. | Critical | Unit/integration / Python, PyYAML, Pillow, jsonschema, cmark, yq, Git | `scripts/test-recipes.sh`, `test_tools.py`, `test_schemas.py` |
| A3-103 | Local, templated and option-like package references fail before configuration writes; exact registry and remote requests remain usable. | Critical | Unit / Python, PyYAML, yq, Git | `test_tools.py`, `recipes/adaptive3/tools.yaml` |
| A3-104 | Duplicate YAML mapping keys reject proposal binding and staging/adoption, preserving configuration bytes, identity and permissions. | Critical | Unit/integration / Python, PyYAML, yq, pinned c2j, Git | `test_tools.py`, `duplicate-config-keys.test.yaml`, `package-probe.test.yaml`, `recipes/adaptive3/tools.yaml` |
| A3-105 | Valid YAML aliases, merge overrides and scalar spellings retain existing configuration meaning during approved additions. | High | Unit / Python, PyYAML, yq, Git | `test_tools.py`, `recipes/adaptive3/tools.yaml` |
| A3-106 | Cold-install controls prepare validator Python dependencies using the real environment tool, while synthetic repository-package installs retain exact allowlists and isolated logs. | Critical | Unit/integration / Python, uv, pinned c2j, Nix | `preparation-installer/uv`, `test_preparation_installer.py`, `../checks/package_negative_preparation.py` |
| A3-107 | Unknown installer commands and unexpected repository packages reject without invoking the real installer; Python preparation failures remain failures. | Critical | Unit / Python, shell | `preparation-installer/uv`, `test_preparation_installer.py` |

## Preparation review and cross-cell negotiation

| Expectation | Files | Priority | Level and dependencies |
| --- | --- | --- | --- |
| A standard delivery presents the one-pager, design and acceptance criteria together before implementation. Incomplete packets return to planning. | adaptive3.yaml, recipes/adaptive3/validate.yaml | High | Integration, c2j |
| A full approval completes verified work within the reviewed scope. A changed plan requires a fresh decision. | recipes/adaptive3/review.yaml, adaptive3.yaml | High | Integration, c2j |
| A short assignment goes directly to implementation and requires human Outcome acceptance. | adaptive3.yaml | High | Integration, c2j |
| A receiving owner can request evidence or propose an alternative. Delivery starts only on mutually agreed terms. | recipes/adaptive3/consultation.yaml | High | Integration, c2j |
| Parent and child reviews expose each relevant request, its origin, the agreement and its transcript even when delivery stalls. | recipes/adaptive3/consultation.yaml, recipes/adaptive3/backstop.yaml | High | Integration, c2j |

## Backstop human instructions and current-job recovery

The latest human direction defers native cancellation and supersession. Cancellation
stays manual; prefer phase returns within this job. These expectations supplement
the earlier recovery checks and supersede their report-free fallback expectations.
All filenames below are relative to `recipe-tests/adaptive3/`.

| Expectation | Files | Importance | Coverage and dependencies |
| --- | --- | --- | --- |
| Clear human instructions return once with original words and a native receipt, without a second Apply. | `backstop-instructions.test.yaml` | critical | integration; c2j |
| Polite instructions through Ask a question can authorize the precise correction; informational questions remain discussion. | `backstop-instructions.test.yaml`, `backstop.test.yaml` | critical | integration; c2j |
| A validated scope amendment returns to Preparation for approval of the revised plan. | `backstop-amendment.test.yaml` | critical | integration; c2j |
| Changed Direction, plans or candidates block later returns that depend on superseded results. | `backstop-policy.test.yaml` | critical | integration; c2j |
| Short-path recovery uses the current Direction. An Outcome from a superseded plan cannot authorize integration of the same candidate. | `backstop-policy.test.yaml` | critical | integration; c2j |
| Current native prerequisites permit forward returns; missing prerequisites withhold Apply. | `backstop-instructions.test.yaml`, `backstop-policy.test.yaml` | critical | integration; c2j |
| Amendment validation reads original attached notes while retaining the current revised direction. | `backstop-validation-notes.test.yaml` | critical | integration; c2j |
| Configure recovery retains its selected next phase after configuration completes. | `backstop-configure.test.yaml` | high | integration; c2j |
| An explicit larger allowance applies to the paused loop on the next matching visit. | `backstop-return.test.yaml`, `renewal.test.yaml` | critical | integration; c2j |
| Phase changes and replayed human receipts cannot renew automatic allowances indefinitely. | `backstop-return.test.yaml`, `renewal.test.yaml` | critical | integration; c2j |
| Escalation shows origin, progress, blocker, options and research; agent failure retains a readable stored report. | `backstop-instructions.test.yaml`, `consumer/browser-backstop.yaml` | high | integration; c2j, Cortex, Chromium |
| Removing the phone criterion refreshes Direction, Preparation, verification and Outcome acceptance while browser validation remains required. | `backstop-scope-flow.test.yaml` | critical | integration; c2j |
| Backstop checks run before the repository suite; early failures retain focused diagnostics. | `repository-verify.test.yaml`, `../repository-verify.test.yaml` | high | integration; c2j, Nix |
| Provider failures retain a readable report and reject unavailable model-setting edits. | `models.test.yaml` | critical | integration; c2j |
| Human cancellation stays terminal and cannot trigger automatic replacement. | `cancellation.test.yaml` | critical | integration; c2j |
| Prior-job Configure recovery defaults omitted or null destinations to Direction without consuming another recovery attempt. | `backstop-configure-recovery.test.yaml` | critical | integration; c2j |

## Phase retries and Backstop

| Expectation | Files | Importance | Test |
| --- | --- | --- | --- |
| Each phase visit starts with fresh counts. Retries within the visit use its allowance. | `adaptive3.yaml`, `recipes/adaptive3/lifecycle.yaml` | Critical | Integration, c2j |
| Fresh human instructions renew phase, merge and Backstop allowances once, including instructions forwarded from another review. | `recipes/adaptive3/retry.yaml`, `adaptive3.yaml` | Critical | Integration, c2j |
| Newly confirmed checks restore both automatic returns. Repeated evidence and phase changes alone spend or preserve the remaining allowance. | `recipes/adaptive3/retry.yaml`, `recipes/adaptive3/hooks.yaml` | Critical | Integration, c2j |
| Backstop can act on a clear Preparation revision using its original receipt without requesting confirmation again. | `recipes/adaptive3/backstop.yaml` | Critical | Integration, c2j |
| A plan revised after another decision keeps its thread. The intervening decision and the final outcome have independent review IDs. | `adaptive3.yaml`, `recipe-tests/adaptive3/backstop-scope-flow.test.yaml` | Critical | Integration, c2j |
| After answering a question Backstop reassesses its blocker, takes an authorized action, or presents the remaining question. | `recipes/adaptive3/discussion.yaml`, `recipes/adaptive3/backstop.yaml` | Critical | Integration, c2j |
| Equivalent evidence can cover a suggested check. A broken promise or missing expressly required check returns to its author. | `validation-feedback.test.yaml`, `build.test.yaml` | Critical | Integration, c2j |
| A verified report correction reaches Outcome with the earlier approval. A code defect returns to Implementation. | `pilot-routing.test.yaml` | Critical | Integration, c2j |
| A fresh author and each repair receive the current finding and the reviewer’s recorded words and uploads. A newer reply replaces them. | `lifecycle.test.yaml`, `review-reply.test.yaml`, `pilot-routing.test.yaml` | High | Integration, c2j |
| A second unchanged named failure uses the delegate. A newly passing check renews repair. | `repair-progress.test.yaml` | High | Unit, c2j |
| An explanation ends at the receiver’s answer. Only the requester can open negotiation for a change. | `consultation.test.yaml` | Critical | Integration, c2j |
| An agent in a consuming cell can read its offline guide and inherit worker defaults or use explicit overrides. | `agent-settings.test.yaml` | High | Integration, c2j and c2ops |
| Fresh agents learn to request missing worker tools because manual installs may disappear between tasks. | `agent-settings.test.yaml` | High | Integration, c2j and c2ops |
| A person sees the blocker and suggested action before the job history. The original request and evidence remain readable. | `backstop.test.yaml`, `backstop-report.yaml` | High | Integration, c2j |

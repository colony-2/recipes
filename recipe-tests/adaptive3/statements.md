# Adaptive3 test statements

All integration cases use the pinned c2j runtime and disposable cell repositories.
Agent decisions are scripted unless a case is explicitly marked live.

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| A3-01 | Each accepted delivery stage advances directly after Execute, complete validation and Review. | Critical | Integration / c2j, Nix | adaptive3.yaml, lifecycle.yaml, cycle.yaml |
| A3-02 | A correction reruns all checks before review, even when only one check failed. | Critical | Integration / c2j, Nix | lifecycle.yaml, validate.yaml |
| A3-03 | Human questions retain the pending item without executing work or consuming automatic attempts. | Critical | Integration / c2j, Nix | review.yaml |
| A3-04 | Human changes reach Execute with original wording and supersede conflicting generated plans. | Critical | Integration / c2j, Nix | review.yaml, prompts/execute.yaml |
| A3-05 | Validation and human review receive the same corrected artifact identities without historical overlays. | Critical | Integration / c2j, Nix | cycle.yaml, tools.yaml, review.yaml |
| A3-06 | Large diagnostics remain available without corrupting bounded control outputs. | Critical | Integration / c2j, Python | tools.yaml |
| A3-07 | Planning, validation and review cannot persist repository edits; implementation can. | Critical | Integration / c2j, Nix | agent.yaml, execute.yaml |
| A3-08 | Caught execution failures enter same-job resolution and can resume successfully. | Critical | Integration / c2j, Nix | adaptive3.yaml, resolver.yaml |
| A3-09 | Consultation runs in the receiving cell and sends its agreed assignment directly to child execution. | Critical | Integration / c2j, Nix | consultation.yaml |
| A3-10 | Nested owner advice retains the suspended conversation without creating an advice job. | High | Integration / c2j, Nix | consultation.yaml |
| A3-11 | Package probes cannot run before policy or human approval, and adoption preserves unrelated configuration. | Critical | Integration / c2j, Nix | packages.yaml, package-probe.yaml, tools.yaml |
| A3-12 | Missing required verification and failed publication remain correctable rather than silently succeeding. | Critical | Integration / c2j, Nix | hooks.yaml, validate.yaml, execute.yaml |
| A3-13 | Unchanged rebases reuse approval after full validation; changed edits require review. | Critical | Integration / c2j, Git | tools.yaml, review.yaml, integration.yaml |
| A3-14 | New sessions receive instructions; resumed sessions receive current tasks without another instruction insertion. | High | Integration / c2j, Nix | agent.yaml, prompts/ |
| A3-15 | Prompt includes create no worker tasks and preserve literal caller text. | High | Integration / c2j | prompts/ |
| A3-16 | Cancellation retains its meaning and never silently recreates cancelled work. | Critical | Integration / c2j | lifecycle.yaml, consultation.yaml |
| A3-17 | Real UI reviews contain readable captures linked from the selected human document. | High | Live integration / Codex, browser | validate.yaml, tools.yaml |
| A3-18 | Default build uses adaptive3; the explicit adaptive2 entrypoint remains available. | Critical | Integration / c2j | build.yaml, adaptive3.yaml, recipes/adaptive2/build.yaml |
| A3-19 | A failed resolver correction asks for human direction before another automatic attempt, even when the error message changes. | Critical | Integration / c2j, Nix | resolver.yaml, adaptive3.yaml |
| A3-20 | Review actions expose feedback entry and preserve questions, changes and uploads through submission. | Critical | Integration / c2j, Cortex renderer | review.yaml, resolver.yaml |
| A3-21 | Required specialist findings prevent acceptance until full validation passes; optional advice has no independent veto. | Critical | Integration / c2j, Nix | validate.yaml, specialists.yaml |
| A3-22 | Configured assessment guidance reaches general and specialist assessors with current human scope and original diagnostic references. | High | Integration / c2j, Nix | validate.yaml, prompts/validate.yaml |
| A3-23 | Repeated resolver discussion preserves the previous proposal and human context without executing work before explicit continuation. | High | Integration / c2j, Nix | resolver.yaml |

| A3-24 | Incomplete receiver titles return through full validation before child submission. | consultation.test.yaml | critical | integration, c2j |
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

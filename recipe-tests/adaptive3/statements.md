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

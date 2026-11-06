# Close the remaining recipe test gaps

Scope fits this cell: recipe contracts, declarative fixtures, and CI. Runtime
lifecycle controls belong to c2j; packaged operation delivery belongs to c2ops.
Custom consultation selection remains on hold pending the hook-workspace decision.

## Implementation plan

1. Collect diagnostics from actual native failure envelopes, including wrapped
   causes. Route failed child attempts and hook failures through the same helper.
   Test real command, extension, and setup failures and materialize their files.
2. Preserve original evidence paths. Give recipe summaries, returned files, and
   failure diagnostics separate directories; test overlapping names and contents.
3. Isolate package adoption guards, assert the precise error, add successful
   adoption, and remove each guard in a temporary copy to prove test sensitivity.
4. Exercise adaptive continuation export/import, session reuse, and nested advice.
   Investigate native goal replacement and interrupted execution controls; use
   existing c2j capabilities and specify missing reusable harness support upstream.
5. Exercise actual hook/include authority with synthetic secrets, both permitted
   and denied. Make CI runtime selection reproducible and require an authored
   packaged-operation smoke test before broad suites.

## Acceptance statements

Each statement is an integration expectation; tests use deterministic model
responses. Dependencies: c2j and Git; packaged smoke additionally requires Nix
and the colony2 cache. Guard tests additionally require Python.

| ID | Priority | Expectation | Relevant files |
| --- | --- | --- | --- |
| TG1 | critical | Failed attempts retain native command and extension logs in the repair inbox, including wrapped failures. | await-goal.yaml, error-documents.yaml |
| TG2 | critical | Setup failures retain their real message without inventing execution logs. | error-documents.yaml, hook-verify.yaml |
| TG3 | critical | Distinct source files survive naming collisions with summaries, execution logs, and directory-like prefixes. | error-documents.yaml, verify.yaml |
| TG4 | critical | Concurrent config changes prevent adoption even when candidate validation is valid. | package-tools.yaml, package-adoption-guard.test.yaml |
| TG5 | critical | A mismatched validation digest prevents adoption even when the base is current. | package-tools.yaml, package-adoption-guard.test.yaml |
| TG6 | high | Matching base and validation digests permit adoption of exactly the validated configuration. | package-adoption-guard.test.yaml |
| TG7 | high | Restoring adaptive consultations preserves transcript, sessions, results, and iteration limits without repeating completed advice or reviews. | consultation.yaml, consultation-start.yaml |
| TG8 | high | Authorized hooks can resolve their synthetic secret through a local include; absent or limited authority denies access. | hook-verify.yaml, hook-authority.test.yaml |
| TG9 | high | Authored packaged agent operations prepare successfully on the recorded runtime before deterministic regression suites run. | .github/workflows/recipes.yml |
| TG10 | critical | A failed child attempt leaves its goal open for recovery while its diagnostic files remain readable. | failure-evidence.test.yaml, goal-attempt-errors.yaml |

Record actual results and remaining external dependencies in an implementation
assessment. A mocked lifecycle result is not a tested runtime transition.

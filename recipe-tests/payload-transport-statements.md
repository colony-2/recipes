# Value artifact transport test statements

Defined before migration. Tests use synthetic data; the private job export is not a fixture.

| Priority | Kind / dependencies | Files | Expectation |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Nix, mocked agents | `recipes/develop/develop.yaml`, `recipes/light/develop.yaml` | Large contexts reach agents intact without context-writer tasks or bulk process environment values. |
| Critical | Integration / c2j | `recipes/light/develop.yaml`, `create.yaml` | Handoffs and creation manifests preserve completed work, references, and outcomes through value artifacts. |
| Critical | Integration / c2j | `recipes/kernel/consultation.yaml` | Transcripts remain stored, readable, and resumable without embedding their content in process arguments or environment. |
| Critical | Integration / c2j | `recipes/kernel/review.yaml`, `recipes/kernel/repair.yaml` | Large feedback and correction evidence preserve every character and never grant approval implicitly. |
| Critical | Integration / c2j, Python | `recipes/light/synopsis.yaml`, `recipes/develop/merge-review.yaml` | File-based renderer inputs preserve validation, reject invalid accounting, and reject failed verification. |
| High | Integration / c2j | `recipes/build/hooks/settings.yaml` | Normalized settings remain available to later hooks without a dedicated settings-writer task. |
| Critical | Integration / c2j | `recipe-tests/value-artifact-smoke.test.yaml`, `recipe-tests/payload-documents.test.yaml` | Unicode, quotes, newlines, template syntax, and shell metacharacters remain literal document data. |

# Hook workspace behavior

These expectations replace recipe hash guards with c2j's inherited `const` behavior.

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| HC-1 | Configure, design research, verification, and publication discard repository edits while returning their reports and artifacts. | Critical; integration, c2j/Git | `recipes/adaptive/hook-*.yaml`, `hook-const.test.yaml` |
| HC-2 | Nested hooks cannot persist edits by declaring `const: false`; prepare can still save generated files. | Critical; integration, c2j/Git | `hook-const.test.yaml`, `recipes/adaptive/hook-prepare.yaml` |
| HC-3 | Planning follows an advanced branch through missing or present read-only hooks without reporting a hook mutation. | Critical; integration, c2j/Git | `hook-const.test.yaml`, `recipes/adaptive2/workflow.yaml` |
| HC-4 | Hook command failures preserve their original diagnostics after attempted repository edits are discarded. | Critical; integration, c2j/Git | `verification-preservation.test.yaml`, `recipes/adaptive/hook-verify.yaml` |
| HC-5 | A public build completes after configure attempts repository edits; those edits never reach the merged result. | Critical; integration, c2j/Git/Nix | `../adaptive2/build-delivery.test.yaml` |
| HC-6 | Hook permission grants and restrictions still apply through nested includes. | Critical; integration, c2j/Git | `hook-authority.test.yaml` |

## Validation — 2026-11-11

All 41 unique cases pass using c2j v0.0.124, native temporary Git repositories,
hook execution, artifact transport, and scripted model responses:

| Suite | Passing cases |
| --- | ---: |
| `hook-const.test.yaml` | 4 |
| `verification.test.yaml` | 16 |
| `verification-preservation.test.yaml` | 2 |
| `hook-authority.test.yaml` | 3 |
| `../adaptive2/build-delivery.test.yaml` | 10 |
| `flow.test.yaml`: publication edits discarded; invalid publication YAML | 2 |
| `../self-improvement/build.test.yaml` | 4 |

The missing-evidence case passed after removing a required mock for the deleted
startup hash-reading command. Its expected artifact-binding failure remains.
The other cases passed their initial runs. Repository structural checks and
`git diff --check` also pass. No live model or external publication was exercised.

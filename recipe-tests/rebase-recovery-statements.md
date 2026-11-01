# Structured rebase recovery test statements

These extend conflict propagation with bounded recovery; all other failure expectations remain supported.

| Importance | Level / dependencies | Files | Statement |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | Restored native conflicts return to implementation with the existing session, request, approved documents, target hashes, conflict paths, and readable diagnostic artifacts. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | Two unsuccessful repairs exhaust the allowance; the third conflict preserves its native failure and never publishes. |
| Critical | Integration / c2j, Git, Nix | `build.yaml`, `recipes/kernel/rebase-recovery.yaml` | Revisions, merge chases, and light-to-heavy escalation preserve conflict repair counts and originating evidence. |
| Critical | Integration / c2j, Git | `recipes/kernel/rebase-recovery.yaml` | Repaired candidates undergo native rebase and fresh validation and approval before publication. |
| Critical | Integration / c2j | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | Unsupported, malformed, unrestored, unrelated, and unclassified failures propagate without automatic conflict repair. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | A failed repair fails the build while the story retains the originating conflict and its diagnostics. |
| High | Integration / c2j, Git | `recipes/light/agent.yaml`, `recipes/develop/agent.yaml` | Recovery starts from a clean restored candidate and can reconcile it against the recorded target without an existing rebase session. |
| High | Integration / c2j, Git, Nix | `recipe-tests/merge-chase.test.yaml` | Nonconflicting upstream chases retain permitted approval reuse and their independent three-chase limit. |

# Verification failure recovery

This corrects the previously tested job-failure behavior for verification exceptions.
Hook validation remains strict; unsuccessful verification now returns to implementation.

| Importance | Level / dependencies | Files | Statement |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Git | `recipes/develop/verify.yaml` | Invalid hooks, report errors, command failures, timeouts, and denied capabilities produce failed verification with readable diagnostics. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | Every unsuccessful verification returns to the implementation session before approval or publication. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | Missing or skipped required verification returns to implementation to configure or repair the hook. |
| Critical | Integration / c2j, Git, Nix | `recipes/develop/verify.yaml`, `recipes/build/hooks/report.yaml` | Reserved artifact exports remain invalid and reach implementation with their names and original failure origin. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` | A repaired hook must pass fresh verification and normal review; previous approval cannot bypass the checks. |
| High | Integration / c2j, Git | `recipes/develop/verify.yaml` | Failure diagnostics survive later task restoration without rebinding invalid hook artifacts. |
| Critical | Integration / c2j | `recipes/develop/verify.yaml` | Cancellation remains cancellation; failures outside verification keep their existing propagation. |

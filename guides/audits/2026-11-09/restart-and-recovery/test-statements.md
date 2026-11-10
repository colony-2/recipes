# Test statements

| Expectation | Priority | Kind / dependencies | Files |
| --- | --- | --- | --- |
| A recovered parent continues a prior receiver assignment without repeating consultation or approved direction review. | Critical | Integration / native c2j, Nix | `cross-parent-recovery.test.yaml`, `coordinate.yaml`, `accepted-handoff.yaml` |
| Only the selected receiver handoff and recovery evidence reach the resumed child. | High | Integration / native c2j, Nix | `cross-parent-recovery.test.yaml`, `coordinate.yaml` |
| Repeating a recovery request reuses the recorded attempt instead of submitting duplicate work. | Critical | Integration / native c2j, Nix | `cross-parent-recovery.test.yaml`, `coordinate.yaml` |
| A completed successful prior attempt is consumed without another execution. | High | Integration / native c2j | `cross-parent-recovery.test.yaml`, `coordinate.yaml` |
| A new assignment without a receiver agreement or recovery source cannot start execution. | Critical | Integration / native c2j | `cross-parent-recovery.test.yaml`, `accepted-handoff.yaml` |
| A recovery source does not bypass comparison with a current receiver agreement. | Critical | Integration / native c2j, Nix | `accepted-recovery.test.yaml`, `accepted-handoff.yaml` |
| Missing approval and changed scope still return to ordinary design review. | Critical | Integration / native c2j, Nix | `approved-recovery.test.yaml`, `recovery-approval.yaml` |
| An active previous attempt is awaited rather than duplicated. | Critical | Integration / native c2j, scripted job status | `recovery-status.test.yaml`, `coordinate.yaml` |
| An unreadable previous attempt returns a useful correction to the working agent. | High | Integration / native c2j, scripted job status | `recovery-status.test.yaml`, `coordinate.yaml` |

Test paths are relative to `recipe-tests/adaptive2/`; production paths to
`recipes/adaptive2/`.

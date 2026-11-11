# Handoff document selection

These expectations precede implementation and extend the existing assignment,
approval, and recovery tests without weakening their scope checks.

| ID | Expectation | Importance; level/dependencies | Files |
| --- | --- | --- | --- |
| HD-1 | New supporting evidence reaches the receiving child without another consultation or attachment approval. | Critical; integration, c2j/Nix/artifacts/children | `handoff-documents.test.yaml`, `recipes/adaptive2/accepted-handoff.yaml` |
| HD-2 | Moving evidence during correction removes its old path from the child's inbox. | Critical; integration, c2j/Nix/artifacts/children | `handoff-documents.test.yaml`, `recipes/adaptive2/develop.yaml` |
| HD-3 | Omitted consultation attachments stay out of subsequent working inboxes while consultation history remains inspectable. | High; integration, c2j/Nix/artifacts | `handoff-documents.test.yaml`, `recipes/adaptive2/develop.yaml` |
| HD-4 | Supporting evidence can be updated without changing the receiver's agreed assignment or triggering byte comparison of attachments. | High; integration, c2j/artifacts | `accepted-recovery.test.yaml`, `recipes/adaptive2/accepted-handoff.yaml` |
| HD-5 | Changed assignments are rejected, the original is restored, and correction sends the original with the current supporting evidence. | Critical; integration, c2j/Nix/artifacts/children | `handoff-documents.test.yaml`, `build-handoff-recovery.test.yaml` |
| HD-6 | Missing assignments and unsafe handoff paths cannot launch children. | Critical; integration, c2j | `handoff.test.yaml`, `recipes/adaptive/handoff.yaml` |

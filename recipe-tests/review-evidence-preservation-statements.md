# Evidence-preservation regression expectations

These statements supplement the approved review plan before corrective implementation. Existing expectations remain unchanged; no requirements are deprecated.

| Priority | Level / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / native c2j, Git, declared Nix Python | `recipes/kernel/review-content.yaml` | Late unclassified security findings remain visible in both the decision brief and evidence ledger regardless of preceding text length. |
| Critical | Integration / native c2j, Git, declared Nix Python | `recipes/kernel/review-content.yaml` | Mixed skipped-hook reports retain unrelated findings while omitting only recognized irrelevant absence boilerplate. |
| Critical | Integration / native c2j, Git, declared Nix Python | `recipes/kernel/review-content.yaml` | Ambiguous reports retain unclassified paragraphs rather than inferring that the whole document is optional-hook boilerplate. |
| Critical | Integration / native c2j, Git, declared Nix Python | `recipes/kernel/review-content.yaml` | Required verification absence remains visible even when a report resembles optional-hook boilerplate. |
| Critical | Integration / native c2j, Git, declared Nix Python | `recipes/kernel/review.yaml`, `recipe-tests/review-brief.test.yaml` | Failed checks and unperformed verification remain visible in published briefs alongside unchanged decisions and artifact references. |
| High | Integration / native c2j, Git, declared Nix Python | `recipes/kernel/review-content.yaml` | Recognized absence-only optional-hook reports remain omitted without changing original attachments or implying successful verification. |

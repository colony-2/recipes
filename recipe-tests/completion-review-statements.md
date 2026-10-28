# Implementation handoff and no-change completion

These expectations replace consultant-session inheritance and unreviewed standalone
light completion. The requested workflow correction takes effect together; no
compatibility period preserves false completion. Fixtures publish this document
as a C2 test artifact before implementation.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Git, Nix | `recipes/develop/coordinate.yaml`, `recipes/light/coordinate.yaml` | Agreed prerequisite work starts a fresh implementation session with the exact agreement artifacts and an explicit execution request. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml` | A light job without changes or children cannot complete successfully before a human accepts its visible no-change rationale. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml` | Rejecting an unjustified no-change outcome returns to implementation; cancellation cannot publish changes or report the request satisfied. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml` | No-change light jobs with successful children may finish without local review; incomplete or failed children cannot justify completion. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/develop.yaml`, `recipes/light/synopsis.yaml` | Changes eliminated by rebasing still require no-change review when no children completed the work. |
| Critical | Integration / c2j, Git, Nix | `recipes/develop/develop.yaml`, `recipes/develop/merge-review.yaml` | Heavy no-change outcomes show an evidence-backed rationale for human acceptance and finish without an empty squash or merge. |
| Critical | Integration / c2j, Git, Nix | `recipes/light/synopsis.yaml`, `recipes/develop/merge-review.yaml` | Missing or blank rationale cannot reach human acceptance; the reviewed document states why the request needs no repository changes. |

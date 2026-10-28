# Merge chase test statements

All statements are integration checks using Git, Nix, the native c2j runner, and mocked model decisions.

- **Critical** — Heavy and light builds rebase upstream advancement and rerun verification; unchanged local changes reuse their existing final approval. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **Critical** — Three chases may succeed; a fourth stale merge preserves its original error without another rebase. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **Critical** — Verification failures after rebasing block review and merge until implementation is corrected. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **Critical** — Revisions and light-to-heavy handoff preserve the consumed chase budget. (`build.yaml`, `recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **Critical** — Unrelated merge errors, squash errors, and rebase conflicts propagate without an upstream-advancement chase. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **High** — An ordinary successful merge consumes no chase and requires only the existing review gates. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)

- **Critical** — Changed reviewed file content, paths, or modes require fresh review after a chase, even when Git rebases cleanly. (`recipes/kernel/git-candidate.yaml`, `recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **Critical** — A chase that eliminates all local changes completes after verification without another review or merge. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)
- **Critical** — Approval reuse applies only to an approved merge chase, never initial no-change completion or implementation repairs. (`recipes/develop/develop.yaml`, `recipes/light/develop.yaml`)

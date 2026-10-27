# c2j compatibility test statements

Defined before the permission migration. Build lifecycle fixtures publish
`build-kernel-statements.md` as an artifact; this file covers the additional
entrypoints and compatibility probes.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, c2ops | `recipes/kernel/agent-turn.yaml`, `recipes/jobs/job-implement.yaml`, `recipes/new-ticket/*.yaml`, `recipes/superpowers/*.yaml`, `recipes/smoke/*.yaml` | Recipe-authored Codex API references resolve without model-secret lease grants, preserving default Git access and child-job submission. |
| Critical | Integration / c2j, c2ops, Nix | `recipes/kernel/agent-turn.yaml` | Fresh and resumed agents can use the authorized Codex credential without exposing its value in results. |
| Critical | Integration / c2j, c2ops, Nix | `recipes/kernel/agent-turn.yaml` | Missing optional Codex credentials preserve provider fallback; other secret access remains denied. |
| High | Integration / c2j, c2ops, Nix | `recipes/jobs/job-implement.yaml`, `recipes/new-ticket/*.yaml` | Implementation and ticket agents can resolve Codex credentials under restricted defaults. |
| High | Integration / c2j, c2ops, Nix | `recipes/superpowers/*.yaml`, `recipes/superpowers/tests/*.yaml`, `recipes/smoke/*.yaml` | Skill-driven agents and session smoke checks can resolve Codex credentials under restricted defaults. |
| High | Integration / c2j, c2ops, Nix | `recipe-tests/fixtures/result-repair.yaml` | Repair fixtures create authorized model sessions before checking repair behavior. |
| Critical | Integration / c2j jobs | `recipes/develop/coordinate.yaml` | Consultation and dependency waits preserve exact-job completion and failure semantics after the wait API migration. |
| High | Integration / c2j, c2ops | `recipes/kernel/agent-turn.yaml`, `recipes/jobs/job-implement.yaml`, `recipes/new-ticket/*.yaml`, `recipes/superpowers/*.yaml`, `recipes/smoke/*.yaml` | Codex reads its configured API URL through the op default; recipes explicitly reference only the API secret. |
| Critical | Integration / c2j, Nix, public Cachix cache | `recipes/kernel/agent-turn.yaml`, `recipe-tests/build-kernel.test.yaml` | Published Codex supports nested build orchestration, explicit secret inputs, session continuation, structured results, and artifact handoff. |
| Critical | Integration / c2j, Nix | `recipe-tests/agent-failure.test.yaml`, `recipe-tests/build-failure.test.yaml` | Published Codex execution failures retain their original message and failing node through nested recipes. |

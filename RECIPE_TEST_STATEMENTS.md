# Recipe Test Statements

These statements are intended to drive `c2j test` cases.

## Statement Catalog

| ID | Test statement | Relevant file(s) | Importance | Type / dependencies | Polarity |
|---|---|---|---|---|---|
| TS-001 | Triage marks appropriate cell jobs as `cell_is_appropriate=true`. | `new-ticket-triage.yaml` | High | Integration (`recipe_case`); deps: `load_cells` command + c2ops `codex` mocks | Positive |
| TS-002 | Triage marks out-of-cell jobs as `cell_is_appropriate=false`. | `new-ticket-triage.yaml` | High | Integration (`recipe_case`); deps: `load_cells` command + c2ops `codex` mocks | Positive |
| TS-003 | Invalid recommended cell yields `recommended_cell_is_valid=false`. | `new-ticket-triage.yaml` | High | Integration (`recipe_case`); deps: `c2j cells --json` command mock | Negative |
| TS-004 | Triage emits a triage decision artifact payload for downstream routing. | `new-ticket-triage.yaml` | Medium | Integration (`recipe_case`); deps: artifact capture | Positive |
| TS-005 | Requirements planning emits `requirements/plan.json`, `requirements/index.md`, and requirement markdown artifacts. | `new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-006 | Requirements outputs expose dependency order and cross-cell flags from planning payload. | `new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: JSON output parsing | Positive |
| TS-007 | Requirements planning accepts user feedback input and returns updated summary outputs. | `new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: input plumbing | Positive |
| TS-008 | Blocking API review sets `api_review_ok=false` and returns blocking issues list. | `new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: contrarian review output | Negative |
| TS-009 | Contrarian review emits `requirements/api-review.json` artifact. | `new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: artifact capture | Positive |
| TS-010 | Planning and review artifacts coexist in one requirements-planning execution. | `new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: multi-artifact output | Positive |
| TS-011 | Implementation uses continue-session path when `session_id` is provided. | `job-implement.yaml` | High | Integration (`recipe_case`); deps: state initial branching | Positive |
| TS-012 | Implementation uses new-session path when `session_id` is absent. | `job-implement.yaml` | High | Integration (`recipe_case`); deps: state initial branching | Positive |
| TS-013 | Implementation returns non-empty `assistant_summary` output for reviewer context and next-session reuse. | `job-implement.yaml` | Medium | Integration (`recipe_case`); deps: c2ops `codex` selector mock outputs | Positive |
| TS-014 | Validation provided-command path persists full and tail validation artifacts. | `job-validate.yaml` | High | Integration (`recipe_case`); deps: `command_execution` mock artifacts | Positive |
| TS-015 | Validation suggested-command path executes and reports pass status. | `job-validate.yaml` | High | Integration (`recipe_case`); deps: `input` + `command_execution` mocks | Positive |
| TS-016 | Validation custom-command path executes and persists output tail artifact. | `job-validate.yaml` | High | Integration (`recipe_case`); deps: `input` + `command_execution` mocks | Positive |
| TS-017 | Validation failure sets `passed=false` and non-zero `exit_code`. | `job-validate.yaml` | High | Integration (`recipe_case`); deps: failure output mapping | Negative |
| TS-018 | Validation outputs stable artifact contract keys for full and tail logs. | `job-validate.yaml` | Medium | Integration (`recipe_case`); deps: output contract | Positive |
| TS-019 | Merge prompts for missing upstream details before approval. | `job-merge.yaml` | High | Integration (`recipe_case`); deps: `input` prompt path | Positive |
| TS-020 | Merge approval `cancel` exits without merge hash output. | `job-merge.yaml` | High | Integration (`recipe_case`); deps: approval branching | Negative |
| TS-021 | Merge approval `merge` returns non-empty `merged_hash`. | `job-merge.yaml` | High | Integration (`recipe_case`); deps: `squashrebasemerge` mock | Positive |
| TS-022 | Prompted merge path executes merge and returns prompted target branch. | `job-merge.yaml` | High | Integration (`recipe_case`); deps: prompt + merge path | Positive |
| TS-023 | Merge outputs expose `target_branch` from merge operation result. | `job-merge.yaml` | Medium | Integration (`recipe_case`); deps: output mapping | Positive |
| TS-024 | `c2j test compile` generates canonical IR JSON artifact. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test compile` | Positive |
| TS-025 | `c2j test validate` returns non-zero when case filters select no cases. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test validate` | Negative |
| TS-026 | `c2j test run` writes `summary.json`, `summary.md`, and per-case results. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test run` | Positive |
| TS-027 | Scenario markdown without fenced YAML/JSON fails compile. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test compile` | Negative |
| TS-028 | Implementation planning emits `implementation/plan.json`, `implementation/index.md`, and per-requirement markdown artifacts. | `new-ticket-implementation-planning.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-029 | Implementation planning outputs expose dependency gating fields and dependency order. | `new-ticket-implementation-planning.yaml` | High | Integration (`recipe_case`); deps: JSON output mapping | Positive |
| TS-030 | Blocking compatibility review sets `compat_review_ok=false` and returns blocking issues. | `new-ticket-implementation-planning.yaml` | High | Integration (`recipe_case`); deps: contrarian review output | Negative |
| TS-031 | Approved implementation plan requiring dependency jobs starts child jobs and enters waiting state. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: `recipes.run` + child recipe mocks | Positive |
| TS-032 | Merge decision `cancel_job` updates workflow to cancelled path without merge. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: input branching | Negative |
| TS-033 | Merge request without local hash returns to implementation instead of executing merge. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: ready-to-merge branching | Negative |
| TS-034 | Successful merge path marks job completion (`job_done=true`) with non-empty merged hash. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: `local_hash` input + `squashrebasemerge` mock | Positive |
| TS-035 | Implementation-reported cross-cell bugs start child bug jobs before continuing workflow. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` pendingDependencies + `recipes.run` mock | Positive |
| TS-036 | Implementation user questions pause flow for structured user input, then continue the same Codex session. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` incompleteCategory + `input` + repeated selector mock | Positive |
| TS-037 | Outcome determination emits outcome artifacts and identifies authoritative test statements at `.c2/tests/*.md`. | `new-ticket-outcome-determination.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks + artifact capture | Positive |
| TS-038 | Outcome outputs expose update requirement flag and validation command plan. | `new-ticket-outcome-determination.yaml` | High | Integration (`recipe_case`); deps: JSON output mapping | Positive |
| TS-039 | Blocking outcome review sets `review_ok=false` and returns blocking issues. | `new-ticket-outcome-determination.yaml` | High | Integration (`recipe_case`); deps: contrarian review output | Negative |
| TS-040 | Main job runs outcome review before implementation and uses outcome validation commands by default. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: outcome child recipe + validation input mapping | Positive |
| TS-041 | Implementation requesting statement changes routes through pre-implementation review instead of direct `.c2/tests/*.md` edits. | `new-ticket.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` incompleteCategory + input gate | Positive |
| TS-042 | Live skill bundle produces the intended behavior: cell triage, compatible requirements, and contrarian rejection of bad requirements. | `skill-quality-smoke.yaml`, `recipe-tests/verify-skill-quality-live.sh` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, pinned git skill ref, Codex API access | Positive |
| TS-043 | Live skill execution reports the pinned HTTPS repo ref resolved to the expected concrete commit hash. | `skill-quality-smoke.yaml`, `recipe-tests/verify-skill-quality-live.sh` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, HTTPS-accessible skill repo, Codex API access | Positive |
| TS-044 | Live Codex skill execution writes the expected marker file and ready status artifact. | `codex-skill-execution-smoke.yaml`, `recipe-tests/verify-codex-skill-execution-live.sh` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, pinned git skill ref, Codex API access | Positive |
| TS-045 | Live Codex skill execution returns a session, resolved skill ref, summary artifact, and progress artifact. | `codex-skill-execution-smoke.yaml`, `recipe-tests/verify-codex-skill-execution-live.sh` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, pinned git skill ref, Codex API access | Positive |
| TS-046 | Embedded child jobs receive submitted artifacts without duplicate artifact refs. | `recipe-tests/verify-child-artifact-forwarding-live.sh` | High | Live c2j integration; deps: `recipe.run_and_get_result`, embedded child job | Positive |
| TS-047 | `rule_gate` validates task-plan JSON and returns `ok=false` for routeable policy failures. | `superpowers-rule-gate-schema-smoke.yaml`, `recipe-tests/verify-superpowers-rule-gate-live.sh` | High | Live c2j integration; deps: c2ops `rule_gate`, JSON Schema | Positive |
| TS-048 | Invalid `rule_gate` input is rejected instead of becoming policy data. | `superpowers-rule-gate-invalid-input-smoke.yaml`, `recipe-tests/verify-superpowers-rule-gate-live.sh` | High | Live c2j integration; deps: c2ops `rule_gate` schema validation | Negative |
| TS-049 | `recipe.await_result_soft` exposes failed child status for deterministic parent routing. | `recipe-tests/verify-superpowers-child-orchestration-live.sh` | High | Live c2j integration; deps: `recipes.run`, `recipe.await_result_soft`, c2ops `rule_gate` | Positive |
| TS-050 | `child_group` preserves required and optional reviewer failure semantics. | `recipe-tests/verify-superpowers-child-orchestration-live.sh` | High | Live c2j integration; deps: `child_group`, embedded child jobs, c2ops `rule_gate` | Positive |
| TS-051 | Native Superpowers task selection picks the first ready task without a task-loop op. | `superpowers-native-task-selection-smoke.yaml` | High | Integration (`recipe_case`); deps: command seed + CEL/JQ template outputs | Positive |
| TS-052 | Native task selection surfaces required child-job boundaries without spawning child jobs. | `superpowers-native-task-selection-smoke.yaml` | High | Integration (`recipe_case`); deps: command seed + CEL/JQ template outputs | Positive |
| TS-053 | One Superpowers task boundary uses distinct same-job Codex role sessions. | `superpowers-task-session-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-054 | `sessionId` omission starts isolated context and explicit `sessionId` resumes it. | `superpowers-session-contract-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-055 | Adaptive parent loop updates plan state before selecting the next task. | `superpowers-adaptive-task-loop-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks + state machine outputs | Positive |
| TS-056 | `codex/run_skill` exposes parsed output artifact and valid status contract fields. | `superpowers-run-skill-output-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` selector mock outputs | Positive |
| TS-057 | `codex/run_skill` repair metadata is visible to recipes after output repair. | `superpowers-run-skill-repair-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` selector mock outputs | Positive |
| TS-058 | C2 Superpowers role skills expose the required recipe-owned orchestration contract. | `superpowers-c2-skill-bundle-smoke.yaml`, `skills-bundle/.agents/skills/c2-superpowers-*` | High | Integration (`recipe_case`); deps: command static bundle check | Positive |
| TS-059 | Superpowers route sends feature work to brainstorming before implementation. | `superpowers-route.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-060 | Superpowers route requires a concrete question when user input is needed. | `superpowers-route.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-061 | Superpowers brainstorming produces a plan-ready design artifact contract. | `superpowers-brainstorm.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-062 | Superpowers brainstorming stops before planning when design questions remain. | `superpowers-brainstorm.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-063 | Superpowers write-plan produces a ready dependent task chain. | `superpowers-write-plan.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-064 | Superpowers write-plan surfaces required C2 child-job boundaries. | `superpowers-write-plan.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-065 | Superpowers route sends submitted plans to execution without skill invocation. | `superpowers-route.yaml` | High | Integration (`recipe_case`); deps: deterministic state-machine routing | Positive |
| TS-066 | Superpowers route sends submitted designs to planning without skill invocation. | `superpowers-route.yaml` | High | Integration (`recipe_case`); deps: deterministic state-machine routing | Positive |
| TS-067 | Superpowers execute-plan runs one same-job implementation/review task boundary. | `superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: deterministic task selection + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-068 | Superpowers execute-plan stops before implementation when a child-job boundary is required. | `superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: deterministic child-boundary detection + node non-execution assertion | Positive |
| TS-069 | Superpowers verify runs required validation commands before reporting success. | `superpowers-verify.yaml` | High | Integration (`recipe_case`); deps: deterministic command execution + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-070 | Superpowers verify keeps failed command evidence as blocking workflow data. | `superpowers-verify.yaml` | High | Integration (`recipe_case`); deps: `command_execution continue_on_error` + c2ops `codex/run_skill`/`rule_gate` selector mocks | Negative |
| TS-071 | Superpowers finish recommends merge-ready only from verified completion evidence. | `superpowers-finish.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-072 | Superpowers finish blocks merge when verification evidence has blocking issues. | `superpowers-finish.yaml` | High | Integration (`recipe_case`); deps: deterministic merge-blocked state + c2ops `codex/run_skill`/`rule_gate` selector mocks | Negative |
| TS-073 | Superpowers finish runs merge only after explicit action and passing finish gate. | `superpowers-finish.yaml` | High | Integration (`recipe_case`); deps: `squashrebasemerge` selector mock + verified finish gate | Positive |

## Notes for Test Authoring

- Prefer `recipe_case` with explicit op mocks for deterministic branch coverage under test-policy sandboxing.
- Op mocks are single-use per invocation; if a node/op can run multiple times, add one mock entry per expected invocation.
- For selector-backed c2ops at `@main`, mock `recipe_within_resolution` once per case and mock the c2j diagnostic node path or op `extension_execution`.
- Recipes that need cell catalogs should load them through `c2j cells --json`; tests should mock the `load_cells` node rather than pass cell lists as public inputs.
- Use `integration_case` only when external workflow context is required and available in the harness.
- Keep artifact assertions focused on outbox contract files, not assistant summary text.
- For live skill checks, use workflow-run acceptance tests that validate authoring quality and contrarian rejection behavior, not just recipe node wiring.

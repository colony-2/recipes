# Recipe Test Statements

These statements are intended to drive `c2j test` cases.

## Statement Catalog

| ID | Test statement | Relevant file(s) | Importance | Type / dependencies | Polarity |
|---|---|---|---|---|---|
| TS-001 | Triage marks appropriate cell jobs as `cell_is_appropriate=true`. | `recipes/new-ticket/new-ticket-triage.yaml` | High | Integration (`recipe_case`); deps: `load_cells` command + c2ops `codex` mocks | Positive |
| TS-002 | Triage marks out-of-cell jobs as `cell_is_appropriate=false`. | `recipes/new-ticket/new-ticket-triage.yaml` | High | Integration (`recipe_case`); deps: `load_cells` command + c2ops `codex` mocks | Positive |
| TS-003 | Invalid recommended cell yields `recommended_cell_is_valid=false`. | `recipes/new-ticket/new-ticket-triage.yaml` | High | Integration (`recipe_case`); deps: `c2j cells --json` command mock | Negative |
| TS-004 | Triage emits a triage decision artifact payload for downstream routing. | `recipes/new-ticket/new-ticket-triage.yaml` | Medium | Integration (`recipe_case`); deps: artifact capture | Positive |
| TS-005 | Requirements planning emits `requirements/plan.json`, `requirements/index.md`, and requirement markdown artifacts. | `recipes/new-ticket/new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-006 | Requirements outputs expose dependency order and cross-cell flags from planning payload. | `recipes/new-ticket/new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: JSON output parsing | Positive |
| TS-007 | Requirements planning accepts user feedback input and returns updated summary outputs. | `recipes/new-ticket/new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: input plumbing | Positive |
| TS-008 | Blocking API review sets `api_review_ok=false` and returns blocking issues list. | `recipes/new-ticket/new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: contrarian review output | Negative |
| TS-009 | Contrarian review emits `requirements/api-review.json` artifact. | `recipes/new-ticket/new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: artifact capture | Positive |
| TS-010 | Planning and review artifacts coexist in one requirements-planning execution. | `recipes/new-ticket/new-ticket-requirements-planning.yaml` | High | Integration (`recipe_case`); deps: multi-artifact output | Positive |
| TS-011 | Implementation uses continue-session path when `session_id` is provided. | `recipes/jobs/job-implement.yaml` | High | Integration (`recipe_case`); deps: state initial branching | Positive |
| TS-012 | Implementation uses new-session path when `session_id` is absent. | `recipes/jobs/job-implement.yaml` | High | Integration (`recipe_case`); deps: state initial branching | Positive |
| TS-013 | Implementation returns non-empty `assistant_summary` output for reviewer context and next-session reuse. | `recipes/jobs/job-implement.yaml` | Medium | Integration (`recipe_case`); deps: c2ops `codex` selector mock outputs | Positive |
| TS-014 | Validation provided-command path persists full and tail validation artifacts. | `recipes/new-ticket/job-validate.yaml` | High | Integration (`recipe_case`); deps: `command_execution` mock artifacts | Positive |
| TS-015 | Validation suggested-command path executes and reports pass status. | `recipes/new-ticket/job-validate.yaml` | High | Integration (`recipe_case`); deps: `input` + `command_execution` mocks | Positive |
| TS-016 | Validation custom-command path executes and persists output tail artifact. | `recipes/new-ticket/job-validate.yaml` | High | Integration (`recipe_case`); deps: `input` + `command_execution` mocks | Positive |
| TS-017 | Validation failure sets `passed=false` and non-zero `exit_code`. | `recipes/new-ticket/job-validate.yaml` | High | Integration (`recipe_case`); deps: failure output mapping | Negative |
| TS-018 | Validation outputs stable artifact contract keys for full and tail logs. | `recipes/new-ticket/job-validate.yaml` | Medium | Integration (`recipe_case`); deps: output contract | Positive |
| TS-019 | Merge prompts for missing upstream details before approval. | `recipes/jobs/job-merge.yaml` | High | Integration (`recipe_case`); deps: `input` prompt path | Positive |
| TS-020 | Merge approval `cancel` exits without merge hash output. | `recipes/jobs/job-merge.yaml` | High | Integration (`recipe_case`); deps: approval branching | Negative |
| TS-021 | Merge approval `merge` returns non-empty `merged_hash`. | `recipes/jobs/job-merge.yaml` | High | Integration (`recipe_case`); deps: `squashrebasemerge` mock | Positive |
| TS-022 | Prompted merge path executes merge and returns prompted target branch. | `recipes/jobs/job-merge.yaml` | High | Integration (`recipe_case`); deps: prompt + merge path | Positive |
| TS-023 | Merge outputs expose `target_branch` from merge operation result. | `recipes/jobs/job-merge.yaml` | Medium | Integration (`recipe_case`); deps: output mapping | Positive |
| TS-024 | `c2j test compile` generates canonical IR JSON artifact. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test compile` | Positive |
| TS-025 | `c2j test validate` returns non-zero when case filters select no cases. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test validate` | Negative |
| TS-026 | `c2j test run` writes `summary.json`, `summary.md`, and per-case results. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test run` | Positive |
| TS-027 | Scenario markdown without fenced YAML/JSON fails compile. | `guides/RECIPE_TESTING_CLI_USER_GUIDE.md` | Medium | CLI integration; deps: `c2j test compile` | Negative |
| TS-028 | Implementation planning emits `implementation/plan.json`, `implementation/index.md`, and per-requirement markdown artifacts. | `recipes/new-ticket/new-ticket-implementation-planning.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-029 | Implementation planning outputs expose dependency gating fields and dependency order. | `recipes/new-ticket/new-ticket-implementation-planning.yaml` | High | Integration (`recipe_case`); deps: JSON output mapping | Positive |
| TS-030 | Blocking compatibility review sets `compat_review_ok=false` and returns blocking issues. | `recipes/new-ticket/new-ticket-implementation-planning.yaml` | High | Integration (`recipe_case`); deps: contrarian review output | Negative |
| TS-031 | Approved implementation plan requiring dependency jobs starts child jobs and enters waiting state. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: `recipes.run` + child recipe mocks | Positive |
| TS-032 | Merge decision `cancel_job` updates workflow to cancelled path without merge. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: input branching | Negative |
| TS-033 | Merge request without local hash returns to implementation instead of executing merge. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: ready-to-merge branching | Negative |
| TS-034 | Successful merge path marks job completion (`job_done=true`) with non-empty merged hash. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: `local_hash` input + `squashrebasemerge` mock | Positive |
| TS-035 | Implementation-reported cross-cell bugs start child bug jobs before continuing workflow. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` pendingDependencies + `recipes.run` mock | Positive |
| TS-036 | Implementation user questions pause flow for structured user input, then continue the same Codex session. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` incompleteCategory + `input` + repeated selector mock | Positive |
| TS-037 | Outcome determination emits outcome artifacts and identifies authoritative test statements at `.c2/tests/*.md`. | `recipes/new-ticket/new-ticket-outcome-determination.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks + artifact capture | Positive |
| TS-038 | Outcome outputs expose update requirement flag and validation command plan. | `recipes/new-ticket/new-ticket-outcome-determination.yaml` | High | Integration (`recipe_case`); deps: JSON output mapping | Positive |
| TS-039 | Blocking outcome review sets `review_ok=false` and returns blocking issues. | `recipes/new-ticket/new-ticket-outcome-determination.yaml` | High | Integration (`recipe_case`); deps: contrarian review output | Negative |
| TS-040 | Main job runs outcome review before implementation and uses outcome validation commands by default. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: outcome child recipe + validation input mapping | Positive |
| TS-041 | Implementation requesting statement changes routes through pre-implementation review instead of direct `.c2/tests/*.md` edits. | `recipes/new-ticket/new-ticket.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` incompleteCategory + input gate | Positive |
| TS-042 | Live skill bundle produces the intended behavior: cell triage, compatible requirements, and contrarian rejection of bad requirements. | `recipes/smoke/skill-quality-smoke.yaml`, `recipe-tests/skill-quality-smoke.scenario.md` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, pinned git skill ref, Codex API access | Positive |
| TS-043 | Live skill execution reports the pinned HTTPS repo ref resolved to the expected concrete commit hash. | `recipes/smoke/skill-quality-smoke.yaml`, `recipe-tests/skill-quality-smoke.scenario.md` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, HTTPS-accessible skill repo, Codex API access | Positive |
| TS-044 | Live Codex skill execution writes the expected marker file and ready status artifact. | `recipes/smoke/codex-skill-execution-smoke.yaml`, `recipe-tests/codex-skill-execution-smoke.scenario.md` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, pinned git skill ref, Codex API access | Positive |
| TS-045 | Live Codex skill execution returns a session, resolved skill ref, summary artifact, and progress artifact. | `recipes/smoke/codex-skill-execution-smoke.yaml`, `recipe-tests/codex-skill-execution-smoke.scenario.md` | High | Live c2j integration; deps: c2ops `codex` at `@main`, extension sandbox disabled, pinned git skill ref, Codex API access | Positive |
| TS-046 | Embedded child jobs receive submitted artifacts without duplicate artifact refs. | `recipe-tests/verify-child-artifact-forwarding-live.sh` | High | Live c2j integration; deps: `recipe.run_and_get_result`, embedded child job | Positive |
| TS-047 | `rule_gate` validates task-plan JSON and returns `ok=false` for routeable policy failures. | `recipes/superpowers/tests/superpowers-rule-gate-schema-smoke.yaml`, `recipes/superpowers/tests/superpowers-rule-gate-schema-smoke.scenario.md` | High | Live c2j integration; deps: c2ops `rule_gate`, JSON Schema | Positive |
| TS-048 | Invalid `rule_gate` input is rejected instead of becoming policy data. | `recipes/superpowers/tests/superpowers-rule-gate-invalid-input-smoke.yaml`, `recipes/superpowers/tests/superpowers-rule-gate-schema-smoke.scenario.md` | High | Live c2j integration; deps: c2ops `rule_gate` schema validation | Negative |
| TS-049 | `recipe.await_result_soft` exposes failed child status for deterministic parent routing. | `guides/NATIVE_TEST_MIGRATION.md (c2j ownership)` | High | Live c2j integration; deps: `recipes.run`, `recipe.await_result_soft`, c2ops `rule_gate` | Positive |
| TS-050 | `child_group` preserves required and optional reviewer failure semantics. | `guides/NATIVE_TEST_MIGRATION.md (c2j ownership)` | High | Live c2j integration; deps: `child_group`, embedded child jobs, c2ops `rule_gate` | Positive |
| TS-051 | Native Superpowers task selection picks the first ready task without a task-loop op. | `recipes/superpowers/tests/superpowers-native-task-selection-smoke.yaml` | High | Integration (`recipe_case`); deps: command seed + CEL/JQ template outputs | Positive |
| TS-052 | Native task selection surfaces required child-job boundaries without spawning child jobs. | `recipes/superpowers/tests/superpowers-native-task-selection-smoke.yaml` | High | Integration (`recipe_case`); deps: command seed + CEL/JQ template outputs | Positive |
| TS-053 | One Superpowers task boundary uses distinct same-job Codex role sessions. | `recipes/superpowers/tests/superpowers-task-session-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-054 | `sessionId` omission starts isolated context and explicit `sessionId` resumes it. | `recipes/superpowers/tests/superpowers-session-contract-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks | Positive |
| TS-055 | Adaptive parent loop updates plan state before selecting the next task. | `recipes/superpowers/tests/superpowers-adaptive-task-loop-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex` selector mocks + state machine outputs | Positive |
| TS-056 | `codex/run_skill` exposes parsed output artifact and valid status contract fields. | `recipes/superpowers/tests/superpowers-run-skill-output-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` selector mock outputs | Positive |
| TS-057 | `codex/run_skill` repair metadata is visible to recipes after output repair. | `recipes/superpowers/tests/superpowers-run-skill-repair-smoke.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` selector mock outputs | Positive |
| TS-058 | Exactly ten C2 Superpowers role skills expose the required recipe-owned orchestration contract. | `recipes/superpowers/tests/superpowers-c2-skill-bundle-smoke.yaml`, `skills-bundle/.agents/skills/c2-superpowers-*` | High | Integration (`recipe_case`); deps: command static bundle check | Positive |
| TS-059 | Superpowers route sends feature work to brainstorming before implementation. | `recipes/superpowers/superpowers-route.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-060 | Superpowers route requires a concrete question when user input is needed. | `recipes/superpowers/superpowers-route.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-061 | Superpowers brainstorming produces a plan-ready design artifact contract. | `recipes/superpowers/superpowers-brainstorm.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-062 | Superpowers brainstorming stops before planning when design questions remain. | `recipes/superpowers/superpowers-brainstorm.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-063 | Superpowers write-plan produces a ready dependent task chain. | `recipes/superpowers/superpowers-write-plan.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-064 | Superpowers write-plan surfaces required C2 child-job boundaries. | `recipes/superpowers/superpowers-write-plan.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill` + `rule_gate` selector mocks | Positive |
| TS-065 | Superpowers route sends submitted plans to execution without skill invocation. | `recipes/superpowers/superpowers-route.yaml` | High | Integration (`recipe_case`); deps: deterministic state-machine routing | Positive |
| TS-066 | Superpowers route sends submitted designs to planning without skill invocation. | `recipes/superpowers/superpowers-route.yaml` | High | Integration (`recipe_case`); deps: deterministic state-machine routing | Positive |
| TS-067 | Superpowers execute-plan runs one same-job implementation/review task boundary. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: deterministic task selection + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-068 | Superpowers execute-plan stops before implementation when a child-job boundary is required. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: deterministic child-boundary detection + node non-execution assertion | Positive |
| TS-069 | Superpowers verify runs required validation commands before reporting success. | `recipes/superpowers/superpowers-verify.yaml` | High | Integration (`recipe_case`); deps: deterministic command execution + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-070 | Superpowers verify keeps failed command evidence as blocking workflow data. | `recipes/superpowers/superpowers-verify.yaml` | High | Integration (`recipe_case`); deps: `command_execution continue_on_error` + c2ops `codex/run_skill`/`rule_gate` selector mocks | Negative |
| TS-071 | Superpowers finish recommends merge-ready only from verified completion evidence. | `recipes/superpowers/superpowers-finish.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-072 | Superpowers finish blocks merge when verification evidence has blocking issues. | `recipes/superpowers/superpowers-finish.yaml` | High | Integration (`recipe_case`); deps: deterministic merge-blocked state + c2ops `codex/run_skill`/`rule_gate` selector mocks | Negative |
| TS-073 | Superpowers finish runs merge only after explicit action and passing finish gate. | `recipes/superpowers/superpowers-finish.yaml` | High | Integration (`recipe_case`); deps: `squashrebasemerge` selector mock + verified finish gate | Positive |
| TS-074 | Superpowers debug routes reproduced failures with root-cause evidence to fix-ready. | `recipes/superpowers/superpowers-debug.yaml` | High | Integration (`recipe_case`); deps: command reproduction + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-075 | Superpowers debug stops before skill invocation when no reproduction command exists. | `recipes/superpowers/superpowers-debug.yaml` | High | Integration (`recipe_case`); deps: deterministic state-machine routing | Negative |
| TS-076 | Superpowers debug routes plan-caused failures back to plan update. | `recipes/superpowers/superpowers-debug.yaml` | High | Integration (`recipe_case`); deps: command reproduction + c2ops `codex/run_skill`/`rule_gate` selector mocks | Negative |
| TS-077 | Superpowers debug requires architecture review after a third reproduced failed attempt. | `recipes/superpowers/superpowers-debug.yaml` | High | Integration (`recipe_case`); deps: command reproduction + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-078 | Superpowers plan review approves an aligned task plan before execution. | `recipes/superpowers/superpowers-plan-review.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-079 | Superpowers plan review blocks incomplete plans and routes them to replanning. | `recipes/superpowers/superpowers-plan-review.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill`/`rule_gate` selector mocks | Negative |
| TS-080 | Superpowers primary orchestrator runs the normal same-job design-to-finish path. | `recipes/superpowers/superpowers.yaml` | High | Integration (`recipe_case`); deps: c2ops `codex/run_skill`/`rule_gate` selector mocks + command gates | Positive |
| TS-081 | Superpowers primary orchestrator stops before implementation when a child-job boundary is required. | `recipes/superpowers/superpowers.yaml` | High | Integration (`recipe_case`); deps: deterministic child-boundary detection + node non-execution assertion | Positive |
| TS-082 | Superpowers execute-plan enforces RED/GREEN/refactor TDD before task review. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: recipe state machine + command gates + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-083 | Superpowers execute-plan routes spec review failure through revision and re-review. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: recipe state machine + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-084 | Superpowers execute-plan routes quality review failure through revision and re-review. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: recipe state machine + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-085 | Superpowers primary orchestrator routes spec review failure through revision and re-review. | `recipes/superpowers/superpowers.yaml` | High | Integration (`recipe_case`); deps: primary state machine + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-086 | Superpowers primary orchestrator enforces RED/GREEN/refactor TDD before task review. | `recipes/superpowers/superpowers.yaml` | High | Integration (`recipe_case`); deps: primary TDD state machine + command gates + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-087 | Superpowers execute-plan routes TDD spec review failure through revision, TDD command reruns, and re-review. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: TDD revision state machine + command gates + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-088 | Superpowers primary orchestrator routes TDD spec review failure through revision, TDD command reruns, and re-review. | `recipes/superpowers/superpowers.yaml` | High | Integration (`recipe_case`); deps: primary TDD revision state machine + command gates + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-089 | Superpowers write-plan emits TDD command contracts for recipe-enforced RED/GREEN/refactor gates. | `recipes/superpowers/superpowers-write-plan.yaml` | High | Integration (`recipe_case`); deps: task-plan schema + c2ops `codex/run_skill`/`rule_gate` selector mocks | Positive |
| TS-090 | Superpowers write-plan rejects child-job tasks missing matching boundary metadata. | `recipes/superpowers/superpowers-write-plan.yaml` | High | Integration (`recipe_case`); deps: deterministic child-boundary policy gate + c2ops `rule_gate` passthrough | Negative |
| TS-091 | Superpowers role-skill invocations install the configured skill bundle ref. | `recipes/superpowers/tests/superpowers-c2-skill-bundle-smoke.yaml`, `recipes/superpowers/superpowers*.yaml` | High | Integration (`recipe_case`); deps: static recipe wiring check for c2ops `codex/run_skill` skills input | Positive |
| TS-092 | Live `codex/run_skill` executes a worktree skill and validates artifact-first JSON output plus status contract artifacts. | `recipes/superpowers/tests/superpowers-run-skill-live-smoke.yaml`, `recipes/superpowers/tests/superpowers-run-skill-live.test.yaml` | High | Live c2j integration; deps: c2ops `codex/run_skill` at `@main`, local worktree skill, Codex API access | Positive |
| TS-093 | Live `codex/run_skill` exposes parsed artifact fields, diagnostics artifacts, and zero repair attempts to downstream recipe nodes. | `recipes/superpowers/tests/superpowers-run-skill-live-smoke.yaml`, `recipes/superpowers/tests/superpowers-run-skill-live.test.yaml` | High | Live c2j integration; deps: c2ops `codex/run_skill` at `@main`, same-recipe artifact bindings | Positive |
| TS-094 | Superpowers primary orchestrator resolves inline phase recipes in embedded runtime. | `recipes/superpowers/superpowers.yaml`, `recipes/superpowers/tests/superpowers-inline.test.yaml` | High | Live c2j integration; deps: `c2j submit --run --embed` and local inline recipe includes | Positive |
| TS-095 | Superpowers execute-plan stops without implementation when no ready task exists. | `recipes/superpowers/superpowers-execute-plan.yaml` | High | Integration (`recipe_case`); deps: deterministic task selection + node non-execution assertions | Negative |

## Default Build and Evolve Recipes

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-096 | Build presents the latest coding summary and commits only after satisfaction is confirmed. | `build.yaml`, `recipe-tests/build.scenario.md` | Critical | Integration; c2j, mocked Codex and input | Positive |
| TS-097 | Repeated feedback continues the same coding conversation and presents each updated summary before approval. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, mocked Codex and input | Positive |
| TS-098 | Rejection without feedback requests feedback again and does not commit. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, mocked Codex and input | Negative |
| TS-099 | Failed coding or missing continuation context cannot commit or silently start a new conversation. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, mocked Codex and input | Negative |
| TS-100 | Evolve explains recipe-only scope, shared defaults, and committed target-cell overrides throughout the feedback loop. | `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, mocked Codex and input | Positive |
| TS-101 | Incomplete coding work requires further feedback before it can be approved. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | High | Integration; c2j, mocked Codex and input | Negative |
| TS-102 | Approval squashes accepted changes into the target upstream branch and reports its resulting commit. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, git, temporary upstream repository | Positive |
| TS-103 | Default recipe tests use disposable runtime storage independently of the persistent user database. | `recipe-tests/run-defaults.sh`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j passthrough harness, temporary database | Positive |
| TS-104 | Each coding iteration supplies a structured result that passes schema validation before human review. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, c2ops rule_gate | Positive |
| TS-105 | Missing, malformed, or incomplete result artifacts prevent approval and upstream merge, including after previously valid iterations. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, c2ops rule_gate | Negative |
| TS-106 | Codex uses automatic runtime and artifact paths; only a scoped target intentionally overrides its working directory. | `build.yaml`, `evolve.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | High | Integration; c2j extension defaults, c2ops Codex manifest | Positive |

## Shared Development Workflow

The simplified defaults use agent and human judgments for mandate fit and test
coverage. Routing schemas validate decisions, not semantic correctness. User-approved
simplification replaces earlier ID, provenance, and command-mapping requirements.

These statements extend the default-recipe contracts above. Build retains automatic
op paths; evolve intentionally overrides the Codex working directory. The shared
workflow adds a design/test-plan approval checkpoint before outcome acceptance.

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-107 | Build and evolve share design, test planning, independent reviews, implementation, verification, and acceptance stages. | `build.yaml`, `evolve.yaml`, `recipes/develop/develop.yaml` | Critical | Integration; c2j, mocked Codex/input | Positive |
| TS-108 | Invalid or rejected design and test-plan results prevent implementation until revised and approved. | `recipes/develop/develop.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; c2j, rule_gate | Negative |
| TS-109 | Test plans precede implementation, remain in the repository, and are copied exactly into review artifacts. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, command checks | Positive |
| TS-110 | A rejecting independent test-plan review prevents implementation until revision and human approval. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, rule_gate, command checks | Negative |
| TS-111 | Feedback resumes the implementation session while independent reviewers receive fresh conversations. | `recipes/develop/develop.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; c2j input rendering | Positive |
| TS-112 | Failed or timed-out verification returns evidence to implementation before acceptance or merge. | `recipes/develop/verify.yaml`, `recipes/develop/develop.yaml` | Critical | Integration; real command execution | Negative |
| TS-113 | Evolve runs Codex in its configured subdirectory with sandboxing enabled and automatic artifact paths. | `evolve.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; c2j rendering; launcher probe documented separately | Positive |
| TS-114 | Retired by explicit removal of custom write-scope enforcement; target-directory behavior remains covered by TS-106. | Historical | — | — | — |
| TS-115 | Requirement feedback returns to design and requires renewed plan approval before implementation resumes. | `recipes/develop/develop.yaml` | Critical | Integration; c2j, mocked input | Positive |
| TS-116 | Human acceptance after the verification step authorizes one squash merge into upstream. | `recipes/develop/develop.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; c2j, disposable upstream | Positive |
| TS-117 | Retired by explicit removal of custom write-scope enforcement; target-directory behavior remains covered by TS-106. | Historical | — | — | — |
| TS-118 | Verification preserves native return codes and logs; an absent hook is explicitly reported as skipped. | `recipes/develop/verify.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | High | Integration; real commands, disposable git repository | Positive/negative |
| TS-119 | Local specialization wrappers can reference shared phases without copying sibling recipes. | `build.yaml`, `evolve.yaml`, `recipes/develop/develop.yaml` | High | Integration; c2j include resolution | Positive |
| TS-120 | Repeated invalid human choices and blank feedback cannot bypass approvals or lose the original request. | `recipes/develop/develop.yaml` | High | Integration; c2j, mocked input | Negative |

## Cross-cell dependencies

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-121 | CLI build and evolve submissions accept the injected recipe type. | `build.yaml`, `evolve.yaml` | Critical | Integration; c2j | Positive |
| TS-122 | Every captured child finishes before its requesting phase resumes or advances. | `recipes/develop/agent.yaml`, `recipes/develop/wait-children.yaml` | Critical | Integration; separate temporary JobDB service, c2j workers | Positive |
| TS-123 | Successful dependencies resume the same conversation with child outputs and artifacts before review. | `recipes/develop/agent.yaml` | Critical | Integration; c2j, deterministic agent | Positive |
| TS-124 | Failed, cancelled, or unmerged dependencies resume the requesting session with outcomes before the phase can advance. | `recipes/develop/wait-children.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; c2j | Negative |
| TS-125 | Duplicate child identities are awaited once, including children already finished when the submitting operation returns. | `recipes/develop/wait-children.yaml` | High | Integration; separate temporary JobDB service | Positive |
| TS-126 | Repeated dependency rounds retain earlier outcomes and never resubmit a captured job automatically. | `recipes/develop/agent.yaml` | Critical | Integration; c2j | Positive |
| TS-127 | Invalid agent results or missing sessions cannot bypass dependency handling or reach acceptance. | `recipes/develop/agent.yaml` | Critical | Integration; c2j | Negative |
| TS-128 | Human feedback preserves completed dependency outcomes and artifacts without creating replacement jobs. | `recipes/develop/develop.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; separate temporary JobDB service | Positive |
| TS-129 | The resumed session can submit corrected dependency work, retaining failed history and awaiting replacement results before advancing. | `recipes/develop/agent.yaml`, `recipe-tests/dependencies.test.yaml`, `recipe-tests/dependency-runtime.test.yaml` | Critical | Integration; separate temporary JobDB service | Positive |
| TS-130 | Unresolved dependency problems reach human feedback only when the resumed session reports that it needs input. | `recipes/develop/agent.yaml`, `recipe-tests/dependencies.test.yaml`, `recipe-tests/dependency-runtime.test.yaml` | Critical | Integration; separate temporary JobDB service | Negative |

| TS-131 | Design instructions require reading the plain Markdown mandate and explaining local, partial, or external ownership. | `recipes/develop/agent.yaml` | Critical | Integration; c2j | Positive |
| TS-132 | An agent requesting mandate clarification returns to human feedback without implementation. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j | Negative |
| TS-133 | Partial designs explain the ownership split; outside decisions produce routing without implementation or merge. | `recipes/develop/develop.yaml`, `recipe-tests/implementation-consultations.test.yaml`, `recipe-tests/consultation-reuse.test.yaml` | Critical | Integration; c2j | Positive |
| TS-134 | Malformed routing responses and consultation requests fail schema validation before advancing the workflow. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j | Negative |
| TS-135 | Consultations run in the selected cell while retaining the originating job identity and returning to its repository. | `recipes/develop/consult.yaml` | Critical | Integration; temporary JobDB, git | Positive |
| TS-136 | Follow-up consultations restore the foreign session without preserving experimental repository changes. | `recipes/develop/agent.yaml`, `recipes/develop/consult.yaml` | Critical | Integration; temporary JobDB, git | Positive |
| TS-137 | Further work resumes the local session; consultation replies return control to that session. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | High | Integration; c2j | Negative |
| TS-138 | Planning cannot submit child jobs; implementation can submit approved work as an ordinary Markdown brief. | `recipes/develop/agent.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; temporary JobDB | Positive and negative |
| TS-139 | Invalid foreign responses, missing sessions, and unavailable repositories cannot silently become accepted designs. | `recipes/develop/consult.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; c2j | Negative |

| TS-140 | Implementation can consult a dependency cell after discovering a bug without first abandoning its coding session. | `recipes/develop/agent.yaml` | Critical | Integration; isolated JobDB, c2j | Positive |
| TS-141 | Implementation edits and dependency history survive foreign discussions; foreign experiments never enter the local candidate. | `recipes/develop/agent.yaml` | Critical | Integration; git, isolated JobDB | Positive |
| TS-142 | Design and implementation reuse the latest foreign session independently for each destination cell. | `recipes/develop/agent.yaml`, `recipe-tests/implementation-consultations.test.yaml`, `recipe-tests/consultation-reuse.test.yaml` | Critical | Integration; isolated JobDB | Positive |
| TS-143 | Newly agreed external work returns to design approval before submission; advisory answers can continue approved implementation directly. | `recipes/develop/agent.yaml`, `recipes/develop/develop.yaml` | Critical | Integration; c2j | Positive and negative |
| TS-144 | Multiple foreign threads retain separate checkpoints and identities; missing continuation checkpoints cannot advance. | `recipes/develop/consult.yaml`, `recipes/develop/agent.yaml` | Critical | Integration; isolated JobDB | Positive and negative |
| TS-145 | Missing repositories or malformed foreign replies prevent continuation; ownership questions can return to human feedback. | `recipes/develop/consult.yaml`, `recipe-tests/implementation-consultations.test.yaml`, `recipe-tests/consultation-reuse.test.yaml` | Critical | Integration; isolated JobDB | Negative |
| TS-146 | Runtime blocker regressions execute independently so a broker or replay failure cannot hide other workspace coverage. | `recipe-tests/consultation-gates.test.yaml` | High | Integration; isolated JobDB | Negative |

| TS-147 | Named build and evolve handoffs execute committed child recipes with includes, reassess ownership, and merge verified work before the parent resumes. | `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, c2j, git | Positive |
| TS-148 | Late dependency discoveries require renewed design approval; parent restart preserves conversations and candidate edits without duplicating child submissions. | `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, c2j workers | Positive and negative |
| TS-149 | Parent acceptance and merge remain unreachable while an approved dependency is pending. | `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, c2j workers | Negative |
| TS-150 | Both entrypoints export verification reports and command logs with child provenance; awaiting parents receive those same artifact keys after worker replacement. | `build.yaml`, `evolve.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, c2j, git | Positive |
| TS-151 | Missing verification artifacts or changed dependency artifact keys cannot pass the full development lifecycle regression. | `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, c2j, git | Negative |

## Proposed native review contract

These cover the draft contract fixtures, not an implemented c2j review op.
Runtime acceptance coverage is specified in `guides/NATIVE_REVIEW_HANDOFF_PROPOSAL.md`
and remains the c2j team's implementation responsibility.

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-152 | Review packages identify their summary, available decisions, and immutable documents independently of recipe-specific presentation. | `contracts/review/v1.schema.json`, `contracts/review/v1.schema.json (superseded proposal)` | High | Contract integration; Python, jsonschema | Positive |
| TS-153 | Review submissions identify the reviewed version and each annotated document's original hash while preserving CriticMarkup text. | `contracts/review/v1.schema.json`, `contracts/review/v1.schema.json (superseded proposal)` | Critical | Contract integration; Python, jsonschema | Positive |
| TS-154 | Unversioned reviews, filesystem-only documents, malformed hashes, unknown fields, and incomplete annotations fail contract validation. | `contracts/review/v1.schema.json`, `contracts/review/v1.schema.json (superseded proposal)` | Critical | Contract integration; Python, jsonschema | Negative |
| TS-155 | Recipe review specifications cannot supply runtime review identities or client download locations. | `contracts/review/v1.schema.json`, `contracts/review/v1.schema.json (superseded proposal)` | High | Contract integration; Python, jsonschema | Negative |
| TS-156 | Review receipts retain the submitted feedback and durable request and response artifacts for downstream consumers. | `contracts/review/v1.schema.json`, `contracts/review/v1.schema.json (superseded proposal)` | High | Contract integration; Python, jsonschema | Positive |

## Immutable Codex session migration

The upstream object-session release replaces legacy ID/artifact resumption.
Existing conversation-continuation expectations remain; legacy checkpoints require
a fresh job and cannot be imported by the new op revision.

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-157 | New conversations omit session inputs; later turns receive the complete checkpoint produced by the selected predecessor. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j, pinned c2ops | Positive |
| TS-158 | Human feedback and dependency recovery resume the latest successful checkpoint without session-state artifact bindings. | `recipes/develop/develop.yaml`, `recipe-tests/dependencies.test.yaml`, `recipe-tests/dependency-runtime.test.yaml` | Critical | Integration; ephemeral JobDB, object fixture | Positive |
| TS-159 | Foreign sessions survive worker replacement while experimental repository changes remain disposable. | `recipes/develop/consult.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; ephemeral JobDB, git, object fixture | Positive |
| TS-160 | Retired with transcript reconciliation; native checkpoint validation remains covered by TS-161 and TS-165. | Historical | — | — | — |
| TS-161 | Missing or invalid successor checkpoints cannot authorize continuation, acceptance, or merge. | `recipes/develop/agent.yaml`, `recipes/develop/consult.yaml` | Critical | Integration; c2j, object fixture | Negative |
| TS-162 | Codex and skill calls share the pinned session contract and reject legacy resume inputs. | `recipes/`, `guides/NATIVE_TEST_MIGRATION.md (c2j/c2ops ownership)` | Critical | Integration; pinned c2ops, deterministic Codex CLI | Positive and negative |
| TS-163 | Session branches restore independent agent histories even when their diagnostic conversation IDs match. | `guides/NATIVE_TEST_MIGRATION.md (c2j/c2ops ownership)` | Critical | Integration; ephemeral JobDB, pinned c2ops | Positive |
| TS-164 | Session objects forwarded across job boundaries remain usable after worker replacement without appearing among deliverable artifacts. | `guides/NATIVE_TEST_MIGRATION.md (c2j/c2ops ownership)` | Critical | Integration; ephemeral JobDB, pinned c2ops | Positive |
| TS-165 | Unavailable, corrupted, wrong-type, or foreign-tenant checkpoints fail instead of starting a fresh conversation. | `guides/NATIVE_TEST_MIGRATION.md (c2j/c2ops ownership)` | Critical | Integration; ephemeral JobDB, pinned c2ops | Negative |

## Native document reviews

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-166 | Build and evolve present stored design and test-statement documents before implementation, then implementation and verification documents before merge. | `recipes/develop/develop.yaml`, `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | Critical | Integration; c2j, ephemeral JobDB | Positive |
| TS-167 | Revision feedback and annotated files reach the intended agent together, preserving CriticMarkup and the latest implementation session. | `recipes/develop/develop.yaml`, `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | Critical | Integration; c2j, ephemeral JobDB | Positive |
| TS-168 | Missing decisions, invalid answers, stale requests, and unavailable uploads leave reviews pending without advancing implementation or merge. | `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | Critical | Integration; native input library, ephemeral JobDB | Negative |
| TS-169 | Text-only and attachment-only revisions work without a second feedback prompt; each revised candidate requires a new review. | `recipes/develop/develop.yaml`, `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | Critical | Integration; c2j, ephemeral JobDB | Positive |
| TS-170 | Returned files cannot silently change approved documents or authorize merging an unreviewed candidate. | `recipes/develop/develop.yaml`, `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | Critical | Integration; c2j, git | Negative |
| TS-171 | Review receipts and original document references remain available after worker replacement and at recipe completion. | `build.yaml`, `evolve.yaml`, `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | High | Integration; c2j, ephemeral JobDB | Positive |
| TS-172 | Feedback from earlier review rounds cannot replace a later response or leak into an unrelated revision. | `recipes/develop/develop.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j | Negative |

## Simplified orchestration

- Build and evolve reach the first design agent through one shared loop, without forwarding-only phase recipes. Files: `recipes/develop/`; importance: high; integration; dependencies: c2j.
- Repeated agent turns preserve the latest session, draft, consultation reply, and dependency outcomes. Files: `recipes/develop/agent.yaml`; importance: critical; integration; dependencies: isolated JobDB, Git.
- Fresh agent calls omit the session input; resumed calls receive the preceding checkpoint. Files: `recipes/develop/agent.yaml`; importance: critical; integration; dependencies: c2j; positive and negative cases.

| ID | Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|---|
| TS-173 | Agents receive current phase results and dependency outcomes directly, with dependency documents available through their artifact inbox. | `recipes/develop/agent.yaml`, `recipe-tests/dependencies.test.yaml`, `recipe-tests/dependency-runtime.test.yaml` | Critical | Integration; ephemeral JobDB, object fixture | Positive |
| TS-174 | Design, implementation, and human feedback continue each foreign conversation from its latest checkpoint without replaying an older reply. | `recipes/develop/develop.yaml`, `recipe-tests/implementation-consultations.test.yaml`, `recipe-tests/consultation-reuse.test.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; ephemeral JobDB, git, object fixture | Positive and negative |
| TS-175 | Empty, duplicate, and previously completed child sets need no extra submissions; failures remain available to the requesting session. | `recipes/develop/wait-children.yaml`, `recipe-tests/dependencies.test.yaml`, `recipe-tests/dependency-runtime.test.yaml` | High | Integration; c2j, ephemeral JobDB | Positive and negative |

## Document placement and verification hooks

| Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|
| Design and summary documents reach subsequent agents through inbox artifacts without entering the merged repository. | `recipes/develop/develop.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, Git, scripted agents | Positive and negative |
| Both build and evolve merge the maintained test plan alongside their implementation changes. | `recipes/develop/agent.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; isolated JobDB, Git | Positive |
| Missing design artifacts prevent review-ready phases from advancing. | `recipes/develop/agent.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j | Negative |
| Verification runs the hook in the selected directory and exports its report and logs to awaiting parent jobs. | `recipes/develop/verify.yaml`, `recipe-tests/build-lifecycle.test.yaml`, `recipe-tests/evolve-lifecycle.test.yaml` | Critical | Integration; c2j, isolated JobDB | Positive |
| Failed verification resumes the implementation session, then repeats inspection and verification. | `recipes/develop/develop.yaml`, `recipe-tests/build.scenario.md`, `recipe-tests/evolve.scenario.md` | Critical | Integration; c2j | Negative |

## Notes for Test Authoring

- Prefer `recipe_case` with explicit op mocks for deterministic branch coverage under test-policy sandboxing.
- Op mocks are single-use per invocation; if a node/op can run multiple times, add one mock entry per expected invocation.
- For selector-backed c2ops at `@main`, mock `recipe_within_resolution` once per case and mock the c2j diagnostic node path or op `extension_execution`.
- Recipes that need cell catalogs should load them through `c2j cells --json`; tests should mock the `load_cells` node rather than pass cell lists as public inputs.
- Use `runtime: {}` for actual JobDB, input, object, child, and Git execution. The `integration_case` label alone retains the legacy executor.
- Keep artifact assertions focused on outbox contract files, not assistant summary text.
- For live skill checks, use workflow-run acceptance tests that validate authoring quality and contrarian rejection behavior, not just recipe node wiring.


## Native test ownership and migration

CLI/runtime guarantees TS-024–027, TS-049–050, TS-146, TS-163–165 and TS-168
are retained above as transferred expectations, not recipe test requirements.
Their c2j/c2ops destinations are recorded in [the coverage map](guides/NATIVE_TEST_MIGRATION.md).
TS-152–156 describe a superseded proposal; the supported review behavior is
TS-166–172. Mixed statements about restart, snapshot isolation and named-recipe
resolution are split there between runtime regressions and recipe decisions.

| Test statement | Relevant files | Importance | Level / dependencies | Case |
|---|---|---|---|---|
| Authors run all declared recipe behavior tests directly with c2j, without generating cases or starting a separate server. | `recipe-tests/*.test.yaml`, `guides/NATIVE_RECIPE_TESTING.md` | Critical | Integration; c2j, Git, declared op tools | Positive |
| Verification failures, invalid replies, and uploaded edits cannot bypass the next required review or authorize a merge. | `recipe-tests/*-lifecycle.test.yaml`, `recipe-tests/*-reviews.test.yaml` | Critical | Integration; c2j, Git, rule_gate | Negative |
| Deterministic discovery excludes live model suites unless explicitly requested. | `recipe-tests/*smoke.scenario.md` | High | CLI integration; c2j | Negative |
| Feedback retains completed dependency outcomes and evidence without submitting duplicate work. | `recipe-tests/dependency-feedback.test.yaml` | Critical | Integration; native c2j, Git, rule_gate | Positive |
| Consultations preserve the local candidate and route each cell's exact previous checkpoint. | `recipe-tests/implementation-consultations.test.yaml` | Critical | Integration; native c2j, Git, rule_gate | Positive |
| Text-only review revisions and redesigns do not inherit earlier annotations. | `recipe-tests/build-reviews.test.yaml`, `recipe-tests/evolve-reviews.test.yaml` | Critical | Integration; native c2j, Git, rule_gate | Negative |
| Consultation continuations receive the complete dependency history in their prompt, including failure details. | `recipe-tests/implementation-consultations.test.yaml` | Critical | Integration; native c2j, Git, rule_gate | Positive and negative mutation |

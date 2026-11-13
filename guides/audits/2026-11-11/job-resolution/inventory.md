# Producer inventory

Observed: 2026-11-11T02:55:30.414951+00:00
JobDB: `http://192.168.1.195:9047/c2`
Job: `3LwPwP9yqfLtuYXFWVz7G4JopWa`
Goal: `3LvaBpjvGvjri89ltvfHlvWyuC5`
Cell: `c2j`
Outcome: `COMPLETED / failed_app`
Recipe: `d102ce6ce65ac9d2735f538c8816f696aa37f3ab`
Coverage: 94 task occurrences; no next cursor.

The numbers below are local inventory indexes, not c2j selectors. Use the exact task IDs with `c2j job log JOB --task TASK --field POINTER` or `c2j job artifact JOB --task TASK --name NAME`.

## Inventory entry 1
Started: 2026-11-11T01:59:58.669519763Z; finished: 2026-11-11T02:00:04.20495171Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/task:"root-source"#1`

Selected fields: `/resolved_commit`, `/resolved_selector`.

## Inventory entry 2
Started: 2026-11-11T02:00:07.233817045Z; finished: 2026-11-11T02:00:07.23444517Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/task:"hook-policy"#1`

Selected field: `/tenant/hooks/.c2~1recipes~1hooks~1build~1verify.yaml/perms/jobdb`.

## Inventory entry 10
Started: 2026-11-11T02:02:09.664880546Z; finished: 2026-11-11T02:02:38.252916Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:direction"#1/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:review"#1/attempt:1/scope:"sequence:adaptive2-review"#1/attempt:1/scope:"op:request_human_review"#1/attempt:1/task:"input:collect_user_input"#1`

Selected fields: `/fields`, `/receipt`. Decision: accept, empty feedback.

## Inventory entry 16
Started: 2026-11-11T02:26:04.002156002Z; finished: 2026-11-11T02:27:56.581819012Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#4/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

Retrieved artifact: `request.md` (original user request).

## Inventory entry 25
Started: 2026-11-11T02:28:10.99876913Z; finished: 2026-11-11T02:28:12.705846339Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:verify"#1/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:verify"#1/attempt:1/scope:"sequence:adaptive-verify"#1/attempt:1/scope:"sequence:check"#1/attempt:1/scope:"sequence:adaptive-hook-verify"#1/attempt:1/task:"hook:446f20289738b68b5cd0175e0ff284afb4d73bc8c075e3fef91302ba0959c197:load"#1`

Selected fields: `/candidate`, `/source`.

## Inventory entry 26
Started: 2026-11-11T02:28:12.717414964Z; finished: 2026-11-11T02:28:14.359769048Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:verify"#1/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:verify"#1/attempt:1/scope:"sequence:adaptive-verify"#1/attempt:1/scope:"sequence:check"#1/attempt:1/scope:"sequence:adaptive-hook-verify"#1/attempt:1/scope:"sequence:invoke_hook"#1/attempt:1/scope:"sequence:c2j-build-verify"#1/attempt:1/scope:"op:platforms"#1/attempt:1/task:"recipe.child_group.run_and_get_result:start"#1`

Selected fields: `/children`, `/git_ref`, `/mode`. Both child records have `status: start_failed`, `error: lease permission denied`, and an empty result job ID.

## Inventory entry 30
Started: 2026-11-11T02:28:19.440717967Z; finished: 2026-11-11T02:29:59.920675291Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#5/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

## Inventory entry 32
Started: 2026-11-11T02:30:03.953492335Z; finished: 2026-11-11T02:30:42.914549048Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#6/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_read_only_session"#1/attempt:1/scope:"state:resume_read_only_session"#1/attempt:1/scope:"op:resume_read_only_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

## Inventory entry 42
Started: 2026-11-11T02:31:07.522034962Z; finished: 2026-11-11T02:31:10.421214505Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:verify"#2/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:verify"#1/attempt:1/scope:"sequence:adaptive-verify"#1/attempt:1/scope:"sequence:check"#1/attempt:1/scope:"sequence:adaptive-hook-verify"#1/attempt:1/scope:"sequence:invoke_hook"#1/attempt:1/scope:"sequence:c2j-build-verify"#1/attempt:1/scope:"op:platforms"#1/attempt:1/task:"recipe.child_group.run_and_get_result:start"#1`

Selected fields: `/children`, `/git_ref`, `/mode`. Both child records have `status: start_failed`, `error: lease permission denied`, and an empty result job ID.

## Inventory entry 46
Started: 2026-11-11T02:31:19.953473843Z; finished: 2026-11-11T02:32:08.146004962Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#7/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

## Inventory entry 56
Started: 2026-11-11T02:32:34.91030321Z; finished: 2026-11-11T02:32:37.695656837Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:verify"#3/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:verify"#1/attempt:1/scope:"sequence:adaptive-verify"#1/attempt:1/scope:"sequence:check"#1/attempt:1/scope:"sequence:adaptive-hook-verify"#1/attempt:1/scope:"sequence:invoke_hook"#1/attempt:1/scope:"sequence:c2j-build-verify"#1/attempt:1/scope:"op:platforms"#1/attempt:1/task:"recipe.child_group.run_and_get_result:start"#1`

Selected fields: `/children`, `/git_ref`, `/mode`. Both child records have `status: start_failed`, `error: lease permission denied`, and an empty result job ID.

## Inventory entry 60
Started: 2026-11-11T02:32:45.847319674Z; finished: 2026-11-11T02:34:03.89028546Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#8/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

## Inventory entry 70
Started: 2026-11-11T02:34:22.070854719Z; finished: 2026-11-11T02:34:24.09630597Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:verify"#4/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:verify"#1/attempt:1/scope:"sequence:adaptive-verify"#1/attempt:1/scope:"sequence:check"#1/attempt:1/scope:"sequence:adaptive-hook-verify"#1/attempt:1/scope:"sequence:invoke_hook"#1/attempt:1/scope:"sequence:c2j-build-verify"#1/attempt:1/scope:"op:platforms"#1/attempt:1/task:"recipe.child_group.run_and_get_result:start"#1`

Selected fields: `/children`, `/git_ref`, `/mode`. Both child records have `status: start_failed`, `error: lease permission denied`, and an empty result job ID.

## Inventory entry 74
Started: 2026-11-11T02:34:30.8206475Z; finished: 2026-11-11T02:35:15.030528382Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#9/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

## Inventory entry 84
Started: 2026-11-11T02:35:35.024708002Z; finished: 2026-11-11T02:35:37.029162211Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:verify"#5/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:verify"#1/attempt:1/scope:"sequence:adaptive-verify"#1/attempt:1/scope:"sequence:check"#1/attempt:1/scope:"sequence:adaptive-hook-verify"#1/attempt:1/scope:"sequence:invoke_hook"#1/attempt:1/scope:"sequence:c2j-build-verify"#1/attempt:1/scope:"op:platforms"#1/attempt:1/task:"recipe.child_group.run_and_get_result:start"#1`

Selected fields: `/children`, `/git_ref`, `/mode`. Both child records have `status: start_failed`, `error: lease permission denied`, and an empty result job ID.

## Inventory entry 88
Started: 2026-11-11T02:35:43.559947006Z; finished: 2026-11-11T02:36:28.971509722Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#10/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

## Inventory entry 90
Started: 2026-11-11T02:36:32.196572126Z; finished: 2026-11-11T02:37:22.439436177Z; status: succeeded.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:work"#11/attempt:1/scope:"sequence:sequence"#1/attempt:1/scope:"sequence:agent"#1/attempt:1/scope:"sequence:adaptive2-agent"#1/attempt:1/scope:"sequence:turn"#1/attempt:1/scope:"state_machine:adaptive2-agent-turn"#1/attempt:1/scope:"state_machine:state-policy:resume_implementation_session"#1/attempt:1/scope:"state:resume_implementation_session"#1/attempt:1/scope:"op:resume_implementation_session"#1/attempt:1/task:"extension_execution:extension_execution"#1`

Selected field: `/response` (especially `next`, `summary`, `questions`, and `requests`).

Retrieved artifacts: `recovery.md`, `implementation.md`, `test-results.md`, `handoff.md`, `test-statements.md`, `approved-direction/one-pager.md`, `evidence/current-verification-summary.md`, `evidence/index.md`, `stdout.jsonl`.

- `approved-direction/one-pager.md`: producer `{"kind":"stored","name":"approved-direction/one-pager.md","stored":{"key":{"jobId":"3LwPwP9yqfLtuYXFWVz7G4JopWa","taskOrdinal":95,"name":"approved-direction/one-pager.md","sizeBytes":7598}}}`
- `evidence/current-verification-summary.md`: producer `{"kind":"stored","name":"evidence/current-verification-summary.md","stored":{"key":{"jobId":"3LwPwP9yqfLtuYXFWVz7G4JopWa","taskOrdinal":95,"name":"evidence/current-verification-summary.md","sizeBytes":1462}}}`
- `handoff.md`: producer `{"kind":"stored","name":"handoff.md","stored":{"key":{"jobId":"3LwPwP9yqfLtuYXFWVz7G4JopWa","taskOrdinal":95,"name":"handoff.md","sizeBytes":2193}}}`

## Inventory entry 93
Started: 2026-11-11T02:37:25.992873179Z; finished: 2026-11-11T02:37:26.296392846Z; status: failed.

Task: `/scope:"$job"#1/attempt:1/scope:"sequence:build"#1/attempt:1/scope:"sequence:workflow"#1/attempt:1/scope:"sequence:adaptive2-workflow"#1/attempt:1/scope:"sequence:run"#1/attempt:1/scope:"state_machine:adaptive2-develop"#1/attempt:1/scope:"state:operational_failure"#1/attempt:1/scope:"sequence:operational_failure"#1/attempt:1/scope:"sequence:adaptive-operational-failure"#1/attempt:1/scope:"op:stop_attempt"#1/attempt:1/task:"command_execution:command_execution"#1`

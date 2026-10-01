# new-ticket test suite

```yaml
recipe: ../recipes/new-ticket/new-ticket.yaml
cases:
- id: ts-031-dependency-jobs-gate-local-implementation
  type: recipe_case
  inputs:
    prompt: 'Cross-cell change


      Requires dependency jobs first

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: true
            dependency_order:
            - REQ-1
            - REQ-2
            requirements:
            - id: REQ-1
              title: API prep
              target_cell: api
              depends_on: []
              scope: Prepare API contract
              api_changes: []
              acceptance_criteria:
              - API contract ready
              risks:
              - Coordination
              open_questions: []
            - id: REQ-2
              title: Local integration
              target_cell: recipe-tests
              depends_on:
              - REQ-1
              scope: Wire local usage
              api_changes: []
              acceptance_criteria:
              - Local integration works
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          requires_dependency_jobs: true
          outputs:
            plan_json: '{"summary":"Dependency jobs required","requires_dependency_jobs":true,"dependency_order":["REQ-1","REQ-2"],"dependency_job_specs":[{"id":"REQ-1","title":"API
              prep","target_cell":"api","depends_on_ids":[],"depends_on_markdown":"- (none)","scope":"Prepare API
              contract","acceptance_criteria_markdown":"- API contract ready","risks_markdown":"- Coordination delay","notes":"Must
              complete before local work"}],"local_steps":["Implement REQ-2 after REQ-1"],"notes_for_user_review":"Wait
              on dependency","compat_review_ok":true,"compat_review_feedback":"Compatible","compat_review_blocking_issues":[]}'
            summary: Dependency jobs required
            requires_dependency_jobs: true
            dependency_order:
            - REQ-1
            - REQ-2
            dependency_job_specs:
            - id: REQ-1
              title: API prep
              target_cell: api
              depends_on_ids: []
              depends_on_markdown: '- (none)'
              scope: Prepare API contract
              acceptance_criteria_markdown: '- API contract ready'
              risks_markdown: '- Coordination delay'
              notes: Must complete before local work
            local_steps:
            - Implement REQ-2 after REQ-1
            notes_for_user_review: Wait on dependency
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/spawn_dependency_jobs/recipes.run
      behavior:
        mode: return
        outputs:
          job_ids:
          - job-dep-1
    - match:
        node_path: new-ticket/dependency_wait_note/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/dependency_wait_hold/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: node_executed
    node_path: new-ticket/spawn_dependency_jobs/recipes.run
  - type: output_equals
    path: dependency_waiting
    value: true
  options:
    validation_mode: path_only
- id: ts-032-cancel-from-merge-review
  type: recipe_case
  inputs:
    prompt: 'Local implementation


      Cancel path

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-1
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 721d9e7ec81772137cea562354d9dcff7d73367149f1a58fd5d05e00cb291348
            artifact:
              jobId: sid-1
              taskOrdinal: 2
              name: __c2j_objects__/721d9e7ec81772137cea562354d9dcff7d73367149f1a58fd5d05e00cb291348.tar
              sizeBytes: 100
          assistantSummary: Implemented changes
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
    - match:
        node_path: new-ticket/validate/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          passed: true
          outputs:
            passed: true
        artifacts:
          validation/output.txt: ok
          validation/output-tail.txt: ok-tail
    - match:
        node_path: new-ticket/ready_to_merge_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: cancel_job
            feedback: ''
            upstream_repo: ''
            upstream_branch: ''
            commit_message: ''
    - match:
        node_path: new-ticket/cancel_job_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_done/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: node_executed
    node_path: new-ticket/cancel_job_route/sleep
  - type: output_equals
    path: canceled
    value: true
  options:
    validation_mode: path_only
- id: ts-033-merge-without-hash-forces-resolution
  type: recipe_case
  inputs:
    prompt: 'Merge without hash


      Merge decision should return to implementation when no hash exists

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: Proceed to merge check.
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-h0
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 01fd446391e2c95ebf4f971f08654443ebefa9cc50acc6d7ad0d33c252e5fce1
            artifact:
              jobId: sid-h0
              taskOrdinal: 3
              name: __c2j_objects__/01fd446391e2c95ebf4f971f08654443ebefa9cc50acc6d7ad0d33c252e5fce1.tar
              sizeBytes: 100
          assistantSummary: Pre-merge implementation completed
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
    - match:
        node_path: new-ticket/validate/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          passed: true
          outputs:
            passed: true
        artifacts:
          validation/output.txt: ok
          validation/output-tail.txt: ok-tail
    - match:
        node_path: new-ticket/ready_to_merge_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: merge
            feedback: ''
            upstream_repo: ''
            upstream_branch: ''
            commit_message: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: incomplete
          sessionId: sid-h1
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 7a26263b98eee3b67581a82add62f7d7ca83faff46b9535e3cb16c1b1269113c
            artifact:
              jobId: sid-h1
              taskOrdinal: 4
              name: __c2j_objects__/7a26263b98eee3b67581a82add62f7d7ca83faff46b9535e3cb16c1b1269113c.tar
              sizeBytes: 100
          assistantSummary: Need clarification before merge
          incompleteReason: 1. Confirm expected merge behavior with no local hash.
          incompleteCategory: needs_user_input
          pendingDependencies: []
    - match:
        node_path: new-ticket/pre_implementation_followup_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: cancel_job
            feedback: ''
            implementation_answers: ''
    - match:
        node_path: new-ticket/cancel_job_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_done/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: output_equals
    path: canceled
    value: true
  options:
    validation_mode: path_only
- id: ts-034-merge-success-completes-job
  type: recipe_case
  inputs:
    prompt: 'Merge success


      Complete job after merge

      '
    local_hash: deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
    upstream_repo: git@example.com:org/repo.git
    upstream_branch: main
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-merge
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: d7b02801dc5f0274745c9ea1b34127293310f450f63b71279ed04e81748ea440
            artifact:
              jobId: sid-merge
              taskOrdinal: 5
              name: __c2j_objects__/d7b02801dc5f0274745c9ea1b34127293310f450f63b71279ed04e81748ea440.tar
              sizeBytes: 100
          assistantSummary: Implemented changes
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
    - match:
        node_path: new-ticket/validate/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          passed: true
          outputs:
            passed: true
        artifacts:
          validation/output.txt: ok
          validation/output-tail.txt: ok-tail
    - match:
        node_path: new-ticket/ready_to_merge_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: merge
            feedback: ''
            upstream_repo: ''
            upstream_branch: ''
            commit_message: ''
    - match:
        node_path: new-ticket/merge/squashrebasemerge
      behavior:
        mode: return
        outputs:
          merged_hash: cafebabecafebabecafebabecafebabecafebabe
          target_branch: main
    - match:
        node_path: new-ticket/complete_done_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/complete_done_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/complete_done_noop/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: output_equals
    path: merged_hash
    value: cafebabecafebabecafebabecafebabecafebabe
  - type: output_equals
    path: job_done
    value: true
  options:
    validation_mode: path_only
- id: ts-035-implementation-opens-cross-cell-bug-jobs
  type: recipe_case
  inputs:
    prompt: 'Implementation finds external bug


      Bug job should be created

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-bug
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 9bcc388eff8a647357eec2bd679ce3cda54c061780ea9e17139fe8eb8ef6ca2b
            artifact:
              jobId: sid-bug
              taskOrdinal: 6
              name: __c2j_objects__/9bcc388eff8a647357eec2bd679ce3cda54c061780ea9e17139fe8eb8ef6ca2b.tar
              sizeBytes: 100
          assistantSummary: Found bug in api cell
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies:
          - component: api
            requestedChanges: 'Bug: null pointer in API validation path.

              Repro: send empty payload to /v1/items.'
    - match:
        node_path: new-ticket/implement_bugs/recipes.run
      behavior:
        mode: return
        outputs:
          job_ids:
          - job-bug-1
    - match:
        node_path: new-ticket/validate/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          passed: true
          outputs:
            passed: true
        artifacts:
          validation/output.txt: ok
          validation/output-tail.txt: ok-tail
    - match:
        node_path: new-ticket/ready_to_merge_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: cancel_job
            feedback: ''
            upstream_repo: ''
            upstream_branch: ''
            commit_message: ''
    - match:
        node_path: new-ticket/cancel_job_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_done/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: node_executed
    node_path: new-ticket/implement_bugs/recipes.run
  - type: output_equals
    path: canceled
    value: true
  options:
    validation_mode: path_only
- id: ts-036-implementation-questions-pause-and-resume
  type: recipe_case
  inputs:
    prompt: 'Implementation needs clarification


      Prompt user and resume codex

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: incomplete
          sessionId: sid-q1
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 1bebed5c95decaffbda1fc7e206654aa41447ef40c4fa0d9d9a45f6bdce5b411
            artifact:
              jobId: sid-q1
              taskOrdinal: 7
              name: __c2j_objects__/1bebed5c95decaffbda1fc7e206654aa41447ef40c4fa0d9d9a45f6bdce5b411.tar
              sizeBytes: 100
          assistantSummary: Needs clarification
          incompleteReason: 1. Should retries be enabled globally or endpoint-specific?
          incompleteCategory: needs_user_input
          pendingDependencies: []
    - match:
        node_path: new-ticket/pre_implementation_followup_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: 1) Endpoint-specific retries only.
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-q1
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: a6a99e130030d7b6e8dabb620227d60b0acfe29ebdebede4184616e8eaf166b5
            artifact:
              jobId: sid-q1
              taskOrdinal: 8
              name: __c2j_objects__/a6a99e130030d7b6e8dabb620227d60b0acfe29ebdebede4184616e8eaf166b5.tar
              sizeBytes: 100
          assistantSummary: Clarification applied and implementation completed
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
    - match:
        node_path: new-ticket/validate/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          passed: true
          outputs:
            passed: true
        artifacts:
          validation/output.txt: ok
          validation/output-tail.txt: ok-tail
    - match:
        node_path: new-ticket/ready_to_merge_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: cancel_job
            feedback: ''
            upstream_repo: ''
            upstream_branch: ''
            commit_message: ''
    - match:
        node_path: new-ticket/cancel_job_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_done/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: node_executed
    node_path: new-ticket/pre_implementation_review/input
  - type: node_executed
    node_path: new-ticket/implement/state_machine/fresh/git+https://github.com/colony-2/c2ops.git//codex/run_skill@ded76dfbd877d3d0749e509844ecdbc57197b572
  - type: output_equals
    path: implementation_user_questions_requested
    value: true
  options:
    validation_mode: path_only
- id: ts-040-outcome-commands-feed-validation-default
  type: recipe_case
  inputs:
    prompt: 'Use outcome validation commands


      Validation should default to outcome command plan

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: sid-validation
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 47b12cb79816904591bdb8930513c945ae862b6e3adcd44276e227b624ed3ff4
            artifact:
              jobId: sid-validation
              taskOrdinal: 9
              name: __c2j_objects__/47b12cb79816904591bdb8930513c945ae862b6e3adcd44276e227b624ed3ff4.tar
              sizeBytes: 100
          assistantSummary: Implemented changes
          incompleteReason: ''
          incompleteCategory: ''
          pendingDependencies: []
    - match:
        node_path: new-ticket/validate/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          passed: true
          outputs:
            passed: true
        artifacts:
          validation/output.txt: ok
          validation/output-tail.txt: ok-tail
    - match:
        node_path: new-ticket/ready_to_merge_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: cancel_job
            feedback: ''
            upstream_repo: ''
            upstream_branch: ''
            commit_message: ''
    - match:
        node_path: new-ticket/cancel_job_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_done/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: node_executed
    node_path: new-ticket/pre_implementation_review/input
  - type: output_equals
    path: validation_selected_commands
    value: npm test
  options:
    validation_mode: path_only
- id: ts-041-implementation-requests-test-statement-update
  type: recipe_case
  inputs:
    prompt: 'Implementation requests statement revision


      Request should route to follow-up review gate

      '
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        node_path: new-ticket/triage/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          outputs:
            cell_is_appropriate: true
            recommended_cell: recipe-tests
            recommended_cell_is_valid: true
            recommended_cell_final: recipe-tests
            rationale: In-cell
    - match:
        node_path: new-ticket/requirements_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          api_review_ok: true
          outputs:
            plan_json: '{"summary":"Reqs"}'
            summary: Requirements ready
            needs_cross_cell_support: false
            dependency_order:
            - REQ-1
            requirements:
            - id: REQ-1
              title: Local change
              target_cell: recipe-tests
              depends_on: []
              scope: Implement locally
              api_changes: []
              acceptance_criteria:
              - Local behavior updated
              risks: []
              open_questions: []
            notes_for_user_review: Review requirements
            api_review_ok: true
            api_review_feedback: Compatible
            api_review_blocking_issues: []
        artifacts:
          requirements/plan.json: '{"summary":"Reqs"}'
          requirements/index.md: '# Requirements'
          requirements/api-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/implementation_planning/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          compat_review_ok: true
          outputs:
            plan_json: '{"summary":"Impl"}'
            summary: Local plan
            requires_dependency_jobs: false
            dependency_order:
            - REQ-1
            dependency_job_specs: []
            local_steps:
            - Implement feature
            notes_for_user_review: Ready
            compat_review_ok: true
            compat_review_feedback: Compatible
            compat_review_blocking_issues: []
        artifacts:
          implementation/plan.json: '{"summary":"Impl"}'
          implementation/index.md: '# Implementation'
          implementation/compat-review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/outcome_determination/recipe.run_and_get_result
      behavior:
        mode: return
        outputs:
          review_ok: true
          outputs:
            plan_json: '{"summary":"Outcome"}'
            summary: Outcome
            current_test_statements_summary: Existing statements cover baseline
            test_statement_updates_required: true
            test_statement_repo_glob: .c2/tests/*.md
            validation_commands: npm test
            notes_for_user_review: Add negative path checks
            review_ok: true
            review_feedback: Looks good
            review_blocking_issues: []
        artifacts:
          outcome/plan.json: '{"summary":"Outcome"}'
          outcome/index.md: '# Outcome'
          outcome/tests-index.md: '# Tests index'
          outcome/validation-commands.txt: npm test
          outcome/review.json: '{"ok":true}'
    - match:
        node_path: new-ticket/pre_implementation_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: continue
            feedback: ''
            implementation_answers: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: incomplete
          sessionId: sid-ts-update
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 1467eff3781684d1e0cbbec12cce8c89d19d072a14aee0b229d50a1347246ecf
            artifact:
              jobId: sid-ts-update
              taskOrdinal: 10
              name: __c2j_objects__/1467eff3781684d1e0cbbec12cce8c89d19d072a14aee0b229d50a1347246ecf.tar
              sizeBytes: 100
          assistantSummary: Needs test statement update
          incompleteReason: Add negative case for retries exhausted path in .c2/tests/service.md.
          incompleteCategory: needs_test_statement_update
          pendingDependencies: []
    - match:
        node_path: new-ticket/pre_implementation_followup_review/input
      behavior:
        mode: return
        outputs:
          fields:
            decision: cancel_job
            feedback: ''
            implementation_answers: ''
    - match:
        node_path: new-ticket/cancel_job_route/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_update/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
    - match:
        node_path: new-ticket/cancel_job_done/sleep
      behavior:
        mode: return
        outputs:
          completed: true
          interrupted: false
          actual_duration: 1ms
          error_message: ''
  assertions:
  - type: node_executed
    node_path: new-ticket/pre_implementation_review/input
  - type: output_equals
    path: implementation_requested_test_statement_update
    value: true
  - type: output_equals
    path: canceled
    value: true
  options:
    validation_mode: path_only
```

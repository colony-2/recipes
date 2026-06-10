# new-ticket-requirements-planning test suite

```yaml
cases:
  - id: ts-005-plan-bundle-artifacts
    type: recipe_case
    inputs:
      prompt: |
        Add auth

        Add auth requirements
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-requirements-planning/load_cells
          behavior:
            mode: return
            outputs:
              stdout: '[{"short_name":"core","repo":"https://github.com/colony-2/core.git"},{"short_name":"frontend","repo":"https://github.com/colony-2/frontend.git"},{"short_name":"api","repo":"https://github.com/colony-2/api.git"},{"short_name":"recipe-tests","repo":"https://github.com/colony-2/recipe-tests.git"}]'
              exit_code: 0
            artifacts:
              feedback/user-feedback.md: ""
              feedback/api-review-feedback.md: ""
              requirements/prior-plan.json: ""
              requirements/plan.json: ""
              requirements/api-review.json: ""
              requirements/index.md: ""
              implementation/plan.json: ""
              implementation/index.md: ""
              outcome/plan.json: ""
              outcome/review.json: ""
              outcome/tests-index.md: ""
              outcome/validation-commands.txt: ""
        - match:
            node_path: new-ticket-requirements-planning/persist_plan_and_docs
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Auth plan","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Add auth","target_cell":"core","depends_on":[],"scope":"Introduce auth checks","api_changes":[],"acceptance_criteria":["Auth required for protected routes"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Review auth boundary"}'
            artifacts:
              requirements/plan.json: '{"summary":"Auth plan","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Add auth","target_cell":"core","depends_on":[],"scope":"Introduce auth checks","api_changes":[],"acceptance_criteria":["Auth required for protected routes"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Review auth boundary"}'
              requirements/index.md: '# Requirements\n- REQ-1'
              requirements/REQ-1.md: '# REQ-1\nAuth requirement' 
        - match:
            node_path: new-ticket-requirements-planning/contrarian_api_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"Compatible","blocking_issues":[]}'
            artifacts:
              requirements/api-review.json: '{"ok":true,"feedback":"Compatible","blocking_issues":[]}'
              requirements/api-review.md: '# API review (contrarian)' 
    assertions:
      - type: artifact_exists
        path: requirements/plan.json
      - type: artifact_exists
        path: requirements/index.md
      - type: artifact_exists
        path: requirements/REQ-1.md

  - id: ts-006-requirement-structure-output
    type: recipe_case
    inputs:
      prompt: |
        Multi-step feature

        Requires dependency ordering
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-requirements-planning/load_cells
          behavior:
            mode: return
            outputs:
              stdout: '[{"short_name":"core","repo":"https://github.com/colony-2/core.git"},{"short_name":"frontend","repo":"https://github.com/colony-2/frontend.git"},{"short_name":"api","repo":"https://github.com/colony-2/api.git"},{"short_name":"recipe-tests","repo":"https://github.com/colony-2/recipe-tests.git"}]'
              exit_code: 0
            artifacts:
              feedback/user-feedback.md: ""
              feedback/api-review-feedback.md: ""
              requirements/prior-plan.json: ""
              requirements/plan.json: ""
              requirements/api-review.json: ""
              requirements/index.md: ""
              implementation/plan.json: ""
              implementation/index.md: ""
              outcome/plan.json: ""
              outcome/review.json: ""
              outcome/tests-index.md: ""
              outcome/validation-commands.txt: ""
        - match:
            node_path: new-ticket-requirements-planning/persist_plan_and_docs
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Two-step plan","needs_cross_cell_support":false,"dependency_order":["REQ-1","REQ-2"],"requirements":[{"id":"REQ-1","title":"Base","target_cell":"core","depends_on":[],"scope":"Base scope","api_changes":[],"acceptance_criteria":["Base works"],"risks":[],"open_questions":[]},{"id":"REQ-2","title":"Follow-up","target_cell":"core","depends_on":["REQ-1"],"scope":"Follow-up scope","api_changes":[],"acceptance_criteria":["Follow-up works"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Order matters"}'
            artifacts:
              requirements/plan.json: '{"summary":"Two-step plan","needs_cross_cell_support":false,"dependency_order":["REQ-1","REQ-2"],"requirements":[{"id":"REQ-1","title":"Base","target_cell":"core","depends_on":[],"scope":"Base scope","api_changes":[],"acceptance_criteria":["Base works"],"risks":[],"open_questions":[]},{"id":"REQ-2","title":"Follow-up","target_cell":"core","depends_on":["REQ-1"],"scope":"Follow-up scope","api_changes":[],"acceptance_criteria":["Follow-up works"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Order matters"}'
              requirements/index.md: '# Requirements\n- REQ-1\n- REQ-2'
              requirements/REQ-1.md: '# REQ-1'
              requirements/REQ-2.md: '# REQ-2' 
        - match:
            node_path: new-ticket-requirements-planning/contrarian_api_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"Looks good","blocking_issues":[]}'
            artifacts:
              requirements/api-review.json: '{"ok":true,"feedback":"Looks good","blocking_issues":[]}'
              requirements/api-review.md: '# API review (contrarian)' 
    assertions:
      - type: output_equals
        path: dependency_order
        value: [REQ-1, REQ-2]
      - type: output_equals
        path: needs_cross_cell_support
        value: false

  - id: ts-007-user-feedback-roundtrip
    type: recipe_case
    inputs:
      prompt: |
        Add caching

        Improve performance
      user_feedback: Include cache invalidation strategy
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-requirements-planning/load_cells
          behavior:
            mode: return
            outputs:
              stdout: '[{"short_name":"core","repo":"https://github.com/colony-2/core.git"},{"short_name":"frontend","repo":"https://github.com/colony-2/frontend.git"},{"short_name":"api","repo":"https://github.com/colony-2/api.git"},{"short_name":"recipe-tests","repo":"https://github.com/colony-2/recipe-tests.git"}]'
              exit_code: 0
            artifacts:
              feedback/user-feedback.md: ""
              feedback/api-review-feedback.md: ""
              requirements/prior-plan.json: ""
              requirements/plan.json: ""
              requirements/api-review.json: ""
              requirements/index.md: ""
              implementation/plan.json: ""
              implementation/index.md: ""
              outcome/plan.json: ""
              outcome/review.json: ""
              outcome/tests-index.md: ""
              outcome/validation-commands.txt: ""
        - match:
            node_path: new-ticket-requirements-planning/persist_plan_and_docs
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Updated with user feedback","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Caching","target_cell":"core","depends_on":[],"scope":"Add cache and invalidation","api_changes":[],"acceptance_criteria":["Cache invalidates on writes"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Feedback applied"}'
            artifacts:
              requirements/plan.json: '{"summary":"Updated with user feedback","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Caching","target_cell":"core","depends_on":[],"scope":"Add cache and invalidation","api_changes":[],"acceptance_criteria":["Cache invalidates on writes"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Feedback applied"}'
              requirements/index.md: '# Requirements\n- REQ-1'
              requirements/REQ-1.md: '# REQ-1' 
        - match:
            node_path: new-ticket-requirements-planning/contrarian_api_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"Feedback integrated","blocking_issues":[]}'
            artifacts:
              requirements/api-review.json: '{"ok":true,"feedback":"Feedback integrated","blocking_issues":[]}'
              requirements/api-review.md: '# API review (contrarian)' 
    assertions:
      - type: output_equals
        path: summary
        value: Updated with user feedback
      - type: output_equals
        path: notes_for_user_review
        value: Feedback applied

  - id: ts-008-blocking-api-review-signal
    type: recipe_case
    inputs:
      prompt: |
        Breaking API proposal

        Introduce breaking change
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-requirements-planning/load_cells
          behavior:
            mode: return
            outputs:
              stdout: '[{"short_name":"core","repo":"https://github.com/colony-2/core.git"},{"short_name":"frontend","repo":"https://github.com/colony-2/frontend.git"},{"short_name":"api","repo":"https://github.com/colony-2/api.git"},{"short_name":"recipe-tests","repo":"https://github.com/colony-2/recipe-tests.git"}]'
              exit_code: 0
            artifacts:
              feedback/user-feedback.md: ""
              feedback/api-review-feedback.md: ""
              requirements/prior-plan.json: ""
              requirements/plan.json: ""
              requirements/api-review.json: ""
              requirements/index.md: ""
              implementation/plan.json: ""
              implementation/index.md: ""
              outcome/plan.json: ""
              outcome/review.json: ""
              outcome/tests-index.md: ""
              outcome/validation-commands.txt: ""
        - match:
            node_path: new-ticket-requirements-planning/persist_plan_and_docs
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Breaking plan","needs_cross_cell_support":true,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Break API","target_cell":"core","depends_on":[],"scope":"Break endpoint","api_changes":[{"service":"api","change_type":"breaking","description":"Remove field","backwards_compatible":false,"migration_plan":"None"}],"acceptance_criteria":["Clients migrated"],"risks":["Client impact"],"open_questions":[]}],"notes_for_user_review":"Needs approval"}'
            artifacts:
              requirements/plan.json: '{"summary":"Breaking plan","needs_cross_cell_support":true,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Break API","target_cell":"core","depends_on":[],"scope":"Break endpoint","api_changes":[{"service":"api","change_type":"breaking","description":"Remove field","backwards_compatible":false,"migration_plan":"None"}],"acceptance_criteria":["Clients migrated"],"risks":["Client impact"],"open_questions":[]}],"notes_for_user_review":"Needs approval"}'
              requirements/index.md: '# Requirements\n- REQ-1'
              requirements/REQ-1.md: '# REQ-1' 
        - match:
            node_path: new-ticket-requirements-planning/contrarian_api_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":false,"feedback":"Breaking change lacks migration","blocking_issues":["Missing migration plan"]}'
            artifacts:
              requirements/api-review.json: '{"ok":false,"feedback":"Breaking change lacks migration","blocking_issues":["Missing migration plan"]}'
              requirements/api-review.md: '# API review (contrarian)' 
    assertions:
      - type: output_equals
        path: api_review_ok
        value: false
      - type: output_equals
        path: api_review_blocking_issues
        value: [Missing migration plan]

  - id: ts-009-api-review-artifacts
    type: recipe_case
    inputs:
      prompt: |
        API review artifact check

        Ensure contrarian artifacts emitted
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-requirements-planning/load_cells
          behavior:
            mode: return
            outputs:
              stdout: '[{"short_name":"core","repo":"https://github.com/colony-2/core.git"},{"short_name":"frontend","repo":"https://github.com/colony-2/frontend.git"},{"short_name":"api","repo":"https://github.com/colony-2/api.git"},{"short_name":"recipe-tests","repo":"https://github.com/colony-2/recipe-tests.git"}]'
              exit_code: 0
            artifacts:
              feedback/user-feedback.md: ""
              feedback/api-review-feedback.md: ""
              requirements/prior-plan.json: ""
              requirements/plan.json: ""
              requirements/api-review.json: ""
              requirements/index.md: ""
              implementation/plan.json: ""
              implementation/index.md: ""
              outcome/plan.json: ""
              outcome/review.json: ""
              outcome/tests-index.md: ""
              outcome/validation-commands.txt: ""
        - match:
            node_path: new-ticket-requirements-planning/persist_plan_and_docs
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Artifact check","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Check","target_cell":"core","depends_on":[],"scope":"Check","api_changes":[],"acceptance_criteria":["ok"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Artifact check"}'
            artifacts:
              requirements/plan.json: '{"summary":"Artifact check","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Check","target_cell":"core","depends_on":[],"scope":"Check","api_changes":[],"acceptance_criteria":["ok"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Artifact check"}'
              requirements/index.md: '# Requirements\n- REQ-1'
              requirements/REQ-1.md: '# REQ-1' 
        - match:
            node_path: new-ticket-requirements-planning/contrarian_api_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"All good","blocking_issues":[]}'
            artifacts:
              requirements/api-review.json: '{"ok":true,"feedback":"All good","blocking_issues":[]}'
              requirements/api-review.md: '# API review (contrarian)' 
    assertions:
      - type: artifact_exists
        path: requirements/api-review.json
      - type: artifact_exists
        path: requirements/api-review.md

  - id: ts-010-plan-and-review-coexist
    type: recipe_case
    inputs:
      prompt: |
        Full bundle

        Verify combined artifact set
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-requirements-planning/load_cells
          behavior:
            mode: return
            outputs:
              stdout: '[{"short_name":"core","repo":"https://github.com/colony-2/core.git"},{"short_name":"frontend","repo":"https://github.com/colony-2/frontend.git"},{"short_name":"api","repo":"https://github.com/colony-2/api.git"},{"short_name":"recipe-tests","repo":"https://github.com/colony-2/recipe-tests.git"}]'
              exit_code: 0
            artifacts:
              feedback/user-feedback.md: ""
              feedback/api-review-feedback.md: ""
              requirements/prior-plan.json: ""
              requirements/plan.json: ""
              requirements/api-review.json: ""
              requirements/index.md: ""
              implementation/plan.json: ""
              implementation/index.md: ""
              outcome/plan.json: ""
              outcome/review.json: ""
              outcome/tests-index.md: ""
              outcome/validation-commands.txt: ""
        - match:
            node_path: new-ticket-requirements-planning/persist_plan_and_docs
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Full bundle","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Bundle","target_cell":"core","depends_on":[],"scope":"Bundle scope","api_changes":[],"acceptance_criteria":["bundle complete"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Bundle review"}'
            artifacts:
              requirements/plan.json: '{"summary":"Full bundle","needs_cross_cell_support":false,"dependency_order":["REQ-1"],"requirements":[{"id":"REQ-1","title":"Bundle","target_cell":"core","depends_on":[],"scope":"Bundle scope","api_changes":[],"acceptance_criteria":["bundle complete"],"risks":[],"open_questions":[]}],"notes_for_user_review":"Bundle review"}'
              requirements/index.md: '# Requirements\n- REQ-1'
              requirements/REQ-1.md: '# REQ-1' 
        - match:
            node_path: new-ticket-requirements-planning/contrarian_api_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"Bundle ok","blocking_issues":[]}'
            artifacts:
              requirements/api-review.json: '{"ok":true,"feedback":"Bundle ok","blocking_issues":[]}'
              requirements/api-review.md: '# API review (contrarian)' 
    assertions:
      - type: artifact_exists
        path: requirements/plan.json
      - type: artifact_exists
        path: requirements/api-review.json
```

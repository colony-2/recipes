# new-ticket-outcome-determination test suite

```yaml
recipe: ../recipes/new-ticket/new-ticket-outcome-determination.yaml
cases:
  - id: ts-037-outcome-bundle-artifacts
    type: recipe_case
    inputs:
      prompt: |
        Outcome planning

        Build test statements before implementation
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-outcome-determination/load_cells
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
            node_path: new-ticket-outcome-determination/build_outcome_bundle
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Outcome ready","current_test_statements_summary":"Existing statements found for API and service integration","test_statement_updates_required":true,"test_statement_repo_glob":".c2/tests/*.md","validation_commands":"npm test\nnpm run lint","notes_for_user_review":"Review updated negative-path coverage"}'
            artifacts:
              outcome/plan.json: '{"summary":"Outcome ready","current_test_statements_summary":"Existing statements found for API and service integration","test_statement_updates_required":true,"test_statement_repo_glob":".c2/tests/*.md","validation_commands":"npm test\nnpm run lint","notes_for_user_review":"Review updated negative-path coverage"}'
              outcome/index.md: '# Outcome bundle'
              outcome/tests-index.md: '# Tests index'
              outcome/validation-commands.txt: 'npm test\nnpm run lint' 
        - match:
            node_path: new-ticket-outcome-determination/contrarian_outcome_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"Outcome quality is acceptable","blocking_issues":[]}'
            artifacts:
              outcome/review.json: '{"ok":true,"feedback":"Outcome quality is acceptable","blocking_issues":[]}'
              outcome/review.md: '# Outcome review (contrarian)' 
    assertions:
      - type: artifact_exists
        path: outcome/plan.json
      - type: artifact_exists
        path: outcome/tests-index.md
      - type: artifact_exists
        path: outcome/review.json
      - type: output_equals
        path: test_statement_repo_glob
        value: .c2/tests/*.md

  - id: ts-038-outcome-outputs-include-validation-commands
    type: recipe_case
    inputs:
      prompt: |
        Validate mapping

        Ensure outputs expose command plan
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-outcome-determination/load_cells
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
            node_path: new-ticket-outcome-determination/build_outcome_bundle
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Outcome mapped","current_test_statements_summary":"No existing statements in cell","test_statement_updates_required":true,"test_statement_repo_glob":".c2/tests/*.md","validation_commands":"go test ./...","notes_for_user_review":"Baseline statements created"}'
            artifacts:
              outcome/plan.json: '{"summary":"Outcome mapped","current_test_statements_summary":"No existing statements in cell","test_statement_updates_required":true,"test_statement_repo_glob":".c2/tests/*.md","validation_commands":"go test ./...","notes_for_user_review":"Baseline statements created"}'
              outcome/index.md: '# Outcome mapped'
              outcome/tests-index.md: '# Tests index'
              outcome/validation-commands.txt: 'go test ./...' 
        - match:
            node_path: new-ticket-outcome-determination/contrarian_outcome_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":true,"feedback":"Looks good","blocking_issues":[]}'
            artifacts:
              outcome/review.json: '{"ok":true,"feedback":"Looks good","blocking_issues":[]}'
              outcome/review.md: '# Outcome review (contrarian)' 
    assertions:
      - type: output_equals
        path: validation_commands
        value: go test ./...
      - type: output_equals
        path: test_statement_updates_required
        value: true

  - id: ts-039-outcome-review-blocks-invalid-statements
    type: recipe_case
    inputs:
      prompt: |
        Bad outcome quality

        Contrarian review blocks weak statements
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: new-ticket-outcome-determination/load_cells
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
            node_path: new-ticket-outcome-determination/build_outcome_bundle
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"summary":"Draft outcome","current_test_statements_summary":"Legacy statements missing metadata","test_statement_updates_required":true,"test_statement_repo_glob":".c2/tests/*.md","validation_commands":"python3 -m pytest -q","notes_for_user_review":"Needs stricter statement format"}'
            artifacts:
              outcome/plan.json: '{"summary":"Draft outcome","current_test_statements_summary":"Legacy statements missing metadata","test_statement_updates_required":true,"test_statement_repo_glob":".c2/tests/*.md","validation_commands":"python3 -m pytest -q","notes_for_user_review":"Needs stricter statement format"}'
              outcome/index.md: '# Draft outcome'
              outcome/tests-index.md: '# Tests index'
              outcome/validation-commands.txt: 'python3 -m pytest -q' 
        - match:
            node_path: new-ticket-outcome-determination/contrarian_outcome_review
          behavior:
            mode: return
            outputs:
              status: completed
              assistantSummary: '{"ok":false,"feedback":"Statements exceed word limit and miss polarity","blocking_issues":["Word limit violations","Missing polarity annotations"]}'
            artifacts:
              outcome/review.json: '{"ok":false,"feedback":"Statements exceed word limit and miss polarity","blocking_issues":["Word limit violations","Missing polarity annotations"]}'
              outcome/review.md: '# Outcome review (contrarian)' 
    assertions:
      - type: output_equals
        path: review_ok
        value: false
      - type: output_equals
        path: review_blocking_issues
        value: [Word limit violations, Missing polarity annotations]
```

# job-validate test suite

```yaml
recipe: ../recipes/new-ticket/job-validate.yaml
cases:
  - id: ts-014-run-provided-commands
    type: recipe_case
    inputs:
      commands: npm test
    mocks:
      ops:
        - match:
            node_path: job-validate/detect_validation_command/detect_validation_command
          behavior:
            mode: return
            outputs:
              stdout: '{"suggested_commands":"npm test"}'
              exit_code: 0
        - match:
            node_path: job-validate/run_provided_validation/run_provided_validation
          behavior:
            mode: return
            outputs:
              exit_code: 0
            artifacts:
              validation/output.txt: 'ok'
              validation/output-tail.txt: 'ok-tail'
    assertions:
      - type: output_equals
        path: passed
        value: true
      - type: artifact_exists
        path: validation/output.txt
      - type: artifact_exists
        path: validation/output-tail.txt

  - id: ts-015-run-suggested-commands
    type: recipe_case
    inputs:
      commands: ""
    mocks:
      ops:
        - match:
            node_path: job-validate/detect_validation_command/detect_validation_command
          behavior:
            mode: return
            outputs:
              stdout: '{"suggested_commands":"go test ./..."}'
              exit_code: 0
        - match:
            node_path: job-validate/choose_validation_mode/choose_validation_mode
          behavior:
            mode: return
            outputs:
              response: use_suggested
        - match:
            node_path: job-validate/run_suggested_validation/run_suggested_validation
          behavior:
            mode: return
            outputs:
              exit_code: 0
            artifacts:
              validation/output.txt: 'go test ok'
              validation/output-tail.txt: 'go test ok tail'
    assertions:
      - type: output_equals
        path: passed
        value: true
      - type: artifact_exists
        path: validation/output.txt

  - id: ts-016-run-custom-commands
    type: recipe_case
    inputs:
      commands: ""
    mocks:
      ops:
        - match:
            node_path: job-validate/detect_validation_command/detect_validation_command
          behavior:
            mode: return
            outputs:
              stdout: '{"suggested_commands":"python3 -m pytest -q"}'
              exit_code: 0
        - match:
            node_path: job-validate/choose_validation_mode/choose_validation_mode
          behavior:
            mode: return
            outputs:
              response: provide_custom
        - match:
            node_path: job-validate/collect_validation_command/collect_validation_command
          behavior:
            mode: return
            outputs:
              response: python3 -m pytest -q
        - match:
            node_path: job-validate/run_custom_validation/run_custom_validation
          behavior:
            mode: return
            outputs:
              exit_code: 0
            artifacts:
              validation/output.txt: 'pytest ok'
              validation/output-tail.txt: 'pytest ok tail'
    assertions:
      - type: output_equals
        path: passed
        value: true
      - type: artifact_exists
        path: validation/output-tail.txt

  - id: ts-017-failed-validation-signals
    type: recipe_case
    inputs:
      commands: npm test
    mocks:
      ops:
        - match:
            node_path: job-validate/detect_validation_command/detect_validation_command
          behavior:
            mode: return
            outputs:
              stdout: '{"suggested_commands":"npm test"}'
              exit_code: 0
        - match:
            node_path: job-validate/run_provided_validation/run_provided_validation
          behavior:
            mode: return
            outputs:
              exit_code: 1
            artifacts:
              validation/output.txt: 'failing tests'
              validation/output-tail.txt: 'failing tail'
    assertions:
      - type: output_equals
        path: passed
        value: false
      - type: output_equals
        path: exit_code
        value: 1

  - id: ts-018-output-artifact-contract
    type: recipe_case
    inputs:
      commands: npm test
    mocks:
      ops:
        - match:
            node_path: job-validate/detect_validation_command/detect_validation_command
          behavior:
            mode: return
            outputs:
              stdout: '{"suggested_commands":"npm test"}'
              exit_code: 0
        - match:
            node_path: job-validate/run_provided_validation/run_provided_validation
          behavior:
            mode: return
            outputs:
              exit_code: 0
            artifacts:
              validation/output.txt: 'ok'
              validation/output-tail.txt: 'ok-tail'
    assertions:
      - type: output_equals
        path: output_artifact
        value: validation/output.txt
      - type: output_equals
        path: output_tail_artifact
        value: validation/output-tail.txt
```

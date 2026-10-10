# Build recipe behavior

Executable declarations; run `c2j test run --file recipe-tests/build.scenario.md`.

```yaml
recipe: ../build.yaml
cases:
- id: happy
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - &id001
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id002
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id003
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - &id004
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id005
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id006
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - &id007
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Review the maintained test plan."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id008
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id009
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Review the maintained test plan."}'
          stderr: ''
    - &id010
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"ok": true}'
          stderr: ''
        artifacts:
          test-statements.md: '# Test statements'
    - &id011
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id012
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id013
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - &id014
      match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: approve
          artifact_refs: {}
          receipt: {}
    - &id015
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id016
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id017
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - &id018
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id019
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id020
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - &id021
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - &id022
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id023
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - &id024
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - &id025
      match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - &id026
      match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: satisfied
          artifact_refs: {}
          receipt: {}
    - &id027
      match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - &id028
      match:
        op: squashrebasemerge
      behavior:
        mode: return
        outputs:
          merged_hash: merged-hash
          target_branch: main
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() == 7 &&
      calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[0].node_path.contains("/design/")
      && calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[1].node_path.contains("/design_review/")
      && calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[2].node_path.contains("/test_plan/")
      && calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[3].node_path.contains("/test_review/")
      && calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[4].node_path.contains("/implementation/")
      && calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[5].node_path.contains("/specification/")
      && calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[6].node_path.contains("/quality/")
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[0].node_path.startsWith("build/develop/root/design/design/development-agent/run/state_machine/root_fresh/")
  options:
    validation_mode: structure_only
- id: direct-plan-feedback
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Review the maintained test plan."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Review the maintained test plan."}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"ok": true}'
          stderr: ''
        artifacts:
          test-statements.md: '# Test statements'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Clarify outcomes
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/design/"))[calls.filter(c,
      c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/design/")).size()-1].inputs.inputs.prompt.contains("Clarify
      outcomes")
  - type: cel_true
    expr: '!calls.exists(c, c.node_path.endsWith("/plan_feedback/input"))'
  options:
    validation_mode: structure_only
- id: direct-implementation-feedback
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Direct revision
          artifact_refs: {}
          receipt: {}
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/"))[calls.filter(c,
      c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).size()-1].inputs.inputs.prompt.contains("Direct
      revision")
  - type: cel_true
    expr: '!calls.exists(c, c.node_path.endsWith("/implementation_feedback/input"))'
  options:
    validation_mode: structure_only
- id: direct-redesign
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: redesign
            feedback: Change scope
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/design/"))[calls.filter(c,
      c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/design/")).size()-1].inputs.inputs.prompt.contains("Change
      scope")
  - type: cel_true
    expr: '!calls.exists(c, c.node_path.endsWith("/plan_feedback/input"))'
  options:
    validation_mode: structure_only
- id: repeat-feedback
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "First outcome"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "First outcome"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Add coverage
          artifact_refs: {}
          receipt: {}
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Second outcome"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Second outcome"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Handle empty input
          artifact_refs: {}
          receipt: {}
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Final outcome"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Final outcome"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: satisfied
          artifact_refs: {}
          receipt: {}
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: squashrebasemerge
      behavior:
        mode: return
        outputs:
          merged_hash: merged-hash
          target_branch: main
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).size()
      == 3
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/"))[1].inputs.inputs.prompt.contains("Add
      coverage")
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/"))[2].inputs.inputs.prompt.contains("Handle
      empty input")
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).size()
      >= 2
  - type: cel_true
    expr: '!has(calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c,
      c.node_path.contains("/implementation/"))[0].inputs.inputs.session)'
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).filter(c,
      has(c.inputs.inputs.session)).all(c, c.inputs.inputs.session.type == "c2ops.codex.session/v1")
  - type: cel_true
    expr: calls.filter(c,c.op == "input" && c.node_path.endsWith("/accept/input")).size() == 3
  - type: cel_true
    expr: calls.filter(c,c.op == "input" && c.node_path.endsWith("/accept/input"))[0].inputs.form.fields[0].question.contains("First
      outcome")
  - type: cel_true
    expr: calls.filter(c,c.op == "input" && c.node_path.endsWith("/accept/input"))[1].inputs.form.fields[0].question.contains("Second
      outcome")
  - type: cel_true
    expr: calls.filter(c,c.op == "input" && c.node_path.endsWith("/accept/input"))[2].inputs.form.fields[0].question.contains("Final
      outcome")
  - type: cel_true
    expr: 'calls.filter(c,c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c,c.node_path.contains("/implementation/")).filter(c,has(c.inputs.inputs.session)).all(c,c.inputs.inputs.session
      == {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7",
      "artifact": {"jobId": "implementation-session", "taskOrdinal": 1, "name": "__c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar",
      "sizeBytes": 100}})'
  options:
    validation_mode: structure_only
- id: redesign
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: redesign
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Change the requirements
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).size()
      >= 2
  - type: cel_true
    expr: '!has(calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c,
      c.node_path.contains("/implementation/"))[0].inputs.inputs.session)'
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).filter(c,
      has(c.inputs.inputs.session)).all(c, c.inputs.inputs.session.type == "c2ops.codex.session/v1")
  - type: cel_true
    expr: calls.filter(c, c.op == "input" && c.node_path.endsWith("/approve_plan/input")).size() == 2
  - type: cel_true
    expr: 'calls.filter(c,c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c,c.node_path.contains("/implementation/")).filter(c,has(c.inputs.inputs.session)).all(c,c.inputs.inputs.session
      == {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7",
      "artifact": {"jobId": "implementation-session", "taskOrdinal": 1, "name": "__c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar",
      "sizeBytes": 100}})'
  options:
    validation_mode: structure_only
- id: implementation-requests-redesign
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "redesign", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "redesign", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Review the external work
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "input" && c.node_path.endsWith("/approve_plan/input")).size() == 2
  options:
    validation_mode: structure_only
- id: human-rejects-plan
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Review the maintained test plan."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Review the maintained test plan."}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"ok": true}'
          stderr: ''
        artifacts:
          test-statements.md: '# Test statements'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: design-needs-input
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "ask_user", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "ask_user", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: design-review-rejects
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "revise", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "revise", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: test-review-rejects
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Review the maintained test plan."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Review the maintained test plan."}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"ok": true}'
          stderr: ''
        artifacts:
          test-statements.md: '# Test statements'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "revise", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "revise", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: test-contract-rejects
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Review the maintained test plan."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Review the maintained test plan."}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: implementation-incomplete
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: incomplete
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "ask_user", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "ask_user", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: specification-rejects
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "revise", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "revise", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: quality-rejects
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "revise", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "revise", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: verification-fails
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 7
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: continue-session
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "continue", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "continue", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[1].inputs.inputs.session.sha256 == "903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7"
  - type: cel_true
    expr: '!has(calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex"))[0].inputs.inputs.session)'
  options:
    validation_mode: structure_only
- id: outside
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "outside", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "outside", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: acknowledge
          artifact_refs: {}
          receipt: {}
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  options:
    validation_mode: structure_only
- id: invalid-human-input
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Review the maintained test plan."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Review the maintained test plan."}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"ok": true}'
          stderr: ''
        artifacts:
          test-statements.md: '# Test statements'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: invalid
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: approve
          artifact_refs: {}
          receipt: {}
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: invalid
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: ' '
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix this
          artifact_refs: {}
          receipt: {}
    - *id015
    - *id016
    - *id017
    - *id018
    - *id019
    - *id020
    - *id021
    - *id022
    - *id023
    - *id024
    - *id025
    - *id026
    - *id027
    - *id028
  assertions:
  - type: output_equals
    path: merged
    value: true
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).size()
      >= 2
  - type: cel_true
    expr: '!has(calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c,
      c.node_path.contains("/implementation/"))[0].inputs.inputs.session)'
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c, c.node_path.contains("/implementation/")).filter(c,
      has(c.inputs.inputs.session)).all(c, c.inputs.inputs.session.type == "c2ops.codex.session/v1")
  - type: cel_true
    expr: 'calls.filter(c,c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).filter(c,c.node_path.contains("/implementation/")).filter(c,has(c.inputs.inputs.session)).all(c,c.inputs.inputs.session
      == {"$c2j_object": "v1", "type": "c2ops.codex.session/v1", "tenant_id": "test", "sha256": "903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7",
      "artifact": {"jobId": "implementation-session", "taskOrdinal": 1, "name": "__c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar",
      "sizeBytes": 100}})'
  options:
    validation_mode: structure_only
- id: invalid-design-artifact
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: false
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
- id: invalid-missing-design
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
- id: invalid-review-artifact
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "The request fits this cell. Add the requested behavior."}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: false
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
- id: invalid-implementation-artifact
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: false
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
- id: missing-session
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: ''
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
- id: agent-error
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: error
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
- id: invalid-revision-artifact
  type: recipe_case
  inputs:
    prompt: Improve requested behavior
    type: build
  mocks:
    ops:
    - match:
        op: recipe_within_resolution
      behavior:
        mode: return
        outputs:
          resolved_selectors: {}
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
    - *id001
    - *id002
    - *id003
    - *id004
    - *id005
    - *id006
    - *id007
    - *id008
    - *id009
    - *id010
    - *id011
    - *id012
    - *id013
    - *id014
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "review", "summary": "Implemented behavior"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "done", "summary": "Ready"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: true
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{"next": "done", "summary": "Ready"}'
          stderr: ''
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: ran
          stderr: ''
          timed_out: false
        artifacts:
          build.log: Executed verification evidence
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: true
          exit_code: 0
          stdout: '{}'
          stderr: ''
        artifacts:
          verification.md: '# Verification'
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
          artifact_refs: {}
          receipt: {}
    - match:
        op: input
      behavior:
        mode: return
        outputs:
          fields:
            decision: revise
            feedback: Fix the reported issue
          artifact_refs: {}
          receipt: {}
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          status: completed
          sessionId: implementation-session
          session:
            $c2j_object: v1
            type: c2ops.codex.session/v1
            tenant_id: test
            sha256: 903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7
            artifact:
              jobId: implementation-session
              taskOrdinal: 1
              name: __c2j_objects__/903e460bdf836d6656c641caac0995fec12b4bdaf56771e2b64a2689b4ea41d7.tar
              sizeBytes: 100
        artifacts:
          result.json: '{"next": "review", "summary": "Implemented behavior"}'
          design.md: '# Design'
          implementation.md: '# Implementation'
    - match:
        op: extension_execution
      behavior:
        mode: return
        outputs:
          ok: false
    - match:
        op: command_execution
      behavior:
        mode: return
        outputs:
          success: false
          exit_code: 1
          stdout: '{}'
          stderr: Check failed
  assertions:
  - type: output_equals
    path: merged
    value: false
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).size() > 0
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !has(c.inputs.inputs.sandbox)
      && c.inputs.inputs.prompt.contains("Improve requested behavior"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, c.inputs.inputs.artifact_inbox_path.endsWith("/inbox")
      && c.inputs.inputs.artifact_outbox_path.endsWith("/outbox"))
  - type: cel_true
    expr: calls.filter(c, c.op == "extension_execution" && c.inputs.selector.endsWith("#codex")).all(c, !c.inputs.inputs.worktree_path.endsWith("/.c2j"))
  - type: cel_true
    expr: '!calls.exists(c, c.op == "squashrebasemerge")'
  options:
    validation_mode: structure_only
```

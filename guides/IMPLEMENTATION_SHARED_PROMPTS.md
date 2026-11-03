# Shared adaptive prompts

The active adaptive recipes now keep authored agent instructions, task wording,
classifier rubrics, child-job requests, and human-review wording in
[prompts.yaml](../recipes/adaptive/prompts.yaml). This follows the empty-sequence
include pattern: named outputs, no worker operation, no child job, and no prompt
artifact. It fits the recipes cell and requires no c2j or c2ops changes.

This covers the adaptive build path and its private helpers. Older recipe
families, creation implementation, and smoke examples are separate consumers and
have not been migrated in this change. Caller-supplied requests and hook guidance
remain inputs. Schemas, field IDs, option values, validation diagnostics, command
scripts, permissions, artifact bindings, and routing remain with their owners.

## Reading and editing text

The include has `sequence: []` and grouped outputs: `agent`, `turn`, `classify`,
`inspect`, `repair`, `consultation`, `children`, and `human`. These are immutable
text definitions, not workflow state. Consumers select the appropriate text from
the completed include; they do not carry a catalog through loop transitions.

For example, a sequence imports the text before consuming it:

```yaml
sequence:
- id: prompts
  include: ./prompts.yaml
  inputs:
    request: ${{ inputs.request }}
    target_directory: ${{ inputs.target_directory }}
    phase: ${{ inputs.assignment == '' ? inputs.phase : inputs.assignment }}
    guidance: ${{ inputs.guidance }}
- id: turn
  include: ./agent-turn.yaml
  inputs:
    instructions: ${{ sequence.prompts.outputs.agent.instructions }}
    prompt: ${{ sequence.prompts.outputs.agent.task }}
    # Existing schema, session, documents, and permission inputs remain here.
```

The consumer selects the assignment. `agent.task` contains the complete framing:

```text
Request: {{ inputs.request }}
Target directory: {{ inputs.target_directory }}

${{ inputs.phase == '' ? '' : vars.phases[inputs.phase] }}
Review the errors in the error directory when present, and address the feedback directory's current comments.
Read consultations/ and jobs/ when present for recorded agreements and outcomes. Do not duplicate recorded work.
{{ inputs.guidance }}
```

The include renders ordinary templates using its named inputs. Consumers pass
only the values they need; scalar defaults let static-text consumers omit inputs.
Request text containing percent signs or template-like expressions remains data.
There is no positional formatting convention or second template-evaluation pass.
Phase selection remains in the consumer; the include looks up the selected text.

The turn wrapper formats the artifact-directory footer at the actual operation:

```yaml
prompt: |-
  {{ inputs.prompt }}

  {{ states.prompts.outputs.turn.directories }}
  inbox: {{ context.environment.op.inbox }}
  outbox: {{ context.environment.op.outbox }}
  {{ states.prompts.outputs.turn.artifacts }}
```

Thus paths belong to the worker executing the operation, including a foreign
cell or resumed session. Standing instructions are still supplied only when
starting a session. Response correction still reads `error/`; normal tasks still
refer to directories rather than enumerating failure filenames.
Consultation turns also refer to inbox rather than listing exchanged filenames.

## Scope and source behavior

Sequence consumers use `sequence.prompts.outputs`. Direct operation states use
an initial `prompts` include state and read `states.prompts.outputs`; its
transitions retain the previous initial-state selection. Nested sequences import
the text locally, and consultation passes the two rendered strings explicitly
into its nested exchange. Root variables cannot alias an include that has not
executed.

Existing worker operation IDs, paths, and session selection remain unchanged.
The include does add empty sequence scopes to the workflow story. It satisfies
the requirement to avoid fake tasks, rather than a stronger zero-workflow-node
requirement.

`./prompts.yaml` resolves relative to its declaring recipe. Git recipe includes
use the same resolved source revision; local authoring uses the local files.
Existing resolved-source persistence captures the expanded recipe. This pattern
uses ordinary include resolution and does not introduce a descendant-only path
restriction or a new import feature.

## Initial extraction validation

The results below describe the initial extraction committed as `777a2b6`.
The subsequent [readability cleanup](IMPLEMENTATION_RECIPE_READABILITY.md)
replaces positional formatting with the named templates shown above and records
its own validation.

[Acceptance statements](../recipe-tests/adaptive/shared-prompts-statements.md)
were written before implementation. The native shared-prompts fixture retains
those statements and the rendered prompt and instructions as artifacts. It
checks that importing and rendering text results in exactly one operation—the
fixture's consumer—and tests literal template-like request text and runtime
directory binding.

Validation on 2026-11-03 used c2j main commit
`f1a153b898c57e93e9b01477d08cc02c1509ee4b`:

- All 24 adaptive suites validated. The complete isolated regression passed
  **149 cases** across those suites.
- Against recipe commit `23d376c`, all 147 existing cases retained their worker
  call counts and paths: 1,247 observed operations. All 1,047 compared prompt,
  instruction, schema, child-request, and human-form fields matched after
  normalizing runtime paths/IDs and concurrent child ordering.
- The two new native prompt cases passed directly against the source recipes.
  Three native human-review cases also passed against source recipes.
- Editing only the prompt include in a separate local fixture changed the
  consumer's rendered text in both native cases, still with one worker call.
- `git diff --check` passed.

The isolated regression uses fixture model responses and replaces published Nix
selectors with their extension primitive in a temporary copy. Native commands
execute normally with installed tools. It validates recipe orchestration, not
live model behavior or published package resolution. The unmodified source run
still encountered the host's Nix `tmpbin/git: File exists` failure. The usual
`submit --run --embed` check still stopped before submission because the shared
JobDB requires its chapter-artifact migration; the shared database was not
modified.

Local evidence: `/tmp/shared-isolated-regression`,
`/tmp/shared-input-comparison.json`, `/tmp/shared-native-prompts`,
`/tmp/shared-native-review`, `/tmp/shared-native-review-self`,
`/tmp/shared-edited-native`, and `/tmp/shared-embedded-submit.log`.

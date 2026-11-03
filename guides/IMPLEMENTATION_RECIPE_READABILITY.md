# Recipe readability cleanup

This work fits the recipes cell. It addresses the remaining serialized fixture
envelopes, positional prompt formatting, and opaque annotation expressions in
the active adaptive path.

## What was unnecessary

`data_json` was an inbox test fixture input, not an agent prompt or production
workflow context. It serialized documents, feedback, errors, and many empty
defaults into one string. The inbox fixture now accepts named artifact maps and
feedback text; each case supplies only relevant values. The agent and coordination
fixtures also stop accepting a general `arguments_json` envelope. Unused values
such as synthetic hook settings, iteration counts, and approval state are gone.

The prompt extraction used Go-template `printf` to fill `%s` positions. That was
an authoring choice, not a c2j requirement. Shared prompts now render normal
templates with named inputs. Consumers read a completed string, for example:

```yaml
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
    prompt: ${{ sequence.prompts.outputs.agent.task }}
    # Other existing turn inputs follow.
```

The artifact directory lines render at the actual worker operation because that
operation owns the paths. Shared prose still lives in `prompts.yaml`. Includes
remain empty sequences and add no worker operations.

Consultation prompts now say “Read the inbox for exchanged documents.” The
parallel `latest_files` bookkeeping and filename list are removed. Actual
artifact bindings and the recorded conversation retain the exchanged documents.

## What the annotations do

Annotations supply human-review titles, descriptions, priority, and links to
supporting documents. Their artifact references identify the content those
descriptions concern. A filename alone is insufficient: another turn can replace
that file, or a parent can give a child's file a new inbox name.

The cleanup removes JSON serialize/parse round trips around artifact references,
filters returned file descriptors once, and stops copying the entire available
document inventory into every annotation. The final annotation contains only its
own reference, descriptor, and resolved or unresolved sources.

`document-bindings.yaml` names the two operations explicitly: rename the visible
attachment, and rename matching annotation IDs. `review.yaml` declares the form
as normal YAML. Its remaining jq functions validate descriptors, match current
artifact identity, exclude stale/self source links, and apply required review
priorities. The previous compressed queries are expanded and commented at those
steps. jq still handles map transformations; replacing those with equally opaque
CEL expressions would not simplify the contract.

## Actual c2j constraints

The inspected c2j implementation at
`f1a153b898c57e93e9b01477d08cc02c1509ee4b` accepts public recipe input types
`string`, `number`, `boolean`, `object`, `artifact`, and `artifact_map`.
Here `object` means a session/object checkpoint, not an ordinary JSON object;
`any`, plain maps, and arrays are unsupported by recipe input validation.

That leaves narrow JSON strings at public job/test boundaries for values such as
consultation request lists, annotations, and saved coordinator threads/jobs. They
are decoded at the boundary and passed as ordinary values internally. Removing
that transport convention completely requires c2j to support ordinary structured
inputs; it does not require a replacement workflow context object in recipes.

Some empty values are meaningful: an artifact-map default means no files, an
absent session means start a session, and the native test runner requires
`runtime: {}` to opt into runtime fixtures. These differ from repeating every
empty workflow field in every test case or prompt.

## Validation

[Acceptance statements](../recipe-tests/adaptive/readability-statements.md) were
defined before implementation and are retained by the native prompt fixture.
Existing checks retain assignment, session, artifact, approval, and verification
expectations. The consultation assertion that required a filename in prompt text
is replaced under the user's directory-handoff instruction; the checks that the
files actually reach the next agent remain.

Validation on 2026-11-03:

- All 25 suites validated. All **151 distinct cases passed**, combining the full
  regression with the corrected consultation-suite rerun. The only failure in
  the first run was the obsolete filename-in-prompt assertion. The nine
  coordination-gate cases also passed after omitting their redundant defaults.
- Sixteen native source cases passed across inbox bindings, shared templates,
  annotation identity, and human review. The shared-template fixture still
  records exactly one worker operation and retains both acceptance documents.
- Against the prior extraction, 1,249 existing worker calls retained their
  counts and paths. Of 1,047 compared prompt/schema/form fields, the only
  differences were 21 consultation prompts receiving the intended inbox wording
  and losing filename inventories. Standing instructions, schemas, and review
  metadata matched.
- `git diff --check` passed. No `data_json`, `arguments_json`, positional prompt
  formatting, or `latest_files` references remain in the adaptive recipes and
  their fixtures.

The complete regression uses the existing isolated copy with fixture model
responses and installed tools for native commands. It does not establish live
model or published Nix-package behavior; the existing shared-JobDB and package
resolution restrictions still limit that end-to-end check.

Local evidence: `/tmp/readable-regression`,
`/tmp/readable-consultation-final`, `/tmp/readable-regression-results.json`,
`/tmp/readable-input-comparison.json`, `/tmp/readable-native-prompts-final`,
`/tmp/readable-native-inbox-final`, `/tmp/readable-native-identity-final`,
`/tmp/readable-review`, `/tmp/readable-review-self`, and
`/tmp/readable-coordination-gates-final`.

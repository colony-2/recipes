# Native structured recipe inputs

The active build, creation, and adaptive consultation entrypoints now declare
`schema_version: 2`. They accept annotations as an array instead of an
`annotations_json` string. Session declarations use `type: checkpoint` and retain
`object_type: c2ops.codex.session/v1`. Recipe release versions are unchanged.

This uses c2j main commit `2537a3c` (schema v2 support). The installed system binary
was older; validation used a locally built binary from that commit.

## Contract and handoff

An annotation has a required string `id` and an `artifact`-typed `ref`. Optional
`descriptor` is an ordinary object; optional `sources` is an array of objects
whose `ref`, when supplied, is also artifact-typed. Other metadata remains
allowed, including lineage and unresolved-source descriptions. Missing annotations
default to `[]`; descriptors and source lists are not invented when absent.

Callers can use ordinary YAML and whole-value expressions:

```yaml
inputs:
  prompt: Implement the agreed design.
  documents: ${{ inputs.documents }}
  annotations:
  - id: design.md
    ref: ${{ inputs.documents['design.md'] }}
    descriptor:
      title: Agreed design
      description: Scope and acceptance criteria.
```

When annotations already exist, forward `annotations: ${{ inputs.annotations }}`.
The coordinator now uses normal YAML mappings for child submissions, passes
annotations alongside documents, and no longer creates `__review_annotations__`
sidecars. The active entrypoints no longer scan documents for annotation transport.
Agent prompts continue to describe tasks and inbox directories; structured inputs
are recipe data, not another context blob in a prompt.

Adaptive fixture inputs also use native `requests`, `keys`, `annotations`,
`threads`, `jobs`, `dependencies`, and `failure` values. Their `_json` wrappers and
boundary parsing are removed. Negative rebase cases still accept deliberately
malformed diagnostic contents so the policy can reject them.

## Scope and compatibility

Root build/create, adaptive consultation, cell initialization, and adaptive
fixtures with declared input contracts use v2. Private helpers without input
schemas remain unversioned: they already pass native values, and declaring v2
would require complete input contracts at every include boundary. Mixed-version
includes are supported by c2j. Older build families and their kernel consultation
contract remain unchanged.

Callers of the migrated entrypoints must pass `annotations` directly. Custom child
recipes used with the adaptive coordinator must accept that input. Historical
jobs retain their captured recipe sources; this migration does not rewrite them.
Model response JSON Schemas still use `object`; those are not recipe input types.
Remaining JSON parsing handles model/hook formats and runtime diagnostic values,
not serialized structured recipe inputs.

## Validation

[Acceptance statements](../recipe-tests/adaptive/schema-v2-statements.md) are
retained as artifacts by the shared-prompt fixture.

Validated on 2026-11-03 with c2j `2537a3c`:

- All 25 adaptive suites validated. All **155 distinct adaptive cases passed**:
  152 in the full regression, plus three new native negative-input cases. Tests
  cover annotation delivery through real child jobs, checkpoint reuse, document
  identity, defaults, verification, recovery, and human review.
- Native source checks reject incorrect annotation IDs, artifact references, and
  JSON strings at all three public entrypoints, with nested field diagnostics.
  The three build rejections are retained in the flow suite.
- The native shared-prompt suite passed both cases and retained the acceptance
  document without adding worker tasks.
- Creation passed 19 of 21 cases, plus its separate checkpoint/creation handoff
  case. The two failures also reproduce against the unchanged pre-migration
  entrypoint: they expect an empty clarification document list, but the existing
  review helper adds a review brief and provenance. Their assertions are unchanged.
- Model response schemas are unchanged; `git diff --check` passed.

The full regression uses an isolated copy with fixture model responses and
installed tools for native commands. It expands Nix selectors to their runtime
operation and bypasses Nix package setup because Nix is unavailable here. This
checks recipe behavior, not live model execution or published package resolution.

Local evidence: `/tmp/v2-adaptive-all`, `/tmp/v2-native-invalid`,
`/tmp/v2-native-prompts-final`, `/tmp/v2-boundary-validation`,
`/tmp/v2-create-complete`, `/tmp/v2-create-handoff-complete`, and
`/tmp/v2-create-baseline-results`.

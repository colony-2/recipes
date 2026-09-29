# Nested CEL values lose content during JSON serialization

Owner: c2j template functions. Observed with the workspace-capable local build `v0.0.54-0.20260929012541-9f9d9d0cfa78+dirty`
(reproduced on 2026-09-29 in both the live dialogue and an isolated c2j test).

## Reproduction

Use this command node in a recipe, with a disposable JobDB:

```yaml
sequence:
  - id: reproduce
    op: command_execution
    inputs:
      env:
        PAYLOAD: '${{ json_stringify({"nested": json_parse("{}")}) }}'
      run: 'printf "%s\n" "$PAYLOAD"'
outputs:
  result: '${{ sequence.reproduce.outputs.stdout }}'
```

Expected: `{"nested":{}}`.
Actual in the live design context: nested objects become `{"Adapter":{}}`.
The design context expression combined `json_parse(inputs.context_json)`,
`states.mandate.outputs.mandate`, and a parsed consultation ledger in a map
literal. All three lost their data:

```json
{"previous":{"Adapter":{}},"mandate":{"Adapter":{}},"consultations":{"Adapter":{}}}
```

The same-job design test caught this on the first A turn: an empty consultation
ledger appeared nonempty, and the mandate's identity/clauses were unavailable.

## Requested fix

Recursively convert CEL map/list values to JSON-native values before marshaling
in `json_stringify`, including nested parsed JSON and state outputs. Cover empty
and populated objects, nested lists/maps, nulls, and state-output compositions.
Review other functions using `normalizeJQInput` for the same conversion issue.

## Recipe workaround

The design and parent workflows concatenate individually serialized JSON values
into fixed-key envelopes. Keys and punctuation are recipe constants; each
nonconstant value is already JSON, so quotes and newlines remain escaped. No
runtime source changes are needed in the recipes cell. The real consultation
integration test verifies that the mandate and full dialogue survive transport.

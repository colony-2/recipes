# Jev API key rejects c2j secret references

Status: **Resolved** in published c2ops
**5645070ebe0a9ca94ab605441954a80d87cfedf1**, verified on 2026-10-27
with c2j **0.0.106**. The published Nix manifest now declares `x-secret: true`.
All 13 classifier integration cases pass with the checked-in published selector,
including the assertion that `api_key` remains a `jev_api_key` secret reference.

Owner: **c2ops**, Jev operation manifest. Recipe routing belongs to this cell;
the operation's credential schema belongs to c2ops.

Observed with c2j **0.0.105** and c2ops `main`/`published`
**a9139f48fd4866d444a3d4f61e840d3bb82feec6** on 2026-10-27.

The build classifier passes:

```yaml
op: nix:github:colony-2/c2ops/published#jev
inputs:
  api_key: ${{ context.secrets.jev_api_key }}
  state: {request: Correct a documentation typo.}
  questions:
    is_heavy:
      type: noul
      instructions: Does this request require a heavy development process?
```

Before the operation executes, c2j reports:

```text
failed to validate selector inputs: input api_key: secret reference requires x-secret: true
```

The field was a plain string in both `jev/op.yaml` and the published `jev/op.json`.
The fix adds the annotation to both manifests:

```yaml
api_key:
  type: string
  x-secret: true
```

No permission block, URL reference, or plaintext credential workaround is needed.
Before publication, classification conservatively selected heavy and exposed the
error in `classification.assessment.error`; integration tests requiring a Jev
fixture failed because schema validation rejected the reference first.

Verification now runs unchanged recipes against
`nix:github:colony-2/c2ops/published#jev`, without the earlier local manifest patch
or Git-selector override. Model responses are fixtures; c2j validates the actual
published manifest and preserves the secret reference. These tests do not call
the live Jev service.

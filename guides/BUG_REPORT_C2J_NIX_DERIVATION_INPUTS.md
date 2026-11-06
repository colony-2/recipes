# Native tool setup rejects Nix 2.20 derivation inputs

Owner: c2j. Observed with `eb636a5` (npm `0.0.120` source), Nix `2.20.6`,
and an authored native recipe test declaring a pinned Nix Python package.
The operation fails during tool setup, before its command or model fixture runs:

```text
json: cannot unmarshal object into Go struct field nativeDerivation.inputDrvs
... of type []string
```

`nix derivation show` from Nix 2.20.6 produces a map keyed by full derivation
paths, without a document-level version. Its `inputDrvs` values have this shape:

```json
{"/nix/store/example.drv": {"dynamicOutputs": {}, "outputs": ["out"]}}
```

`pkg/toolenv/native.go` decodes `inputDrvs` as `map[string][]string`. It also
supports version-4 documents with `inputs.drvs`, but misses this intermediate
format. Its tests cover the array and version-4 forms, not the object-valued
`inputDrvs` form produced by this real Nix version.

Reproduce with Nix 2.20.6 and c2j from this commit:

```sh
c2j test run --file recipe-tests/adaptive/classify.test.yaml --case missing-context
```

The failure occurs in `classify/read_repository_context`, which declares
`nix:github:NixOS/nixpkgs/e7439b6b14ad3cc35d05608ebca9bce01a25f5f8#python3`.
Directly inspecting a realized derivation with both Nix versions confirms the
different JSON shapes. Nix 2.34.8 emits version 4 and this case passes unchanged.

Please either support object-valued `inputDrvs` (retaining rejection of nonempty
dynamic outputs) with captured real-output fixtures, or enforce a documented Nix
minimum before recipe execution with an actionable version error. No recipe
should remove its tool declarations to get around this failure.

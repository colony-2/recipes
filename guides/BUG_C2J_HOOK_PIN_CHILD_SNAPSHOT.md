# c2j: a clean hook pin cannot be inherited by a consultation child

Observed with c2j source `85f9c9011a9d` while implementing local build hooks.
Runtime correction belongs to c2j; this repository owns the regression scenario.

## Affected test and temporary skip

- Test ID: `heavy-accepts-successful-unmerged-child`.
- Suite: [`recipe-tests/build-dependency-disposition.disabled.yaml`](../recipe-tests/build-dependency-disposition.disabled.yaml).
- Owner of the runtime fix: c2j.
- Status: open; excluded from automatic suite discovery at the user's request.

The runner has no per-case skip field. The single-case suite was renamed from
`build-dependency-disposition.test.yaml` to `build-dependency-disposition.disabled.yaml`.
Directory discovery selects `*.test.yaml`, so it omits this file. The fixture and
assertions remain intact; this is not an expected-error test or a passing substitute.

## Reproduction

Use a hook-capable c2j build, then run from the recipes repository:

```sh
c2j test run \
  --file recipe-tests/build-dependency-disposition.disabled.yaml \
  --case heavy-accepts-successful-unmerged-child \
  --out-dir /tmp/hook-pin-child-reproduction --case-timeout 5m
```

The disabled filename still supports explicit single-file execution.

The startup configure hook is absent. c2j correctly pins the consuming candidate.
The design then launches a custom consultation recipe as a child in the same
repository at that exact candidate. No implementation changes have occurred.

Expected: the child inherits the exact clean candidate, completes its consultation,
and allows the parent to accept the successful unmerged prerequisite. A clean
commit already fetchable from the source repository needs no additional snapshot.

Actual: child submission fails before consultation or implementation with:

```text
inherited workspace commit requires its snapshot artifact
```

Failing node:

```text
build/run/heavy/heavy/develop/coordinate/sequence/coordinate/build-coordinate/launch_serving_consultation/launch_serving_consultation
```

## Cause

`pkg/ops/recipe/workspace.go:inheritWorkspace` requires `RestoreArtifact` whenever
`start.GitRef == g.PersistHash`. Hook resolution records a persist hash even for a
clean, fetchable commit, without creating a thin-pack artifact. Those are compatible
states individually, but the inheritance check treats the missing artifact as an
error even when the commit is available from the source repository.

## Required correction

Allow inheritance of an exact, fetchable pinned commit without requiring an
unnecessary snapshot. Keep requiring the recorded snapshot for synthetic/unpushed
commits, and retain parent/base identity and consuming-workspace authority.

Test both absence and presence of a read-only hook, then child submission before
any local mutation. Also test an unpushed candidate, a lost required snapshot, and
an advancing source branch. Never silently fall back to the branch tip.

The recipes must not manufacture empty commits or change child submissions to
floating refs to work around this issue.

## Re-enable after the fix

Run the explicit reproduction against the corrected c2j version and require the
original assertions to pass. Then restore discovery:

```sh
git mv recipe-tests/build-dependency-disposition.disabled.yaml \
  recipe-tests/build-dependency-disposition.test.yaml
```

Remove the temporary-skip comments and entry in `recipe-tests/SKIPPED.md`, update
this report with the fixed c2j version, and run normal directory discovery. Keep
the original success assertions; do not replace them with an expected failure.

## Separate local test prerequisite

The same c2j source's `pkg/toolenv/native.go:decodeNativeDerivation` accepts legacy
`inputDrvs` arrays and version-4 `inputs.drvs` objects, but rejects Nix 2.20/2.31's
unversioned `inputDrvs` objects containing `outputs` and `dynamicOutputs`.
This prevents provisioning the existing Python dependency before recipe execution.

Local testing used real Nix 2.31.5 with a temporary adapter that converts static
`inputDrvs` objects to equivalent legacy output arrays. It rejects dynamic outputs
and does not mock dependencies or recipe operations. No adapter or c2j source
changes are included in the implementation. c2j should accept this documented Nix
representation directly. Local portable Nix also required rollback journal mode
instead of WAL; that is an environment-specific setup constraint.

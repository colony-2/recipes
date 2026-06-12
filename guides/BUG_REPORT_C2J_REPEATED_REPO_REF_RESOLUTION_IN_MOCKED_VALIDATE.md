# Bug Report: `c2j test validate` Repeatedly Resolves Same repo@ref For Mocked Extension Op

## Summary

`c2j test validate` repeatedly runs remote ref resolution for the same
git-backed extension op selector during one mocked recipe case.

A self-contained one-op mocked validation case performs three separate:

```text
git ls-remote https://github.com/colony-2/c2ops.git ... main
```

calls even though the recipe contains only one git-backed selector:

```text
git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
```

The op is fully mocked. The run does not execute Codex, does not clone the
c2ops repository, and does not run `index-pack`. Almost all wall time is spent
in repeated remote ref checks.

This report is self-contained. It does not require access to the C2 recipes
repository, local `/src` files, Superpowers recipes, or any other project
assets.

## Version

Observed with:

```text
c2j version v0.0.35-0.20260612001443-2513cc557532
/usr/local/bin/c2j sha256 f3e219856d02fedfb34b6660d4c480128fa910926f5d39b6b538729324963b86
```

## Reproduction

Run this script in any environment with `c2j`, `strace`, `rg`, and network
access to GitHub:

```bash
set -euo pipefail

WORK_DIR="$(mktemp -d /tmp/c2j-reporef-repro.XXXXXX)"

cat > "$WORK_DIR/recipe.yaml" <<'YAML'
id: reporef-resolution-repro
version: 0.1.0
sequence:
  - id: run_skill
    op: git+https://github.com/colony-2/c2ops.git//codex/run_skill@main
    inputs:
      skill: repro-skill
      prompt: "Return mocked output."
      status_contract:
        path: repro/status.json
      output:
        from: artifact
        path: repro/result.json
        format: json
        schema:
          type: object
          required: [summary]
          properties:
            summary:
              type: string
outputs:
  status: "{{ sequence.run_skill.outputs.status }}"
  summary: "${{ sequence.run_skill.outputs.parsed_output.summary }}"
YAML

cat > "$WORK_DIR/scenario.md" <<'YAML'
# repo ref resolution repro

```yaml
cases:
  - id: mocked-run-skill
    type: recipe_case
    mocks:
      ops:
        - match:
            op: recipe_within_resolution
          behavior:
            mode: return
            outputs:
              resolved_selectors: {}
        - match:
            node_path: "reporef-resolution-repro/run_skill/git+https://github.com/colony-2/c2ops.git//codex/run_skill@main"
          behavior:
            mode: return
            outputs: &run_skill_output
              status: completed
              sessionId: sid-repro
              assistantSummary: Repro mocked output.
              incompleteReason: ""
              incompleteCategory: ""
              pendingDependencies: []
              skills_installed: []
              skill: repro-skill
              raw_summary: Repro mocked output.
              output_source: artifact
              output_path: repro/result.json
              raw_output: '{"summary":"mocked"}'
              parsed_output:
                summary: mocked
              output_schema_valid: true
              output_schema_errors: []
              output_repair_attempts: 0
              status_contract_path: repro/status.json
              status_contract_present: true
              status_contract_valid: true
              status_contract_json:
                status: completed
              status_contract_errors: []
              diagnostics: {}
        - match:
            op: extension_execution
          behavior:
            mode: return
            outputs: *run_skill_output
    assertions:
      - type: output_equals
        path: status
        value: completed
      - type: output_equals
        path: summary
        value: mocked
```
YAML

TRACE_DIR="$WORK_DIR/trace"
mkdir -p "$TRACE_DIR"

strace -ff -tt -T -e trace=process -s 256 \
  -o "$TRACE_DIR/trace" \
  c2j test validate \
    --recipe-file "$WORK_DIR/recipe.yaml" \
    --file "$WORK_DIR/scenario.md" \
    --parallelism 1 \
    --json

printf 'work_dir=%s\n' "$WORK_DIR"

printf 'git ls-remote execs: '
rg 'execve\("/usr/bin/git", \["git", "ls-remote"' "$TRACE_DIR" | wc -l

printf 'git clone execs: '
(rg 'execve\("/usr/bin/git", \["git", "clone"' "$TRACE_DIR" || true) | wc -l

printf 'git index-pack execs: '
(rg 'index-pack' "$TRACE_DIR" || true) | wc -l

printf 'codex execs: '
(rg '/usr/local/bin/codex|vendor/.*/codex/codex|execve\("codex"' "$TRACE_DIR" || true) | wc -l
```

## Observed Result

The mocked case validates successfully:

```text
mocked-run-skill valid (3007ms)
{"cases":1,"invalid_or_error":0,...}
```

The process trace shows:

```text
git ls-remote execs: 3
git clone execs: 0
git index-pack execs: 0
codex execs: 0
```

In the observed run, the three `git ls-remote` calls accounted for almost all
wall time:

```text
c2j wall time:          about 3.7s
git ls-remote calls:    3
git ls-remote sum:      about 3.6s
```

Representative trace entries:

```text
execve("/usr/bin/git", ["git", "ls-remote", "https://github.com/colony-2/c2ops.git", "refs/heads/main", "refs/tags/main", "refs/tags/main^{}", "main"], ...)
execve("/usr/lib/git-core/git-remote-https", ["/usr/lib/git-core/git-remote-https", "https://github.com/colony-2/c2ops.git", "https://github.com/colony-2/c2ops.git"], ...)
```

## Expected Result

Within one recipe/test-case resolution snapshot, the normalized repo/ref:

```text
https://github.com/colony-2/c2ops.git@main
```

should be resolved at most once. The repository-relative op path
`codex/run_skill` should then use that pinned resolved commit.

For a fully mocked selector-backed op:

- the mocked op result should be returned without runtime re-resolution of the
  same floating ref;
- semantic validation should read any required manifest from the already
  resolved snapshot or from a cache entry keyed by the resolved commit;
- missing mock fields should produce test diagnostics, not trigger additional
  remote ref checks.

If `c2j test validate` intentionally has multiple internal phases that each need
the same selector metadata, those phases should share the selected repo/ref
resolution or consume a pinned selector from the first phase. They should not
each call `git ls-remote` for the same repo/ref.

## Larger Profiling Evidence

A larger mocked validation case in the C2 recipe suite showed the same behavior
at scale. This is supporting evidence only; the reproduction above is the
self-contained case.

Profiled command:

```bash
strace -f -ttt -T -e trace=process -s 512 \
  -o /tmp/c2j-profile-ts080/process.trace \
  c2j test validate \
    --recipe-file /src/superpowers.yaml \
    --file /src/recipe-tests/superpowers.scenario.md \
    --case ts-080-superpowers-orchestrates-same-job-happy-path \
    --parallelism 1 \
    --json
```

Parsed process lifetimes:

```text
c2j total wall:             139.336s
git ls-remote top-level:    134 calls, 137.539s total, 1.026s avg
git remote-https wrapper:   134 calls, 134.769s total
git-remote-https binary:    134 calls, 132.972s total
git clone:                  0
git index-pack:             0
Codex exec:                 0
```

The `git remote-https` and `git-remote-https` processes are nested under
`git ls-remote`; they are not additional wall time to add on top of the
top-level `git ls-remote` total.

## Impact

Mocked recipe validation remains network-bound even after repository
materialization caching. Full c2ops clones and pack processing are gone, but
repeated floating-ref checks still dominate runtime.

This prevents production recipes with many selector-backed extension op nodes
from being validated quickly, even when all selector-backed ops are mocked and
no Codex process is invoked.

## Related Requirement

This violates the intended single repo/ref snapshot behavior documented in:

```text
guides/REQUIREMENTS_SINGLE_REPO_REF_RESOLUTION.md
```

The relevant expectation is that every git-backed recipe selector, inline
include, child recipe selector, and extension op selector using the same
normalized `repo@ref` in one recipe resolution snapshot uses the same resolved
commit.

## Suspected Area

The trace suggests selector materialization caching is working, because there
are no `git clone` or `index-pack` calls. The repeated work appears to be in
floating-ref resolution for selector-backed extension ops during
`c2j test validate`, including mocked execution paths.

Likely places to inspect:

- test validation's selector resolution phases;
- extension-op manifest resolution during mocked cases;
- validate-mode extension execution or zero-output handling;
- runtime fallback paths that re-resolve a selector instead of consuming the
  recipe snapshot's resolved selector metadata.

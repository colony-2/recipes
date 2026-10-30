# Build hook validation

The implementation replaces implicit `build.sh` discovery with five local hooks:
configure, before_design, prepare, verify, and publish. Startup settings carry phase
prompt additions, named values, and specialist requests. Required specialists must
explicitly pass; each checkpoint visit starts a fresh consultation. Publish is an
ordinary post-merge include, using the merged commit and normal c2j failure handling.

## Runtime used

Validation used c2j built from local source `85f9c9011a9d` (reported version
`v0.0.108-0.20261030001705-85f9c9011a9d+dirty`). The installed v0.0.105 release
predates local recipe hooks. No c2j source was changed for this implementation.

The environment used real Nix packages and a temporary adapter for c2j's Nix
JSON decoder, described in [the runtime issue report](BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md).
This adapter is not part of the recipes. Native Git, artifact, hook, permission,
review, and child-job execution ran in temporary fixture repositories. Agent and
classifier responses were mocked. No live publication or external deployment ran.

## Commands

Using the hook-capable executable and the environment setup described above:

```sh
c2j test run --directory recipe-tests --out-dir /tmp/build-hooks-all \
  --parallelism 4 --case-timeout 5m
c2j test run --file recipe-tests/build-hooks-flow.test.yaml \
  --out-dir /tmp/build-hooks-flow-final --parallelism 3 --case-timeout 5m
c2j test run --file recipe-tests/build-hook-identity.test.yaml \
  --out-dir /tmp/build-hook-identity2 --parallelism 3 --case-timeout 5m
c2j submit 'Validate build hook wrappers' \
  --advanced-recipe-file recipe-tests/fixtures/build-hooks.yaml \
  --artifact build-hooks.test-statements.md=recipe-tests/build-hooks.test-statements.md \
  --cell /src --run --embed
bash build.sh
git diff --check
```

The initial directory run exposed recipe and fixture issues. After corrections,
affected suites and cases were rerun individually; results below combine each
case's latest execution rather than claiming one uninterrupted green directory run.

Embedded smoke job `3LOOfSLnqLLoayFvqXrsPL6KHYF` completed successfully with the
initial test statements attached. It used an isolated embedded JobDB, preserving
the pre-existing local database. It exercised absent hooks against a clean pinned
candidate; present hooks and unpushed candidates are covered by integration fixtures.

## Results

Across the full discovery run and targeted reruns, **269 of 270 unique cases pass**.
The remaining failure is the c2j limitation below. All 23 upstream merge-chase
cases pass, including repeated advancement, changed differences requiring fresh
approval, verification repair, conflicts, and escalation.

All 35 focused hook cases pass:

| Suite | Passing cases |
| --- | ---: |
| Configuration, research, preparation, and late resolution | 7 |
| Integrated light/heavy flows and configured security reviews | 3 |
| Specialist assessment gates and fresh checkpoint sessions | 4 |
| Verification, absence, required checks, malformed outputs, mutation, errors, and timeout | 13 |
| Publication, absence, failure, mutation, and branch advancement after merge | 5 |
| Hook-source identity and relative includes | 3 |

The integrated hook suite also passes `c2j test validate`. Repository structural
checks (`bash build.sh`), YAML parsing (including valid inline hook fixtures), and
`git diff --check` pass. Source inspection uses pinned Python and `yq-go` packages.
Example GitHub Actions verification is provided but was not executed against a
live workflow.

The runtime upgrade required JSON normalization of native artifact references at
artifact namespace and repair boundaries. The consultation scheduling fixture also
normalizes numeric inputs; all nine scheduling cases pass, including the existing
40-inline/41-child-jobs threshold.

## Remaining runtime limitation

`heavy-accepts-successful-unmerged-child` in
`recipe-tests/build-dependency-disposition.disabled.yaml` exposes a c2j defect: startup
hook resolution pins a clean commit, then custom consultation child submission
requires a snapshot artifact even though that commit is fetchable. The fix belongs
to c2j. See [the reproduction and required correction](BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md).
The recipe retains exact candidate inheritance rather than substituting a floating
branch or manufacturing a commit.

The user authorized temporarily excluding this case after validation. Its suite
now uses `.disabled.yaml`, preserving explicit execution while excluding automatic
discovery. The 269 passing cases remain enabled; the excluded case is recorded in
[the skip register](../recipe-tests/SKIPPED.md).

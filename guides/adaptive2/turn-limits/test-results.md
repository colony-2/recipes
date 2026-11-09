# Turn-limit and handoff validation

Runtime: c2j `0.0.124`, pinned by `.c2j-version`, with the normal packaged c2ops
operations. Tests use disposable registered cell repositories and embedded jobs.
Codex decisions and human answers are scripted. Artifact binding, input receipts,
inline consultation, child execution, Git operations, and recipe transitions run
through c2j.

## Commands

```sh
c2j test run --directory recipe-tests/adaptive2 --case-timeout 3m \
  --out-dir /tmp/turn-fix-a2-final
c2j test run --directory recipe-tests/self-improvement --parallelism 2 \
  --case-timeout 3m --out-dir /tmp/turn-fix-hooks
c2j test run --file recipe-tests/adaptive/recovery-progress.test.yaml \
  --parallelism 2 --case-timeout 3m --out-dir /tmp/turn-fix-shared
c2j test run --file recipe-tests/adaptive/recovery.test.yaml \
  --out-dir /tmp/turn-fix-failure-codes
```

In this workspace these commands use `/tmp/operational-c2j`, which runs the pinned
binary and Nix store. The default installed c2j is older.

## Results

**57 unique native cases pass** after the fixes and focused reruns:

| Coverage | Passed |
| --- | ---: |
| Adaptive2 public build, consultation, budgets, handoffs, correction diagnostics, and native merge races | 48 |
| Existing local build hooks | 4 |
| Previous adaptive workflow recovery regressions | 3 |
| Shared failure-code compatibility | 2 |
| **Total** | **57** |

The directory run passed 41 cases and found four incorrect review paths in the
new merge test fixtures. After correcting those paths, all four merge cases
passed. A focused consultation rerun passed all four cases, including the newly
added nesting-limit diagnostic. Both new response-repair diagnostic cases passed.
These focused results supersede the earlier fixture failures; no failing case is
excluded from the totals above.

```sh
c2j test run --file recipe-tests/adaptive2/merge-turns.test.yaml \
  --case-timeout 3m --out-dir /tmp/turn-fix-merge
c2j test run --file recipe-tests/adaptive2/consultation-turns.test.yaml \
  --parallelism 2 --case-timeout 3m --out-dir /tmp/turn-fix-consult-final
c2j test run --file recipe-tests/adaptive2/response-repair.test.yaml \
  --out-dir /tmp/turn-fix-repair-codes
```

Each output directory retains per-case `result.json` evidence and suite summaries.
The report counts unique cases rather than repeated executions. `git diff --check`
also passes. Repeated mock definitions were folded into YAML aliases only after
checking that the parsed test data remained identical. After the final formatting
cleanup, the public build's `approved-direction-continues-with-fresh-implementation`
case passed again (`/tmp/turn-fix-final-smoke`). All adaptive2 recipe and test YAML
files also parsed successfully.

## Scope

The public-build regressions cover unchanged and changed handoff copies, recovery
without republishing, precise exhausted-correction errors, repeated human reviews,
new and reused package decisions, consultation receipts, bounded autonomous work,
operational correction, and merge chasing. Focused consultation tests also cover
nested human direction and bounded agent-only exchanges. Existing public build,
child routing, verification, publication, and hook tests are included.

An initial run used the test harness's default 60-second per-case timeout while
multiple suites ran concurrently. Longer review scenarios timed out; the normal
command above allows three minutes per case. Early fixture failures also exposed
missing correction-map restoration and incorrect assumptions about the child's
wait path; the final regressions exercise those paths explicitly.

No production jobs were answered, restarted, or submitted. These tests do not
claim that an uncapped human conversation bypasses runtime time/resource budgets,
or that scripted model responses establish live document quality.

# Native Git refresh fails after a same-cell child build

Date: 2026-10-16 UTC
Status: Fixed in c2j `ee1420b12dee`; verified on 2026-10-16. No recipe-level refresh workaround.
Owner: c2j — Git operations, workspace preparation, and recipe execution context.
Reporting cell: recipes.

## Resolution

Installed from GitHub with `go install github.com/colony-2/c2j/cmd/c2j@main` and
verified using `/home/shai/go/bin/c2j`, version
`v0.0.78-0.20261016014732-ee1420b12dee`.

All eight setup cases and the `native-default-base` reproduction now pass,
including the real child merge → native refresh → parent verification case.
The embedded submission of the minimal reproduction also passes. The direct
native-operation reproduction at the end of this report now succeeds with both
the shallow clone and full-clone control.
The production recipe supplies only `target_base_hash` to `thinpackrebase`.

The fix adds task-time defaults `context.git.execution.base_hash` and
`context.git.execution.head_hash`, resolves shallow ancestry incrementally, and
persists the refreshed base and remaining local commits for subsequent tasks.
The legacy `context.git.resolved_hash` can intentionally remain unresolved; the
fix does not force it to pin the job early.

The c2j team also determined that the failure-then-success observation below was
a **whole-job retry**, not replay losing a recorded result. A new attempt saw the
child's completed merge and took the already-initialized path. That retry policy
is unchanged. The original observation and reproduction evidence are retained
below as historical context, not as an outstanding replay defect.

See the [team response](../RESPONSE_C2J_THINPACKREBASE_CHILD_REFRESH.md).

Retested with c2j `v0.0.79-0.20261016052546-6a25847a90d0`: the eight setup cases
and native-default reproduction still pass. The full model-mocked build lifecycle
test now also passes after the separate
[test-runtime secret provider issue](BUG_REPORT_C2J_RUNTIME_TEST_OPTIONAL_SECRETS.md)
was fixed. It exercises the real child build, four review responses, child merge,
native parent refresh, and parent merge, verifying that the mandate is visible
before the original request's design begins.

## Impact and expected behavior

Build now checks for `.c2j/mandate.md` before design. When missing, it starts a
same-cell build to initialize the mandate, waits for its merged result, and calls
`thinpackrebase` with that result's `merged_hash`. The next operation must see the
mandate in the parent's managed worktree before the original request continues.

The native operation should resolve the parent's managed base, refresh to the
merged child commit, and propagate its Git context to subsequent operations.
It must support the shallow worktrees c2j itself prepares. Actual divergent
history must still be rejected; shallow history must not be misreported as
divergence.

Two independent defects blocked this flow on v0.0.77. The recipe uses `thinpackrebase`;
the temporary shell fetch/merge workaround has been removed at the maintainer's
request. Fixes to the runtime belong to c2j, not this cell.

## Versions and scope of evidence

- Installed CLI: `c2j version v0.0.77`, built with Go 1.27.1, linux/arm64.
- CLI SHA-256: `1b0eaacb2e717d2b024ef5c1aa21d3f7378b216fbcb027ead39ea328cdbf65de`.
- Git: 2.39.5.
- Inspected c2j checkout: `fe82ba2686b59cbac795a3e4a05dcf13ccc9a8a3`.
- Direct operation reproduction ran against that checkout. Its
  `pkg/git/thinpackrebase/rebase.go` is byte-identical to the installed v0.0.77
  module-cache source.
- Reproductions use temporary local repositories. No model, Nix, credentials,
  remote Git service, or production merge is needed. No c2j source was modified.

## Defect 1: the native base-hash default is empty

Even a no-op refresh to the current HEAD fails with the op's documented default
for `base_hash`. A preceding real command can read HEAD, but the recipe-visible
`context.git.resolved_hash` is empty.

From the recipes repository:

```sh
c2j test run \
  --file guides/repros/thinpackrebase/default-base.case.yaml \
  --case-timeout 1m \
  --out-dir /tmp/thinpackrebase-default-base
```

The [recipe](repros/thinpackrebase/default-base.yaml) captures the actual HEAD
and rendered context value, then invokes the real `thinpackrebase` with
`target_base_hash` equal to that HEAD. It deliberately omits `base_hash` to
exercise the operation's default. The [case](repros/thinpackrebase/default-base.case.yaml)
declares expected successful behavior; its failure is not converted into a
passing expected-error test.

Observed inspection output:

```json
{"head":"fbb714227ad2b465c4606a574e413e0dfba379e6","rendered_base":""}
```

Observed failure (exit status 4 from `c2j test run`):

```text
sequence node 1 failed: op input validation failed: validate op input:
Key: 'ThinpackRebaseInput.BaseHash' Error:Field validation for 'BaseHash' failed on the 'required' tag
```

This occurs before the operation runs. It also prevents runtime mocks of
`thinpackrebase` from testing later recipe branches: input validation precedes
the mock.

The same failure was also reproduced outside the test harness with the embedded
runtime, so it is not limited to test fixtures:

```sh
c2j submit \
  --recipe-file guides/repros/thinpackrebase/default-base.yaml \
  --inputs-json '{"prompt":"Diagnose native Git base resolution"}' \
  --run --embed
```

The live command exited 1 with the identical `ThinpackRebaseInput.BaseHash`
validation failure after its inspection operation succeeded.

Investigation pointers in c2j:

- `pkg/git/thinpackrebase/wrapper.go`: `BaseHash` defaults to
  `{{ context.git.resolved_hash }}` and is required.
- `pkg/worker/compiler/compiler.go`: `executeOpAttempt` injects defaults,
  resolves templates, and validates inputs before constructing the activity
  invocation with workspace preparation.
- `pkg/git/gitstate/workspace_controller.go`: `cloneIfNeeded` resolves HEAD
  into the prepared task's `ResolvedBaseHash`.

The empty rendered value and validation failure are confirmed. The precise fix
for propagation or resolution timing requires the c2j team's assessment; reading
HEAD successfully in a prepared operation does not prove its value reached the
outer recipe context.

## Defect 2: present target objects conceal missing shallow ancestry

Passing an explicit, correct base isolates a second defect. Given two commits
`A -> B`, with B the mandate merge, reproduce c2j's workspace preparation:

1. Clone upstream at B with depth 1 and `--no-single-branch`.
2. Fetch A with depth 1 and check out A.
3. Invoke `thinpackrebase` with base/persist A and target B.

Both commits exist locally. In the complete upstream, B's parent is A.
Nevertheless, the shallow boundaries hide that ancestry from Git's graph walk.

Observed output from the direct operation reproduction below:

```text
base=dd3a384732634a31a298655f17b720d7d77db6bd
target=cb00e6f071cc15afd87ee01cb55a1763ba913cf5
target_parent=dd3a384732634a31a298655f17b720d7d77db6bd
shallow=true target_object=commit
ancestry_check=exit status 1
thinpackrebase_error=target base cb00e6f does not descend from current base dd3a384
shallow=false target_object=commit
ancestry_check=<nil>
```

The control uses a separate full clone of the same upstream, the same A/B inputs,
and the same native function. It succeeds, returning `new_base_hash = B`,
`new_persist_hash = B`, and a `git_context_patch` containing B. Commit hashes vary
between executions.

Confirmed cause in `pkg/git/thinpackrebase/rebase.go`:

- `ensureTargetAvailable` (around line 188) returns immediately if B's commit
  object exists. Object presence does not establish complete ancestry.
- Its fetch path uses ordinary `git fetch`, without explicitly addressing shallow
  history.
- `ensureLinearHistory` (around line 206) then interprets a negative
  `git merge-base --is-ancestor A B` as genuine divergence.
- `pkg/git/gitshallow/gitshallow.go` (around lines 69–84) creates exactly the
  depth-1 clone/fetch layout used in the reproduction.

The operation needs to distinguish missing ancestry from real divergence and
obtain sufficient history inside the native operation before making that
decision. Recipes must not need a shell unshallow/merge step.

## End-to-end regression and historical retry observation

From the recipes repository:

```sh
c2j test run \
  --file recipe-tests/cell-setup.test.yaml \
  --case child-merge-refresh-real-git \
  --case-timeout 1m \
  --out-dir /tmp/cell-setup-native-refresh
```

This uses a deterministic child build fixture and real child-job execution,
`squashrebasemerge`, native refresh, and parent worktree observation. No model
calls are involved. Its assertions require exactly one native refresh and a
subsequent parent operation that sees the merged mandate.

During the original investigation, after the child merged,
the final runtime report recorded the parent's initial check as `ready`, although
that job had already launched initialization when the mandate was missing. The
parent could report successful completion without the refresh/verify calls; the
explicit regression assertions failed. In an earlier run with a supplied base,
the log recorded the shallow-ancestry error, followed by a repeated check and
parent completion. This is not evidence that refresh succeeded. The underlying
cause was subsequently identified by the c2j team as a whole-job retry; see the
resolution above. These assertions are retained to verify the native refresh path.

Original v0.0.77 setup suite result: five cases passed; three failed. The refresh-failure
and missing-refreshed-mandate cases failed early on the empty base default. The real
child case failed the required refresh/verification assertions. These failures
were retained, and all eight cases now pass without weakening their expectations.

## Acceptance criteria for c2j

- Native `base_hash` defaults resolve correctly from the managed parent state,
  including when the submitted context initially contains only repository/ref.
- A valid descendant refresh succeeds on c2j-created shallow worktrees even when
  the target object already exists; include a test with pending local commits.
- Truly divergent history and rebase conflicts still fail without losing the
  parent's changes.
- The returned Git metadata and refreshed content reach the next operation.
- Resuming within an attempt retains recorded task results. Separate whole-job
  retries may reevaluate setup against the updated upstream under the existing policy.
- The original expected-success recipes tests pass without shell refresh,
  fabricated context hashes, or expected-error exemptions.

## Direct native-operation reproduction

Save the following as `/tmp/thinpackrebase-repro.go`, then run from a c2j checkout:

```sh
go run /tmp/thinpackrebase-repro.go
```

The program calls the native `thinpackrebase.Run` implementation. The shell Git
commands only construct and inspect disposable fixture repositories; they do
not replace the refresh operation.

```go
package main

import (
 "context"
 "encoding/json"
 "fmt"
 "os"
 "os/exec"
 "path/filepath"
 "strings"

 "github.com/colony-2/c2j/pkg/git/thinpackrebase"
)

func git(dir string, args ...string) string {
 cmd := exec.Command("git", append([]string{"-C", dir}, args...)...)
 out, err := cmd.CombinedOutput()
 if err != nil { panic(fmt.Sprintf("git %v: %v: %s", args, err, out)) }
 return strings.TrimSpace(string(out))
}
func main() {
 root, err := os.MkdirTemp("", "thinpackrebase-repro-")
 if err != nil { panic(err) }
 defer os.RemoveAll(root)
 upstream := filepath.Join(root, "upstream")
 if err := os.Mkdir(upstream, 0755); err != nil { panic(err) }
 git(upstream, "init", "-q", "-b", "main")
 git(upstream, "config", "user.name", "Repro")
 git(upstream, "config", "user.email", "repro@example.test")
 git(upstream, "commit", "-q", "--allow-empty", "-m", "base")
 base := git(upstream, "rev-parse", "HEAD")
 if err := os.WriteFile(filepath.Join(upstream, "mandate.md"), []byte("Own this repository.\n"), 0644); err != nil { panic(err) }
 git(upstream, "add", "mandate.md")
 git(upstream, "commit", "-qm", "mandate")
 target := git(upstream, "rev-parse", "HEAD")
 fmt.Printf("base=%s\ntarget=%s\ntarget_parent=%s\n", base, target, git(upstream,"rev-parse", target+"^"))
 for _, shallow := range []bool{true, false} {
  workspace := filepath.Join(root, fmt.Sprintf("shallow-%v", shallow))
  args := []string{"clone", "-q"}
  if shallow { args = append(args, "--depth", "1", "--no-single-branch") }
  args = append(args,"file://"+upstream,workspace)
  git(root,args...)
  if shallow { git(workspace,"fetch","-q","--depth","1","origin",base) }
  git(workspace,"checkout","-q",base)
  fmt.Printf("shallow=%s target_object=%s\n",git(workspace,"rev-parse","--is-shallow-repository"),git(workspace,"cat-file","-t",target))
  cmd:=exec.Command("git","-C",workspace,"merge-base","--is-ancestor",base,target)
  fmt.Printf("ancestry_check=%v\n",cmd.Run())
  output, err := thinpackrebase.Run(context.Background(),thinpackrebase.ThinpackRebaseInput{RepoPath:workspace,BaseHash:base,PersistHash:base,TargetBaseHash:target,BaseRepo:"file://"+upstream})
  if err != nil { fmt.Printf("thinpackrebase_error=%s\n",err) } else { data,_:=json.Marshal(output); fmt.Printf("thinpackrebase_output=%s\n",data) }
 }
}
```

# Adaptive3 merge queue refactor

## Recommendation

Move the queue's batch decisions and Git helpers into one Recipes-owned Python
program, exposed as a c2j extension op. Keep grouped admission, isolated check
jobs, hook execution, Git persistence, and native merge in the recipe. Start
with behavior parity inside today's sealed batches. Use the same decision
interface to compare Uber SubmitQueue as a Go library if we want to improve
which checks the queue runs.

The review decision is whether to start with the Python extraction and use
measured results to justify a SubmitQueue integration. This plan fits the
Recipes cell's ownership of workflow policy and its implementation. The c2j
cell owns any changes to runtime scheduling, grouping, or workspace primitives.
[Recipes purpose](../../PURPOSE.md)

## Where the complexity is today

The queue has 11 helper YAML files totaling 1,266 lines. Eight contain inline
Python. Admission and selection logic is also split between Python, CEL, and
shell checks. For example, the subset planner sees lists of IDs and pass/fail
bits, while YAML validates child results, accumulates evidence, and decides
which result can be used for landing. Extracting only the heredocs would leave
that split in place.
[Subset selection](../../recipes/adaptive3/merge-queue-select.yaml) ·
[Landing](../../recipes/adaptive3/merge-queue-land.yaml)

| Responsibility | Proposed home |
| --- | --- |
| Group by cell and canonical branch, seal generations, wait for predecessors and check children | c2j grouping and child jobs, wired by Recipes |
| Validate and deduplicate contributions, order by original submission age, reconcile already-landed IDs | Python op |
| Replay source bundles, capture conflict evidence, install an exact assembled bundle, confirm landed receipts | Python Git helpers with c2j workspaces and artifact bindings |
| Decide whether to try a baseline, probe subsets, select a passing stack, or report an operational failure | Python decision functions |
| Start bounded conflict repair, run the repository verifier, retry on upstream movement, publish the exact verified stack | Recipes using native c2j steps |
| Assemble per-change outcomes and failure evidence | Python op |

The current queue validates the full stack first. On a validation failure it
checks the published baseline, runs isolated subset probes, and verifies the
selected assembly again before landing. It admits up to 50 contributions per
serial generation and probes up to four subsets at a time. Those are the
starting behaviors for the extraction.
[Queue behavior](../../recipes/adaptive3/README.md#merge-queue) ·
[Batch receiver](../../merge-batch.yaml) · [Check recipe](../../merge-check.yaml)

## What SubmitQueue can supply

I reviewed the Apache-2.0 Go module at `19dfedd69985`. Its exported
`Speculator` is a usable library boundary. It accepts a snapshot of batches,
dependencies, and prior paths, and returns proposals to build or cancel paths.
The standard implementation combines the `bestfirst` generator with the
`sticky` allocator, which fills a build budget without preempting running
checks. A standalone Go program imported those packages by upstream version
and produced two build proposals for a two-batch dependency example. The
upstream tests for the standard planner, generator, allocator, and
`pathoverlap` analyzer passed locally.
[Speculator contract](https://github.com/uber/submitqueue/blob/19dfedd699850578be199632c9faf8dabbeb93a1/submitqueue/extension/speculation/speculator/speculator.go) ·
[Standard implementation](https://github.com/uber/submitqueue/tree/19dfedd699850578be199632c9faf8dabbeb93a1/submitqueue/extension/speculation/speculator/standard) ·
[License](https://github.com/uber/submitqueue/blob/19dfedd699850578be199632c9faf8dabbeb93a1/LICENSE)

| Approach | Fit |
| --- | --- |
| Import the upstream Go planner into a small JSON-speaking op | Feasible without a SubmitQueue service. Useful if we have meaningful dependency paths to rank. The adapter would map C2 changes and check receipts into the upstream batch/path model, then map build proposals back to ordered contribution IDs. |
| Fork or extract a narrow upstream component | Worth considering if a comparison shows a useful algorithm and the public interface cannot express our inputs. Keep the fork at the planner boundary and pin its upstream revision. Owning a fork of the controller would also mean maintaining its admission, finalization, storage, and message dispatch assumptions. |
| Use the full upstream controller with c2j adapters | The controller expects its own persisted batch and path transitions, message delivery, and land callbacks. Plugging c2j into its Git or CI providers would still leave those lifecycle decisions in the controller. This would require replacing or duplicating substantial c2j queue behavior. |
| Extract the current policy into a Python op | Direct fit for the existing sealed-batch behavior and the YAML cleanup. It also gives us a baseline and a decision interface for comparing an upstream planner. |

The semantic difference matters. SubmitQueue funds possible futures for
multiple in-flight batches. Each path predicts which earlier dependencies will
land before a particular batch. Adaptive3 already has one sealed generation
and looks for an age-preferred, passing subset inside it. A direct library
integration would need to model contributions as upstream batches or otherwise
translate that decision. The speculator returns proposals, and the upstream
controller owns verdicts. Keep our landing gate and per-change receipts in
C2. Path overlap could help prioritize probes, with combined verification
still controlling what may land.
[Upstream speculation](https://github.com/uber/submitqueue/blob/19dfedd699850578be199632c9faf8dabbeb93a1/doc/rfc/submitqueue/speculation.md) ·
[Controller wiring](https://github.com/uber/submitqueue/blob/19dfedd699850578be199632c9faf8dabbeb93a1/submitqueue/orchestrator/controller/speculate/speculate.go) ·
[Path overlap](https://github.com/uber/submitqueue/blob/19dfedd699850578be199632c9faf8dabbeb93a1/submitqueue/extension/conflict/pathoverlap/README.md)

For a library trial, the Go adapter can translate a path that assumes an
older contribution succeeds into a probe containing that contribution and
the path's head, in queue order. Map completed c2j check receipts back into
path results. Convert proposals only for the current pinned generation and
deduplicate against already observed probes. The same c2j recipe runs the
checks and decides whether their receipts authorize landing. Running
speculation across later generations would require a separate design for
how those generations become visible before their predecessors complete.

## Proposed task boundary

Package the Python program in a directory such as `recipes/merge-queue/`. Use
`op.yaml` with a top-level `python` environment and `command: [python3, main.py]`.
Start with the standard library and Git, with `requires-python: ">=3.10"` and
`dependencies: []`. The process reads a schema-validated request on stdin,
writes a typed result to stdout, and writes bundles and diagnostics to the
c2j outbox. The manifest's Python declaration selects the interpreter and
libraries. The extension selector identifies the executable source.
[c2j extension Python support](https://github.com/colony-2/c2j/blob/c412b478897ee0637f879b3c7b13b1afbdf092a6/EXTENSION_OPS.md#python-libraries) ·
[Execution tools](https://github.com/colony-2/c2j/blob/c412b478897ee0637f879b3c7b13b1afbdf092a6/EXECUTION_TOOLS.md#python-script-environments)

Use named requests for intake, assembly, decision, install, and receipts.
Keep decision functions independent of Git and c2j, and share one Git helper
for worktree and bundle checks. A decision receives ordered contributions,
the pinned base, the verification policy, and the observed check results. It
returns the next decision and only the relevant data, such as the ordered
IDs to probe or the passing check to use. An ordinary conflict or rejection
returns a typed outcome with diagnostics. A failure to read or establish the
required evidence fails the operation. The batch recipe retains the small
set of explicit states that execute those decisions and feed outcomes back.
Each call completes inside one task.

Pass `context.environment.op.worktree_path`, `inbox`, and `outbox` explicitly.
c2j materializes input bundles and carries producer refs between tasks. Use
`const: true` for decision and scratch assembly calls. Invoke install as a
writable task against the pinned clean worktree and let c2j persist it. The
native merge is the only step that updates the target branch. Invoke it
on the installed, verified head with its prepared base. On upstream movement,
the recipe reruns intake against the new tip with its existing bounded chase.
The caller confirms its own reachable Change-Id and commit before publishing.
[Op-visible paths](../OP_VISIBLE_PATHS_USER_GUIDE.md) ·
[Git integration](../ops/OP_GIT_INTEGRATION.md) ·
[Grouping contract](https://github.com/colony-2/c2j/blob/c412b478897ee0637f879b3c7b13b1afbdf092a6/GUIDE-Recipe-Grouping.md)

The new boundary was exercised in a disposable c2j test at `c412b47`. A
Python op with a manifest-selected interpreter read a typed request and inbox
file, wrote an artifact, and a subsequent call used the artifact to write a
managed workspace file that a third task could read. This tested the execution
contract. The queue itself still needs the migration and parity cases below.

## Implementation and review checkpoints

1. **Extract decisions and intake first.** Move contribution validation, age
   ordering, subset planning, interpretation of check receipts, and outcome
   assembly into typed Python functions. Compare their outputs and chosen
   probes against the existing native cases. Keep approval, verification,
   parallelism, and budget behavior while making the logic directly testable.
2. **Move the Git scripts and simplify the batch recipe.** Consolidate replay,
   conflict evidence, bundle installation, and receipt confirmation in the same
   program. Keep native squash, child dispatch, hook execution, and merge at
   their current authority boundaries. Replace shell JSON parsing and CEL
   policy expressions with typed op inputs and outputs. Keep the contribution
   and receipt wire formats and publish the caller, receiver, check recipes,
   and op source together. Test an old admitted caller across the revision
   change using its recorded receiver and artifacts.
3. **Measure verification work before tuning it.** Compare check starts,
   duplicate checks, check elapsed time, and age ordering on the same inputs.
   The current subset loop retains pass/fail summaries and rebuilds the final
   candidate. Evaluate carrying the complete successful receipt and exact
   assembly bundle forward. Reuse requires matching base, candidate head,
   ordered contributions, effective verification identity, and policy. An
   advanced base, changed assembly, mismatched policy, or missing evidence
   triggers fresh verification. Keep this change separate from the parity
   refactor. [Existing verification receipt](../../recipes/adaptive3/verify-candidate.yaml)
4. **Compare SubmitQueue at the planner boundary.** Run a small pinned Go
   adapter over recorded or synthetic batch inputs using the same check
   budget and final landing gate. Include interacting changes, an older
   change that fails alone but passes with another, an infrastructure failure,
   and a moving base. Compare verifier calls, time to a landable stack, and
   whether the chosen stack respects the current age preference. Adopt the
   dependency if it reduces work or improves selection enough to justify
   the adapter and packaging. A useful adapter can run as a Go extension
   with the same planner inputs and outputs. Consider a narrow fork only
   if that benefit depends on changing the upstream planner interface.

## Acceptance for the refactor

- Unit-test contribution and receipt validation, queue ordering, evidence
  classification, and bounded selection with ordinary Python test cases.
  Cover invalid child evidence, failing baseline, interacting changes, and
  search exhaustion. Use temporary real Git repositories for bundles,
  conflicts, binary and mode changes, failed install, and already-landed IDs.
- Exercise the actual op selector and Python environment in native c2j tests.
  Use real grouping, artifact transfer, workspaces, child checks, and merge.
  Script model decisions only. Rerun the existing caller, replay, selection,
  and public build cases. Check the affected requirements in the
  [merge queue test statements](../../recipe-tests/adaptive3/merge-queue-statements.md)
  and add coverage where the current cases leave a gap.
- Before rollout, exercise a grouped batch with multiple contributors,
  a serial successor, interruption and recovery, an upstream-advance race,
  and mixed per-change outcomes. Verify that the merged head is the verified
  head, failed results retain readable evidence, and publication observes
  each caller's confirmed commit. Record task counts and results on the
  selected c2j runtime. [Native recipe testing](../NATIVE_RECIPE_TESTING.md)

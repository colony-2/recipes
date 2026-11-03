# Direct recipe state and file handoffs

This work fits the recipes cell and changes the active adaptive build path.
Externalized prompts remain set aside. No c2j or c2ops implementation changes are
needed. Acceptance statements were defined before implementation in
[direct-state-statements.md](../recipe-tests/adaptive/direct-state-statements.md).

## State ownership

The general `flow` object has been removed from the adaptive recipes and their
helper interfaces. Each include receives named values relevant to its task.
Configuration stays at the enclosing recipe scope; changing documents and
sessions are passed explicitly where they cross a scope boundary.

| Information | Source or handoff |
| --- | --- |
| Request, target directory, selectors, verification requirement, iteration limit | Enclosing recipe inputs; never copied through a loop-wide object. |
| Configure guidance and specialist assignments | The actual configure outputs selected in build.yaml. The main loop no longer accepts all hook settings. |
| Candidate and changed-file inventory | `states.prepare.outputs.candidate`; changed status is computed from its files when needed. |
| Verification gate and evidence | `states.verify.outputs.allowed`, `result`, and artifact outputs. No shadow verification flag. |
| Independent assessment | The assessment step's `approved`, `next`, and response outputs. No copied assessment status or last event. |
| Coordination registries | The coordinator's jobs and threads outputs, with initial caller-supplied dependencies as the fallback. |
| Completed agent response | The work step's native turn/result. No additional result stored in every transition. |
| Human acceptance | The review response and its receipt; actual verifier and assessor outputs still gate completion. |
| Attempt and recovery counts | Native state run history, including the caller's initial rebase-repair count when applicable. |
| Documents and annotations | Explicit artifact-map/list handoffs between steps that add or revise them. |
| Session and current assignment | Explicit dispatch inputs. Coordination and response repair can provide a newer session. |

Some values must persist separately because later steps cannot infer them from
the current checkout: agreed prerequisite keys, the candidate and hook identity
used for approval, the merge-chase count, and the original documents retained
during response repair. These have specific owners and consumers. They are not
repackaged into a generic context object.

The `resume_merge` routing value records whether a rebase follows an upstream
advance. Fresh verification still runs before approval reuse. Ordinary repairs
and changed candidate content continue through independent assessment.

c2j's scope boundaries require explicit input mappings into nested sequences and
includes. A state reads the producing step's property, passes that value to its
child, and exports only what downstream consumers need. These mappings preserve
scope without introducing global aliases or runtime state readers.

## Errors and feedback

Failures are converted into artifact bindings where they are handled:

- Verification keeps its typed result for gates and prepares current logs and
  a readable result note for the agent. Successful logs use `verification/`;
  failures and required-skipped checks use `error/`.
- Preparation, response repair, and rebase recovery prepare their own error
  notes and diagnostic files. No error history or event flag is required by
  the agent include.
- Human responses become feedback files when the review returns. Coordination
  emits its per-key status documents alongside agreements and child reports.
- Artifact-binding recovery inspects the actual supplied bindings. It no longer
  maintains alternate filename patterns or copies a synthetic verifier failure
  into workflow state.

The agent receives the current assignment and actual artifact references. Its
generic instruction is:

```text
Review the errors in the error directory when present, and address the feedback directory's current comments.
Read consultations/ and jobs/ when present for recorded agreements and outcomes. Do not duplicate recorded work.
```

No filename list, failure object, phase-history file, or duplicate evidence
manifest is added to the prompt. Artifact maps remain necessary for c2j to
materialize the files. Old transient errors are excluded from accumulated
documents; the producing step supplies the current error bindings separately.

Typed status remains authoritative for routing. Encapsulating diagnostics in
files does not remove required verification, child-completion, or approval gates.

## Regression coverage

The existing fixtures now call the specific helper inputs and inspect actual
outputs rather than asserting fields of an internal `flow` snapshot. Native
rebase checks still verify saved changes, adopted target, preserved concurrent
work, fresh verification, and the absence of agent-run `git rebase` commands.

Focused cases additionally cover:

- An agent consumes an error log with no corresponding failure/event record and
  no filename enumeration in its prompt.
- After repeated invalid implementation responses and human direction, correction
  remains read-only and retains its error files and original test statements.
- A malformed response missing required fields cannot overwrite completed
  documents or bypass response repair.

## Validation results

Runtime baseline: c2j `f1a153b898c57e93e9b01477d08cc02c1509ee4b`.

- **147 cases across 23 adaptive suites passed**, using fixture agent decisions
  and real native Git, hook, artifact, review, and child-job operations.
- **34 native cases passed directly against repository recipes**, without the
  package-resolution workaround: inbox bindings (9), smoke (1), command logs (4),
  extension diagnostics (1), verifier contracts (16), rebase recovery (1), and
  validation children (2).
- `c2j test validate --directory recipe-tests/adaptive --parallelism 2` and
  `git diff --check` passed. Source inspection found no `flow`, last-phase mirror,
  copied verification/assessment flags, or specialist/validation round registry
  in the active adaptive recipes.
- Native smoke job `3LbvNQpG6iQM2uXXy9j1ZsMQpbO` bound the new DS acceptance
  statements, consumed the real execution log through `error/`, and retained its
  statements and result artifacts in the fixture report.

Reports: `/tmp/direct-regression-complete` for the regression run and
`/tmp/direct-source-*` for native source runs.

The agent-mocked regression suite used the same isolated package-resolution
workaround described in the [preceding report](IMPLEMENTATION_STANDARD_AGENT_INBOX.md):
published selector calls were expanded to their extension primitive in a temporary
copy, existing fixture mocks supplied agent results, and installed tools replaced
Nix package provisioning. Repository recipes retain their published selectors and
package declarations. These results do not validate live model sessions or the
host's published Nix resolution.

Direct `submit --advanced-recipe-file ... --run --embed` was attempted again with
the smoke recipe and attached DS statements. The existing local JobDB still
rejects opening its database until the upstream chapter-artifact migration is
performed. No shared database was migrated. The same smoke passed through c2j's
isolated native test runtime.

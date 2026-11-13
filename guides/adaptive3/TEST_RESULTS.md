# Adaptive3 test results — 2026-11-13

Initial runtime: c2j `c244db82949ea989cd90d4352325b40b88cca5d0`. Recipe baseline:
`c0c69bd`. The initial results below are historical; follow-up results use the
current `.c2j-version` pin, `3fec5e455133216ab103a4eb693143e09640742b`.

## Results

| Check | Result |
| --- | --- |
| Source validation | All adaptive3 cases accepted by native `c2j test validate`. |
| Adaptive3 native execution | 42 cases passed: 41 across nine suites in the final full run, plus the subsequently added native cancellation case. The preinstalled-tool environment is described below. |
| Embedded validator tests | 8 passed against the actual code extracted from `tools.yaml`. |
| Existing adaptive2 dependency/requirements suite | 19 passed unchanged on the updated c2j revision. This is a focused regression check, not the whole adaptive2 suite. |
| Live one-pager and review discussion | Passed using real Execute, Validate and answering agents with scripted human replies. |
| Live receiving-owner consultation | Passed using real Execute, Validate and independent Review agents. The first attempt hit provider capacity; the same-provider retry passed. |
| Conditional sequence probes | Both focused probes passed on updated c2j; the old pinned build executed the skipped step. |
| Recipe timeout policy | Passed for all 127 workflow/example files discovered by the repository checker. |

## What the native suites exercise

| Suite | Cases | Tested behavior |
| --- | ---: | --- |
| `build.test.yaml` | 8 | Explanation completion; full feature merge; same-job failure resolution; completed-merge preservation during publish recovery; scope return to Direction; stale merge with full revalidation and approval reuse; managed hook workspaces; human direction after a failed resolver correction. |
| `consultation.test.yaml` | 5 | Receiver workspace; nested advice; receiver-authored child assignment; actual child failure/result consumption; explicit choice of an existing delivery workflow. |
| `cycle.test.yaml` | 4 | Complete activity pass; questions remain in Review; literal request text; read-only planning cannot persist code edits. |
| `integration.test.yaml` | 4 | Unchanged rebase reuses native approval; content, mode and binary changes require review. These use real Git objects and patches. |
| `lifecycle.test.yaml` | 6 | Every check repeats after correction; human feedback resets automatic allowance; exhausted automatic work remains recoverable; required verification cannot be waived; native error logs reach repair; actual uploaded notes reach Review and Execute. |
| `package-probe.test.yaml` | 1 | Approved config installs `uv:pytest==8.3.5`; a fresh task actually runs `pytest --version`. |
| `packages.test.yaml` | 4 | Human denial prevents probes; policy/human approval precede failed probes; successful fresh-job probe precedes exact adoption. |
| `resolver.test.yaml` | 2 | Discussion requires explicit Continue; Continue with an empty message preserves the proposed correction, earlier stage and uploaded notes. |
| `tools.test.yaml` | 7 | Valid/missing links; final title validation; 2,000-file diagnostics kept out of stdout; unrelated config rejection; proposal versus adoption. |
| `cancellation.test.yaml` | 1 | Native human cancellation while an agent is prepared preserves existing work and remains terminal; it does not enter resolution or create replacement work. |

The eight direct tests add readable/corrupt images, escaping and machine-local
links, large diagnostics, binary/mode approval comparisons, and exact package
configuration checks. They extract and execute the embedded source instead of
maintaining a second implementation of the validators.

Some native cases deliberately fail a child command or hook. Those errors in the
runner log are expected inputs; the case passes only if the parent handles them
as asserted. The final nine-suite run has zero failed suites. The additional
cancellation case uses c2j's prepared-operation controls and checks native
cancellation and preserved effects; it does not run a model.

## Execution environment and limits

This host has no normal `/nix` installation and cannot mount one. Portable Nix
allowed dependency downloads and real c2ops execution, but native activation of
the validators' declared packages failed in c2j's derivation JSON parser. Trying
newer portable Nix encountered separate local SQLite/openat errors.

To test the recipe behavior, a disposable copy removed **only** `execution_needs`
from `tools.yaml` and `package-probe.yaml`. Python, Pillow, cmark and yq were
preinstalled on PATH. The source files in this repository retain their dependency
declarations. Successful read-only c2ops manifest evaluations were cached in the
temporary environment to avoid repeated portable-Nix startup cost.

The native runner still executed the actual recipe graph, templates, command
bodies, artifact transport, input forms/receipts, managed repositories, Git
operations and waits. Most agent choices were scripted. Child submission mocks
created actual local disposable child jobs; they substituted for remote selectors
whose adaptive3 files have not yet been published. The package success fixture
used the actual local `package-probe.yaml`, native config activation and real uv
provisioning. It did not mock `pytest --version`.

These results establish orchestration and validator behavior in that environment.
They do **not** establish unmodified Nix dependency activation on a production
worker, remote selector deployment, or resilience to every runtime failure.
Those boundaries are recorded in [RUNTIME_REQUIREMENTS.md](RUNTIME_REQUIREMENTS.md).

## Live examples

The [notebook one-pager and question/answer](results/README.md) completed in about
3 minutes 47 seconds. The completed storage consultation took about 3 minutes
6 seconds. Each completed trial used three actual agent responses, all accepted
by the output schemas with zero repair attempts.

The storage owner challenged the new restore endpoint, proposed using the existing
version-checked update, and explained the effect of counting distinct autosaves.
Its independent reviewers checked those claims against the disposable repository.
Advice acceptance did not pretend that the parent had approved the changed semantics.

There is no live UI screenshot or full delivery/merge trial in this result set.
The image tests validate attachment usability; relevance is still an agent
assessment and needs live evaluation. Mocked choices establish routing, not
general model judgment.

## Commands for a normal worker

Use the c2j revision in `.c2j-version` and a supported Nix environment:

```sh
c2j test validate --directory recipe-tests/adaptive3
c2j test run --directory recipe-tests/adaptive3 --parallelism 2 --case-timeout 5m
python -m unittest discover -s recipe-tests/adaptive3 -p 'test_tools.py' -v
c2j test run --file recipe-tests/adaptive2/dependency-requirements.test.yaml --case-timeout 5m
python3 recipe-tests/checks/recipe_timeout_policy.py .
```

The direct Python tests need PyYAML, Pillow, cmark, yq and Git. `--case-timeout`
limits the test harness, not production recipe execution. Live commands and
fixture details are in the [test README](../../recipe-tests/adaptive3/README.md).


## Follow-up implementation results

| Check | Final result |
| --- | --- |
| Native source validation | All 82 cases validate. |
| Native recipe execution in the dependency-substitution lane | All 82 cases pass across the full run and targeted follow-ups. |
| Direct embedded-validator tests | 9 pass. |
| Actual Cortex adapter/renderer DOM tests | 3 pass using the generated native forms. |
| c2j model-default materialization | Default matrix and required/nested default checks pass. |
| Unmodified native dependency activation on a supported worker | Not established; the audited Cortex job demonstrates a real Pillow activation failure. |
| Compact native directory references | Unavailable; 1,024 files expand to 202,940 bytes of reference metadata. |

The broad execution run passed 79 of 81 cases. One test-lane copy lacked a required
document fixture; the default-build suite passed after restoring it. The other
case still expected human renewal after one automatic resolver correction; its
fixture now exercises the specified two corrections before human renewal and passes.
A further receiving-owner adoption case passes. Targeted follow-ups also verify
recovered bug classification and command/Git diagnostics returned with child results.

Native execution uses a disposable copy with only the validators' `execution_needs`
removed and their declared tools preinstalled. Native state machines, managed Git,
submissions, waits, input forms and command bodies execute. Model decisions are
scripted. This setup cannot verify dependency realization or activation on a real
worker. It must not be used to claim that the audited Pillow failure is fixed.

The actual repeated-upstream test performs native merges and rebases, pauses after
three automatic merge-chase returns, renews one attempt and completes without
repeated human approval for the unchanged edit. Child checks cover failed and
successful attempts, a corrected retry, adoption of active/completed attempts,
receiver-side adoption and invalid reports after submission. The cancelled-child
message is a scripted native-result fixture; parent cancellation has a real
prepared-operation cancellation test.

See [the implementation assessment](FOLLOWUP_IMPLEMENTATION.md) for each todo item
and [the job audit](AUDIT_3M28e5.md) for the production failure and test gap.

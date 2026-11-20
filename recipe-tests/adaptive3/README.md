# Adaptive3 tests

Run with the c2j revision in `.c2j-version`, working Nix and the trusted colony2
cache. Tests use disposable repositories and JobDBs. Native operations execute;
model choices are scripted except in explicitly selected live suites.

```sh
c2j test validate --directory recipe-tests/adaptive3
c2j test run --directory recipe-tests/adaptive3 --parallelism 1 --case-timeout 5m
```

`--case-timeout` is a test-runner limit, not a recipe execution timeout.

The direct validator tests execute the actual Python embedded in `tools.yaml`
against real files and Git objects. They need Python, PyYAML, Pillow, cmark, yq
and Git on PATH. Schema tests additionally use jsonschema to validate actual producer
reports independently of mocked provider success flags:

```sh
python -m unittest discover -s recipe-tests/adaptive3 -p 'test_*.py' -v
```

These direct tests do not test dependency preparation. For the declared uv Python
environment and retained-cache reuse, run the [two-task worker check](../../guides/adaptive3/VALIDATOR_WORKER_CHECK.md).
It includes the actual validator with its dependencies intact; recorded runs cover
valid, missing and corrupt PNG attachments. Native `tools.test.yaml` also includes
the corrupt-image correction regression.

Coverage is described in [statements.md](statements.md). Cycle/lifecycle tests
cover full validation, review dialogue, original human wording and attempt
allowances. Integration tests compare real rebased binary/content/mode changes
and native approval receipts. Consultation uses receiving workspaces and native
child waits; its submission fixture creates a disposable local child in place
of the remote, unpublished adaptive3 selector. This tests result consumption,
not deployment of that selector.

`change-count-scope.test.yaml` inspects resolved prompts for all six purposes,
both directly and through real validation routes, including configured specialists.
Only Outcome receives change-count report requirements. `reporting.test.yaml`
compares the native measurements and candidate patch delivered to each assessor
with independent Git output, and covers complete, missing, invented and inconsistent
reports. Lifecycle controls retain full rechecking for actual defects and required
command failures. Scripted agent responses test routing, not live model judgment.

`context-routing.test.yaml` checks shared guidance delivery to fresh agent sessions.
`publication-ref.test.yaml` checks actual independent-child startup content for
implicit same-cell, explicit same-cell and cross-cell requests, saved caller edits,
and intentional candidate validation. The same suite creates distinguishable branches
before ordinary CLI submission to check captured non-main self/root defaults for
advice, submission and child content. It does not test automatic remote configuration
discovery. These use scripted agent choices and do not measure prompt effectiveness.
The separate [recommendation comparison](../../guides/repros/dependency-ordering/rubric.md)
uses fresh authenticated model sessions; its native routing cases only check the
comparison's instruction and scenario plumbing.

Package tests distinguish proposals from adoption and check approval before
probing, including a real fresh-task `uv:pytest==8.3.5` probe.
`package-probe-cli.test.yaml` submits the candidate through the actual CLI with a
stored proposal and read-only validator binding. It checks optional context,
command arguments, missing authority, required fields, typing and denied submission.
`package-probe-schema.test.yaml` also checks recipe typing where the CLI rejects
an invalid prompt first. `package-probe-cancellation.test.yaml` injects a native
cancellation envelope at the actual probe command after a real bounded write;
it checks catch behavior, not process cleanup. Existing preparation, rejection,
probe-failure/retry, native human cancellation and permission suites remain required. The public entrypoint
tests native Git publication and recovery in the same job. Do not infer model
judgment or complete runtime resilience from these scripted choices.

The [recorded results](../../guides/adaptive3/TEST_RESULTS.md) distinguish normal
source validation from the local preinstalled-tool execution environment. The
[assessment](../../guides/adaptive3/IMPLEMENTATION.md) records runtime boundaries.

Live suites are excluded by default. To generate actual writing for review:

```sh
c2j test run --file recipe-tests/adaptive3/examples.live.yaml --include-live --case-timeout 5m
c2j test run --file recipe-tests/adaptive3/consultation.live.yaml --include-live --case-timeout 5m
```

These require a working Codex provider. Human replies are scripted; the writing,
validation and conversational answers are live. See the
[saved trial documents](../../guides/adaptive3/results/README.md).

`default-build.test.yaml` targets root `build.yaml` directly, covering explanation,
feature delivery and repository-improvement hooks through adaptive3.

Review/v2 checks use the shared [contract corpus](../review-v2/contract-vectors.json)
and [acceptance statements](../review-v2/statements.md). Run the declaration/native
suite and Python checks before the consumer checks:

```sh
c2j test run --directory recipe-tests/review-v2
python3 -m unittest discover -s recipe-tests/review-v2 -p test_contract.py -v
```

The Recipes-owned consumer harness temporarily places tests in an unchanged,
published Cortex checkout with its locked dependencies. Pass complete native case
reports; missing reports or empty reviews fail. The following cases supply actual
Direction, discussion, Backstop and Package forms:

```sh
python3 recipe-tests/adaptive3/consumer/run.py /path/to/cortex \
  /path/to/review/cases/direction-decision/result.json \
  /path/to/review/cases/question-keeps-approval-pending/result.json \
  /path/to/backstop-actions/cases/apply-authorizes-displayed-action/result.json \
  /path/to/packages/cases/document-comments-regenerate-before-probe/result.json
```

This runs published presentation dispatch, validators, DOM controls and direct
native SQLite schema/upload submissions. Build Cortex and its test worker using
its normal locked build first, then run the real HTTP/browser tests:

```sh
python3 recipe-tests/adaptive3/consumer/run-browser.py /path/to/cortex --workers 1
```

The browser suite includes generated forms, production adaptive3 review/discussion
includes, controlled worker restarts and the frozen legacy form. It writes individual
screenshots, worker diagnostics, native outcomes and a restart comparison in the
Playwright results directory. Its agent is scripted to isolate routing; it reads
actual original/upload bytes. Real Codex answering context is checked separately:

```sh
python3 recipe-tests/adaptive3/consumer/run-context.py /tmp/adaptive3-context-check
```

That runner supplies a case-local provider to the real Codex CLI and c2ops,
checks actual file reads, ordered discussion and answering-session continuation,
and leaves production credentials unused. See the current [form contract](../../guides/REVIEW_V2.md).

The document-reader suite also checks complete native producer metadata, role ordering,
overview selection and drafts at desktop and phone widths. Include the native report
from `complete-selected-details-reach-form` for conflicting role/order coverage.

Follow-up suites cover requester correction/adoption, isolated diagnostic paths,
backstop-first continuation and independent finite loop allowances. `renewal.test.yaml`
advances an actual disposable upstream repeatedly to test merge chasing and approval
reuse. `collections.test.yaml` measures expanded native file-reference metadata;
it is not a claim that compact directory references exist.

Continuation orchestration scripts the backstop's recovered records. Exact history
retrieval is covered separately by `inspection.test.yaml`. The cancelled-child message
fixture scripts the terminal response; actual cancellation is covered for the parent.
See [the follow-up assessment](../../guides/adaptive3/FOLLOWUP_IMPLEMENTATION.md)
for the supported-worker dependency-activation gap exposed by a real Cortex job.

For a live writing check on managed workers, use the small containing lifecycle in
`guides/repros/live-document-details-check.yaml` with `c2j submit --from-workspace-now`
and a bounded preparation request. It accepts the CLI's prompt/title/type inputs,
uses normal model authorization and performs full validation without publication.
The local live suite needs its own valid provider credentials; HTTP 401 is a failed
live check, even when deterministic producer tests pass.

For the semantic negative case, submit `guides/repros/misleading-document-details-check.yaml`
on a managed worker with the same workspace option. It seeds schema-valid descriptors
about databases and billing on local draft-recovery documents, requires live independent
rewrite findings, and passes those findings into the existing correction lifecycle.
It succeeds only after the corrected preparation receives independent acceptance.

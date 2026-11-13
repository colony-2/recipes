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
and Git on PATH:

```sh
python -m unittest discover -s recipe-tests/adaptive3 -p 'test_tools.py' -v
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

Package tests distinguish proposals from adoption and check approval before
probing, including a real fresh-task `uv:pytest==8.3.5` probe. The public entrypoint
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

Consumer regression: after native cycle/backstop tests, run the real Cortex form
adapter and renderer in an isolated Cortex checkout with its locked dependencies:

```sh
python3 recipe-tests/adaptive3/consumer/run.py /path/to/cortex \
  /path/to/cycle/cases/questions-stay-in-review/result.json \
  /path/to/backstop/cases/backstop-retains-discussion-session/result.json
```

This exercises click, text entry, Back, upload and submit against actual generated
forms. It is a DOM integration test, not a deployed browser test.

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

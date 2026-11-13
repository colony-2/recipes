# Check the validator on a supported worker

The local preinstalled-tool tests check validation behavior. They do not establish
that c2j prepares the declared Python interpreter and libraries correctly.

This check runs the actual validator twice, in separate task environments, against
a Markdown file and a small PNG. It includes the shipped `tools.yaml` without
overriding its dependencies or injecting Python paths. The second task exercises
repeated preparation. Successful task records carry `setup.python` in their runtime
output envelope; failed preparation also attaches `_c2j/preparation.json`. The
ordinary `c2j job log --field` view exposes operation outputs, not that envelope.
A first task on an already-warm worker is not proof of fresh-cache coverage.

The validator now declares its script libraries through c2j's Python block:

```yaml
execution_needs:
  python:
    requires-python: ">=3.10"
    dependencies: ["Pillow==12.0.0"]
  packages:
    - nix:github:NixOS/nixpkgs/e7439b6b14ad3cc35d05608ebca9bce01a25f5f8#cmark
```

Python 3.10 is the minimum for the selected Pillow release. uv selects a compatible
worker interpreter and prepares its libraries; cmark remains a Nix CLI tool.
The repository's `.c2j-version` pins the first supporting main commit,
`d031eb49c6777555cca1f58449b8451b1fc77c37`. Both submission and execution must use
a supporting c2j build.

From this repository:

```sh
# Collect real preparation and validation results on the selected worker pool.
c2j submit 'Check the actual validator dependencies in two separate tasks.' \
  --cell recipes --jobdb http://192.168.1.195:9047/c2 \
  --title 'Check adaptive3 Python and Markdown tools' \
  --advanced-recipe-file guides/repros/validator-environment-check.yaml \
  --artifact review/README.md=recipe-tests/adaptive3/fixtures/validator/README.md \
  --artifact review/pixel.png=recipe-tests/adaptive3/fixtures/validator/pixel.png \
  --json
```

The job collects both outcomes even when validation fails. Its `summary`, `first`
and `repeat` outputs distinguish successful collection from successful validation.
Use `c2j job log` and exact task IDs to inspect command logs and preparation records.

## Earlier failure

Run on 2026-11-13 at 17:02 UTC, using the old separate Nix declarations:

- Job: `3M3pwm8Fo0AQPLpEYfw5lZMUi2K`.
- Goal: `3M3pwfdfmHTI53t0xqMzewyFC4e`.
- Both tasks failed with `ModuleNotFoundError: No module named 'PIL'`.
- Final summary: “Validator environment check did not pass.”

The [original report](../BUG_REPORT_C2J_PYTHON_DEPENDENCY_ENVIRONMENT.md) led to the
new Python environment support. c2j now documents separate Nix Python/library
declarations as unsupported; use this block or a prebuilt composed Nix environment.

## New configuration: real worker results

Run on the same JobDB on 2026-11-13, starting at 20:39 UTC. Each row ran the
unchanged validator body twice, with the new declaration above:

| Input | Job | Both task results |
| --- | --- | --- |
| Markdown with its attached valid PNG | `3M4GOglL4hFRUjqbFtLqUKLEmJf` | `passed`, zero findings |
| Same Markdown, PNG omitted | `3M4GaA3xZyqFKEhNEwku1RfV2t0` | `changes`, one missing-link finding |
| Same Markdown, PNG replaced with text | `3M4Ga5yl69dzukGqtHZziWd0tdO` | `changes`, one unreadable-image finding |

The first task prepared Python **3.14.4** and Pillow **12.0.0** in the Pulse shared
tool cache. Its Python preparation took **1,607 ms**, including a Pillow download
and uv installation using `--link-mode hardlink`. The second task reused the same
environment identity and interpreter in **1 ms**, with no uv command recorded.
All four tasks in the negative checks also reused that environment in **1–2 ms**.
This establishes fresh environment preparation and reuse across separate tasks
and jobs on this worker pool. It does not establish cross-host sharing or actual
hardlink use beyond uv's requested mode.

The missing-image finding named `review/README.md` and `pixel.png`. The corrupt
image finding named `review/pixel.png` and reported that Pillow could not identify
it. These are correctable validation findings, not Python import failures.
The probe jobs finish successfully because they collect results; inspect
`first.status` and `repeat.status`, not only the outer job status.

A separate rejection probe, `3M4GysRkSAFX4WFhyzdoN9lVHuQ`, requested
`Pillow==0.0.0` with the same Python constraint. uv rejected the nonexistent
version during preparation. Its task output was null, the command body did not
execute, and `_c2j/preparation.json` retained the dependency-resolution error and
uv command logs. The outer job caught that expected failure for inspection.

Reproduce the missing-image test by omitting the PNG `--artifact` argument above.
For the corrupt-image test, attach a plain text file under `review/pixel.png`.
Inspect the results and exact task IDs with:

```sh
c2j job result JOB --jobdb http://192.168.1.195:9047/c2 --field '' --output -
c2j job log JOB --jobdb http://192.168.1.195:9047/c2 --json
c2j job artifact JOB --jobdb http://192.168.1.195:9047/c2 \
  --task 'TASK_ID_FROM_LOG' --name error/review-files.log --output -
```

The preparation measurements above were read from the persisted runtime envelopes
of task chapters 4 and 5 in each job. Successful preparation did not produce a
`_c2j/preparation.json` artifact in these runs.

Other checks: all adaptive3 suites passed source validation with the updated c2j;
all ten direct validator tests passed using local preinstalled dependencies. A new
native `corrupt-image` regression case requires a correction with exactly one
finding. Local native execution was blocked before validation by the sandbox's
Nix SQLite database error, including with its alternate Nix launcher. The six
remote task executions above provide actual preparation coverage without changing
or stripping the validator's dependencies.

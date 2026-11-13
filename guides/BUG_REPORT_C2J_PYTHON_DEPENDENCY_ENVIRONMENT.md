# Bug: Python dependency preparation succeeds but the task cannot import Pillow

Owner: c2j. Work type: bug report.

Filed 2026-11-13 against `http://192.168.1.195:9047/c2`:

- Goal: `3M2nxdy26CqBg7b2FzRob6uoeMN`.
- Job: `3M2nxf25SYsee0HnOxsaw94fLpG`.

A task explicitly declares Python and Pillow in its own `execution_needs`.
c2j reports successful preparation, then that same task fails at `import PIL`.
Please determine the supported Python-library declaration and interpreter
contract, fix the violated behavior, and add tests through actual task preparation.

Follow-up: [explicit Python environments](FEATURE_REQUEST_C2J_PYTHON_ENVIRONMENTS.md)
proposes the library/interpreter contract and a uv-backed option. Current `uv:`
declarations install CLI tools; changing the Pillow reference to `uv:Pillow` is
not a replacement for a script-library environment.

## Observed failure

- JobDB: `http://192.168.1.195:9047/c2`.
- Cortex job: `3M28e5T04Yl6CQBKQpa0Or9Tj4M`.
- Goal: `3M28e09e4klaxUOouqJuUiJTg4u`.
- Recipe: recipes commit `47016ffd5aa3a593523973635f547ce0cd473e17`.
- Node: the `review_files` command in adaptive3 validation.
- Original failure: result ordinal 11, 2026-11-13 02:42 UTC. The same command
  subsequently failed in base and c2j consultations, result ordinals 22 and 38.

The declaration on the failing command is:

```yaml
execution_needs:
  packages:
  - nix:github:NixOS/nixpkgs/e7439b6b14ad3cc35d05608ebca9bce01a25f5f8#python3
  - nix:github:NixOS/nixpkgs/e7439b6b14ad3cc35d05608ebca9bce01a25f5f8#python3Packages.pillow
  - nix:github:NixOS/nixpkgs/e7439b6b14ad3cc35d05608ebca9bce01a25f5f8#cmark
```

The retained preparation record lists Python and cmark as `reused`, Pillow as
`prepared`, and native environment preparation as `prepared`. All three packages
are scoped to that exact command. The command then runs `python3` and fails:

```text
ModuleNotFoundError: No module named 'PIL'
```

There is no dependency on another task's installation or shell environment.
The retained package list contains no `uv:` declaration. An installation into uv
followed by execution with a Nix interpreter is therefore a hypothesis to test,
not an established explanation of this particular failure.

## Investigate the contract before choosing the fix

The user believes Python packages may only be supported through uv. Please confirm
that contract and document the correct declaration and invocation for an importable
library such as Pillow. Distinguish Python CLI tools from libraries imported by a
script; installing a tool does not establish which interpreter a script will use.

Check the exact `python3` selected for this task: executable path, version,
`sys.path`, package installation location, and relevant activation variables.
Exercise Nix Python, the supported uv library path, and their combination where
supported. Do not repair one interpreter by accidentally mixing incompatible
site-packages from another.

In the inspected c2j source at `3fec5e455133216ab103a4eb693143e09640742b`,
`pkg/toolenv/native.go` filters out `PYTHONPATH` and `PYTHONNOUSERSITE` when capturing
native activation. This is a candidate cause, not a prescribed solution. The
receiving c2j consultation reported that an explicit import-path probe worked;
verify its actual evidence and the deployed runtime before relying on that result.
The inspected uv implementation uses `uv tool install`; confirm the intended
library-import mechanism rather than assuming a global interpreter can import
any uv-installed package.

## Expected behavior and acceptance

1. State the supported Python package/interpreter contract and the exact working
   declaration/invocation for Pillow. If the recipe uses an unsupported mechanism,
   return the needed recipe correction to the recipes owner.
2. Unsupported or rejected dependency requests fail during preparation with the
   offending reference and actionable reason. They must not be reported as a
   successful setup followed by an unrelated-looking import failure.
3. Supported dependencies are available through their documented interpreter in
   that task. Test interpreter selection and imports together, including mixed
   declarations where supported or an explicit rejection where unsupported.
4. Cover fresh preparation and retained-cache reuse. Correct or invalidate cached
   activation when required. Each task remains independent; no cross-task shell
   changes or ambient package installations are required.
5. Keep the original preparation error visible in the command/task failure and
   its diagnostics. If setup fails, the command body must not execute.
6. Reproduce using real dependency preparation on a supported worker. Do not
   substitute preinstalled Pillow or manually supplied import paths in the
   acceptance test.

The attached minimal recipe prints interpreter identity and import paths before
attempting `import PIL`. It is a proposed reproducer; the recorded production
command and preparation artifacts are the evidence of the observed failure.

Recovery is currently circular: the consultation proposing this fix also runs the
same shared validator and fails before delivery. Avoid repeating that unchanged
route. Use a supported owner execution path for the repair while preserving the
required human decisions and verification. After deployment, the original Cortex
job can rerun its complete validation in a fresh task environment.

## Evidence attached to the submitted job

- `evidence/preparation.json`: original `_c2j/preparation.json`, result ordinal 11.
- `evidence/review-files.log`: original `_c2j/execution/review_files.log` from that task.
- `python-dependency-repro.yaml`: minimal declaration and diagnostic import probe.

Use `c2j job log` to discover the exact task occurrence IDs; ordinals above are
locators, not valid `--task` selectors. Inspect the original job if further evidence
is needed. Do not copy whole histories into the response.

## Subsequent worker probe

The submitted repair job started diagnostic child
`3M2oINy9BiYRlbhD6YhRoX2Ebrk` at 08:19 UTC on 2026-11-13. Its `first` and `reuse`
results both identify Nix Python 3.14.7, report unset `PYTHONPATH` and
`PYTHONNOUSERSITE`, and record `import_ok: false` with `No module named 'PIL'`.
The child succeeded because its diagnostic script caught `ImportError` and exited
zero. This is a real worker reproduction of the import problem, not a passing
acceptance test or a delivered repair. The exact script and output are retained
in its `_c2j/execution/reuse.log`.

# Cortex job blocked by the shared validator

Job: `3M28e5T04Yl6CQBKQpa0Or9Tj4M`  
Goal: `3M28e09e4klaxUOouqJuUiJTg4u`  
JobDB: `http://192.168.1.195:9047/c2`  
Inspected: 2026-11-13. Recipe commit: `47016ffd5aa3a593523973635f547ce0cd473e17`.

The job is awaiting human input in its resolver. It has not implemented the
requested fix for background scrolling during review text navigation.

## What went wrong

The `review_files` command fails at `from PIL import Image`, before checking any
review document. Its command logs report `ModuleNotFoundError: No module named
'PIL'` on three separate executions:

| Result ordinal | Cell | Time (UTC) | Work interrupted |
| --- | --- | --- | --- |
| 11 | cortex | 02:42 | Original direction review |
| 22 | base | 02:56 | Consultation about repairing the validator environment |
| 38 | c2j | 04:10 | Consultation proposing the runtime correction |

The recipe declares Python and Pillow as separate native dependencies. Preparation
succeeded, but the Python interpreter cannot import Pillow. The c2j consultation
reports a successful read-only probe after supplying the missing Python import
path. Independently, current c2j source `3fec5e4`, `pkg/toolenv/native.go`, confirms
that its native environment export filter omits `PYTHONPATH` and
`PYTHONNOUSERSITE`. The activation cache is versioned `native-v2`.

This is an environment activation problem. It is not evidence that Cortex's
proposed UI change or its review document is wrong.

## Why recovery got stuck too

The resolver first sought recipes-owner advice, then base and c2j consultations.
The c2j owner supplied a concrete repair assignment. Before that assignment could
proceed to delivery, consultation validation invoked the same broken Python
command. Recovery therefore depends on the prerequisite it is trying to repair.

The current question asks for approval to deliver and deploy the runtime repair
through an alternative execution path, then rerun validation in this same job.
It is not approval of the scrolling fix. No runtime delivery is recorded in the
inspected sequence.

The human's clarification that the modifier key may be Alt, Control or Command
was incorporated into the proposal. The next continuation still encountered the
validator failure; it did not reject that clarification.

## Required correction and test gap

c2j owns native dependency activation and cache compatibility. The proposed repair
needs the Python environment exports, invalidation of incompatible cached
activation, and a supported worker rollout. After deployment, resume before a
fresh validator execution and rerun the complete stage cycle.

Recipes owns the validator's dependency declaration and its integration tests.
Our disposable local lane substitutes installed dependencies because native Nix
activation cannot run successfully on this host. Those tests establish validator
behavior and recipe routing; they do **not** establish that its shipped dependency
declaration works on a real worker. This job demonstrates that missing coverage.
A release check must run the unmodified validator on a supported worker and check
Pillow import, image decoding, Markdown parsing and the other declared tools.

The resolver should show this concrete blocker and retain the useful consultation
result. Repeatedly requesting the same consultation cannot repair the worker.
Do not weaken image validation or add an internal state file to work around it.
No production job or c2j source was changed during this inspection.

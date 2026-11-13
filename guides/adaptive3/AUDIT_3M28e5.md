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

## Follow-up: why it repeats, and how to break the cycle

Rechecked on 2026-11-13 after the review/Backstop todo implementation
(`38bcd16`). The job still has the same 35 recorded tasks and is waiting on the
question opened at **04:13 UTC**. Its goal remains open. There is no recorded UI
implementation or new repair delivery. It is currently waiting, not actively
burning through another loop.

The concrete sequence was:

1. Cortex produced its scrolling-fix proposal. File validation failed importing
   Pillow before inspecting the files.
2. Recovery submitted a recipes advice job, `3M29fZIRNNsFyTcjTqNwhvEPjuw`.
   It failed because its custom input schema did not accept `title`.
3. Inline consultation then progressed through recipes → c2j → base. Base
   proposed a composed Python package. Validating that proposal failed on Pillow
   too, so the proposal could not complete consultation or become delivery work.
4. The human clarified that the modifier could be Alt, Control or Command. That
   clarification was retained. Continue sent the work back through Direction.
5. Another c2j consultation identified a native activation/cache repair. Its
   proposal again failed the same file validator. Recovery asked for a repair
   through an unspecified “bootstrap path” and stopped at the current question.

The task results contain concrete assignments, but those assignments are proposals.
No task in this sequence delivered them. More advice or another unchanged Continue
cannot make the environment work.

### Two causes, with different owners

**c2j:** preparation reports success, but the declared Python cannot import its
declared library. The separate repair job `3M2nxf25SYsee0HnOxsaw94fLpG`, goal
`3M2nxdy26CqBg7b2FzRob6uoeMN`, already covers this. It is also waiting for human
input, since **08:38 UTC**. Its current question asks for an authorized recipes
advice invocation after a custom foreign include was denied `codex_api_key`.
Its diagnostic children confirmed the failure; their successful collection did
not repair it. The [reuse guide](REUSE.md) now explains that permission boundary.

**Recipes:** `tools.yaml` imports Pillow before looking at any file. The original
proposal and both repair proposals were Markdown-only collections. An image
library failure therefore blocks even the text needed to agree on its repair.
The same validator is used by consultation, so moving the conversation to another
owner repeats the dependency problem.

The old recovery form also linked to an unattached `/tmp/...` file while opening
the scrolling proposal. The committed Backstop changes fix that presentation for
new recipe executions. They do not alter this job's captured `47016ffd` recipe
or fix Python activation.

### Small next recipe change

Move `from PIL import Image` into the existing image-file check in `tools.yaml`.
Keep the declared dependency and all validation checks. Markdown and link checks
would still run on every text review; every image would still require successful
decoding. No stage selection, recovery exception or skipped validation is needed.

I tested this proposed change in a disposable copy with third-party Python
libraries deliberately unavailable:

| Check | Current validator | Proposed import location |
| --- | --- | --- |
| Markdown-only repair proposal | Crashes importing Pillow | Passes file/link validation |
| Proposal with an attached PNG | Crashes importing Pillow | Returns a validation finding naming the PNG and missing Pillow |

This experiment establishes that the small change breaks this particular
dependency cycle. It does not repair worker preparation, and was **not applied
to the production recipe** as part of this audit. Add permanent missing-library
tests for text-only reviews and image-containing reviews, retaining valid/corrupt
image tests and the real-worker preparation check.

Do not generalize this into automatic permission changes or a mechanism that
skips failed checks. An unavailable Python interpreter or Markdown parser could
still require operator intervention; Backstop must keep native human input usable.

### Route to completing the original work

1. Make and deploy the small validator change. Supply the existing c2j repair
   with the recipes advice above; another recipes consultation is unnecessary.
   If its captured recipe cannot reach review, continue that repair goal in a new
   attempt using the corrected recipe and its existing proposal/diagnostics.
2. Finish c2j's activation repair and deploy it to the workers. Verify fresh and
   reused task environments with the [unchanged real-worker check](VALIDATOR_WORKER_CHECK.md).
   A successful diagnostic job alone is insufficient; both validator results must pass.
3. Continue the original Cortex job into a fresh Direction execution. The deployed
   runtime repair can benefit its retained recipe. Preserve the modifier-key
   clarification, rerun the complete validation, then obtain direction approval
   and implement the scrolling fix. Do not resubmit the environment investigation.

The review/Backstop improvements make this easier to understand. The import change
breaks the text-review deadlock; the c2j repair fixes the environment needed for
the eventual UI screenshots. Neither a larger retry budget nor another approval
of the same vague correction would address those causes.

Evidence: exact native task outputs for the original job's agent tasks and review
form, the c2j repair's latest agent output and pending form, both goal states, and
the disposable validator experiment. This follow-up changed no observed job,
approval, permission or runtime.

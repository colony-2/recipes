# Repair approval recovery for long jobs

## Problem and plan

Job `3Lt55O3VBr9T0vr73PveQ7mQvwB` used recipes `75730dd` and correctly
supplied `resume_from: 18f1949f-58d5-4e5d-8fbe-59fdb6c94d83`. Reading the
source's first 100 tasks exceeded c2j's 256 KiB terminal limit. The recipe
mistook that inspection error for missing approval and entered read-only design.
The agent recovered useful files, but its execution request was rejected during
design and the attempt stopped. Its claim that `resume_from` was missing was
incorrect. No implementation or child submission occurred.

This bug fits the recipes cell's responsibility. Fix the inspection helper to
read exact JSON through temporary files for identity, paginated task inventories,
and selected outputs. Keep pagination and original approval/artifact references.
Distinguish a completed inspection that finds no usable approval from an
inspection failure. The former retains normal direction review; the latter stops
with its actual diagnostic instead of starting design or requesting approval.

Test with a real long source history whose first page exceeds the terminal limit
and whose approval is on a later page. Confirm recovery reaches writable
implementation without another direction review. Exercise a missing source job
and preserve the existing revised-direction, scope-change, and sibling recovery
cases. Recheck the real source approval read-only; do not resume observed jobs.

## Assessment

Implemented the planned helper correction in
`recipes/adaptive2/recovery-approval.yaml`. Identity, task pages, human answers,
and review forms now use `--output` with fresh temporary paths. A completed read
that finds no usable approval retains the existing direction-review behavior.
CLI, JSON, timeout, artifact-download, and incomplete-inventory failures stop with
`ADAPTIVE_RECOVERY_INSPECTION_FAILED`; the cause and native command diagnostic are
retained. An active source also stops instead of starting duplicate work. The
read-only assessment and writable implementation boundaries are unchanged.

Validation used pinned c2j **0.0.124**:

- Six cases in `recipe-tests/adaptive2/approved-recovery.test.yaml` passed:
  long history, unavailable source, active source, revised direction, changed
  scope, and preservation of a candidate through a read-only configure hook.
- `recipe-tests/adaptive2/sibling-recovery.test.yaml` passed with actual task
  credentials and a previous sibling's native approval/artifact records.
- All **90** adaptive2 cases passed structural validation. This was validation,
  not another full execution of those cases.
- The long-history fixture creates 105 completed command tasks. It proves the
  first page exceeds 256 KiB and fails without `--output`, and that approval
  occurs after that page. The fixed build reaches implementation and merge with
  only the original direction review and the final outcome review.
- Both the long-history and unavailable-source regressions fail against an
  isolated copy of the old helper. Its captured response reproduces the real
  defect: `valid: false` with the terminal-limit error as the reason.
- Read-only checks with the corrected helper recovered native approvals and
  original one-pagers from Cortex source
  `18f1949f-58d5-4e5d-8fbe-59fdb6c94d83` and assistant source
  `5XivOhnMfQbK9GOtTPDdepv4RXD`.

The plan is complete. No changes to c2j, coordination permissions, or review
requirements were needed. Native tests script model decisions; the resumed
product implementation has not been executed or certified by these checks.
No observed job was restarted, submitted, cancelled, or answered during the fix.

## Continue the Cortex job

The failed job's original submission selects
`git+https://github.com/colony-2/recipes.git//build.yaml@main` and already contains
the correct `resume_from`. After publishing this fix to `main`, restart at the
built-in submission boundary to resolve the updated recipe while preserving
the goal and original inputs. A later execution boundary would retain the old
captured recipe.

```sh
# Retry from the original submission, loading the fixed recipe and retaining
# the existing goal and original Cortex/assistant approval references.
c2j restart 3Lt55O3VBr9T0vr73PveQ7mQvwB \
  --jobdb http://192.168.1.195:9047/c2 \
  --scope c2j:submission --goal continue \
  --request-id cortex-approval-recovery-fix-20261109-1
```

Reuse that request ID if retrying the same CLI request, to avoid duplicate
continuations. This command was not executed during validation.

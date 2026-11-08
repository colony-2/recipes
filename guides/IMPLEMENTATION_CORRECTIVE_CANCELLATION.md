# Corrective cancellation in parent recovery

This recipe-owned fix follows the
[cancellation audit](AUDIT_CANCELLATION_FEEDBACK_2026-11-08.md). The separate
[c2j request](FEATURE_REQUEST_C2J_CANCELLATION_MESSAGES.md) covers exposing the
persisted cancellation message; that runtime change remains outside this work.

## Plan

1. Clarify the agent guidance: use a child's cancellation feedback to revise the
   approach and continue the parent assignment where appropriate. Respect an
   instruction to stop the broader work; do not blindly repeat the cancelled
   approach.
2. Remove the coordinator's blanket exclusion of cancelled attempts from the
   existing explicit `replaces` path. Keep recorded-job validation, cell matching,
   selected handoffs, and reuse of an already active or successful replacement.
3. Test corrected cancellation replacement, no automatic resubmission when
   observing cancellation, message delivery when supplied by c2j, and duplicate
   prevention. Acceptance is recorded in AR-19–AR-21 of the
   [recovery statements](../recipe-tests/adaptive/recovery-statements.md).

No new cancellation classifier, permission flag, or workflow is needed. Agent
judgment selects the next action; the coordinator executes the explicit request.

## Job identities

The recipe reads submitted job IDs from `recipes.run` outputs. In
`coordinate.yaml`, `job_id` is `launch_prerequisite_build.outputs.job_ids[0]`.
Generated references such as `request-21-0` label consultation threads and
documents. They are not job IDs and are not used to assign child-job identities.

## Implementation and validation

Implemented the two planned changes in `prompts.yaml` and `coordinate.yaml`.
The existing `replaces` request now permits cancelled attempts, including a
completed recipe whose assignment outcome is cancelled. Active and successful
replacements are still followed; no new fields, classifier, or worker tasks were
introduced. The process guide and adaptive README describe the same behavior.

The former cancellation fixtures asserted a blanket block even when the parent
explicitly supplied a corrected assignment. They now exercise that correction.
AR-03's existing requirement against automatic retries remains covered by cases
that observe cancellation or repeat an assignment without `replaces`.

Focused validation on c2j v0.0.124, source
`33e2a4de4e99d3a577a38dca4b8de33d43a099ce`:

- The updated native cancellation case failed against the original coordinator,
  then passed after the transition change.
- Native parent recovery: 3 cases passed, including fresh job identity,
  successful corrected execution, retained parent work, and no repeated dispatch.
- Coordination contract: 12 cases passed, including both cancelled runtime
  status and cancelled assignment outcome, feedback-only returns, and following
  an active replacement.
- Child document delivery: 4 cases passed, including readable cancellation
  feedback without final recipe outputs.

The native cancellation case exercises a recipe cancellation failure with real
child submission, workspaces, and results. External cancellation result shapes
are scripted for the recipe tests; they do not establish that c2j now transports
JobDB cancellation messages. That remains the separate runtime request. Tests
establish orchestration and evidence delivery, not an LLM's interpretation of
free-text intent. No observed production job was changed.

Broader adaptive regression: **305 cases passed across 61 suites, zero failed**.
Repository `build.sh`, documentation-link checks, and whitespace checks also passed.

```sh
/tmp/operational-c2j test run --directory recipe-tests/adaptive \
  --parallelism 4 --case-timeout 10m \
  --out-dir /tmp/corrective-cancellation-adaptive-nix
```

The wrapper supplies the pinned c2j binary and the workspace's configured portable
Nix store. The first broad invocation omitted that environment and was stopped
after package setup failures; the configured rerun above completed successfully.

All recipe-owned plan items are complete. The external message-transport request
remains open, and later production observation is needed to assess how agents
interpret cancellation feedback with the updated guidance.

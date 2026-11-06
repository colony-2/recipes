# Parent recovery acceptance statements

Defined before implementation from the [approved plan](../../guides/PROPOSAL_AGENT_AUTONOMY_AND_PARENT_RECOVERY.md).
Paths in the table are relative to `recipes/adaptive/`.
The exact-job and fresh-submission expectations replace the previous goal-wait
and automatic iteration-stop behavior; no compatibility path is retained.

| ID | Importance | Level / dependencies | Files | Expectation |
| --- | --- | --- | --- | --- |
| AR-01 | Critical | Integration / c2j native child lifecycle | `await-child.yaml`, `develop.yaml` | A failed child reaches its parent with the original failure even while its goal remains open. |
| AR-02 | Critical | Integration / native child submission and soft wait | `coordinate.yaml`, `develop.yaml` | Parent correction starts a new job from the normal starting state; successful replacement results satisfy that assignment despite the earlier failure. |
| AR-03 | Critical | Integration / c2j cancellation | `await-child.yaml`, `coordinate.yaml` | Child cancellation is reported distinctly and does not automatically start another execution. |
| AR-04 | High | Integration / c2j child notification | `await-child.yaml`, `coordinate.yaml`, `child-results.yaml` | A failed child reaches the parent while an earlier sibling runs; temporarily deferred monitoring retains pending children. |
| AR-05 | Critical | Integration / native artifacts | `agent-turn.yaml`, `response-repair.yaml` | Correction receives the original relevant evidence bytes without copying incidental output or changing producing identities. |
| AR-06 | High | Integration / native artifacts | `artifact-result.yaml`, `error-documents.yaml`, `child-results.yaml` | Distinct diagnostics survive delivery; summaries identify unsuccessful assignment outcomes even when the execution itself completed. |
| AR-07 | Critical | Integration / native workspaces | `consultation.yaml` | Returning from foreign advice restores the requester's unpublished candidate without fetching it from upstream or substituting the branch tip. |
| AR-08 | High | Integration / scripted model replies, native orchestration | `consultation.yaml`, `coordinate.yaml` | Accepted nested implementation work reaches its serving coordinator without advisory dispatch recursion or repeated registration. |
| AR-09 | High | Integration / scripted model replies, native artifacts | `consultation.yaml`, `response-repair.yaml` | File-only correction preserves substantive agreement and does not request a human acknowledgement. |
| AR-10 | Critical | Integration / package preparation and actual probe | `packages.yaml`, `package-check.yaml` | A failed version probe returns its diagnostic for correction; configuration adoption requires a successful probe of the intended candidate. |
| AR-11 | Critical | Integration / c2j environment scopes | `packages.yaml`, `package-tools.yaml` | Invalid proposed packages cannot prevent the management task from correcting the proposal. |
| AR-12 | High | Integration / configured package policy | `package-policy.yaml`, `packages.yaml` | Policy-approved tooling proceeds without repeated review; an expansion outside that policy reaches the configured decision path. |
| AR-13 | High | Integration / scripted model replies, runtime budgets | `develop.yaml` | Dependency waiting and completed advice do not exhaust implementation turns; exhausted budgets preserve actionable work for the responsible parent. |
| AR-14 | High | Integration / scripted model replies | `develop.yaml`, `resolve-target.yaml` | An invalid consultation ref reaches the requester as its actual resolution error before another repair is attempted. |
| AR-15 | Critical | Integration / c2ops native schema contract | `agent.yaml`, `consultation.yaml` | The full response schemas are accepted natively; invalid annotations are rejected without silently relying on prompt-only output. |
| AR-16 | High | Integration / prompt rendering, scripted replies | `prompts.yaml`, `review.yaml` | An answered consultation returns its result; a genuine unresolved user decision receives a specific question and current decision brief. |
| AR-17 | Critical | Integration / native submission and coordinator re-entry | `coordinate.yaml` | Re-entering after a recorded replacement submission follows that job without launching another; unrelated required children remain tracked. |
| AR-18 | High | Integration / child failure before final outputs | `await-child.yaml`, `coordinate.yaml` | A child without final artifacts can be retried using its available failure and original inputs, without retrieving intermediate outputs or inheriting its session. |

## Coverage boundaries

AR-04 currently covers an already-finished later sibling before waiting. Waking
when that sibling finishes after the wait begins needs c2j support. AR-13 covers
explicit caps, progressing work, and three consecutive unchanged repair turns;
notification after runtime budget termination is a deployment responsibility.
AR-15 uses the actual shared adaptive/creation schemas, deterministic positive and
negative validation, and an explicitly invoked native-provider smoke suite.
See the [assessment](../../guides/ASSESSMENT_AGENT_AUTONOMY_AND_PARENT_RECOVERY.md)
for full implementation evidence and runtime gaps.

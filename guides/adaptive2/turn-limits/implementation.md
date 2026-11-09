# Human replies and accepted handoffs

Implemented against the [approved plan](../PROPOSAL_AUTONOMOUS_TURN_LIMITS.md),
2026-11-09. This addresses recipe behavior observed in job
`7f7199c5c7c08380f4a5fc1e809c476d`; that job was not changed or restarted.

The reported failure came from rejecting unchanged handoff copies, followed by
two unsuccessful correction attempts. Its final message incorrectly combined
response correction with an implementation-turn limit. The optional turn counter
also had a separate bug: human questions and reviews could consume its allowance.

## Changes against the plan

| Planned change | Implementation | Evidence |
| --- | --- | --- |
| Carry the receiver's accepted handoff | The coordinator finds the accepted assignment in consultation history. Matching references pass directly; different references trigger a comparison of the selected files' bytes. Identical copies forward the original receiver references. | Public-build tests create actual receiver and parent artifacts, then submit a real child. |
| Restore originals during correction | Rejected edits are preserved under `error/rejected-handoff/`. The original bindings replace both the normal and correction document maps and the retained output map. | A changed outbox copy is rejected; the next agent sees the original and can select it without writing another file. |
| Keep selected inputs focused | Only selected files from the agreed handoff, plus explicit `recovery/` and `feedback/` files, reach execution. Missing, ambiguous, unknown, and edited assignments have distinct explanations. | Existing focused-handoff and recovery-file tests remain in the suite. |
| Exclude human interaction from turn limits | Positive `max_iterations` now counts autonomous implementation work since the latest distinct collected human response. Questions, review requests, repair turns, and the immediate response to human input are excluded. Zero remains the default. | Repeated questions, direction revisions, and outcome revisions finish with `max_iterations: 1`. Automatic continuation still stops. |
| Recognize actual human progress | Direction, outcome, questions, package decisions, and inline consultation direction supply their existing native input receipts. Request/submission identifiers deduplicate reused responses. Automatic policy decisions do not supply a new receipt. | Native package-decline and saved-decision replay tests; public-build consultation response test; focused receipt replay tests. |
| Renew suspended consultation callers | Nested consultations record the human-response count when suspending the caller. Returning advice renews its round only if a new input receipt was collected. | A nested human answer permits the caller to continue; automatic debate still reaches its limit. |
| Renew operational and Git attempts | Operational correction and repeated-assessment guards now recognize the human-response boundary. Rebase-conflict and merge-chase guards recognize it too, including before an exhausted merge guard rejects another attempt. | Public-build operational-recovery tests and native concurrent-Git-writer tests. |
| Report the actual stop reason | Autonomous work, exhausted response correction, unavailable correction checkpoints, exhausted operational correction, and consultation exchange/depth limits have separate reasons/codes. Response exhaustion includes the unresolved validation message. | Tests assert the actual handoff error and bounded automatic-work behavior; shared failure tests retain their original default code. |

## How the counter works

The recipe derives a count of distinct collected human-review receipts from its
existing state history. A work turn records that count and whether it is the first
turn following new human input. The budget helper reads only phase, assignment,
next action, and these two scalar markers from previous work turns. It does not
copy agent documents or response bodies into the budget inputs.

A new human response renews the allowance. Reading the same response again does
not. The check applies before another autonomous implementation turn; it cannot
stop framing or planning because earlier implementation work used its allowance.
No new human question is introduced to refill a counter.

The two small helper includes evaluate ordinary recipe state and selected
artifacts. They add no model task, event registry, or persistent hash inventory.
File comparison runs only when a selected reference differs from the original;
Python is declared as an execution dependency for that comparison.

## What stayed in place

Receiver-authored scope, separate planning and implementation sessions, focused
artifact selection, package approval/probing, child recovery, verification, and
native Git publication remain in use. Unchanged-diff merge chasing still reuses
human approval. Response correction, unchanged operational failures, automatic
consultation debate, and native Git retry loops remain bounded.

The public `build.yaml` and standalone adaptive2 entrypoint both have the new
`max_iterations` semantics. The previous adaptive implementation remains a
regression fixture with its earlier lifetime counter; it has not been presented
as implementing this policy. The shared failure helper only gains an optional
failure code, with its existing default preserved.

Custom consultation recipes can return `review_receipts` from their actual input
responses to renew their caller's allowance. Existing adaptive2 inline and nested
consultations expose these receipts automatically. Model output must not invent
receipts. Runtime execution/time budgets remain independent of recipe turn limits.

## Assessment

The incident's reference-identity failure is covered through the public build,
including real output normalization and retained correction artifacts. That is
the integration boundary the earlier handoff fixture omitted. Counter coverage
now includes repeated human rounds under a positive allowance, saved-response
replay, nested advice, package decisions, and native Git races.

The implementation stays within recipes; no c2j API change is required. It does
not increase retry limits to hide an unresolved failure. It repairs the handoff
bindings and makes human progress explicit in the existing loops.

**57 native cases pass**, including 48 adaptive2 cases. Test results, commands,
and remaining verification limits are recorded in
[test-results.md](test-results.md). Model decisions and human responses in those
tests are scripted; the tests establish orchestration behavior, not prose quality.

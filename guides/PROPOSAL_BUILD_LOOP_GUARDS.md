# Bound autonomous build loops

Status: investigation and proposal; no loop guards implemented.

The value-artifact migration was committed separately as `5274e14`. This work fits
the recipes cell for workflow policy, counters, escalation, and regression tests.
Generic engine limits and shared budgets across child jobs belong to c2j.

## What the job demonstrates

Without the context transport failure, the recorded job could have continued
recovering, but the export cannot establish that it would have run forever.
There is no parent-level liveness guarantee in the current build recipes.
Bounded individual consultations do not bound the number of fresh consultations
or the number of development/recovery cycles.

Current protections:

- [Consultation](../recipes/kernel/consultation.yaml) bounds each round, defaulting
  to four consultant iterations. Fresh thread keys get fresh budgets.
- [Result repair](../recipes/kernel/repair.yaml) allows two automatic corrections
  before human direction. This is a local correction budget, not a build budget.
- Heavy and light builds allow three upstream merge chases.
- Coordination avoids launching an already-recorded prerequisite job under the
  same key and skips already-recorded consultation requests.

Current gaps found by source inspection:

1. Heavy/light `record -> work` accepts `next: continue` without an overall limit.
2. [Coordination](../recipes/develop/coordinate.yaml) can skip a repeated request
   or a wait on an already-terminal dependency. Its caller still announces
   “Coordination state changed” and returns to the agent, even if nothing changed.
3. A new expert thread key permits another bounded consultation about the same
   unresolved dependency. Thread-key deduplication does not bound recovery.
4. A required `before_design` specialist returning `agreed` + `revise` causes
   `design_context -> design_next -> design_context`. The developer does not run
   between checks. Each visit increments the specialist round and creates a
   fresh thread. A persistent adverse finding can therefore repeat indefinitely.
   See [development routing](../recipes/develop/develop.yaml) and
   [specialist routing](../recipes/build/hooks/specialists.yaml).
5. Schema-valid responses reset the development `repair_attempts` field. Rejected
   response paths preserve the prior count where wired, but alternating valid
   actions and errors cannot be bounded by this local repair counter alone.

The historical consultation-to-execution handoff defect is already fixed in
`111d099`. We still need containment for the next defect, including fresh-thread
recovery chains that all return syntactically valid results.

## Options

| Option | What it catches | Limitations / ownership |
| --- | --- | --- |
| Correct no-op and adverse-result routing | Known repeated waits and assessments without a correction opportunity | Necessary recipe fixes; cannot anticipate every future cycle |
| Detect repeated state without progress | Repeated `continue`, terminal waits, A-B-A cycles, repeated failed gates | Recipe policy; progress classification can have false positives or be fooled |
| Bound recovery for each unresolved target | Repeated consultation about the same child failure under new thread keys | Needs stable target identity and explicit recovery association |
| Cap autonomous work between human checkpoints | Bounds repeated activity even when every turn produces new prose or keys | Must cover all re-entry paths; may interrupt legitimate long work |
| Set an enclosing timeout | Limits elapsed duration of an autonomous scope using existing c2j support | Existing timeouts include suspended waiting; a short whole-build timeout penalizes human/child waits |
| Engine-level transition/work budget | Catches loops even when a recipe omits its guard, including operation-free state cycles | c2j capability proposal; cross-job accounting needs controller enforcement |
| Ask an LLM whether progress is happening | Can recognize semantic repetition and explain a stall | Useful diagnostic only; it must not be able to waive hard limits |

## Recommended recipe policy

Use the first four options together. They solve different problems. A hard bound
is what guarantees finite autonomous work; progress heuristics provide earlier,
more useful intervention.

### 1. Correct the known routes

Return explicit coordination effects (`changed`, newly launched jobs, newly
observed child outcomes, and skipped requests). Do not manufacture a changed-state
message. If requested dependencies are still running, use the existing durable
wait path. Repeated requests concerning terminal dependencies need correction or
human direction rather than another unchanged wait/agent cycle.

A failed required before-design assessment must lead to a specific correction
opportunity or human direction. It must not immediately launch another fresh
assessment of the same unresolved condition. Preserve the requirement to pass
that gate before advancing beyond it.

### 2. Track evidence of progress, with conservative rules

Maintain a small, durable progress record based on recipe-observed facts:

- Repository content/candidate changes, ignoring metadata-only commit changes.
- Content changes to designated design/test/implementation deliverables.
- A prerequisite advancing in execution or producing a new authoritative result.
- Acceptance of a previously unresolved gate against the relevant candidate.
- Explicit human direction/approval recorded by the input operation.

Transcript growth, new artifact handles, timestamps, session IDs, renamed thread
keys, repeated summaries, and another expert agreeing that recovery is needed do
not by themselves resolve a failed dependency. Avoid hashing the entire context:
its bookkeeping and transcripts change on every cycle.

Different phases need different progress rules. A changed design document can
justify further design work, but cannot reset the recovery count for an unchanged
failed child job. Track visits to normalized checkpoint signatures, so cycling
between two states does not evade a consecutive-identical-state detector.
Progress detection is an early warning, not permission for unlimited execution.

### 3. Attach recovery to a stable unresolved target

Recovery consultation requests should identify the dependency or gate they are
trying to resolve. The recipe validates that association against its ledger.
For child recovery, key accounting by the existing child job and failure/result
revision; for repeated specialist assessments, use the checkpoint, configured
specialist identity, and relevant candidate/evidence revision. A new consultation
thread key must not grant a fresh recovery allowance.

Proposed starting policy: **two automatic recovery rounds per unchanged target**.
A round may collect several distinct experts, with an independently bounded batch;
it does not grant another round merely because those experts agreed on the failure.
After the allowance is exhausted, preserve evidence and ask for human direction.
Do not invent a parent-side ability to resume or repair another job: actual recovery
must use supported operations and the owning workflow.

### 4. Give every autonomous segment a finite allowance

Proposed initial controls, subject to tuning:

- Escalate after **three repeated checkpoint visits without qualifying progress**.
- Escalate after **two recovery rounds for the same unchanged target**.
- An outer **autonomous-cycle allowance**, initially **64**, charged at guarded
  work/assessment/recovery re-entry points, including `design_context` and hooks.
  Charging only development-agent turns misses the specialist loop above.

These are policy starting points, not limits inferred from the current job.
The number of experts/consultations admitted in one cycle must also be finite and
explicitly bounded; the existing 40-inline threshold is an execution choice, not
a work budget. Decide that separate batch limit during implementation. Existing
per-consultation and repair limits remain in force inside a charged cycle.

The outer allowance never resets just because state changed, a phase was renamed,
a new thread was opened, or the job switched from light to heavy. Each permitted
automatic cycle must reach another guard, terminate, or wait for external input.
Audit all paths, especially specialist, prepare, verification, redesign, and
response-repair loops. An unguarded cycle invalidates the guarantee.

Keep the ledger in durable recipe state and forward it explicitly on light-to-heavy
handoff. Use logical action identities so completed-action replay does not charge
again; actual additional attempts still need a bounded retry policy. Plain waits
and replay consume no new autonomous-cycle allowance. Waiting must not be polled
through repeated agent calls.

At a limit, route to a human-input state that keeps the primary job open and
preserves its candidate, sessions, children, and evidence. Offer cancel, or grant
a bounded extension with direction. There is no automatic extension and no
approval of the work implicit in extending a budget. Keep cumulative usage;
a human grant adds an explicit allowance rather than erasing history.

## Engine backstop

Inspected c2j revision `393531b2f402f3b6007256c262e0ddefbc3bded1`, specifically
`pkg/recipe/node.go`, `pkg/worker/compiler/execution_scope.go`,
`statemachine_compiler.go`, and `timeout_recovery_test.go`. It exposes `timeout`
on node metadata and wires it into a scope's total deadline. Its timeout recovery tests explicitly retain the deadline
across suspended external-input waits. These build state machines do not currently
set an enclosing timeout. I found no authored transition-count limit in the
inspected node metadata or state-machine compiler.

A c2j transition/work budget would complement recipe policy: count durable logical
state entries or admitted actions, survive replay and retries, and provide an
uncatchable final resource ceiling even if a recipe's recovery handler loops.
A soft threshold could be handled by the recipe to request direction; the hard
ceiling must not be reset by catching its own exhaustion error. Extending it
requires an explicit controller-authorized grant.

A per-job cap does not bound a recursively spawning job tree. A shared parent/child
budget requires c2j enforcement and propagation through `recipes.run`, including
custom recipes. Recipe inputs alone cannot guarantee that arbitrary children honor
such a budget. This is a separate owner-level capability, not a prerequisite for
adding the recipe guards above.

## Regression cases to define before implementation

- Repeated `continue` eventually asks for direction despite changing summary prose.
- Repeated terminal waits do not invoke the developer indefinitely.
- New thread keys about an unchanged failed child share one recovery allowance.
- Persistent before-design `revise` findings cannot endlessly rerun specialists.
- Phase cycling and light-to-heavy escalation preserve cumulative allowances.
- New transcript/artifact identities do not count as completed dependency work.
- Real design/candidate/child progress avoids premature no-progress escalation.
- A finite series of real changes still reaches the outer autonomous-cycle limit.
- Suspended child/human waits do not spend active-cycle allowance.
- Replay preserves counts without double-charging completed logical actions.
- Human direction grants only the recorded extension and never approves work.
- Guard exhaustion preserves the candidate and keeps the ticket open for direction.

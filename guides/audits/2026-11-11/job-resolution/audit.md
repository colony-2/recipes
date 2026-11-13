# Job review: repeated verification denial ends in agent-declared failure

Observed 2026-11-11 through `http://192.168.1.195:9047/c2`.
Requested job: `3LwPwP9yqfLtuYXFWVz7G4JopWa`, cell `c2j`.

## Finding

Yes: this job has the same terminal routing problem as the earlier
`cortex-assistant` job `3LwJYdNiGWMsmXRiSZpBSTKsk1G`. The final working agent
returned `next: fail`, and the recipe immediately ran `stop_attempt`, producing
`COMPLETED / failed_app`. No human decision addressed the final blocker.

The underlying issue differs. Here, actual platform child submissions returned
`lease permission denied`; this is not the completed-goal test from the earlier
job. Five in-job verification passes each recorded two `start_failed` children
with empty job IDs and no platform artifacts. These are ten denied launch records,
not ten failed platform executions or ten independent root causes.

## What led to termination

| UTC time | Recorded event |
| --- | --- |
| 01:59:54 | Job created for changing local verification to collect macOS 26 and Ubuntu child results. |
| 02:02:38 | Human approved the proposed direction without additional feedback. |
| 02:26–02:35 | Agent repeatedly returned `review`, reporting TS-01–TS-14 source checks passing and TS-15 runtime integration deferred. |
| 02:28:12, 02:31:07, 02:32:34, 02:34:22, 02:35:35 | Verification child-group outputs each recorded the same two permission-denied launches. First two passes used candidate `0cee9b3064ea6261a4179fe99aba59b40f0b7325`; last three used `ef043a5f57b74f01db032ac0bd8092c6e887fd0a`. |
| 02:35:43 | Working turn began that returned `blocked`, without a package request or human question. |
| 02:36:32 | Recovery turn began in the resumed implementation session. It returned `fail`, stating there was no changed capability or useful correction. |
| 02:37:25 | `operational_failure/stop_attempt` began and deliberately failed the job. |

The final agent's public message was: “I’ll return `fail` as instructed, retaining
the implementation, passing source evidence, and exact permission failure for the
parent.” Its final response contains `next: fail`, with no questions or requests.
The full task identities and selected output fields are in [inventory.md](inventory.md).

The captured recipe revision is `d102ce6ce65ac9d2735f538c8816f696aa37f3ab`.
At that revision, `blocked` without packages or pending work routes to recovery;
`fail` routes directly to operational failure. The observed ending is the explicit
agent-failure route, not an exhausted-allowance decision or a human stop.

## A scope inconsistency also needs resolution

The human-approved one-pager says actual two-platform execution remains
implementation acceptance work, and that missing submission permission must yield
a clear failed verification. The later execution handoff and formal statements
instead designate TS-01–TS-14 as source acceptance and TS-15 as later deployment
integration, explicitly not a prerequisite for source acceptance.

The executable verification gate still requires both platforms. Returning `review`
therefore runs the same gate again. No human receipt after direction approval was
found in the 94-task inventory; the later source-only boundary must not be treated
as a separately verified human waiver. An auditor should reconcile these records
with the human rather than silently bypass the gate or repeat it unchanged.

The agent's report of passing source checks is retained evidence, not an independent
certification by this audit. The actual platform verdict correctly remains failed.

## Permission evidence and ownership

The retained policy record for `.c2/recipes/hooks/build/verify.yaml` has a secret
resolution grant and an empty `jobdb.jobs` object. Actual launch outputs establish
the denial. This is consistent with the agent's missing-submission-grant diagnosis,
but this audit did not exercise policy administration or prove that one specific
configuration edit is sufficient under every applicable permission ceiling.

- Recipes owns the repeated review/verification/recovery routing and the terminal
  response to a resolvable blocker.
- The c2j cell owns its local verification hook, implementation and acceptance
  documents.
- The deployment/JobDB configuration owner controls the effective submission grant;
  compatible executors also remain unverified because neither child launched.

The existing November 9 allowance-escalation fix is included in this newer recipe.
It did not remove the explicit agent `fail` route or reconcile this verification
gate with the assignment. This is a gap in coverage, not evidence that the job ran
a recipe from before that fix.

## What the proposed resolution flow would change

It would preserve this job and inspect the first established external blocker
instead of repeatedly sending it through source review and the unchanged gate.
A fresh session would present concrete choices, such as arranging the required
permission through its owner and then rerunning verification, or revisiting the
acceptance boundary and its enforced gate. Any acceptance change needs an explicit
decision; permission denial must not be relabeled as successful verification.

See [the proposal](../../../adaptive2/PROPOSAL_JOB_RESOLUTION.md).

## Coverage and limits

One newly requested job was inspected: all 94 task inventory entries, selected
exact outputs, five verification child-group outcomes, the approval receipt,
working responses, and selected artifacts. The earlier requested assistant job
is comparison context, not an additional newly sampled job. Retained artifacts
mention two live probes, but their separate job histories were not re-audited here.
No parent outcome or later replacement outcome is inferred.

The initial attempt to retrieve `request.md` from the final working task returned
“artifact not found in the selected job/task”; the original request was successfully
retrieved from an earlier working task. No required evidence remains unavailable
for the terminal-routing finding.

Raw records and downloads remain in `/tmp/job-audit-3LwPwP` and
`/tmp/job-audit-3LwPwP-log.json`. Selected evidence and producer references are
retained with this audit. No tests were rerun, permissions changed, reviews answered,
jobs restarted, or recipe code edited.

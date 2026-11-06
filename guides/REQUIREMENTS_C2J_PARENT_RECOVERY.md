# Remaining runtime requirements for parent recovery

Owner: c2j for recipe/runtime APIs; worker provisioners for resource fulfillment.
Evidence baseline: main `089061be7a21`, inspected and exercised on 2026-11-06.
These requests supplement the implemented fresh-submission recovery flow. They do
not require job restart or intermediate-result retrieval.

## Wake when any tracked child completes

The recipe can inspect every tracked job with `recipe.await_result_soft` and
`return_when: current_status`. This delivers an already-failed sibling before
waiting. If all jobs are pending, the current terminal wait targets one job. A
later sibling failure cannot wake that wait.

Provide a native durable operation with roughly this shape (illustrative API):

```yaml
op: recipe.await_any_result_soft
inputs:
  targets:
    - {job: first-job}
    - {job: second-job}
  wait: {on: job, condition: complete}
```

Return terminal envelopes for ready jobs plus the remaining targets. Preserve the
existing exact-job failure/status/artifact contract, including cancellation and
failures before recipe outputs exist. Subscribe before/atomically with the status
scan so a completion cannot be lost. Register JobDB dependencies and release the
worker while waiting; no polling command or administrative token should be needed.
Do not require goal success or cancel unrelated siblings.

Acceptance: first child stays running, second fails after both were scanned, and
the parent wakes with the second failure while still tracking the first.

## Apply approved resource/capability requests as execution requirements

c2j already exposes task execution requirements and an `environment_required`
handoff. The runtime does not itself provision machines. The missing recipe-facing
piece is accepting a typed, dynamically approved requirement value for the next
execution or validation job. In this baseline, scalar fields can be templated,
but capability/package lists are literal strings normalized during recipe loading;
the whole resources mapping cannot be supplied as a typed template value.

Allow a recipe to pass a validated requirement object to a new task/job, for example:

```yaml
execution_needs: ${{ sequence.environment_policy.outputs.requirements }}
```

An equivalent explicit submission input is also suitable. Resolve values before
requirement validation and execution selection. Inherited ceilings and policy
restrictions must remain enforced by the runtime; an agent's requested value is
not an approval. The recipe needs to receive an actionable refusal or suspended
status, the concrete unmet requirements, and eventual fulfillment/failure. It must
be able to keep the management/recovery task runnable in its existing environment.

Expected recipe flow after support exists:

1. Agent requests concrete resources/capabilities and explains the failed operation.
2. Cell/operator policy accepts bounded requests or asks for one focused decision.
3. Only after that decision, submit an isolated validation job with the approved
   requirements and candidate cell configuration.
4. Let the provisioner satisfy the requirement handoff. Confirm the actual requested
   capability with a bounded probe; an echo alone does not prove Docker works.
5. Adopt the persistent `.c2/config` change only after successful validation. If the
   next work needs a new worker, submit a fresh job with the validated configuration
   and ordinary starting inputs. Return any failure to the parent.

Acceptance: policy-approved memory/Docker needs reach the provisioner, denied
expansion runs no probe, preparation failure leaves management usable, and a
successful probe permits persistent adoption without a second approval for the
same request.

Current recipe behavior: packages already use policy → isolated validation job →
conditional adoption. Memory/Docker requests are explicit unmet needs returned to
the parent/execution owner; no automatic provisioning or generic environment
approval loop is claimed. Root-level notification still belongs to the deployment.

## Preserve cancellation classification in soft results

A native recipe cancellation currently returns `status: failed` and
`failure_kind: task_error` from `recipe.await_result_soft`, even though
`outputs.attrs.c2j_failure.kind` is `cancellation`. Preserve that structured
classification at the soft-result boundary so callers can directly distinguish it
from repairable execution failure. The current coordinator checks the original
envelope and never automatically replaces this cancelled work. Its regression
fixture is `native-cancelled-child-is-not-replaced`.

## Separate future work

Task-level output inspection and selected intermediate-artifact reuse remain in
[the future recovery proposal](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md).
Fresh recovery works without those APIs. Private Git/module transport and package
installer defects still belong to their respective runtime/tool owners.

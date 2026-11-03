# Feature request: effective capabilities in c2j self

Status: implemented upstream; retained as historical rationale. The authoritative
contract is the [current self documentation](https://github.com/colony-2/c2j/blob/main/README.md#c2j-self).
Validated runtime baseline: f1a153b898c5. It reports permission and availability
separately, last-known lease state, and inherited child restrictions. The original
schema sketches and child-policy assumptions below are superseded by that contract.
Date: 2026-11-03.
Owner: c2j CLI and runtime authorization integration.

## Outcome

An agent running a task can ask `c2j self` what c2j actions its current authority
allows, with applicable limits and useful reasons for denial. It can decide
whether an assigned action is executable without guessing from prompt prohibitions,
examining credentials, or submitting a real job as a permission test.

Keep existing cell information. Add a concise capability summary and an additive
machine-readable representation under `c2j self --json`. Match the effective
runtime permission checker, including attenuation and enclosing limits. In an
embedded runtime, report effective permissions even when no bearer token exists.

This request partially fits the recipes cell: agent guidance and task scope belong
to recipes; CLI discovery and authoritative permission evaluation belong to c2j.
Any op-launcher capability gap belongs to c2ops. See the
[agent proposal](PROPOSAL_STANDARD_AGENT_INBOX.md).

## Context

The inspected `self --help` documents resolved current-cell information; it does
not document an effective permission summary. That observation is not a claim
that every existing self field has been inspected or that the underlying runtime
lacks the relevant authorization metadata.

The [node permission guide](https://github.com/colony-2/c2j/blob/main/GUIDE-Node-Permissions.md)
distinguishes supplied secret inputs from delegated authority. It describes
restricted task grants and ceilings, tenant-scoped submission, child policy that
is independently determined, and embedded per-call checks. The new CLI output
should explain these effective capabilities without revealing credential values.

Task instructions and runtime capabilities answer different questions:

- The task authorizes a concrete activity: for example, submit an agreed job to
  the reporting cell and let the workflow consume its automatic child-job outputs.
- c2j authorizes an operation under current authority: submission may be granted,
  denied, expired, or unverifiable.

Both must permit the action. A broad submit capability is not an instruction to
start arbitrary work; a task instruction cannot elevate a denied runtime grant.

## Proposed human output

Illustrative output, not existing CLI behavior:

```text
Cell: github.com/example/orders
Task: implement_export
Authority: delegated task permissions

Job submission: allowed within the current tenant
Target restriction: no additional cell restriction reported by this permission
Job lifecycle changes: denied by current task grant
Secret retrieval: limited to granted names (values are never displayed)
Validity: limited by the current task's live authority

Submission creates a job; it does not establish completion.
Child jobs use their own recipe policy.
Follow the current task's instructions for which work to submit.
```

Only show a target restriction, deadline, named resource scope, or explanation
that the authorization layer actually supplies. Where authority expires at a
known time, display it; otherwise explain the live-task condition rather than
inventing a deadline. For permission categories with mixed per-resource decisions,
show “restricted” and the known scope, not a misleading global yes/no.

Do not assert that all job reads or waits are allowed just because submission is
allowed. Report such actions only when their effective permissions can be
established. Existing dependency-cell listings remain separate from authorization.

## Required semantics

1. Use the active task's effective authority and the same authorization logic as
   the real operation. Do not infer permission from environment variable presence,
   copied YAML, owner credentials, or a decoded bearer token alone.
2. Distinguish allowed, denied, restricted, and unknown/unavailable. A failed
   discovery request is not proof of denial or permission. Include a concise
   reason when the runtime provides one.
3. Preserve resource constraints and relevant tenant/task boundaries. An allowed
   summary may still require a target-specific check. Do not invent finer scopes
   than the runtime enforces.
4. Include safe capability metadata, never token strings, secret values, signing
   material, or the owner's credentials. Resource names should be shown only to
   the extent the current caller is permitted to learn them.
5. Refresh from current authority on invocation. Real operations remain authorized
   at execution time; a prior self result is not a reservation or permission grant.
6. Work under restrictive task scopes. Capability introspection must not require
   broader rights than the task possesses or fall back to an owner identity.
7. Outside a task, identify the current authority source or say task capabilities
   are unavailable. Do not silently describe an unrelated owner's capabilities.
8. Preserve existing self output fields and --json compatibility. Add a versioned
   capabilities object using the runtime's existing action names; owners should
   finalize its schema rather than introducing a separate policy language.

The first useful capability is child-job submission, but the design should expose
other supported delegated operations consistently. Do not add fictional commands
or flags to the agent instructions before discovery is implemented.

## Optional target-specific check

If a summary cannot answer whether a specific submission is permitted, expose a
read-only permission check for the proposed action and target, using the same
checker as submit. A possible future syntax is `c2j can submit --cell ...`, but
this request does not require that spelling or a new command for its first phase.

The check must create no job, execute no recipe, and grant no extra authority.
It assesses permission only; it cannot guarantee recipe validity, tool availability,
network success, or future authorization. An agent should use a preflight where
available and still handle an actual submission denial normally.

## Agent guidance enabled by this feature

```text
Use c2j self for your cell and current c2j capabilities. Use c2j cells to discover
allowed dependent cells, and c2j submit --help for installed submission options.
You may submit jobs to other cells when the task authorizes the work and your
current capabilities permit it. Child submissions are automatically included in
the task's special outputs; do not duplicate their IDs in your response. Follow
the task's instructions for waiting and reporting results.
If capability information is unavailable or an operation is denied, report the
required intervention; do not substitute another credential or invent authority.
```

The runtime already includes child submissions in special task output fields.
The agent-turn wrapper forwards jobs, including job_ids consumed by the adaptive
flow. This feature does not request a new tracking or handoff mechanism. Recipes
should consume those existing outputs when submission is task-authorized instead
of rejecting every nonempty list. Waiting and completion policy remain recipe
choices; capability introspection does not change those choices.

## Acceptance statements

Resolve exact CLI/runtime source filenames in the c2j cell before implementation.
The files listed here identify the consuming documentation contracts.

| ID | Expectation | Contract files | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| SC-01 | Task capability output reflects effective grants after enclosing limits and attenuation. | guides/C2J_USER_GUIDE.md | Critical | Integration / c2j authorization fixtures |
| SC-02 | Allowed, denied, restricted, and unavailable authority remain distinguishable without attempting real submissions. | guides/C2J_USER_GUIDE.md | Critical | Integration / c2j authorization fixtures |
| SC-03 | Capability output reveals no credential values and never falls back to a broader identity. | guides/C2J_USER_GUIDE.md | Critical | Integration / restricted-task fixtures |
| SC-04 | Embedded and delegated execution report equivalent effective permissions without requiring a bearer token. | guides/C2J_USER_GUIDE.md | Critical | Integration / embedded and delegated runtimes |
| SC-05 | Dependency discovery is not presented as permission to submit, and child policy inheritance is described accurately. | guides/C2J_USER_GUIDE.md | High | Integration / CLI output fixtures |
| SC-06 | Permission changes or expiry remain enforced at submission even after an earlier allowed summary. | guides/C2J_USER_GUIDE.md | Critical | Integration / permission lifecycle fixtures |
| SC-07 | Existing self JSON fields remain compatible when capability information is added. | guides/C2J_USER_GUIDE.md | High | Integration / CLI compatibility fixtures |

# Agent autonomy and parent recovery: implementation assessment

Implementation date: 2026-11-06. Scope: shared adaptive recipes, their tests,
examples, and guidance. This follows
[the approved plan](PROPOSAL_AGENT_AUTONOMY_AND_PARENT_RECOVERY.md).
Recipes owns these changes; c2j and worker provisioners own the remaining runtime
capabilities identified below. No production jobs were resubmitted or restarted.

## What changed versus the plan

| Planned step | Implemented behavior | Assessment |
| --- | --- | --- |
| 1. Operating context and native schemas | Shared prompts explain the job/cell, persistence, directories, task connection/routes, ordinary debugging, and concrete requests. Full response schemas have typed metadata, required nullable optional fields, and boundary normalization. | Implemented and exercised against the live provider with fallback disabled. |
| 2. Exact-child results | `await-child.yaml` replaces goal-only waiting in coordination, package checks, creation, custom consultations, and direct validation collection. Native job IDs drive control flow. Old goal helpers were removed. | Implemented. A failed execution reaches its parent while its goal remains OPEN. |
| 3. Evidence and workspace recovery | Repair receives the previous response and relevant original bytes, including referenced directory subtrees. Child summaries and produced files have separate paths. Requesters return to their managed candidate after foreign advice. | Implemented with materialized-inbox and changed-workspace tests. |
| 4. Consultation handoff | `answered` ends factual advice. `consult` requests obtain advice inline; `execute` requests return work to the enclosing coordinator. Nested acceptance exports its actual owner and usable agreement. Invalid refs return resolution errors. | Implemented. Existing arbitrary custom consultation selectors still use their explicit child path; their waiting now follows exact jobs. |
| 5. Fresh parent-driven attempts | An execution request with corrected instructions can replace a failed or semantically incomplete child under its existing agreement. New jobs start from the normal configured ref with original agreement inputs; replacements satisfy only their own assignment. | Implemented. No restart, intermediate-output retrieval, unpublished child checkout, or child session reuse. Any-child wakeup remains external. |
| 6. Packages, requirements, and review | Cell package-policy hook, isolated candidate validation, conditional adoption, original failure delivery, and corrected fresh probes. Review/test prompts keep checks proportional and questions specific. | Packages and prompt changes implemented. Dynamic memory/Docker requirement adoption remains blocked on c2j/provisioner integration. |
| 7. Progress limits and documentation | Default fixed turn cap removed. Explicit caps count substantive implementation turns. Repeated unchanged blockers get three correction turns before an actionable handoff. Process and authoring guidance updated. | Implemented. Runtime execution/time budgets remain the overall bound. Root-owner notification remains a deployment responsibility. |

## Parent recovery contract

The parent receives a failed child's exact job result, original failure envelope,
and available exported final artifacts. A failure before final outputs is valid
input to recovery; the recipe does not invent missing evidence or fetch chapters.
It resumes the working agent with `error/`, `results/`, and `feedback/`.

For another attempt, the agent returns an ordinary execution request:

```yaml
next: coordinate
requests:
  - action: execute
    agreement: <reference from the accepted consultation>
    request: Use the corrected probe. Investigate the reported failure before continuing.
```

The coordinator reuses the accepted assignment, target cell/ref, recipe, and
agreement documents, appends the correction, and records the new native job ID and
which execution it replaces. Re-entry follows that recorded execution. A previous
failure no longer permanently blocks the assignment after its replacement succeeds;
unrelated required work remains tracked. Corrections to package probe arguments
change actual argv inputs through the package proposal, rather than only prose.

Active and successful submissions are reused. Cancellation never automatically
creates another execution. The native cancellation test revealed that c2j may expose
`status: failed` / `failure_kind: task_error` while its original structured failure
has `kind: cancellation`. The coordinator respects that structured cause and retains
the original result unchanged. It does not infer cancellation from error text.

The fresh-attempt test creates unpublished files in a child before failing its next
command. Its replacement proves those files and the parent's unpublished files are
absent from the new checkout. The parent's own candidate remains intact, including when the child targets the same
cell. A repeated
execution request after success proves no third child is created.

## Files, responses, and consultations

- Child status: `results/<job>/status.md`; exported child files:
  `results/<job>/artifacts/`; failures: `error/children/<job>/`.
- Summaries distinguish execution completion from assignment failure, and include a
  bounded outcome summary. Original failure envelopes and diagnostic files remain
  available. Temporarily deferring monitoring during design or response repair
  retains the pending job list for the next implementation turn.
- Consultation evidence: `coordination/<reference>/artifacts/`; generated status:
  `coordination/<reference>/status.md`. Binding metadata alongside the original
  documents preserves identity and annotation links through the prefix change.
- Response repair binds only matched files, relevant candidate matches, and referenced
  directory subtrees. Unrelated downloads stay on their producer. Original stored
  references and bytes survive; repair can return an unchanged bound document.
- Returning from foreign advice inherits the requester's managed workspace, rather
  than creating a checkout at an unpublished SHA. Advisory experiment changes remain
  discarded. Missing optional requester checkpoints are omitted from the public
  include input instead of being passed as `{}`.
- Shared and nested consultations stay inline. Factual answers finish immediately;
  accepted nested scopes and execution needs return to the coordinator without a
  second registration/acknowledgement dialogue. Failed advice returns its actual cause
  for correction rather than terminating the parent automatically.

## Native schema correction

The live test first reproduced provider rejection after fixing metadata types:
`schema.required` must include every property. Merely replacing `{}` types did not
solve the contract. `response-schemas.yaml` now holds the adaptive and creation response
schemas as an empty include, adding no worker task. Optional fields are required on
the provider wire and allow `null`; the agent boundary removes null optional fields
before existing routing and artifact processing. Native operation responses remain
available on their producing task. The creation review uses the same schema include;
the kernel agent boundary used by creation also normalizes nullable metadata. Older
light/develop/kernel-consultation schema definitions are outside this adaptive-flow
change and were not represented as having passed the native provider check.

The live smoke uses the authored c2ops Codex selector, zero repair attempts, and
asserts `schema_mode: native`, completed status, and valid output. Agent, inspection,
consultant, requester-cancellation, and creation shapes passed. Deterministic cases validate
real exported schemas with JSON Schema, including invalid metadata, package requests,
corrected execution requests, and specific human questions. Routing mocks remain
useful, but are not counted as provider acceptance evidence.

## Environment requests and review

The cell can supply `.c2/recipes/hooks/build/package-policy.yaml` returning exact
reference/probe pairs. The default approves nothing. Policy is read in a fresh workspace at the cell’s
normal ref, so an unreviewed candidate cannot grant itself approval by editing the
policy hook; that candidate remains available for normal review and merge. The
[example](../examples/build-hooks/package-policy.yaml) shows `go version` and
`ruff --version`. A corrected probe can use an explicitly configured policy;
changing the request does not silently inherit an old human approval.

Validation runs on a separate proposed configuration. The parent adopts only a
successful matching digest and only if its own configuration still matches the
approved base. Tests run actual probes and intentionally invalid package setup,
showing that failures leave parent management usable. The corrected candidate is
then validated and adopted without another review when exact policy covers it.

Prompts distinguish project libraries from persistent worker tools, describe denied
operations as actionable feedback, and ask for precise resource/capability needs.
They do not ask the agent to decide its authority repeatedly. Tests and reviews keep
formal expectations, allow corrected commands for equivalent evidence, and avoid
turning optional worker identity metadata into new acceptance requirements. Human
questions require a current decision brief and a concrete choice or missing fact.

## Remaining gaps and explicit limits

1. **Any-child wakeup (AR-04, partial).** All tracked statuses are inspected first,
   so an already-failed later sibling is returned while an earlier one remains
   pending. If all are pending, only one native terminal wait is available. Prompt
   notification of a later sibling failure needs a native durable wait-any operation.
2. **Memory/Docker provisioning (step 6, partial).** c2j exposes execution needs and
   an environment handoff, but cannot yet accept the dynamically approved typed
   requirement object needed for this recipe loop. Agents return the precise unmet
   need; no automatic resource approval, reprovisioning, or persistent adoption is
   claimed. Packages are fully wired through their existing separate-child boundary.
3. **Root supervision and runtime budgets.** Runtime limits and cancellation still
   apply; root-owner notification and provisioner fulfillment require deployment
   services. Recipes cannot guarantee a final agent turn after the runtime kills a job.
4. **Custom selector interface.** Arbitrary custom consultation recipe selectors keep
   their existing child execution interface. The shared/nested driver is inline; a
   broader conversion of custom selectors to inline hooks was not introduced here.
5. **Intermediate child recovery remains deferred by design.** See the
   [separate proposal](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md). New attempts
   start again with available original inputs, not selected intermediate results.

Concrete c2j requests and acceptance examples are recorded in
[recovery runtime requirements](REQUIREMENTS_C2J_PARENT_RECOVERY.md). Transport and
installer defects still require their owners; this change returns their failures
to the agent/parent that can arrange the correction.

## Verification

The behavioral baseline was recorded before implementation in
[recovery-statements.md](../recipe-tests/adaptive/recovery-statements.md).
Native child submission, failures, cancellation classification, workspace restoration,
artifact binding, and package probes are real. Agent choices are scripted for routing
tests. The live schema test exercises provider acceptance rather than model capability.

Commands (use the repository's pinned c2j release and configured execution tools):

```sh
c2j test validate --directory recipe-tests/adaptive
c2j test run --directory . --case-timeout 3m --out-dir /tmp/recipe-results
# Explicit live transport test; requires the configured Codex authentication:
c2j test run --file recipe-tests/adaptive/response-schema-native.live.yaml \
  --case-timeout 2m --out-dir /tmp/recipe-native-schema-results
```

The live suite is explicitly invoked, not discovered by the normal `*.test.yaml`
scan. It uses local Codex authentication with the proxy API override disabled and
asks for fixed JSON responses without tools or repository work.

Verification uses the repository's pinned **c2j 0.0.120**. The ordinary
`/usr/local/bin/c2j` on this machine was older, so it was not used. The five final
native-provider cases passed on that pinned release; upgrading the runtime pin
was unnecessary.

The initial repository-wide run covered 726 cases: 560 passed and 166 failed.
Three failures were adaptive fixtures corrected in this change. The other 163
were checked against an isolated source snapshot of the original commit
`538ff7cf6394b4fd6610d7dbd16d31a6c69c0301`, using the same pinned runtime and tools.
158 also failed there. Those failures include obsolete legacy cell identifiers,
fixture ref/registration setup, older review assertions, and an unavailable Nix
rule-gate package. They are not claimed as fixed by this implementation.

Final results:

| Check | Result |
| --- | --- |
| Adaptive recipe contracts | All 54 suites validated, including the corrected child-summary fixture. |
| Adaptive behavioral cases | **271/271 passed**, using the full sweep and targeted reruns after fixes. |
| Live native response schemas | **5/5 passed**, with native mode and zero repair attempts. |
| Five nonadaptive cases that passed on baseline | **5/5 passed again on current code**: two accounting, two annotation, and one review-brief case. Their earlier failures were transient tool setup failures. |
| Remaining repository-wide failures | **158 preexisting failures** reproduced on the original source snapshot. The review-synthesis case was rerun to confirm its baseline assertion failure after an earlier tool-binding race. |
| Patch and documentation checks | `git diff --check` passed; local links in changed guidance and the assessment resolve. |

The last behavioral reruns covered native failure and cancellation, same-cell fresh
submission, parent completion after replacement, coordination, merge/rebase behavior,
deferred child monitoring, and original versus generated child status files. They
also verify that a completed child reporting a failed assignment exposes that
distinction in its readable summary. No adaptive failures remain in these checks.

The repository-wide suite is **not fully green**. Reproducing failures on the original
commit establishes that they predate this change; it does not establish that they
are harmless or all belong to obsolete recipes. Their relationship to the active
adaptive flow still requires dependency and failure-path analysis. Local logs and machine-readable results are under
`/tmp/recipes-recovery-tests/`; the test cases and commands above are the reproducible
record retained in this repository.

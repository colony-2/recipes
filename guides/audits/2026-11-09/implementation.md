# November 9 recipe improvements

The changes keep adaptive2's existing phases and agents. They repair review
attachments and approved recovery, add decisions at exhausted automatic allowances,
and reuse approval for an unchanged patch after neighboring upstream edits.
The [plan](improvement-plan.md) remains the reference; [test-results.md](test-results.md)
records verification and its limits.

## Changes against the plan

| Planned change | Implementation and assessment |
| --- | --- |
| Judge screenshots from the actual UI change | Existing implementation and assessment prompts require relevant actual captures, distinguish mockups and fixture evidence, permit justified exemptions, and route missing evidence to validation. Native routing and a live screenshot review were exercised. Model quality still needs follow-up audits. |
| Validate the selected review packet | Shared selection plus a read-only CommonMark/HTML link check runs in accounting and immediately before merge review. It follows every selected document's local links, checks readable targets, detects escapes/cycles, and reports incomplete validation at resource limits. Selection stays explicit; images are not auto-attached. |
| Recover approved work into implementation | New `resume_from` input verifies the prior native direction receipt in the same cell and retrieves the exact approved one-pager. Read-only assessment checks assignment coverage and required handoff/tests. Approved recovery enters fresh writable implementation; missing/revised approval and changed scope use normal design. Replacement coordination forwards the source job. |
| Preserve recovered workspaces | Configure/classify/run inherit the owner workspace. Entry candidate capture still feeds the configure guard. Failure output preserves the original configure reason and artifacts. Tests cover absent/successful configure hooks on recovered work and rejection of real mutation. Foreign consultation and exact publication selections remain deliberate. |
| Ask at exhausted automatic allowances | Shared decision helper serves adaptive2 and retained adaptive implementation, response repair, consultation correction and inspection correction. Supported bounded choices, custom integer validation, contradictory-feedback clarification, deterministic fallback and original native receipts are implemented. Existing human-turn accounting also covers helper decisions. |
| Reuse unchanged approval after same-file upstream edits | The original stored approved diff is applied to the new base in a scratch Git index; complete tree equality proves the patch is unchanged. This handles missing old candidate commit objects. Conflicts, extra behavior, file-mode and binary differences cannot use this route. Verification remains required. |
| Avoid invented prerequisites | Design, consultation and recovery guidance asks for existing interfaces, the smallest actual gap, explicit exclusions, concrete failures, and correct distinction between Git refs and handoff paths. No new classifier or taxonomy. |
| Make environment requests actionable | Package examples use resolvable references; existing policy approval and fresh candidate probe stay in place. Prompts distinguish packages from executor resources and missing source. Runtime boundaries below are documented rather than inventing an unsupported `.c2/config` machine-switch contract. |

## Limit semantics and retained work

A configured zero implementation allowance remains disabled. A positive allowance
pauses only eligible automatic work; human question/response turns stay excluded.
A grant is a new bounded round, not an increase in lifetime totals. Correction
starts with two retries and can receive a larger round for that episode. A later
unrelated invalid report uses the default. Decision preparation consumes no grant.
Receipt identities prevent renewal on replay; all original task history remains.

Continuation retains phase, assignment, session, managed Git, accepted documents,
rejected response, validation issues and selected artifact references. Fresh
correction starts a read-only session. A scope choice returns through planning.
No grant bypasses verification or publication approval. Unsafe already-started
side effects keep their operational-failure handling; debate/depth, Git,
unchanged-blocker and runtime limits were not replaced.

The helper returns the human receipt before its caller handles Stop. A stopped
build or inspection ends as `failed_app`, with `ADAPTIVE_STOPPED_BY_USER`, preserved
artifacts and no merge. Inline consultation returns an explicit cancelled result
and receipt; it is not an agreement. This is an **incomplete** runtime outcome,
not a claim that c2j cancelled the job. Already-running siblings can continue,
as stated in the brief. No production jobs were answered or changed.

## Runtime and environment boundaries

Inspected c2j 0.0.124's execution guide, configuration loader and
`ops.SuspendExecution` implementation. Node `execution_needs` supports scoped
resources, executor base/platform and capabilities; unmet needs yield
`environment_required` for a provisioner. The operation-level continuation directive
is durable and replayable. c2j itself does not provision the new environment.

The cell `.c2/config` loader exposes package and language-toolchain configuration;
its `base: go` is not an executor image. There is no generic agent response contract
here that can turn an arbitrary proposed machine change into an approved runtime
suspension. The existing package workflow already probes the exact unmerged
configuration in a separate child before adoption. It remains the implemented
path for tools. A memory/Docker/base change needs an agreed recipe/hook requirement
and compatible provisioner; local package success cannot certify that environment.
Remote executor provisioning and runtime acceptance were not established by these
recipe tests. Owners: c2j/c2ops and the cell providing the executor.

The native harness covers input waiting and actual child completion status, but
cannot hold a response for a controlled duration, restart the worker mid-wait,
or exercise deadline expiry. Those lifecycle controls remain a c2j test-harness
requirement. Recipe grants do not extend runtime deadlines. No output label is
used as evidence of runtime cancellation or suspended clocks.

Git gateway authorization, missing Apple source, recurring browser provisioning
and the reported zero-second scope timeout remain separate owner investigations
from the audit. This change does not broaden permissions to hide those failures.

## Human inspection

Live trials exercise the real packaged model and native review assembly in
isolated local cells. The UI trial uses a real Chromium capture of a changed
static page; the model judges it and writes the merge packet. Limit trials cover
implementation progress, a mechanical attachment problem and a scope conflict.
Selected documents are retained unchanged under [results](results/README.md).
The test responses finish local trials; they are not human product approvals.

The next audit should compare jobs capturing this commit with older captured
recipes, and inspect final packets rather than producer image counts. Watch for
complete galleries, justified screenshot applicability, approved recovery reaching
implementation, useful bounded decisions, and fewer unchanged-patch approvals.

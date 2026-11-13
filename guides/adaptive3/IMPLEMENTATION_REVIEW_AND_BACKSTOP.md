# Clearer reviews and Backstop: implementation assessment

Implemented the recipe changes in [the plan](PLAN_REVIEW_AND_BACKSTOP.md).
Python dependency preparation and compact directory transport remain external
blockers. Neither is marked complete in [the todo list](TODO.md).

## Changes against the plan

| Planned change | What changed |
| --- | --- |
| Restore readable documents | Shared system guidance uses the owner's voice, starts with the user's problem and recommendation, and leaves process bookkeeping out of documents. The existing validator assesses clarity. One-pager sections, the per-cell scope table and all important design questions remain. |
| Rename Resolver | Active recipe files, prompts, state paths, tests and current process documentation use **Backstop**. Historical audits retain the original name. Responsibilities and cell boundaries are unchanged. |
| Clear approval choices | The existing review activity selects **Approve direction**, **Accept answer**, **Accept and merge**, **Accept outcome**, or tool approval from the current stage and actual result. Tool refusal returns to the requester without probing or adopting configuration. |
| Separate discussion and changes | **Ask a question** and **Request changes** use the same conversation agent. Questions keep review open. Empty submissions reopen the form. Original text and uploaded notes remain available. |
| Identify the requester | Descriptive review titles begin with the stage or **Backstop**. Agent-written subjects allow room for that prefix. Model controls show current settings; renewal requests show the actual finite allowance. |
| Reconsider new guidance | Bare Continue can apply the shown correction. Continue with text or attachments goes through Backstop again before choosing a stage. Conflicting scope changes require clarification. The destination runs its full activity cycle. |
| Readable recovery requests | Simple corrections fit in the question. Optional supporting documents use working relative links and an existing primary document. The existing file validator checks these links. Agent failure, invalid reports and validator failure retain native human input. |
| Foreign-include permissions | A [reuse guide](REUSE.md) explains the caller's input-secret grant, enclosing ceilings and the need for a containing lifecycle. Native tests use a separate Git repository and synthetic secrets. No blanket secret capability was added. |
| Diagnostic results | Prompts distinguish completing an investigation from fixing the original problem. Tests return successful diagnostic jobs' negative findings to the requester and require acceptance probes to fail on negative results. |
| Real dependency preparation | An unchanged validator ran twice on the real worker pool. Both failed to import Pillow. The [recorded worker check](VALIDATOR_WORKER_CHECK.md) and [c2j bug](../BUG_REPORT_C2J_PYTHON_DEPENDENCY_ENVIRONMENT.md) document the remaining work. |

## Validation

- **106 native cases pass**, counting the full run and corrected targeted reruns
  once per case. Coverage includes real state transitions, native input forms,
  permission evaluation, local Git operations, child results and loop budgets.
- **10 validator tests pass**, executing the embedded scripts against real files,
  links, images and Git changes.
- **14 Cortex consumer tests pass**, using its actual form adapter and renderer.
  They exercise questions, change requests, typing, uploads, Back, retained edits,
  model controls, and stage/Backstop titles in the queue and detail page.
- Source validation, repository build checks, timeout-policy checks and whitespace
  checks pass.

The deterministic tests script model decisions. The consumer tests mock backing
services and unrelated document/context components; they are DOM tests, not a
deployed browser check.

This host cannot activate the declared Nix dependencies successfully. Native
execution tests therefore use a disposable copy with preinstalled tools and only
the dependency declarations removed from `tools.yaml` and `package-probe.yaml`.
The recipes' scripts, state transitions, prompts, native permissions and Git
operations remain in use. This checks their behavior; it does not prove worker
preparation works. The real-worker failure is reported separately above.

Initial native failures exposed fixtures needing another Backstop reply after
Continue with feedback, missing files in the disposable checkout, and diagnostic
fixture declarations. Those were corrected and rerun. Final inspection also found
that invalid agent reports omit the proposed review title; Backstop now presents
its native error form in that case, with two dedicated regressions.

## Live writing check

The first live trial produced a readable one-pager but returned its primary as an
`outbox/...` path. Validation correctly requested correction. The shared context
now explains that the response needs an artifact name such as `review/design.md`.
The live test uses the complete bounded lifecycle so it can correct findings
before human review, instead of assuming its first draft will pass validation.

The final live trial passed: a real agent produced the one-pager, full validation
passed, another agent answered the scripted human question, and the review stayed
open until explicit approval. See the [unaltered document and dialogue](results/notebook-reviews-2026-11-13/dialogue.md).
Its opening and design questions are clearer; the dialogue still adds some
implementation/review-status commentary that could be shorter. A trial during the
fixture migration stopped at review because its scripted response used the wrong
native node path. Correcting the path produced the passing run.

## Scope and remaining boundaries

This work adds no evidence ledger, mandatory recovery document, separate repair
activity or document-management workflow. Review choices use one shared activity;
link checking remains output validation. Runtime permission enforcement and worker
preparation remain c2j's responsibility.

The c2j Python bug must be fixed and deployed, then checked with fresh preparation,
cache reuse and rejected-dependency cases. Compact directory transport still needs
the [documented runtime/UI support](RUNTIME_REQUIREMENTS.md#4-transport-a-selected-directory-as-one-native-reference).
Until then, native artifact references can still expand into large metadata maps.

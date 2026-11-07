# Handoff, routing, and recovery implementation

Implementation date: 2026-11-07. This implements the [accepted plan](PLAN_ADAPTIVE_HANDOFF_ROUTING_AND_RECOVERY.md) and [selected intermediate recovery](PROPOSAL_CHILD_RECOVERY_WITH_INTERMEDIATE_RESULTS.md). Runtime baseline: c2j v0.0.122, tag commit `483cb48a328ea58fe8c231b8a4e3a1c11bf39422`. No production jobs were changed and no c2j source changes were made.

## Changes against the plan

| Planned correction | Implementation |
| --- | --- |
| Execution handoff from settled outcomes | Test planning must publish `handoff.md` and formal statements. A parent prepares one `work/<assignment>/` directory per execution. Child prompts read this generated assignment, not the consultation request or transcript. |
| Explicit owner routing | Execution uses the request's registered cell and ref. Handoff validation precedes target resolution and submission. Advice from root or another consultant cannot silently determine the execution workspace. |
| Separate sessions | Each design, test-plan, and implementation phase starts fresh. Inline and custom consultation calls receive no progression checkpoint, and their output checkpoint cannot replace it. Resumption within a phase remains available. |
| Recovery respects persistence | Recovery supplements the actual phase instructions. Design stays read-only; implementation can persist repairs. Response-only corrections remain read-only. |
| Selected document delivery | The response selects current documents instead of unioning every prior report. The current handoff and formal baseline remain explicit phase inputs. Advice can select its own handoff directory; execution receives only its selected directory. Original task artifacts remain retained. |
| Stop polling | `next: wait` uses durable native waiting. Direct and coordinator jobs share status collection and failures. A narrow Jev question distinguishes actual independent work from status-only continuation; uncertainty requests a focused correction. |
| Acceptance scope | Planning and review distinguish source acceptance, deployment, and parent integration. Missing optional metadata is not a new acceptance requirement. Existing verification, merge, and publication gates remain enforced. |
| Large repository context | Purpose, architecture, and README receive independent serialized size budgets. Jev receives useful bounded context and a truncation indicator. Complete supplied handoffs bypass classifier-driven design while respecting configured design requirements. |
| Inspection in initial context | All new sessions explain current-job/direct-child inspection, task occurrence IDs, fields, artifact downloads, pagination, large output files, and snapshots. Inspection is described separately from submission permissions. |
| Selective recovery | Parent instructions explain choosing useful failed-child outputs, exporting a snapshot to scratch, producing an explicit patch, and supplying a corrected handoff to a fresh attempt. The next writable task reviews, applies, and retests recovered work. Starting again remains the fallback. |

The public response contract removes `agreement`. Execution requests use `cell`, `ref`, `handoff`, and optional native `replaces` job ID. This is not a compatibility layer. Internal consultation records remain historical outcomes, not agent-generated execution keys.

## Validation

Regression expectations were written before implementation in [handoff-recovery-statements.md](../recipe-tests/adaptive/handoff-recovery-statements.md).

Native tests cover selected post-consultation files arriving byte-for-byte in a different execution owner's inbox; an unrelated document and sibling handoff are excluded. A separate native test runs inspection with a task token and job submission disabled, reads a failed child's intermediate artifact, exports its cumulative snapshot, creates a patch, and submits a fresh child that applies and verifies it. The child cannot read its parent. The previous child and its session are not restarted.

The snapshot fixture uses a same-cell child and maps its synthetic test repository URL to the actual fixture checkout for prerequisite Git fetches. The snapshot API, artifact retrieval, bundle reconstruction, patch application, and child submissions are real. Foreign-cell handoff delivery is exercised separately. No live model quality claim follows from these deterministic tests.

**All 289 current adaptive test cases pass**, using c2j v0.0.122. This combines the broad adaptive run with focused reruns after corrections and additional regression cases; it is not a claim that every repository test suite was rerun.

The broad run initially passed 274 of 283 cases. Its nine failures exposed two production bugs and outdated fixture expectations: freeform specialist assignments were incorrectly used as phase lookup keys in a shared prompt, and unresolved source citations could cause a null-key lookup in review. Both production bugs are fixed. Fixture expectations now require generated handoffs, fresh phase sessions, and selected documents instead of accumulated reports. Six additional cases brought the final inventory to 289, with no missing or failing cases. The final context review also corrected the truncation indicator for a single clipped field below the overall size budget; a dedicated regression verifies the model is told its context is incomplete.

The complete build-loop tests distinguish explicit waiting, status-only continuation, and genuine independent work. The first two reach the native wait operation without extra working turns; independent work continues before waiting. Publication coverage also verifies that a failed verification result blocks publication of an actual changed candidate even when the hook operation itself returned successfully. Routing gates reject missing owners, unsafe directories, and unknown replacement jobs before workspace resolution or submission, with valid fixture cells and files supplied so unrelated fixture failures cannot satisfy the assertion.

Validation used `c2j test run --directory recipe-tests/adaptive --parallelism 2 --case-timeout 180s`, followed by `--file` reruns of affected suites. The runtime was built from the v0.0.122 tag; the published `@colony2/c2j@0.0.122` package reports the same commit. The repository's `.c2j-version` now selects this version for CI. Local execution used the existing Nix store through a portable wrapper because the host wrapper was unavailable; no repository runtime workaround was added.

## Practical limits

- Selection and handoff quality remain agent judgments. Structural validation checks paths and real selected artifacts, not semantic completeness or whether the agent is “good enough.”
- Recovery does not automatically restore all prior files or an entire failed checkout. Explicitly selected artifacts and patches are ordinary inputs, reviewed and retested in a new execution.
- Task tokens inspect their own job and direct children, not parents, siblings, or arbitrary jobs. Missing essential inputs are reported to the parent for a corrected submission.
- The runtime waits on one pending child after first checking all tracked jobs. Wake-on-any-child remains a c2j enhancement; this change prevents busy polling but does not create that runtime primitive.
- Existing custom consultation selectors keep their documented child-recipe interface. Their sessions are isolated; converting arbitrary custom selectors into inline hooks remains outside this change.
- Non-adaptive suites, including full-creation fixtures, were not rerun for this change. The previously documented c2j fixture-identity limitation remains tracked in [the fixture requirement](FEATURE_REQUEST_C2J_RUNTIME_FIXTURE_REFERENCES.md).

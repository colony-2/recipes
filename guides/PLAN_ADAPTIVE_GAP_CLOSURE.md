# Finish adaptive coordination, recovery, reviews, and packages

Plan recorded before implementation, 2026-11-05.

Status: implemented locally. See the
[implementation assessment](ASSESSMENT_ADAPTIVE_GAP_CLOSURE.md) for the comparison,
validation, and runtime boundaries. The planned work below is retained unchanged.

This work fits the recipes cell: contracts, orchestration, prompts, diagnostics,
review assembly, and deterministic recipe tests. c2j owns goal/attempt lifecycle,
restart scopes, package preparation, and provisioning. Cortex owns rendering.
No backward compatibility is required. The explicit instruction supersedes the
earlier additive migration/deprecation proposal. Historical captured recipes are
not edited. Existing unrelated working-tree changes are preserved.

## 1. Coordination: use the new contract throughout

- Remove agent `consultations`, `keys`, `next: consult`, and `next: submit`, the
  translation include, old human `redesign` answers, and job-target fallbacks.
- Consume a list of `requests` directly. Each request is consultation or execution
  of a recorded agreement. Independent actions can coexist in one batch.
- Read agreement/submission records from native state invocation outputs. Remove
  carried `threads`/`jobs` status maps and prior-map inputs. Recipe-generated
  agreement references identify a real consultation; agents do not invent keys.
- Native goal IDs identify submitted work. Repeated execution references reuse
  that goal. Wait for outstanding goals before accepting completion, while allowing
  independent local work after submission. Reuse native result identities and
  preserve the existing root-cell creation behavior.
- Goal-result diagnostics may inspect the actual attempts named by a failed goal.
  This is evidence retrieval, never a job-ID compatibility target or success gate.

Acceptance: mixed independent actions, distinct requests to one owner, repeated
execution without duplication, goal-only dependency targeting, required work
blocking completion, and root-cell creation. Old response fields are rejected.

## 2. Operational recovery: stop asking the product reviewer

- Keep bounded automatic response correction. Exhaustion or missing checkpoints
  becomes an operational attempt failure with preserved evidence, not a review.
- Consultation bounds, repeated unchanged assessment findings, unexplained blockers,
  and work-attempt limits likewise stop the attempt for authorized goal recovery.
  A limit alone is never a product question.
- Only explicit, specific agent decision requests and required authorizations
  produce human reviews. Return actionable assessment feedback to the working
  agent first so it can request packages, owner work, or a real decision.
- Preserve native execution failures, artifacts, and restart boundaries. Add
  goal-oriented recovery instructions and diagnostic ownership. Do not close the
  goal merely because an attempt failed, grant permissions, or hide failure as
  successful recipe completion. Do not introduce a monitoring service.

Acceptance: technical failures and exhausted bounds create no input form;
explicit decisions still do; failure codes/evidence identify the recovery action.

## 3. Reviews: current decision and selected evidence everywhere

- Require an explicit overview identity at each review call. Derive a fresh brief
  from the current decision when the current response did not supply one; never
  silently choose an accumulated `review.md` or merge brief.
- Assemble one primary brief plus its explicit, identity-checked sources and
  evidence required for that decision. Apply this to questions and consultations
  as well as final acceptance. Keep unrelated history in the job story.
- Remove generic title fallbacks and unused redesign labels. Preserve the user's
  exact feedback; the working agent chooses implementation versus design.

Acceptance: stale briefs and unrelated accumulated documents are excluded;
current explicitly selected evidence remains readable; titles describe the
actual question; final reviews retain mandatory validation evidence.

## 4. Packages: decisions, evidence, and recovery persist

- Reuse native package-state invocation outputs for prior decisions. An identical
  declined reference/probe request does not create another approval. Repeated
  approved requests reuse authorization and validation goals when their exact
  proposal matches. A changed probe/proposal needs fresh authorization.
- Preserve preparation and command diagnostics under `error/`, including evidence
  from terminal attempts of an explicitly failed validation goal. Keep the parent
  config unchanged until validation succeeds for the exact candidate.
- Retain the pre-adoption config and record a recovery boundary. If later setup
  prevents the agent from starting, propagate a specific operational failure with
  the original setup evidence and instructions to repair the executor and restart
  the failed scope within the same goal. There is no product approval to retry.
- Configuration changes after authorization are never overwritten. Use the native
  pre-adoption restart boundary for an authorized revised proposal if needed;
  do not run a rollback command in an environment that cannot start, or invent
  an unsupported workspace-reset primitive.
- Keep exact reference/probe policy in a trusted include, separate from the
  request and implementation program. Empty policy means explicit authorization;
  this work does not invent trusted packages on the operator's behalf.

Acceptance: duplicate refusal/approval, changed probes, actual diagnostic artifact
binding, unchanged parent on validation failure, config identity checks, and
post-adoption preparation failure without a review or loss of existing work.

## Validation and assessment

Write test statements before edits and retain them as a fixture artifact. Update
the native fixtures with the new contract; test recipe routing, permissions,
artifact identities, package setup, and failure behavior. No live-agent quality
benchmark or Cortex visual exercise is required for this work. Record actual
results and remaining runtime boundaries in a separate implementation assessment.

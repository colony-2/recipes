# Operational outcomes and evidence: implementation plan

This work fits the recipes cell. Tune the existing adaptive workflow using the
[job audit](AUDIT_ALL_JOBS_2026-11-07.md); keep native workspaces, selective files,
inline consultation, package policy, and fresh child submissions. c2j owns job
inspection and provisioning; application cells own their fixes and publication.

1. **Finish the assigned investigation.** Planning, execution, and review prompts
   distinguish an investigation's findings (including specific unavailability)
   from the parent's later recovery outcome. Give child assignments their own
   acceptance statements. Parent-wide statements are supporting context, not the
   child's formal baseline. Missing evidence cannot pass a requirement that
   actually demands that evidence. Test the existing successful no-change path
   with an investigation deliverable and its scoped acceptance.
2. **Find existing evidence.** Update initial context and the inspection playbook
   to follow producer job/task/artifact references. Use current JobDB read
   permissions, not an assumed parent/sibling prohibition. Pin c2j 0.0.124, which
   ships that behavior. Extend the real inspection/recovery test: a child obtains
   a selected parent artifact without submission permission or blanket copying.
3. **Use unpublished code deliberately.** Explain snapshot/patch recovery for
   bounded validation and publication ordering for ordinary Git/module consumers.
   Handoffs record the producer and whether a revision is published. Keep the
   native snapshot-to-fresh-child test and do not add implicit publication.
4. **End an unsuccessful attempt.** Add schema-valid `next: fail`, route it
   directly to the existing failure export, and preserve its reason and files.
   Reworded blocker summaries or assessment findings must not bypass the three-correction budget;
   intervening successful work or candidate changes still allow progress.
   Require a concrete correction or transient-failure evidence for resubmission.
   Preserve supplied `recovery.md` without colliding with generated guidance.
   Test direct failure, failure after recovery, varied summaries, preserved
   files, and the existing successful recovery/progress paths.
5. **Keep environment and review requirements scoped.** Latest human scope
   decisions override generated checklists. Defer excluded Docker/architecture
   checks; use compatible installed tools unless an exact version is required.
   Necessary packages use existing policy/probes; other unmet capabilities return
   to the coordinator. A human question identifies the necessary unresolved
   decision and does not ask again for an already given answer. Review overviews
   start with the outcome, current decision, and changes since prior approval.
   Retain package, feedback, expectation protection, and review regression tests.

Tests use scripted agent responses to check contracts and control flow, plus
native command, artifact, workspace, and inspection operations. They do not
claim to prove the model will always make the right judgment. Assess the final
implementation against this plan, run the full adaptive suite, and commit. Live
jobs retain their captured recipes; this work does not resubmit or change them.

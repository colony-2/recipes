# Complete recovery of work coordinated by an earlier parent

Recipe bug: Cortex `3Lt9OHY4qBqZQud8OR1iKj6V1Wd` recovered its approval and code,
but the coordinator rejected previous child IDs and receiver handoffs because
neither appeared in this new parent's coordination history.

This fits the recipes cell. The independent restart numeric-type bug belongs to
c2j and is reported separately with a reproduction.

## Plan

- Keep prior-job inspection and artifact selection with the agent. Explain how to
  use `resume_from`, `replaces`, and the receiver's recovered assignment together.
- Allow an explicit previous attempt to be inspected even when another parent
  submitted it. Reuse the existing child status/wait path to avoid duplicating
  running or successfully completed attempts.
- When no current consultation agreement exists, allow a recovery handoff to reach
  the receiver's existing approval inspection and scope assessment. This is not an
  approval: absent or changed approval still requires ordinary design review.
- Preserve existing handoff comparison when this job has a receiver agreement.
  Recovery must not bypass correction of a modified current assignment.
- Add native coverage for a recovered parent coordinating an earlier receiver's
  work, selective evidence delivery, repeated submission prevention, completed work,
  and missing agreements without recovery. Keep existing approval/scope regressions.

No imported coordinator history, new agreement IDs, generic recovery service, or
additional review stage. Stop after implementation, relevant tests, and an
assessment. Do not change or restart the observed jobs.

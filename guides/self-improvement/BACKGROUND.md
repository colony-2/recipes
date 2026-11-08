# Background and decisions

This is historical context for recipe improvements, especially work motivated by
observed jobs. [General recipe guidance](../RECIPE_IMPROVEMENT_GUIDE.md) contains
principles that apply to ordinary edits too; the [documentation map](../README.md)
points to the current contracts. Ownership is defined by [PURPOSE.md](../../PURPOSE.md).
An audit can span many cells without making this cell responsible for implementing
every external outcome.

## Why this method exists

Our recurring objective is to make underlying agents effective at completing work:
give them enough context to investigate, repair mistakes, obtain useful inputs,
coordinate dependencies, and ask understandable questions when a human decision
is needed. Workflow machinery should support those abilities. It should not make
the human debug internal phases, locate already-retained files, or repeat an answer.

We have changed the workflow several times. That history argues for understanding
the existing mechanism before replacing it, while leaving room for a redesign
when the mechanism is the demonstrated cause. Explain which observed problem a
change solves, what behavior it preserves, and what complexity it adds.

## Representative evidence and implementation history

| Background | Why it matters |
| --- | --- |
| [Agent autonomy and recovery assessment](../ASSESSMENT_AGENT_AUTONOMY_AND_PARENT_RECOVERY.md) | Parent follows failed attempts and takes responsibility for the next useful action. |
| [Handoff and recovery assessment](../ASSESSMENT_HANDOFF_ROUTING_AND_RECOVERY.md) | Distinct sessions, selected documents, corrected routes, and recovery from retained intermediate work. |
| [All-job audit, November 7](../AUDIT_ALL_JOBS_2026-11-07.md) | Investigation acceptance exceeded its assignment; agents missed retained documents/code; reworded blockers evaded a retry bound. |
| [Operational-outcomes assessment](../ASSESSMENT_OPERATIONAL_OUTCOMES.md) | Explicit failure, bounded recovery, producer inspection, scoped reviews, and native regression evidence. |
| [Testing-gap assessment](../ASSESSMENT_RECIPE_TEST_GAP_CLOSURE.md) | Why simplified fixtures and schema-only checks missed real orchestration boundaries. |
| [Direct-state implementation](../IMPLEMENTATION_DIRECT_RECIPE_STATE.md), [standard agent inbox](../IMPLEMENTATION_STANDARD_AGENT_INBOX.md) | Why state stays in recipe properties while selected files carry evidence and feedback. |
| [Instruction and skill rationale](../PROPOSAL_AGENT_INSTRUCTIONS_AND_SKILLS.md) | Small standing context plus optional specialized expertise; skills do not replace workflow transitions. |
| [Legacy workflow removal](../ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md) | Which old implementations were retired and which creation helpers remain. |

These reports explain decisions, not permanent bug lists. Check the producing
recipe commit, runtime version, session history, actual artifact availability,
and subsequent changes before proposing the same correction again. A new child
can still receive a bad handoff from an older parent. Missing optional provenance
is a limitation, not automatically a new acceptance requirement.

Find additional dated audits, proposals, implementation reports, and external
requirements through the history section of the documentation map. Update this
background when evidence changes a general lesson; keep per-cycle details in the
audit artifacts rather than adding every new failure to standing instructions.

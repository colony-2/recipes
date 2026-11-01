# Adaptive build process

Current flow selected by [build.yaml](build.yaml), implemented in
[recipes/adaptive](recipes/adaptive/README.md). Like the [original diagram](BUILD_PROCESS.md),
boxes group work and diamonds show decisions. Agents determine how to do the work;
the recipe controls validation, child jobs, review, and publication.

## Main workflow

```mermaid
flowchart TD
    Start([Build request]) --> Config[Configure hook: guidance and specialist checkpoints]
    Config --> Decide{Jev: design needed?}
    Decide -->|Yes, uncertain, or required by configuration| Context[Before-design hook and configured specialists]
    Decide -->|No| Tests[Define test-statements.md before implementation]
    Context --> Design[Conceptualize and design: ownership, outcomes, alternatives, interfaces, compatibility]
    Design --> DesignDoc[Publish design.md and agreed prerequisite keys]
    DesignDoc --> Tests
    Tests --> Plan[Run configured plan specialists]
    Plan --> PlanOK{Required findings resolved?}
    PlanOK -->|No| Context
    PlanOK -->|Yes| Work[Implement, test, and coordinate agreed child work]
    Work -->|Scope needs redesign| Context
    Work -->|Ready; required children succeeded| Rebase[Native rebase onto current target]
    Rebase -->|Structured conflict| Recovery[Conflict recovery: see below]
    Recovery --> Work
    Rebase -->|Success| Prepare[Prepare hook; record candidate and hook identity]
    Prepare --> Prepared{Preparation passed or skipped?}
    Prepared -->|No| Work
    Prepared -->|Yes| Specialists[Run configured outcome specialists]
    Specialists --> SpecialistOK{Required findings resolved?}
    SpecialistOK -->|No| Work
    SpecialistOK -->|Yes| Verify[Run verify hook; retain result and evidence]
    Verify --> Verified{Verification permits completion?}
    Verified -->|Failure or required skip| Work
    Verified -->|Yes| Assess[Independent candidate assessment]
    Assess --> Assessed{No blocking findings?}
    Assessed -->|No| Work
    Assessed -->|Yes| Summary[Prepare merge-review.md: outcomes, every changed file, evidence, commit message]
    Summary --> SummaryOK{Evidence and accounting sufficient?}
    SummaryOK -->|No| Work
    SummaryOK -->|Yes| Review{Human outcome review}
    Review -->|Restart design with new information| Context
    Review -->|Revise with feedback or annotations| Work
    Review -->|Cancel| Cancelled([Complete: cancelled])
    Review -->|Accept without edits| Changes{Local changes remain?}
    Changes -->|No| Unchanged([Complete: unchanged])
    Changes -->|Yes| Merge[Squash reviewed candidate; native merge]
    Merge -->|Upstream advanced| Chase[Bounded upstream chase: see below]
    Merge -->|Other error| Failed([Job fails with diagnostics])
    Merge -->|Success| Publish[Publish hook against merged commit]
    Publish --> Published{Publication passed or skipped?}
    Published -->|Yes| Done([Complete: implemented])
    Published -->|No| PublishFailed([Job fails; merge already happened])

    classDef human fill:#fff3cd,stroke:#9a6700,color:#24292f
    classDef artifact fill:#ddf4ff,stroke:#0969da,color:#24292f
    class Review human
    class DesignDoc,Tests,Summary artifact
```

- **Review:** normally one human outcome review; design has no routine approval gate.
  Specific agent questions and iteration limits can request earlier direction.
  Revision needs feedback or uploaded edits; acceptance with edits returns to work.
- **Formal evidence:** test statements have stable IDs, expectations, filenames,
  importance, test level, and dependencies. Implementation reports results against
  that baseline; changing the plan requires redesign and preserves existing expectations.
- **Review documents:** c2j annotations prioritize `merge-review.md`, test statements,
  test results, and independent findings, with design and implementation as support.
- **Failures:** verification execution, output, evidence, or mutation failures return
  to implementation. Cancellation remains cancellation. Other fatal errors can stop
  any phase; the chart omits repetitive error edges.

## Cross-cell coordination

Design, test planning, and implementation can request serving consultation. Only
implementation submits agreed work. This coordination returns to the current phase.

```mermaid
flowchart TD
    Need([Another cell must produce work]) --> Owner{Existing owner or new cell?}
    Owner -->|Existing cell| Serving[Consult the serving cell on a bounded request]
    Owner -->|New cell| Root[Consult the project root on ownership and creation]
    Serving --> Agreement{Serving agreement reached?}
    Root --> Agreement
    Agreement -->|No| Resolve[Continue dialogue or reconcile the unresolved request]
    Resolve --> Agreement
    Agreement -->|Yes| Phase{Implementation phase?}
    Phase -->|No| Record[Record agreed key; continue planning]
    Phase -->|Yes| Known{Job already recorded for this key?}
    Known -->|Yes| Reuse[Use recorded job and outcome]
    Known -->|No| Launch[Recipe starts child build or root-owned creation job]
    Launch --> Independent[Continue independent local work]
    Independent --> Wait[Recipe waits when blocked and before completion]
    Reuse --> Wait
    Wait --> Success{Required child succeeded?}
    Success -->|No| Repair[Reconcile failure; completion remains blocked]
    Success -->|Yes| Resume[Resume parent with durable outcome and evidence]
```

**Agreement is mandatory before submission.** Stable keys prevent duplicate jobs
across retries and redesign. Creation retains root-owned approval and readiness
requirements; creating a cell does not implement the original feature request.

## Native rebase recovery and upstream advancement

Conflict repair and upstream chasing have separate budgets. Neither retries
arbitrary Git failures or repeats publication after an already successful merge.

```mermaid
flowchart TD
    Advanced([Merge reports upstream advanced]) --> Budget{Fewer than three chase retries?}
    Budget -->|No| Fail([Job fails])
    Budget -->|Yes| Rebase[Increment chase count; native rebase onto current target]
    Rebase -->|Success| Prepare[Prepare candidate; rerun outcome specialists and verification]
    Prepare --> Passed{All required checks permit completion?}
    Passed -->|No| Work[Return to implementation and normal assessment and review]
    Passed -->|Yes| Same{Same change digest or empty delta, and same hook identity?}
    Same -->|No| Fresh[Fresh independent assessment, merge summary, and human review]
    Same -->|Yes| Changes{Local changes remain?}
    Changes -->|No| Done([Complete: unchanged or delegated])
    Changes -->|Yes| Merge[Reuse approval; squash and attempt native merge]
    Merge -->|Upstream advanced| Advanced
    Merge -->|Success| Publish([Run publish hook; fail if publication fails])
    Merge -->|Other error| Fail

    Conflict([Native rebase fails, in either path]) --> Eligible{Restored structured conflict, complete diagnostics, fewer than two repairs?}
    Rebase -->|Failure| Conflict
    Eligible -->|No| Fail
    Eligible -->|Yes| Save[Save entire binary candidate diff and commit log]
    Save --> Adopt[Reset known clean candidate to recorded base; native rebase onto recorded target]
    Adopt --> Clear[Increment repair count; clear verification and outcome approval]
    Clear --> Work
```

The agent reconciles the saved delta with concurrent changes; it never performs
the rebase itself. Small control state travels through inputs and outputs. Diffs,
documents, command output, and consultation transcripts remain artifacts. Hooks
return values and evidence directly, without a second report-inspection task.

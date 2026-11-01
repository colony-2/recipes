# Build recipe process

Conceptual view of [build.yaml](build.yaml), the
[light workflow](recipes/light/develop.yaml), and the
[heavy workflow](recipes/develop/develop.yaml). Boxes group related operations;
diamonds show decisions. This documents the current recipes, not a proposed flow.

## Main workflow

```mermaid
flowchart TD
    Start([Build request]) --> Configure[Configure hook: settings, guidance, specialists]
    Configure --> Classify[Read repository context; classify this cell's scope, complexity, uncertainty, and risk]
    Classify --> Route{Confidently light and no design requirement?}

    subgraph Light[Light workflow]
        LI[Implement and test using existing patterns]
        LI --> LD[Coordinate needed child work; wait for successful child outcomes]
        LD --> Escalate{Complexity requires heavy workflow?}
        Escalate -->|Yes| Handoff[Preserve session, candidate, artifacts, and completed child outcomes]
        Escalate -->|No| LR[Inspect diff; rebase; run prepare hook]
        LR -->|Rebase failure| ConflictGate
        LR --> LP{Preparation acceptable?}
        LP -->|No| LI
        LP -->|Yes| LS[Run configured outcome specialists]
        LS --> LSP{Required specialists pass?}
        LSP -->|No| LI
        LSP -->|Yes| LV[Run verify hook; record evidence]
        LV --> LVP{Verification permits completion?}
        LVP -->|Failed| LI
        LVP -->|Required but skipped| LI
        LVP -->|Yes| Delegated{No local changes and successful children?}
        Delegated -->|Yes| DelegatedDone([Complete: delegated])
        Delegated -->|No| Synopsis[Create synopsis.md: outcome, file inventory, evidence, proposed commit message]
        Synopsis --> LA{Human outcome review}
        LA -->|Feedback or annotated documents| LI
        LA -->|Cancel| Cancelled
        LA -->|Accept without changes| HasChanges
    end

    subgraph Heavy[Heavy workflow]
        Research[Before-design hook and specialists: gather context]
        Research --> Design[Conceptualize and design: purpose fit, requirements, scope, alternatives, interfaces, acceptance criteria]
        Design --> DesignDoc[Publish design.md; agree serving-cell prerequisites]
        DesignDoc --> Tests[Define test-statements.md before implementation]
        Tests --> PA[Independent plan assessment and configured specialists]
        PA --> PAP{Explicit passing assessments?}
        PAP -->|No| Research
        PAP -->|Yes| Plan{Human design and test-plan review}
        Plan -->|Feedback or annotated documents| Research
        Plan -->|Cancel| Cancelled
        Plan -->|Approve without changes| HI[Implement approved design and tests]
        HI --> HD[Launch approved prerequisites; continue independent work; wait before completion]
        HD --> HR[Rebase onto current target; run prepare hook]
        HR -->|Rebase failure| ConflictGate
        HR --> HP{Preparation acceptable?}
        HP -->|No| HI
        HP -->|Yes| HA[Independent candidate assessment and outcome specialists]
        HA --> HAP{Explicit passing assessments?}
        HAP -->|No| HI
        HAP -->|Yes| HV[Run verify hook; record verification.md and evidence]
        HV --> HVP{Verification permits completion?}
        HVP -->|Failed| HI
        HVP -->|Required but skipped| HI
        HVP -->|Yes| Accounting[Fresh reviewer accounts for every changed file and proposes commit message]
        Accounting --> AccountOK{File accounting acceptable and current?}
        AccountOK -->|Revise| HI
        AccountOK -->|Candidate stale| HR
        AccountOK -->|Yes| Outcome[Present merge-review.md, candidate diff, and verification evidence]
        Outcome --> Accept{Human outcome review}
        Accept -->|Revise implementation with feedback| HI
        Accept -->|Redesign with feedback| Research
        Accept -->|Cancel| Cancelled
        Accept -->|Accept without changes| HasChanges
    end

    Route -->|Yes| LI
    Route -->|No or uncertain| Research
    Handoff --> Research

    ConflictGate{Classified restored conflict, complete evidence, fewer than two repairs?}
    ConflictGate -->|No| Failed
    ConflictGate -->|Yes| ConflictRepair[Increment repair count; bind diagnostics; clear candidate approval and verification]
    ConflictRepair --> ConflictPath{Current workflow?}
    ConflictPath -->|Light| LI
    ConflictPath -->|Heavy| HI

    HasChanges{Local changes remain?}
    HasChanges -->|No| Unchanged([Complete: unchanged])
    HasChanges -->|Yes| Squash[Squash reviewed candidate with reviewed commit message]
    Squash --> Merge[Fast-forward merge into target branch]
    Merge -->|Success| Publish[Run publish hook against merged commit]
    Publish --> PublishOK{Publish passed or skipped?}
    PublishOK -->|Yes| Implemented([Complete: implemented])
    PublishOK -->|No| PublishFailed([Job fails; merge already happened])
    Merge -->|Upstream advanced| Chase[Bounded merge retry: see chart below]
    Merge -->|Other error| Failed([Job fails with diagnostic])
    Cancelled([Complete: cancelled])

    classDef human fill:#fff3cd,stroke:#9a6700,color:#24292f
    classDef artifact fill:#ddf4ff,stroke:#0969da,color:#24292f
    class Plan,Accept,LA human
    class DesignDoc,Tests,Synopsis,Outcome artifact
```

- **Light selection:** usable context and a valid Jev probability of heavy work
  between 0 and 0.10. `require_design` or configured design-stage specialists force
  heavy. Classification concerns this cell's work, not the size of the overall project.
- **Conceptualization:** part of heavy design, rather than a separate recipe phase.
  Design covers alternatives, compatibility, acceptance criteria, and ownership.
  A missing `PURPOSE.md` does not block work; repository evidence supplies context.
- **Clarification and ownership:** during agent work, focused questions pause and
  then resume the current phase. Answers do not approve a plan. A request outside
  the cell's purpose can finish with `outside`; light first settles launched children.
- **Verification:** skipped checks permit normal review unless
  `require_verification` is true. Required skips and hook execution, validation,
  or report failures return to implementation with diagnostics. Cancellation
  still stops execution. Light delegated outcomes also pass through
  preparation, specialists, and verification. Heavy no-change outcomes still
  require independent assessment and human acceptance.
- **Review:** approval accompanied by feedback or uploaded edits requires revision
  and another review. A revision selection without actionable feedback repeats the
  review prompt. Required specialists must explicitly pass.
- **Recovery:** correctable agent-output errors get up to two automatic corrections,
  then human direction. Dependency failures require reconciliation rather than
  silently completing or duplicating child jobs. Execution errors can fail a job
  at any stage; the chart does not draw every error edge.

## Cross-cell coordination

This flow can interrupt agent work and then return to its current phase. Heavy
design must identify agreed prerequisite keys before plan approval; implementation
can launch only approved prerequisites. Light has no local plan-approval gate.

```mermaid
flowchart TD
    Need{What external outcome is needed?}
    Need -->|Existing serving cell| Consult[Consult owning cell; agree bounded request and handoff artifacts]
    Consult --> Agreement{Agreement reached?}
    Agreement -->|No| Resolve[Continue dialogue; use synthesis and human deconfliction when needed]
    Resolve --> Consult
    Agreement -->|Yes| Mode{Parent workflow?}
    Mode -->|Light| Launch[Launch child build with stable request key]
    Mode -->|Heavy| Approved{Prerequisite included in approved plan?}
    Approved -->|No| Plan[Include agreed request in design; obtain plan approval]
    Plan --> Approved
    Approved -->|Yes| Launch
    Need -->|New cell| Creation[Route creation request to root-owned creation workflow]
    Creation --> RootReview[Root owns creation architecture and human approval]
    RootReview --> Ready{Creation ready?}
    Ready -->|Yes| Resume[Resume parent with recorded child outcome]
    Ready -->|No| Recovery[Reconcile failure or seek human direction]
    Launch --> Work[Continue independent work while child runs]
    Work --> Wait[Wait when blocked and before parent completion]
    Wait --> Success{Child merged, delegated, or unchanged?}
    Success -->|Yes| Resume
    Success -->|No| Recovery
```

Creation also follows the parent's applicable prerequisite approval rules.
Each child build classifies its own work. Completed outcomes and stable request
keys are retained across retries and light-to-heavy escalation.

## Merge retry when upstream advances

Both paths catch `MERGE_UPSTREAM_ADVANCED` from the merge operation and allow at
most three upstream-chase retries. This is a targeted recovery path, not a retry
of arbitrary merge or publish failures.

```mermaid
flowchart TD
    Advanced([Merge reports upstream advanced]) --> Budget{Fewer than three chase retries used?}
    Budget -->|No| Fail([Job fails])
    Budget -->|Yes| Rebase[Increment retry count; rebase; run prepare hook]
    Rebase -->|Rebase failure| Recoverable{Restored structured conflict and fewer than two repairs?}
    Recoverable -->|No| Fail
    Recoverable -->|Yes| ConflictRepair[Increment separate repair count; attach evidence; invalidate candidate approval]
    ConflictRepair --> Repair
    Rebase --> Prepared{Preparation acceptable?}
    Prepared -->|No| Repair[Return to implementation and normal review flow]
    Prepared -->|Yes| Reusable{Same change digest or no changes, and same hook digest?}
    Reusable -->|No| Fresh[Invalidate prior outcome approval; run normal assessment, verification, and review]
    Fresh --> Normal([Continue main workflow])
    Reusable -->|Yes| Specialists[Reuse outcome approval; rerun outcome specialists]
    Specialists --> SpecialistOK{Required specialists pass?}
    SpecialistOK -->|No| Repair
    SpecialistOK -->|Yes| Verify[Run fresh verification]
    Verify --> Verified{Verification permits completion?}
    Verified -->|Failed| Repair
    Verified -->|Required but skipped| Repair
    Verified -->|Yes| Changed{Local changes remain?}
    Changed -->|No| Done([Complete: delegated or unchanged])
    Changed -->|Yes| Merge[Squash and attempt merge again]
    Merge -->|Upstream advanced| Advanced
    Merge -->|Success| Publish([Run publish hook; complete if successful or skipped])
    Merge -->|Other error| Fail
```

Fresh review follows the selected path: light produces a synopsis; heavy performs
independent assessment and file accounting. Light delegation without local changes
retains its normal exception to local outcome review.

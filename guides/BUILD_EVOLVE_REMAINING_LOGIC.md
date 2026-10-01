# Build/evolve orchestration after simplification

The five remaining embedded Python blocks have been removed.

| Former logic | Current behavior |
|---|---|
| Mandate parser and provenance recorder | Agents read `.c2j/mandate.md` as Markdown and use c2j's Git history when reviewing changes. |
| Design validator and handoff formatter | Agent authors `outbox/design.md`; a small schema checks routing and native review presents the document. |
| Implementation handoff comparator | Agent consults another cell, requests redesign when needed, and explains the changes in `outbox/implementation.md`. |
| Test-plan catalog validator and renderer | Author maintains `.c2j/test-plan.md`; an independent agent reviews expectations and coverage. A native command copies the exact plan for review. |
| Verification executor and candidate ledger | Native command runs target-relative `build.sh` when present, uses its return status, and publishes a report and log. |

The shared phase loop resumes the local session or consults another cell as
requested by `next`. A consultation retains the latest foreign session and reply.
Native op metadata supplies child jobs; native await operations return outcomes
and artifacts. No context preparation, transcript reconstruction, turn recorder,
custom scope guard, or hash snapshot operation remains.

The small shell steps create the target directory, read schema-checked result
JSON, copy the maintained test plan for review, and run/report the verification
hook. Native review handles uploaded Markdown/CriticMarkup and review receipts.
`finish.yaml` uses c2j's current Git state for the accepted squash merge.

Designs, summaries, and execution evidence remain runtime artifacts. Only maintained
responsibility and test expectations belong in `.c2j/mandate.md` and
`.c2j/test-plan.md`; the workflow does not accumulate per-job documents in Git.

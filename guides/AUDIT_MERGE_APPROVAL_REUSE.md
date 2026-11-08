# Merge approval reuse: job 3EhcYPdVGfpaXtxMoxXYrAIQ15A

Observed on 2026-11-08 through read-only c2j inspection of
`http://192.168.1.195:9047/c2`. This is a single-job causal audit, not a
cohort-wide failure-rate measurement. No live job was changed.

## Finding

The [job](https://jobs.colony2.com/c2/jobs/3EhcYPdVGfpaXtxMoxXYrAIQ15A)
presented three merge reviews, received two acceptances and one revision request,
and ultimately merged successfully. There was **one failed merge attempt**, not
three failed merges.

After the first approval, the implementation required no code changes. The second
review covered a byte-identical patch after a clean rebase. The third covered
21 added documentation lines answering the human's compatibility question.

## Timeline

All timestamps are UTC.

| Event | Time | Evidence and outcome |
| --- | --- | --- |
| First review requested | Nov 7, 03:10:19 | Canonical lease events; 41 changed files. Repository verification hook absent; separately recorded implementation and assessment checks available. |
| First review accepted | Nov 8, 02:48:42 | `decision: accept`, empty feedback, no attachments. |
| First merge attempted | Nov 8, 02:48:48 | Failed because the target branch had advanced. |
| Rebase completed | Nov 8, 02:49 | Native rebase succeeded without conflict repair. Candidate patch remained byte-identical. |
| New verification ran | Nov 8, 02:49–02:56 | Upstream now supplied a verification hook. Environment, integration and race checks passed. |
| Second review requested | Nov 8, 02:59:49 | Same implementation; fresh assessment approved it, but changed hook identity prevented approval reuse. |
| Human requested clarification | Nov 8, 03:02:30 | `decision: revise`; feedback: “is this change backwards compatible?” |
| Follow-up completed | Nov 8, 03:07 | Added 21 lines to `docs/GUIDE-LEASE-EVENTS.md`; no behavior or code changes. |
| Third review requested | Nov 8, 03:19:47 | Compatibility explanation, renewed verification and assessment. |
| Third review accepted | Nov 8, 03:32:52 | `decision: accept`, empty feedback. |
| Second merge succeeded | Nov 8, 03:33:07 | Published `ea45f87bf010437a08575d7626409f8d0f1ffe35` to `refs/heads/main`. |

## Why the second review happened

The job captured recipes commit `de2e9cdc3a113f3c811c3ca998815b0b45adf143`.
Its `inspect_chased_candidate` transition required both an unchanged local-change
digest and an unchanged hook digest to reuse approval. That condition also exists
in the [development recipe](../recipes/adaptive/develop.yaml) at audit time.
The subsequent correction removes hook identity from this decision; see the
[implementation assessment](ASSESSMENT_MERGE_APPROVAL_REUSE.md).

The local-change comparison passed:

- First candidate: `bf63ca59cf799413d17760006d1447210cc72d3e`, base
  `f92ae253a5da7a6b81944d0bdf4cadb085772140`.
- Rebased candidate: `582222654cd2ebfef62e37d2a894884fd9522242`, base
  `3e75f8ec47bb9eab699508c3c8c3d1542367f2ba`.
- Both local-change digests:
  `b88923b8f6ef8835a806426a5d8e8f8f6abd1dc462aec217601ef955aac8cf96`.
- Independently downloaded `merge-candidate.diff` artifacts were byte-identical:
  148,780 bytes, SHA-256
  `b3fe990527c882a6f16d5ba1d9f32cf0e23343254180663f0f72b6006681cadc`.

The hook comparison failed:

- Previous hook digest:
  `5ec9995e3eda3f886fc95b8394a2886d92d94009b14bfa5fac85f2db67b8cb07`.
- Rebased hook digest:
  `0cf5487bc8037c43d8ff7f52e3e222ba25dc6ae796b29d9a1529ce1e4b848ce3`.
- Hook-load records establish a real upstream change: the original
  `.c2/recipes/hooks/build/verify.yaml` was absent; the rebased candidate had it.
- Its environment, integration and race checks all passed before the second review.

Thus the recipe sent the candidate through fresh assessment, summary and human
review solely because the hook identity differed. This example does **not**
demonstrate either of the other suspected causes: full-file comparison rejecting
a harmless same-file upstream edit, or an opaque hook identity changing merely
because the commit changed. Those remain separate regression cases to consider.

## What changed for the third review

The human selected Request changes to ask about backward compatibility. The agent
returned a direct answer: the feature was not fully backward compatible, and the
existing contract required those boundaries. It changed only documentation:

- `docs/GUIDE-LEASE-EVENTS.md`: **21 lines added, zero removed**.
- The first and second candidate patches have 41 identical file changes; comparing
  the second and third patch blocks shows only this guide differs.
- The supplied `compatibility.diff` independently describes the same 21-line addition.
- Candidate became `2465125b667ddde1183d544823a4c64ef44277c7`; base and hook identity
  remained unchanged. Fresh verification and independent assessment passed.

The added section explains mandatory Go interface changes, the additive HTTP
endpoint, new clients against old servers, forward SQLite format 11→12 migration,
the old binary rejecting format 12, no downgrade, and coordinated writer rollout.
These were existing behavior and compatibility risks, not new behavior introduced
after approval. The first review mentioned mandatory interfaces and coordinated
rollout, but did not foreground the explicit “not fully backward compatible” answer.

A response to that human question was necessary. Because it surfaced material
compatibility considerations, a focused confirmation could be appropriate; it
should distinguish those existing risks from the documentation-only follow-up.
It should not imply another implementation or merge repair occurred.

## Review presentation gap

The second brief correctly said no implementation content change was identified,
but again presented the entire 41-file feature for approval. The third mentioned
the compatibility clarification, then presented the full feature again. Neither
form supplied the original approved merge-review document as a separately named
reference. The summaries described earlier reviews without a durable link to the
actual approval baseline.

## Implications for the proposed correction

1. Retain the accepted human decision and its exact review/candidate references.
   A later model assessment or regenerated summary is not a new human approval.
2. Rerun changed verification. Under the subsequently agreed rule, a new, passing
   upstream hook does not invalidate approval of unchanged work. Approval reuse
   does not need another model assessment or human decision in that case; remove
   hook fingerprinting from the decision entirely.
3. If another decision is needed, make the difference the primary brief and attach
   the original approved review as supporting evidence. In this job, the third
   brief should lead with the compatibility answer and the 21-line documentation
   addition, explicitly stating that no code or behavior changed.
4. Add native regressions matching this example: approval, target advancement,
   absent-to-present verification hook, identical patch, passing fresh checks,
   and no second input request. Separately cover clarification/documentation
   follow-up and materially changed behavior requiring a focused new review.

These changes belong to this recipes cell. This audit does not establish a need
for new c2j inspection APIs. No recipe changes or live-job actions were made.

## Evidence inventory and reproduction

Job: `3EhcYPdVGfpaXtxMoxXYrAIQ15A`; cell: `jobdb`; parent:
`07c92827-240d-488a-b6a8-7d250406fcfe`; final status: completed/success.
The inspection inventory contained 69 task occurrences and no continuation cursor.

Review request IDs:

| Review | Request ID |
| --- | --- |
| First | `4ccb5824-5d8a-42c2-aeb2-78498c97ed0a` |
| Second | `ca429cc1-73c7-418c-b2d7-9611221a2725` |
| Third | `beee0cad-7dbb-49ae-a038-f06468a1e23a` |

Retrieve exact task IDs with `c2j job log JOB --limit 100 --output tasks.json`.
Repeated node paths have distinct IDs; select the occurrence by time and enclosing
state occurrence. See the [inspection playbook](JOB_INSPECTION_PLAYBOOK.md).

| Task selection | Evidence used |
| --- | --- |
| Root source resolution | Captured recipe commit. |
| `prepare` occurrences 1, 2, 3: `inspect_candidate_diff` | Candidate JSON and binary patches. |
| `prepare` occurrences 1, 2, 3: `inspect_hook_sources` | Hook identity digests. |
| `verify` occurrences 1 and 2: hook load | Verification hook absent, then present. |
| `verify` occurrences 2 and 3: `summarize` | All configured checks passed. |
| `inspect_chased_candidate` occurrence 1 | Reconfirmed unchanged candidate digest. |
| `accounting` occurrences 1, 2, 3 | Actual `merge-review.md` artifacts. |
| `accept` occurrences 1, 2, 3 | Generated form documents and recorded human responses. |
| `work` occurrence 2 | Compatibility response and documentation-only implementation report. |
| Final accounting | `compatibility.diff`, implementation and test reports. |
| `rebase` and `merge` occurrences | Clean rebase; one upstream-advance failure; final successful merge. |

Raw downloads remain in scratch at `/tmp/merge-review-audit-3EhcYP-kNoGoZ` for
this session. Durable producer references above permit retrieval while JobDB
retains the records. This audit compared saved evidence; it did not rerun JobDB's
application tests or independently certify the complete lease-events feature.

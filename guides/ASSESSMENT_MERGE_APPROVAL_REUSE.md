# Merge approval reuse: implementation versus proposal

This change implements the correction agreed after the
[three-review job audit](AUDIT_MERGE_APPROVAL_REUSE.md). It changes recipe routing
and artifact delivery, with prompt changes for presentation. No c2j or c2ops
runtime change is required.

## Implemented changes

| Agreed change | Implementation |
| --- | --- |
| Remove hook fingerprinting from approval | Deleted `hook-identity.yaml`, its preparation operation, and all hook-digest plumbing. Changed hooks still run normally. |
| Reuse approval deterministically for unchanged work | After successful checks, compare the current change digest with the candidate recorded by the latest human acceptance. An unchanged candidate goes directly to merge; an empty delta completes. No additional assessment, summary, or human input runs. |
| Preserve the actual human approval baseline | `accept` exports the candidate and immutable review/diff/inventory artifact references alongside its existing human response. Native state history remains the source of approval. |
| Provide focused subsequent reviews | Assessment and summary receive `approved/merge-review.md`, `approved/merge-candidate.diff`, and `approved/merge-candidate.json`. Prompts require the additional decision, changed work, reason, evidence, and a link to the original review. |
| Make references explicit in the form | Follow-up forms include original and current comparison artifacts regardless of the agent's source annotations. The current brief is primary, the original review supporting, and diffs/inventories diagnostic. |
| Verify the observed failure and related boundaries | Native merge-chase tests cover changed and newly introduced hooks, failed checks, substantive repairs, clarification, immutable references, and multiple accepted candidates. |

`approved-review-documents.yaml` is an empty-sequence projection of actual human
review history. It creates no worker task, classifier, or maintained approval map.
It selects the latest acceptance without feedback or attachments and renames
references for the inbox; it does not copy or regenerate the original contents.
The recipe reasserts those references before summary and form construction, so
returned agent copies cannot replace the accepted baseline.

## Decisions and limits

- Automatic reuse requires the latest human decision to be acceptance without
  requested edits. A subsequent revision request, cancellation, feedback, or upload
  is not silently overridden using an older approval.
- If a verification failure is transient and the agent resumes without changing
  the candidate, fresh passing checks can reuse the existing approval. This uses
  the human decision directly instead of the former `resume_merge` flag.
- Changed content still receives assessment and human review. The summary explains
  differences from the last acceptance, even if an intervening review was rejected
  or asked a question. A subsequent acceptance becomes the comparison baseline
  for later merge retries.
- The existing change digest remains conservative: it compares paths, before/after
  file contents and modes independently of commit IDs. Harmless upstream edits to
  the same changed file can still require review. No new semantic-equivalence
  classifier or whitespace-insensitive comparison is introduced.
- Retry bounds, conflict diagnostics, required verification, cancellation, and
  publication-failure behavior remain in force.

## Validation

Acceptance statements A08 and A23–A27 in
[the adaptive test statements](../recipe-tests/adaptive/test-statements.md) define
the updated contract. Model decisions are scripted; native Git, artifact storage,
workspaces, hook execution, state transitions, and human-response handling execute
through the pinned c2j 0.0.124 runtime. These checks establish orchestration and
reference identity, not the prose quality of a live model's follow-up brief.

All 18 native merge-chase cases passed, including five new cases for introduced
hooks, failed changed-hook verification, clarification with immutable references,
latest-acceptance reuse, and transient failure recovery without code changes.
Existing changed-hook expectations now require one review instead of two.
The ordinary no-change build and all four self-improvement build cases also passed.
Running the new-hook regression against the pre-change recipe in an isolated
checkout fails: that recipe incorrectly asks for another assessment of the
unchanged candidate rather than proceeding to merge.

Final validation on c2j v0.0.124 (source
`33e2a4de4e99d3a577a38dca4b8de33d43a099ce`):

- Complete adaptive suite: **301 passed, zero failed**, including all 18 merge-chase cases.
- Self-improvement builds through the normal entrypoint: **4 passed, zero failed**.
- Native suite validation, repository `build.sh` checks, documentation links, and
  staged whitespace checks passed.

Runtime commands, using the pinned binary with the local Nix environment:

```sh
c2j test run --directory recipe-tests/adaptive --parallelism 4 --case-timeout 10m
c2j test run --directory recipe-tests/self-improvement --parallelism 2 --case-timeout 10m
```

The observed job was inspected only. These changes do not modify its captured
recipe, historical approvals, or already completed merge.

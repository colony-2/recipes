# Current handoffs, retained history

## Problem and plan

Job `F7M2b6MWxHqAwhXNQOmMc0HEbRL` could not send an agreed request to
JobDB. The agent moved four evidence files as instructed, but the recipe merged
their old paths back into the next request. It then asked the human for more
correction attempts. The evidence was useful; treating its filenames as part of
the agreement caused the failure.

This is a recipes-cell bug and simplification. No c2j changes are needed.

The same defect recurred in job `3LwZeVsMscWBrAU9ox6RuhBEaTo`, running
recipes commit `c7385f04b8d00592242fc71ad1e731955b3f8f69`. Its agent moved five
supporting files and then selected only the three accepted files, but the recipe
retained the original paths and requested more correction attempts. This fix was
rebased onto that upstream commit on 2026-11-11.

1. Use the current agent selection for working documents and outgoing requests.
   Stop implicitly accumulating `coordination/` files. Keep the existing request,
   approved direction, execution assignment, and formal test baseline available.
2. Keep consultation history in its existing records and producing tasks.
   Selecting fewer files must not erase the conversation or accepted assignment.
   Agents can retrieve older outputs with the existing c2j inspection tools.
3. Check the receiver's `handoff.md`, rather than freezing every attachment.
   Preserve the original assignment reference; compare republished copies and
   return substantive assignment edits for receiver revision. Supporting evidence
   can be added, updated, moved, or omitted without a new agreement.
4. Explain this contract in the working, consultation, recovery, and receiving
   prompts. The receiver puts agreed scope and acceptance in `handoff.md` and
   evaluates supporting documents as evidence. Conflicting scope requires a
   revised assignment; an additional log does not.
5. Exercise the public build with real artifact transport and child execution.
   Prove moved and omitted files stay omitted, selected evidence arrives, history
   survives, and changed assignments still cannot silently execute.

The existing `files` response is the single current selection. An agent can name
an unchanged inbox file without copying it. `handoff` chooses the portion of that
selection to send to a child. There is no new manifest, registry, approval step,
or task. Required-file and safe-path checks remain.

## Validation

Acceptance is defined before implementation in
[handoff document test statements](../../recipe-tests/adaptive2/handoff-documents-statements.md).
Native tests script agent decisions; they test recipe behavior, not model judgment.
Existing running jobs retain their captured recipe; this change does not mutate
or answer them.

## Implementation assessment

The implementation follows the plan without adding orchestration nodes or a new
document format:

- `develop.yaml` no longer retains all `coordination/` files between working
  turns. Existing consultation records still contain the original conversation
  and artifact references.
- `accepted-handoff.yaml` compares and restores only `handoff.md`. The attachment
  allowlist and its special `feedback/` and `recovery/` exceptions are removed.
  Those directories remain useful conventions, not permission categories.
- Working, recovery, receiving, and consultation prompts explain current
  selection, direct reuse of inbox files, and retrieval of historical outputs.
- Existing human approval, formal test expectations, child lifecycle, safe-path
  checks, and assignment correction remain in place.

The three new public-build regressions failed against the previous recipe and
pass with these changes. A separate native check confirms that updated supporting
evidence is forwarded without comparison against an earlier attachment. Existing
assignment-rewrite tests and new missing-assignment/unsafe-path tests also pass.

The receiver-authored assignment is still protected by a byte comparison when
republished. This intentionally preserves the existing ownership rule: requesters
ask the receiver to revise its assignment. Interpreting contradictory evidence or
deciding a material scope change remains agent work, supported by the existing
planning and approval-recovery checks. The tests do not measure that judgment.

Reproduce with the pinned c2j `v0.0.124`:

```sh
c2j test run --file recipe-tests/adaptive2/handoff-documents.test.yaml --case-timeout 2m
c2j test run --file recipe-tests/adaptive2/accepted-recovery.test.yaml --case-timeout 2m
c2j test run --file recipe-tests/adaptive2/handoff.test.yaml --case-timeout 2m
c2j test run --directory recipe-tests/adaptive2 --case-timeout 10m --parallelism 2
c2j test validate --directory recipe-tests/adaptive2
bash build.sh
```

Previous results on 2026-11-10:

| Check | Result |
| --- | --- |
| New public-build regressions against the previous recipe | All three failed, exposing rejected evidence and retained old paths. |
| New public-build regressions after the change | All three passed, including actual receiving-child inbox assertions. |
| Adaptive2 native regression suite | All 110 distinct cases passed across the initial run and unchanged timeout reruns. |
| Structural validation | All 110 cases validated. |
| Repository purpose check (`bash build.sh`) | Passed. |

The initial parallel native run used a three-minute per-case timeout: 105 cases
passed and five long human-review/merge cases timed out. All five passed unchanged
with a ten-minute timeout and lower parallelism. No assertion or recipe limit was
relaxed. The commands above use the longer runner timeout for reproducibility.

## Rebase verification on 2026-11-11

Rebased onto recipes main `c7385f04b8d00592242fc71ad1e731955b3f8f69` and
validated the isolated staged changes, excluding unrelated workspace edits.
The CLI was updated to c2j main `a97a6b3d50444a8a4cc75ce34ff46e358f2a60fb`
(`v0.0.125-0.20261111033229-a97a6b3d5044`). Both upstream revisions were
rechecked during validation.

| Check | Result |
| --- | --- |
| Full adaptive2 native regression run | All 110 cases in 27 suites passed in one completed run; ten-minute per-case timeout, parallelism two. |
| Focused public-build handoff regressions | All three passed, including materialized child inboxes and retained consultation history. |
| Accepted-assignment checks | All three passed: unchanged assignment, revised supporting evidence, and rejection of an assignment rewrite. |
| Structural validation on c2j main | All 110 cases validated. |
| Repository purpose and local-link checks (`bash build.sh`) | Passed. |
| Patch whitespace checks | Passed. |

Initial attempts encountered local Nix setup failures before recipe assertions.
The completed run used Nix 2.34.8 with the portable store exposed at `/nix`, a
writable temporary cache, and the published c2ops package restored from its
public cache. No recipe assertion, mock, or acceptance requirement was changed
to accommodate the environment. The earlier interrupted or setup-failed runs
are not counted as passing validation. The repository's release pin remains
`0.0.124`; the main CLI was used explicitly for this verification.

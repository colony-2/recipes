# Make adaptive2 the default build

The public `build.yaml` now runs adaptive2. This follows the initial document
trials, the owner-voice revision, and the request to try the new flow through the
normal build entrypoint. No blocking recipe issue was found in the focused native
checks. It is a rollout for further human evaluation; the
remaining live-trial limitations below are still open.

## Changes

| Area | Result |
| --- | --- |
| Public entrypoint | `build.yaml` version 3.0.0 includes `recipes/adaptive2/workflow.yaml`. Existing input names and defaults remain, except the default consultation selector now names adaptive2. |
| Work framing | Delivery begins with a feature, bug, or oversight one-pager and an explicit direction review. A completed explanation can return its answer immediately. |
| Outputs | `process` is `adaptive2`; `classification` and new `work_kind` use `feature`, `bug`, `explanation`, or `oversight`. Review receipts distinguish direction and outcome. Consumers expecting the old heavy/direct classification need adjustment. |
| Child builds | The normal named `build` selector is preserved. With the shared entrypoint it runs adaptive2; explicit repository-local build overrides and `build_recipe` inputs remain honored. The standalone adaptive2 entrypoint uses the same default. |
| Consultations | The default runs adaptive2 inline. The receiving cell writes the agreed typed handoff. The parent forwards its original files and any selected recovery evidence. |
| Shared mechanisms | Existing package checks, managed workspaces, native Git, verification, child inspection, and bounded recovery remain. Root-owned cell creation is unchanged. |
| Documentation | The README, current process diagram, hook guide, testing guide, and documentation map describe the new default. Earlier proposals and trial reports are labeled as the preceding milestone. |
| Previous regressions | Old adaptive suites explicitly use a test-only copy of their former entry contract. They continue to exercise the old flow and shared helpers; their passes are not counted as adaptive2 branch coverage. |

The commit also records the previously uncommitted adaptive2 implementation,
plain-language changes, native fixtures, and original generated review packets.
The [initial implementation assessment](IMPLEMENTATION.md) and
[writing iteration](PLAIN_LANGUAGE_ITERATION.md) describe that earlier work.

## Validation

The public-entrypoint cases cover direction approval, cancellation, revision,
unanswered review, explanation completion, exact approved-artifact retention,
fresh implementation, and outcome review. Additional cases cover actual native
merge, response correction, failed or missing required verification and repair,
publication failure after merge, and invalid annotations.

A native child case resolves the normal named `build` from the submitting
repository, uses the actual public entrypoint and include tree, enters the storage
cell's managed workspace, and stops at its direction review before implementation.
It uses the original receiver-authored handoff, not a substitute child recipe.
The existing handoff tests continue to reject rewritten assignments and allow
selected recovery evidence with the original.

The four self-improvement cases now run the public adaptive2 path. They exercise
configure and verify hooks, preserve supplied audit evidence, require no audit
deliverables for an ordinary request, and return a concrete inspection failure
without asking an unrelated human question.

The repository-wide native run on 2026-11-09 finished with **407 passing cases and
18 failures**. All 23 adaptive2 cases and all four self-improvement/hook cases
passed. The previous adaptive suites passed 305 cases. Two opt-in live suites
were excluded by the normal runner.

The failures are the 18 creation-fixture failures already documented in
[`recipe-tests/SKIPPED.md`](../../recipe-tests/SKIPPED.md), across `create`,
`create-handoff`, and `creation-publication`. These cases remain enabled. The
creation recipes and fixtures are unchanged, and `create-approved-set` reproduced
the identical `publish-cells.publish.sequence: invalid_request` failure in a clean
checkout of baseline `33f6474`. The harness cannot supply its generated repository
identities to the mocked proposals; see the existing
[c2j fixture requirement](../FEATURE_REQUEST_C2J_RUNTIME_FIXTURE_REFERENCES.md).
This rollout neither fixes nor hides that limitation. No new failing case was found.

Commands used the pinned c2j 0.0.124 with its existing Nix/proot package environment:

```sh
c2j test run --directory . --case-timeout 3m --out-dir /tmp/adaptive2-default-full
c2j test run --file /tmp/adaptive2-default-baseline/recipe-tests/create.test.yaml \
  --case create-approved-set --case-timeout 3m \
  --out-dir /tmp/adaptive2-default-baseline-result
```

The baseline command ran against the detached previous commit; its expected
reproduction failed. Full reports remain at the paths above. The first focused
run caught an added assertion that expected successful top-level outputs after
publication failure; that assertion was removed, retaining checks that merge
occurred and the failure was reported. The final full run passed that case.

Model responses and review answers are scripted in these tests. They verify orchestration,
artifact transport, Git, and hook behavior; they do not establish prose quality.
The [live document packets](results/README.md) are separate evidence of that quality.

## Remaining limits

- One larger UI framing trial timed out after producing documents but before its
  final model response. Its cause remains unresolved; the retained files are
  labeled as incomplete drafts. Later smaller bug and consultation trials passed.
- A full live implementation-to-merge cycle and a live multi-owner oversight and
  recovery trial remain to be done. Native delivery tests are not substitutes.
- Each delivery child currently has its own direction review. Reuse of an approved
  parent brief and prerequisite execution during planning are planned, not enabled.
- Explicit child recipe overrides can select another workflow. Default remote
  selectors follow published `main`; they do not pin every child to the parent's
  captured recipe revision.

## Trying the change

Publish the commit to the recipe source used by the JobDB, then submit fresh jobs
through the ordinary `build` entrypoint. Existing jobs retain the recipe they
captured; restarting an old execution does not test this new default. Local native
runs already consume this checkout directly. This change does not modify or submit
production jobs.

Start with a small bug or feature. Inspect the first one-pager, its approval title,
and any consultation exchange before approving implementation. Then review the
outcome brief against that approved direction. Keep job IDs and concrete confusing
passages for the next wording or flow adjustment.

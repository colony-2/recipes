# Plan for publish hook repair and promotion

**Require separate reviewed changes for publisher behavior and product behavior** in cells adopting this protocol. Keep the publish hook, its private helpers, and their tests together. Use Adaptive3’s existing implementation, verification, outcome review, and integration cycle for repairs. Hook editors continue to edit one publisher. Adaptive3 selects the fallback, validates the evidence, and writes the promotion commit.

This proposal addresses a failure we observed twice in the same cell. Both SDK changes landed on `main`. The first release job closed with an explicit exception for its missing tag. The next reached the Git proxy and failed to create its tag. A successful merge or a successful job is therefore insufficient evidence that a publisher worked. [First SDK job](https://jobs.colony2.com/c2/jobs/HcFQtCCF7hI5oiVwVUy8nN1PRRK) · [Second SDK job](https://jobs.colony2.com/c2/jobs/3MKCAeLDmgT67eBQe6Z8fW1ZKCN)

## Which changes can land together?

The Adaptive3 wrapper enforces this rule before merge admission. It classifies the final reviewed diff against its accepted base after preparation and rebase. A single contribution containing both publisher and product changes goes back to implementation for splitting, even if it would be the only item in a batch. Direct-merge builds apply the same check to their single candidate.

| Change | Proposed behavior |
| --- | --- |
| Product code, dependencies, or release version only | Run the publisher for the exact landed product commit. An already accepted publisher stays pinned across ordinary releases. A separately landed publisher awaiting its first real trial can be exercised here. |
| Publisher only | Land the candidate with the previous working reference intact. Trial it on a genuine release operation. If the destination already contains the unchanged payload and the new behavior cannot be exercised, keep the previous reference and attach the trial to the next eligible release. An already-existing tag alone cannot prove that a new tag creator works. |
| Publisher and product together | Return the diff to implementation before merge. Split it into ordered contributions. For a new format, first land a publisher that understands both formats, then land the payload that uses the new format. If safe ordering is impossible, return to design to settle the transition and its acceptance criteria. |
| Adaptive3 promotion record only | Validate the trusted receipt and update the reference. This bookkeeping commit skips publication. A mixed diff or a user-authored edit to the record cannot use this route. |

Adaptive3 recognizes the root-relative hook at `.c2/recipes/hooks/build/publish.yaml` and private includes, helpers, or tests kept under its sibling `publish/` directory. A helper-only edit there counts as a publisher change. The Git comparison counts both sides of a move and includes deletions. A release version consumed as data belongs to the product. For hooks that execute files elsewhere, establish ownership of those dependencies before enabling automatic fallback.

### Run publisher merges inline

With the default merge queue enabled, Adaptive3 inspects the reviewed candidate against its base. Product-only changes use the existing cell and branch queue with up to 50 contributions. For a publisher-only change, the caller includes the same merge recipe with exactly its own contribution, bundle, and verification policy. A mixed change goes back to implementation for splitting. Builds using `merge_queue: false` keep their direct merge and apply the same mixed-change check. [Integration routing](../../recipes/adaptive3/execute.yaml) · [Merge submission](../../recipes/adaptive3/merge-queue-submit.yaml)

The inline merge starts as soon as the approved build reaches integration. It can overtake a queued change, and another merge can land while the publisher is being verified. An exact previously verified commit can reuse its matching verification receipt. The native merge checks the prepared base. If the tip advances, the merge recipe can replay and reverify against the new tip up to three times. Publication uses the caller’s confirmed landed commit. A product that requires the new publisher needs an explicit dependency on its delivery. Release destinations with unresolved external effects still need the separate ordering described below. [Merge recipe](../../recipes/adaptive3/merge-queue-batch.yaml) · [Publisher routing and competing merge tests](../../recipe-tests/adaptive3/publisher-merge.test.yaml)

## Two stages and one working reference

1. **Land and trial.** Suppose publisher A is the last working version and B lands on `main`. The wrapper tries B and retains A’s reference. A build starting from raw `main` can use this wrapper. Pin the release payload and destination for the attempt so a retry still operates on the same release.
2. **Accept and record.** Once B produces the required release outcome, a proposed Adaptive3 step named `record_publish_outcome` writes `publish-receipt.json` as its own task artifact. A separate framework-owned Git commit updates a sidecar next to the hook, such as `publish.accepted.json`, from A to B. This keeps the tested publisher code intact and avoids a commit having to name its own SHA.

The sidecar identifies the accepted publisher source commit and its native JobDB artifact reference, including the producer job, task occurrence or ordinal, and artifact name. The receipt records the trusted wrapper revision, cell, branch, destination, exact publisher implementation, release payload identity, and evidence that the release met its current acceptance criteria. An ordinary successful release with A records the release outcome in JobDB and needs no new pin commit. A release completed by fallback also retains A. The job responsible for delivering B still owns its repair.

Before any external write, verify the inherited reference against the accepted base and retrieve the original receipt from its producer. Check the expected wrapper and step, successful outcome, identities, and evidence. A missing pin is valid only when the accepted base has none. A removed, forged, unreadable, or wrong-destination reference takes the diagnostic route. A legacy hook with no receipt earns its first pin on a verified release. Preserve optional-hook behavior for cells with no publisher. Intentional retirement of a managed publisher requires an explicit reviewed change so deletion cannot silently reset history. [Artifact inspection](../JOB_INSPECTION_PLAYBOOK.md) · [Build hook contract](../BUILD_HOOKS_USER_GUIDE.md)

## Reuse the existing cycle after failure

Adaptive3 already carries the confirmed merge into publication retries. Its integration state can route a `changes` result to implementation, and Backstop handles blocked work and exhausted attempts. Extend that handoff with the release payload, attempted publisher, prior receipt, destination observations, and original diagnostics. Keep the completed merge in the handoff across **every** revision. Cancellation stops the attempt and preserves evidence for later reconciliation. [Integration transitions](../../adaptive3.yaml) · [Execution](../../recipes/adaptive3/execute.yaml) · [Existing hook recovery test](../../recipe-tests/adaptive3/hook-recovery.test.yaml)

| What the wrapper can establish | Next action |
| --- | --- |
| B failed before any external effect, or the destination confirms A can safely resume | Try A once against the **same payload** if it satisfies this release’s requirements. Verify the resulting release, record which publisher delivered it, and keep B’s failure visible. If A and B have the same executable identity, skip the redundant fallback. |
| B may have partially published | Inspect the actual destination. For example, if upload succeeded and updating the index failed, verify the uploaded digest before resuming. An ambiguous timeout stays in recovery until the effects can be reconciled. A hook’s exit code alone cannot authorize a second submission. |
| The publisher needs a code fix | Return to the existing writable implementation cycle. Reverify the fix and use normal outcome review for changed behavior. Trial the reviewed repair from its managed candidate against the retained release payload before landing the fix. If fallback already delivered that payload, use a meaningful remaining acceptance check or await the next eligible release. Preserve the tested publisher source and verify its identity when landing and promoting it. |
| Product code caused the failure | Prepare and review a product fix through the normal build. The corrected product gets a new payload identity and its own release attempt. Carry forward evidence of any external effects on the earlier version. |
| Credentials, infrastructure, or access block progress | Use Backstop to route the concrete prerequisite to its owner. Resume when the prerequisite changes under valid authority. Retries use the existing lifecycle allowances. |

Bind the publisher implementation separately from the payload. A local native test confirmed that a Git-pinned old YAML invoking `sh publish-helper.sh` ran the **new** helper from the execution workspace. Materialize the selected publisher and its helpers together, then give it the approved payload as a separate input. Preserve source trust and per-hook permissions for both invocations. For legacy hooks whose effects or dependencies cannot be established, retain diagnosis and repair. [Runtime hook source semantics](https://github.com/colony-2/c2j/blob/6a5157f513e8325e30b448004c9b0ff209485d69/GUIDE-Local-Recipe-Hooks.md#choosing-the-hook-source)

## Ordering, retries, and delivery

Serialize external writes per destination. Before promotion, compare the current accepted reference with the one the trial started from and verify the selected publisher is still eligible on the target branch. Preserve unrelated changes that have landed. A stale or superseded attempt cannot overwrite a later promotion. If a crash follows receipt creation, finish the metadata commit from the validated receipt. If it follows an external write but precedes the receipt, inspect the destination first. A repeated request for an already accepted receipt succeeds without publishing again.

Keep later publications out of a destination with unresolved effects. Permit the active release’s own repair to proceed without waiting behind that gate. A trial awaiting its first suitable payload has made no external write and may admit that payload. Existing merge grouping ends before the caller publishes, so a publication gate needs its own ordering. This protocol covers callers of the wrapper. External systems observing live writes directly still need destination-specific recovery. [Merge queue lifecycle](../../recipes/adaptive3/README.md#merge-queue)

1. **Recipes** adds receipt validation and a trusted recording step to integration, then exercises bootstrap and metadata-only promotion in a disposable cell. Validate artifact retention and recovery for the supported lifetime of a pin before rollout.
2. **Recipes and c2j** prove independent publisher and payload binding, existing hook authority, destination ordering, and conditional metadata updates under concurrent jobs. Use native workspaces, Git operations, and artifacts where sufficient. Assign any missing execution or storage primitive to c2j or JobDB before enabling automatic fallback.
3. **Recipes and a pilot cell** define publisher-owned paths, current release acceptance, and how to inspect partial effects. Enforce the split on both merge paths, connect the existing repair cycle, then enable automatic fallback for the demonstrated cases. Expand to other cells after the pilot. Hook authors write their release procedure. The shared wrapper owns version selection and promotion.

## Planned native acceptance tests

Extend [hook recovery tests](../../recipe-tests/adaptive3/hook-recovery.test.yaml) and [merge queue coverage](../../recipe-tests/adaptive3/merge-queue-statements.md). Use a retained destination shared across attempts and count its writes. These are implementation acceptance criteria.

| Test statement | Importance | Kind and dependencies | Relevant files |
| --- | --- | --- | --- |
| Product-only publication uses the landed payload and preserves the accepted publisher pin. | Critical | Integration, c2j, Git | `execute.yaml`, `hooks.yaml` |
| A helper-only publisher change enters trial. A mixed submission returns for splitting before either merge path lands it. | Critical | Integration, c2j, Git | `prepare-candidate.yaml`, `merge-queue-land.yaml`, `integration.yaml` |
| A publisher change lands alone through the inline merge while product changes can continue through grouped submission. | Critical | Integration, c2j, Git | `execute.yaml`, `merge-queue-submit.yaml` |
| A competing branch update triggers fresh verification. Publication uses the publisher’s confirmed landed commit. | Critical | Integration, c2j, Git | `merge-queue-batch.yaml`, `hooks.yaml` |
| A first publisher earns its pin on an exercised release. A skipped trial leaves the pin unset. | High | Integration, c2j, Git | `hooks.yaml`, `execute.yaml` |
| A deleted pin, forged producer, missing artifact, or receipt for another destination prevents external writes. | Critical | Integration, c2j, JobDB | `hooks.yaml`, `execute.yaml` |
| A clean failure can deliver the new payload through old publisher helpers. Fallback success keeps the old pin. | Critical | Integration, c2j, Git | `hooks.yaml`, `execute.yaml` |
| A partial upload followed by a lost response preserves the object, blocks overtaking, and resumes only after the destination confirms its identity. | Critical | Integration, c2j, destination fixture | `execute.yaml`, `lifecycle.yaml` |
| Publisher repair reuses implementation, verification, and outcome review, then delivers the original payload without repeating its merge. | Critical | Integration, c2j, Git | `adaptive3.yaml`, `cycle.yaml`, `execute.yaml` |
| A product fix receives a new release identity. An incompatible fallback cannot satisfy the new product’s release requirements. | Critical | Integration, c2j, Git | `adaptive3.yaml`, `hooks.yaml` |
| Restart after receipt creation produces one metadata commit and one release. An older trial cannot replace a newer accepted publisher. | Critical | Integration, c2j, JobDB, Git | `execute.yaml`, `merge-queue-submit.yaml` |

# Exact-commit fast-forward verification: test statements and candidate checks

These expectations were agreed before implementation in the supplied exact-commit fast-forward design. Each statement is at most 30 words. Paths are repository-relative. Execution evidence is reported separately.

## Test statements

| ID | Expectation | Filenames | Priority | Level / dependencies |
| --- | --- | --- | --- | --- |
| FF-01 | The default queued build verifies once and publishes the exact supplied verified commit after outcome approval. | `adaptive3.yaml`, `recipe-tests/adaptive3/default-build.test.yaml` | Critical | Integration / pinned c2j, Git, uv, Nix, scripted decisions |
| FF-02 | An unchanged verified commit fast-forwards without another hook invocation, retaining its original result and evidence. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv, controlled hook |
| FF-03 | Contributions without saved receipts follow ordinary verification and produce valid landing receipts. | `recipe-tests/adaptive3/merge-queue-caller.test.yaml` | Critical | Integration / pinned c2j, Git, uv |
| FF-04 | Reuse eligibility depends on exact publication identity and fast-forward ancestry, without an item-count gate. | `recipe-tests/test_merge_queue.py` | Critical | Unit / Python, Git |
| FF-05 | Duplicate and already-landed appends do not prevent reuse of valid evidence for the exact remaining publication head. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | High | Integration / pinned c2j, Git, uv |
| FF-06 | Individually passing contributions cannot skip verification of a combined stack whose tip differs from every supplied verified commit. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv |
| FF-07 | Rebase, repair, squash or metadata changes require fresh verification when they change the commit, even if file trees match. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv, candidate variants |
| FF-08 | Missing, malformed, failed or operationally failed receipts cannot bypass verification. | `recipe-tests/test_merge_queue.py` | Critical | Unit / Python |
| FF-09 | Foreign producer identities and receipts for another source commit or original base cannot authorize reuse. | `recipe-tests/test_merge_queue.py` | Critical | Unit / Python |
| FF-10 | Changed verification requirements, settings or directories prevent receipt reuse. | `recipe-tests/test_merge_queue.py` | Critical | Unit / Python |
| FF-11 | Equivalent settings with reordered object keys retain eligibility. | `recipe-tests/test_merge_queue.py` | High | Unit / Python |
| FF-12 | Contradictory duplicate evidence disables reuse in either append order without rejecting otherwise valid source work. | `recipe-tests/test_merge_queue.py` | Critical | Unit / Python |
| FF-13 | Consistent duplicate receipts retain eligible evidence despite different producer identities or log locations. | `recipe-tests/test_merge_queue.py` | High | Unit / Python |
| FF-14 | Optional skipped verification stays visibly skipped; required verification cannot reuse a skipped result. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv, optional-hook control |
| FF-15 | Subset probes and final checks reuse qualifying exact-head evidence; selection history cannot certify a different head. | `recipe-tests/adaptive3/merge-queue-selection.test.yaml` | Critical | Integration / pinned c2j, Git, uv |
| FF-16 | Empty baseline checks retain their existing verification behavior. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | High | Integration / pinned c2j, Git, uv |
| FF-17 | Existing source, bundle and history validation still rejects invalid contributions despite supplied passing receipts. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv, invalid-source variants |
| FF-18 | Non-fast-forward targets cannot authorize reuse, and unsafe publication never force-updates branch history. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv, diverged remote |
| FF-19 | Target ancestry governs publication eligibility without requiring equality to the receipt base, while ordinary contribution validation remains enforced. | `recipe-tests/test_merge_queue.py` | High | Unit / Python, Git |
| FF-20 | Upstream races preserve the merge guard; retries verify any rewritten candidate before publication. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | Critical | Integration / pinned c2j, Git, uv, advancing remote |
| FF-21 | Re-entered checks recompute eligibility for the current head and target rather than trusting an earlier reuse decision. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | High | Integration / pinned c2j, Git, uv, repeated-check fixture |
| FF-22 | Dirty workspaces, unreadable required Git objects and repository failures cannot be reported as successful reuse. | `recipe-tests/test_merge_queue.py` | Critical | Unit / Python, Git |
| FF-23 | Reused evidence preserves original context and readable log bytes without replacing assembly, conflict or repair artifacts. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | High | Integration / pinned c2j, Git, uv, colliding artifact names |
| FF-24 | Unreadable stored evidence reports a retrieval failure instead of claiming successful evidence validation. | `recipe-tests/adaptive3/merge-queue-fast-forward.test.yaml` | High | Integration / pinned c2j, Git, uv, artifact-read fault |
| FF-25 | Reuse preserves caller confirmation and publish-hook execution at the confirmed landed hash. | `recipe-tests/adaptive3/merge-queue-caller.test.yaml` | Critical | Integration / pinned c2j, Git, uv, publish hook |
| FF-26 | Already-landed retries confirm their original hash without creating another commit. | `recipe-tests/adaptive3/merge-queue-caller.test.yaml` | High | Integration / pinned c2j, Git, uv |


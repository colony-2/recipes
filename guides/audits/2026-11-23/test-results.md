# Adaptive3 pilot evidence

## What changed in a real turn

On the native failed-verification fixture, the first writable author prompt contained 789 words. Its resumed repair contained 64, including the reviewer’s original words and the operation’s identity and paths. The author received the failing diagnostic, kept its checkpoint, repaired the candidate and passed the second check. The fresh orientation supplied 64 additional words. The resumed call supplied none. These counts describe one fixture. [Candidate and repair test](../../../recipe-tests/adaptive3/lifecycle.test.yaml)

Nine recovery-action cases now run the extracted predicate directly. They cover available, absent, null, empty and whitespace actions, plus four invalid or unavailable stage choices. The leaf suite is 65 lines. Its nine cases took 0.15–0.22 seconds each in one run. Seven repeated full-flow cases were removed. The broad suite and leaf together went from 1,650 lines to 1,070. A retained null-action case still exercised the real discussion and form and took 105 seconds on the same c2j binary. Local load varied. [Predicate tests](../../../recipe-tests/adaptive3/backstop-action.test.yaml) · [Retained discussion cases](../../../recipe-tests/adaptive3/backstop-actions.test.yaml)

## Fresh model sample

Six independent, read-only Codex calls used `gpt-6.2-sol` with its default reasoning setting. Each author saw the Implementation instructions relevant to the decision and a synthetic record. Each reviewer saw the Outcome review instructions, the same evidence and the author’s actual reply. These were text judgments without tools, schema enforcement or a live scheduler.

| Evidence presented | Author's decision | Reviewer's decision |
| --- | --- | --- |
| The existing dependency waited until B finished. Reservation was a design suggestion. | Send for review with the observed ordering. | Covered. |
| The dependent job started one minute before B finished. Its unit test passed. | Repair the scheduler check. | Repair Implementation. |
| The requester explicitly required the scheduler trace. Only the passing test was available. | Stuck because the trace was unavailable in the sample. | Repair Implementation to supply the missing trace. |

The reviewer kept the promise and required method distinct in all three examples. The third author response leaves an open field question. In an equipped worker, does it obtain an available trace before escalating?

## Native checks

The test runner came from c2j main `a6de3eca42509bb9caac1ac2f8af74b37319c192`. Test jobs used disposable cells. Model responses were scripted for routing checks. The six observations above sampled model judgment separately. [Runner pin](../../../.c2j-version)

| Boundary | Evidence |
| --- | --- |
| Parent routing | Several native include sites supplied ordered responses. The public parent took Implementation → Outcome → Implementation → Outcome for a code defect. A wording correction reached Outcome with the existing approval. A stalled check reached the delegate with its diagnostic and the correction returned to Implementation. [Routing cases](../../../recipe-tests/adaptive3/pilot-routing.test.yaml) |
| Approval and repair | A public feature with full Preparation approval completed native verification and Outcome coverage before merge. Independent cases checked equivalent proof, a broken wait, an expressly required trace and a presentation edit. [Public build](../../../recipe-tests/adaptive3/build.test.yaml) · [Assessment](../../../recipe-tests/adaptive3/validation-feedback.test.yaml) |
| Human review | All 13 native review cases passed. In three recovery cases the generated reports were 51–68 words. Each opened with the blocker. When an action was available, it came next. A failed investigator still produced a readable form. [Review cases](../../../recipe-tests/adaptive3/review.test.yaml) · [Delegate reports](../../../recipe-tests/adaptive3/backstop.test.yaml) |
| Existing work and permissions | A malformed author report after a real child submission produced one submission and one wait. The author received that exact job's failure before completing. Allowed and denied include grants were exercised. [Child recovery](../../../recipe-tests/adaptive3/child-recovery.test.yaml) · [Permissions](../../../recipe-tests/adaptive3/reuse-permissions.test.yaml) |
| Consultation | All nine cases ran. A storage question ended after the answer, including when a receiver offered a change and when advice was nested. An explicit change request could end with an agreement, a decline or delivery. [Consultation tests](../../../recipe-tests/adaptive3/consultation.test.yaml) |
| Environment and adapter | A consumer cell with no Recipes checkout received the offline guide at the native selector boundary. Omitted settings inherited worker defaults and an explicit effort override preserved the worker model. The published source for each of the four linked guide pages returned HTTP 200. [Adapter tests](../../../recipe-tests/adaptive3/agent-settings.test.yaml) |
| Merge queue | A receiver restarted after a failed publish. Another batch published first. An unrelated successful job kept the caller open. The repair with the retained original assembly completed the caller without a second merge. [SQLite and Git scenarios](../../../recipe-tests/adaptive3/queue-publication-scenario.test.json) |
| Repository checks | All 36 Python validator tests, 21 merge-queue tests, timeout policy across 139 files and the repository build passed. c2j validated 1,057 declarations across 188 suites and excluded three live scenarios. All 22 native cases in the focused Backstop hook passed. The full runtime suite remains a pre-merge check. [Verify hook](../../../.c2/recipes/hooks/build/verify.yaml) |

The pinned CLI matched a Docker check to an Ubuntu offering in a disposable catalog and rejected KVM on that same offering. The lab tenant returned `not_configured` on a read-only catalog lookup. Live Docker allocation and human readability of the revised forms still need field observation. The exact-output regression also retrieved an attachment beyond the first page. [Agent guide](../../../recipes/adaptive3/prompts/context.yaml) · [Inspection case](../../../recipe-tests/adaptive3/inspection.test.yaml)

Reproduce a focused suite with `c2j test run --file recipe-tests/adaptive3/pilot-routing.test.yaml`. Use `c2j test validate --directory .` for declarations. For the complete pre-merge run use `bash scripts/test-recipes.sh /tmp/recipes-verify`.

## Control and rollout

The audit’s 200 jobs predate the counter fix. A separate read-only search from November 23 07:10:27 through 20:35:05 UTC examined jobs under the 140 newly created goals returned for that window. It found two eligible c2j builds at control revision `6b5a701c`. They had visited Direction and Preparation, with 2/4 and 1/2 cycles respectively. Both were still READY. Jobs attached to older goals could be absent from that narrow control search. It cannot estimate a terminal escalation rate. [First control job](http://db.lab.c2.run:8081/c2/jobs/6sQ7bnwYhfgRHF5LEOX4be8mhZa) · [Second control job](http://db.lab.c2.run:8081/c2/jobs/B99FIWNf8JSL7M08KPWlGFoAjrc)

Production rollout and both 100-build observation windows remain pending. Count distinct builds entering Backstop in their own execution, record the actual phase visits and cycle counts, and report Git infrastructure incidents separately. Inspect failures and missed defects alongside the escalation rate. [Cohort rules](inventory.md#which-rate-to-use) · [Rollout plan](improvement-plan.md#rollout-and-decision-to-continue)

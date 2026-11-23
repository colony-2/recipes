# Adaptive3 pilot implementation

Adaptive3 keeps two authors and an independent reviewer. The planning author can propose how to test a promise. The implementer can show a better test. A method the requester explicitly chose still counts. “Show me the result” requests a final review. “Finish if verified” lets the existing approval cover a result that meets the promise. The original decision and its receipt travel with the handoff. [Review wording](../../../recipes/adaptive3/prompts/review.yaml) · [Principles](../../adaptive3/PRINCIPLES.md)

| When | What changes |
| --- | --- |
| A reviewer finds a code defect at Outcome | The writable author gets the finding. A verified implementation needing only a report edit goes forward to the Outcome author with the correction and earlier approval. |
| Implementation retries | A continuing author gets the diagnostic and relevant review reply. A fresh checkpoint gets the assignment and orientation. One author-requested local retry is available. A second identical named failure without verified progress ends the local loop. Older hooks with only free text keep the finite visit limit. |
| One cell asks another how something works | The answer returns directly. Only the requester opens negotiation. The receiver can ask a question, decline or offer terms. A separate delivery requires agreement and the existing planning checks. |
| A person needs to decide | The title names the issue. The delegate’s report opens with the blocker and suggested action. The original request, work and sources follow. A review reply travels with its recorded actor. |
| An agent needs help with C2 | Every agent receives an offline task guide. It covers worker bases and capabilities, packages, exact job and review lookups, child work, publication and escalation. The short orientation points to it. |

## Pilot revisions

Apply through the existing build entrypoint. Each revision includes its predecessors. Leave jobs already in flight on their captured recipes. [Rollout measures and stop conditions](improvement-plan.md#rollout-and-decision-to-continue)

| Revision | Change to observe |
| --- | --- |
| `370c70e` | Pin c2j main. Replace 16 agent call declarations with four using optional inputs. Adopt exact receiver jobs for publication recovery and attach the C2 guide. |
| `9b2f607` | Approve the promised behavior, distinguish suggested checks and attribute review replies. |
| `7d0b1b3` | Shorten only the resumed Implementation repair turn. |
| `67bdc03` | Route defects and wording edits to their owners and bound local repair. Test the public parent's actual include sequence. |
| `fe7f891` | End consultation on an answer. Keep exceptional assistance with the delegate. Isolate the recovery action decision. |
| `559da5f` | Preserve the exact publication repair reference across another attempt. Check automation attribution and phase-specific reviewer outcomes. |
| `bd6c75f` | Keep the original review words and attachments on a repair. Finish nested advice on the answer. Exercise the delegate's return to the implementer and check retained queue records across pages. |
| `e388505` | Lead the delegate report with the blocker and action. Keep tool-installation guidance with planning and tool decisions. Attribute quoted feedback to the actor listed on the receipt. This is the integrated pilot candidate. |

The c2j pin also retires shared goal waits. After a group has merged, recovery can consume a separate publication job only when its retained queue assembly belongs to the original receiver and its source matches the original native merge. Each caller still checks its own Change-Id on the branch. A later independent batch cannot release an earlier caller. [Queue recovery](../../BUILD_HOOKS_USER_GUIDE.md#queue-receipt-and-upgrade)

The job audit found 36 of 90 builds entering Backstop and 38 trips straight from Implementation through Backstop and back. The changes above provide shorter alternatives. Field impact requires new jobs on a deployed revision. Hold the session-count experiment until repair routing stabilizes. Compare missed defects, delivery and human corrections as well as the target of one or two exceptional visits per hundred builds. [Audit](audit.md) · [Local evidence](test-results.md)

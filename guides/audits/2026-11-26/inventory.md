# November 26 review inventory

The cohort is the union of two snapshots of pending human input on the `c2` tenant at `db.lab.c2.run:9047`. At 00:08 UTC, 14 jobs were waiting. At 19:18 UTC, 13 were waiting. Seven jobs appeared in both. Five of those seven had a new form. The mac01 operator question and the older Recipes merge request were the same outstanding forms. Six jobs entered the queue and seven left. Jobs that entered and left between snapshots are outside this cohort.

I queried all 23 registered cells for the native input-collection route and checked the tenant-wide ready list. I read 79 recorded form requests across the 20 jobs, their available replies, and the primary documents for the interval and current queue. The comparison counts form generation from 00:08:00 through 19:18:15 UTC. A document count is the number of named references on the form, including the primary. References can recur across forms. These counts do not measure storage duplication, downloads or reading time.

All 31 new forms carried a primary document. They offered 288 document references in total, with a median of seven per form. Four replies reused every exact document reference from the preceding form in their thread. These were two Codex retry explanations, one timed-retry clarification and one labels clarification. No new form had question text identical to its immediate predecessor in the same job. Whether a decision was repeated required reading the exchange. Nineteen jobs resolved recipe sources at `f4948656`. The older Recipes job resolved `919a8452`. This cohort therefore cannot establish the field effect of the later local changes.

## Waiting at 19:18 UTC

| Job | New forms | Files on waiting form | What the exchange shows |
|---|---:|---:|---|
| [Cortex · DAG browser repairs](https://jobs.colony2.com/c2/jobs/3Mbh2RCm7sNR3kGMzhTuaClekmX) | 3 | 32 | The requester approved keeping two visible fixes, then explicitly directed Cortex to combine the migration fixes and land. The latest form restates that instruction and asks to approve the checks. |
| [Cortex · Typing jumps](https://jobs.colony2.com/c2/jobs/3McO3PDMSul8iEKaPoEg3vla7vH) | 4 | 18 | Four successive completion approvals led to another question about the shared browser baseline. The latest asks about eight pixels of Original request spacing, which the DAG owner was already asked to fix. |
| [c2j · Job labels](https://jobs.colony2.com/c2/jobs/NxQOW4rkdSt6KxtA7W8QI9I8bsK) | 3 | 6 | The requester accepted the existing document listing, then asked what a metadata lease was. The answer reused all six files and asked again about the plan. Approving this plan was described as leaving implementation for a separate decision. |
| [c2j · Timed retries](https://jobs.colony2.com/c2/jobs/Cu60BU3yaA1xSW9r0xLeqyYydQ2) | 2 | 8 | A request to explain “parked” produced a useful account of where retry state lives, followed by another request to proceed. Both forms carry the same eight files and offer only **Revise**. |
| [c2ops · Offline provider mirror](https://jobs.colony2.com/c2/jobs/R5xW1eALi1HxQ63Txm3S0Y0LmcO) | 1 | 3 | The scope is agreed. The form asks whether to keep going with the generated attachment labels or make another run to change them. |
| [pgjobdb · Archive checker](https://jobs.colony2.com/c2/jobs/LHSBNI2xc1aLdWXB5hvvyVK20la) | 1 | 4 | Both owners accepted the checker work. The form asks Root whether the generated report must be fixed before work proceeds. |
| [pgjobdb · Lease timestamp](https://jobs.colony2.com/c2/jobs/3Ma82aw2kRdhI9UvgfMU7AbWS8Z) | 2 | 9 | Permission for an upstream append fix preceded a materially different format-16 migration proposal. The second decision deserves a clear approval action. Its only button is **Revise**. |
| [JobDB · Native verification](https://jobs.colony2.com/c2/jobs/3MaP2ed5BEnYN9cy6OZRVzsRuuE) | 3 | 7 | JobDB moved from requesting runner permission to reporting a real missing Darwin verdict. After a connection reset and a corrected address it reached Pulse, but still needed historical launch evidence. Direct that evidence request to the operator and keep the merge blocked. |
| [act · Local verification](https://jobs.colony2.com/c2/jobs/3MaP2idjFZQDjwPpgmu1X6NRzIj) | 1 | 4 | The revised plan honors the local-runner instruction and reports offline build failures. It bundles approval of the plan with a request for contacts at cells it already identifies. |
| [macVZ · Agent package](https://jobs.colony2.com/c2/jobs/3MaP2kRI3WNr7CDRbWhR3EXS65U) | 1 | 5 | The requester already directed the owner handoff. The latest form reports the owner, failure and readiness to forward it. No repair has been dispatched. The handoff belongs with the owner. |
| [macVZ · Crash-report retention](https://jobs.colony2.com/c2/jobs/3McQC2wENfm8NBWAscfsHV6Gb2D) | 0 | 0 | The same operator question remains open. It says exactly which records to look for and provides a **Send operator reply** button. |
| [Pulse · HTTP listener](https://jobs.colony2.com/c2/jobs/3MednNRs54u3Fq13cxCR8uyJefC) | 1 | 1 | The form answers the configuration question in its message and offers **Accept answer**. The guide is available for detail. |
| [Recipes · Inactive document feedback](https://jobs.colony2.com/c2/jobs/GkhYoi7MYLb3vLwaZ32r1mBB49b) | 0 | 24 | The November 23 merge decision is still open. Its old buttons and original outcome are carried forward. It generated no repeat form in this interval. |

## In the earlier queue only

| Job | New forms | What happened |
|---|---:|---|
| [c2ops · Codex stability](https://jobs.colony2.com/c2/jobs/3McLeFBVnmC8GJQNkRJi3LeFho9) | 6 | Two questions about existing retry behavior were answered using the same four-file plan. The job later asked for permission to discuss the design and then presented an actual two-cell design choice. It is waiting for dependent work. |
| [Cortex · Drop targets](https://jobs.colony2.com/c2/jobs/3McOGSoghm10SMBeslWjJG44i82) | 0 | The requester selected **Take to Completion**. The job is waiting on dependent work. |
| [Cortex · Inbox HTTP repairs](https://jobs.colony2.com/c2/jobs/3McL7JKHVTJyIej91tvhe7Yl2pP) | 1 | The job acknowledged approval to return the tested patch but presented another form asking someone to release the parent's wait. The child was subsequently cancelled. |
| [Infra · Offline bootstrap](https://jobs.colony2.com/c2/jobs/3MaP2eb7O7VVwK0McOyRKHzHwB6) | 0 | The existing review was answered. The job moved to waiting on dependent work. |
| [JobDB · Initial history](https://jobs.colony2.com/c2/jobs/3McQ7WcVJvZjuoZTgTf3o2nCT0o) | 1 | The requester chose to ship the chapter fix first. A subsequent plan retained that decision, was approved and the job completed successfully. |
| [JobDB · Storage report](https://jobs.colony2.com/c2/jobs/3McIaNj6OkyghML9WbRZDjoXKYJ) | 0 | The amended answer was accepted and the job completed successfully. |
| [Root · Cell archiving](https://jobs.colony2.com/c2/jobs/3McKGRdrgR0hzrDobkPksLQcIuH) | 1 | After the initial approval, a checker misidentified the main module. The person approved publishing the checker correction. Root is waiting on dependent work. |

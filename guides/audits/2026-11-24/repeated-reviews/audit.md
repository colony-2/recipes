# Why four jobs kept asking for review

JobDB recorded 21 human-facing forms across the four requested jobs. Eighteen had answers and three were still open when inspected on November 24, 2026, at 18:27–18:30 UTC. Two jobs show reproducible failures to carry an approved external assignment into implementation. A third asked the human to grant an internal consultation. The fourth added a meaningful test, but presented the entire plan again without identifying that change in the question.

| Job | Forms | What the human was waiting on at the snapshot |
| --- | ---: | --- |
| [c2j lease timestamps](https://jobs.colony2.com/c2/jobs/0983ec11-ec4c-4c41-8f99-09efb51e2a15) | 3 | Plan v3, after full approval of v2 |
| [Cortex project switcher](https://jobs.colony2.com/c2/jobs/3MUJ9HshLaK9WMP7VficJq1NUD0) | 14 | A recovery form after two blank lines split a Markdown table |
| [Cortex sidebar comments](https://jobs.colony2.com/c2/jobs/3e2b2b46a46861f5a822270c8373148a) | 1 | A recovery form before the first plan approval |
| [c2j hook-permission refresh](https://jobs.colony2.com/c2/jobs/3MUV6oKzLhNpXOq5iv4CwARoTDY) | 3 | No human input pending. A candidate had reached the verification hook. |

## Lease timestamps

The first revision was warranted. The initial plan proposed new lease fields. The requester pointed out that the expiry time already existed and asked for one timestamp covering the last successful acquisition or renewal. Plan v2 reflected that correction and received full approval at 07:29 UTC.

Implementation then asked JobDB to deliver the agreed work. Its request changed **“preceding update” to “previous update.”** Replacing that phrase makes the entire request equal to the accepted assignment. The recipe compares the cell and the complete assignment string. A mismatch sends implementation back to Preparation as newly required external work. JobDB agreed again. No delivery child appeared before v3. [Delivery decision in the pinned recipe](https://github.com/colony-2/recipes/blob/c81aa284e462c2bce30a9605f548bfc042fa11c7/recipes/adaptive3/lifecycle.yaml#L107-L119)

Plan v3 appeared at 07:43 in the same review thread. All 46 test rows match v2 byte for byte. The packet grew from 12 to 14 files with another negotiation report and transcript. Its notes record baseline tests and checks to run after publication. The reviewer explicitly said the recorded approval covered the scope. The new version documented activity, but there was no fresh product decision for the human.

## Cortex project switcher

The recipe entered Direction 10 times, Preparation 11 times, Implementation four times, and Backstop six times. Two Backstop visits produced human forms. The forms fall into three sequences.

1. **Questions and genuine changes.** Asking about the proposed catalog configuration and later about an execution token each produced a reply and reopened the existing form. In both cases every document reference and the review ID stayed identical. Separate human replies corrected genuine assumptions about JobDB, current database use, and where the switcher belonged in the account menu.
2. **Four approvals with the same title.** All four packets contained the same 41 test rows. Each opened with a new review ID, an empty conversation, and the same generic approval question. After the first approval the team sought a new, read-only assignment for Root to identify the running lab JobDB configuration. The second packet added that assignment and candidate evidence. The author explicitly requested the first return to add Root. After the second, third, and fourth approvals, the author requested delivery of the same 658-character agreement. All three saved plans listed only pgjobdb and JobDB. Root was missing, even though its agreement appeared in the approved documents. Each delivery request sent the job back to Preparation. The first two repeat forms received approvals. The third received the SQLite clarification described below. The third packet corrected which commit the screenshots and tests came from. The fourth added evidence for the rebased candidate. Those are valuable verification updates. Neither resolved the missing Root entry. [How approval captures assignments](https://github.com/colony-2/recipes/blob/1d7826ec4ebd127a55eb608f0535bac68c07b2a8/adaptive3.yaml#L676-L678)
3. **Later decisions and the current stop.** A candidate existed and managed verification produced evidence. The requester clarified that stock SQLite testing was sufficient, changed the startup URL to omit the tenant, and requested tenant-first UI paths. Review exposed a real collision with existing bookmarks. The revised design resolved it. The remaining finding was two blank lines that put nine checks outside their Markdown table. Backstop verified the repair in a scratch copy and requested a return to the author. The actual recovery inputs had automatic return disabled. Its own form then failed 13 file checks and presented a generic recovery question.

Five presentations used the account-menu plan title, including the later one answered with the SQLite clarification. The four positive answers included one request to review the final outcome. The repeated prompts in that stretch were all **Preparation** prompts. None was the requested final outcome review.

## Cortex sidebar comments

There was exactly one human form. Preparation negotiated with c2j about the API and CLI, JobDB about durable storage and SQLite, and pgjobdb about PostgreSQL. The plan already contained 38 proposed checks. Earlier probes found two concrete handoff issues. A sidebar passed as an ordinary upload could turn a legacy approval into a revision, and the standalone Ask export omitted the notes.

The proposed next action was to ask Recipes how to pass the file through those paths. The author reported being stuck after using the three-consultation allowance. The fourth conversation was never attempted. The delegate entered with automatic recovery enabled, zero automatic returns used, and permission to send the author back to Preparation. It chose to ask the human for another consultation. The displayed question then reported six file errors. Its links to the three planning documents and three negotiation reports all failed validation. [Consultation limit and routing](https://github.com/colony-2/recipes/blob/c81aa284e462c2bce30a9605f548bfc042fa11c7/recipes/adaptive3/lifecycle.yaml#L107-L119)

## c2j hook-permission refresh

The first form came from an earlier routing failure. Preparation returned `revise_plan` while working through private replay keys. The pinned recipe sent that result to Backstop. The human asked it to open a Recipes ticket. A child job was recorded and subsequently cancelled. [Recorded child job](https://jobs.colony2.com/c2/jobs/3MUZxPZaF7sTearATaDORDOgHNI)

The next day, the first full plan approval covered permission refresh for pinned, import-free hooks. Implementation pointed out that a normal Adaptive build follows candidate hook edits and would still require a new job after a grant change. Switching to base hooks could accidentally verify an older hook. Preparation kept the approved scope, made selecting a first rollout workflow optional for implementation, and added blocking check A5 to protect normal Adaptive builds. The first approved document has 35 test rows and the second has 36. The reviewer’s “unchanged” description compared drafts within the second Preparation pass. It missed the difference from the document the human last approved.

The human approved both plans, 20 minutes apart. They had identical titles, generic approval questions, and different review IDs. This was a real compatibility finding. A focused message could have said “Normal Adaptive builds will still need a new job after a grant edit. We added one test to keep candidate verification working.” That gives the human a clear choice if normal builds were the intended audience. After the second approval, the agent produced a candidate and the recipe entered verification.

## What to change first

1. **Dispatch the agreement the owner accepted.** Remove the plan’s copied assignment list. Hand the implementer a reference to the original agreement, including when it came from a nested conversation. Resolve that reference to start or find the child. Reopen negotiation when the requested work changes materially.
2. **Have the delegate review a repeat decision first.** Before presenting another approval, have the recipe call the delegate. It can apply the existing human decision, send a repair to its owner, or ask about a material change. Preserve an explicit request to review the final result.
3. **Put the difference in the thread.** Answer a question as a message against the existing review. For a new decision, name what changed since the last human-approved version and why it needs them. Keep full documents accessible. A stable review ID helps people find the history. The lease case shows that it cannot, by itself, prevent an unnecessary approval.
4. **Keep conversations bounded and give the author room to consult more owners.** Retain the per-consultation round limit. Start with a proposed ten distinct consultations per phase. Let the delegate resolve an exhausted conversation, assess a request to exceed the phase allowance, or send a concrete repair back to the author. Escalate to the human when their decision would change what happens next. [Correction plan and regression cases](improvement-plan.md)

These are recipe changes. Cortex can make a discussion reply and a new approval easier to distinguish visually. The native history already accounts for the repeated forms in this sample. The jobs were pinned before the latest review-label and unified-reply changes. This audit covers their recorded behavior, with no browser replay or measurement of the frequency across all jobs. [Complete form and stage inventory](inventory.md)

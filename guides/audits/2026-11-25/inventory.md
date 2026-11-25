# Job inventory, November 24–25, 2026

The primary cohort contains 224 recipe jobs created from 20:23:13 UTC November 24 through 20:23:13 UTC November 25 in tenant `c2`. Each job link opens its retained history. Times in the tables are UTC. [Findings and priorities](audit.md)

## Adaptive3 builds

D means Direction, P Preparation, I Implementation, O Outcome, M Integration and B exceptional Backstop. A digit is the number of recorded outer work cycles on that visit. Returning to P starts a new visit. A cycle can contain a real repair, a consultation, or a request to start a child. Forms count messages presented, including answers to questions. An open review and a child wait describe the last task at the cutoff.

| Start | Job · cell | Request | Parent | Recipe | Decision sequence | Forms | Result or wait |
|---|---|---|---|---|---|---:|---|
| 11-24 23:41 | [aaaac418-](https://jobs.colony2.com/c2/jobs/aaaac418-b654-4559-8821-05ce79518355) c2j | Add support for EAGAIN for extension ops | — | 70a38b7c | D2 → P2 → I2 → O1 → I1 → O1 → M1 | 3 | success |
| 11-24 23:43 | [59231eda-](https://jobs.colony2.com/c2/jobs/59231eda-a6e2-439a-9d37-8ff0a05f2b30) cortex | Add Support for "sidebar" comments | — | 70a38b7c | D2 → P4 → B | 1 | cancelled |
| 11-24 23:44 | [3MZhCiRqR](https://jobs.colony2.com/c2/jobs/3MZhCiRqRik9j9YjNpJNalziOSe) jobdb | Implement and publish JobDB last lease update time | [0983ec11-](https://jobs.colony2.com/c2/jobs/0983ec11-ec4c-4c41-8f99-09efb51e2a15) | d93874a0 | D2 → P1 → I2 → O1 → M1 | 2 | success |
| 11-25 02:28 | [2d3d95b9-](https://jobs.colony2.com/c2/jobs/2d3d95b9-cefc-4fcf-83a2-de23d6702112) pulse-docker | pulse provider default capacity | — | d93874a0 | D2 | 1 | success |
| 11-25 02:30 | [6badc59d-](https://jobs.colony2.com/c2/jobs/6badc59d-cb0f-47af-a568-498e5eaa36cf) c2j | Persist caller wait intent | — | d93874a0 | D1 → B → D1 → I1 → O1 → M1 | 3 | success |
| 11-25 03:25 | [3Ma82aw2k](https://jobs.colony2.com/c2/jobs/3Ma82aw2kRdhI9UvgfMU7AbWS8Z) pgjobdb | Adopt and publish PostgreSQL last lease update time | [0983ec11-](https://jobs.colony2.com/c2/jobs/0983ec11-ec4c-4c41-8f99-09efb51e2a15) | f4948656 | D1 → P2 → I1 → P2 → I1 → P3 → I3 → B | 6 | human review |
| 11-25 05:05 | [3MaKC4EJW](https://jobs.colony2.com/c2/jobs/3MaKC4EJWLccFNXZRuLZaU8Ll3C) c2j | dynamic hook permissions | — | f4948656 | D3 → P1 → I2 → O3 → M1 | 2 | success |
| 11-25 05:16 | [3MaLY2L6g](https://jobs.colony2.com/c2/jobs/3MaLY2L6g3nUBQneygaCbyE2GKa) cortex | ui support for projects | — | f4948656 | D4 → P2 → D1 → P1 → I3 → P4 → B → D4 → B → D4 → B → D2 → P2 → I1 → B → I5 → P1 → I1 | 8 | child wait |
| 11-25 05:26 | [3MaMm0UTS](https://jobs.colony2.com/c2/jobs/3MaMm0UTSTnRMuxQ0GI4yvO4EQT) root | Add Labels | — | f4948656 | D2 → P3 → B → D1 → B → D5 → P1 → I1 | 6 | child wait |
| 11-25 05:29 | [3MaNDEVLu](https://jobs.colony2.com/c2/jobs/3MaNDEVLudVOluo964MsstJ1UcK) root | Remove Goals | — | f4948656 | D2 → P3 → B → P1 → B → P1 → B → P1 → D1 → P1 → D2 → P1 → I2 | 4 | child wait |
| 11-25 05:33 | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) c2ops | Add Useful Metrics to Ops | — | f4948656 | D2 → P1 → D1 → P2 → I2 | 2 | child wait |
| 11-25 05:36 | [3MaO3b2Lx](https://jobs.colony2.com/c2/jobs/3MaO3b2Lx8ynKwmSCgOz1kMcaMH) c2j | Project Administration | — | f4948656 | D1 → P3 → D1 → P1 → I4 → O1 → M1 | 3 | success |
| 11-25 05:39 | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) root | verify hooks | — | f4948656 | D1 | 0 | child wait |
| 11-25 05:41 | [3MaOf36tL](https://jobs.colony2.com/c2/jobs/3MaOf36tL7bO8fFdoB4Sn3r9rsd) root | Fix root verify after the JobDB endpoint update | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → I3 → O1 | 1 | human review |
| 11-25 05:44 | [3MaP1pW9Y](https://jobs.colony2.com/c2/jobs/3MaP1pW9YHeX1ZHvWiGOKO0EUfQ) c2j | parallel node | — | f4948656 | D5 → P2 → D1 → P1 → I3 → O1 | 5 | human review |
| 11-25 05:44 | [3MaP2idjF](https://jobs.colony2.com/c2/jobs/3MaP2idjFZQDjwPpgmu1X6NRzIj) act | Add JobDB verification for the act fork | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P2 → I2 → P1 | 2 | human review |
| 11-25 05:44 | [3MaP2f1bC](https://jobs.colony2.com/c2/jobs/3MaP2f1bCwEo9oIyN8cm6AvEGAG) auth | Wire auth tests into the JobDB verify hook | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → B → D1 → I1 → O1 → M1 | 1 | success |
| 11-25 05:44 | [3MaP2eb7O](https://jobs.colony2.com/c2/jobs/3MaP2eb7O7VVwK0McOyRKHzHwB6) infra | Add offline bootstrap verification to the infra cell | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P4 | 1 | human review |
| 11-25 05:44 | [3MaP2hDCv](https://jobs.colony2.com/c2/jobs/3MaP2hDCvCa7GXtgaOQVrLT3ZOR) shai | Add candidate and native-platform verification for shai | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → P2 | 1 | human review |
| 11-25 05:44 | [3MaP2haaC](https://jobs.colony2.com/c2/jobs/3MaP2haaC0PgRUrbmwZFl2cvRyV) vz-macos | Add native macOS verification for vz-macos | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P3 → B | 1 | human review |
| 11-25 05:44 | [3MaP2gTny](https://jobs.colony2.com/c2/jobs/3MaP2gTny122DL2EiQOER4KjSvT) c2j | Cover all published c2j platforms in JobDB verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → B → D2 → P5 → B → D1 → P3 → B → P1 → I4 → B | 6 | human review |
| 11-25 05:44 | [3MaP2ed5B](https://jobs.colony2.com/c2/jobs/3MaP2ed5BEnYN9cy6OZRVzsRuuE) jobdb | Run JobDB verify tests on every published platform | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P2 → D1 → B → D1 → P2 → I1 → O1 → D2 → P2 → I2 → O1 | 6 | human review |
| 11-25 05:44 | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) pulse | Restore Pulse Docker and published-platform verify coverage | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → P2 | 0 | child wait |
| 11-25 05:44 | [3MaP2ipKx](https://jobs.colony2.com/c2/jobs/3MaP2ipKxKyq1tLaSaXbVyiudCz) cortex | Run Cortex checks on every published CLI platform | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P2 → B → D2 → P6 → B → P1 | 3 | child wait |
| 11-25 05:44 | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) gitvend | Cover Gitvend native platforms and Compose in JobDB verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → P2 | 0 | child wait |
| 11-25 05:44 | [3MaP2f4VW](https://jobs.colony2.com/c2/jobs/3MaP2f4VWCJXwLw9OHcE2JsF0v8) pgjobdb | Verify both published pgjobdb Linux targets and omitted test checks | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → P2 | 0 | child wait |
| 11-25 05:44 | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) base | Include smoke-version tests in Base verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → I2 → O1 → D1 → P3 → I5 → O1 | 3 | ACTIVE |
| 11-25 05:44 | [3MaP2kRI3](https://jobs.colony2.com/c2/jobs/3MaP2kRI3WNr7CDRbWhR3EXS65U) pulse-macvz | Cover macVZ host and script tests in JobDB verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P5 → B → P1 | 4 | human review |
| 11-25 05:44 | [3MaP2kOm5](https://jobs.colony2.com/c2/jobs/3MaP2kOm5xRW6j05OhM2AJa7pjz) pulse-tart | Cover Tart host-specific tests in JobDB verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D2 → P2 | 0 | child wait |
| 11-25 05:52 | [3MaPwzzie](https://jobs.colony2.com/c2/jobs/3MaPwzzie5Sxb7OraYzrZcmzWiM) cortex-assistant | Add the documented race suite to Assistant verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → I1 → P1 | 1 | cancelled |
| 11-25 05:52 | [3MaPwz3El](https://jobs.colony2.com/c2/jobs/3MaPwz3Elhwj2eKo4UnOvotOfeg) pulse-docker | Run the Pulse Docker hook-contract suite in verify | [3MaOPBDDZ](https://jobs.colony2.com/c2/jobs/3MaOPBDDZLCS4oOjSTRxo6IeDHY) | f4948656 | D1 → I1 → O1 → M1 | 2 | success |
| 11-25 16:36 | [8lej3piGB](https://jobs.colony2.com/c2/jobs/8lej3piGBxpPnfYBGrNE2CTz68L) jobdb | Recover independently editable job metadata in JobDB | [3MaMm0UTS](https://jobs.colony2.com/c2/jobs/3MaMm0UTSTnRMuxQ0GI4yvO4EQT) | f4948656 | D3 → B → D2 → P1 → D2 → B | 3 | human review |
| 11-25 16:42 | [3Mbh2RCm7](https://jobs.colony2.com/c2/jobs/3Mbh2RCm7sNR3kGMzhTuaClekmX) cortex | Restore the Cortex DAG browser verification gate | [3MaLY2L6g](https://jobs.colony2.com/c2/jobs/3MaLY2L6g3nUBQneygaCbyE2GKa) | f4948656 | D2 → I4 → P2 | 1 | human review |
| 11-25 17:26 | [3MbmPf0wj](https://jobs.colony2.com/c2/jobs/3MbmPf0wjAWwY0E8QulCUrBn1ds) c2j | add a new status field to all recipe nodes, persist on each task output | — | f4948656 | D2 → P1 → D3 → P2 → B | 2 | human review |
| 11-25 17:27 | [3MbmW2Bxc](https://jobs.colony2.com/c2/jobs/3MbmW2BxcHJdtm2umSa6N0NlWzM) cortex | expanded message bug | — | f4948656 | D1 → B → D1 → I4 → P1 | 1 | human review |
| 11-25 17:54 | [UiOXfJCyb](https://jobs.colony2.com/c2/jobs/UiOXfJCyb3nLw5G7TmWyq0Z7jOs) cortex | Remove remaining Cortex goal wiring and require independent restart intent | [3MaNDEVLu](https://jobs.colony2.com/c2/jobs/3MaNDEVLudVOluo964MsstJ1UcK) | f4948656 | D4 → P2 | 1 | human review |

## Which earlier review could the person have seen?

I checked the question and primary document on the earliest human-facing form in each of the 31 builds that presented one. Four contained the literal phrase “since the last review” or “since the previous review.” This narrow count omits ambiguous wording such as “revised plan.” The records establish what each job presented. They do not record whether the person opened a document.

| First form in the job (UTC, Nov 25) | What happened before it | What the human received |
|---|---|---|
| 05:42 · [Cortex project switcher](https://jobs.colony2.com/c2/jobs/3MaLY2L6g3nUBQneygaCbyE2GKa) | The planning author narrowed the plan after internal review. The reviewer passed the revision. | The first 1P opened with “What changed since the last review.” At 06:05 there *was* a human baseline. The person had said the JobDB catalog was already live, and the next plan explained how that changed the proposed default. |
| 06:25 · [Base verification](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | On the short path, the implementation reviewer found that diagnostic output could corrupt the hook verdict. The implementer fixed it and the reviewer passed it. | The first merge question introduced the fix with “Since the previous review.” The person’s first reply asked whether verification actually built a Docker image. |
| 06:34 · [JobDB platform verification](https://jobs.colony2.com/c2/jobs/3MaP2ed5BEnYN9cy6OZRVzsRuuE) | The author and reviewer settled how to report a platform job that failed before uploading results. | The first 1P opened with “What changed since the last review” and described the switch to reading GitHub’s job result. |
| 06:40 · [Infra candidate verification](https://jobs.colony2.com/c2/jobs/3MaP2eb7O7VVwK0McOyRKHzHwB6) | Infra and c2ops negotiated package publication. The reviewer then asked the author to clarify the links. | The first 1P introduced the agreement with “Since the last review.” The accompanying question asked whether the labeled links were sufficient. |

The same confusion appeared even with a genuine earlier human approval. In the JobDB lease-timestamp job, the person approved the plan at 00:01. The author then implemented the field, repaired two tests and passed verification. The internal reviewer requested a report edit. At 03:14 the first outcome told the person that only the report had changed since their last review. That description fits the last exchange between the agents. The person had last been shown the design and tests for the proposed feature. [JobDB lease timestamps](https://jobs.colony2.com/c2/jobs/3MZhCiRqRik9j9YjNpJNalziOSe)

## Open human decisions

These 15 reviews were still open on live builds. Two other unanswered forms belonged to cancelled builds. The notes describe what the person actually sees and where action belongs.

| Job | Stage | Decision before the human |
|---|---|---|
| [3Ma82aw2k](https://jobs.colony2.com/c2/jobs/3Ma82aw2kRdhI9UvgfMU7AbWS8Z) | Backstop | The candidate needs verification and the human requested approval before merge. The current question asks how to record an existing JobDB offer. |
| [3MaOf36tL](https://jobs.colony2.com/c2/jobs/3MaOf36tL7bO8fFdoB4Sn3r9rsd) | Outcome | Outcome review for a bounded Root fixture repair. The hook passed. |
| [3MaP1pW9Y](https://jobs.colony2.com/c2/jobs/3MaP1pW9YHeX1ZHvWiGOKO0EUfQ) | Outcome | The person requested final review. The form is waiting for Accept and merge, while its message says no new decision is needed. |
| [3MaP2idjF](https://jobs.colony2.com/c2/jobs/3MaP2idjFZQDjwPpgmu1X6NRzIj) | Preparation | Whether to authorize a private runner repository, candidate staging and narrowly scoped credentials. This is a material external commitment. |
| [3MaP2eb7O](https://jobs.colony2.com/c2/jobs/3MaP2eb7O7VVwK0McOyRKHzHwB6) | Preparation | Whether the plan can proceed with links despite the recipe-generated attachment labels. The reviewer had already accepted the links. |
| [3MaP2hDCv](https://jobs.colony2.com/c2/jobs/3MaP2hDCvCa7GXtgaOQVrLT3ZOR) | Preparation | Approval of the Shai plan for host and Docker checks. The message distinguishes qualified lanes from Apple Silicon Docker and explains how the hook obtains Go. |
| [3MaP2haaC](https://jobs.colony2.com/c2/jobs/3MaP2haaC0PgRUrbmwZFl2cvRyV) | Backstop | The requester withdrew the work because the cell is being deprecated. The delegate says no implementation decision remains, yet the source job is waiting on another reply. |
| [3MaP2gTny](https://jobs.colony2.com/c2/jobs/3MaP2gTny122DL2EiQOER4KjSvT) | Backstop | Operator evidence for the Apple Silicon child after six leases and no recorded test. A real runner problem. |
| [3MaP2ed5B](https://jobs.colony2.com/c2/jobs/3MaP2ed5BEnYN9cy6OZRVzsRuuE) | Outcome | Final review of revised three-platform scope. The Linux AMD64 evidence is distinct from the other two lanes. |
| [3MaP2kRI3](https://jobs.colony2.com/c2/jobs/3MaP2kRI3WNr7CDRbWhR3EXS65U) | Preparation | Review of a revised ARM64 verify plan after the human supplied platform guidance and requested a capacity retry. |
| [8lej3piGB](https://jobs.colony2.com/c2/jobs/8lej3piGBxpPnfYBGrNE2CTz68L) | Backstop | Who can edit metadata by default and who owns edit history. The previous reply left genuine ambiguity. |
| [3Mbh2RCm7](https://jobs.colony2.com/c2/jobs/3Mbh2RCm7sNR3kGMzhTuaClekmX) | Preparation | Approval to separate two unrelated fixture repairs from the DAG candidate after review found a conflict. |
| [3MbmPf0wj](https://jobs.colony2.com/c2/jobs/3MbmPf0wjAWwY0E8QulCUrBn1ds) | Backstop | Permission to open a JobDB negotiation for a field the requester had already asked to store directly. |
| [3MbmW2Bxc](https://jobs.colony2.com/c2/jobs/3MbmW2BxcHJdtm2umSa6N0NlWzM) | Preparation | Whether to split mobile-title behavior, including a real pending-message truncation defect, from nine existing DAG failures. |
| [UiOXfJCyb](https://jobs.colony2.com/c2/jobs/UiOXfJCyb3nLw5G7TmWyq0Z7jOs) | Preparation | Approval of the Cortex goals-removal plan after reconciling command excerpts. The message emphasizes checking the packet. |

## Other recipe jobs

These are separate jobs in JobDB. They include verification, qualification, publishing, merge-queue and diagnostic work. They are outside the Adaptive3 intervention denominator. The result column is the recorded lifecycle result. A failed application result can be a deliberate diagnostic.

| Started | Job · cell | Recipe | Parent | Result |
|---|---|---|---|---|
| 11-24 21:48 | [3MZT7pJGd](https://jobs.colony2.com/c2/jobs/3MZT7pJGdDUo8DkU2tPaBplkOaa) c2ops | c2ops-verify-only | — | failed_app |
| 11-24 21:49 | [3MZTAg8eG](https://jobs.colony2.com/c2/jobs/3MZTAg8eG2IIpqbOjD7PNRwTU36) c2ops | c2ops-verify-only | — | failed_app |
| 11-24 21:49 | [3MZTCLgKj](https://jobs.colony2.com/c2/jobs/3MZTCLgKjHjqciPgKeah65iwfTN) c2ops | c2ops-verify-only | — | failed_app |
| 11-24 21:53 | [3MZTfg8Cr](https://jobs.colony2.com/c2/jobs/3MZTfg8CrgPvvmvURaUTZfDVNLR) c2ops | c2ops-verify-only | — | cancelled |
| 11-24 22:06 | [3MZVFKRlh](https://jobs.colony2.com/c2/jobs/3MZVFKRlhMwQc8iG1AbNH6p2wuY) pulse-cloudhypervisor | cloudhypervisor-native-inputs | — | success |
| 11-24 22:08 | [3MZVTAtch](https://jobs.colony2.com/c2/jobs/3MZVTAtchTjTQXPrRUxsDmTFCmh) pulse-cloudhypervisor | cloudhypervisor-native-worker-check | — | cancelled |
| 11-24 22:09 | [3MZVfBWCO](https://jobs.colony2.com/c2/jobs/3MZVfBWCOew6Mzoc7NcLr38DNqc) c2ops | c2ops-verify-only | — | failed_app |
| 11-24 22:09 | [verify-9a](https://jobs.colony2.com/c2/jobs/verify-9a65fe7567985e3aabab9c757b740c00) c2ops | verify-platform | [3MZVfBWCO](https://jobs.colony2.com/c2/jobs/3MZVfBWCOew6Mzoc7NcLr38DNqc) | success |
| 11-24 22:09 | [verify-45](https://jobs.colony2.com/c2/jobs/verify-450343441cb876d8bc0bbe0dbab50e5e) c2ops | verify-platform | [3MZVfBWCO](https://jobs.colony2.com/c2/jobs/3MZVfBWCOew6Mzoc7NcLr38DNqc) | failed_app |
| 11-24 22:09 | [verify-f3](https://jobs.colony2.com/c2/jobs/verify-f38bb0d04d8c872a71fdf1c2a8d513c6) c2ops | verify-platform | [3MZVfBWCO](https://jobs.colony2.com/c2/jobs/3MZVfBWCOew6Mzoc7NcLr38DNqc) | cancelled |
| 11-24 22:12 | [3MZVyVzOL](https://jobs.colony2.com/c2/jobs/3MZVyVzOL755bhg9xa9gX52dva3) pulse-cloudhypervisor | stage-amd64-verification-tools | — | success |
| 11-24 22:20 | [3MZX2mOST](https://jobs.colony2.com/c2/jobs/3MZX2mOST7jmBiwQ22cs6nNghxQ) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-24 22:20 | [3MZX2m8TA](https://jobs.colony2.com/c2/jobs/3MZX2m8TAu11JDvRV5pcDLZBmds) pulse-cloudhypervisor | qualify-native-amd64 | — | cancelled |
| 11-24 22:26 | [3MZXf6E9K](https://jobs.colony2.com/c2/jobs/3MZXf6E9KhI6G0TRVBdiMm8zMUm) pulse-cloudhypervisor | stage-amd64-test-sysroot | — | success |
| 11-24 22:26 | [3MZXirKDg](https://jobs.colony2.com/c2/jobs/3MZXirKDgoLDtii3MRNT4QT9UEW) c2ops | c2ops-verify-only | — | failed_app |
| 11-24 22:26 | [verify-76](https://jobs.colony2.com/c2/jobs/verify-76140936341553f55b2beae161a2dc0e) c2ops | verify-platform | [3MZXirKDg](https://jobs.colony2.com/c2/jobs/3MZXirKDgoLDtii3MRNT4QT9UEW) | success |
| 11-24 22:26 | [verify-2e](https://jobs.colony2.com/c2/jobs/verify-2e186802a03e80a013b5f7becc811a99) c2ops | verify-platform | [3MZXirKDg](https://jobs.colony2.com/c2/jobs/3MZXirKDgoLDtii3MRNT4QT9UEW) | success |
| 11-24 22:26 | [verify-02](https://jobs.colony2.com/c2/jobs/verify-02297bd53be1b7ce7a73c7e96b79d6dc) c2ops | verify-platform | [3MZXirKDg](https://jobs.colony2.com/c2/jobs/3MZXirKDgoLDtii3MRNT4QT9UEW) | success |
| 11-24 22:27 | [3MZXtH3mG](https://jobs.colony2.com/c2/jobs/3MZXtH3mGDMs9vtJNNKK5JmNdZ3) pulse-cloudhypervisor | diagnose-native-local-tests | — | success |
| 11-24 22:29 | [3MZY2rHvM](https://jobs.colony2.com/c2/jobs/3MZY2rHvMzAu1Nn2uHeWOvr5ven) pulse-cloudhypervisor | stage-amd64-guest-linker-runtime | — | success |
| 11-24 22:31 | [3MZYGRqUG](https://jobs.colony2.com/c2/jobs/3MZYGRqUGLuDlQTI6bMHQNQFale) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-24 22:31 | [3MZYGYmWE](https://jobs.colony2.com/c2/jobs/3MZYGYmWEv33Bn3TblzpDd9hZ8f) pulse-cloudhypervisor | qualify-native-amd64 | — | cancelled |
| 11-24 22:32 | [3MZYRKtsi](https://jobs.colony2.com/c2/jobs/3MZYRKtsivMotsUczcA5zHe6GGw) pulse-cloudhypervisor | stage-x86-system-emulator | — | success |
| 11-24 22:43 | [3MZZidnT6](https://jobs.colony2.com/c2/jobs/3MZZidnT6aDoe6aLZUg1S55blrP) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-24 22:47 | [3MZaDAzk0](https://jobs.colony2.com/c2/jobs/3MZaDAzk0eQK72EDJryVlLCV4p7) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-24 22:52 | [3MZaqeSPp](https://jobs.colony2.com/c2/jobs/3MZaqeSPp7jxxpM3wYIsXJ1HekD) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-24 22:56 | [3MZbK7cIx](https://jobs.colony2.com/c2/jobs/3MZbK7cIx8z925r5UjZ1XnAW0SV) c2ops | verify-result-check | — | success |
| 11-24 22:57 | [3MZbTMQu0](https://jobs.colony2.com/c2/jobs/3MZbTMQu04Euc6yZM1Dmh7APLbS) c2ops | c2ops-native-disk-check | — | success |
| 11-24 23:00 | [3MZbnh1G6](https://jobs.colony2.com/c2/jobs/3MZbnh1G63IbNMl08kSk4qMFYQP) c2ops | c2ops-verify-codex-amd | — | success |
| 11-24 23:00 | [3MZbng8Hl](https://jobs.colony2.com/c2/jobs/3MZbng8HlvEiqpkcadmpIjafEG0) c2ops | c2ops-verify-codex-mac | — | success |
| 11-24 23:03 | [3MZcDuHAZ](https://jobs.colony2.com/c2/jobs/3MZcDuHAZC7mqHfxCoAWf63yFJy) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-24 23:03 | [3MZcFm7ji](https://jobs.colony2.com/c2/jobs/3MZcFm7jiwqgVaSRo5mmZnyoM1g) c2ops | c2ops-native-disk-check | — | cancelled |
| 11-24 23:04 | [3MZcH1UsC](https://jobs.colony2.com/c2/jobs/3MZcH1UsCNokBbSsbNHygiKHBLz) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-24 23:04 | [3MZcJo07C](https://jobs.colony2.com/c2/jobs/3MZcJo07Corfw3cSZwOLxrcDjOy) pulse-cloudhypervisor | measure-native-partial-worker | — | success |
| 11-24 23:08 | [3MZcrbPaT](https://jobs.colony2.com/c2/jobs/3MZcrbPaTLUGRpeOCTBapNeNNuI) c2ops | c2ops-verify-only | — | cancelled |
| 11-24 23:09 | [verify-8b](https://jobs.colony2.com/c2/jobs/verify-8bf9ee04831eee41bd3029169756e27c) c2ops | verify-native-packages | [3MZcrbPaT](https://jobs.colony2.com/c2/jobs/3MZcrbPaTLUGRpeOCTBapNeNNuI) | cancelled |
| 11-24 23:09 | [verify-79](https://jobs.colony2.com/c2/jobs/verify-79411fadf819a49931c063843b476e75) c2ops | verify-platform | [3MZcrbPaT](https://jobs.colony2.com/c2/jobs/3MZcrbPaTLUGRpeOCTBapNeNNuI) | cancelled |
| 11-24 23:09 | [verify-29](https://jobs.colony2.com/c2/jobs/verify-2950a3b5340783a5a7fcdaada0445101) c2ops | verify-platform | [3MZcrbPaT](https://jobs.colony2.com/c2/jobs/3MZcrbPaTLUGRpeOCTBapNeNNuI) | success |
| 11-24 23:09 | [verify-cd](https://jobs.colony2.com/c2/jobs/verify-cde34985b26d3e9024ed25dfbc2085d8) c2ops | verify-platform | [3MZcrbPaT](https://jobs.colony2.com/c2/jobs/3MZcrbPaTLUGRpeOCTBapNeNNuI) | success |
| 11-24 23:27 | [3MZfB0TTf](https://jobs.colony2.com/c2/jobs/3MZfB0TTfKqUqWSKAQwQfTFOQWi) c2ops | c2ops-verify-go-build-arm | — | success |
| 11-24 23:31 | [3MZfZ0C7L](https://jobs.colony2.com/c2/jobs/3MZfZ0C7Ldb6fF68HILrbISbfoV) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-24 23:31 | [3MZfdXl6z](https://jobs.colony2.com/c2/jobs/3MZfdXl6z4go8Fy4pzknLSqaDvy) c2ops | c2ops-verify-go-build-arm | — | success |
| 11-24 23:46 | [3MZhPhkNo](https://jobs.colony2.com/c2/jobs/3MZhPhkNoluey0m1iFLl9UXVGWf) c2ops | c2ops-verify-only | — | failed_app |
| 11-24 23:46 | [verify-ba](https://jobs.colony2.com/c2/jobs/verify-ba19e608af8527c3222280424eb65679) c2ops | verify-native-packages | [3MZhPhkNo](https://jobs.colony2.com/c2/jobs/3MZhPhkNoluey0m1iFLl9UXVGWf) | failed_app |
| 11-24 23:46 | [verify-6f](https://jobs.colony2.com/c2/jobs/verify-6f0f7cb10d627210f8b842d6cbf045f9) c2ops | verify-platform | [3MZhPhkNo](https://jobs.colony2.com/c2/jobs/3MZhPhkNoluey0m1iFLl9UXVGWf) | failed_app |
| 11-24 23:46 | [verify-7b](https://jobs.colony2.com/c2/jobs/verify-7bfb66c2ab854fdc159b660258e2bfea) c2ops | verify-platform | [3MZhPhkNo](https://jobs.colony2.com/c2/jobs/3MZhPhkNoluey0m1iFLl9UXVGWf) | success |
| 11-24 23:46 | [verify-17](https://jobs.colony2.com/c2/jobs/verify-177fdd1b20ce441daf45b202a7ad25a8) c2ops | verify-native-packages | [3MZhPhkNo](https://jobs.colony2.com/c2/jobs/3MZhPhkNoluey0m1iFLl9UXVGWf) | success |
| 11-24 23:46 | [verify-d9](https://jobs.colony2.com/c2/jobs/verify-d9be93d711b3a8187932ee0aa2ea71bc) c2ops | verify-platform | [3MZhPhkNo](https://jobs.colony2.com/c2/jobs/3MZhPhkNoluey0m1iFLl9UXVGWf) | success |
| 11-24 23:59 | [3MZizwE2t](https://jobs.colony2.com/c2/jobs/3MZizwE2t5w6tvZ8G2G7hJAeX9E) c2ops | verify-native-packages | — | failed_app |
| 11-25 00:24 | [3MZm6Mf6R](https://jobs.colony2.com/c2/jobs/3MZm6Mf6R0maEG37BT1pP8r8Pib) pulse-cloudhypervisor | qualify-physical-host-entrypoint | — | success |
| 11-25 00:27 | [3MZmRKkYz](https://jobs.colony2.com/c2/jobs/3MZmRKkYzqidvF9IhN2qp9Kxjla) c2ops | native-cli-fixtures | — | success |
| 11-25 00:28 | [3MZmajO56](https://jobs.colony2.com/c2/jobs/3MZmajO56qFmMNwgBR3d43sKNV3) c2ops | verify-native-packages | — | success |
| 11-25 00:35 | [3MZnSDHnS](https://jobs.colony2.com/c2/jobs/3MZnSDHnSIzZdc7HcOvOxgyauNq) pulse-cloudhypervisor | qualify-physical-host-entrypoint | — | success |
| 11-25 01:05 | [3MZr6uW6N](https://jobs.colony2.com/c2/jobs/3MZr6uW6NrLXnxGMuDvcRwKNz4e) pulse-cloudhypervisor | resolve-native-bootstrap-assets | — | success |
| 11-25 01:10 | [3MZreHLoz](https://jobs.colony2.com/c2/jobs/3MZreHLozPQre0hANd66myLWaqt) pulse-cloudhypervisor | verify-native-bootstrap-sources | — | success |
| 11-25 01:11 | [3MZrlIHnV](https://jobs.colony2.com/c2/jobs/3MZrlIHnVngwRBEWu80JYok9Ntm) c2ops | c2ops-native-disk-check | — | success |
| 11-25 01:11 | [3MZrmr84K](https://jobs.colony2.com/c2/jobs/3MZrmr84K1aLCjBq1sL8k0ZoGaf) c2ops | c2ops-verify-only | — | success |
| 11-25 01:11 | [verify-97](https://jobs.colony2.com/c2/jobs/verify-97f535491bdb91a0e51c1528988db2b4) c2ops | verify-native-packages | [3MZrmr84K](https://jobs.colony2.com/c2/jobs/3MZrmr84K1aLCjBq1sL8k0ZoGaf) | success |
| 11-25 01:11 | [verify-b7](https://jobs.colony2.com/c2/jobs/verify-b771011521958f03c956da8abd4d5337) c2ops | verify-platform | [3MZrmr84K](https://jobs.colony2.com/c2/jobs/3MZrmr84K1aLCjBq1sL8k0ZoGaf) | success |
| 11-25 01:11 | [verify-af](https://jobs.colony2.com/c2/jobs/verify-af1163bcdc519333fc85f7a5d89b75f0) c2ops | verify-platform | [3MZrmr84K](https://jobs.colony2.com/c2/jobs/3MZrmr84K1aLCjBq1sL8k0ZoGaf) | success |
| 11-25 01:11 | [verify-c7](https://jobs.colony2.com/c2/jobs/verify-c7998934537e4d8dbf1055272d9ae951) c2ops | verify-native-packages | [3MZrmr84K](https://jobs.colony2.com/c2/jobs/3MZrmr84K1aLCjBq1sL8k0ZoGaf) | success |
| 11-25 01:11 | [verify-db](https://jobs.colony2.com/c2/jobs/verify-dbde883e4c5c213b118088e56ecf8bb2) c2ops | verify-platform | [3MZrmr84K](https://jobs.colony2.com/c2/jobs/3MZrmr84K1aLCjBq1sL8k0ZoGaf) | success |
| 11-25 01:18 | [3MZsZveRm](https://jobs.colony2.com/c2/jobs/3MZsZveRmSo7EZ4VnXQ1Btd4aKw) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 01:25 | [3MZtVxTCa](https://jobs.colony2.com/c2/jobs/3MZtVxTCasYeHg3heGCPlrcvb7j) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 01:33 | [3MZuR3pzJ](https://jobs.colony2.com/c2/jobs/3MZuR3pzJRIdW4fpBpQ8yO5rGDP) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 01:36 | [3MZuoTNMh](https://jobs.colony2.com/c2/jobs/3MZuoTNMhCYPxHhtNHCIUk0aFVm) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 01:39 | [3MZvBpwCZ](https://jobs.colony2.com/c2/jobs/3MZvBpwCZ0jQIOFrzxSesgFWCE4) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 01:42 | [3MZvXcWMb](https://jobs.colony2.com/c2/jobs/3MZvXcWMbtZ9LwSNLNwV5n6rn8N) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 01:47 | [3MZw7iIJD](https://jobs.colony2.com/c2/jobs/3MZw7iIJDeApUhgXQ3XnBtfWl0P) pulse-cloudhypervisor | stage-offline-amd64-setup-tests | — | cancelled |
| 11-25 01:53 | [3MZwqEov2](https://jobs.colony2.com/c2/jobs/3MZwqEov2mVLFBqmpwgsKlQ4Zux) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 01:53 | [3MZwr4FH6](https://jobs.colony2.com/c2/jobs/3MZwr4FH69miRd3xP0pdBL1HSuG) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 01:59 | [3MZxfTxRq](https://jobs.colony2.com/c2/jobs/3MZxfTxRq9wXcHOr3h53M4Z4gOW) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 02:06 | [3MZyOXxIN](https://jobs.colony2.com/c2/jobs/3MZyOXxINpjvoZQoS7QHP6jgg8B) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 02:07 | [3MZycq95j](https://jobs.colony2.com/c2/jobs/3MZycq95jOFsPrKzwxDIzVYbWwq) pulse-cloudhypervisor | qualify-native-arm64 | — | cancelled |
| 11-25 02:11 | [3MZz1ec5E](https://jobs.colony2.com/c2/jobs/3MZz1ec5EOiUmgAsVnBSFXESItq) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 02:12 | [3MZz9MzE8](https://jobs.colony2.com/c2/jobs/3MZz9MzE8XhoGDhpJYtPgHfVuaq) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 02:19 | [3MZzylQDX](https://jobs.colony2.com/c2/jobs/3MZzylQDXWKIkGtL2Oa9RF9OLWU) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 02:19 | [3Ma03vsqW](https://jobs.colony2.com/c2/jobs/3Ma03vsqW0H5MymLEk2VT6CdBez) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 02:23 | [3Ma0Zgjzq](https://jobs.colony2.com/c2/jobs/3Ma0ZgjzqVKt3j8xGeeipqhVa05) c2ops | publish-c2ops | — | failed_app |
| 11-25 02:23 | [5LVCKeL2b](https://jobs.colony2.com/c2/jobs/5LVCKeL2bMMhQmH5L4l260ouvZX) c2ops | .c2/recipes/hooks/build/publish/build | [3Ma0Zgjzq](https://jobs.colony2.com/c2/jobs/3Ma0ZgjzqVKt3j8xGeeipqhVa05) | cancelled |
| 11-25 02:23 | [M1VEsZRMo](https://jobs.colony2.com/c2/jobs/M1VEsZRMoZs6rJb9c2yvIXiHA2V) c2ops | .c2/recipes/hooks/build/publish/build | [3Ma0Zgjzq](https://jobs.colony2.com/c2/jobs/3Ma0ZgjzqVKt3j8xGeeipqhVa05) | cancelled |
| 11-25 02:23 | [TlqgW3FiR](https://jobs.colony2.com/c2/jobs/TlqgW3FiRowRM1jFZjje2UeiYN8) c2ops | .c2/recipes/hooks/build/publish/build | [3Ma0Zgjzq](https://jobs.colony2.com/c2/jobs/3Ma0ZgjzqVKt3j8xGeeipqhVa05) | cancelled |
| 11-25 02:24 | [3Ma0hXVOP](https://jobs.colony2.com/c2/jobs/3Ma0hXVOPXeKReusP1mTU32tdgd) c2ops | publish-c2ops | — | failed_app |
| 11-25 02:24 | [DxdO4nXrY](https://jobs.colony2.com/c2/jobs/DxdO4nXrY2w6DEFoTDeHKnEORjF) c2ops | .c2/recipes/hooks/build/publish/build | [3Ma0hXVOP](https://jobs.colony2.com/c2/jobs/3Ma0hXVOPXeKReusP1mTU32tdgd) | cancelled |
| 11-25 02:24 | [4a2grKZrP](https://jobs.colony2.com/c2/jobs/4a2grKZrPV3j9QBhZpVoEyJ9lo1) c2ops | .c2/recipes/hooks/build/publish/build | [3Ma0hXVOP](https://jobs.colony2.com/c2/jobs/3Ma0hXVOPXeKReusP1mTU32tdgd) | failed_app |
| 11-25 02:24 | [7z4UaXfOq](https://jobs.colony2.com/c2/jobs/7z4UaXfOqd1sEuyVdqzBk6pxqHp) c2ops | .c2/recipes/hooks/build/publish/build | [3Ma0hXVOP](https://jobs.colony2.com/c2/jobs/3Ma0hXVOPXeKReusP1mTU32tdgd) | failed_app |
| 11-25 02:24 | [3Ma0iVVxu](https://jobs.colony2.com/c2/jobs/3Ma0iVVxuiZ7ympC4wz7zgYyX5s) pulse-cloudhypervisor | qualify-native-arm64 | — | cancelled |
| 11-25 02:28 | [3Ma17QnNA](https://jobs.colony2.com/c2/jobs/3Ma17QnNA5DRxEkbNCxfUJiaUGE) c2ops | check-pydantic-store | — | success |
| 11-25 02:32 | [3Ma1ftdFx](https://jobs.colony2.com/c2/jobs/3Ma1ftdFx0LY5vqo9oo34zvNREJ) c2ops | build-publish-packages | — | cancelled |
| 11-25 02:32 | [3Ma1fpbBR](https://jobs.colony2.com/c2/jobs/3Ma1fpbBRkMqZI5WgwfF3CCp74i) c2ops | build-publish-packages | — | cancelled |
| 11-25 02:32 | [3Ma1fxDrU](https://jobs.colony2.com/c2/jobs/3Ma1fxDrUHgBwJRon8vTkTcauw4) c2ops | build-publish-packages | — | cancelled |
| 11-25 02:32 | [3Ma1g16UA](https://jobs.colony2.com/c2/jobs/3Ma1g16UAbz4Ui4btR3hij6DNNA) c2ops | finish-c2ops-publication | — | cancelled |
| 11-25 02:40 | [3Ma2eAW3T](https://jobs.colony2.com/c2/jobs/3Ma2eAW3TnMxZFl1GEJh4ODPRGw) cortex | ask | [b61aaf9c9](https://jobs.colony2.com/c2/jobs/b61aaf9c92fbe2db555aca52961068c6) | cancelled |
| 11-25 02:49 | [3Ma3guodB](https://jobs.colony2.com/c2/jobs/3Ma3guodBzYAQYjx5jZAlPiMwWq) c2ops | check-publish-environment | — | success |
| 11-25 02:51 | [3Ma3uJ919](https://jobs.colony2.com/c2/jobs/3Ma3uJ919PhK1r2flRZQrBrL5nO) c2ops | check-release-archive | — | failed_app |
| 11-25 03:06 | [check-c2o](https://jobs.colony2.com/c2/jobs/check-c2ops-79a0bf0-codex-store) c2ops | diagnose-store-contents | — | success |
| 11-25 03:08 | [check-79a](https://jobs.colony2.com/c2/jobs/check-79a0bf0-content-aarch64-linux) c2ops | check-candidate-integrity | — | success |
| 11-25 03:08 | [check-79a](https://jobs.colony2.com/c2/jobs/check-79a0bf0-content-aarch64-darwin) c2ops | check-candidate-integrity | — | success |
| 11-25 03:08 | [check-79a](https://jobs.colony2.com/c2/jobs/check-79a0bf0-content-x86_64-linux) c2ops | check-candidate-integrity | — | success |
| 11-25 03:12 | [check-79a](https://jobs.colony2.com/c2/jobs/check-79a0bf0-archive-size-amd64) c2ops | measure-verified-archive | — | success |
| 11-25 03:12 | [3Ma6VVKJZ](https://jobs.colony2.com/c2/jobs/3Ma6VVKJZeA6Yb49KXKU4y1O32m) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-25 03:14 | [3Ma6jks4T](https://jobs.colony2.com/c2/jobs/3Ma6jks4TwrKXA1OogOK3xx5gdn) c2ops | check-publication-workspace | — | failed_app |
| 11-25 03:16 | [sizes-79a](https://jobs.colony2.com/c2/jobs/sizes-79a0bf0-x86_64-linux) c2ops | measure-native-release-packages | — | success |
| 11-25 03:21 | [3Ma7aQ4VP](https://jobs.colony2.com/c2/jobs/3Ma7aQ4VPRtpJ5mGEV2IaMd9qwW) c2ops | build-publish-packages | — | cancelled |
| 11-25 03:21 | [3Ma7aXzO9](https://jobs.colony2.com/c2/jobs/3Ma7aXzO9JJJJFcCevBnTK89Ipr) c2ops | build-publish-packages | — | failed_app |
| 11-25 03:21 | [3Ma7acVdA](https://jobs.colony2.com/c2/jobs/3Ma7acVdAuamyzlnqUTYWjeGGGR) c2ops | build-publish-packages | — | failed_app |
| 11-25 03:21 | [3Ma7aZJ7u](https://jobs.colony2.com/c2/jobs/3Ma7aZJ7uE7ORrz3rAGJ9phPVR4) c2ops | finish-c2ops-publication | — | cancelled |
| 11-25 03:21 | [GMSUxYpY9](https://jobs.colony2.com/c2/jobs/GMSUxYpY9fPGUbOnF5nf9iHd27n) jobdb | merge-batch | — | success |
| 11-25 03:21 | [3Ma7bHNj1](https://jobs.colony2.com/c2/jobs/3Ma7bHNj1XLBZiEQHIZwTZc028c) c2ops | check-write-profile | — | success |
| 11-25 03:23 | [3Ma7qwdkz](https://jobs.colony2.com/c2/jobs/3Ma7qwdkzbj1GpZ3mJSTVhzJYHY) c2ops | check-publication-cache-api | — | success |
| 11-25 03:24 | [3Ma7vhq5z](https://jobs.colony2.com/c2/jobs/3Ma7vhq5zDESzXwU2koEGDMje6L) c2ops | check-release-upload-set | — | success |
| 11-25 03:25 | [3Ma83Sp1P](https://jobs.colony2.com/c2/jobs/3Ma83Sp1PlFm76nFgdyfCYSrF7v) c2ops | build-publish-packages | — | failed_app |
| 11-25 03:25 | [3Ma83aBCY](https://jobs.colony2.com/c2/jobs/3Ma83aBCYjTDAQJCaVeQkvDrVJE) c2ops | build-publish-packages | — | success |
| 11-25 03:25 | [3Ma83dRlP](https://jobs.colony2.com/c2/jobs/3Ma83dRlPHswpkooqtGbjJ19mGv) c2ops | build-publish-packages | — | success |
| 11-25 03:25 | [3Ma83heXw](https://jobs.colony2.com/c2/jobs/3Ma83heXwwOGF4ZlGJG26l3Hion) c2ops | finish-c2ops-publication | — | failed_app |
| 11-25 03:27 | [3Ma8GhLAP](https://jobs.colony2.com/c2/jobs/3Ma8GhLAPghwFNrvqfdFtbtiitB) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-25 03:37 | [3Ma9UnTx0](https://jobs.colony2.com/c2/jobs/3Ma9UnTx0ZijZeEn0JVGiytSBUo) c2ops | verify-colony2-public-key | — | success |
| 11-25 03:38 | [3Ma9czwMV](https://jobs.colony2.com/c2/jobs/3Ma9czwMVkch49LNKbGrOitR9ir) c2ops | build-publish-packages | — | success |
| 11-25 03:38 | [3Ma9d6Fx2](https://jobs.colony2.com/c2/jobs/3Ma9d6Fx2R8oHspqHHXIx4BREZg) c2ops | finish-c2ops-publication | — | success |
| 11-25 03:55 | [3MaBmi6as](https://jobs.colony2.com/c2/jobs/3MaBmi6asEDXFqa0K1ApmGmX3t3) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-25 04:24 | [3MaFGj7uU](https://jobs.colony2.com/c2/jobs/3MaFGj7uUtuwp9RIp2U2aeu9dJg) pulse-cloudhypervisor | qualify-native-arm64 | — | cancelled |
| 11-25 04:25 | [3MaFJZNF3](https://jobs.colony2.com/c2/jobs/3MaFJZNF3SzrLhuvFgrhMw96MvO) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 04:37 | [3MaGmyNAL](https://jobs.colony2.com/c2/jobs/3MaGmyNALTv47EZJqD4bybLFK9t) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 04:48 | [3MaIDeYH7](https://jobs.colony2.com/c2/jobs/3MaIDeYH76vEgKRVpt3am1bRrXw) pulse-cloudhypervisor | qualify-native-arm64 | — | cancelled |
| 11-25 04:49 | [3MaIGypEc](https://jobs.colony2.com/c2/jobs/3MaIGypEcvASygilS5lahNMo4K2) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 04:51 | [3MaIXZWSr](https://jobs.colony2.com/c2/jobs/3MaIXZWSrdIHbS9HEzUqSABAICb) pulse-cloudhypervisor | test-amd64-ubuntu-with-tcg | — | success |
| 11-25 04:53 | [PkuTRpk4l](https://jobs.colony2.com/c2/jobs/PkuTRpk4liCDCSNqVZvLaKFJnGF) c2j | merge-batch | — | success |
| 11-25 04:58 | [3MaJKivb6](https://jobs.colony2.com/c2/jobs/3MaJKivb6nLGOVBWwEcwnUJ6sfD) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 05:36 | [3MaO1I0lp](https://jobs.colony2.com/c2/jobs/3MaO1I0lphSOBmDIAU7qjPUjhau) pulse-cloudhypervisor | qualify-native-arm64 | — | cancelled |
| 11-25 05:38 | [3MaOISr0M](https://jobs.colony2.com/c2/jobs/3MaOISr0MRCHth2FKJThWpj7AmO) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-25 05:53 | [3MaQ1rPJO](https://jobs.colony2.com/c2/jobs/3MaQ1rPJObCZaAeyk8v9fZHhVx7) root | root-candidate-verify | [3MaOf36tL](https://jobs.colony2.com/c2/jobs/3MaOf36tL7bO8fFdoB4Sn3r9rsd) | failed_app |
| 11-25 05:59 | [3MaQl8wT4](https://jobs.colony2.com/c2/jobs/3MaQl8wT4emOCbFZCWLvAChqMI8) root | root-candidate-verify | [3MaOf36tL](https://jobs.colony2.com/c2/jobs/3MaOf36tL7bO8fFdoB4Sn3r9rsd) | success |
| 11-25 06:14 | [3MaSf9QiO](https://jobs.colony2.com/c2/jobs/3MaSf9QiOP4PybelWkezhidvkfs) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | failed_app |
| 11-25 06:14 | [3MaSf7mO3](https://jobs.colony2.com/c2/jobs/3MaSf7mO3TepjFcK7BC4MZJ5EN8) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | failed_app |
| 11-25 06:14 | [3MaSf9kmb](https://jobs.colony2.com/c2/jobs/3MaSf9kmbD9qkPf3RDevzxbNLyk) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | failed_app |
| 11-25 06:14 | [3MaSf7yvB](https://jobs.colony2.com/c2/jobs/3MaSf7yvBGCKBT2iImKIebAtmri) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | failed_app |
| 11-25 06:14 | [3MaSfClDS](https://jobs.colony2.com/c2/jobs/3MaSfClDSi7qYLtUCNGqABePLId) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | failed_app |
| 11-25 06:14 | [3MaSg5WxC](https://jobs.colony2.com/c2/jobs/3MaSg5WxCuFg8BB8PzoX3sGxUgw) pgjobdb | pgjobdb-worker-placement-diagnostic | [3MaP2f4VW](https://jobs.colony2.com/c2/jobs/3MaP2f4VWCJXwLw9OHcE2JsF0v8) | success |
| 11-25 06:15 | [3MaShax99](https://jobs.colony2.com/c2/jobs/3MaShax99bwTYqZtI8qEdRQ9QzG) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | success |
| 11-25 06:15 | [3MaShdbHX](https://jobs.colony2.com/c2/jobs/3MaShdbHXPeDEpFhZlDj86FQWHL) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | success |
| 11-25 06:15 | [3MaShb8B8](https://jobs.colony2.com/c2/jobs/3MaShb8B8JHcWX9PqmWwxSK1rtL) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | AWAITING_FUTURE |
| 11-25 06:15 | [3MaShgqf7](https://jobs.colony2.com/c2/jobs/3MaShgqf7pgci5PYTfuAvtBFkWF) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | success |
| 11-25 06:15 | [3MaShdKVf](https://jobs.colony2.com/c2/jobs/3MaShdKVf4H3kJDvadrdMSvh1gf) gitvend | gitvend-routing-probe | [3MaP2fnBT](https://jobs.colony2.com/c2/jobs/3MaP2fnBTixgKIw3gz83GLTcM2Y) | success |
| 11-25 06:15 | [3MaSkFTmq](https://jobs.colony2.com/c2/jobs/3MaSkFTmqu2GBh8jbCuelyseJK8) pgjobdb | pgjobdb-docker-placement-diagnostic | [3MaP2f4VW](https://jobs.colony2.com/c2/jobs/3MaP2f4VWCJXwLw9OHcE2JsF0v8) | AWAITING_FUTURE |
| 11-25 06:18 | [3MaT4EgzZ](https://jobs.colony2.com/c2/jobs/3MaT4EgzZho8YD1LnOJDiLbrgc4) pulse-cloudhypervisor | qualify-native-arm64 | — | success |
| 11-25 06:18 | [3MaT8XtUT](https://jobs.colony2.com/c2/jobs/3MaT8XtUTqAn54YpyTKE3jYOeWc) pulse-tart | pulse-tart-macos-placement | [3MaP2kOm5](https://jobs.colony2.com/c2/jobs/3MaP2kOm5xRW6j05OhM2AJa7pjz) | failed_app |
| 11-25 06:19 | [3MaTCpw0j](https://jobs.colony2.com/c2/jobs/3MaTCpw0jn17RnqJFXWcrQRVbUU) pulse-cloudhypervisor | qualify-first-run-yaml | — | success |
| 11-25 06:20 | [3MaTIiSY0](https://jobs.colony2.com/c2/jobs/3MaTIiSY03miSe3pnM54PWVYYtn) pulse-tart | pulse-tart-macos-placement | [3MaP2kOm5](https://jobs.colony2.com/c2/jobs/3MaP2kOm5xRW6j05OhM2AJa7pjz) | CRASH_CONCERN |
| 11-25 06:26 | [3MaU3sBKb](https://jobs.colony2.com/c2/jobs/3MaU3sBKbMat8wYrOhZNIYnPLyC) c2j | parallel-direction-remote-probe | [3MaP1pW9Y](https://jobs.colony2.com/c2/jobs/3MaP1pW9YHeX1ZHvWiGOKO0EUfQ) | failed_app |
| 11-25 06:26 | [3MaU4BEds](https://jobs.colony2.com/c2/jobs/3MaU4BEdsY8nxym5pmXmGqHh5tO) vz-macos | ask | [3MaP2haaC](https://jobs.colony2.com/c2/jobs/3MaP2haaC0PgRUrbmwZFl2cvRyV) | cancelled |
| 11-25 06:26 | [V80T26kX8](https://jobs.colony2.com/c2/jobs/V80T26kX8KcDQ7qUQ2SZPXrK31Z) c2j | pkg/worker/test-fixtures/recipes/test-sleep-operation | [3MaU3sBKb](https://jobs.colony2.com/c2/jobs/3MaU3sBKbMat8wYrOhZNIYnPLyC) | success |
| 11-25 06:26 | [QaHRavwqU](https://jobs.colony2.com/c2/jobs/QaHRavwqU0GYiLwTsp8nLc4TTyT) c2j | pkg/worker/test-fixtures/recipes/artifact-inbox-command | [3MaU3sBKb](https://jobs.colony2.com/c2/jobs/3MaU3sBKbMat8wYrOhZNIYnPLyC) | success |
| 11-25 06:26 | [3MaU7QyAV](https://jobs.colony2.com/c2/jobs/3MaU7QyAVe0epMFbZhBkuMPGEfN) pulse | pulse-verify-placement-probe | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) | failed_app |
| 11-25 06:26 | [3MaU7JLFN](https://jobs.colony2.com/c2/jobs/3MaU7JLFNlpqhd1V4rpyX0GG61Q) pulse | pulse-verify-placement-probe | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) | AWAITING_FUTURE |
| 11-25 06:26 | [3MaU7P2i5](https://jobs.colony2.com/c2/jobs/3MaU7P2i5VqQVwZYUiTk480JinU) pulse | pulse-verify-placement-probe | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) | CRASH_CONCERN |
| 11-25 06:26 | [3MaU7M6iU](https://jobs.colony2.com/c2/jobs/3MaU7M6iUuKinJ6ufyWY7ZmaVgu) pulse | pulse-verify-placement-probe | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) | failed_app |
| 11-25 06:27 | [3MaUC9Dv1](https://jobs.colony2.com/c2/jobs/3MaUC9Dv1MZymtVzCWUy0g7omJw) c2j | parallel-direction-remote-probe | [3MaP1pW9Y](https://jobs.colony2.com/c2/jobs/3MaP1pW9YHeX1ZHvWiGOKO0EUfQ) | success |
| 11-25 06:27 | [G9nc3AunB](https://jobs.colony2.com/c2/jobs/G9nc3AunBmrq5nM7SM9p9bT0V7S) c2j | pkg/worker/test-fixtures/recipes/test-sleep-operation | [3MaUC9Dv1](https://jobs.colony2.com/c2/jobs/3MaUC9Dv1MZymtVzCWUy0g7omJw) | success |
| 11-25 06:27 | [6C6JPJuVe](https://jobs.colony2.com/c2/jobs/6C6JPJuVeH3M4fFchYQn9CIoGAG) c2j | pkg/worker/test-fixtures/recipes/outbox-artifacts | [3MaUC9Dv1](https://jobs.colony2.com/c2/jobs/3MaUC9Dv1MZymtVzCWUy0g7omJw) | success |
| 11-25 06:27 | [3MaUFwCWY](https://jobs.colony2.com/c2/jobs/3MaUFwCWYMV5xT0izoCuu1xVFsw) pulse | pulse-verify-placement-probe-v2 | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) | success |
| 11-25 06:28 | [3MaUJwb6z](https://jobs.colony2.com/c2/jobs/3MaUJwb6zqQ3VxrB46FSdHdRCYB) pulse | pulse-verify-placement-probe-v2 | [3MaP2iahg](https://jobs.colony2.com/c2/jobs/3MaP2iahgHCsfgMh3W3nbFGqWpG) | failed_app |
| 11-25 06:50 | [3MaWzhdn2](https://jobs.colony2.com/c2/jobs/3MaWzhdn2m20G9YIu1hdmDc0EyZ) pulse-cloudhypervisor | qualify-arm64-recovery-and-isolation | — | cancelled |
| 11-25 07:30 | [5qSJgnnfH](https://jobs.colony2.com/c2/jobs/5qSJgnnfHntUzW8mAKUvvzftx0X) pulse-docker | merge-batch | — | success |
| 11-25 10:18 | [PkuTRpk4l](https://jobs.colony2.com/c2/jobs/PkuTRpk4liCDCSNqVZvLaKFJnGG) c2j | merge-batch | — | success |
| 11-25 10:22 | [PkuTRpk4l](https://jobs.colony2.com/c2/jobs/PkuTRpk4liCDCSNqVZvLaKFJnGH) c2j | merge-batch | — | success |
| 11-25 10:23 | [3MawyIhap](https://jobs.colony2.com/c2/jobs/3MawyIhapFxTjIp8dctZ0ReVigz) cortex | cortex-synthetic-verify-routing | [3MaP2ipKx](https://jobs.colony2.com/c2/jobs/3MaP2ipKxKyq1tLaSaXbVyiudCz) | CRASH_CONCERN |
| 11-25 15:03 | [PkuTRpk4l](https://jobs.colony2.com/c2/jobs/PkuTRpk4liCDCSNqVZvLaKFJnGI) c2j | merge-batch | — | success |
| 11-25 16:52 | [3MbiCyv8G](https://jobs.colony2.com/c2/jobs/3MbiCyv8GUH3qiVq7CGAg91c4cZ) base | base-verify-worker-preflight | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |
| 11-25 16:59 | [verify-9e](https://jobs.colony2.com/c2/jobs/verify-9e9bed3a945bb41abb7cac3564e5d3f5) c2ops | verify-native-packages | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | CRASH_CONCERN |
| 11-25 16:59 | [verify-f1](https://jobs.colony2.com/c2/jobs/verify-f1e45196ead2253aa68d4e5d474da767) c2ops | verify-platform | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | CRASH_CONCERN |
| 11-25 16:59 | [verify-27](https://jobs.colony2.com/c2/jobs/verify-27a524eb711be41ffc85134af501bb60) c2ops | verify-platform | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | failed_app |
| 11-25 16:59 | [verify-ef](https://jobs.colony2.com/c2/jobs/verify-efe432da20148545c0ded254f6edad59) c2ops | verify-native-packages | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | failed_app |
| 11-25 16:59 | [verify-a6](https://jobs.colony2.com/c2/jobs/verify-a61fa82e722eb42d71cfc368b3b28465) c2ops | verify-platform | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | failed_app |
| 11-25 17:00 | [3MbjBfm90](https://jobs.colony2.com/c2/jobs/3MbjBfm901ZG8tbMB5uB2Pmn8FE) c2j | c2j-build-verify | [3MaP2gTny](https://jobs.colony2.com/c2/jobs/3MaP2gTny122DL2EiQOER4KjSvT) | success |
| 11-25 17:00 | [3MbjBfYF4](https://jobs.colony2.com/c2/jobs/3MbjBfYF4QgmFoxvmGc4SUEynuN) c2j | c2j-build-verify | [3MaP2gTny](https://jobs.colony2.com/c2/jobs/3MaP2gTny122DL2EiQOER4KjSvT) | CRASH_CONCERN |
| 11-25 17:05 | [3MbjpPzfo](https://jobs.colony2.com/c2/jobs/3MbjpPzfofcZ5DrGImMsXdYHIWv) base | base-native-image-verification-diagnostic | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |
| 11-25 17:07 | [49v1BiUgq](https://jobs.colony2.com/c2/jobs/49v1BiUgqhlCLr0FMmu1iHN8bzN) auth | merge-batch | — | success |
| 11-25 17:07 | [3Mbk53WGl](https://jobs.colony2.com/c2/jobs/3Mbk53WGlxblUIFMQjnlpcfoV0M) base | base-native-image-runtime-failure-diagnostic | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | failed_app |
| 11-25 17:08 | [verify-6e](https://jobs.colony2.com/c2/jobs/verify-6e774cab2fbb406e83fceb316affbc4a) c2ops | verify-native-packages | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | CRASH_CONCERN |
| 11-25 17:08 | [verify-5b](https://jobs.colony2.com/c2/jobs/verify-5b800d388eee96b76cd8430f7ddad2b7) c2ops | verify-platform | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | CRASH_CONCERN |
| 11-25 17:08 | [verify-59](https://jobs.colony2.com/c2/jobs/verify-595d40a3837b502a4208ac46b37b976a) c2ops | verify-platform | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | success |
| 11-25 17:08 | [verify-9b](https://jobs.colony2.com/c2/jobs/verify-9bf106cb1ffa94d6de59450b4ce2a110) c2ops | verify-native-packages | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | success |
| 11-25 17:08 | [verify-37](https://jobs.colony2.com/c2/jobs/verify-37b8e8981b777a050b0dda344185094d) c2ops | verify-platform | [3MaNfJeOA](https://jobs.colony2.com/c2/jobs/3MaNfJeOAPedewlJYpCTn1WLCmr) | success |
| 11-25 17:33 | [3MbnEWLTp](https://jobs.colony2.com/c2/jobs/3MbnEWLTpOX1gAJO2c5sSEe8ZBm) base | base-native-image-verification-diagnostic | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |
| 11-25 18:19 | [3Mbskt9Ql](https://jobs.colony2.com/c2/jobs/3Mbskt9QlBJJ8YilA6ioWvUey5M) base | base-native-image-verification-diagnostic | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |
| 11-25 18:19 | [3MbsktrJh](https://jobs.colony2.com/c2/jobs/3MbsktrJhFcfsPgMqaFoDnL67lk) base | base-native-image-runtime-failure-diagnostic | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |
| 11-25 18:59 | [3Mbxi0iRq](https://jobs.colony2.com/c2/jobs/3Mbxi0iRqJF2Z22Y2Nvu5qNaTKL) base | base-native-image-clean-candidate | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |
| 11-25 18:59 | [3Mbxi0BDK](https://jobs.colony2.com/c2/jobs/3Mbxi0BDKHcEpncQxzIABrK88tw) base | base-native-image-clean-runtime-fault | [3MaP2ev4I](https://jobs.colony2.com/c2/jobs/3MaP2ev4IDOJrfQSCJl8iEMWYu3) | success |

## Older jobs inspected separately

Inspected visible older live jobs and older parents of cohort jobs. A task counts as activity here if its start or finish fell in the window. This is a cross-check on carried work. A terminal older job with no newly created child can be absent from it.

| Job · cell | Start | Tasks with in-window activity | Result |
|---|---|---:|---|
| [0983ec11-](https://jobs.colony2.com/c2/jobs/0983ec11-ec4c-4c41-8f99-09efb51e2a15) c2j | 2026-11-24 03:20 | 15 | cancelled |
| [3MUTajher](https://jobs.colony2.com/c2/jobs/3MUTajherXex1sm8w9nJxTSvmBE) jobdb | 2026-11-23 03:23 | 0 | CRASH_CONCERN |
| [3MXUizqA3](https://jobs.colony2.com/c2/jobs/3MXUizqA3LJ5hSsqdoyZbu0DwRR) c2ops | 2026-11-24 05:02 | 0 | READY |
| [GkhYoi7MY](https://jobs.colony2.com/c2/jobs/GkhYoi7MYLb3vLwaZ32r1mBB49b) recipes | 2026-11-21 05:58 | 0 | READY |
| [T9UdA1V6I](https://jobs.colony2.com/c2/jobs/T9UdA1V6I4v1GWJAwcHvuzDo2E1) c2ops | 2026-11-23 02:43 | 0 | READY |
| [b61aaf9c9](https://jobs.colony2.com/c2/jobs/b61aaf9c92fbe2db555aca52961068c6) cortex | 2026-11-24 18:25 | 8 | cancelled |

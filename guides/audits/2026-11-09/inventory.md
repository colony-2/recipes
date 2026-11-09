# Jobs inspected: November 8–9, 2026

Selection: jobs created from **2026-11-08 19:11:11 UTC through 2026-11-09 19:11:11 UTC**, on `http://192.168.1.195:9047/c2`. All 44 retained matches were inspected; 11 belong to Cortex. See the [audit](audit.md) and [plan](improvement-plan.md).

The initial census read 255 retained jobs over three pages using the JobDB query API with `includeHidden: true` and `stores: [ACTIVE, ARCHIVED]`, then applied the frozen creation window locally. The CLI lacked equivalent visibility/store filters. Physically purged records cannot be included. Thirteen selected jobs were hidden. Status below is the initial census status; detail reads continued while jobs ran. Cortex-assistant moved from READY to ACTIVE during those reads.

Inspection used c2j **0.0.124**, all 44 task inventories (1,873 recorded task occurrences at those reads), and 356 selected exact task outputs. Initial artifact previews were bounded at 25; complete paginated inventories were retrieved where needed. Absence in a preview was not treated as evidence of missing files. All selected task-output and artifact reads eventually succeeded after retrying transient inspection timeouts. Full runtime build identity was not established for every historical worker.

Dates below are UTC; `11-09 05:32` means November 9 at 05:32. Parent links are shortened for readability. `H` means hidden, `A` means archived at census; `—` means neither. `success` is the job result, not a claim that every check passed.

## Cortex jobs

| Job | Created | Cell | Outcome/state | Recipe | Visibility | Parent | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [3LsmZNUoxBXwnTcoJKekMAZagiX](https://jobs.colony2.com/c2/jobs/3LsmZNUoxBXwnTcoJKekMAZagiX) | 11-09 19:06 | cortex | ACTIVE | `1c7cdc74` | — | — | Latest fix: recovering approved tabs work and dependencies; too early to assess outcome. |
| [16ea3496131b3f96923e1dad79efd9d2](https://jobs.colony2.com/c2/jobs/16ea3496131b3f96923e1dad79efd9d2) | 11-09 06:17 | cortex | ACTIVE | `610a59bb` | — | — | HTML/SVG preview implementation completed; browser failure repaired, then rebase conflict. No merge form yet in snapshot. |
| [aeb762876842fc003425d35907500856](https://jobs.colony2.com/c2/jobs/aeb762876842fc003425d35907500856) | 11-09 05:41 | cortex | success | `610a59bb` | A | — | Authentik/permissions investigation completed without implementation approval. |
| [7ca74bfa70249331df08ea6b8330fb49](https://jobs.colony2.com/c2/jobs/7ca74bfa70249331df08ea6b8330fb49) | 11-09 05:37 | cortex | success | `610a59bb` | A | — | Scrolling feature merged. Review includes two phone screenshots; browser failure recovered. |
| [6d44f0e7b4396c9da893699aeb8eda1b](https://jobs.colony2.com/c2/jobs/6d44f0e7b4396c9da893699aeb8eda1b) | 11-09 05:35 | cortex | failed_app | `610a59bb` | A | — | Tabs partially implemented. Bad consultation Git ref repaired; accepted-handoff transport eventually declared impossible. |
| [1f72f9d9e783e9a9722c0c861a1af01b](https://jobs.colony2.com/c2/jobs/1f72f9d9e783e9a9722c0c861a1af01b) | 11-09 05:32 | cortex | success | `610a59bb` | A | — | Execution tree merged after rebase repair. Both merge forms omit four available screenshots, including after explicit feedback. |
| [6a70318940363160d26f63d5323b8fb2](https://jobs.colony2.com/c2/jobs/6a70318940363160d26f63d5323b8fb2) | 11-09 05:31 | cortex | ACTIVE | `610a59bb` | — | — | Goals filter: invented storage scope corrected. First review has images; repeat review loses them despite unchanged local edits. |
| [WZ9xJfKBfxGFhnNadct9jb3IQSX](https://jobs.colony2.com/c2/jobs/WZ9xJfKBfxGFhnNadct9jb3IQSX) | 11-09 02:49 | cortex | READY | `610a59bb` | — | [07c92827-2…](https://jobs.colony2.com/c2/jobs/07c92827-240d-488a-b6a8-7d250406fcfe) | Timeline review waiting. After screenshot request, new gallery is attached but all four linked PNGs are omitted. |
| [18f1949f-58d5-4e5d-8fbe-59fdb6c94d83](https://jobs.colony2.com/c2/jobs/18f1949f-58d5-4e5d-8fbe-59fdb6c94d83) | 11-09 02:26 | cortex | PENDING_JOBS | `610a59bb` | — | — | Assistant parent waits for cortex-assistant child; recovered prior assignment and implemented local boundary work. |
| [7f7199c5c7c08380f4a5fc1e809c476d](https://jobs.colony2.com/c2/jobs/7f7199c5c7c08380f4a5fc1e809c476d) | 11-09 01:04 | cortex | failed_app | `610a59bb` | HA | — | Old handoff identity trap and human-inclusive iteration limit; superseded by recovery job. |
| [1fac9e89-36cf-4a4f-a797-7d4fe887c65c](https://jobs.colony2.com/c2/jobs/1fac9e89-36cf-4a4f-a797-7d4fe887c65c) | 11-09 00:35 | cortex | success | `610a59bb` | A | — | Compact-ID payload fix merged after correcting backend/ID-allocation assumptions. No visual change; screenshots reasonably omitted. |

## Other jobs

| Job | Created | Cell | Outcome/state | Recipe | Visibility | Parent | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [3LsmdOIAypjvQciQDRPKy17Mk0o](https://jobs.colony2.com/c2/jobs/3LsmdOIAypjvQciQDRPKy17Mk0o) | 11-09 19:07 | jobdb | success | `1c7cdc74` | A | — | Latest fix: verified replacement publication and consumer version; no duplicate implementation. |
| [3LsSrjvAQeIbY0h6vBWMBPzBfO7](https://jobs.colony2.com/c2/jobs/3LsSrjvAQeIbY0h6vBWMBPzBfO7) | 11-09 16:24 | c2j | ACTIVE | `610a59bb` | — | [3Lkn1955P8…](https://jobs.colony2.com/c2/jobs/3Lkn1955P8gAaHVdCfJSseHtvCm) | Recovery association/receipt verification; reports a zero-second scope timeout despite successful commands. Follow-up verification active. |
| [2h5XJ0icclMY2C4atTMmGVXpWtw](https://jobs.colony2.com/c2/jobs/2h5XJ0icclMY2C4atTMmGVXpWtw) | 11-09 06:44 | jobdb | success | `610a59bb` | HA | [NRIUmogvCv…](https://jobs.colony2.com/c2/jobs/NRIUmogvCvutaKsP74YZity8qNG) | Replacement JobDB delivery published after recovering useful source from BA8Q; healthy recovery. |
| [BA8QGnX93OJWssPiz4HiOKyH1yz](https://jobs.colony2.com/c2/jobs/BA8QGnX93OJWssPiz4HiOKyH1yz) | 11-09 06:02 | jobdb | failed_app | `610a59bb` | A | [NRIUmogvCv…](https://jobs.colony2.com/c2/jobs/NRIUmogvCvutaKsP74YZity8qNG) | Old handoff identity rejection repeats until iteration limit; useful work recovered by replacement. |
| [3LrCVU5aIj9Yz5kpra3RAOVlVKU](https://jobs.colony2.com/c2/jobs/3LrCVU5aIj9Yz5kpra3RAOVlVKU) | 11-09 05:40 | c2j | success | `610a59bb` | HA | [3Lkn1955P8…](https://jobs.colony2.com/c2/jobs/3Lkn1955P8gAaHVdCfJSseHtvCm) | HistoryService delivery published; later parent bookkeeping/recovery association remained disputed. |
| [c358d633b62cb868d05d5ac01e32e2e0](https://jobs.colony2.com/c2/jobs/c358d633b62cb868d05d5ac01e32e2e0) | 11-09 05:39 | jobdb | READY | `610a59bb` | — | — | Security proposal revised into separate decisions; awaiting direction review. User requested iterative design. |
| [NRIUmogvCvutaKsP74YZity8qNG](https://jobs.colony2.com/c2/jobs/NRIUmogvCvutaKsP74YZity8qNG) | 11-09 05:25 | pgjobdb | ACTIVE | `610a59bb` | — | [07c92827-2…](https://jobs.colony2.com/c2/jobs/07c92827-240d-488a-b6a8-7d250406fcfe) | Postgres review-history work waiting on JobDB publication; parent retrieved useful failed-child output before replacement. |
| [3Lr0lTvZ3QfnboLunczW9j6T1p2](https://jobs.colony2.com/c2/jobs/3Lr0lTvZ3QfnboLunczW9j6T1p2) | 11-09 04:03 | recipes | success | `inline` | A | [JfJDOvdgYv…](https://jobs.colony2.com/c2/jobs/JfJDOvdgYvvITvbl6ugtbhi6kZ9) | Corrected helper invocation completed, reporting hosted verification failure. Helper success does not mean verification passed. |
| [3Lr0hf4uob5rEW9DbHLfyt2wPT2](https://jobs.colony2.com/c2/jobs/3Lr0hf4uob5rEW9DbHLfyt2wPT2) | 11-09 04:03 | recipes | failed_app | `inline` | A | [JfJDOvdgYv…](https://jobs.colony2.com/c2/jobs/JfJDOvdgYvvITvbl6ugtbhi6kZ9) | Inline helper failed prompt-input binding; corrected by 3Lr0l. |
| [JfJDOvdgYvvITvbl6ugtbhi6kZ9](https://jobs.colony2.com/c2/jobs/JfJDOvdgYvvITvbl6ugtbhi6kZ9) | 11-09 03:26 | recipes | failed_app | `610a59bb` | A | [SVYbGlC2gS…](https://jobs.colony2.com/c2/jobs/SVYbGlC2gSzO0r8bUo1bEkBx1tT) | Hosted verification reached GitHub but received 401; report also identifies 18 retained creation-fixture failures. |
| [3LquYc2p2KIQmVHCIpPJLUDzj9k](https://jobs.colony2.com/c2/jobs/3LquYc2p2KIQmVHCIpPJLUDzj9k) | 11-09 03:12 | c2j | failed_app | `a3fea1fc` | A | [SVYbGlC2gS…](https://jobs.colony2.com/c2/jobs/SVYbGlC2gSzO0r8bUo1bEkBx1tT) | Old adaptive: restored candidate differs from separately resolved configure workspace; false configuration-mutation failure. |
| [3LquN99YfHthT2NqUw9jlkm4wZ1](https://jobs.colony2.com/c2/jobs/3LquN99YfHthT2NqUw9jlkm4wZ1) | 11-09 03:11 | c2j | failed_app | `610a59bb` | A | [SVYbGlC2gS…](https://jobs.colony2.com/c2/jobs/SVYbGlC2gSzO0r8bUo1bEkBx1tT) | Adaptive2: same recovered-workspace/configuration failure before any agent task. |
| [LiouuSJHsY7Dbw8iRNgwslXI3gv](https://jobs.colony2.com/c2/jobs/LiouuSJHsY7Dbw8iRNgwslXI3gv) | 11-09 03:03 | vz-macos | failed_app | `610a59bb` | A | [Fvv4qAFeUl…](https://jobs.colony2.com/c2/jobs/Fvv4qAFeUl4TKPXxOt4rWHY3EH7) | Package probe failed during Nix tool setup. Not enough retained error detail to assign the exact realization cause. |
| [3LqtNozqBaFK7YOqbKRcJRxgrSX](https://jobs.colony2.com/c2/jobs/3LqtNozqBaFK7YOqbKRcJRxgrSX) | 11-09 03:03 | c2j | failed_app | `610a59bb` | A | [Mw4GH987vP…](https://jobs.colony2.com/c2/jobs/Mw4GH987vPBwuA2tUL2TlcOqZyB) | Assignment requires fencing/recovering an existing parent continuation; no supported interface and submission denied. |
| [FFVtWEMd1bf4RrHjzKLjNkRIjon](https://jobs.colony2.com/c2/jobs/FFVtWEMd1bf4RrHjzKLjNkRIjon) | 11-09 03:00 | vz-macos | failed_app | `610a59bb` | HA | [Fvv4qAFeUl…](https://jobs.colony2.com/c2/jobs/Fvv4qAFeUl4TKPXxOt4rWHY3EH7) | Package probe uses invalid flake:go_1_25 reference. |
| [D90RloCTwwfa5WbhbTbYfcqYYLL](https://jobs.colony2.com/c2/jobs/D90RloCTwwfa5WbhbTbYfcqYYLL) | 11-09 02:56 | vz-macos | success | `610a59bb` | A | [4912eea3-8…](https://jobs.colony2.com/c2/jobs/4912eea3-8db9-4130-b8b8-529b920eaf1d) | Corrected package check succeeded. |
| [UmjkVQmvkOlwMcAKll2Kpv6Blhx](https://jobs.colony2.com/c2/jobs/UmjkVQmvkOlwMcAKll2Kpv6Blhx) | 11-09 02:56 | recipes | failed_app | `610a59bb` | HA | [Mw4GH987vP…](https://jobs.colony2.com/c2/jobs/Mw4GH987vPBwuA2tUL2TlcOqZyB) | Recovery assignment demands controller operations from a build/design task; unsupported operation and submission denial. |
| [Fvv4qAFeUl4TKPXxOt4rWHY3EH7](https://jobs.colony2.com/c2/jobs/Fvv4qAFeUl4TKPXxOt4rWHY3EH7) | 11-09 02:56 | vz-macos | failed_app | `610a59bb` | A | [23a69302-e…](https://jobs.colony2.com/c2/jobs/23a69302-e319-4813-b7a8-5cf73928f7fa) | Native macOS acceptance required on Linux executor; package/config attempts did not supply the missing base/SDK. |
| [BhhdkmOqog32QwsV9obDWbNTnzt](https://jobs.colony2.com/c2/jobs/BhhdkmOqog32QwsV9obDWbNTnzt) | 11-09 02:56 | pulse-tart | READY | `610a59bb` | — | [23a69302-e…](https://jobs.colony2.com/c2/jobs/23a69302-e319-4813-b7a8-5cf73928f7fa) | Verification-hook direction waiting for human review; exact CI toolchain parity remains unverified. |
| [SGjbiyRNGOTSm74sd3QPTSxmfgF](https://jobs.colony2.com/c2/jobs/SGjbiyRNGOTSm74sd3QPTSxmfgF) | 11-09 02:48 | jobdb | success | `610a59bb` | A | [07c92827-2…](https://jobs.colony2.com/c2/jobs/07c92827-240d-488a-b6a8-7d250406fcfe) | JobDB lifecycle/timeline delivery completed and published. |
| [4912eea3-8db9-4130-b8b8-529b920eaf1d](https://jobs.colony2.com/c2/jobs/4912eea3-8db9-4130-b8b8-529b920eaf1d) | 11-09 02:42 | vz-macos | ACTIVE | `610a59bb` | — | — | API work iterated through repeated reviews; human removes public Placement. Revised plan ready after direction approval. |
| [YdFSHTjwIslP2hFpxaPlXDSaq6q](https://jobs.colony2.com/c2/jobs/YdFSHTjwIslP2hFpxaPlXDSaq6q) | 11-09 02:41 | vz-macos | failed_app | `610a59bb` | A | [289e028b-a…](https://jobs.colony2.com/c2/jobs/289e028b-a01f-473a-9cdb-4d04ed364931) | Linux executor lacks Apple SDK/codesign; returned concrete unmet native prerequisite without unchanged retry. |
| [5XivOhnMfQbK9GOtTPDdepv4RXD](https://jobs.colony2.com/c2/jobs/5XivOhnMfQbK9GOtTPDdepv4RXD) | 11-09 02:41 | cortex-assistant | READY | `610a59bb` | — | [18f1949f-5…](https://jobs.colony2.com/c2/jobs/18f1949f-58d5-4e5d-8fbe-59fdb6c94d83) | Assistant direction repeatedly expanded scope; human requests simple recipe loop and defers permissions. Resumed after census. |
| [14bf2980-813d-47f6-ac4b-e1cfc053b488](https://jobs.colony2.com/c2/jobs/14bf2980-813d-47f6-ac4b-e1cfc053b488) | 11-09 02:34 | c2ops | failed_app | `610a59bb` | A | — | c2ops implementation retained; required Nix codex/skill outputs uncached and executor builds disabled. |
| [1d3f2f9a-098a-471d-bf48-07c4171ec225](https://jobs.colony2.com/c2/jobs/1d3f2f9a-098a-471d-bf48-07c4171ec225) | 11-09 02:28 | vz-macos | success | `610a59bb` | HA | — | API usage audit completed; later implementation is a separate cohort job. |
| [4EGsNC56SdzmhpvlJzF1aCFtwBt](https://jobs.colony2.com/c2/jobs/4EGsNC56SdzmhpvlJzF1aCFtwBt) | 11-09 01:07 | pulse | success | `610a59bb` | HA | [9aAH9sxUsA…](https://jobs.colony2.com/c2/jobs/9aAH9sxUsAe4QdicgfVurBOavIG) | Corrected package check succeeded. |
| [WpLvreRXPAgXqpGD9wCuoZ51vIo](https://jobs.colony2.com/c2/jobs/WpLvreRXPAgXqpGD9wCuoZ51vIo) | 11-09 00:39 | pulse | failed_app | `610a59bb` | HA | [9aAH9sxUsA…](https://jobs.colony2.com/c2/jobs/9aAH9sxUsAe4QdicgfVurBOavIG) | Package probe uses invalid flake:go_1_26 reference. |
| [a8d1457a-cf71-410c-be71-c28f6330c031](https://jobs.colony2.com/c2/jobs/a8d1457a-cf71-410c-be71-c28f6330c031) | 11-09 00:37 | c2j | success | `610a59bb` | HA | — | c2j execution base/capabilities configuration change published after reviews. |
| [db9a0421-505f-4a8f-8229-1e982cd2a785](https://jobs.colony2.com/c2/jobs/db9a0421-505f-4a8f-8229-1e982cd2a785) | 11-09 00:25 | c2j | success | `610a59bb` | HA | — | Configuration-capability explanation completed without implementation review. |
| [289e028b-a01f-473a-9cdb-4d04ed364931](https://jobs.colony2.com/c2/jobs/289e028b-a01f-473a-9cdb-4d04ed364931) | 11-09 00:15 | root | failed_app | `610a59bb` | A | — | Root configuration work blocked by native macOS acceptance on Linux; missing prerequisite unchanged. |
| [f6b4e60d-2fb9-45aa-a791-b8f8ceaef0bd](https://jobs.colony2.com/c2/jobs/f6b4e60d-2fb9-45aa-a791-b8f8ceaef0bd) | 11-09 00:11 | root | cancelled | `33f64742` | HA | — | Cancelled root setup attempt; distinguish cancellation from failure. |
| [3bUmsll6yYzIbTVhOI3COMTvKlZ](https://jobs.colony2.com/c2/jobs/3bUmsll6yYzIbTVhOI3COMTvKlZ) | 11-09 00:01 | vz-macos | failed_app | `33f64742` | HA | [935b15d3-3…](https://jobs.colony2.com/c2/jobs/935b15d3-3550-48bd-a99f-f31d0fa495cd) | Native dependency points to unavailable developer-local Apple source; owner source/module graph needed. |
| [935b15d3-3550-48bd-a99f-f31d0fa495cd](https://jobs.colony2.com/c2/jobs/935b15d3-3550-48bd-a99f-f31d0fa495cd) | 11-08 23:57 | root | failed_app | `33f64742` | HA | — | Root setup also blocked by missing local Apple dependency; parent/child share cause. |

## Older parents inspected as supporting context

These six jobs are outside the creation window and are excluded from cohort counts. They explain retained handoffs, cancellations, restored candidates, and waiting parents.

| Job | Cell | Created UTC | Observed state |
| --- | --- | --- | --- |
| [07c92827-240d-488a-b6a8-7d250406fcfe](https://jobs.colony2.com/c2/jobs/07c92827-240d-488a-b6a8-7d250406fcfe) | root | 2026-11-07 02:31 | PENDING_JOBS |
| [23a69302-e319-4813-b7a8-5cf73928f7fa](https://jobs.colony2.com/c2/jobs/23a69302-e319-4813-b7a8-5cf73928f7fa) | root | 2026-11-07 02:56 | PENDING_JOBS |
| [3Lkn1955P8gAaHVdCfJSseHtvCm](https://jobs.colony2.com/c2/jobs/3Lkn1955P8gAaHVdCfJSseHtvCm) | cortex | 2026-11-06 23:11 | PENDING_JOBS |
| [9aAH9sxUsAe4QdicgfVurBOavIG](https://jobs.colony2.com/c2/jobs/9aAH9sxUsAe4QdicgfVurBOavIG) | pulse | 2026-11-08 08:31 | cancelled |
| [Mw4GH987vPBwuA2tUL2TlcOqZyB](https://jobs.colony2.com/c2/jobs/Mw4GH987vPBwuA2tUL2TlcOqZyB) | c2j | 2026-11-07 00:22 | failed_app |
| [SVYbGlC2gSzO0r8bUo1bEkBx1tT](https://jobs.colony2.com/c2/jobs/SVYbGlC2gSzO0r8bUo1bEkBx1tT) | c2j | 2026-11-06 23:23 | cancelled |

## Failed-job grouping

This groups the 18 failed jobs by primary observed blocker. Related parents, children, and probes are not independent incidents.

| Group | Jobs |
| --- | ---: |
| Old handoff/turn-limit failures | 3 |
| Environment, dependency, and package failures | 9 |
| Controller-style recovery assignments ordinary build tasks cannot perform | 2 |
| Recovered-workspace/configuration gate failures | 2 |
| Hosted verification/acceptance failure | 1 |
| Corrected inline helper binding failure | 1 |

## Separately requested follow-up outside the window

This job was inspected after the audit at the user's request. It is excluded
from the 44-job cohort, revision distribution, and failure counts above.

| Job | Created UTC | Cell | Outcome | Recipe | Parent | Finding |
| --- | --- | --- | --- | --- | --- | --- |
| [0NUMMlLN6YlOv34xXc4sQcW2AKo](https://jobs.colony2.com/c2/jobs/0NUMMlLN6YlOv34xXc4sQcW2AKo) | 2026-11-09 19:46:37 | cortex-assistant | failed_app | `1c7cdc74` | [18f1949f…](https://jobs.colony2.com/c2/jobs/18f1949f-58d5-4e5d-8fbe-59fdb6c94d83) | Approved recovery started in read-only design. Patch changes did not persist; dependency execution was rejected by the phase gate. Failed after two agent turns, without hitting a turn cap. |

Raw histories and exploratory downloads remain in scratch; selected producer references and reproducible comparisons are in [evidence.md](evidence.md). No observed job was answered, cancelled, restarted, resubmitted, or edited.

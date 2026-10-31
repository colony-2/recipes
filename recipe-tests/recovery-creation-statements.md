# Recovery and reviewed creation test statements

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Git | `recipes/develop/merge-review.yaml` | Incomplete accounting is corrected against the same candidate and reviewer session before acceptance or implementation revision. |
| Critical | Integration / c2j | `recipes/develop/accounting.yaml` | Repeated invalid accounting requests human direction; cancellation prevents publication and retains evidence. |
| Critical | Integration / c2j | `recipes/develop/accounting.yaml` | Missing, duplicate, extra, incorrect, or unexplained file entries cannot authorize publication. |
| High | Integration / c2j | `recipes/develop/accounting.yaml` | Empty candidates accept empty accounting only with a substantive review message and the existing human acceptance gate. |
| Critical | Integration / c2j, Git | `recipes/kernel/resolve-target.yaml` | Target discovery distinguishes readable refs, absent local repositories, empty repositories, missing refs, and unresolved access without checking out the target. |
| Critical | Integration / c2j | `recipes/light/coordinate.yaml`, `recipes/develop/coordinate.yaml` | Creation requests reach the configured root without consulting an unavailable target; repeated keys reuse the recorded creation job. |
| Critical | Integration / c2j | `recipes/kernel/create-request.yaml` | Failed publication or registration never establishes readiness, even when the creation job completes normally. |
| Critical | Integration / c2j, Git | `recipes/create/publish.yaml`, `recipes/create/initialize.yaml` | Approved initial contents are published by a job owned by the destination cell, preserving root history. |
| Critical | Integration / c2j reviews, Git | `recipes/create/review.yaml`, `create.yaml` | Human review binds repository identity, initial contents, and catalog edits before publication or registration edits. |
| Critical | Integration / c2j | `recipes/light/develop.yaml`, `recipes/light/agent.yaml` | Delegation-only creation remains light; feature requests remain unfinished until subsequent feature work succeeds. |
| High | Integration / c2j, Jev | `recipes/build/classify.yaml` | Classification assesses local coordination independently of architecture and implementation delegated to reviewed child workflows. |
| Critical | Integration / c2j | `recipes/kernel/recovery.yaml` | Recovery retains stage errors and completed effects; uncertain side effects require reconciliation instead of automatic replay. |

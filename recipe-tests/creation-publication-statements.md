# Creation publication failure expectations

These extend the creation statements: unsuccessful Git publication is a job
failure, not a successful `publication_failed` or `registration_failed` result.
Non-publication review and recovery outcomes retain their existing contracts.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, Git | `recipes/create/initialize.yaml`, `recipes/create/publish.yaml`, `create.yaml` | Rejected initial publication fails initialization and creation, preserves diagnostics, and never registers the unpublished cell. |
| Critical | Integration / c2j, Git | `recipes/create/publish.yaml` | When later publication fails, earlier published identities and the failing child identity remain available as durable artifacts. |
| Critical | Integration / c2j, Git | `create.yaml` | Rejected catalog publication fails creation while retaining published cell identities; successful cell repositories remain intact. |
| Critical | Integration / c2j, Git | `create.yaml` | Catalog squash failures propagate without attempting merge, rebasing, or replacing their diagnostic with a generic failure. |
| Critical | Integration / c2j, Git | `recipes/create/initialize.yaml`, `create.yaml` | Successful creation preserves initial Git identity and independent cell histories; catalog publication uses separate squash and merge operations. |
| High | Integration / c2j, Git | `recipes/create/initialize.yaml` | Initial publication never rebases onto an existing destination or overwrites unrelated history. |
| High | Integration / c2j, Git | `create.yaml` | Catalog advancement fails publication without silently rebasing the reviewed catalog or restarting successful initialization jobs. |

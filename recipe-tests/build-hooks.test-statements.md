# Build hook test statements

These expectations were defined in the proposal before implementation. Each statement
is under 30 words; filenames and test metadata are annotations. The statements were
attached to embedded smoke job `3LOOfSLnqLLoayFvqXrsPL6KHYF`.

| Expectation | Importance | Kind / dependencies | Files |
| --- | --- | --- | --- |
| Light and heavy builds share applicable hook contracts; design hooks run only on the heavy path. | Critical | Integration / embedded c2j | `recipes/light/develop.yaml`, `recipes/develop/develop.yaml` |
| Configuration runs before classification and persists across revision, upstream chasing, and escalation. | High | Integration / embedded c2j | `build.yaml`, `recipe-tests/build-hooks-flow.test.yaml`, `recipe-tests/build-specialists.test.yaml` |
| Prompt additions reach their intended phases without replacing workflow instructions or accumulating duplicate text. | High | Integration / embedded c2j | `recipes/develop/agent.yaml`, `recipes/light/agent.yaml` |
| Named values reach later hooks through the settings artifact without being evaluated as templates. | High | Integration / embedded c2j | `recipe-tests/build-hooks-flow.test.yaml`, `recipe-tests/build-specialists.test.yaml` |
| Research evidence reaches design and plan review; redesign refreshes that evidence. | High | Integration / embedded c2j | `recipes/develop/develop.yaml`, `recipe-tests/build-hooks-flow.test.yaml`, `recipe-tests/build-specialists.test.yaml` |
| Required design work selects heavy; configured outcome specialists also run on light builds. | Critical | Integration / embedded c2j | `build.yaml`, `recipe-tests/build-light.test.yaml` |
| Required security consultation needs an explicit passing assessment; agreement on adverse findings cannot satisfy the gate. | Critical | Integration / embedded c2j | `recipe-tests/build-hooks-flow.test.yaml`, `recipe-tests/build-specialists.test.yaml` |
| Updated proposals and candidates cannot reuse stale specialist assessments. | Critical | Integration / embedded c2j | `recipe-tests/build-kernel.test.yaml`, `recipe-tests/merge-chase.test.yaml` |
| Missing hooks produce explicit skipped evidence without invoking an existing build script. | Critical | Integration / embedded c2j | `recipes/develop/verify.yaml`, `recipe-tests/verification.test.yaml` |
| Required verification blocks successful completion when the hook is absent or skips. | Critical | Integration / embedded c2j | `build.yaml`, `recipe-tests/verification.test.yaml` |
| Failing tests return evidence to implementation and prevent merge. | Critical | Integration / embedded c2j | `recipes/develop/verify.yaml`, `recipe-tests/verification.test.yaml` |
| Invalid hooks, denied capabilities, timeouts, and malformed outputs never become skipped or successful verification. | Critical | Integration / embedded c2j | `recipe-tests/verification.test.yaml` |
| Preparation changes appear in the candidate inventory and receive the normal assessment and outcome review. | Critical | Integration / embedded c2j | `recipes/kernel/git-candidate.yaml`, `recipe-tests/build-hooks-flow.test.yaml`, `recipe-tests/build-specialists.test.yaml` |
| Verification cannot approve a candidate it modified. | Critical | Integration / embedded c2j | `recipes/develop/verify.yaml`, `recipe-tests/verification.test.yaml` |
| Unchanged and delegated outcomes run configured verification before successful completion. | High | Integration / embedded c2j | `recipe-tests/build-light.test.yaml`, `recipe-tests/completion-review.test.yaml` |
| Upstream advancement repeats preparation and verification; changed preparation or hook definitions invalidate approval reuse. | Critical | Integration / embedded c2j, Git fixture | `recipe-tests/merge-chase.test.yaml` |
| Publish runs after successful merge using that exact commit, even if the target branch advances. | Critical | Integration / embedded c2j, Git fixture | `recipe-tests/build-merge.test.yaml` |
| Unchanged, delegated, cancelled, and failed-merge outcomes do not invoke publish. | Critical | Integration / embedded c2j | `recipe-tests/build-merge.test.yaml` |
| Publish failures propagate through ordinary execution handling without a recipe-specific recovery workflow. | High | Integration / embedded c2j | `recipe-tests/build-merge.test.yaml` |
| Hook evidence cannot overwrite approved specifications or canonical review reports. | High | Integration / embedded c2j | `recipe-tests/verification.test.yaml` |
| A local hook can include an unpushed relative recipe and run against its pinned candidate. | High | Integration / embedded c2j, Git fixture | `recipe-tests/verification.test.yaml` |

Use fixture hooks and mock publishing operations for recipe tests. Do not publish
real packages or deployments to validate orchestration. Confirm native hook behavior
with `c2j submit --advanced-recipe-file ... --run --embed`; static validation alone does not
resolve repository-local hooks.

| Hook identity expectation | Importance | Kind / dependencies | Files |
| --- | --- | --- | --- |
| Relative hook includes outside the hook directory invalidate reused approval when their definitions change. | Critical | Integration / embedded c2j, Nix | `recipe-tests/build-hook-identity.test.yaml` |
| Missing hooks remain unchanged across unrelated edits; external selectors conservatively require renewed review for each candidate. | High | Integration / embedded c2j, Nix | `recipe-tests/build-hook-identity.test.yaml` |

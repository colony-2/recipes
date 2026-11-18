# When to test, wait for a job, or ask about publication

I recommend two short prompt replacements in the default Adaptive3 build. Tell the implementer what happens after local testing, and tell a consumer exactly when it can use an upstream change. The shared context currently says to wait for “publication and availability.” That leaves a Git consumer looking for a second signal after the delivery job succeeds. A recent c2ops recovery illustrates the related ordering problem. The agent reached human input because acceptance required evidence of a publication that acceptance itself would unlock. [Shared context](../../recipes/adaptive3/prompts/context.yaml) · [c2ops job](https://jobs.colony2.com/c2/jobs/77cU2aMTlfszeZR6EXqk82AIZhG)

## Suggested prompt wording

**Implementation.** Consolidate the two existing instructions about focused checks and managed verification into one passage. [Implementation prompt](../../recipes/adaptive3/prompts/execute.yaml)

> Run focused local tests that exercise your fix, including edits to a verify hook. When those checks pass, return the candidate for review. The recipe runs the cell’s configured suite before merge and sends failures and diagnostics back to you for repair. The recipe handles merge and publication.

**Cross-cell dependencies.** Replace the shared instruction to wait for publication with the following. Keep the existing guidance on compatibility order and isolated testing of unfinished work. [Dependency guidance](../../recipes/adaptive3/prompts/context.yaml)

> Wait for the job delivering the upstream change to succeed. For a Git dependency, that success is sufficient. Update your pin if needed and test your consumer normally. For a precompiled Nix package or Docker image, continue when the delivery job publishes it. If publication is manual, ask the human to confirm it once the job succeeds, then resume the dependent check.

The relevant job is the one assigned to deliver the change. A successful investigation can report a finding while delivery is still pending. Reuse the existing job wait for work in progress and the existing recovery path for a failed delivery. For a manual release, one question is sufficient, for example “The c2ops delivery job succeeded. Has the Nix package containing that fix been published for this worker?” An affirmative answer lets the consumer proceed. Its normal build or test will surface a stale pin or an unavailable package.

## Additional adjustments

- **Align planning and assessment.** Replace Preparation’s existing deployment warning and align Validate’s existing deployment sentence with the same rule. Suggested wording is “Assess the candidate with pre-merge evidence. When the assignment requests a release, assess that result after the release step.” This keeps a generated test plan from turning publication into a prerequisite for its own merge. Integration can still report the actual result of a requested release. [Preparation and Integration](../../recipes/adaptive3/prompts/execute.yaml) · [Validate](../../recipes/adaptive3/prompts/validate.yaml)
- **Check the suite behind the promise.** Adaptive3 runs the configured verify hook. A missing hook can skip unless verification is required, and the runtime’s hook-source policy determines which hook revision runs. In Recipes, the hook calls a narrow purpose-document check while GitHub Actions runs the broader recipe tests. I’d have Recipes wire its intended suite into pre-merge verification as a separate change. Each producer owns automating its package or image publication. [Hook contract](../BUILD_HOOKS_USER_GUIDE.md) · [Recipes hook](../../.c2/recipes/hooks/build/verify.yaml) · [Local check](../../build.sh) · [CI suite](../../.github/workflows/recipes.yml)

## How to judge the change

The existing lifecycle test exercises a real verify failure and checks that its diagnostic reaches the working agent. For a hook edit, extend that coverage with a candidate hook whose diagnostic differs from the base version, under the supported candidate-source policy. For the prompt wording, inspect a small sample of subsequent jobs. A Git consumer should resume on delivery success, an automatically published package should need no human input, and a manual package consumer should ask once after success. Those observations would justify any further change to orchestration. [Lifecycle tests](../../recipe-tests/adaptive3/lifecycle.test.yaml)

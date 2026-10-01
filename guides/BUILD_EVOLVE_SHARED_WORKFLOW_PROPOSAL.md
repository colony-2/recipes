# Shared build and evolve workflow

Build and evolve use one workflow. Build starts at the cell root; evolve starts
in `.c2j` and explains that the requested changes concern workflows and their
instructions. Applicable `AGENTS.md` files provide domain guidance. Both read
`.c2j/mandate.md` at the cell root. `target_directory` can specialize the working
directory without introducing a custom changed-file enforcement system.

The primary recipe orchestrates these phases:

1. Assess mandate fit and author a design, consulting other cells when helpful.
2. Independently review the design.
3. Maintain the Markdown test plan, then independently review its coverage.
4. Obtain human approval of the design and test plan through native document review.
5. Implement, with independent specification and quality reviews.
6. Execute the verification hook and present its actual outcome.
7. Obtain human satisfaction, then squash merge into the upstream branch.

Feedback continues implementation in the same Codex session. Requirement changes
return to design and renewed plan approval. Reviewers have independent sessions.
Invalid structured responses or missing sessions stop the run. Failed verification
returns directly to implementation with evidence; unresolved questions go to human
feedback. Uploaded edits, including CriticMarkup, require revision and another
review even if the submitted decision was approve or satisfied.

## Documents and routing

| Content | Location | Why |
|---|---|---|
| Cell mandate | `.c2j/mandate.md` in Git | Maintained responsibility boundary |
| Test plan | `.c2j/test-plan.md` in Git | Maintained behavioral expectations |
| Design | `outbox/design.md`, then downstream inboxes | Job-specific design and review handoff |
| Implementation summary | `outbox/implementation.md`, then downstream inboxes | Job-specific outcome review |
| Verification report and logs | `outbox/verification.md`, `outbox/build.log` | Execution evidence |
| Phase routing | `outbox/result.json` | Small schema-validated decisions |

Designs and summaries do not accumulate in the repository. The test-plan review
artifact `test-statements.md` is an exact copy of the maintained plan. c2j stores
reviewed revisions and receipts. Agents read documents from their inbox, and use
Git history for mandate, test-plan, and implementation changes. No custom hashes,
requirement IDs, statement catalogs, or semantic validation certificates are needed.

A phase response has `summary` and `next`. Authors use `review`, `continue`, or
`ask_user`; design also supports `outside`, and implementation supports `redesign`.
Design and implementation can use `consult` with `{cell, message, ref?}`. Independent
reviewers return `done`, `revise`, or `ask_user`. Schemas check these routing fields;
agents and humans judge whether the content is sound.

Test statements remain Markdown, at most 30 words per statement, with relevant
filenames, importance, unit/integration classification, and dependencies. Include
positive and negative cases for critical behavior. Independent review assesses
coverage, meaningful assertions, and feasibility. Existing expectations must not
be weakened to make implementation pass; describe proposed changes and their
deprecation plan for human review.

## Verification and integration

`verify.yaml` uses native `command_execution` to run `bash ./build.sh` in the
selected target directory, with a ten-minute default timeout. It preserves the
log and inspects the native success, exit-code, and timeout outputs. An absent
hook is explicitly reported as **skipped**, with no claim that automated checks
passed; the human can still accept the outcome. Failure returns to implementation.

A project can specialize this phase with its own verification op, including a
GitHub Actions op for an existing workflow. Keep the `ok`, `result`, `evidence`,
`review_documents`, and `artifact_refs` outputs used by the coordinator. There is
no per-statement command executor in the default recipe.

c2j supplies the current Git candidate and checkpoints changes automatically.
`finish.yaml` requires acceptance and a successful verification step, then calls
`squashrebasemerge` with the native current hash and `rebase: false`. Upstream
advancement stops integration; it does not silently rebase an accepted outcome.

## External work

[Cross-cell sessions](CROSS_CELL_REPO_SESSIONS_DESIGN.md) apply during both design
and implementation. Consultation retains separate session objects and the latest
reply for each destination cell. Actual prerequisite work is submitted only after
human design approval. The runtime's `jobs.job_ids` supplies dependencies, and
`recipe.await_result_soft` waits for all of them. All terminal results, including
failed and cancelled work, return to the requesting session for diagnosis.

The defaults resolve from `github.com/colony-2/recipes` when committed local
`.c2j/recipes/build.yaml` or `.c2j/recipes/evolve.yaml` overrides are absent. Local
wrappers can include this shared workflow by Git selector. Invalid recipes and
access failures do not trigger fallback.

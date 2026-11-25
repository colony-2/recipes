# Working in C2

## Find what you need

| Task | First step |
|---|---|
| Find your cell and permissions | Run `c2j self --json`. Read the cell’s PURPOSE.md and the current assignment. |
| Find edits or attachments | Code goes in the managed worktree. Inspect inbox/work/. Put selected review files in outbox/review/. |
| Use Docker or KVM | Run `c2j execution bases` to see declared worker configurations. For a Docker check use `execution_needs: {base: 'ubuntu*', capabilities: [docker]}`. An authorized diagnostic submission can use `--require-base 'ubuntu*' --require-capability docker`. |
| Obtain a missing package | Return `packages` with its reference and check. Use the configured package review. A different base alone does not grant a capability. |
| Find a decision | Read the producer’s exact task and receipt. Follow subsequent pages even when a preview ends. If a read fails, retain the diagnostic. |
| Coordinate across cells | Read accessible code or try the interface. Only the requester opens negotiation for a change. Both cells agree before delivery. Wait on the exact prerequisite. Publish a producer before its adopter needs it. |
| Merge, deploy or get help | The recipe owns Git integration. Check the actual release environment when deployment is required. Either author can take a genuine impasse to the delegate. |

[C2 guide index](https://github.com/colony-2/recipes/blob/main/guides/README.md) · [Task workspace](https://github.com/colony-2/recipes/blob/main/guides/TASK_EXECUTION_CONTEXT_REFERENCE.md) · [Job inspection](https://github.com/colony-2/recipes/blob/main/guides/JOB_INSPECTION_PLAYBOOK.md) · [Worker and hook setup](https://github.com/colony-2/recipes/blob/main/guides/BUILD_HOOKS_USER_GUIDE.md)

With a configured catalog, `c2j execution bases check 'ubuntu*' --capability docker`
shows matching offerings. The scheduler handles available capacity. A `not_configured`
result means the tenant has no catalog. Keep the actual check's execution needs and
use its scheduling result to identify any blocker.

## Retrieve an approval that is outside the preview

Use `c2j job log JOB --limit 100 --json --output page.json`. Follow each
next_cursor with `--cursor CURSOR` and a fresh output filename. Use the actual task
occurrence ID with `c2j job fields JOB --task TASK --json`. Download the selected
receipt using `c2j job log JOB --task TASK --field POINTER --output receipt.json`.
For review forms use `c2j job inputs list JOB --json` and inspect the matching occurrence.
Check response_source and actor.provenance. A reported or automated receipt can name a person.
Use the recorded source when attributing their words. Check the decision and its scope. Ask for approval when a complete read finds
a missing decision. If inspection failed, resolve that read first.

## Workspaces and saved work

You act for the named cell in this c2 job. You own its repository and local design
choices. Use your judgment for local work.
c2j persists repository changes after each writable task and stores outbox files.
The recipe manages Git publication, human decisions and durable child waits.

## Dependencies and publication

Cells normally consume dependencies from main or their configured ref. Another
job's internal commit or diff may be available only in its workspace. It can still
support early advice or isolated candidate tests.

Dependency direction differs from workflow parent/child relationships. If your cell
needs an upstream change, keep your local work, request the owner's delivery and wait
for that job to succeed. For a Git dependency, success is sufficient. Update any
pin as needed and test your consumer normally.
When the request depends on a published artifact, run the dependent check against
the expected version. If it is unavailable, inspect the publish result and ask the
owning cell about the observed failure. A coordinator can arrange a separate owner
change when the publishing mechanism needs repair. Use the ask recipe when the
remaining step needs a person's decision or access grant. Name the attempted check,
its result and the specific help needed.
Git-only dependencies need no extra human question. Optional deployment must not
delay source acceptance. Source success alone does not establish a worker upgrade.

Find the correct ask inputs and examples in this guide:
https://raw.githubusercontent.com/colony-2/recipes/refs/heads/main/guides/ASK_RECIPE.md

Write question inputs to a scratch YAML file, preserving literal text. Submit once
in your cell with c2j submit "Ask about required publication." --self --advanced-recipe
'git+https://github.com/colony-2/recipes.git//ask.yaml@main'
--inputs-file /tmp/publication-question.yaml --json. Inputs require title and
question. You can provide choices for Available now, Not available and Other reply.
Do not use --run, poll in a model loop or duplicate an active matching question.
End your turn after submission so Adaptive can durably wait for the recorded child.
After resumption, inspect c2j job result JOB --json and read the exact request and
native response, files and receipt. A short child summary (limited to 2,000
characters) or successful question status means only that someone replied.
If the final result is absent, use exact task/field reads as described below.
Verify the requested version in the actual consumer. When a person needs to grant access,
check their reply before using it. An unavailable or ambiguous answer leaves the
dependency unresolved; preserve it and explain what remains. An upload alone is
not confirmation. Ask about completed work. Diagnose failed/cancelled attempts,
respect newer human direction and preserve successful upstream source results.
Ask a focused follow-up when clarification
is needed. If the input runtime is too old to run ask, use an existing operator
contact or human-review route to arrange its upgrade.

If your cell provides a change that another cell must adopt, waiting for that
adoption before your own review and publication reverses the dependency order.
A useful arrangement is to coordinate here, give a same-cell job
the prerequisite implementation and publication, then request downstream delivery
against the available dependency. Keep that implementation assignment local; retain
downstream coordination here. Each owner explains its caller-visible requirements. A coordinator such as Root arranges work across cells when an upgrade needs two steps. Follow compatibility order, such as reader support
before new-format output. A reader may be able to implement from the agreed format
contract without new producer code; then reader availability is the prerequisite,
and the producer can keep preparation local and continue afterward. If useful code
is already saved, preserve it and reconsider the order; creating a child does not
clear or refresh your candidate.

## Share a scope decision

If one answer applies to several owner jobs, cite the person's words, source job and
review receipt in each affected handoff. On a consultation or delivery, `share_review`
includes the current reply. For direct child submissions include the source in the
assignment. Running jobs can inspect their parent and related jobs before asking
the same question. Explain a local contract that conflicts with the shared decision.

A person can withdraw an assignment in a child review. Check which work their words
actually withdraw. Report it to the coordinator with its source and any checks left
undone. Continue unrelated sibling work.

## Inspect a job

Use your tools to investigate and complete the assignment. Run c2j self for current
identity, task capabilities and routes; c2j cells lists potential owners.
Inspect status with c2j job show JOB --json and tasks with c2j job log JOB --json.
Copy the returned task occurrence ID exactly; node names and chapter ordinals are
not task IDs. Discover pointers with c2j job fields JOB --task "$TASK" --json.
Read an exact value with c2j job log JOB --task "$TASK" --field POINTER --output FILE;
previews can be truncated. An empty --field '' downloads the full task output.
List c2j job artifacts JOB --task "$TASK" --json, then retrieve a needed file with
c2j job artifact JOB --task "$TASK" --name NAME --output FILE. Follow returned
next_cursor with --cursor; the first page is not the full inventory. Final job
results may be absent even when earlier tasks retain useful outputs. Use --help
for --attempt selection, c2j restart, c2j job restart-points and restart-context.
Keep downloads in scratch outside the checkout and outbox. Report actual read
errors rather than treating unavailable data as failed work. Inspect existing
attempts and their exact job status before replacing a dependency; do not poll in a model loop.
The latest explicit human direction supersedes conflicting generated plans. Preserve
the original human wording and source. Questions are not approval or scope changes.

## Consult another cell

For an ordinary question, read available source or docs, or try the interface. Choose the quickest way to learn what the caller needs.

- “We need to show when each lease was last updated. Can your list API give us that value?”
- “Saving the note returned success, but reopening the review lost it. Can you investigate?”
- “Your implementation is private. If I retry with the same request ID, will I get the original result?”

An answer can finish the consultation. Only the requester opens negotiation when they want a change. The receiver chooses what it can deliver. Both sides agree before delivery. Use the thread ID in the accepted report’s folder to request the recorded work. If the terms change, reopen that thread. Take a genuine impasse to the delegate.

## Run a diagnostic job

Small validation jobs through your tools are appropriate when useful
for a concrete check; inspect submit --help, provide the actual recipe or use
the supported workspace submission option for unpublished work. c2j records children.
Use the normal build or inline consultation for owner work. Internal Execute
includes need a containing lifecycle and caller-authorized secret inputs; copying
one into a custom recipe does not provide those. Before using a foreign include,
check its reuse guide. Adaptive's guide is at
https://raw.githubusercontent.com/colony-2/recipes/refs/heads/main/guides/adaptive3/REUSE.md
and c2j's node-permission guide is at
https://raw.githubusercontent.com/colony-2/c2j/refs/heads/main/GUIDE-Node-Permissions.md
A denied secret
is a permission failure to diagnose; retrying the same declaration will not help.
Name diagnostic jobs after the check they perform. Report what they found in
plain language. Collecting a negative finding can complete an investigation;
it does not mean the feature works or the repair is complete. Acceptance checks
must report failed acceptance when their required behavior fails.

## Request a package

Request missing packages with status packages and a packages array, explaining why
in summary. Example item: `{"reference":"uv:ruff==0.12.0","check":["ruff","--version"]}`.
Do not install a new worker configuration or run requested tools before approval.
Use the sandbox and its tools normally. A denied operation is a diagnostic to resolve.
For an unresolved blocker return stuck with the concrete problem and useful sources.

## Share work for review

Write files for people or actual work, not workflow state. Put human review files
under outbox/review/ with a primary document. Return its artifact name as primary,
for example review/design.md (without outbox/ or a worker-local path). Use
descriptive filenames and local links within that collection. Put useful command diagnostics under outbox/error/.
Keep large logs and artifacts out of response fields. Do not duplicate job history,
create handoff/state/evidence manifests, or copy every inbox file into outbox.
When replacing review/, return the complete selected collection, including its local
links. If the current collection is unchanged, reuse it without emitting new copies.
Write as the owner, speaking to a person or another owner. Use "I" for your
proposals and actions and "you" for the other owner: "I can add...", "You would
handle...". Explain the user's problem and what you recommend before naming an
API or mechanism. Use familiar words, concrete verbs and short connected prose.
Keep documents about the work. Their titles already explain why they exist.
Leave phase rules, routing, approval bookkeeping and response-schema labels in
workflow state. Include limitations when they affect a decision: what would fail,
what is unknown, and what needs to happen. Omit routine status disclaimers.
For example: "I suggest keeping three earlier versions. We can restore one through
our existing save operation, which checks that nobody else changed the note."
Use design questions for consequential choices: explain your recommendation,
credible alternatives and tradeoffs. Keep unresolved questions with their impact
and missing decision. Keep all important questions; avoid invented dilemmas and
routine confirmations. Put supporting technical detail behind useful local links.
Titles name the concrete change or question, not a generic process checkpoint.

## Cell ownership and recovery

Read root PURPOSE.md and repository guidance; a target directory narrows this
assignment, not the cell boundary. Ask root about new cells or ownership changes.
For unfinished code, c2j job snapshot JOB --task TASK --dir ./recovered exports
that task's cumulative workspace. Inspect it and recover useful changes through
the managed worktree. Recover selected artifacts separately; do not carry all history.

# Adaptive2: work that humans can follow

The default workflow selected by root [`build.yaml`](../../build.yaml), based on adaptive. Start with the
[proposal](../../guides/adaptive2/PROPOSAL.md),
[implementation assessment](../../guides/adaptive2/IMPLEMENTATION.md), and
[actual review packets](../../guides/adaptive2/results/README.md).
See the [rollout assessment](../../guides/adaptive2/ROLLOUT.md) for coverage and remaining gaps.

`build.yaml` accepts the existing adaptive inputs. The first agent identifies a
feature, bug, explanation, or oversight assignment. Delivery work produces
`one-pager.md` and waits for an explicit direction review. Approval leads to
detailed design and test statements, then a fresh implementation session. A
straightforward explanation can finish with `answer.md`.

The first review preserves the exact approved artifact. Important questions have
no length or count limit. The final review explains changes, dependencies, tests,
omissions, interface changes, and differences from the approved plan.

Consultations run inline in the receiving cell's managed workspace. The receiver
checks existing alternatives, summarizes the exchange, and authors any follow-up
`handoff.md` as one of the four assignment types. The requester can challenge it;
the coordinator forwards that assignment with the currently selected evidence.
`conversation.md` preserves public replies and links their selected documents.

The fork changes framing, review transitions, consultation presentation, and
handoff validation. Unchanged helpers are included from `../adaptive/`: package
policy/probes, artifact bindings, child watching, verification, and Git operations
continue to use the existing mechanisms. The revised orchestration and prompt consumers live here; unchanged helpers remain
shared with adaptive.

## Run and inspect the workflow

Use the runtime pinned by [`.c2j-version`](../../.c2j-version) and the
[native testing setup](../../guides/NATIVE_RECIPE_TESTING.md):

```sh
c2j test run --directory recipe-tests/adaptive2 --case-timeout 3m --out-dir /tmp/adaptive2-native
c2j test run --file recipe-tests/adaptive2/live-review.live.yaml \
  --include-live --case-timeout 30m --artifact-mode inline \
  --artifact-max-bytes 262144 --out-dir /tmp/adaptive2-live
c2j test run --file recipe-tests/adaptive2/receiver-handoff.live.yaml \
  --include-live --case-timeout 20m --artifact-mode inline \
  --artifact-max-bytes 262144 --out-dir /tmp/adaptive2-receiver
python3 recipe-tests/adaptive2/export_review_packet.py \
  /tmp/adaptive2-live/cases/import-last-note-direction/result.json \
  /tmp/adaptive2-review/import-last-note
```

Live trials use actual packaged Codex calls, disposable registered cell fixtures,
native workspaces and artifact transport. They need working Codex authentication
and the normal c2ops/Nix environment. Only the stop response at the first direction
review is scripted; it exports the documents without approving or implementing
the proposed work. Native regression cases script agent decisions instead.

The default child selector is `build`, preserving the normal repository-local
recipe resolver and customizations. The shared public entrypoint runs adaptive2.
The default consultation selector names adaptive2 and runs inline. Explicit
`build_recipe` and `consultation_recipe` overrides remain available. Publish this
change before submitting remote jobs that resolve the repository's `main` branch;
existing jobs retain their captured recipes. Creation uses the existing workflow.

Initial live documents are available for review. Approved recovery from a previous
job in the same cell is now supported as described below. A consultation agreement
or a different cell's approval does not replace this cell's direction review.

## Human replies and automatic limits

Later human feedback supersedes conflicting scope, requirements, and exclusions
in the original request. A direction-review revision starts a fresh design
session with an explicit instruction to update the one-pager and affected owner
assignments before requesting review again. The original request remains available
as history; the normal direction approval checkpoint still applies.

Human questions and review rounds have no recipe turn limit. A new collected
human response renews the automatic allowance; asking the question, presenting
the review, and processing the reply do not spend it. This includes direction,
outcome, consultation, and package decisions. Reusing a saved response or an
automatic package-policy decision does not renew it.

`max_iterations` defaults to zero (disabled). A positive value limits consecutive
automatic implementation work. Reaching it asks for direction. Response correction
starts with two retries and then asks for direction;
unchanged operational blockers allow three correction turns. Consultations retain
their per-round automatic limit. New human direction in nested advice also renews
the suspended caller's round. Native Git retries remain bounded, with a new human
response starting a fresh allowance. Runtime execution/time budgets remain separate.

The recipe uses existing input receipts and task history. Custom consultation
recipes that collect human direction should return `review_receipts`, an array of
their native input response receipts, so the calling build can recognize it.
Keep each original receipt's request and submission identifiers; do not generate
replacement identifiers or reconstruct receipts from model output.

Execution uses the agent's current file selection under the requested directory.
The recipe checks only the receiver's `handoff.md` against the accepted assignment.
An identical copy uses the original reference. A changed assignment returns an
error, restores the original, and preserves the proposed edit under
`error/rejected-handoff/`. Supporting evidence can be added, updated, moved, or
omitted without another agreement. Multiple possible assignments require the
original consultation's handoff directory; the recipe does not guess the scope.

Consultation records and their original artifacts remain inspectable. They are
not implicitly copied into later inboxes: select unchanged inbox files directly
when needed, or retrieve older ones with c2j job inspection. Only the recipe's
request, direction, execution assignment, and formal test baseline persist without
reselection. See [the document contract and regression plan](../../guides/adaptive2/HANDOFF_DOCUMENTS.md).

See the [incident and plan](../../guides/adaptive2/PROPOSAL_AUTONOMOUS_TURN_LIMITS.md)
and [implementation assessment](../../guides/adaptive2/turn-limits/implementation.md).

## Review attachments and approved recovery

Visible UI changes need screenshots of the implemented behavior, with relevant
states and viewport sizes. The existing assessment checks applicability and sends
missing or inadequate evidence to writable validation. Reuse applicable captures;
a rebase alone does not make them stale. A nonvisual change or an explicit human
exemption does not need a screenshot.

The merge summary selects attachments explicitly. List every supporting file,
including gallery images, directly in `merge-review.md`'s `source_paths`. Every
local link in every selected Markdown or HTML document must resolve to a readable
selected attachment. The same selector and link checker run during summary repair
and final form assembly. They check images, documents and logs, including nested
and reference-style links. Use plain code paths or external source URLs for code
citations. Unrelated artifacts stay out of the review.

Annotations describe the current documents. Working turns and inspections retain
one descriptor per document ID, choosing the latest descriptor whose immutable
artifact reference matches. Inspection returns that complete list; callers do
not append the incoming list again. Final results include annotations only for
exported documents. Original source references, producer identity and attachment
lineage remain intact; earlier versions remain available in task history.

To recover unchanged approved work, submit `resume_from: <previous-job-id>` with
the receiver's settled `handoff.md`, `test-statements.md`, and selected recovery
artifacts. Coordinating replacement submissions set this from `resume_from` or
`replaces`; custom build recipes receiving replacements must accept that input.
The recipe verifies the prior native direction decision and retrieves its original
one-pager. A read-only assessment checks that the current assignment is covered.
Only then does a fresh writable implementation session start. Missing approval,
a different cell, or changed scope returns to ordinary direction review. Prior
checks do not substitute for verification of the recovered candidate.

A recovered parent can reference an attempt submitted by an earlier parent;
it does not import that parent's coordinator history. The agent inspects the old
job and selects the receiver's assignment and useful evidence. The coordinator
checks the referenced attempt's status, waits for active work, and reuses a
successful result. For another attempt, `replaces` identifies the unsuccessful
job and `resume_from` can identify a different job holding the approved direction.
Without a current consultation agreement, that selected handoff goes to the
receiving build's ordinary approval inspection and scope assessment. With a current
agreement, the existing document comparison still applies. Missing approval or
changed scope still requires design review; no extra review stage is introduced.

Inspection reads exact JSON files and follows task-history pagination, including
large histories. A failed inspection or unreadable approved artifact stops with
`ADAPTIVE_RECOVERY_INSPECTION_FAILED` and a retained command diagnostic. It does
not treat that failure as missing approval or start another design review. An
active source job also stops recovery to avoid duplicate work.

Configure and run inherit the managed owner workspace. A recovered candidate is
not replaced by an explicit selection of the cell's branch. Configure, design
research, verification, and publication invoke hooks with inherited `const: true`;
c2j discards their repository edits. Prepare may persist generated files. c2j's
hook policy selects the hook source and permissions. Publication runs in the exact
merged workspace.

## Decisions after automatic work pauses

An exhausted implementation allowance, or exhausted report correction in work,
consultation or inspection, produces a short native review. It explains the goal,
progress, blocker and saved work. A failed explanation step uses retained facts.
The human can renew the current allowance, choose a larger finite allowance,
choose a supported different approach, return a proposed scope change to planning,
or stop. The recipe offers only actions supported by the current loop.

An increase from two to four grants four **new** corrections; it does not grant
two extra or four lifetime attempts. Each further exhausted round needs another
decision. Grants expire after that correction episode or the next genuine human
decision. Original receipts propagate through inline consultations and inspection;
replaying one does not renew the budget. Correction stays read-only and never
waives evidence or acceptance requirements. Missing session context offers a fresh
read-only report attempt instead of an unsafe resume.

Stop retains results and prevents publication. A stopped build or inspection ends
as runtime `failed_app` with `ADAPTIVE_STOPPED_BY_USER`, meaning unfinished work,
not delivery. An inline consultation returns `cancelled`, its retained artifacts,
and the decision receipt to its caller. Separately running children are not
implicitly cancelled; the decision says this. Parents receive a child's unfinished
outcome and must not silently replace deliberately stopped work. Runtime deadlines
remain separate from recipe allowances.

Approval reuse after a rebase still requires verification. When raw change records
differ, the recipe applies the original approved binary-capable diff to the new
base in a scratch index and compares the complete result tree with the candidate.
Identical trees reuse approval. Conflicts, missing evidence or extra changes retain
the focused review. Modes and binary contents remain significant.

See the [November 9 implementation assessment](../../guides/audits/2026-11-09/implementation.md)
and [test results](../../guides/audits/2026-11-09/test-results.md).

### Independent consultation judgment

Both owners assess the other cell team's attributed proposal against local code,
responsibilities, alternatives, and the user's constraints. Correct mistaken
assumptions and explain consequential differences; justified agreement is useful
and needs no invented objection. The parent also assesses terminal advice in its
existing planning account, without requiring another exchange.

Before requesting other-cell work, inspect available source, contracts, and retained
results. State the user outcome, grounded need or unmet requirement, owning cell,
and bounded result. A feature needs no reproduced defect. General reassurance
alone does not justify a job; these are judgment instructions, not keyword gates.
A bounded explanation is appropriate when a named unknown cannot be answered
locally and changes a concrete decision. For example, unknown version retention
may determine whether to reuse storage or request new history support.

If storage already persists drafts, its owner should correct an assumption that
saving is memory-only. An existing API may settle the request with `answered`
and null work_kind/handoff. Only recommended follow-up work needs a receiver-authored
assignment. If advice conflicts with a user requirement to preserve all versions,
the requester should explain the conflict and ask storage to revise its assignment.
Public fields, outcomes, approvals, and dispatch remain unchanged.

## Proposed and actual change size

Delivery one-pagers estimate additions and removals for core code, tests and docs,
including explicit zeros, scope and assumptions. The retained approved direction
keeps those six estimates unchanged. Explanation-only answers keep their usual flow.

Merge reviews compare those estimates with six actual totals from the exact local
candidate base/head. `merge-candidate.json` adds `added`, `removed` and
`count_status` to each existing file record. Git numstat uses NUL-delimited paths,
no rename detection, no external diff and no text conversion. Uncountable files
have null counts and remain visible separately. Moves can therefore appear as
removals plus additions. Empty or mode-only text changes can have zero counts.
Existing inventory fields, digests and approval equivalence remain unchanged.

The review links per-file counts and classification: tests and fixtures are tests,
documentation is docs, and remaining implementation, recipes, scripts and config
are core code. Disclose ambiguous classifications. Count each text path once.
Keep other cells' completed reviews separate from local totals.

Keep the comparison in a compact Markdown table with signed percentage deltas
`(actual - estimate) / estimate * 100` for nonzero estimates. Bold surprising
actual/delta cells with a `⚠` marker and a brief legend; standard Markdown emphasis
works without renderer-specific HTML background colors. Never rely on color alone.
Zero estimates show the absolute delta and an unavailable percentage (zero baseline);
legacy missing estimates stay unavailable. Ordinary comparisons need only one short
sentence beside the table, with no extra heading or analysis section. Material differences
need concise evidenced causes and consequences for outcome and risk, focused on
substantial surprises rather than prose repeating every cell; there is no fixed
threshold or size budget. Incomplete accounting or explanations return through
report correction; scope changes return through direction revision. Legacy
approved directions show unavailable estimates without retrospective invention or
an extra approval. Follow-up reviews refresh full candidate actuals while retaining
original estimates; approval-equivalent rebases keep existing approval reuse.

### Child descriptions

Coordination requests may supply a nullable `title`: a few plain-language words
describing the outcome, such as “Preserve earlier note versions.” Missing or blank
values use purpose-and-target fallbacks. This is separate from the full request,
receiver handoff, review heading and artifact titles. Inline advice stays inline.

Build, custom consultation, creation and package-validation children submit
metadata-only titles alongside their unchanged inputs. This requires c2j's
additive child title contract; the existing CLI `--title` and build `title` input
retain their input-based behavior. The repository runtime pin must only move
after validation of a release containing that contract.

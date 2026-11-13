# Adaptive2 history audit: what adaptive3 kept and what it lost

Audited on 2026-11-13. Adaptive3 revision: `47016ff`.

Adaptive3 preserves the main process: frame the request, obtain human direction,
prepare the work, implement and validate it, obtain outcome approval, and publish.
It also removes several mechanisms that caused repeated trouble: internal handoff
files, conversation state files, growing annotation lists, and recipe-owned Git
hash guards.

**That does not mean all the lessons from adaptive2 survived.** The largest gaps
are child recovery, cross-job approval reuse, diagnostic preservation, and some
repository-defined review requirements. Several other protections now depend on
agent judgment without the earlier supporting context or regression coverage.

This is an audit, not an implementation plan. No findings below have been fixed
as part of this audit. The preceding default-build switch was committed separately
as `47016ff`; its verification is in [ROLLOUT.md](ROLLOUT.md).

## Scope and evidence

I reviewed the latest **48 commits affecting adaptive2 or the shared build flow**
before adaptive3 was introduced. They span October 30–November 12, 2026. The first
23 directly touch adaptive2; the remaining 25 concern the shared implementation
and earlier build components from which it inherited behavior.

The selection is reproducible:

```sh
git log c0c69bd -48 --format='%H %ad %s' --date=short -- \
  recipes/adaptive2 recipe-tests/adaptive2 guides/adaptive2 \
  recipes/adaptive recipe-tests/adaptive build.yaml recipes/response-schemas.yaml
```

The historical endpoint is `c0c69bdca6788657ba02a2a53bd84c63c4d6d7cc`.
I compared the changed behavior, related explanations and tests with the current
adaptive3 source. Some commit subjects describe a merge review rather than the
problem fixed; the purpose column below describes the change itself.

This is a source-history audit. It does not establish how any currently deployed
job behaved. A source match is also not proof that an agent will consistently use
the available guidance well.

The available execution evidence is recorded in [TEST_RESULTS.md](TEST_RESULTS.md)
and [ROLLOUT.md](ROLLOUT.md): 42 underlying adaptive3 cases, three additional
public-build cases, eight direct validator tests, and two live agent trials.
Most orchestration tests script agent choices. The documented preinstalled-tool
environment substituted for this host's unsuccessful normal Nix activation.
There is no live UI delivery trial or complete production-worker validation.

Statuses mean:

- **Addressed:** the core behavior is present; relevant checks are named where available.
- **Replaced:** adaptive3 removed the mechanism that needed the fix. This does not require restoring it.
- **Partial:** part of the lesson is retained, but behavior or coverage is weaker.
- **Gap:** the specific capability or safeguard is absent or has regressed.

Across the 48 commits, the assessments are **13 addressed, 9 replaced, 21 partial,
and 5 gaps**. These count commit-level judgments, not separate bugs; several
commits address the same recurring problem. Prompt-level matches are labeled as
such and are not claims of demonstrated production behavior.

## Commits directly affecting adaptive2

Newest first. Each commit link opens the original change.

| Commit | Main purpose | Adaptive3 assessment |
| --- | --- | --- |
| [c0c69bd](https://github.com/colony-2/recipes/commit/c0c69bdca6788657ba02a2a53bd84c63c4d6d7cc) — Reconcile obsolete child requirements | Stop a failed historical child from blocking completion after human direction makes its outcome unnecessary, replaces it, or assigns it locally. Keep genuine outstanding work visible. | **Partial.** There is no separate failed-child completion gate to reconcile. [Validation](../../recipes/adaptive3/prompts/validate.yaml) judges current scope and explicitly excludes superseded prerequisites. However, discovering successful continuations and avoiding duplicate active work are only instructions; no equivalent replacement/adoption case is tested. See finding 1. |
| [a43ff5a](https://github.com/colony-2/recipes/commit/a43ff5a5c65d7aa33084364c9e919f58fc03065e) — Remove recipe-imposed timeouts | Stop short shell, model and inspection deadlines from killing otherwise valid work. | **Addressed.** Adaptive3 adds no execution deadline. Automatic iteration allowances are separate from elapsed time. The repository timeout scanner passed across 127 workflow/example files. Runtime cancellation and external limits remain runtime concerns. |
| [16c7427](https://github.com/colony-2/recipes/commit/16c7427c0475196691d9e7c6df0cd011bba8c8e8) — Render consultations with native templates | Remove Python used to format conversation state; preserve useful titles, links and selected evidence when constructing human-readable consultation output. | **Replaced.** Agents write human documents; native task records retain the exchange. [Consultation](../../recipes/adaptive3/consultation.yaml) does not render a conversation file. Prompt includes are empty sequences. However, there is no automatically assembled conversation overview; human inspectability still needs evaluation. |
| [f198c2d](https://github.com/colony-2/recipes/commit/f198c2ded29174b62a210f921c443d541fbf3081) — Validate final attachment titles | Prevent a final generated attachment title from exceeding the input-form contract, even when its source metadata passed earlier checks. | **Replaced.** The annotation-title assembly pipeline is gone. The exact review title is checked before the form and passed unchanged; `invalid-final-title` covers rejection. This does not address missing child titles, which have a separate fallback. |
| [67dc672](https://github.com/colony-2/recipes/commit/67dc672e1c309d8ec437ca28141c5c4305dec823) — Retain selected evidence after relocation | Keep selected supporting evidence and its identity when consultation documents move between namespaces; stop growing child-result payloads and avoid synthesized null outcome fields. | **Partial.** Adaptive3 avoids that relocation/annotation pipeline and replaces the current `review/` collection rather than accumulating its history. It still passes complete selected collections into consultation and complete native child results through feedback. It has no comparable long, nested, large-result stress test. See finding 8. |
| [71a0253](https://github.com/colony-2/recipes/commit/71a0253ccf64e2e3a2c041c0373cf77ad900a154) — Keep consultation state native | Eliminate `conversation.json` and unnecessary command-driven state/rendering; retain the conversation in recipe state and publish only useful presentation. | **Replaced.** Consultation uses native outputs and a small parent stack; no conversation/state manifest is generated. The only embedded tools are output validators. Nested advice is exercised by `nested-owner-advice`. |
| [50cce57](https://github.com/colony-2/recipes/commit/50cce572508cd54bfdbe8adbac48b901829a7e43) — Separate resolver discussion from permission to continue | Let humans ask questions without spending or renewing work attempts; require a separate resolution, keep the discussion, and make choices understandable. | **Partial.** `discuss-before-continuing` establishes that discussion does not resume work. But each resolver answer starts a fresh agent without the earlier discussion or previous proposal explicitly supplied. Its form also uses a generic title. Multi-question continuity is not tested. See finding 7. |
| [a431e25](https://github.com/colony-2/recipes/commit/a431e25b84e645ba48bbeae664ce5173d941acd0) — Give child jobs descriptive titles | Make delegated delivery, custom work, creation and package validation recognizable in job listings. | **Partial.** The receiver's title becomes child metadata. Missing titles still become “Complete the agreed owner request”; package probes use “Validate approved worker tools.” Title completeness is not required for advice. This is already [todo item 2](TODO.md). |
| [30b8b2b](https://github.com/colony-2/recipes/commit/30b8b2bae3ceca1798566f8656427cadf74f1ec4) — Recover reports after child submission | Correct an invalid agent report without forgetting jobs it already launched, duplicating submissions, or treating a diagnostic child failure as the end of all useful work. | **Gap.** [The agent wrapper](../../recipes/adaptive3/agent.yaml) exports response, session and artifacts, but not native child-job outputs. An invalid response becomes `stuck`. c2j retains the child in history, but adaptive3 does not automatically bring that identity into correction or wait on it. See finding 1. |
| [27bb83d](https://github.com/colony-2/recipes/commit/27bb83d2b856e5c043a5111ae1daed889dc81bb7) — Show expected and actual change size | Give humans a grounded size comparison, with exact candidate line counts, per-file categories and honest treatment of binary files. | **Gap, with changed requirements.** Adaptive3 asks for optional estimates/comparisons but provides no required measured report. The latest user decision replaces numerical estimates with a per-cell small/medium/large table and retains actual measured changes, including test frameworks as test code. That is [todo item 3](TODO.md), not implemented behavior. |
| [dc0d369](https://github.com/colony-2/recipes/commit/dc0d369e75a33c298997ce2145b813f996b38a06) — Encourage independent consultation judgment | Prevent agreeable but ungrounded delegation: inspect existing capability, challenge false premises, and request only work or explanation that advances a concrete outcome. | **Addressed at the prompt level.** Direction asks agents to inspect existing behavior; receiving-owner advice challenges unnecessary APIs and wrong assumptions; independent validation checks the recommendation. The [live storage trial](results/README.md) challenged a redundant restore endpoint. This is a useful example, not proof of general model quality. |
| [2fa3296](https://github.com/colony-2/recipes/commit/2fa3296836b2faf8aa1ff8ece7bb44ac1b15bda4) — Diagnose child startup and local submission | Teach agents to distinguish child startup failure from parent inspection failure, and use actual local recipes/workspace submission when unpublished Git revisions cannot be fetched. | **Partial.** [Standing context](../../recipes/adaptive3/prompts/context.yaml) retains submit-help discovery and local recipe/workspace options. It omits the more concrete instruction to inspect the child's own status and earliest failed tasks separately from the parent's read error. No equivalent startup-recovery test exists. |
| [e1bded0](https://github.com/colony-2/recipes/commit/e1bded080b6ecbca315b0b359dbbc505a4cb1fd4) — Let agents select current supporting evidence | Stop freezing every supporting file as part of an agreed handoff; preserve the receiver's assignment while allowing useful evidence to change and old material to be omitted. | **Replaced.** There is no internal handoff file or byte-comparison gate. The receiver's assignment is submitted directly, and agents own the selected review collection. A newly emitted collection must be complete; omitted files remain in their producing tasks. Link validation catches broken references, not every missing but relevant document. |
| [c7385f0](https://github.com/colony-2/recipes/commit/c7385f04b8d00592242fc71ad1e731955b3f8f69) — Focus one-pager questions on real choices | Replace filler Q&A with consequential decisions, alternatives, tradeoffs and unresolved choices, without an arbitrary question limit. | **Addressed at the prompt level.** [Direction instructions](../../recipes/adaptive3/prompts/execute.yaml) preserve consequential questions without a count cap and reject filler. The live one-pager trial supplies a concrete writing sample. |
| [d102ce6](https://github.com/colony-2/recipes/commit/d102ce6ce65ac9d2735f538c8816f696aa37f3ab) — Trust native const hooks | Remove cross-task hash guards that incorrectly treated normal floating-ref resolution as mutation; let c2j enforce const and hook-source permissions. | **Addressed.** [Hooks](../../recipes/adaptive3/hooks.yaml) use native const for configure, research, verify and publish; prepare is writable. Publication selects the merged workspace. No hook fingerprint/hash guard remains. `prepare-verify-publish-use-managed-workspace` covers the main path. |
| [834b088](https://github.com/colony-2/recipes/commit/834b088079bba0bd94b33549e65d9818e76604c2) — Explain restart discovery | Help agents discover restart points/context and the supported restart CLI rather than guessing recovery commands. | **Gap.** Adaptive3 explains task inspection and snapshots, but omits the `job --help`, `restart --help`, `restart-points` and `restart-context` discovery guidance. Same-job resolution reduces the need for restarts, but does not replace this knowledge for external recovery. |
| [a6874d9](https://github.com/colony-2/recipes/commit/a6874d96e51dd4b59b7a338c19def933934c81e4) — Keep annotations current | Prevent duplicate or stale document descriptions from accumulating and inflating chapter payloads; match metadata to the exact exported artifact. | **Replaced.** Adaptive3 has no accumulated annotation list. Forms receive the current artifact map and primary document directly. This removes the specific growth mechanism, not all possible chapter-size risk. |
| [e5f0af2](https://github.com/colony-2/recipes/commit/e5f0af208c9bf7dc91b53d537c2fe17f8836d944) — Recover child work across parent jobs | Let a replacement parent inspect and adopt an earlier parent's active/successful child, or replace a failed attempt while retaining useful approval and work. | **Partial.** Agents can inspect earlier attempts and snapshots. But consultation always submits a new job once delivery advice is accepted; it has no native adopt-existing-child branch, and does not pass `resume_from` to its delivery child. See findings 1 and 2. |
| [1006fc4](https://github.com/colony-2/recipes/commit/1006fc471e01d7d4d86c3c32356185304cfa026c) — Honor later human scope | Stop the initial request or old non-goals from overriding a human's explicit change; revise the one-pager and affected assignments before approval. | **Addressed.** Human wording/uploads reach correction; human changes start a fresh work session; scope changes return to Direction. `human-scope-change-returns-to-direction` and `attached-human-feedback-reaches-review-and-execute` exercise this. Subsequent factual alignment remains an agent responsibility. |
| [83c771b](https://github.com/colony-2/recipes/commit/83c771beec1aafce8b8c3a255c8a32dc8159ac73) — Recover approval from large histories | Read exact output instead of truncated previews, follow task pagination, and distinguish unreadable approval from no approval or an active source job. | **Gap.** There is no cross-job approval recovery operation. `resume_from` adds an instruction, then the new job enters ordinary Direction and human review. The shortened inspection prompt also omits pagination/exact-output guidance. See finding 2. |
| [75730dd](https://github.com/colony-2/recipes/commit/75730ddf6a32b8c7e5fd4b3d3170fa6e4c6c88ae) — Improve screenshots, recovery and limit decisions | Require usable UI evidence and linked attachments; recover approved work; make exhausted work discussable; reuse rebase approval through binary-capable tree comparison. | **Partial.** Link/image checks, visual-evidence instructions, resolver entry and tree-based approval comparison exist. Cross-job approval recovery is absent; screenshot applicability has no live delivery trial; repeated automatic failure handling is weaker. The former “stop attempt” failure outcome is intentionally replaced by resolution and native cancellation. |
| [1c7cdc7](https://github.com/colony-2/recipes/commit/1c7cdc7450347d49363076940faa002203482032) — Exclude human turns from budgets and recover accepted handoffs | Stop human discussion/revisions consuming an automatic work cap; avoid rejecting harmless copies of an already accepted assignment. | **Addressed in the new structure.** Human questions stay in Review; human changes reset the lifecycle allowance; default `max_iterations` is zero. No copied handoff file needs validation because delivery receives the receiver's assignment directly. Tests cover human reset, question-only review and receiver-authored submission. |
| [610a59b](https://github.com/colony-2/recipes/commit/610a59bba9eb707b96f84972b929958dff1c6dcb) — Introduce the human-readable adaptive2 flow | Frame work as feature, bug, explanation or oversight; add a one-pager direction checkpoint, separate implementation sessions, structured outcome review and receiver-authored consultation. | **Partial.** The four types, two human checkpoints and stage/session separation survive. The new live trials show clearer owner language. A consolidated consultation exchange and retained approved one-pager are no longer automatically presented in later reviews; agents must retain/retrieve useful material. Full human-inspection quality is not established. |

## Earlier shared-build changes inherited by adaptive2

These commits predate the adaptive2 directory. They are included because their
lessons matter to the replacement, not because they are adaptive2-only changes.

| Commit | Main purpose | Adaptive3 assessment |
| --- | --- | --- |
| [33f6474](https://github.com/colony-2/recipes/commit/33f6474224ab962518729c5f6feac8144ecdf6ea) — Allow corrected replacements after cancellation | Treat a corrective cancellation as feedback on an attempt while respecting instructions to stop the broader work. | **Partial.** [Resolver instructions](../../recipes/adaptive3/prompts/resolver.yaml) make this distinction and consultation retains terminal child results. The native cancellation test covers cancellation of the current job, not a cancelled child followed by a corrected replacement. There is no equivalent replacement-identity/re-entry test. |
| [da6148a](https://github.com/colony-2/recipes/commit/da6148a60596026ba2b86656fa87e738c8fc4b89) — Preserve merge approval across rebases | Avoid asking humans to reapprove the same edit; show a focused comparison and original approval when additional changes are needed. | **Partial.** Unchanged rebases reuse the native receipt after full validation; content, mode and binary changes trigger review. But the original approved review document is not bound alongside the approved patch. A focused follow-up depends on the agent retrieving it. See finding 2. |
| [91ac4e5](https://github.com/colony-2/recipes/commit/91ac4e5ef1701918aabd3226af2bd5719bdf40ff) — Bound fruitless recovery and scope evidence correctly | Stop endless unchanged failures; judge a child by its own assignment; accept useful investigation findings without demanding the parent's whole outcome; allow bounded local validation of unpublished work. | **Partial.** Current-scope and no-unrequested-deployment guidance survives. A failed resolver correction asks for human direction. Ordinary repeated `changes` can still loop with the default unlimited allowance, and detailed unpublished-local-build guidance is reduced. No equivalent repeated-negative-assessment test exists. |
| [de2e9cd](https://github.com/colony-2/recipes/commit/de2e9cdc3a113f3c811c3ca998815b0b45adf143) — Make job inspection usable | Explain discovery of task IDs, actual field pointers, exact downloads, final versus intermediate results, pagination and missing/denied evidence. | **Partial.** Basic log, fields, artifact and snapshot commands remain. Exact `--output` retrieval, pagination, attempts, final-result commands and pointer-type caveats are omitted. The example `/response/summary` is presented without the earlier warning that it may not exist. See finding 6. |
| [8cecc78](https://github.com/colony-2/recipes/commit/8cecc782390ecc15b98cbdee1e5e2673235ab2de) — Separate execution instructions and recover useful child work | Stop design instructions leaking into implementation; preserve writable execution; select useful old outputs; suspend rather than poll; process failed/completed children. | **Partial.** Stage-specific prompts and fresh stage sessions preserve the first two fixes; snapshots and native terminal waits preserve part of recovery. There is no combined collector for tool-submitted children or ready siblings. The model now waits on one consultation delivery at a time. |
| [a3fea1f](https://github.com/colony-2/recipes/commit/a3fea1fcfefb3b403dad1e9e20cf9ab48953411c) — Remove obsolete workflows and repair test coverage | Eliminate unused heavy/light/superpowers paths while retaining the creation helpers and meaningful native review tests. | **Replaced/retained cleanup.** Adaptive3 does not revive those workflows or the extra model review renderer. Creation remains a separate existing workflow. The public-default tests target adaptive3; retained adaptive2 tests now target its explicit entrypoint. |
| [5c6a6fb](https://github.com/colony-2/recipes/commit/5c6a6fbb3d3c40c83ebc03574f7591b4d92ed5ff) — Put child recovery with the parent | Observe the actual attempt even while its goal remains open; return useful failures/results to the parent and let it correct the assignment. | **Partial.** Native terminal job waits and same-job resolution preserve the main intent for recipe-submitted delivery. The parent cannot help a still-open child in its resolver, and direct child submissions are not collected. See finding 1 and the [runtime requirements](RUNTIME_REQUIREMENTS.md). |
| [538ff7c](https://github.com/colony-2/recipes/commit/538ff7cf6394b4fd6610d7dbd16d31a6c69c0301) — Preserve complete failure evidence | Walk wrapped failures; retain same-named logs under distinct paths; keep verification files separate from human documents. | **Gap.** Adaptive3 reads only top-level command/extension diagnostics and flattens each to its basename. Nested causes and same-named files can be lost. Hook evidence is merged into the review inbox without an isolated namespace. The existing native-log test exercises a simple failure, not these cases. See finding 3. |
| [8930386](https://github.com/colony-2/recipes/commit/8930386f80b360c2470808805c638041ec43d335) — Keep nested advice inline and preserve evidence | Avoid spawning jobs just to consult another owner; restore the requesting workspace/session and keep check outputs from replacing reviewed documents. | **Partial.** Inline and nested receiver workspaces are tested. Delivery alone starts a child. The evidence-isolation part is weaker: hook output can win a same-key merge with selected review documents. Arbitrary custom consultation selectors are no longer an input; dedicated delivery selectors remain supported. |
| [b687a62](https://github.com/colony-2/recipes/commit/b687a6227729063288f4158046b4d868d561dc3b) — Preserve credentials under permission restrictions | Avoid replacing the full permission policy when only changing submission or creation permission, which had removed Git credentials. | **Addressed structurally.** Adaptive3's agent wrapper does not replace the task's permission policy. Existing cell registration retains its inherited policy and explicit create grant. This removes that recipe mistake; it does not prove every deployment's credential configuration. |
| [562ff6a](https://github.com/colony-2/recipes/commit/562ff6afbb92c1727a9bd4606416c30b2948cd2e) — Simplify coordination, reviews and environment requests | Accept useful titles; explain job context; let agents route human changes; select artifacts; add policy-approved package probes and recover failed dependency work. | **Partial.** Titles, context, review interpretation, selected documents and package approval/probe/adoption are present and tested. The old goal-only wait was deliberately superseded by job waits. Direct child accounting and several recovery safeguards from this larger change are missing; no need to restore its key maps or stop-attempt machinery. |
| [531599a](https://github.com/colony-2/recipes/commit/531599adc1e95134ed6a552d0b2a96dfd3f84d25) — Avoid parsing truncated repository context | Stop treating a bounded stdout preview as complete JSON during design classification. | **Replaced.** Agents inspect the repository directly; there is no repository-context JSON builder/Jev classifier. The embedded validators return small structured summaries and retain detailed diagnostics in files. `large-diagnostics` covers 2,000 reported file issues. |
| [d667c8a](https://github.com/colony-2/recipes/commit/d667c8a9a0cdf53d205cd69e9db0cd5681428b04) — Use cell names and explicit creation authority | Stop passing repository URLs as cell identities; register cells in root with the explicit create permission while preserving Git push/catalog updates. | **Addressed in source.** Consultation selects a named cell; owner work inherits its managed workspace. Root can choose the existing `create.yaml`, which still owns registration, initialization and catalog changes. Dedicated workflow selection is tested; complete adaptive3→root→new-cell publication is not. |
| [7a0e7c0](https://github.com/colony-2/recipes/commit/7a0e7c093532c3c92b65e956ac6932dc79bae591) — Adopt schema v2 objects | Replace JSON-string transport and misnamed structured types with native objects, arrays, artifacts and checkpoints. | **Addressed.** Public build/adaptive3 contracts use schema v2. Private includes pass native values; the agent response boundary removes unused nullable fields once. Current native tests and live calls exercise the contract. |
| [0e04887](https://github.com/colony-2/recipes/commit/0e04887230fb2c879fda1a50fcddedfe718dd0ff) — Simplify templates and artifact handling | Remove positional `printf` prompt formatting and opaque JSON plumbing; use named template inputs and runtime-owned artifact identity. | **Addressed.** Separate [prompt includes](../../recipes/adaptive3/prompts/) use named inputs and ordinary templates. No annotation pipeline or `data_json` transport remains. `literal-request-text` checks that user text is not reinterpreted as a template. |
| [777a2b6](https://github.com/colony-2/recipes/commit/777a2b6bedaafd409eb9fcd199053852f829146d) — Share prompt text without fake tasks | Externalize prompts into an empty-sequence include while keeping operational decisions in the consuming recipe. | **Addressed.** Adaptive3 keeps this pattern, split by activity. Prompt includes create no worker operations. Some short fallback/status text remains in orchestration YAML. |
| [23d376c](https://github.com/colony-2/recipes/commit/23d376cc0ed4a6d0d311d4da93f50e6b3ef5cbeb) — Read native recipe state directly | Replace a compound `flow` bundle and derived state files with specific inputs and native operation/history outputs. | **Addressed.** Stages read native outputs; helpers pass their current documents, settings, session and feedback. There is no mirrored coordinator ledger or workflow-state file. Some structured feedback is still necessary to convey a current result, but it is not a reconstruction of all workflow state. |
| [04d3120](https://github.com/colony-2/recipes/commit/04d31209cc4ff25a08f6ac069271aeb3f35f608f) — Give agents clean context and native diagnostics | Insert standing instructions only on new sessions, explain `c2j self`, use standard error/feedback locations, and consume automatically recorded child outputs. | **Partial.** New/resumed session handling and directory-level context survive. Direct child outputs are not exported by the wrapper, and diagnostic forwarding is incomplete. See findings 1 and 3. |
| [53a44f1](https://github.com/colony-2/recipes/commit/53a44f1b5dfca22062fc197269038196ef47c63d) — Keep verification logs and remove review self-links | Return actual failed-command evidence to correction and avoid generated annotations linking a document to itself. | **Partial.** Simple native failure evidence reaches correction; the annotation self-link generator is gone. Wrapped/colliding logs and several failed-hook paths lack equivalent coverage and forwarding. |
| [65c1861](https://github.com/colony-2/recipes/commit/65c18618cc708707553ce9b0605ec69888b01b53) — Simplify hooks and remove kernel dependence | Use native hook contracts and typed settings without duplicated provenance machinery; keep the adaptive flow independent of creation's kernel. | **Addressed for the architecture.** [Hooks](../../recipes/adaptive3/hooks.yaml) use native includes and declared outputs. `build-settings.json` exists only at the existing hook adapter boundary. Adaptive3 does not include the creation kernel. Specific hook-setting omissions are recorded against the original hook commit below. |
| [d89a87e](https://github.com/colony-2/recipes/commit/d89a87e9c6b3e320b56f388d905afaed71f96327) — Introduce one adaptive build flow | Replace heavy/light routing with a shared process covering planning, verification, consultation, human acceptance and Git integration. | **Replaced.** Five explicit stages use one activity lifecycle. Direction is now a required human checkpoint for delivery; correction repeats the complete destination cycle. `public-feature-native-merge` and `correction-repeats-every-check` cover the replacement. |
| [f22ac49](https://github.com/colony-2/recipes/commit/f22ac49908b1aa6db939982340f6798dd9649c4c) — Propagate publication failures and bound merge recovery | Stop failed publication being treated as success; retain completed effects and avoid an endless rebase chase. | **Partial.** Failed publication reaches resolution and a completed merge survives retry; native tests cover both. However, repeated stale merges re-enter stages with a fresh lifecycle counter, so a positive per-stage allowance does not bound the whole chase. Creation's separate publication path remains unchanged. See finding 5. |
| [84a8898](https://github.com/colony-2/recipes/commit/84a889884fcf78f44de9ab80dcfb99ddf5329d5e) — Make review presentation follow actual artifacts | Tie descriptions and supporting evidence to producer identity; provide a clear primary brief and preserve the evidence behind it. | **Replaced, with limits.** Native references and a selected primary review document replace the annotation/synthesis pipeline; link/image validation checks the published collection. There is no automatic source-lineage overview, and earlier approved documents are not automatically attached to follow-up review. |
| [5761b14](https://github.com/colony-2/recipes/commit/5761b144d34f8f1d4786bdebd303efd6577dfc91) — Repair incomplete output and review root creation | Return bad reports for correction and require approval of new-cell identity, initial purpose and root configuration before publication. | **Partial.** Required review files return through the full cycle; invalid agent responses enter the resolver. Missing advice titles still use filler. Existing root creation keeps its reviewed publication boundaries, but complete creation through adaptive3 has not been exercised end to end. |
| [6eb7dcf](https://github.com/colony-2/recipes/commit/6eb7dcfeeb84b8f96d35accc2a586c13b3df756e) — Add repository hooks and specialist checkpoints | Let repositories configure behavior and require specialist reviews at research, planning and outcome checkpoints. | **Partial.** All five hooks and three specialist checkpoints are called. Required planning/implementation specialists gate validation. A required `before_design` rejection is only summarized to the working agent; `plan_assessment` prompt additions are not consumed by the assessment. There is no negative configured-specialist test. See finding 4. |

## Findings that affect confidence in adaptive3

### 1. Child recovery is less complete than the general resolver story suggests

There are two different cases.

For a delivery child submitted by
[consultation.yaml](../../recipes/adaptive3/consultation.yaml), adaptive3 waits for
its terminal result. A failure returns `stuck`, including the child result, to
the parent resolver. This is present and tested.

For a child submitted through an agent's tools,
[agent.yaml](../../recipes/adaptive3/agent.yaml) exports no native child inventory.
If the agent then returns invalid output, the wrapper retains its session and
artifacts but supplies only a generic `stuck` response. The child is discoverable
in c2j history, but is not automatically presented as existing work during repair.
There is no test for “submit a real child, return an invalid report, correct the
report without submitting again.” That was the central lesson of `30b8b2b`.

Likewise, a recovered parent can inspect an earlier successful replacement, but
its consultation submission path does not adopt that job. It always submits a new
one after delivery advice. The resolver can guide an agent to use existing work;
this is not equivalent to the earlier tested adoption behavior.

A still-open child is a separate limitation. The parent waits for terminal status
and cannot react through this path while the child is asking its own human/resolver
for help. This is already recorded as a
[c2j runtime requirement](RUNTIME_REQUIREMENTS.md#2-allow-a-parent-to-help-a-still-open-child),
not something proven fixed by same-job resolution.

### 2. Prior approval survives a rebase, but not a new job in the same way

Within one job, the approved patch and native receipt survive a stale merge. The
whole-tree comparison handles content, file modes and binary data. Fresh
validation still happens. These are strong, relevant tests.

Across jobs, `resume_from` in [adaptive3.yaml](../../adaptive3.yaml) is only text
in the assignment. There is no operation to discover, validate and recover the
old direction approval. The new job enters Direction and requests human acceptance
again. That is a behavioral regression relative to `83c771b`, `e5f0af2` and
`75730dd`, even though an agent may recover useful implementation files.

For a changed candidate within the same job, the saved approval carries its
receipt and patch, not the original approved review document. The outcome prompt
asks for differences and a reference to the earlier approval, but does not
explicitly provide that document. The tests establish when a review happens;
they do not establish that the reviewer receives the intended focused comparison.

### 3. Several diagnostic and evidence protections were dropped

The catches in [hooks.yaml](../../recipes/adaptive3/hooks.yaml) and
[cycle.yaml](../../recipes/adaptive3/cycle.yaml) read diagnostics only from the
current failure's `attrs.command` and `attrs.extension`. They rename each entry
to `error/<basename>`. Two different `check.log` paths can therefore become the
same entry. A diagnostic carried only by a nested cause is not selected.

There are also forwarding differences. A failed before-design or prepare hook
becomes `response.failure`; a failed publish is in `response.publish`. Their
artifact references remain inside those native results, but are not explicitly
bound as `problem.errors` for the resolver's next inbox. Verification has a
separate forwarding path and is better covered.

Finally, validation merges hook artifacts after selected documents. A hook can
supply the same key as a human-facing document and replace that inbox binding.
The previous implementation isolated verification files precisely to prevent
this. These observations follow directly from the source; the existing simple
native-error test does not cover them. The original task records remain available
for inspection, so “not forwarded” does not mean “deleted from JobDB.”

### 4. Repository customization is only partly preserved

[execute.yaml](../../recipes/adaptive3/execute.yaml) always goes from the
before-design specialist result to work. A required specialist's `changes`
status is not a condition on that transition or on later Direction validation.
Its summary is shown to the agent, which may address it, but the required
checkpoint is no longer enforced as it was in the old contract.

Planning and implementation specialists do contribute to the final validation
result. This is a specific pre-design gap, not a claim that all specialists are
ignored.

The configure schema still accepts `prompt_additions.plan_assessment`, but the
validation/independent-review prompts do not consume it. `outcome_assessment`
text is given to the outcome writer; it is not included in the independent
assessment. Hooks can therefore appear configured while part of their intended
guidance is unused. Existing adaptive3 tests exercise ordinary hooks, not these
negative/customized assessment cases.

### 5. Remaining automatic loops are not all covered by resolution limits

Human questions correctly stay in Review and do not spend automatic work turns.
Explicit human changes reset the allowance. A failed automatic resolver correction
requires human direction before another resolver attempt.

However, the default allowance is unlimited. An agent that keeps returning
`changes` can continue around the ordinary lifecycle without ever reporting
`stuck`. The old repeated-unchanged-negative-assessment protection is gone.

Repeated stale merges are another case: Integration returns to Implementation,
and each stage entry initializes a new lifecycle counter. Even a positive
`max_iterations` does not account for the whole merge chase. Tests cover one
stale merge, not repeated upstream advancement. Keeping jobs recoverable is
intentional; it does not by itself ensure that repeated ineffective work reaches
a human or resolver.

### 6. The inspection instructions lost useful operational detail

The new context is shorter, which helps readability. It also drops answers to
questions that repeatedly blocked agents:

- How to discover an actual field pointer rather than assume `/response/summary`.
- How to download full values with `--output` instead of parsing a preview.
- How to follow pagination or select an attempt.
- How final result artifacts differ from a task's intermediate artifacts.
- How to discover restart points and restart context.

The repository still has [JOB_INSPECTION_PLAYBOOK.md](../JOB_INSPECTION_PLAYBOOK.md),
but the standing agent context does not point to it. In other cells, that local
recipes-repository path is not necessarily available. The presence of the guide
here is therefore not evidence that a worker received it.

### 7. Human-facing completeness has known gaps

The three [agreed todo items](TODO.md) remain outstanding. Of those, descriptive
child titles and qualitative/actual change reports directly overlap this history.
The model override item is additional work, not a fix already supplied by adaptive3.

Ordinary human review keeps a resumed answering session. Resolver discussion does
not: each answer starts fresh and receives the current question, original problem
and documents. Prior questions/answers and the last proposed correction are not
explicitly passed into that next answer. They remain inspectable through job
history, but repeated coherent discussion is not established by the single-question
test.

Consultation is now recorded in native tasks rather than assembled into a
conversation document. That avoids internal document management, but it also
means the parent must make consequential owner advice visible in its own review.
The live owner trial shows useful disagreement. There is no end-to-end test or
live example showing a human easily following several owners' exchanges and the
final decision from one review.

### 8. Artifact growth is reduced, not proven impossible

Adaptive3 removes the previous cumulative annotation and conversation-state
payloads. It uses one current review collection, stores large output in files,
and gives its few validators small stdout summaries. Those are substantive
improvements.

There are still two important boundaries:

- Returning any new `review/` files replaces the whole current collection. Agents
  must include every still-needed file. Link checks catch omitted link targets;
  they do not detect every useful unlinked item that was accidentally omitted.
- Consultation receives the current collection and returns native child results
  through feedback. There is no large nested-child-result or long multi-stage
  chapter-size regression test. The 2,000-file validator test establishes bounded
  validator stdout, not bounded end chapters for a real long job.

Screenshots illustrate the difference. Missing links and corrupt image files are
mechanically rejected. Whether a UI change needs screenshots, and whether an image
shows the correct state, is assessed by an agent. That guidance exists, but the
available results do not include a live UI implementation/review proving it works.

## Overall assessment

The central abstraction is retained: agents do the work and judgment; native
operations carry out publication, waits and human decisions. Many historical
fixes needed only because of the old document/state machinery no longer apply.

The audit does **not** support calling adaptive3 fully equivalent to the mature
adaptive2 behavior. In particular, a general resolver is not a substitute for
presenting the correct child identity, actual failure files, earlier approval or
configured review requirement. Those are specific missing inputs or transitions,
not evidence that agents need another elaborate coordination protocol.

The findings above are left for review and prioritization. This audit makes no
additional recipe changes.

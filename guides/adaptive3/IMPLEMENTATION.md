# Adaptive3 implementation and assessment

Adaptive3 is implemented separately and is now the default behind
[`build.yaml`](../../build.yaml). [`adaptive3.yaml`](../../adaptive3.yaml) remains
its direct entrypoint. See the [rollout notes](ROLLOUT.md).
This work fits the recipes cell; c2j remains responsible for durable execution,
permissions, workspaces and runtime recovery.

The main change is one shared **Execute → full Validate → Review** cycle across
Direction, Preparation, Implementation, Outcome acceptance and Integration.
Corrections repeat the destination stage's complete cycle. Human questions stay
in the pending review. Acceptance advances directly.

Read the [actual trial documents](results/README.md) to assess the writing, and
[test results](TEST_RESULTS.md) for the evidence and its limits. The
[design](DESIGN.md) records the intended structure.

The [follow-up list](TODO.md) records human-directed model overrides, incomplete
result correction, qualitative scope by cell and measured code-change reports.

## Delivered against the plan

| Plan | Implementation |
| --- | --- |
| Separate adaptive3 | New public entrypoint, helpers, prompts and tests. Existing adaptive2 recipe sources remain separate; the public build now forwards to adaptive3. |
| Define the activities once | `execute.yaml`, `validate.yaml` and `review.yaml` own the activities. `cycle.yaml` composes one pass; `lifecycle.yaml` handles corrections and service interruptions. |
| Five visible stages | Named states in the public entrypoint. Direction and Outcome require human acceptance; other stages use independent agent assessment. An accepted explanation finishes at Direction. |
| Human-readable work | Four work types; the existing one-pager and outcome headings; descriptive titles; consequential Q&A without a question-count cap; change-size estimates and actuals as useful review information. |
| Dialogue separate from changes | A read-only review session answers questions. Change requests carry the original human words and current uploaded notes into Execute. Scope changes return to Direction. Human turns do not consume automatic attempts. |
| Agents own their work products | The producer selects the current `review/` collection. Validation and native human input use those artifact identities. Replacing the collection does not overlay historical files. |
| Consultation and delivery | Inline advice runs in the receiving workspace, including nested advice. The receiver writes the assignment and may select an existing delivery workflow. Native child submission and waiting retain actual outcomes and partial-result references. |
| Same-job resolution | Caught failures and automatic allowance exhaustion return `stuck`. The resolver proposes a correction for the same or an earlier stage. If that correction gets stuck too, human direction is required before another attempt. Discussion alone does not grant that attempt. |
| Preserve local customization | Existing configure, before-design, prepare, verify and publish hook API and paths. Required verification cannot be waived by the assessing agent. Configured specialists use the shared Validate activity. |
| Package requests | Agent request → policy or human approval → fresh probe job → adoption of the tested config. A validator rejects unrelated configuration changes and checks actual adoption. |
| Native Git and approval reuse | Native rebase, squash and merge. Stale merge returns through Implementation and Outcome. A validator compares the whole resulting tree, including modes and binary content, to reuse approval for unchanged work. Publication recovery preserves a completed merge. |
| Keep prompts separate | Empty-sequence prompt includes with named templates. Standing instructions are inserted when a session starts; resumed sessions receive current task text. |
| Embed the few scripts | `tools.yaml` contains exactly three output validators. Workers do not need separately resolved Python source files. |

## Where to read the code

| Files | Responsibility |
| --- | --- |
| `adaptive3.yaml` | Stage order, returns to earlier stages, resolver entry and concise final outputs. |
| `lifecycle.yaml`, `cycle.yaml` | Corrections, human/automatic attempt accounting, and the common activity pass. |
| `execute.yaml`, `validate.yaml`, `review.yaml` | Work, full checks and human/agent review. |
| `consultation.yaml`, `resolver.yaml` | Owner dialogue, delegated delivery and recovery in this job. |
| `packages.yaml`, `package-probe.yaml` | Approval, fresh-environment testing and configuration adoption. |
| `agent.yaml` | Native c2ops invocation, session boundaries and read-only/writable tasks. |
| `hooks.yaml`, `specialists.yaml`, `integration.yaml` | Existing customization points and native Git operations. |
| `tools.yaml` | Review files/links/images; equivalence to an approved edit; approved package configuration. |
| `schemas.yaml`, `prompts/` | Small response shapes and human language for each activity. |

All helper paths above are under [`recipes/adaptive3/`](../../recipes/adaptive3/).
The widest input contracts have eight properties. There are no per-stage wrapper
recipes. Git state, review receipts, sessions, child results and artifact identity
remain native runtime values.

Diagnostics reach the next correction as selected files under `inbox/work/error/`.
Human uploads use `inbox/work/feedback/`. Review documents use `inbox/work/review/`.
Older material is available through the job inspection commands explained in the
standing context and the [inspection playbook](../JOB_INSPECTION_PLAYBOOK.md).

## Adjustments made while implementing

**One pass and its loop are separate includes.** Consultation needs the same
Execute/Validate/Review pass. Separating `cycle.yaml` from `lifecycle.yaml` avoids
recursive static includes while retaining a single definition of each activity.
Nested consultations keep only the cell, request, current documents and mode
needed to return to their caller.

**Configured specialists share Validate.** The fixed mapping in `validate.yaml`
runs `before_design` assessments on Direction, `plan_assessment` on Preparation,
and `outcome_assessment` on Implementation. Outcome assesses the human report
without duplicating specialist calls. Research hooks still inform Execute.
General and specialist assessors receive the configured assessment guidance and
current human scope. All required findings return together through the ordinary
full correction cycle; optional advice has no independent veto.

**Provider schemas need nullable fields.** The agent provider requires declared
properties to be required. Each activity uses its own small schema with nullable
branch fields; `agent.yaml` drops unused top-level nulls once. Native live calls
validated these schemas without output-repair attempts. The recipe does not ask
agents to write a compound workflow-state response.

**Public contracts use schema v2; private helpers use native values.** The public
entrypoint, probe and schema exports are typed. Internal includes pass native
receipts, checkpoints and failures without duplicating every runtime structure
as another schema. This follows the repository's existing include pattern.

**Fresh inline consultation is initiated from Execute.** During review, the agent
can inspect previous owner replies and use tools for a small clarification check.
A fresh owner negotiation returns through Execute and the full cycle. The broader
design idea of suspending a review into inline consultation is not a separate
implemented transition; doing so would reintroduce recursive recipe includes.

**Tests are grouped by actual boundaries.** Public stage, hook and recovery cases
live in `build.test.yaml`; review/artifact cases live in the cycle and lifecycle
suites. There is no need for a separate file for every planned test-suite name.

## Problems the tests caught and fixed

- Native artifact binding uses the descriptor's name as well as its map key.
  Correcting both made approval patches and human feedback available at their
  intended paths without changing stored artifact identity.
- Forwarding every validator artifact also forwarded workspace restore artifacts.
  Validators now export only their selected diagnostic files and candidate patch.
- Nested sequence inputs must explicitly expose the native merge message.
  The full-entrypoint merge test caught the missing scope import.
- A failed publish must retain the successful merge when resolution resumes.
  The publication recovery test verifies one merge and a later publish attempt.
- Native review forms need `kind: review` for the expected receipt lifecycle.
  Resolver discussion and repeated-resolution tests exercise actual input forms.
- Empty or invalid agent responses need to become `stuck`, not ordinary success.
  Required verification failures likewise cannot be converted to success by a model.
- Human attachments need an explicit upload field and must reach both the answering
  agent and the next Execute. The test uses an actual file and checks original content.
- An empty-message Continue must retain the resolver's proposed correction and
  chosen earlier stage. A native input test also preserves uploaded direction.

A separate native cancellation test confirms that a human stop does not become
an automatic resolver attempt and that previously recorded work remains intact.

The earlier conditional-sequence failure was a c2j bug. Latest main
`c244db82949ea989cd90d4352325b40b88cca5d0` passed the focused `when` probes and is now
the repository's `.c2j-version` pin. Adaptive3 uses explicit lifecycle transitions;
the recipe does not patch the runtime.

## Limits before wider use

The deterministic behavior is tested, and real agents produced the linked review
examples. This is ready for further opt-in evaluation, subject to these limits:

1. **The unmodified Nix dependency path still needs a normal-worker run.** This
   environment could not activate the validator dependencies through c2j's Nix
   derivation parser. Native execution tests used preinstalled tools in disposable
   recipe copies. Production dependency declarations remain intact. See the
   [test environment details](TEST_RESULTS.md).
2. **Universal same-job resilience needs runtime support.** The recipe handles
   tested ordinary failures. Authoring/template failures, an unavailable worker,
   and a still-open child's request for parent help need runtime-owned behavior.
   [Runtime requirements](RUNTIME_REQUIREMENTS.md) defines the remaining boundary.
3. **Remote children need published sources.** Delivery and package probes select
   adaptive3 files from recipes `main`. Publish these files before trying remote
   delegated delivery. Local test children use captured local fixtures instead.
4. **Live evaluation is still narrow.** The one-pager/dialogue trial and a completed owner consultation passed. A real
   receiver challenged the API request; an earlier attempt hit model capacity.
   There is not yet a live UI screenshot trial or a full live delivery/merge trial.
   The deterministic image checks prove usable attachments, not their relevance.

Memory, Docker and other broader environment requirements are outside the package
service delivered here. Their provisioning and durable suspension belong to c2j
and the environment owner. The default now uses adaptive3 following the requested switch; these runtime
requirements and follow-up trials remain open.

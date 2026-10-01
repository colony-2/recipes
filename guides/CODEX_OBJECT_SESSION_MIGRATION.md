# Recipe migration to Codex object sessions

Codex and `codex/run_skill` selectors are pinned to c2ops
`ded76dfbd877d3d0749e509844ecdbc57197b572` (the latest `main` verified on
2026-09-30). Both use `c2ops.codex.session/v1`.

Workers and recipe authoring tools require c2j immutable-object support, introduced
in `e1334817a353d4868a97fa5452fe8fe3aee2fc13`. Validation here uses a clean build
of c2j `9f6d147`, which includes that support. The adapter requires Codex CLI
**0.157.1**, including inside the sandbox, and Go 1.26 or later for Go-backed ops.
Updating a submitting CLI alone does not update remote workers.

## Routing

Start a conversation by omitting `session`. Continue by forwarding the exact
complete object from the selected predecessor:

```yaml
- id: start
  op: git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572
  inputs:
    prompt: Investigate the requested behavior.
- id: continue
  op: git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572
  inputs:
    prompt: Implement the agreed change.
    session: '${{ sequence.start.outputs.session }}'
```

A recipe accepting a submitted session declares `type: object` with
`object_type: c2ops.codex.session/v1`. Shared phases normalize an omitted input
to null only within their orchestration scope. Explicit fresh/resume branches
omit the key from fresh op/include inputs; **no Codex op receives `session: null`**.
The same branching also preserves typed optional inputs across included recipes.

The shared agent, human revision loop, dependency recovery, and foreign-cell
consultation route the latest successful object explicitly. Build/evolve export
`session` at the root for later jobs. Their `session_id` outputs remain diagnostics.
Superpowers exports object references alongside its diagnostic role IDs.
Skill-enforcing calls use `codex/run_skill`; plain `codex` accepts skill sources
but no longer accepts the old top-level skill-selection inputs.

Consultations retain the latest object and reply for each destination cell.
The runtime story preserves earlier executions; recipes do not reconstruct a
transcript or pin a custom commit ledger. Matching diagnostic IDs do not permit
merging divergent checkpoints.
The ordinary evidence and user-deliverable artifact contracts remain separate.

## Upgrade boundary

This is the upstream's hard breaking migration. Neither `sessionId` nor
`resume_context` is a valid op input, even when empty. Remove all
`codex-home-state` bindings and overrides of `CODEX_HOME`, `CODEX_SQLITE_HOME`, or
`C2J_OBJECT_OUTBOX` from recipe env. The runtime supplies the object outbox.

Existing legacy checkpoints cannot be imported. Finish old jobs with their old
recipe/runtime or start a fresh job on this version with an appropriate task
summary. There is no automatic fallback that discards conversation history.
Existing serialized consultation ledgers containing only legacy IDs/artifact
bundles likewise require a fresh job.

Object references can cross jobs within one tenant, but forwarding does not pin
retention. Keep their originating job/task artifacts for as long as continuation
is required. Agent state does not carry repository edits: c2j Git snapshots and
node workspaces still determine the code seen by each invocation.

## Validation

Run `c2j test run --directory recipe-tests --case-timeout 5m`. Native declarations
publish real session objects and verify which checkpoint each recipe forwards;
Git state, child work, reviews, and merges run through c2j's normal workers.

Generic object replay, immutable branches, private state visibility and invalid
references are tested in c2j. The Codex adapter's private homes, rollout/database
format, failure cleanup and skill continuation are tested in c2ops. See the
[coverage map](NATIVE_TEST_MIGRATION.md) for exact destinations and verified tests.
The recipe repository no longer emulates the Codex CLI or starts a separate JobDB.

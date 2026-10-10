# Recipe migration to Codex object sessions

Codex and `codex/run_skill` now use the published c2ops packages
`nix:github:colony-2/c2ops/main#codex` and
`nix:github:colony-2/c2ops/main#skill-run`. Both retain `c2ops.codex.session/v1`.
The Nix migration does not change the session handoff contract below.

Workers and authoring tools need packaged-op support from current c2j `main`
(migration build: `82362f0ec1ad68b79ed2fb078ca9418e722de0cd`). Configure Nix and
the trusted `colony2` Cachix cache. The packages contain compiled op executables;
their manifests declare Codex CLI **0.157.1** through pnpm. A Go toolchain is
needed to build c2j from source, not to execute these prebuilt ops.
Updating a submitting CLI alone does not update remote workers.

## Routing

Start a conversation by omitting `session`. Continue by forwarding the exact
complete object from the selected predecessor:

```yaml
- id: start
  op: nix:github:colony-2/c2ops/main#codex
  inputs:
    prompt: Investigate the requested behavior.
- id: continue
  op: nix:github:colony-2/c2ops/main#codex
  inputs:
    prompt: Implement the agreed change.
    session: '${{ sequence.start.outputs.session }}'
```

A recipe accepting a submitted session declares `type: object` with
`object_type: c2ops.codex.session/v1`. The shared agent loop normalizes an omitted input
to null only within their orchestration scope. Explicit fresh/resume branches
omit the key from fresh op/include inputs; **no Codex op receives `session: null`**.
Only the implementation and consultation entrypoints branch at an include boundary;
there are no intervening phase recipes repeating that choice. The Codex calls
select fresh/resumed and root/scoped inputs in one set of sibling states.

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

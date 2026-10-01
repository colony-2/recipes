# Build/evolve logic remaining after simplification

The recipes now use direct prompt context, native child-job discovery and awaits,
artifact bindings, and separate Codex session objects. They no longer record or
merge consultation transcripts, prepare context files, or enforce changed-file
write scopes. The coordinator passes one current consultation map between phases.

Five embedded Python blocks remain for a separate policy review:

| Location | What remains | Question for the next review |
|---|---|---|
| `recipes/develop/mandate.yaml` | Read the committed mandate, validate its format, and report clause IDs and provenance. | Which format checks belong in authoring validation instead of every run? |
| `recipes/develop/design.yaml` | Validate ownership and requirement links, route a consultation, validate agreed handoffs, and publish review documents. | Which policies need deterministic enforcement beyond the schema and design review? |
| `recipes/develop/implement.yaml` | Route a consultation, compare proposed handoffs with approved work, and require redesign for new external changes. | Can consultation routing become shared recipe expressions while retaining the approval rule? |
| `recipes/develop/test-plan.yaml` | Validate statement length, IDs, requirement coverage, negative cases, and command mappings; render Markdown. | Which constraints belong in the schema, and which require a cross-document check? |
| `recipes/develop/verify.yaml` | Run approved commands with deadlines, capture evidence, map results to statements, and check candidate stability. | Is an existing verification operation a better home for this execution contract? |

Two small shell operations remain: `cat` exposes a schema-checked result artifact
as structured recipe data through `json_parse`; `snapshot.yaml` creates the target
directory when requested and reports Git HEAD/cleanliness. The latter preserves
initial-mandate provenance and prevents merging a candidate that changed after
verification. Neither implements a write-scope policy.

The current plain Codex op does not export arbitrary parsed phase output.
`codex/run_skill` does, but switching these generic phases into skills would be a
separate design choice. No new artifact retrieval or child-job operation is needed
for this workflow.

# Why some recipe inputs still use JSON strings

c2j's public recipe input schema accepts scalars, artifacts, artifact maps, and
object checkpoints. Its `object` type means a checkpoint such as an agent
session—not an ordinary JSON object. Plain maps and lists are not supported.

Consequently, values such as annotation lists and saved coordination records
cross some job/test boundaries as strings (`annotations_json`, `threads_json`).
Recipes decode them once and use structured values internally. This limitation
does not require dumping JSON into agent prompts or wrapping all workflow state
in one object; those unnecessary envelopes have been removed from the adaptive
fixtures.

**Needed change, owned by c2j:** support ordinary map/list inputs with validation,
defaults, and reliable preservation through submission, persistence, and child
jobs. Keep checkpoint and artifact types distinct. Recipes could then accept
`annotations: [...]` directly and remove the corresponding stringify/parse calls.

This is an input-schema limitation, separate from jq transformations that rename
artifact bindings or validate annotation identity. Adding structured input types
would remove the transport workaround, not those transformations.

Verified against c2j commit `f1a153b898c57e93e9b01477d08cc02c1509ee4b`,
`pkg/recipe/recipe.go` (`InputSchema.validate`). See the
[recipe cleanup notes](IMPLEMENTATION_RECIPE_READABILITY.md) for examples and
validation results.

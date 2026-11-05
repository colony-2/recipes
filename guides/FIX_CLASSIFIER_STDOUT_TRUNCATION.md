# Classifier stdout truncation

Job `1fa7464c-774d-4061-8da1-04d77f91d637` failed before implementation because
`read_repository_context` emitted repository documentation as JSON on stdout.
c2j shortened that output to its diagnostic preview and appended a truncation
notice. Parsing the resulting preview failed when resolving `context_usable`.

The collector now retains its bounded context in `repository-context.json` and
limits the serialized inline JSON to 8,000 bytes, below the roughly 10 KB preview
ceiling. JSON escaping counts toward that limit. If context exceeds the budget,
stdout contains a small valid payload with `usable: false`; the original collected
context remains in the artifact. Each source file still has the existing 64 KiB
read bound, and partial or unreadable context remains unusable for skipping design.

Jev currently accepts inline state, not a context artifact. This fix therefore
requires design for larger contexts rather than attempting classification on a
truncated excerpt. The design agent reads the repository normally. Supporting
large context directly in Jev would require a separate artifact/file input contract.

The final routing expressions tolerate malformed JSON and honor
`stdout_truncated`. Such input cannot authorize skipping design, even if the model
returns a low complexity score. Small, complete context retains its prior routing.

Nine targeted regression cases passed using native command execution and artifact
handling, with model responses mocked. The tests cover small context, a 20 KB
README with its ending preserved in the artifact, escaped Unicode, combined
source sizes, the file-size bound, unreadable/missing documents, malformed JSON,
and explicit stdout truncation.

All 36 existing build-flow regression cases also passed.

Validation used an isolated recipe copy with Nix package provisioning omitted and
selectors expanded to extension operations. The source run could not provision
packages because this machine has no `/nix`; no live Jev calls were made.

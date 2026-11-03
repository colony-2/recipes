# Execution diagnostics in recipes

Runtime baseline: c2j `f1a153b898c5` or newer. See the
[upstream contract](https://github.com/colony-2/c2j/blob/main/GUIDE-Command-Failure-Diagnostics.md)
for capture limits and execution semantics.

New command and extension failures provide version-2 diagnostic references under
`failure.attrs.command.diagnostics` or `failure.attrs.extension.diagnostics`.
Bind `_c2j/execution/<node-id>.log` into the next agent's `error/` directory.
The log supplies portable directory context, command, timestamped attributed
output, and results. Forward references; never embed the log in prompts.

The adaptive verify helpers preserve both failure types. `task-documents.yaml`
provides consumer aliases without replacing the original stored identity.
When no log exists, a short error document preserves the actual failure.

Command stdout/stderr fields are bounded previews. Set
`capture_diagnostics: always` for commands whose successful validation evidence
must survive. Extensions retain logs automatically. Keep typed status fields for
control flow: process exit and operation success are distinct.

Historical version-1 stream artifacts remain readable under `error/legacy/`.
Do not reconstruct interleaving or timestamps from those separate streams.

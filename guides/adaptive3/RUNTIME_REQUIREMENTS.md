# Runtime requirements for resilient adaptive3 jobs

The recipe now routes ordinary caught failures into a resolver in the same job.
The following runtime capabilities are needed before promising that only a human
can end an unfinished job. These are c2j requirements, not additional recipe
bookkeeping. No external ticket was submitted as part of this implementation.

## 1. Keep accepted jobs recoverable after runtime failures

Template/schema errors and failures that prevent a worker or resolver from running
cannot reliably be repaired by another node in the broken recipe.

c2j should retain the job, its last durable boundary and the original diagnostic,
put it into an inspectable suspended state, and provide an explicit operation to
resume it after correction. Human cancellation should still cancel it. Recovery
must preserve recorded effects such as merges, submitted children and approvals.

Acceptance example: a publish invocation cannot start. The merged commit remains
recorded; after the environment is fixed, the same job continues publication
without performing the merge again.

## 2. Allow a parent to help a still-open child

Adaptive3 uses the native terminal child wait today. If a child is waiting for
help in its own resolver, its parent needs a durable notification and a way to
respond while that child remains open.

Expose the child request, the relevant task/result references and an operation
to supply guidance or approved input. The native wait should wake for this event
as well as terminal outcomes. Do not require an agent to poll or the child to fail
just to notify its parent. Preserve cancellation messages and the distinction
between a stop request and a request to retry with corrections.

Acceptance example: a storage child asks whether an existing API is acceptable.
The parent can read that request, answer using its human-approved direction, and
continue waiting for the same child.

## 3. Verify validator dependency activation on supported workers

The shipped `tools.yaml` declares Python, Pillow, cmark and yq dependencies through
native `execution_needs`. On this host, portable Nix 2.18/2.20 produced a derivation
JSON shape rejected by c2j:

```text
json: cannot unmarshal object into Go struct field nativeDerivation.inputDrvs of type []string
```

The current c2j parser handles older array values and the newer versioned shape;
this intermediate shape needs compatibility or a documented supported Nix version.
Portable Nix 2.35 could not complete on this host due to local SQLite/openat
permission errors, so it did not settle the normal-worker behavior.

Run the unmodified adaptive3 suites on a supported worker. The acceptance condition
is native installation and execution of the declared validators, with no removed
`execution_needs` or preinstalled-tool substitution. The local execution results
are documented separately in [TEST_RESULTS.md](TEST_RESULTS.md).

A real worker has now demonstrated an additional activation failure:
[the Cortex job audit](AUDIT_3M28e5.md) records three `No module named 'PIL'`
failures after successful dependency preparation. Current c2j source filters out
Python's import-path activation variables. Supported-worker acceptance must cover
those variables and cached activation, not merely package realization. The local
preinstalled-dependency test lane cannot prove this contract.

## 4. Transport a selected directory as one native reference

The current pinned runtime (`3fec5e4`) supports stored, external, value and attached
file references. A stored key names one job/task/file. An artifact-set binding
expands a map of those references; it is not a compact directory reference.
Object checkpoints use a different opaque archive contract and are unsuitable
for ordinary human review attachments.

The new native collection test measures this directly:

| Files delivered | References emitted, including command log | Serialized reference map |
| --- | --- | --- |
| 32 | 33 | 6,524 bytes |
| 1,024 | 1,025 | 202,940 bytes |

File bytes arrive correctly, but metadata grows with file count before any review
or child-result copies. The recipe cannot honestly promise compact directory
transport with this contract. It groups selected files by directory and keeps
presentation to a title, primary document and descriptive local links.

c2j should provide one immutable directory reference that binds a selected subtree,
materializes in inbox, survives child results and review forms, and allows paginated
listing and exact file reads. Retain original producer identity and relative paths.
Cortex should browse the same collection without requiring every file reference
in the form. Neither side should need a custom archive or per-file prose metadata.

Acceptance: pass a 1,024-file subtree through child completion and human review;
keep serialized recipe state bounded by the number of selected collections,
verify exact bytes and safe paths, and navigate local links in the actual review
UI. Until that exists, TODO item 10 is blocked at the runtime/consumer boundary.

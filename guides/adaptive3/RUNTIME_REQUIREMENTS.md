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

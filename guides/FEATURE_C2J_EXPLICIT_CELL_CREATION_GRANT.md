# Explicit cell creation from a root-owned recipe node

Implemented by c2j main `d6553a2` and adopted by the shared creation recipe on
2026-11-05. This request originally identified the missing grant in `dc36b1b`.

## Supported contract

```yaml
perms:
  jobdb:
    cells:
      create: true
```

Only the designated command receives this grant. Inside a task,
`c2j cell create NAME --repo REPO --request-id ID --json` uses the authenticated
task broker and owning tenant. Missing authority fails without falling back to
ambient administrator credentials. Reusing the request ID with the same fields
reconciles retries; conflicting creation requests do not replace a registry entry.

An optional literal `cells.cellNames` list narrows the grant. The shared recipe
uses approved names supplied at runtime and grants creation only to its fixed
registration command; agents receive no creation authority.

Sources: [named-cell contract](https://github.com/colony-2/c2j/blob/d6553a2/GUIDE-Named-Cells.md)
and [permission contract](https://github.com/colony-2/c2j/blob/d6553a2/GUIDE-Node-Permissions.md).

## Recipe integration

1. Root reviews and obtains approval for names, repository destinations, purposes,
   and the exact root dependency-config change.
2. [register-cell.yaml](../recipes/create/register-cell.yaml) checks root ownership
   and runs the CLI in root. It uses a stable job/name request ID and retains
   `registration.json` before child submission.
3. The cell-owned initialization child publishes its approved PURPOSE.md.
4. Root applies, verifies, and publishes the approved dependency configuration.
5. Only completion of all required steps establishes readiness.

Registration supplements Git publication and the dependency update. Partial
completion is retained; a later failure does not delete registry records or
published repositories.

## Separate submission authority

Cell creation does **not** grant submission rights to the new cell. The deployment
must authorize the parent's destination-cell submission scope separately. Merely
being named `root` or selecting its workspace supplies no administrative authority.

See the [implementation and validation report](IMPLEMENTATION_NAMED_CELLS.md).

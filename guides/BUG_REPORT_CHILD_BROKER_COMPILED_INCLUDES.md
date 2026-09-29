# Child broker rejects compiled includes as reserved metadata

Owner: c2j. Observed 2026-09-29 with the local workspace-capable build
`v0.0.54-0.20260929012541-9f9d9d0cfa78+dirty`.

## Reproduction

Run a parent command op against a separate JobDB service. Inside that op, submit
this local recipe through the inherited child broker:

```yaml
id: included-child
sequence:
  - id: phase
    include: ./phase.yaml
```

`phase.yaml` can be a simple recipe containing a command op. Invoke:

```sh
c2j submit 'Refined design brief' --cell /path/to/child-cell \
  --recipe-file /path/to/included-child.yaml --json
```

Expected: a child job is recorded, and workers can run the compiled recipe.
Observed:

```text
child job broker rejected submit: decode embedded recipe "refined-child":
__c2j_internal metadata is reserved for compiler-generated recipe snapshots
```

The live consultation test reproduced this after the complete A/B/A/B/A design
conversation. The child included `mandate.yaml`; there was no authored
`__c2j_internal` field. The same test submits successfully when the fixture's
mandate definition is written inline rather than through `include`.

## Likely cause and requested fix

`childbroker.NewSubmitRequest` marshals the resolved recipe, including
compiler-generated metadata. `Server.submit` decodes it with
`recipe.LoadRecipeFromReader`, which rejects internal metadata in authored
recipes. Preserve the distinction between untrusted authored YAML and trusted
compiler snapshots across the broker boundary; do not simply permit arbitrary
internal metadata in source recipes. Add a broker integration test with an
included child recipe, including workspace-bearing includes.

## Impact and test boundary

The recipe dialogue and direct child submission work. Child recipes containing
compiled includes need this runtime fix before their brokered submission can be
relied on, including applicable local/shared default-recipe paths. No runtime
files were changed in this cell. The deterministic handoff test inlines its small
fixture so it can independently verify refined-brief transport, real job
attribution, captured `jobs.job_ids`, waiting, and session resumption. It does not
claim that brokered submission of included production defaults is fixed.

## Independent regression

`recipe-tests/verify-consultations.py` now includes `broker-includes`, which submits
and executes a child with a compiled include through the real broker using a
separate ephemeral JobDB. It has no node workspace or child-wait dependency, so the
workspace replay issue cannot mask this failure. Run it through
`recipe-tests/run-defaults.sh`; the suite remains nonzero until this regression
and the replay regression both pass.

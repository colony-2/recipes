# Bug: scoped restart changes numeric recipe values and breaks completion

Owner: c2j. Work type: bug report.

Job `3Lt6z0TiPnXSLGknmx7Sr801LBr` on `http://192.168.1.195:9047/c2`
successfully merged vz-macos commit `13418ef1c46de214e1864affecf4a96bb91e5b12`
into `refs/heads/main`, then failed while evaluating final outputs:

```
failed to resolve input 'rebase_repairs': failed to evaluate CEL expression: no such overload
```

The job retained recipes `610a59bba9eb707b96f84972b929958dff1c6dcb` and restarted
at `merge_reviewed_candidate`. Its restarted activation reports c2j
`f04763b5cca378aba2f71321bc18732df0c30da9`. Do not rerun that publication to reproduce
this bug: the merge already happened.

## Cause and reproduction

The attached `restart-counter.go` uses c2j's public template package. Run it from
a c2j source checkout with `go run /path/to/restart-counter.go`.
It resolves the actual recipe default, repeats the unchanged output expression,
then calls the native `CloneForRestart` / `AdoptRestart` path without a context patch.

Default:

```
${{ inputs.?prior_rebase_repairs.orValue(0) }}
```

Output expression:

```
${{ inputs.prior_rebase_repairs + (state_exists('rebase_repair') ? size(states.rebase_repair.runs) + 1 : 0) }}
```

Observed on c2j `33e2a4de4e99d3a577a38dca4b8de33d43a099ce` (0.0.124):

```
recipe default: int64(0)
initial Go value: int64(0)
initial unchanged expression: map[counter:0]; error=<nil>
repeat without restart Go value: int64(0)
repeat without restart unchanged expression: map[counter:0]; error=<nil>
after native restart clone/adopt Go value: float64(0)
after native restart clone/adopt unchanged expression: map[]; error=failed to resolve input 'counter': failed to evaluate CEL expression: no such overload
JSON control: typed field=int64; interface map value=float64
```

This does not mean Go changes a concrete integer struct field's type. The resolver's
`templateData.ContainerInputs` is `map[string]interface{}`. `CloneForRestart` in
`pkg/template/attempt.go` marshals and unmarshals the entire template data through
`encoding/json`. Numbers decoded into interface values become float64. CEL then
correctly rejects mixed double/integer addition. A concrete int64 struct field
survives the same JSON round trip; the reproduction includes that control.

The relevant restart implementation and CEL adapter are unchanged between the
reproduced release, the incident's runtime commit, and inspected main
`11574b555465d1558754b436f68ef5c7ac0912ff`.

## Requested outcome

Preserve recipe values and their CEL semantics across scoped restart, including
values inside nested maps/lists, transition data and enclosing scopes. Do not
require recipes to cast counters merely because a restart occurred. Check large
integers as well as ordinary counters so a fix does not conceal precision loss.
Preserve legitimate floating-point values too. Keep the existing restart isolation
and graph-sharing guarantees.

Tests should compare unchanged expressions before/after restart and cover a
native scoped restart that reaches final outputs after its resumed task succeeds.
The attached probe isolates the resolver defect; it does not claim to exercise the
whole CLI restart lifecycle. Add that lifecycle coverage in c2j.

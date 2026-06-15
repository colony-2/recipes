---
title: "Failure Handling"
weight: 38
---

Recipe nodes can use `timeout`, `retry`, and `catch` to control failures.

Timeout:

```yaml
- id: bounded
  op: command_execution
  timeout: 2m
  inputs:
    run: npm test
```

Op-specific command timeout:

```yaml
- id: bounded_command
  op: command_execution
  inputs:
    timeout: 30s
    run: npm test
```

Catch clauses choose exactly one action:

- `to`: route to another state.
- `continue`: complete the failed node with replacement outputs.
- `fail`: reclassify or annotate the failure.

Route from a failed state:

```yaml
state:
  initial: risky
  states:
    risky:
      op: command_execution
      inputs:
        run: exit 1
      catch:
        - id: recover
          when: true
          to: fallback
    fallback:
      op: command_execution
      inputs:
        run: printf recovered
```

Continue with replacement outputs:

```yaml
catch:
  - id: soft_fail
    when: true
    continue:
      outputs:
        ok: false
        reason: validation failed
```

Reclassify a failure:

```yaml
catch:
  - id: explain
    when: true
    fail:
      kind: policy_error
      code: missing_review
      message: Required review was not present.
```

Prefer deterministic policy failures as data when the parent workflow should continue. `c2ops rule_gate` is usually better than making a command fail for policy checks.


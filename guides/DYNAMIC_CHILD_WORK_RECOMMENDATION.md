# Recommendation: Dynamic Child Work In C2 Recipes

## Status

Draft recommendation.

## Problem

`new-ticket` needs to start child work from runtime data:

- dependency jobs from implementation plans;
- adversarial reviewer recipes from a review policy;
- child jobs requested dynamically by an agent.

The current recipe patterns make this hard to read:

- dynamic child specs are constructed with inline `jq`;
- fixed reviewer sets become repeated recipe states;
- downstream consumers must know too much about how children were started;
- child failures are not always easy to treat as workflow data.

The first instinct was to add a generic `for_each` node. That may still be
useful later, but it risks exposing a raw `items[]` shape that pushes complexity
to every downstream consumer.

## Recommendation

Do not make generic `for_each` the first primitive.

Instead, add a C2-specific **`child_group` node** for durable child recipe work.
It should:

- start child recipes from a typed item list, optionally waiting for all child
  results;
- preserve every child job ID, status, output, artifact, and failure;
- expose useful built-in summaries such as `job_ids`, `failed_required`, and
  `blocking_issues`;
- write an optional aggregate artifact such as `reviews/review-pack.json`;
- make downstream routing simple.

Keep **deferred submit/await** as a separate feature for child work discovered
inside command, Codex, or other agent subprocesses.

Use a generic `for_each` or `map`/`collect` primitive only after the child-group
shape proves insufficient for non-child-recipe work.

## Recommended Primitive Stack

| Need | Recommended primitive |
| --- | --- |
| Fixed linear workflow | `sequence` |
| Branching lifecycle | `state` |
| Durable child recipe set from typed items | `child_group` |
| Agent subprocess asks for child work | deferred `c2j submit --await` |
| Generic repeated non-child action | defer until a stronger use case exists |
| Aggregating child results into a policy shape | `child_group.aggregate` named profiles |

## Why Not Raw `for_each` First

A raw `for_each` node would likely expose outputs like:

```yaml
states.counterpoint.outputs.items[0].collected.blocking_issues
```

That is technically complete, but downstream recipes then need to write list
filtering, flattening, and required/optional failure logic repeatedly.

For C2's current use cases, downstream code usually wants higher-level fields:

```yaml
states.counterpoint.outputs.ok
states.counterpoint.outputs.summary.failed_required
states.counterpoint.outputs.aggregate.blocking_issues
states.counterpoint.outputs.child_job_ids
```

That argues for a domain-aware child-work node first.

## Relationship To Deferred Submit/Await

`child_group` is for recipe-authored child work. The parent recipe knows the
item list and starts children as part of the recipe graph.

Deferred submit/await is for subprocess-authored child work. An agent or command
inside an op decides it needs child work and calls:

```bash
c2j submit --await ...
```

The framework records the intent, submits children after the task completes,
persists the parent task output, and resumes the parent after children complete.

These features are complementary. `child_group` should not replace deferred
submit/await.

## Expected `new-ticket` Shape

```text
intake bundle
-> child_group: reviewer recipes
-> rule_gate: pre-implementation policy
-> implementation skill loop
-> validation
-> rule_gate: final policy
```

Dependency jobs can use the same child-group pattern:

```text
implementation plan
-> child_group: dependency jobs
-> waiting/umbrella control
```

## Open Questions

- Should `child_group` be a new core node type or a built-in recipe op?
- Should aggregation be limited to child status fields, or support named
  aggregate templates?
- Should child output artifacts be automatically bundleable by group key?

V1 should avoid concurrency controls, custom aggregation expressions,
`await_existing`, and wait-without-result modes. Keep the surface to:

- `start`;
- `run_and_get_result` with wait-for-all/result-all semantics;
- `required`;
- `when`;
- named aggregate profiles: `none`, `review_pack`, and `job_ids`.

Non-goal for the first version: wait-for-any / wait-for-at-least-one monitoring.
SWF does not currently have a good durable primitive for that, so `child_group`
should stick to start-only and wait-for-all/result-all semantics. For the same
reason, fail-fast while children are still running should also be out of scope;
required/optional failure policy should be evaluated after all selected children
are terminal.

## Alternatives Considered

### Explicit Recipe Nodes

Use ordinary `sequence` or `state` nodes for each child recipe.

Best when:

- the set of children is small and static;
- each child has distinct routing;
- the job story should show separate named states.

Weakness:

- noisy for reviewer sets;
- does not handle dynamic dependency specs well;
- aggregation still needs custom logic.

### Generic `for_each`

Add a map-style node sibling to `sequence` and `state`.

Best when:

- C2 needs repeated non-child actions;
- item executions are independent;
- downstream consumers can handle an ordered `items[]` list.

Weakness:

- downstreams may need repeated list traversal and flattening;
- required/optional child semantics are not naturally built in;
- child job IDs and review packs are domain concerns layered on top.

The current recommendation is not to implement this first.

### Extension Op Spec Renderer

Use a c2ops extension op to transform an input artifact into a `recipes.run`
payload.

Best when:

- the immediate pain is inline `jq`;
- the child execution can still be done by existing recipe ops.

Weakness:

- does not own child job status;
- cannot improve job-story grouping by itself;
- cannot provide durable await semantics.

This can be a bridge, but not the final primitive.

### Deferred Submit/Await

Use the nested job context proposal:

```bash
c2j submit --await --recipe child ...
```

Best when:

- an agent or command subprocess discovers child work dynamically;
- the parent task should not burn its lease polling;
- the parent task must not rerun after child completion.

Weakness:

- not a replacement for recipe-authored child sets;
- first version may only return child job IDs, not child outputs;
- needs core c2j/SWF support.

This should be implemented independently of `child_group`.

## Related Docs

- [REQUIREMENTS_CHILD_GROUP_NODE.md](new-ticket-simplification/REQUIREMENTS_CHILD_GROUP_NODE.md)
- [PROPOSAL_C2J_NESTED_JOB_CONTEXT_AND_DEFERRED_WAIT.md](PROPOSAL_C2J_NESTED_JOB_CONTEXT_AND_DEFERRED_WAIT.md)

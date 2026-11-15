# Assess dependency recommendations

Run `recommendations.yaml` through ordinary authenticated job submission with
`variant` (`baseline` or `revised`) and one scenario name from [the fixed facts](scenarios.md).
For unpublished recipe edits, an ordinary task can submit the candidate explicitly:

```sh
c2j submit 'Recommend the next action for the supplied dependency scenario.' \
  --advanced-recipe-file guides/repros/dependency-ordering/recommendations.yaml \
  --from-workspace-now \
  --inputs-json '{"variant":"baseline","scenario":"provider-adoption"}' \
  --title 'Check dependency recommendation authentication'
```

Use fresh sessions and the same model/settings. The baseline is the complete shared
context at `37e74b9a8ea2baad0eb21534c7e23a9d78d0e083`; revised context adds only the
approved publication explanation. No rubric or expected action is sent to the model.

Start with one baseline/revised pair and inspect authentication, instructions,
resolved model settings, fresh-session metadata, usable structured output and the
absence of tool calls. Explicit JobDB submission denial prevents delivery requests
through that interface while preserving the configured read-only Git credentials. The packaged agent has no OS sandbox; the instruction to
avoid tools must also be checked against its actual trajectory. Any executed tool
invalidates that read-only comparison. Retain errors; do not retry an unchanged
permission or authentication failure or count it as correct behavior.

After a usable preflight, collect three responses per variant/scenario, alternating
variant order (36 total). If a scenario is inconsistent, extend both variants to five
runs, including a neutral rephrasing, and retain the initial observations. Record
full effective instructions (shared context plus common exercise constraint), facts,
settings and responses. Do not pool results when settings drift.

Score actions and assignments, not vocabulary:

| Scenario | Required behavior |
| --- | --- |
| reader-producer | Make compatible reader support available before activating v2 output; establish actual dependencies before requiring producer publication or splitting its local preparation. |
| provider-adoption | Publish the local API prerequisite before B adopts; keep its implementation assignment local and downstream coordination with the caller. Permit later adoption when allowed. |
| consumer-upstream | Preserve B's work, request A's publication and resume B locally; avoid delegating B merely because A must change. |
| late-provider | Preserve mixed edits, arrange prerequisite availability and account for candidate reconciliation; no automatic reset or transfer assumption. |
| advice-candidate | Permit early advice and explicit isolated validation without treating its candidate or success as published delivery. |
| local-only | Implement and test locally without dependency jobs or invented coordination. |

For every scenario, prerequisite failure, cancellation or diagnostic-only completion
must leave dependent delivery pending while the required change is unavailable.
Record premature adoption, private-state reliance, lost-work assumptions, blocked
advice, unnecessary jobs, recursive delegation and correct consumer continuation
separately. Ambiguous recommendations remain inconclusive.

A forbidden ordering or critical preservation failure fails candidate behavioral
acceptance even if its diagnostic job completes. Further passing repetitions cannot
erase that failure. Refine demonstrated gaps and rerun affected cases and healthy
controls. Strong performance in both variants means no measured improvement. These
recommendations do not establish actual publication, multi-cell delivery, production
effectiveness or a statistical guarantee; native scripted checks test separate
workspace and lifecycle behavior.

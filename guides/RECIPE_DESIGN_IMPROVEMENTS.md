# Recipe design improvements

Job `3LX5qRkgkAaQGCpQs1cg4jHHI5T` passed verification twice but returned to
implementation because assessment lacked evidence of the requested upstream
`c2j submit --run --embed` validation. The agent was forbidden to submit jobs,
and the workflow had no step to perform that validation. Repeated attempts
ended at the iteration limit without resolving the finding.

The recipe should ensure that every required outcome has an authorized actor
and an executable path to completion.

- **Permit bounded validation runs.** Distinguish running a recipe as an
  integration test from delegating project work. Let implementation agents run
  required tests and retain invocation, candidate identity, results, and artifacts.
- **Route findings by the action needed.** Distinguish code defects, missing
  evidence, environment blockers, and requirement questions. Each finding should
  identify an owner, next action, and closure condition instead of returning only
  `revise`.
- **Support blockers without dependency jobs.** Missing tools or execution
  environments must be reportable without prerequisite job keys. Route these to
  an actor who can supply the missing capability or decide the scope.
- **Stop retries that cannot make progress.** When the same finding recurs with
  no relevant change, request the specific intervention needed. Raising the
  iteration limit does not resolve an impossible handoff.
- **Reuse valid verification evidence.** Documentation-only follow-ups should
  return to assessment without repeating all checks when the verified code,
  verification definition, and relevant execution conditions remain valid.
- **Check acceptance feasibility early.** Before implementation, identify who
  performs each required validation, their authority and prerequisites, and how
  evidence reaches assessment.

Keep independent assessment: passing checks may leave requested outcomes
unproven. Improve how findings lead to resolution. Prioritize validation
authority and actionable blocker routing.

These are proposed recipe improvements, not implemented behavior. Shared flow
and instruction changes belong to this cell; any required execution or permission
capabilities belong to c2j/c2ops.

# Requirements: Sequential Task Job Orchestration

## Status

Draft requirements for expressing adaptive task execution with existing c2j
recipe primitives.

## Motivation

Implementation plans often contain a sequence of small tasks that should become
small, reviewable, mergeable C2 jobs. These tasks are not the same shape as
parallel reviewer fanout.

c2j jobs already provide durability, auditability, artifacts, typed
inputs/outputs, git persistence, target refs, and job stories. The task
execution pattern should use those core concepts directly rather than creating
a secondary task-request/task-result protocol or a new task-loop runtime
primitive.

The normal pattern is:

1. A planner step creates or updates a durable plan state artifact.
2. The parent recipe selects the current head task.
3. The parent starts one child task job using ordinary recipe inputs.
4. The child job implements, validates, reviews, and merges/advances its target
   ref as part of its own success path.
5. The parent softly awaits the child job.
6. The parent routes the child status, outputs, artifacts, and job story
   context to the planner.
7. The planner updates the plan state.
8. The loop repeats.

When the target ref is `main`, each successful child task advances `main`, and
the next child task naturally starts from the updated `main`. If the work should
run experimentally, the same pattern uses a different target ref.

## Goals

- Express dependent task execution with normal state machines, child jobs,
  recipe inputs/outputs, artifacts, target refs, and soft child status.
- Keep plan state as durable recipe artifacts or structured recipe outputs,
  separate from implementation git commits.
- Let child task jobs own task-local implementation, TDD, review, validation,
  and merge/advance behavior.
- Let the parent recipe sequence work and route child outcomes to planner
  decisions.
- Avoid starting all dependent implementation tasks up front.
- Avoid inventing a second request/result/base-handoff system beside c2j jobs.
- Keep the pattern easy to inspect in job stories and easy to test with mocked
  child outcomes.

## Non-Goals

- Do not add a task-job-loop primitive to c2j core.
- Do not require `task_request.json` or `task_result.json` as a new protocol.
- Do not require explicit commit, thinpack, or `base_after` handoff between
  parent and child in the normal target-ref workflow.
- Do not make the parent recipe re-review child implementation correctness.
- Do not make c2j infer why a child failed or decide how to repair it.
- Do not use the implementation git worktree as the durable plan-state store.
- Do not replace `child_group` for parallel reviewer/adversarial fanout.

## Requirement 1: Native Recipe Loop

The parent task loop should be authored as an ordinary recipe state machine.

Each iteration must be able to:

- select the next task from the current plan state;
- start exactly one child task job with ordinary recipe inputs;
- pass the task text, constraints, relevant artifact refs, and target ref as
  child inputs;
- softly await the child job;
- inspect child status, outputs, artifacts, and job story references;
- route the result to a planner or decision step before selecting the next
  task.

The next task must be selected after the prior child outcome is known. A static
`for_each` over the original task list is the wrong default shape for dependent
implementation work.

## Requirement 2: Plan State

Plan state should be durable recipe data, not hidden LLM session state.

The plan state should be able to track:

- task IDs and task text;
- dependencies and readiness;
- task status;
- target ref policy, defaulting to the job or project target ref;
- scope and validation expectations;
- child recipe or skill hints;
- feedback and rationale from prior child jobs;
- skipped, blocked, superseded, and completed task IDs.

The planner may use a continuing Codex session for continuity, but the durable
plan artifact or structured output is the source of truth.

## Requirement 3: Child Job Handoff

The parent should hand the selected task to the child job through existing
recipe inputs and artifact bindings.

Typical child inputs:

- task ID and task text;
- current plan context needed for this task;
- target ref, usually inherited as `main`;
- relevant artifacts or artifact refs;
- constraints, scope, and validation expectations;
- selected skill or prompt contract.

The child job invocation, inputs, artifacts, outputs, and job story are the
durable handoff. A separate handoff artifact may still be useful for a specific
recipe, but it is not a platform requirement.

## Requirement 4: Child Job Responsibility

The child task job owns task-local success.

A successful child task job should have:

- implemented the task;
- run required TDD/debug/review loops;
- produced required evidence and artifacts;
- satisfied task-local gates;
- merged or advanced the target ref when the task changes code.

The parent should treat child success as a completed task outcome. If the child
cannot complete the task, it should fail or return a non-success status with
outputs/artifacts that the parent can pass to the planner.

## Requirement 5: Target Ref Sequencing

The normal git handoff between dependent task jobs is the target ref.

Requirements:

- Each child task job runs against a target ref, defaulting to `main` unless the
  plan or recipe overrides it.
- A successful code-changing child advances that target ref as part of its own
  workflow.
- The next child targeting the same ref starts from the updated ref.
- Experimental or branch-scoped plans use the same pattern with a different
  target ref.
- The parent should not need to pass explicit commit hashes or thinpacks between
  dependent child jobs in the normal target-ref workflow.

## Requirement 6: Parent Continuation Decision

After each child outcome, the parent should ask what to do next rather than
re-evaluating task correctness.

The decision step should receive:

- current plan state;
- child job ID and terminal status;
- child outputs and artifacts, including partial outputs when available;
- validation or failure summaries exposed by the child;
- target ref used by the child;
- relevant job story references.

The decision step may be implemented with c2ops `run_skill`, a Codex session,
`rule_gate`, structured human input, or ordinary recipe transitions. It should
emit updated plan state and the next action.

Possible next actions:

- continue to the next ready task;
- retry or resume the same task;
- split or rewrite remaining tasks;
- skip or supersede a task with rationale;
- stop for human input;
- cancel or fail the workflow.

## Requirement 7: Optional Plan Helper Ops

If CEL/templates make plan manipulation noisy, c2ops-style helper ops may be
added. These helpers should be small, deterministic, and optional.

Good candidates:

- select the next ready task from a plan artifact.

No such helper is currently required. Validate the native recipe state-machine
approach first; add a helper only if task selection becomes hard to read or
hard to test.

This helper should not run child jobs, inspect implementation correctness,
merge code, or replace the recipe state machine.

## Requirement 8: Relationship To Child Groups

Use the sequential task loop when:

- tasks are code-mutating;
- tasks depend on earlier successful task jobs;
- later prompts or validation may change after earlier results;
- the next child should start from a target ref advanced by the previous child.

Use `child_group` when:

- children are independent;
- all children can start from the same context;
- waiting for all selected children is correct;
- downstream routing depends on an aggregate such as a review pack.

The two patterns compose: a child task job may use `child_group` internally for
parallel reviewers, and the parent may run `child_group` for adversarial
feedback between implementation tasks.

## Requirement 9: Job Story And Tests

The job story should show:

- selected task ID and reason;
- child job ID and target ref;
- child terminal status;
- child outputs/artifacts used by the planner;
- planner update or next action;
- final loop outcome.

Recipe tests should be able to mock:

- task selection;
- child success;
- child failure with partial outputs;
- blocked tasks;
- planner rewrites;
- target-ref overrides.

Tests should not need real child jobs to validate parent routing behavior.

## Acceptance Criteria

- A parent recipe can run two dependent child task jobs targeting `main`; the
  second child naturally starts after the first child advances `main`.
- A parent recipe can run the same pattern against an experimental target ref.
- A failed child job is treated as structured workflow data via soft child
  status and routed to a planner decision.
- The pattern works without `task_request.json`, `task_result.json`,
  `base_after`, or a task-loop primitive.
- Reviewer/adversarial fanout remains expressible with `child_group`.

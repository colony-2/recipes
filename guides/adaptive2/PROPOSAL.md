# Adaptive2: make the work easy to follow

**Current status:** `build.yaml` now selects adaptive2 for new submissions.
See [the rollout assessment](ROLLOUT.md). The plan and initial trial results below
record the earlier opt-in milestone; pending capabilities remain identified.

**Proposal, 2026-11-08.** Start here. [Design details](DESIGN.md),
[example documents](EXAMPLES.md), and [live trial plan](TRIALS.md) expand this page.
The first slice is now implemented as a separate recipe; the current adaptive recipe remains unchanged.
See the [implementation assessment](IMPLEMENTATION.md) and [real review packets](results/README.md).

## Problem Description

A human joining a job should quickly understand what was asked, why it matters,
what the cells decided, and what needs approval. Expert attention is scarce;
the recipe should do the work of framing the task before asking for it.
Today that story is scattered
across technical reports. Design can be skipped, and the first routine human
checkpoint comes after implementation. A consultation's final agreement can
hide the alternatives considered and what remains unsettled.

## Non Goals

Replace working recovery, package requests, managed workspaces, verification, or
merge handling. Introduce a new job engine, elaborate classification system, or
mandatory debate. Automatically remove the final human review in this version.

## What we are planning to do

Start from adaptive and introduce four understandable assignments:

- **Feature request:** add or change a capability.
- **Bug report:** correct behavior that differs from an expectation.
- **Explanation:** answer a question, with evidence and limits.
- **Oversight:** organize an outcome into feature, bug, and explanation work.

For delivery work, first write a one-pager using these five sections. Keep the
narrative concise and retain every important design question and answer; that
table may be the largest section. “One-pager” imposes no page or word limit.
Consult relevant cells and show UI mockups when needed to judge the direction.
Ask the human to approve that direction **before** detailed specification and
implementation. A simple explanation can return its answer directly.

After approval, develop the detailed design, test statements, and a fresh
implementation handoff. Keep the existing implementation and recovery loop.
The final review starts with what changed and whether it matches the approved
direction, then shows dependencies, tests, omissions, and interface changes.

At every meaningful handoff, show the original problem, current position, and
next action. Use descriptive titles, such as **“Approve 1p for c2j feature: add
CLI debug capabilities.”** Give each consultation a short summary and a readable exchange
history. Preserve the participants' actual replies and link their evidence.
When follow-up work is needed, the receiving cell writes the agreed handoff as a
feature request, bug report, explanation, or oversight assignment. The requester
checks the outcome and scope; the coordinator passes the receiver's document through.

## Compat/Upgrade

Add an opt-in `recipes/adaptive2/build.yaml` entrypoint. Keep `build.yaml` on
adaptive during trials. Adaptive2 children must use adaptive2 too. Preserve the
existing hooks and recovery contracts; jobs already running retain their recipe.

## Key challenges/design questions & answers

| Question | Proposed answer |
| --- | --- |
| Does every request need a lengthy design? | No. A small fix gets a small one-pager. Explanations usually return an answer. |
| How do we avoid easy, unexamined agreement? | Ask owners to check existing capabilities, challenge assumptions, and explain alternatives. Do not manufacture disagreement. |
| Will every child ask the same approval question? | Reuse an explicitly reviewed child brief. New scope needs a new decision; a parent goal alone is insufficient approval. |
| Can the human still change direction later? | Yes. Reopen the one-pager for material changes; keep ordinary corrections in implementation. |
| How will we know the documents help? | Run real agents through real recipes in disposable cells and review their actual documents before expanding the rollout. |

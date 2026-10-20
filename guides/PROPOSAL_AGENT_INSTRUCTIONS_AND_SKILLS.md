# Discussion: initial agent instructions and optional skills

Status: packaging options, separate from the
[consultation recipe specification](PROPOSAL_CONSULTATION_SESSIONS.md).
The consultation loop, separate sessions, consultant agreement decision,
iteration budget, escalation, and submission gates are recipe responsibilities
under every option. A skill does not implement or replace that mechanism.

## Stable setup and current work

Use Codex `instructions` for stable guidance when a session is created: a cell is
the whole repository; use root `PURPOSE.md` if present and infer purpose
contextually otherwise; respect ownership; request consultation before delegating
changes; and continue independent work before yielding as blocked.

Use the current prompt and bound assets for the task, phase permissions, present
role assignment, selected workspace paths, questions, new evidence, and human
direction. Follow-ups do not repeat cell setup. Changing `instructions` cannot
change a resumed session; use a fresh session when permanent guidance must differ.

## Packaging options

| Option | Initial instructions | Optional skills | Tradeoff |
| --- | --- | --- | --- |
| A. Comprehensive guidance | Cell model, coordination obligations, and detailed advice for framing requests, evaluating purpose and overlap, and comparing technologies | Specialized domain techniques | Discoverable but adds material many sessions never need. |
| B. Small core plus optional expertise | Cell model, ownership rules, consultation triggers, and progress-before-wait obligations | Richer domain advice and reusable analytical techniques when relevant | Smaller setup while universal obligations remain visible. |
| C. Minimal setup with extensive skills | Basic task setup and a skill index | Most explanatory cell and domain guidance | Depends heavily on discovering and loading the right guidance. |

Recommend **B**, without making skill availability a prerequisite for any
consultation profile. The recipe must always supply enough task instructions and
criteria for root eligibility, feature negotiation, or expert assessment. Optional
skills can improve the analysis—for example, security methodology or a project's
technology policy—but must not be required to discover how to progress the
recipe, preserve sessions, count turns, or request review.

Root evaluation prompts belong in the shared consultation profile and are passed
at execution time. They do not require a root-local skill or copied workflow
boilerplate. Project skills may add policy or expertise when available; they
cannot override the recipe's approval and agreement boundaries.

This packaging decision can be made independently of implementing consultation.
First establish the recipe contract and necessary role prompts; extract optional
knowledge into skills only where reuse and discoverability justify it.

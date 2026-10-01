# Mandates and cross-cell design

The implemented convention is deliberately small:

- Read the plain Markdown [cell mandate](CELL_MANDATE_SPEC.md) from `.c2j/mandate.md`.
- Explain whether the request fits, partially fits, or belongs outside the cell.
- Use a separate session in another cell's workspace for design feedback when useful.
- Put the design and agreed external briefs in outbox artifacts for human review.
- Submit actual external work only after approval, then await native child-job results.

The [shared workflow](BUILD_EVOLVE_SHARED_WORKFLOW_PROPOSAL.md) describes the phase
boundaries and document locations. [Cross-cell conversations](CROSS_CELL_REPO_SESSIONS_DESIGN.md)
describes session handoff during design and implementation.

Ownership, agreement, and coverage are agent and human judgments. Recipes validate
routing responses with small JSON schemas; they do not attempt to establish these
judgments through clause IDs, outcome IDs, hashes, or handoff certificates.

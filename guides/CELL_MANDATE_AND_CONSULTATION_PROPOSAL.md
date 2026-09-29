# Cell mandates and cross-cell consultation

This overview is superseded by two focused documents:

- [Cross-cell repository sessions design](CROSS_CELL_REPO_SESSIONS_DESIGN.md):
  a cell B repository session within cell A's existing job, with disposable
  repository state and durable conversation state.
- [Cell mandate specification](CELL_MANDATE_SPEC.md): the canonical
  `.c2j/mandate.md` convention and the `fits`, `partial`, and `outside` assessment
  contract. [This cell's mandate](../.c2j/mandate.md) adopts the file convention.

The shared build/evolve recipes now implement these gates and hosted dialogues
using c2j node workspaces. No new session operation is required. Actual work
continues through separate jobs after design approval. The implementation design
lists c2j broker/replay bugs that currently block reliable production handoffs.

## Architectural choice

A cell defines responsibility, a job owns execution, and a session holds a
conversation. A can host a B-grounded conversation without a job running in B.
Ordinary cross-cell discussion should use that hosted session; actual B work
should use a B job and the existing child-job dependency flow.

| Model | Appropriate use |
|---|---|
| A reads B's documents and code | Quick discovery and factual lookup |
| A hosts a B-grounded repository session | Requirements dialogue, mandate assessment, and design feedback |
| A starts a consultation job in B | Work requiring B's execution environment or an independent lifecycle |
| Persistent service representing B | A future option if shared continuity justifies the service complexity |

The earlier proposal treated an enforced read-only checkout as a requirement.
That is unnecessary: local edits and experiments may occur in a disposable
checkout, provided repository changes are never carried into A, B's upstream,
or subsequent turns. The conversation and explicitly selected evidence persist;
the checkout does not. Read-only sandbox support is not a prerequisite.

A handoff to real B work carries a brief, transcript, and provenance. It never carries an implicitly approved implementation or the
consultation's experimental repository changes.

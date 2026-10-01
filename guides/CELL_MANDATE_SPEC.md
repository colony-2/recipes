# Cell mandate

Every cell keeps its authoritative responsibility boundary in **`.c2j/mandate.md`**,
relative to the cell root. Build and evolve read the same file regardless of their
working directory. Root `AGENTS.md` links to it; nested instructions specialize
working practices without changing ownership.

The mandate is ordinary Markdown describing what the cell should and should not
do. Purpose, responsibilities, exclusions, neighboring owners, and boundary
examples can help readers. There is no required front matter, section structure,
clause identifier, or machine-readable assessment document. See
[this cell's mandate](../.c2j/mandate.md).

During design the agent explains one of three judgments in its summary and design:

- **Fits:** the requested work belongs here.
- **Partially fits:** some work belongs here and some belongs elsewhere. Explain
  the split and identify the external owners or the ownership questions to resolve.
- **Outside:** the work belongs elsewhere. Explain the suggested routing; the
  local workflow acknowledges that outcome without implementation or merge.

A missing or ambiguous mandate calls for clarification. Uncertainty is not a
fourth ownership category. Agents can consult another cell to evaluate ownership,
refine interfaces, or decide whether a new cell is appropriate. Human design
approval resolves the proposed scope; a JSON schema cannot establish ownership.

An agent must not expand its authority by editing the mandate. Propose boundary
changes explicitly to the human maintainer and affected owners. Review changes
using the starting revision and Git history already maintained by c2j. Do not
record mandate hashes, clause ledgers, or a second baseline in the recipe.
A brief from another cell is context for a new job, which reassesses its own
mandate and seeks its own design approval.

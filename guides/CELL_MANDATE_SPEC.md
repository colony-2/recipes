# Cell mandate

A cell encompasses the entire repository in which its job operates. Every file
in that repository belongs to the cell. A task's target directory narrows the
work requested; it does not narrow the cell or establish another cell.

Every cell keeps its authoritative responsibility boundary in **`.c2j/mandate.md`**,
relative to the cell root. Build and evolve read the same file regardless of their
working directory. Root `AGENTS.md` links to it; nested instructions specialize
working practices without changing ownership.

The mandate is ordinary Markdown describing what the cell should and should not
do. It describes responsibilities, not a file inventory or path allowlist; files
do not need to be named in it to belong to the cell. Purpose, responsibilities,
exclusions, neighboring owners, and boundary examples can help readers. There is
no required front matter, section structure,
clause identifier, or machine-readable assessment document. See
[this cell's mandate](../.c2j/mandate.md).

The mandate need not comprehensively cover dependencies. Mention external
relationships where they clarify the responsibility boundary. Agents discover
task-relevant dependencies through the project's normal dependency system and
tooling. `c2j cells --json` lists cells we likely have influence over, which can
make coordinated dependency changes for new features easier. That listing is
neither an exhaustive dependency graph nor proof of control over a dependency.
Incomplete dependency discovery does not make a mandate incomplete.

During design the agent explains one of three judgments in its summary and design:

- **Fits:** the requested work belongs here.
- **Partially fits:** some work belongs here and some belongs elsewhere. Explain
  the split and identify the external owners or the ownership questions to resolve.
- **Outside:** the work belongs elsewhere. Explain the suggested routing; the
  local workflow acknowledges that outcome without implementation or merge.

Build checks for `.c2j/mandate.md` at the repository root before design. If missing,
it starts a separate same-cell build with a concrete mandate initialization prompt.
That job inspects the repository to describe current responsibilities, likely
purpose, and relevant external responsibility boundaries, distinguishing evidence
from inference without requiring a comprehensive dependency inventory. It proposes
the boundary for normal human design review, creates the
mandate, and follows the normal verification and merge approval flow.

The initialization build uses `bootstrap_mandate: true` to prevent recursive
setup jobs. This mode fixes the task to mandate initialization at the repository
root; it does not bypass review or authorize unrelated implementation. The parent
waits for successful completion and a merged commit, uses `thinpackrebase`
to refresh its managed Git state to that commit, and checks that
the mandate is present before designing the original request. Child failure, an unmerged result,
or a missing mandate after refresh stops the parent before design.
Runners need c2j commit `ee1420b12dee` or later, which fixes native refresh defaults,
shallow ancestry, and persistence into subsequent tasks. See the
[resolved bug report](BUG_REPORT_C2J_THINPACKREBASE_CHILD_REFRESH.md).

The native suites are `recipe-tests/cell-setup.test.yaml` (setup branches and Git
refresh) and `recipe-tests/build-cell-setup.test.yaml` (the full parent/child build
lifecycle with mocked model decisions and real reviews, gates, and merges).
Run them with `c2j test run --file <suite> --case-timeout 10m`. The full suite requires Nix and the
published c2ops packages; use c2j `6a25847a90d0` or later for the runtime's empty
secret/configuration fixtures. It needs no model credentials. See the
[native testing guide](../GUIDE-Native-Recipe-Testing.md).

Outside this explicit initialization path, a missing mandate calls for
clarification; an ambiguous boundary still calls for clarification. Uncertainty
is not a fourth ownership category. Agents can consult another cell to evaluate ownership,
refine interfaces, or decide whether a new cell is appropriate. Human design
approval resolves the proposed scope; a JSON schema cannot establish ownership.

An agent must not expand its authority by editing the mandate. Propose boundary
changes explicitly to the human maintainer and affected owners. Review changes
using the starting revision and Git history already maintained by c2j. Do not
record mandate hashes, clause ledgers, or a second baseline in the recipe.
A brief from another cell is context for a new job, which reassesses its own
mandate and seeks its own design approval.

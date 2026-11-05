# Shared recipes with registered cell names

Named-cell routing validated against `dc36b1b`; delegated registration validated
against c2j main `d6553a2` on 2026-11-05.

## Failure and correction

Job `6111daac-1a8c-43eb-b3a2-6aebd518967e` was correctly submitted to `gitvend`.
The shared build selected `context.git.repo` as its workspace cell, passing
`github.com/colony-2/gitvend` where the runtime now requires a registered name.
The failed job captured the old recipe; updating shared recipes does not rewrite
that job. A fresh submission is needed after the fix is published.

Owner workspaces now use `context.workflow.cell`, including configure, classify,
implementation, upstream resolution, and publication. Consultation routing keeps
`target.cell` separate from `target.repo`, and matches creation results by name.
Target probing enters a native named workspace, so c2j resolves repository
identity, credentials, and Git transport. Resolution failures remain unknown
rather than proving the repository is absent.

The default root cell is `root`; root discovery no longer derives a cell identity
from a repository location. Creation explicitly selects the root workspace and
checks that the job itself is root-owned. The local recipe repository config
declares `self.cell: recipes`.

## Explicit registration implemented

The requested sequence is approval, `c2j cell create`, cell-owned PURPOSE.md
publication, and the root dependency-config update. Registration is an additional
step, not a replacement for either existing Git change. Initialization now uses
the proposed name with an explicit repository assertion.

`recipes/create/register-cell.yaml` now runs the CLI in root with
`perms.jobdb.cells.create: true` only on its command node. It checks root job
ownership, uses a stable job/name request ID, and retains `registration.json`
before initialization. No agent or sibling task inherits creation authority.
The CLI uses the task broker; no administrative credential workaround is needed.

The deployment must separately authorize child submission to the new cell.
Creation does not expand the owning lease's target-cell ceiling. A denial stops
the workflow with registration retained, without reporting a ready cell.

## Validation

- Adaptive regression: **159 cases across 26 suites passed**, including native
  coordination, rebase recovery, upstream advancement, and publication checks.
- Four new native routing cases cover a registered name with a distinct repo,
  rejection of repository URLs as names, an unregistered name, and a missing ref.
  These are included in the adaptive total and also passed directly from source.
- A separate native creation guard test passed: a non-root-owned job cannot
  create through a root workspace.
- Creation decline, redirection, and cancellation: **three cases passed**.
- After the prompt edits, all **four agent-prompt cases passed** again.

The regression used an isolated copy with Nix selector operations expanded to
their extension primitive and package provisioning omitted. Model decisions and
human responses were fixtures; commands, workspaces, artifacts, and Git operations
were native. This does not validate live Nix provisioning, model behavior, or
deployment permissions. Native fixture scripts now obtain local upstream paths
from their Git remote instead of assuming `context.git.repo` is a filesystem path.

On `d6553a2`, three new cases passed using the real CLI and task broker: repeat
registration preserves identity and denies an ungranted sibling; conflicting
retries fail; foreign ownership is rejected. Two publication cases passed with
native child jobs and Git pushes, covering successful publication and receive-pack
rejection. An additional native case confirms that a registry conflict stops
child submission. Only registration is mocked in the two publication cases because the
local harness pre-registers and authorizes its seeded destination repositories.
The root ownership guard and three review rejection/cancellation cases also passed
again. The new expectations are in
[cell-registration-statements.md](../recipe-tests/cell-registration-statements.md).

Full creation regression under named cells remains unvalidated: legacy creation
fixtures conflate names and repository locators. Existing root configuration
integration remains unchanged. No production jobs were restarted and no production
registry, repository, or dependency configuration was published during validation.

Acceptance statements are in
[named-cells-statements.md](../recipe-tests/adaptive/named-cells-statements.md).

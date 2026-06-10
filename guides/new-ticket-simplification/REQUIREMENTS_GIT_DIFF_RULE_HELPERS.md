# Requirements: Git Diff Rule Helpers

## Status

Draft requirements for c2j recipe policy checks.

## Motivation

C2 workflows rely on cell ownership and phase boundaries. Recipes need to prove
that changes stayed in the current cell, planning stages did not modify source
code, and implementation stages did not edit protected artifacts such as
`.c2/tests/*.md` unless explicitly routed through outcome determination.

Today those checks are usually expressed as shell commands or left to reviewer
instructions. They should be deterministic recipe rule helpers.

## Goals

- Provide stable predicates for common git diff policy checks.
- Make cell-boundary enforcement easier to author and test.
- Support `rule_gate` without embedding shell scripts.
- Keep changed path details visible in job stories.

## Non-Goals

- Do not replace human code review.
- Do not infer semantic compatibility from file paths alone.
- Do not mutate git state.
- Do not bypass normal c2 git persistence.

## Requirement 1: Changed Path Inspection

c2j should expose a helper or rule type that returns changed paths for the
current recipe git state.

Required helper shape:

```cel
git_changed_paths(base, head)
```

Required rule shape:

```yaml
- id: current_cell_only
  type: git_diff_paths
  severity: blocking
  base: "${{ context.git.base_hash }}"
  head: "${{ context.git.hash }}"
  allow:
    - "**"
  deny:
    - "../**"
```

The exact base/head defaults should be documented. If omitted, the helper should
compare the current op or job git state against the locked base for the current
cell.

## Requirement 2: Path Allow And Deny Rules

`git_diff_paths` should support:

- `allow` glob patterns;
- `deny` glob patterns;
- `require_changed` boolean;
- `allow_deleted` boolean;
- `allow_renamed` boolean.

Deny patterns should win over allow patterns.

The rule result should include matched paths and the pattern that matched.

## Requirement 3: Phase Boundary Checks

The helper should support common phase policies:

- planning may edit only `.c2/tests/*.md` and outbox artifacts;
- implementation may not edit `.c2/tests/*.md`;
- merge candidates must stay inside the current cell;
- generated artifacts should not be committed unless explicitly allowed.

These policies may be built-in named presets or documented examples using
`git_diff_paths`.

Example:

```yaml
- id: implementation_did_not_edit_test_statements
  type: git_diff_paths
  severity: blocking
  deny:
    - ".c2/tests/*.md"
  message: "Implementation must request test statement updates instead of editing them directly."
```

## Requirement 4: Cell Boundary Awareness

When c2j knows the current cell root, git diff helpers should support a
`current_cell_only` mode.

Example:

```yaml
- id: changed_paths_in_current_cell
  type: git_diff_paths
  preset: current_cell_only
  severity: blocking
```

If c2j cannot determine the cell root, the rule should fail with a clear error
unless the recipe provides explicit allow patterns.

## Requirement 5: Rename And Delete Reporting

The output should preserve change kind:

```json
{
  "path": "new/path.txt",
  "old_path": "old/path.txt",
  "change": "renamed"
}
```

Recommended change kinds:

- `added`;
- `modified`;
- `deleted`;
- `renamed`;
- `copied`;
- `type_changed`.

## Requirement 6: Job Story And Diagnostics

The job story should show:

- base and head used for the diff;
- changed path count;
- allowed paths;
- denied paths;
- matching pattern details;
- preset name, when used.

Diagnostics should distinguish "no git base available" from "paths violated the
rule."

## Requirement 7: Recipe Testing

Recipe tests should be able to mock changed path lists without requiring real
git commits.

Tests should be able to assert:

- allowed path pass;
- denied path failure;
- current-cell-only failure;
- rename handling;
- no-change handling when `require_changed=true`.

## Efficiency Examples

### Example 1: Block Test Statement Edits During Implementation

Before:

```yaml
check_test_statement_edits:
  op: command_execution
  inputs:
    run: |
      set -euo pipefail
      if git diff --name-only "$BASE" "$HEAD" | grep -E '^\.c2/tests/.*\.md$'; then
        echo "Implementation edited test statements directly" >&2
        exit 1
      fi
```

After:

```yaml
final_gate:
  op: rule_gate
  inputs:
    rules:
      - id: implementation_did_not_edit_test_statements
        type: git_diff_paths
        severity: blocking
        deny:
          - ".c2/tests/*.md"
        message: "Implementation must request test statement updates instead."
```

Efficiency gain: the policy is declarative, testable without real git commands,
and emits the exact offending path in structured output.

### Example 2: Current Cell Boundary

Before:

```yaml
check_cell_boundary:
  op: command_execution
  inputs:
    run: |
      set -euo pipefail
      c2j self --json > self.json
      git diff --name-only "$BASE" "$HEAD" > changed.txt
      python3 scripts/check_changed_paths_in_cell.py self.json changed.txt
```

After:

```yaml
final_gate:
  op: rule_gate
  inputs:
    rules:
      - id: changed_paths_in_current_cell
        type: git_diff_paths
        preset: current_cell_only
        severity: blocking
```

Efficiency gain: every recipe can reuse the same cell-boundary predicate and
job-story diagnostics instead of carrying custom scripts.

## Acceptance Criteria

- A final gate can block merge when changed files are outside the current cell.
- An implementation gate can block direct `.c2/tests/*.md` edits.
- Rule output identifies the exact path and pattern that caused failure.
- Recipe tests can validate path policies without running git commands.

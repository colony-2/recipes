# Selected documents for repair and review

Job `3Lft2gScFyph0OzbvTooal1tMmv` produced 1,285 artifacts, including 1,200
validation files. Repair promoted the entire inventory into review documents.
Chapter 60 reached 485,026 bytes against a 262,144-byte limit; document references
accounted for 479,178 bytes. Contents were already in artifact storage.

## Change

`adaptive/artifact-result.yaml` now exports a separate `documents` map containing
only successfully resolved response references. Build repair, consultation repair,
failed consultations, and assessment/review publication use this selected map.
They no longer promote every output artifact into an inbox or human review.

The complete reference inventory remains available internally for correcting a
missing or mistyped response declaration. This matters when an agent produces a
file but forgets to list it, then corrects only the response in the next turn.
Retaining its original identity avoids forcing it to republish the file. This
inventory is not bound into the repair inbox or used as the review document list.
Original files remain stored on their producing task.

The per-turn prompt now says outbox is for intentional deliverables and relevant
supporting evidence. Source downloads, dependencies, build trees and temporary
validation work belong in scratch space outside outbox. Detailed evidence remains
individually accessible; a large set should have a concise index with links.
Archives are not the default. Large explanations/logs belong in files, with short
response summaries. The guidance applies to resumed as well as new sessions.

No document contents, JSON, artifact identities, or evidence lists are silently
truncated. This change does not impose an arbitrary first-N selection. An agent
that explicitly declares thousands of deliverables can still exceed a downstream
payload limit; selection addresses the observed accidental inventory promotion.

## Validation

- Three native regressions produce 1,300 incidental files and exercise selection,
  response-repair review, preserved stored identity, and direct reading of an
  unselected original artifact. Missing and ambiguous declarations stay errors.
- The adaptive regression suite passed all 171 cases across 28 suites, including
  consultation correction that reuses an originally undeclared file.
- The shared-prompt regression checks the new outbox/evidence guidance.

The broad regression used an isolated copy with Nix provisioning omitted and
selector operations expanded to extension operations. Model responses were mocked;
commands, Git operations, artifacts and human-response handling were native. The
three large-inventory cases also passed directly against the source recipes.

The correction is local and uncommitted. Existing remote jobs were not resumed or
modified. Runtime limits on raw operation artifact inventories remain c2j-owned.

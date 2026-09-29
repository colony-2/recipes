# Cell mandate specification

Status: repository authoring convention, version `c2.cell-mandate/v1`.
The mandate file and instruction links can be adopted now. Structured assessment
gates described here still require implementation in build/evolve and c2j tools.

## Canonical location and discovery

Every cell keeps one authoritative mandate at **`.c2j/mandate.md`**, relative to
its repository root. Use this exact lowercase filename. It does not move with
the recipe's `target_directory`: build and evolve consult the same cell mandate.

Root `AGENTS.md` must link to the mandate and instruct agents to read it before
design or ownership assessment. Nested instruction files may specialize working
practices but do not override the mandate. Cell catalogs and descriptions are
discovery indexes, not additional authoritative copies.

Resolve the cell's identity and repository through c2j configuration. Do not
derive identity from a title in the document or require it to duplicate config.
Consultations read the mandate from the same pinned commit as the consulted
source. Record that commit and SHA-256 of the exact file bytes in assessments.

If the file is missing, malformed, or conflicts with applicable ownership
instructions, report `needs_clarification`. Existing purpose text can inform a
draft mandate but is not an automatic substitute for an accepted mandate.

## Document format

The file is Markdown with this YAML front matter:

```yaml
---
schema: c2.cell-mandate/v1
---
```

Use one title and these required level-two headings:

| Heading | Content |
|---|---|
| `Purpose` | A short statement of the outcomes the cell exists to provide |
| `Owns` | Responsibilities, each a list item beginning with `OWN-NN:` |
| `Does not own` | Exclusions, each beginning with `EXCLUDE-NN:` |
| `Interfaces` | Public boundaries and dependencies, each beginning with `INTERFACE-NN:` |
| `Boundary examples` | At least one example each labelled `fits`, `partial`, and `outside` |
| `Changing the mandate` | The responsible decision maker and acceptance procedure |

`NN` is a positive integer written with at least two digits. Identifiers are
unique within the file, remain stable when wording is clarified, and must not
be reused for a different responsibility. Removed identifiers are retired.
`Owns` must contain at least one responsibility. Empty exclusion or interface
lists must explicitly say `None currently declared`; absence of an exclusion
does not grant ownership of everything else.

Write responsibilities in outcome language. Include the important things the
cell deliberately does not do. Implementation details and test commands belong
in `AGENTS.md` or supporting documentation, not in the mandate unless they define
an actual ownership boundary.

See [this repository's mandate](../.c2j/mandate.md) for a complete example.

## Design assessment contract

Assess the requested outcomes against the mandate before committing to a local
implementation plan. Preserve stable outcome IDs through request decomposition.
There are exactly three fit verdicts:

| `fit` | Meaning |
|---|---|
| `fits` | Every requested outcome belongs to the assessed cell |
| `partial` | At least one requested outcome belongs here and at least one does not |
| `outside` | No requested outcome belongs to the assessed cell |

Clarification is an assessment state, not a fourth fit verdict. If ownership
cannot yet be determined, set `assessment_status` to `needs_clarification`, set
`fit` to null, and provide questions. Do not turn uncertainty into rejection.
A known external outcome may still have an unknown target owner without making
the current cell's `partial` or `outside` verdict uncertain.

Proposed artifact: `mandate-assessment.json`, validated before its design is
accepted. This example illustrates a partial request:

```json
{
  "version": "c2.mandate-assessment/v1",
  "request_id": "pagination",
  "request_revision": "<request-content-hash>",
  "cell": "github.com/example/client",
  "mandate": {
    "path": ".c2j/mandate.md",
    "commit": "<consulted-commit>",
    "sha256": "<mandate-content-hash>"
  },
  "assessment_status": "assessed",
  "fit": "partial",
  "rationale": "Client iteration belongs here; server token generation does not.",
  "outcomes": [
    {
      "id": "R1",
      "statement": "Clients can iterate through all result pages.",
      "ownership": "local",
      "suggested_owner": "github.com/example/client",
      "mandate_evidence": ["OWN-01"],
      "reason": "The cell owns the client API."
    },
    {
      "id": "R2",
      "statement": "The server provides stable continuation tokens.",
      "ownership": "external",
      "suggested_owner": "github.com/example/server",
      "mandate_evidence": ["EXCLUDE-01"],
      "reason": "The cell does not own server behavior."
    }
  ],
  "questions": [],
  "consultations": []
}
```

Validation rules for the proposed gate:

- Require the version, request identity/revision, cell, mandate provenance,
  status, fit, rationale, outcomes, questions, and consultation references.
  A missing mandate has null commit/hash as appropriate and requires clarification;
  the gate must allow this diagnostic result without allowing implementation.
- Every requested outcome appears exactly once; additions, removals, or splits
  require an explicit request revision or decomposition mapping.
- `ownership` is `local`, `external`, or `unresolved`. An assessed result has no
  unresolved outcomes. Its fit verdict must match the counts of local/external
  outcomes and the outcomes list must not be empty.
- `suggested_owner` is a canonical cell identity or null. A local outcome names
  the assessed cell. An external outcome may leave its owner unknown.
- Require a reason and cite applicable responsibility/exclusion identifiers.
  A boundary gap can cite the mandate's Purpose or Owns section with an explicit
  explanation; do not invent a clause to satisfy validation.
- Require nonempty questions for `needs_clarification`; assessed results have
  no unresolved ownership questions. Other design questions remain in the design.
- A schema gate checks structure and consistency. Independent design review
  checks whether the ownership judgment is justified by the actual mandate.

`partial` requires a complete allocation of local and external outcomes in the
design, including unknown owners and necessary interface decisions. Approval
must not silently omit the external portion. Only local work enters this cell's
implementation phase; actual external changes become work for their owner.

Supporting dependencies discovered during design are distinct from the original
requested outcomes. A wholly local feature can need external supporting work
without retroactively changing the ownership of the original request.

`outside` produces a routing/rejection explanation and possible owner or
boundary-change proposal. It must not report an implementation success.
Mandate fit does not establish feasibility, value, or design quality; those are
separate parts of design review.

## Evolution and adoption

Read the accepted mandate at the start of a job and record its revision. An
evolve job can propose a mandate change, but cannot use its unaccepted edits
to authorize additional implementation scope in that same job. Follow the
document's decision procedure and reassess affected work after acceptance.

If ownership changes while work is running, identify the change and revalidate
the approved scope before integration. A consultation carried into another job
is context, not a waiver of that job's current mandate assessment.

For existing cells, derive a first draft from their purpose and established
ownership, have the responsible maintainer accept it, then add the AGENTS link.
Do not infer new ownership from files merely happening to live in a repository.

# Document titles, purpose and reading priority

Adaptive3 producers return `document_details` alongside `primary` and the overall
review `title`. Every selected `review/` attachment has exactly one descriptor:

```yaml
document_details:
- document_id: review/decision.md
  title: Keep unsent drafts after reopening the browser
  description: Review the saving behavior, limits and evidence before approving it.
  role: primary
  order: 10
- document_id: review/checks.md
  title: Draft recovery checks
  description: Inspect the positive and failure cases supporting this decision.
  role: supporting
  order: 0
primary: review/decision.md
```

Use exact attachment IDs, including images and proposed configuration files.
Titles contain 1–120 Unicode code points; purposes contain 1–300. Both must be
nonblank valid Unicode without U+0000–U+001F or U+007F controls. Roles are primary,
supporting or diagnostic; order is an integer from 0 to 1000000. Equal orders
are allowed. A nonempty collection has one primary matching its overview.
An empty collection uses `document_details: []` and `primary: null`.

Roles group documents by reading importance, followed by order within each group.
They grant no authority. The overall review title is separate, with its existing
100-character limit. Native combined presentation must fit 65536 compact Go JSON
bytes, including keys, overview and escaping. Shorten purposes and deliberately
select a focused collection when needed; do not truncate or silently drop evidence.

The existing file check validates details against the exact selected keys before
exporting native `document_metadata`. The independent validator checks whether
titles and purposes describe the actual files usefully. Any finding returns through
the ordinary full correction cycle; its finite allowance and Backstop remain.
No annotation history, title extraction or separate repair stage is involved.

Emitting any `review/` files replaces the collection; describe that complete
replacement. Emitting none reuses the incoming collection; describe every selected
file again. Removed descriptors are never merged back in. Changed contents receive
full validation even when their IDs stay the same. Question replies preserve the
checked collection, metadata and overview. Human uploads remain feedback until
explicitly selected by a producer.

Package proposals and document-bearing Backstop/recovery questions use the same
check. Package proposals keep `review/README.md` as primary. A failed Backstop
preparation shows a document-free question with findings and hides Apply until
the collection is readable and a concrete action is available. The checked summary
includes that action. Diagnosis and settings discussion do not authorize stage work.
Provider failure still permits model/settings input. Native integration of
an already accepted candidate retains file checks without a new producer turn.

New/custom producers must return the required array. Recorded forms and jobs
using older recipes retain their behavior. c2j v0.0.117 or later compatible support
is required for executing workers and form-serving integrations. Cortex owns
role ordering and fallback selection; source support alone does not prove fleet
versions. No runtime release, migration or deployment is part of this correction.

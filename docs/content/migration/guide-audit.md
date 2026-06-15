---
title: "Guide Audit"
weight: 91
---

Every existing `guides/` file has an audit record in `docs/data/guide-audit.yaml`.

Disposition meanings:

- `migrate`: behavior is current and belongs in the reference.
- `partial`: useful sections migrate after commands/examples are updated.
- `pattern-only`: keep as design guidance, not API reference.
- `historical`: keep out of the reference except as background.
- `bug-report`: do not migrate as authoring guidance.
- `obsolete`: superseded by current `c2j` behavior.

Check audit completeness:

```bash
docs/scripts/audit-guides.sh
```

The audit intentionally separates implemented behavior from requirements, proposals, and bug reports. Reference pages should cite validated examples or current `c2j`/`c2ops` source behavior before carrying old guide content forward.


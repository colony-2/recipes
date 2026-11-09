# Recover saved drafts through bounded storage history

## Parent problem and question

Notebook users need to restore an earlier draft after an accidental overwrite, including after closing the browser or switching devices. The request asks storage to assess existing alternatives and the smallest compatible change, with direction only and a storage-authored, typed handoff if necessary.

## Recommendation and reasons

Storage agrees a **feature** boundary: retain a bounded, durable history of successful saves per draft and expose a history read. Restore a chosen snapshot through the existing version-checked `PUT /drafts/{id}`. The [storage handoff](work/handoff.md) defines proposed behavior, compatibility, acceptance, and required inputs. No implementation was performed.

The existing API already supports frequent saves and rejects stale versions, but it cannot retrieve overwritten text. The supplied implementation keeps only the latest `{text, version}` in a process-local dictionary. Its version number is a concurrency token, not a retrievable revision history. See [evidence](evidence.md) and the passing [local checks](evidence/checks.txt).

Recommend keeping **three previous successful versions plus the current draft**, pending confirmation of what “last three” means. This supplies three actual restore choices after an overwrite and bounds raw stored text at 256 KiB per draft under the existing 64 KiB limit. If the requirement instead means three saved versions total, retain two previous versions plus current, bounded at 192 KiB. This choice is explicit and unresolved; it is not a hidden expansion of the requirement.

## Alternatives and tradeoffs

| Alternative | Assessment |
| --- | --- |
| Existing GET/PUT alone | Suitable for current saves and conflicts. No history read or retained old text; insufficient for recovery. |
| Browser undo or local draft cache | May help unsent edits on one browser, but cannot establish shared recovery from another device. Notebook owns this separate concern. |
| Backups or database revision features | Could supply an implementation primitive if the deployed backend has them. None is evidenced here; operational backup restore is not an existing per-draft recovery API. |
| Client writes extra draft IDs for snapshots | Existing clients would bypass capture; head update, snapshot creation, pruning, and access rules would lack a shared atomic contract. Prefer capture inside storage's existing write path. |
| New autosave or dedicated restore endpoint | Unnecessary for the bounded proposal. Existing PUT already accepts text with a version precondition. |
| Full audit log, merge engine, idempotency system, larger draft limit | Additional capabilities outside this feature. Reconsider only if review changes the requirement. |

## Agreed work by owner

- **Storage — feature:** durable bounded history, additive history read, atomic version-checked writes and retention, compatibility documentation, and checks specified in [handoff.md](work/handoff.md). Restore creates a new version through PUT and never rewinds the head version.
- **Notebook — separate ownership, no agreement authored here:** presenting history, choosing and confirming restoration, retaining unsaved text, save scheduling, and handling conflicts. The coordinator should obtain notebook's own handoff for that work. This consultation does not assign its UI implementation.

## Remaining open issues

[Review choices](review-choices.md) preserves the counting ambiguity, repeated saves, empty drafts, retention, conflicts, large drafts, and older API clients, with recommendations and consequences. Agreement covers storage's feature boundary; it does not stand in for human selection of the unresolved product semantics.

The actual durable store, HTTP adapter, draft identity/access mapping, and deployed connection are not supplied. The repository is explicitly a pure contract model. Durable cross-device recovery must be demonstrated against the real backing service before release; passing model tests alone is insufficient. Pre-rollout overwritten content cannot be recovered from this model.

The inbox was empty. `c2j self` and `c2j cells` failed with `Error: requires .c2/config.yaml`, so no deployment routes or related-cell metadata were available. No configuration was fabricated, and these optional discovery failures do not block this evidence-based consultation.

# notebook and storage: Determine whether the existing draft API safely supports autosave, including concurrent tabs, lost responses, conflicts, and size limits. Recommend whether any storage change is necessary; provide source-backed findings for notebook's direction review. Advisory only; no implementation.

Status: agreed

## notebook — requester

Determine whether the existing draft API safely supports autosave, including concurrent tabs, lost responses, conflicts, and size limits. Recommend whether any storage change is necessary; provide source-backed findings for notebook's direction review. Advisory only; no implementation.

- [notebook-index.html](notebook-index.html)
- [notebook-purpose.md](notebook-purpose.md)
- [notebook-readme.md](notebook-readme.md)
- [request.md](request.md)
- [user-request.md](user-request.md)

## storage — consultant

Reuse GET/PUT; no autosave endpoint is needed. However, overlapping writes reproduced a model bug: both can succeed at the same version and silently overwrite text. Storage’s atomicity fix is scoped for after direction approval; deployed request serialization remains unverified. Findings cover lost-response reconciliation, conflict recovery, and the inclusive 65,536-byte UTF-8 limit. No repository implementation changed.

- [iter1/consultant/evidence/baseline-tests.txt](iter1/consultant/evidence/baseline-tests.txt)
- [iter1/consultant/evidence/probe-output.txt](iter1/consultant/evidence/probe-output.txt)
- [iter1/consultant/evidence/probe.py](iter1/consultant/evidence/probe.py)
- [iter1/consultant/evidence/sources.md](iter1/consultant/evidence/sources.md)
- [iter1/consultant/findings.md](iter1/consultant/findings.md)
- [iter1/consultant/summary.md](iter1/consultant/summary.md)
- [iter1/consultant/work/handoff.md](iter1/consultant/work/handoff.md)

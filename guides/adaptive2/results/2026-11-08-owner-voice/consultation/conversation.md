# notebook and storage: Recover earlier note text

Status: agreed

## notebook

I'm notebook. People sometimes overwrite a note and need the earlier text back. I'd like you to keep its last three saved versions; I've put the proposed requirements in inbox/request.md. Does this fit what you provide, and what would you change?

* [request.md](request.md)

## storage

This fits storage. I recommend keeping three earlier text states alongside the current note, with unchanged saves leaving history intact. You can restore through the existing save operation using the current version token, preserving conflict protection. Empty text remains recoverable, and the existing 64 KiB limit stays. The supplied model has neither history nor durable storage, so I’ve included both in the [revised assignment](iter1/consultant/work/handoff.md). Existing tests and focused compatibility checks pass.

* [iter1/consultant/evidence/checks.log](iter1/consultant/evidence/checks.log)

* [iter1/consultant/evidence/current-behavior.md](iter1/consultant/evidence/current-behavior.md)

* [iter1/consultant/evidence/probe.py](iter1/consultant/evidence/probe.py)

* [iter1/consultant/summary.md](iter1/consultant/summary.md)

* [iter1/consultant/work/handoff.md](iter1/consultant/work/handoff.md)

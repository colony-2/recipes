# Notebook history consultation

This trial used real agents in disposable notebook and storage repositories.
The requester was the fixture's `root` cell, whose purpose was notebook UI.
The receiver ran in the storage workspace. No delivery job was requested.

## Request

> Our notebook needs users to recover old saves. Can you add a new restore endpoint and keep five versions, including every autosave?

## Storage response

I can do this, but the documented APIs already support recovering retained text through the existing version-checked PUT. I propose a feature to retain five distinct versions, including current, without adding a restore endpoint. Unlike counting every autosave event, identical autosaves would remain no-ops. Every changed autosave would consume a slot, so five versions offer limited recovery depth. These counting semantics need product agreement; notebook owns the recovery UI.

Read the [receiver's proposal](review/five-version-recovery-proposal.md).

## Assignment written by the receiver

Increase storage retention from three to five distinct saved versions, including current. Count each content-changing autosave; preserve identical-save no-ops and stale-writer rejection. Verify retention and save semantics. Reuse the existing history GET and version-checked PUT for recovery. Notebook owns the recovery UI. Confirm agreement on counting distinct versions before delivery.

## Independent review

The advice meets the assignment and matches README.md and storage.js. It proposes a feature retaining five total distinct versions, reuses version-checked PUT for recovery, and identifies notebook’s UI dependency. It explicitly explains that identical autosaves would remain no-ops, departing from counting every autosave event. Documented API behavior is correctly distinguished from verified code. No corrections needed; human agreement on the proposed semantics remains pending.

## Trial outcome

Execute, full Validate and independent Review passed. All three live agent
responses passed their output schemas without repair attempts. Advice acceptance
means the receiver's proposal is ready to return to the requester; the proposed
counting semantics still need agreement in the parent's direction review.

Source: `consultation.live.yaml`, case `receiver-challenges-new-api`, run on
2026-11-13 with c2j `c244db82949ea989cd90d4352325b40b88cca5d0`, disposable job
`3M1zkCO3CVaLPcPQ5D6wS8K7XDZ`. The proposal and responses are actual agent outputs,
without editing. An earlier trial hit model capacity during final Review; this
completed retry used the same configured provider.

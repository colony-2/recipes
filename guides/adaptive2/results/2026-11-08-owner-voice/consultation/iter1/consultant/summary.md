# Recover earlier note text

I recommend keeping the current note plus three earlier saved text states and restoring through our existing save operation. This fits storage's responsibility. You keep version selection and preview in notebook; I would provide bounded history and the persistence needed to read it from another browser or device. My [revised assignment](work/handoff.md) defines the work.

The main changes to your proposal are:

- **Three earlier states, in addition to the current one.** Consecutive saves of unchanged text should not use history slots. They will still advance the current version, preserving the existing contract. Explicitly saved empty text remains recoverable.
- **Use the existing save operation for restore.** Submit the selected text with the version of the current note your editor last read or saved. A historical version identifies the snapshot; it is not the token for overwriting the current note. An intervening edit must produce a conflict.
- **Store current text and history durably together.** The supplied implementation is an in-memory model with no history. It does not establish durable recovery. The assignment includes persistence and documents the serving configuration needed for browser/device recovery.

I would keep the existing 64 KiB UTF-8 limit for each saved text and retain only successful server saves. Unsent browser text remains notebook's responsibility. The [code findings and local checks](evidence/current-behavior.md) support these defaults.

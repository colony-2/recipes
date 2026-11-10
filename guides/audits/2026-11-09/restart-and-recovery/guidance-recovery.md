# Carry the latest human guidance into a fresh Cortex attempt

Job `3LsmZNUoxBXwnTcoJKekMAZagiX` captured recipes `1c7cdc7`, before the
feedback-priority fix in `1006fc4`. At inspection it was waiting for direction
review. Its latest consultation withdrew a separate reader interface and proposed
exposing an existing checkpoint type instead. That remaining proposal needs to be
judged against the user's request to use existing durable records and inspection.

These commands were provided to the user, not executed by this investigation.
The fresh submission creates a new goal and loads the published recipe on main.
Its latest prior direction decision was revise, so recovery does not reuse an
older conflicting approval.

```sh
# Cancel the old attempt so it cannot continue in parallel.
# Keep its history, feedback and artifacts accessible for recovery.
c2j delete --jobdb http://192.168.1.195:9047/c2 \
  --job-id 3LsmZNUoxBXwnTcoJKekMAZagiX

# Load the current recipe and explicitly prioritize the latest human guidance.
# Inspect retained work, rewrite the one-pager, and return for direction review.
c2j submit --jobdb http://192.168.1.195:9047/c2 --cell cortex \
  --title "Finish Cortex conversations using existing durable job records" \
  --inputs-json '{"resume_from":"3LsmZNUoxBXwnTcoJKekMAZagiX"}' \
  'Continue the work from 3LsmZNUoxBXwnTcoJKekMAZagiX. Read its original request, latest human feedback, consultation replies, and retained work. My latest guidance supersedes earlier proposals: JobDB already durably retains reviews, responses, and execution state, and c2j already provides history inspection. Inspect and use those capabilities before proposing new storage, retention guarantees, or reader interfaces. Explain any remaining gap through a concrete operation that existing APIs cannot perform. Reassess the proposed checkpoint-type export on that basis. Rewrite the one-pager around these findings and return it for review; do not carry earlier approval over conflicting scope.'
```

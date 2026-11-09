# Earlier attempts and what they revealed

The files in [import-last-note-partial](import-last-note-partial/one-pager.md)
are the first live bug framing, retained unchanged. Its supporting evidence was
not exported before the disposable runtime was cleaned up, so the evidence links
in that early document are incomplete. Use the final packet linked from the
[review index](../README.md) for a complete review.

Other attempts:

- The first feature run timed out after 15 minutes, after storage explained that
  its existing API could support autosave. It did not produce a completed review.
- The first receiver run wrote a handoff but omitted the directory's trailing
  slash. Recipe validation rejected it. Misleading repair text prompted an
  unnecessary correction loop and a human question. The recipe now accepts both
  spellings and reports the actual validation error.
- A subsequent diagnostic rewrite had a c2j scope error. Native tests caught it;
  the corrected suite and final live runs use explicit node inputs.
- Early bug captures kept the one-pager but not all supporting file bodies. The
  live wrapper now materializes the selected packet before fixture cleanup.

The original [receiver summary alias](receiver-presentation/summary.md) and
[conversation heading](receiver-presentation/conversation.md) are also retained.
The alias changed the base directory for relative links; the heading repeated the
whole request. The recipe now emits a short index linking the unchanged source
summary, and uses its descriptive heading for the conversation. A native replay
of the recorded live response verified the correction. Links in these old
presentation files may be incomplete; use the final receiver packet.

Raw reports remain in local `/tmp/adaptive2-*` directories. These attempts are
not counted as successful complete packets. No generated document has been
edited into a better-looking example.

The final feature trial also hit its 30-minute deadline after drafting the UI
packet, without returning a final response. See the main index for that incomplete
result. Its unselected [outer summary alias](draft-saving-outer-summary.md) is
retained here unchanged; the draft one-pager links the canonical inner summary.

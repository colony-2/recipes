# Operational outcome test statements

- O1 [Critical] [integration] [recipes/adaptive/develop.yaml] [c2j] An explicit failure ends the attempt immediately, preserving its explanation and selected evidence without a human question.
- O2 [Critical] [integration] [recipes/adaptive/develop.yaml] [c2j] Rewording consecutive blockers without candidate progress cannot grant additional recovery turns.
- O3 [Critical] [integration] [recipes/adaptive/develop.yaml] [c2j] Successful intervening work and changed candidates can continue recovery without an artificial global turn limit.
- O4 [Critical] [integration] [recipes/adaptive/operational-failure.yaml] [c2j] Failure export preserves an existing recovery document byte-for-byte and reports the original failure without an artifact collision.
- O5 [Critical] [integration] [recipes/adaptive/coordinate.yaml] [c2j] A child can retrieve a required parent artifact using task credentials without submission permission or copying unrelated files.
- O6 [Critical] [integration] [recipes/adaptive/coordinate.yaml] [c2j, Git] Selected unpublished work can be inspected and applied in a fresh child's managed workspace without publishing or changing the parent's checkout.
- O7 [High] [integration] [recipes/adaptive/develop.yaml] [c2j] An investigation meeting its own acceptance statements can finish with documented unavailability while leaving the parent's broader outcome unresolved.
- O8 [Critical] [integration] [recipes/response-schemas.yaml] [c2j, jsonschema] The agent response schema accepts explicit failure and still rejects invalid response fields.
- O9 [Critical] [integration] [recipes/adaptive/develop.yaml] [c2j] Repeated negative assessments of an unchanged candidate enter bounded recovery even when the assessor rephrases its findings.

Scripted responses validate routing and preservation, not model judgment. Existing
package, review, expectation-protection, handoff, and recovery-progress cases
remain regression coverage for the associated prompt changes.

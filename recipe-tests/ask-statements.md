# Question recipe acceptance statements and candidate checks

These statements were defined before implementation. They expand the accepted proposal and use the [recipe contract](../guides/ASK_RECIPE.md). Expectations remain distinct from executed test results.

## Test statements

| ID | Expectation | Priority | Level / dependencies | Files |
| --- | --- | --- | --- | --- |
| ASK-01 | A question without documents opens a review v2 form with its exact title, question and default reply choice. | Critical | Integration / pinned c2j, Nix, Python | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-02 | Replies preserve exact Unicode, whitespace, quotes and long text, together with the native human receipt and original question. | Critical | Integration / pinned c2j, Nix, Python | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-03 | Affirmative, negative and other replies complete the question while preserving their distinct choices without claiming deployment or approval. | Critical | Integration / pinned c2j, Nix, Python | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-04 | Missing, mistyped or blank required inputs fail with useful feedback before any human input request opens. | Critical | Integration / pinned c2j | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-05 | Empty choices, duplicate choice identifiers, invalid feedback rules and continuing choices fail before any human input request opens. | Critical | Integration / pinned c2j, Nix, Python | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-06 | Empty or whitespace-only required replies are rejected; existing attached documents do not satisfy the required contribution. | Critical | Integration / pinned c2j, Nix, Python, stored artifacts | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-07 | A new stored upload can satisfy a required reply only when that choice permits uploads. | Critical | Integration / pinned c2j, Nix, Python, stored artifacts | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-08 | Confirmation choices forbidding feedback reject text and uploads, and unknown choices or settings are rejected. | Critical | Integration / pinned c2j, Nix, Python | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-09 | Invalid document references, unattached overview identifiers and unresolved reply uploads cannot produce a valid answer. | Critical | Integration / pinned c2j, Nix, Python, stored artifacts | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-10 | Selected document metadata and producer identities survive presentation; originals and same-named reply files remain separately retrievable with unchanged bytes. | High | Integration / pinned c2j, Nix, Python, stored artifacts | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-11 | Asking a question leaves the application repository unchanged and invokes no model, deployment, package-installation or Git publication operation. | Critical | Integration / pinned c2j, Nix, Python, Git | `ask.yaml`, `recipe-tests/ask.test.yaml` |
| ASK-12 | A foreign consumer resolves the question recipe and its form builder from the selected Recipes source without copying helpers into its repository. | Critical | Integration / pinned c2j, Nix, Python, isolated Git repositories | `ask.yaml`, `recipe-tests/ask-source.test.yaml` |
| ASK-13 | An unanswered question remains pending; resuming the same job preserves its request identity without opening a duplicate question. | Critical | Integration / pinned c2j, SQLite, separate runner invocations | `ask.yaml`, `recipe-tests/checks/ask_resumption.py` |
| ASK-14 | Resuming after an accepted reply preserves its original response, receipt and uploaded bytes, matching an uninterrupted control. | Critical | Integration / pinned c2j, SQLite, separate runner invocations, stored artifacts | `ask.yaml`, `recipe-tests/checks/ask_resumption.py` |
| ASK-15 | Adaptive waits for the recorded question child and resumes with its actual job identity, terminal status and retrievable original reply. | Critical | Integration / pinned c2j, Nix, scripted agent, native child input | `recipes/adaptive3/cycle.yaml`, `recipes/adaptive3/children.yaml`, `recipe-tests/adaptive3/ask.test.yaml` |
| ASK-16 | Failed or cancelled question children return their actual outcomes to Adaptive without reporting affirmative confirmation or starting a replacement question automatically. | Critical | Integration / pinned c2j, Nix, native cancellation controls, scripted agent | `recipes/adaptive3/children.yaml`, `recipe-tests/adaptive3/ask.test.yaml` |
| ASK-17 | Question submission and reply retrieval remain usable when Adaptive forwards only a short child summary. | High | Integration / pinned c2j, Nix, scripted agent, stored artifacts | `recipes/adaptive3/prompts/context.yaml`, `recipe-tests/adaptive3/ask.test.yaml` |
| ASK-18 | Agents request required manual publication confirmation after source delivery succeeds and before using the unavailable deployment in a dependent check. | High | Integration / sampled Adaptive execution, manual-publication fixture | `recipes/adaptive3/prompts/context.yaml`, `guides/ASK_RECIPE.md` |
| ASK-19 | Git-only and already established automated publication outcomes do not require another human confirmation; optional deployment does not delay source acceptance. | High | Integration / sampled Adaptive execution, Git and automated-publication fixtures | `recipes/adaptive3/prompts/context.yaml`, `guides/ASK_RECIPE.md` |
| ASK-20 | Unavailable or ambiguous replies leave the deployment dependency unresolved; only confirmation applicable to the requested version and environment permits the dependent check. | Critical | Integration / sampled Adaptive execution, manual-publication fixture | `recipes/adaptive3/prompts/context.yaml`, `guides/ASK_RECIPE.md` |

## Checks

`ask.test.yaml` exercises the actual entrypoint, builder and native response gate.
`ask-source.test.yaml` submits the candidate through a separate Git recipe source
from a consumer without helper files. `adaptive3/ask.test.yaml` checks the containing
lifecycle with scripted author decisions and actual question input.

`checks/ask_resumption.py` and its bounded client in `fixtures/ask/native.go` cover
ASK-06–10 and ASK-13–14 using real stored files, an isolated SQLite database and
separate runner processes. They also check the actual Adaptive child collector's
file forwarding and cancellation behavior for ASK-15–17. The pinned prepared-op
cancellation control requires the suite's root job to be cancelled; it cannot
validate a cancelled child with a successful parent. The bounded client instead
cancels the pending child through the native API, then resumes the collector.

The shared verification script runs this driver using its existing Go toolchain.
It builds against the exact immutable c2j source pin; it changes no runtime code.
ASK-18–20 require live agent observation. Scripted routing checks and inspection
of installed instructions do not establish those judgment expectations.

`checks/ask_agent_acceptance.py` generates six isolated live Adaptive cases using
`adaptive3/ask-live.yaml`. Source delivery and human replies are controlled;
author and assessor operations remain live. Cases cover affirmative, unavailable
and ambiguous replies, automated publication, Git-only consumption and optional
deployment. The checker compares real child results, author resumption order,
native question receipts and executable check timestamps. It rejects a check
before source success or confirmation and preserves the exact installed prompt.
The shared verify script validates these declarations without making model calls.
The question count measures opened native prompts. A failed declaration may be
corrected after its terminal result is consumed; the checker retains that failure
and rejects overlapping, unanswered or extra answered attempts.
See the native testing guide for the separate credentialed execution route.
The containing lifecycle also checks that agents receive the absolute question
guide URL and the instruction to ask after completed source work leaves a
non-Git dependency without an observed update. The original expectations stand.

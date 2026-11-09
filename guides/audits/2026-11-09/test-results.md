# November 9 implementation test results

The native suites and focused reruns pass. The live UI trial delivers an actual
phone screenshot in the final review packet; three live limit trials produce
readable decisions. See the unchanged [review examples](results/README.md) and
the [assessment against the plan](implementation.md).

## Runtime and execution

Tests used the repository-pinned c2j **0.0.124**, source commit
`33e2a4de4e99d3a577a38dca4b8de33d43a099ce`, through `/tmp/operational-c2j`.
The globally installed CLI was older. This wrapper ran the pinned binary with
the available local Nix store. Recipe baseline: `1c7cdc7` plus this implementation.
Native cases use disposable local cells and JobDBs. Model decisions and human
answers are scripted except in the explicitly selected live trials.

| Coverage | Suites | Cases | Final result |
| --- | ---: | ---: | --- |
| Retained adaptive and shared helpers | 63 | 310 | Passed |
| Adaptive2 public build and focused helpers | 20 | 88 | Passed |
| Public build with self-improvement hooks | 1 | 4 | Passed |
| Live UI and limit-decision trials | 2 | 4 | Passed |

The 402 native cases were verified across the broad runs and focused reruns,
not one clean invocation of the whole set. The first broad adaptive2 run exposed
a state-scope error in the new repair allowance. Other initial failures included
old assertions expecting immediate termination at limits, missing shared-helper
files in named-build fixtures, and a missing inline receipt export. These were
fixed and the affected cases rerun. Old cap tests now explicitly choose Stop;
their work-pass counts and human-turn exclusions remain asserted.

Commands, using `c2j` to denote the pinned wrapper:

```sh
c2j test run --directory recipe-tests/adaptive2 --case-timeout 3m \
  --parallelism 4 --out-dir /tmp/audit-fixes-adaptive2-first
c2j test run --directory recipe-tests/adaptive --case-timeout 3m \
  --parallelism 4 --out-dir /tmp/audit-fixes-adaptive
c2j test run --directory recipe-tests/self-improvement --case-timeout 3m \
  --out-dir /tmp/audit-fixes-self-improvement

# Focused reruns use the affected file and, when appropriate, --case.
c2j test run --file recipe-tests/adaptive2/limit-decision.test.yaml \
  --case-timeout 3m --out-dir /tmp/audit-fixes-decisions-complete
c2j test run --file recipe-tests/adaptive2/sibling-recovery.test.yaml \
  --case-timeout 3m --out-dir /tmp/audit-fixes-sibling-recovery

c2j test run --file recipe-tests/adaptive2/visual-review.live.yaml \
  --include-live --case-timeout 4m --parallelism 1 \
  --out-dir /tmp/audit-fixes-live-visual-final
c2j test run --file recipe-tests/adaptive2/limit-decision.live.yaml \
  --include-live --case-timeout 4m --parallelism 1 \
  --out-dir /tmp/audit-fixes-live-limits-final
```

The UI trial also needs `chromium` on PATH. Here it used the installed Playwright
headless Chromium. Its retained PNG is 15,588 bytes. Binary observations, rather
than the text call trace, were required to export it intact. The exporter now
accepts explicit run provenance instead of labeling every trial with an old
hard-coded recipe revision.

## What the regressions establish

| Requirement | Native evidence |
| --- | --- |
| Screenshot relevance | `visual-evidence.test.yaml`: missing actual UI evidence returns to writable validation; nonvisual and explained exemptions can pass. Model judgment is scripted here. |
| Complete review attachments | `review-links.test.yaml`: relative/encoded/reference/HTML links, galleries, missing files, cycles, exclusions and resource bounds. `review-packet.test.yaml`: actual selected references and final forms, including four new corrections without bypassing validation. |
| Approved recovery | `approved-recovery.test.yaml`: native stored approval, persisted candidate, current checks, changed scope, revised approval and read-only configure. `sibling-recovery.test.yaml`: a real replacement child can inspect an earlier sibling's approval. |
| Workspace safety | `build-delivery.test.yaml`: real mutating configure hook still fails with its original cause. Recovery cases preserve a candidate distinct from upstream. Existing consultation and publication cases retain deliberate workspace behavior. |
| Approval equivalence | `adaptive/approval-equivalence.test.yaml`: actual Git histories for neighboring context, changed behavior, binary and mode differences. Both merge-chase suites retain current verification and reuse unchanged approval. |
| Existing coordination/packages/hooks | Full retained adaptive and self-improvement suites: handoff identity, child outcomes, package policy/probe/adoption, hook failures and public entrypoint behavior. |

Limit proposal coverage:

| Acceptance | Evidence and boundary |
| --- | --- |
| LE-01, LE-02 | `build-limits`, `human-turns`: preserve candidate, continue through verification, and retain ordinary behavior below a limit. |
| LE-03, LE-06 | `response-repair`, inline `consultation`, `review-packet`, `build-handoff-recovery`: all correction contexts, retained response/artifacts, read-only repair and unchanged validation. |
| LE-04, LE-15 | `autonomous-budget`, `build-limits`, consultation and gallery cases: exact new allowances, renewed decisions and expiry at the next human round or correction episode. |
| LE-05 | `autonomous-budget` verifies receipt replay does not renew a grant. Child tests assert one submission. Process-restart replay remains untested; see below. |
| LE-07 | `limit-scope-choice-returns-to-direction` returns through direction review before implementation. |
| LE-08 | `limit-decision`: unavailable or malformed explanation uses deterministic facts; failed feedback checking asks for clarification. |
| LE-09, LE-10 | Public build and `limit-child`: Stop produces an actual failed/incomplete outcome, no merge, no replacement child; Continue finishes the same child. Inline consultation propagates its stop receipt and retained documents. |
| LE-11 | `response-repair`: missing checkpoint permits a fresh read-only report; an invalid response accompanied by child submissions does not enable blind retry. |
| LE-12 | Three actual live briefs retained under `results/limits`; readability observations are recorded with them. This is not a human approval of their quality. |
| LE-13 | `limit-decision`: contradictory feedback and zero, negative, fractional, unlimited, oversized or non-increasing custom values require another decision. |
| LE-14 | Retained adaptive suite and `adaptive/limit-escalation.test.yaml`; unrelated operational failures keep their existing outcomes. |

`bash build.sh` checks purpose-document structure only. YAML loading, Python
compilation, exported artifact hashes and `git diff --check` supplement the native
tests; none substitutes for them.
The three retained model briefs contain blank final lines. Their original bytes
are preserved; the final whitespace check excludes only `blank-at-eof` warnings.

## Limits of this evidence

- The harness answers native forms promptly. It cannot hold one for a controlled
  duration, restart the worker mid-wait, or exercise deadline expiry. Recipe-level
  receipt tests and actual child completion statuses do not prove those behaviors.
- Stop is `failed_app` with retained work and `ADAPTIVE_STOPPED_BY_USER`, not runtime
  cancellation. It does not stop separately running siblings or satisfy delivery.
- Remote executor provisioning, browser availability on deployed workers, Git
  gateway authorization and missing external source were not changed or certified.
  c2j suspension support does not by itself provision a requested environment.
- Scripted agent responses prove orchestration, not model judgment. The live UI
  trial covers assessment and packet delivery for a small static change. It does
  not establish screenshot quality for every product or a full live design cycle.
- Existing production jobs retain their captured recipes. These tests neither
  migrate them nor demonstrate adoption by deployed workers.

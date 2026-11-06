# Consultation and evidence regressions — 2026-11-06

## What failed

Both reports used JobDB `http://192.168.1.195:9047/c2`. The consultation used
recipe revision `b687a6227729063288f4158046b4d868d561dc3b`; the gitvend build
used `74c1886489258393685c58c38fedb6a890cf1601`.

### Downstream consultation: 7RN1ykcqWKaKYEeaDzrui6aOrQ7

The c2ops consultant requested command-failure artifact advice from c2j. The
nested consultation's goal `3LiGeslCTcNwSEtjfDdQiHLOrQz` succeeded; its successful
attempt was `DEMnk2Tgo3fTuDz5QPJOQeNIObM`. The parent then failed resolving
`adaptive-consultation.downstream.sequence` with `no such key: outputs`.

The recipe used `recipes.run_and_wait` as though it collected child response
bodies. Its actual output contains `goal_ids`, `job_ids`, `items`, and `wait`.
Successful items identify their result, but there is no top-level `outputs`
collection. The faulty expression was `sequence.consult_owners.outputs.outputs`.
The consultation agent and child execution had succeeded.

### Review handoff: 3LiGHbnBFqqMQhwspgI5tfy4WEV

This gitvend attempt belongs to goal `3LfrNEnKrGmUcZ05Ge9ZP2QuRuW`.
The verification command succeeded at chapter 31. The assessor approved the
candidate at chapter 32, reporting all five automatic checks passed. Its declared
files included `assessment.md` and copies of the supplied `result.json` and
`evidence.json`.

The next reviewer could not start at chapter 33: `evidence.json` was supplied by
both the document map and the evidence map. `agent-turn.yaml` expanded those maps
through separate `./` and `.` bindings into the same inbox. c2j correctly rejected
the duplicate destination. This is a recipe binding mistake, not an external
executor defect. The later agent described the executor as the blocker because
that is how the generic recipe recovery message presented the preparation error.
The attempt stopped as `failed_app`; successful verification was not a completed
build outcome.

## Why existing tests missed these bugs

1. **A mock repeated the mistaken operation contract.** The original
   `downstream-owner-advice-resumes-original-consultation` case mocked
   `recipes.run_and_wait` with an invented `outputs` array. Both the recipe and
   test agreed on the same wrong assumption. Running a case through the native
   runtime does not verify an operation whose result is replaced by a mock.
2. **The evidence fixtures omitted a valid handoff.** Reviewers returned only new
   `assessment.md` or `merge-review.md` files. No assessor returned supplied
   execution evidence to the following reviewer. Missing-artifact and deliberate
   collision tests existed, but they treated collision as a repairable failure;
   they did not require this ordinary evidence echo to succeed.
3. **Some tests bypassed consultation entirely.** Required-goal cases mocked
   consultation submission and waiting. They tested the build-goal gate without
   exercising the consultation's workspace, transcript, or result handling.
4. **Counts overstated integration coverage.** The reported pass count mixed
   native-runtime cases, native cases with mocked orchestration, and fast
   expression/branch cases. Even `type: integration_case` does not select the
   native runtime without a `runtime` block. Counting cases is not evidence that
   every important boundary was exercised.
5. **The previous credential failure had a related boundary gap.** Local Git
   fixtures did not require authenticated checkout. The subsequent permission
   regressions exercise the real credential helper and child broker with
   synthetic secrets, but still do not authenticate to a remote Git server.

These are test-design failures. Testing whether Codex is a capable agent would
not fix them: both new regressions use valid, deterministic agent responses.

## Changes and regression approach

- Shared top-level and nested consultation turns execute in the parent job.
  Nested advice saves the parent conversation and resumes its original participant
  and checkpoint after direct inline results return. Siblings are processed in
  order. A depth bound still produces an operational failure, never agreement.
- The shared conversation initializer is an empty sequence include. Nested
  conversations reuse it without recursive file expansion or additional jobs.
- Successful verification artifacts are mounted under `verification/` in task
  inboxes. Check output named `test-statements.md` cannot replace the approved
  specification. Raw hook result references retain their original provenance.
- Agent turns and candidate inspection bind one merged inbox map. Original
  execution evidence takes precedence over document copies at the same location.
- Preparation failures now direct recovery to the responsible recipe or execution
  setup instead of automatically attributing the problem to the executor.
- Nested tests mock model responses only; consultation orchestration, workspace
  selection, checkpoint publication, and artifact binding use native operations.
- Four inbox cases exercise fresh/resumed, read-only/implementation tasks. The
  same cases fail against the prior recipe with the reported duplicate-binding
  error and pass with the corrected binding.
- The prior nested path was also reproduced with a real local child recipe and
  native `recipes.run_and_wait`, replacing only the remote recipe source with a
  small fixture. The child succeeded and the parent failed on the missing field.
- A full build case has its assessor return a copy of verification evidence and
  checks that the next reviewer receives the original evidence.
- Required-goal cases now execute real inline consultations with fixture model
  responses rather than inventing consultation child results.

The existing custom-selector interface and child-job route are retained while
its inline replacement is pending investigation of c2j's hook workspace
restriction. Ordinary static includes support foreign task workspaces. Current
`cell://` hooks are bound to the consuming repository, and include source strings
are otherwise expanded before runtime. Do not claim that an arbitrary runtime
recipe selector has become a supported inline include.

## Verification scope

The current 41 adaptive suites contain 210 cases: 180 use the native runtime and
30 use the fast branch/expression harness. All 210 passed the broad local run.
After the final result-binding cleanup, the affected consultation, inbox-binding,
and recovery suites were rerun. Production attempts were inspected only; they
were not restarted or resubmitted.

Validation uses c2j `eb636a5`, disposable JobDB/Git fixtures, deterministic model
responses, and native orchestration/artifact/workspace execution. The local broad
regression copy lowers packaged model selectors to `extension_execution` and
uses installed Python/yq for native commands instead of fetching Nix packages.
This does not run live Codex, test Nix package acquisition, or exercise a remote
Git credential provider. Those boundaries must be reported separately.

Keep native orchestration unmocked for its contract tests. Mock terminal goal
states only in tests specifically about a gate's response to those states, and
pair those with native child lifecycle coverage. Schema validation for mocked
native-operation outputs would be a useful c2j enhancement; recipes should not
rely on such validation being present today.

An attempted run directly from the authored Nix selector failed during package
setup: the required `c2ops-codex-0.1.0` store path had no available substituter.
The model and consultation logic had not started. The local regression results
therefore establish runtime wiring, not availability of that published package.

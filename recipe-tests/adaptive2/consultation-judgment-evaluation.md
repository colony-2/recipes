# Consultation judgment examples

Run `consultation-judgment.live.yaml` with `--include-live`. Each case starts a
fresh packaged Codex call with the changed shared prompts, an isolated local
repository, and source/contract evidence embedded in the suite. No model response
is mocked. These are focused prompt examples, not end-to-end coordination tests.
The deterministic consultation and recovery suites cover routing separately.

The fixture accepts `api_base_url` and `api_key_env` for a configured worker's
existing API provider. Supply these in a temporary suite copy when the disposable
test runtime has no provider configuration. Keep credentials in the named worker
environment variable; never put their value in a suite or transcript. Otherwise
the operation uses ordinary Codex authentication. No model override is selected.

The output-presence assertion is a harness check only. Review actual responses
and artifacts against these criteria before recording a behavioral pass:

| Example | Acceptance | Required evidence |
| --- | --- | --- |
| receiver-corrects-false-premise | CJ-04 | Cites SQLite persistence; corrects the memory-only premise; explains reuse or a narrower justified change. |
| requester-preserves-user-constraint | CJ-05 | Explains why pruning conflicts with preserving all versions; asks storage to revise its own assignment. |
| supported-need-ends-with-answer | CJ-06 | Explains existing history/restore; returns answered with null work_kind/handoff, without an acknowledgment round. |
| reassurance-needs-no-job | CJ-07 | Uses available evidence; generates no other-cell request for general reassurance. |
| unknown-retention-changes-decision | CJ-08 | Requests a bounded storage explanation about history/retention and relates its answer to reuse versus new work. |

Retain the exact suite inputs, shared prompt source identity, actual replies,
selected documents, and a written rationale for each result. Missing credentials,
failed execution, or output presence alone cannot pass these criteria. Five
examples provide representative evidence, not a production effectiveness rate.

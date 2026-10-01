# Cross-cell conversations within one job

A job in cell A can ask an agent in cell B to evaluate ownership, refine a design,
explain an interface, or diagnose a missing dependency. Discussion alone does not
need a separate job. Actual implementation in B still belongs to a B job.

`phase.yaml` handles this during design and implementation. A returns:

```json
{
  "summary": "The client needs advice on the service's token interface.",
  "next": "consult",
  "consultation": {
    "cell": "github.com/example/service",
    "message": "What should happen when the token is invalid?",
    "ref": "main"
  }
}
```

`cell` is a resolvable c2j selector; `ref` defaults to `main`. The recipe runs
`consult.yaml` under a node `workspace` in that cell. The B agent reads B's
`AGENTS.md`, mandate, and repository. It returns `{summary, next}`, where `next`
is `done` or `ask_user`. The summary contains the answer, questions, or a complete
agreed brief in natural language.

The recipe resumes A's own session with B's reply. A decides whether to ask B
another question, continue its work, or ask the human. A later consultation of
the same cell passes B's latest session object. The state map is keyed by cell
selector and contains just that session and the latest response. Use the same
selector spelling for follow-ups. Different cells retain separate sessions;
there are no custom thread IDs, turn counters, transcript mergers, or pinned
commit ledgers. Each turn resolves its requested workspace ref normally; the
agent should reassess relevant repository changes when resuming.

B's Codex operation uses `const: true`: temporary repository experiments are
allowed but discarded after that turn. The session persists through the native
object protocol. No child job is created for this conversation, and submitting
jobs from consultation is forbidden. Invalid replies or missing session objects
stop continuation instead of silently creating a new conversation.

A can discover the need for B during implementation. Its local edits, session,
and dependency outcomes survive the discussion. Advice within the approved scope
can be applied directly. New external work requires A to return `next: redesign`,
include the agreed brief in its design, and obtain renewed human approval. This
is an agent/reviewer responsibility; a schema does not certify semantic agreement.

After approval A can submit a prerequisite with `c2j submit --cell B --build` or
`--evolve`, putting the agreed brief in the prompt. Preserve inherited broker
environment and submit asynchronously without `--run`. B's new job performs its
own mandate assessment and reviews. Its consultation session is not implicitly
transferred into that new job.

The submitting op's native `jobs.job_ids` supplies every required child. The
recipe awaits terminal results, including failures and cancellation, then resumes
A with outputs and namespaced artifacts. A diagnoses failures and incorporates
successful dependency versions; completion alone does not refresh A's snapshot.
Worker restarts must preserve the wait and avoid duplicate submissions.

Tests run real workspace switches, stored session objects, child submission,
separate workers, and squash merges against temporary repositories and an isolated
in-memory JobDB. Only model decisions are scripted. Coverage includes design
refinement, late implementation discoveries, multiple cells, feedback, invalid
replies, discarded experiments, recovery, and restart during a dependency wait.

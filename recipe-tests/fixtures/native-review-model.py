"""Script agent decisions; keep document producers, reviews, sessions and merges real."""

import json
import os
from pathlib import Path

root = Path(os.environ["WORKTREE"])
inbox = Path(os.environ["INBOX"])
out = Path(os.environ["OUTBOX"])
instructions = os.environ["INSTRUCTIONS"]
session = os.environ["SESSION"]
home = Path(os.environ["SESSION_HOME"])
role = (
    "design"
    if instructions.startswith("Assess")
    else "implement"
    if instructions.startswith("Implement")
    else "plan"
    if instructions.startswith("Write outcome")
    else "review"
)
prior = json.loads((home / "session.json").read_text()) if session else {"round": 0}
assert not session or session == "review-fixture-" + role
turn = prior["round"] + 1
trace = Path(os.environ["TRACE"])
previous = (
    [json.loads(line) for line in trace.read_text().splitlines()]
    if trace.exists()
    else []
)
round_number = 1 + sum(row["role"] == role for row in previous)
attachments = {
    str(p.relative_to(inbox / "prior/review")): p.read_text()
    for p in (inbox / "prior/review").rglob("*")
    if p.is_file()
}
with trace.open("a") as f:
    f.write(
        json.dumps(
            dict(
                role=role,
                session=session,
                turn=turn,
                feedback=os.environ["FEEDBACK"],
                attachments=attachments,
            )
        )
        + "\n"
    )
base = dict(
    status="ready",
    summary=f"{role} outcome {round_number}",
    questions=[],
    blocking_issues=[],
)
context = json.loads((inbox / "phase/context.json").read_text())
context = context.get("phase", context)
if role == "design":
    mandate = context["mandate"]
    assert mandate["valid"]
    result = dict(
        base,
        design_markdown=f"# Design {round_number}\n\nRequested behavior works.\n",
        requirements=[dict(id="R1", statement="Requested behavior works")],
        assessment=dict(
            assessment_status="assessed",
            fit="fits",
            rationale="Local responsibility",
            questions=[],
            outcomes=[
                dict(
                    id="R1",
                    statement="Requested behavior works",
                    ownership="local",
                    suggested_owner=mandate["cell"],
                    mandate_evidence=["OWN-01"],
                    reason="Owned behavior",
                )
            ],
        ),
        consultation=None,
        handoffs=[],
    )
elif role == "plan":
    result = dict(
        base,
        statements=[
            dict(
                id=key,
                statement=statement,
                requirement_ids=["R1"],
                files=["test_feature.py"],
                importance="critical",
                level="integration",
                dependencies=[],
                case=case,
            )
            for key, statement, case in [
                ("T1", "Requested behavior works.", "positive"),
                ("T2", "Invalid behavior is rejected.", "negative"),
            ]
        ],
        commands=[
            dict(
                id="behavior",
                run="python3 test_feature.py",
                statement_ids=["T1", "T2"],
                timeout_seconds=10,
            )
        ],
    )
elif role == "implement":
    target = root / (".c2j" if os.environ["MODE"] == "evolve" else ".")
    target.mkdir(exist_ok=True)
    (target / "feature.txt").write_text("behavior-" + str(turn))
    (target / "test_feature.py").write_text(
        "from pathlib import Path\nv=Path('feature.txt').read_text()\nassert v.startswith('behavior-')\nassert not v.startswith('invalid-')\n"
    )
    result = dict(
        base,
        changes=["Requested behavior works"],
        statement_tests=[
            dict(statement_id=key, files=["test_feature.py"]) for key in ["T1", "T2"]
        ],
        consultation=None,
        proposed_handoffs=[],
    )
else:
    result = base
(out / "result.json").write_text(json.dumps(result))
(home / "session.json").write_text(json.dumps({"round": turn}))
print(json.dumps(dict(status="completed", sessionId="review-fixture-" + role)))

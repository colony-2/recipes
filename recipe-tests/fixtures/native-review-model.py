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
base = dict(next="done" if role=="review" else "review", summary=f"{role} outcome {round_number}")
assert (root / ".c2j/mandate.md").exists()
if role == "design":
    (out / "design.md").write_text(f"# Design {round_number}\n\nRequested behavior works.\n")
elif role == "plan":
    assert (inbox / "prior/design.md").exists(), list(inbox.rglob("*"))
    (root / ".c2j/test-plan.md").write_text("# Test plan\n\n- Requested behavior works. Files: test_feature.py; critical; integration; dependencies: none.\n- Invalid behavior is rejected. Files: test_feature.py; critical; integration; dependencies: none.\n")
elif role == "implement":
    assert (inbox / "prior/design.md").exists()
    assert (root / ".c2j/test-plan.md").exists()
    target = root / (".c2j" if os.environ["MODE"] == "evolve" else ".")
    target.mkdir(exist_ok=True)
    (target / "feature.txt").write_text("behavior-" + str(turn))
    (target / "test_feature.py").write_text("from pathlib import Path\nv=Path('feature.txt').read_text()\nassert v.startswith('behavior-')\nassert not v.startswith('invalid-')\n")
    (target / "build.sh").write_text("python3 test_feature.py\n")
    (out / "implementation.md").write_text("# Implementation\n\n"+base['summary'])
else:
    assert (inbox / "prior/design.md").exists(), list(inbox.rglob("*"))
result = base
(out / "result.json").write_text(json.dumps(result))
(home / "session.json").write_text(json.dumps({"round": turn}))
print(json.dumps(dict(status="completed", sessionId="review-fixture-" + role)))

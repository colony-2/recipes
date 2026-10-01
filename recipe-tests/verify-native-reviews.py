# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Real build/evolve document reviews and public-library submissions on isolated JobDB."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import tempfile
import time
import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "lifecycle", ROOT / "recipe-tests/verify-development-lifecycle.py"
)
lifecycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lifecycle)
c, d, deps, e = lifecycle.c, lifecycle.d, lifecycle.deps, lifecycle.e
MARKUP = "# Feedback\n\n{--old--}{++new++} {~~before~>after~~} {==focus==}{>>explain π and recovery<<}\n"


def install(repo, mode, work):
    folder = repo / ".c2j/recipes"
    shutil.copytree(ROOT / "recipes/develop", folder / "develop")
    agent = d.objects.replace(
        c.read("agent.yaml"),
        folder / "develop",
        dict(
            MODE=mode,
            TRACE=str(work / "trace.jsonl"),
            WORKTREE="{{ context.environment.op.worktree_path }}",
            INBOX="{{ context.environment.op.inbox }}",
            OUTBOX="{{ context.environment.op.outbox }}",
            INSTRUCTIONS=e("inputs.instructions"),
            FEEDBACK=e("inputs.feedback"),
        ),
        (ROOT / "recipe-tests/fixtures/native-review-model.py").read_text(),
    )
    c.write(folder / "develop/agent.yaml", agent)
    verify = c.read("verify.yaml")
    del verify["sequence"][0]["inputs"]["sandbox"]
    c.write(folder / "develop/verify.yaml", verify)
    for name in ["build", "evolve"]:
        entry = yaml.safe_load((ROOT / (name + ".yaml")).read_text())
        entry["sequence"][0]["include"] = "./develop/develop.yaml"
        c.write(folder / (name + ".yaml"), entry)
    d.git(repo, "add", ".")
    d.git(repo, "commit", "-qm", "Install review defaults")


def exercise(work, server_binary, client, mode):
    work.mkdir()
    server = subprocess.Popen(
        [str(server_binary)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    workers = []
    logs = []
    try:
        assert select.select([server.stdout], [], [], 20)[0]
        url = server.stdout.readline().strip()
        assert url.startswith("http://127.0.0.1:")
        env = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith(("C2J_CURRENT_", "C2J_CHILD_JOB_"))
            and k != "C2J_TENANT_ID"
        }
        env.update(
            C2J_JOBDB=url + "/test",
            TMPDIR=str(work),
            GIT_AUTHOR_NAME="Recipe Test",
            GIT_AUTHOR_EMAIL="recipe-test@example.com",
            GIT_COMMITTER_NAME="Recipe Test",
            GIT_COMMITTER_EMAIL="recipe-test@example.com",
        )
        repo = c.seed(work, "cell")
        install(repo, mode, work)
        upstream = work / "upstream.git"
        d.run(["git", "init", "--bare", "-q", "-b", "main", str(upstream)])
        d.git(repo, "remote", "add", "origin", str(upstream))
        d.git(repo, "push", "-q", "origin", "main")
        base = d.git(repo, "rev-parse", "HEAD")
        job = json.loads(
            d.run(
                [
                    "c2j",
                    "submit",
                    "Improve requested behavior",
                    "--" + mode,
                    "--cell",
                    str(upstream),
                    "--json",
                ],
                env=env,
            )
        )["job_id"]

        def start():
            log = (work / f"worker-{len(workers)}.log").open("w")
            logs.append(log)
            worker = subprocess.Popen(
                [
                    "c2j",
                    "run",
                    "one",
                    "--job-id",
                    job,
                    "--input-mode",
                    "ops",
                    "--await-threshold",
                    "2s",
                    "--poll-interval",
                    "100ms",
                    "--wait-timeout",
                    "600s",
                ],
                env=env,
                stdout=log,
                stderr=log,
            )
            workers.append(worker)
            return worker

        worker = start()

        def call(action, payload=None):
            return subprocess.run(
                [str(client), url, job, action],
                input=json.dumps(payload) if payload is not None else None,
                text=True,
                capture_output=True,
                timeout=30,
            )

        def pending(title, previous=None):
            deadline = time.monotonic() + 100
            while time.monotonic() < deadline:
                response = call("get")
                if response.returncode == 0:
                    form = json.loads(response.stdout)
                    if form.get("request_id") != previous:
                        assert form["title"] == title, form
                        assert (
                            form["kind"] == "review"
                            and form["request_id"]
                            and not form.get("response_schema")
                        ), form
                        # Stop at the input boundary before responding. Otherwise the old
                        # worker can race the submission and execute the next review cycle.
                        worker.wait(timeout=60)
                        return form
                if (
                    worker.poll() is not None
                    and "input required"
                    not in (work / f"worker-{len(workers) - 1}.log").read_text()
                ):
                    raise AssertionError(
                        (work / f"worker-{len(workers) - 1}.log").read_text()[-6000:]
                    )
                time.sleep(0.1)
            raise AssertionError(
                "Review did not become pending: "
                + response.stderr
                + "\n"
                + "".join(p.read_text()[-4000:] for p in work.glob("worker-*.log"))
            )

        def submit(
            form,
            decision=None,
            feedback=None,
            uploads=None,
            error=False,
            request_id=None,
            extra=None,
        ):
            nonlocal worker
            fields = {}
            if decision is not None:
                fields["decision"] = decision
            if feedback is not None:
                fields["feedback"] = feedback
            fields.update(extra or {})
            response = call(
                "submit",
                dict(
                    request_id=request_id or form["request_id"],
                    submission_id="test-" + str(time.monotonic_ns()),
                    fields=fields,
                    uploads=uploads or {},
                ),
            )
            if error:
                assert response.returncode != 0, (fields, response.stdout)
                assert (
                    json.loads(call("get").stdout)["request_id"] == form["request_id"]
                )
            else:
                assert response.returncode == 0, response.stderr
                worker.wait(timeout=10)
                worker = start()
            return json.loads(response.stdout) if response.returncode == 0 else None

        def unchanged():
            assert (
                d.run(["git", "--git-dir", str(upstream), "rev-parse", "main"]).strip()
                == base
            )

        def rows(role):
            return [
                r
                for r in map(
                    json.loads, (work / "trace.jsonl").read_text().splitlines()
                )
                if r["role"] == role
            ]

        plan = pending("Approve design and test plan")
        assert set(plan["documents"]) == {"design", "test_statements"}, plan
        original = copy.deepcopy(plan["documents"])
        original_read = call("read", original["design"])
        assert original_read.returncode == 0, original_read.stderr
        original_text = json.loads(original_read.stdout)["content"]
        unchanged()
        submit(plan, error=True)
        submit(plan, "invalid", error=True)
        submit(plan, "approve", error=True, request_id="stale-request")
        bad = copy.deepcopy(original["design"])
        bad["stored"]["key"]["jobId"] = "missing-job"
        submit(plan, "revise", error=True, extra={"annotated_design": bad})
        assert not rows("implement")
        submit(
            plan,
            "revise",
            "Include the annotations",
            {"annotated_design": {"name": "design-edits.md", "content": MARKUP}},
        )
        next_plan = pending("Approve design and test plan", plan["request_id"])
        assert next_plan["documents"]["design"] != original["design"]
        assert (
            json.loads(call("read", original["design"]).stdout)["content"]
            == original_text
        )
        assert not rows("implement")
        assert (
            rows("design")[-1]["attachments"] == {"design-edits.md": MARKUP}
            and rows("design")[-1]["feedback"] == "Include the annotations"
        )
        submit(next_plan, "revise", "Text-only follow-up")
        plan = pending("Approve design and test plan", next_plan["request_id"])
        assert (
            rows("design")[-1]["attachments"] == {}
            and rows("design")[-1]["feedback"] == "Text-only follow-up"
        )
        submit(plan, "approve")
        outcome = pending("Review verified outcome", plan["request_id"])
        assert set(outcome["documents"]) == {
            "design",
            "test_statements",
            "implement",
            "verification",
        }
        unchanged()
        # Replay must preserve the same pending occurrence and exact source documents.
        worker.terminate()
        worker.wait(timeout=10)
        worker = start()
        replay = pending("Review verified outcome")
        assert (
            replay["request_id"] == outcome["request_id"]
            and replay["documents"] == outcome["documents"]
        )
        submit(replay, "satisfied", error=True, request_id=plan["request_id"])
        unchanged()
        submit(
            replay,
            "revise",
            uploads={
                "annotated_outcome": {"name": "outcome-edits.md", "content": MARKUP}
            },
        )
        revised = pending("Review verified outcome", replay["request_id"])
        assert (
            rows("implement")[-1]["session"] == "review-fixture-implement"
            and rows("implement")[-1]["turn"] == 2
        )
        assert rows("implement")[-1]["attachments"] == {"outcome-edits.md": MARKUP}
        assert revised["documents"]["implement"] != outcome["documents"]["implement"]
        unchanged()
        submit(revised, "redesign", "Change the requirements")
        plan = pending("Approve design and test plan", revised["request_id"])
        assert (
            rows("design")[-1]["feedback"] == "Change the requirements"
            and not rows("design")[-1]["attachments"]
        )
        submit(plan, "approve")
        outcome = pending("Review verified outcome", plan["request_id"])
        assert (
            rows("implement")[-1]["turn"] == 3
            and not rows("implement")[-1]["attachments"]
        )
        # Uploaded edits accompanying approval cannot bypass revision and reapproval.
        submit(
            outcome,
            "satisfied",
            uploads={"annotated_outcome": {"name": "last-edits.md", "content": MARKUP}},
        )
        final = pending("Review verified outcome", outcome["request_id"])
        unchanged()
        assert rows("implement")[-1]["turn"] == 4
        receipt = submit(final, "satisfied")
        assert worker.wait(timeout=120) == 0, "".join(
            p.read_text()[-6000:] for p in work.glob("worker-*.log")
        )
        result = deps.request(url + "/test/job?id=" + job)["Attempts"][-1]["Output"][
            "Data"
        ]
        assert result["merged"] and result["verification"]["ok"]
        assert result["reviews"]["outcome"] == receipt["receipt"] and result["reviews"][
            "outcome"
        ]["actor"] == {"id": "recipe-reviewer", "kind": "human"}
        assert (
            result["review_documents"] == final["documents"]
            and result["reviews"]["plan"]["request_id"] == plan["request_id"]
        )
        assert (
            d.run(
                [
                    "git",
                    "--git-dir",
                    str(upstream),
                    "rev-list",
                    "--count",
                    base + "..main",
                ]
            ).strip()
            == "1"
        )
        assert (
            d.run(["git", "--git-dir", str(upstream), "rev-parse", "main"]).strip()
            == result["merged_hash"]
        )
        print(
            "native reviews: "
            + mode
            + " document reviews, invalid submissions, annotations, revisions, replay and approved squash merge passed",
            flush=True,
        )
    except Exception:
        destination = (
            Path(os.environ.get("C2J_TEST_LOG_DIR", "/tmp/native-review-failures"))
            / mode
        )
        destination.mkdir(parents=True, exist_ok=True)
        for log in logs:
            log.flush()
        for path in list(work.glob("*.log")) + list(work.glob("*.jsonl")):
            shutil.copy(path, destination / path.name)
        raise
    finally:
        for worker in workers:
            if worker.poll() is None:
                worker.terminate()
                worker.wait(timeout=10)
        for log in logs:
            log.close()
        server.terminate()
        server.wait(timeout=10)


def verify_autofill(work):
    """A document-free clarification uses the same native acceptance path."""
    coordinator = c.read("develop.yaml")
    for node in coordinator["state"]["states"].values():
        if node.get("op") == "input":
            assert node["inputs"]["form"]["kind"] == "review"
            assert "autofill" not in node["inputs"]["form"]
    form = copy.deepcopy(
        coordinator["state"]["states"]["plan_feedback"]["inputs"]["form"]
    )
    form["documents"] = {}
    form["fields"][0]["question"] = "Clarify the requested outcome."
    form["autofill"] = {
        "fields": {"decision": "revise", "feedback": "Clarified outcome"}
    }
    recipe = work / "autofill.yaml"
    c.write(
        recipe,
        {
            "id": "native-review-autofill",
            "sequence": [{"id": "review", "op": "input", "inputs": {"form": form}}],
            "outputs": {
                "actor": e("sequence.review.outputs.receipt.actor.kind"),
                "decision": e("sequence.review.outputs.fields.decision"),
            },
        },
    )
    d.run_suite(
        recipe,
        [
            {
                "id": "clarification",
                "type": "recipe_case",
                "inputs": {},
                "mocks": {
                    "ops": [
                        {
                            "match": {"op": "auto-fill-input"},
                            "behavior": {"mode": "passthrough"},
                        },
                        {"match": {"op": "input"}, "behavior": {"mode": "passthrough"}},
                    ]
                },
                "assertions": [
                    {"type": "output_equals", "path": "actor", "value": "automation"},
                    {"type": "output_equals", "path": "decision", "value": "revise"},
                ],
            }
        ],
        work / "autofill",
    )
    print(
        "native reviews: text-only clarification autofill records automation actor",
        flush=True,
    )


def main():
    with tempfile.TemporaryDirectory(prefix="native-reviews-") as temp:
        work = Path(temp)
        server = work / "jobdb-service"
        client = work / "review-client"
        d.run(
            ["go", "build", "-o", str(server), "."],
            cwd=ROOT / "recipe-tests/jobdb-service",
        )
        d.run(
            ["go", "build", "-o", str(client), "."],
            cwd=ROOT / "recipe-tests/review-client",
        )
        verify_autofill(work)
        for mode in sys.argv[1:] or ["build", "evolve"]:
            exercise(work / mode, server, client, mode)


if __name__ == "__main__":
    main()

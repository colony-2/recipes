# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Exercise the real c2j graph, gate ops, commands and git integration in isolation.

Codex and human replies are fixtures. No model API, persistent job database, or
project upstream is used. Tests do not substitute a Python state-machine model.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
CODEX = "git+https://github.com/colony-2/c2ops.git//codex@ded76dfbd877d3d0749e509844ecdbc57197b572"
GATE = "git+https://github.com/colony-2/c2ops.git//rule_gate@main"
import importlib.util
import sys
sys.dont_write_bytecode = True
_object_spec = importlib.util.spec_from_file_location('object_fixture', ROOT/'recipe-tests/object-session-fixture.py')
objects = importlib.util.module_from_spec(_object_spec); _object_spec.loader.exec_module(objects)
HASH = "a" * 40
BASE = dict(next="done", summary="Ready")
DESIGN = dict(next="review", summary="The request fits this cell. Add the requested behavior.")
PLAN = dict(next="review", summary="Review the maintained test plan.")
IMPLEMENTATION = dict(next="review", summary="Implemented behavior")


def session_ref(identity="session", turn=0):
    digest = hashlib.sha256(f"{identity}:{turn}".encode()).hexdigest()
    return {"$c2j_object":"v1","type":"c2ops.codex.session/v1","tenant_id":"test", "sha256":digest,
            "artifact":{"jobId":identity,"taskOrdinal":turn+1,"name":"__c2j_objects__/"+digest+".tar","sizeBytes":100}}


def run(args, **kwargs):
    p = subprocess.run(args, text=True, capture_output=True, **kwargs)
    if p.returncode:
        raise AssertionError(f"{args}\n{p.stdout[-5000:]}\n{p.stderr[-7000:]}")
    return p.stdout


def mock(op, output, artifacts=None):
    value = {"match": {"op": op}, "behavior": {"mode": "return", "outputs": output}}
    if artifacts is not None:
        value["behavior"]["artifacts"] = artifacts
    return value


def command(value, success=True, artifacts=None):
    return mock("command_execution", {"success": success, "exit_code": 0 if success else 1, "stdout": json.dumps(value), "stderr": "" if success else "Check failed"}, artifacts)


def phase(result, *, valid=True, status="completed", session="implementation-session", documents=True):
    artifacts = {"result.json": json.dumps(result)}
    if documents: artifacts.update({"design.md": "# Design", "implementation.md": "# Implementation"})
    ops = [mock("extension_execution", {"status": status, "sessionId": session, **({"session": session_ref(session)} if session else {})}, artifacts), mock("extension_execution", {"ok": valid})]
    if valid: ops.append(command(result))
    return ops

def response(choice, text=None):
    return mock("input", {"fields": {"decision": choice, **({"feedback": text} if text is not None else {})}, "artifact_refs": {}, "receipt": {}})


def feedback(text="Fix the reported issue"):
    return mock("input", {"fields": {"decision": "revise", "feedback": text}, "artifact_refs": {}, "receipt": {}})


def planning():
    return phase(DESIGN) + phase(BASE) + phase(PLAN) + [command({"ok": True}, artifacts={"test-statements.md": "# Test statements"})] + phase(BASE)


def implementation(summary="Implemented behavior"):
    return phase({**IMPLEMENTATION, "summary": summary}) + phase(BASE) + phase(BASE)


def verification(ok=True):
    result = mock("command_execution", {"success": ok, "exit_code": 0 if ok else 7, "stdout": "ran", "stderr": "", "timed_out": False}, {"build.log": "Executed verification evidence"})
    return [result, command({}, artifacts={"verification.md": "# Verification"})]

def finish():
    return [response("satisfied"), mock("extension_execution", {"ok": True}), mock("squashrebasemerge", {"merged_hash": "merged-hash", "target_branch": "main"})]


def case(name, ops, merged=True):
    return {"id": name, "type": "recipe_case", "inputs": {"prompt": "Improve requested behavior"}, "mocks": {"ops": [mock("recipe_within_resolution", {"resolved_selectors": {}}), command({})] + ops}, "assertions": [{"type": "output_equals", "path": "merged", "value": merged}]}


def routing_cases():
    start = planning() + [response("approve")]
    end = implementation() + verification() + finish()
    cases = [case("happy", start + end)]
    cases += [case("direct-plan-feedback", planning() + [response("revise", "Clarify outcomes")] + start + end)]
    cases += [case("direct-implementation-feedback", start + implementation() + verification() + [response("revise", "Direct revision")] + end)]
    cases += [case("direct-redesign", start + implementation() + verification() + [response("redesign", "Change scope")] + start + end)]
    cases += [case("repeat-feedback", start + implementation("First outcome") + verification() + [response("revise"), feedback("Add coverage")] + implementation("Second outcome") + verification() + [response("revise"), feedback("Handle empty input")] + implementation("Final outcome") + verification() + finish())]
    cases += [case("redesign", start + implementation() + verification() + [response("redesign"), feedback("Change the requirements")] + start + end)]
    cases += [case("implementation-requests-redesign", start + phase({**IMPLEMENTATION,"next":"redesign"}) + [feedback("Review the external work")] + start + end)]
    cases += [case("human-rejects-plan", planning() + [response("revise"), feedback()] + start + end)]
    for name, prefix in [
        ("design-needs-input", phase({**DESIGN, "next": "ask_user"})),
        ("design-review-rejects", phase(DESIGN) + phase({**BASE, "next": "revise"})),
        ("test-review-rejects", phase(DESIGN) + phase(BASE) + phase(PLAN) + [command({"ok": True}, artifacts={"test-statements.md": "# Test statements"})] + phase({**BASE, "next": "revise"})),
        ("test-contract-rejects", phase(DESIGN) + phase(BASE) + phase(PLAN) + [command({}, False)]),
    ]:
        cases.append(case(name, prefix + [feedback()] + start + end))
    for name, prefix in [
        ("implementation-incomplete", phase({**IMPLEMENTATION, "next": "ask_user"}, status="incomplete")),
        ("specification-rejects", phase(IMPLEMENTATION) + phase({**BASE, "next": "revise"})),
        ("quality-rejects", phase(IMPLEMENTATION) + phase(BASE) + phase({**BASE, "next": "revise"})),
    ]:
        cases.append(case(name, start + prefix + [feedback()] + end))
    cases += [case("verification-fails", start + implementation() + verification(False) + end)]
    cases += [case("continue-session", phase({**DESIGN,"next":"continue"}) + start + end)]
    cases += [case("outside", phase({**DESIGN,"next":"outside"}) + [response("acknowledge")], False)]
    cases += [case("invalid-human-input", planning() + [response("invalid"), response("approve")] + implementation() + verification() + [response("invalid"), response("revise"), feedback(" "), feedback("Fix this")] + end)]
    for name, prefix in [
        ("invalid-design-artifact", phase(DESIGN, valid=False)),
        ("invalid-missing-design", phase(DESIGN, documents=False)),
        ("invalid-review-artifact", phase(DESIGN) + phase(BASE, valid=False)),
        ("invalid-implementation-artifact", start + phase(IMPLEMENTATION, valid=False)),
        ("missing-session", start + phase(IMPLEMENTATION, session="")),
        ("agent-error", start + phase(IMPLEMENTATION, status="error")),
        ("invalid-revision-artifact", start + implementation() + verification() + [response("revise"), feedback()] + phase(IMPLEMENTATION, valid=False)),
    ]:
        cases.append(case(name, prefix + [command({}, False)], False))
    return cases


def instrument(source, dest):
    shutil.copytree(source / "recipes/develop", dest / "recipes/develop")
    for name in ("build", "evolve"):
        shutil.copy(source / f"{name}.yaml", dest)
    for path in dest.rglob("*.yaml"):
        doc = yaml.safe_load(path.read_text())
        def visit(node):
            if not isinstance(node, dict):
                return
            if "op" in node and node["op"] in (CODEX, "input", "squashrebasemerge"):
                node.setdefault("vars", {})["observed_inputs"] = copy.deepcopy(node["inputs"])
                if node["op"] == CODEX:
                    node["vars"]["observed_target_is_evolve"] = '${{ inputs.target_directory == ".c2j" }}'
                    if "worktree_path" in node["inputs"]:
                        assert node["inputs"]["worktree_path"] == "{{ context.environment.op.worktree_path }}/{{ inputs.target_directory }}"
            for key in ("sequence",):
                for child in node.get(key, []):
                    visit(child)
            if "state" in node:
                for child in node["state"]["states"].values():
                    visit(child)
        visit(doc)
        path.write_text(yaml.safe_dump(doc, sort_keys=False))


def run_suite(recipe, suite, dest, *, parallelism=1, failure_contains=None):
    dest.mkdir(parents=True, exist_ok=True)
    fixture = dest / "suite.yaml"
    fixture.write_text(yaml.safe_dump({"cases": suite}, sort_keys=False))
    run(["c2j", "test", "compile", "--recipe-file", str(recipe), "--file", str(fixture), "--strict", "--out", str(dest / "compiled.json")])
    outcome = subprocess.run(["c2j", "test", "run", "--recipe-file", str(recipe), "--file", str(fixture), "--out-dir", str(dest), "--parallelism", str(parallelism), "--case-timeout", "120s", "--artifact-mode", "inline"], timeout=600, text=True, capture_output=True)
    results = {p.parent.name: json.loads(p.read_text()) for p in (dest / "cases").glob("*/result.json")}
    assert len(results) == len(suite), results.keys()
    if failure_contains:
        assert outcome.returncode != 0
        assert all(r["status"] == "failed" and failure_contains in r["run"].get("failure_reason", "") for r in results.values()), results
        return results
    assert all(r["status"] == "passed" for r in results.values()), {k: r["run"].get("failure_reason", r["run"].get("assertions")) for k, r in results.items() if r["status"] != "passed"}
    assert outcome.returncode == 0, outcome.stderr[-3000:]
    return results


def verify_routing(work):
    instrument(ROOT, work / "observed")
    for name in ("build", "evolve"):
        cases = routing_cases()
        # c2j's named build/evolve submission contract injects this field.
        for test in cases:
            test["inputs"]["type"] = name
        results = run_suite(work / "observed" / f"{name}.yaml", cases, work / name, parallelism=4)
        for case_id, result in results.items():
            observations = result["run"]["diagnostics"].get("vars", [])
            observed = [(o["node_path"], o["vars"]["observed_inputs"]) for o in observations if "observed_inputs" in o["vars"]]
            agents = [(p, v) for p, v in observed if "prompt" in v]
            assert agents, (name, case_id)
            target_flags = [o["vars"]["observed_target_is_evolve"] for o in observations if "observed_inputs" in o["vars"] and "prompt" in o["vars"]["observed_inputs"]]
            assert target_flags == [name == "evolve"] * len(agents)
            if case_id == "happy":
                assert [p.split("/")[3] for p, _ in agents] == ["design", "design_review", "test_plan", "test_review", "implementation", "specification", "quality"]
            for path, value in agents:
                assert value["sandbox"] == {"type": "shai"}
                assert "Improve requested behavior" in value["prompt"]
                for field in ("workdir_path", "artifact_inbox_path", "artifact_outbox_path"):
                    assert field not in value, (name, case_id, path, field)
                if name == "evolve":
                    # c2j intentionally redacts concrete worktree paths in diagnostics.
                    assert "worktree_path" in value
                    assert ".c2j/recipes/build.yaml" in value["prompt"]
                else:
                    assert "worktree_path" not in value
                if "/implementation/" not in path and case_id != "continue-session":
                    assert "session" not in value and "sessionId" not in value, (name, case_id, path)
            if case_id in ("repeat-feedback", "redesign", "invalid-human-input"):
                implementers = [v for p, v in agents if "/implementation/" in p]
                assert len(implementers) >= 2, (name, case_id, [p for p, _ in agents])
                assert "session" not in implementers[0]
                assert all(v["session"] == {**session_ref("implementation-session"), "artifact": {**session_ref("implementation-session")["artifact"], "name": "[REDACTED]"}} for v in implementers[1:]), (case_id, [v.get("session") for v in implementers])
            if case_id == "direct-implementation-feedback":
                implementers = [v for p, v in agents if "/implementation/" in p]
                assert "Direct revision" in implementers[-1]["prompt"]
                assert not any(p.endswith("/implementation_feedback") for p, _ in observed)
            if case_id in ("direct-plan-feedback", "direct-redesign"):
                designs = [v for p, v in agents if "/design/" in p]
                assert ("Clarify outcomes" if case_id == "direct-plan-feedback" else "Change scope") in designs[-1]["prompt"]
                assert not any(p.endswith("/plan_feedback") for p, _ in observed)
            if case_id == "repeat-feedback":
                assert "Add coverage" in implementers[1]["prompt"]
                assert "Handle empty input" in implementers[2]["prompt"]
                accepts = [v for p, v in observed if p.endswith("/accept")]
                assert len(accepts) == 3
                assert [s in v["form"]["fields"][0]["question"] for s, v in zip(["First outcome", "Second outcome", "Final outcome"], accepts)] == [True] * 3
            if case_id in ("redesign", "implementation-requests-redesign"):
                approvals = [p for p, _ in observed if p.endswith("/approve_plan")]
                assert len(approvals) == 2, (name, case_id, approvals)
            if case_id.startswith("invalid-") and case_id != "invalid-human-input" or case_id in ("missing-session", "agent-error"):
                assert not any("commit_message" in v for _, v in observed)
        print(f"{name}: {len(results)} c2j routing cases and rendered input contracts passed", flush=True)


def git(repo, *args):
    return run(["git", "-C", str(repo), *args]).strip()


def repository(work, name):
    repo = work / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "recipe-test@example.com")
    git(repo, "config", "user.name", "Recipe Test")
    (repo / ".c2j").mkdir()
    (repo / ".c2j/recipe.txt").write_text("original\n")
    (repo / "app.txt").write_text("application\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "seed")
    return repo


def script(recipe, state=None):
    doc = yaml.safe_load((ROOT / "recipes/develop" / recipe).read_text())
    return doc["state"]["states"][state]["inputs"]["run"] if state else doc["sequence"][0]["inputs"]["run"]


def command_test(code, env, ok=True):
    p = subprocess.run(["bash", "-euo", "pipefail", "-c", code], env={**os.environ, **env}, text=True, capture_output=True)
    assert (p.returncode == 0) == ok, (p.returncode, p.stdout, p.stderr)
    return json.loads(p.stdout) if ok else None



def verify_plan_contract(work):
    # Publication copies the actual tracked Markdown; no JSON reconstruction.
    doc = yaml.safe_load((ROOT / "recipes/develop/test-plan.yaml").read_text())
    code = doc["sequence"][1]["state"]["states"]["copy"]["inputs"]["run"]
    repo = repository(work, "plan-cell"); out = work / "plan-out"; out.mkdir()
    plan = repo / ".c2j/test-plan.md"
    text = "# Test plan\n\n- Valid requests succeed. Files: test.sh; critical; integration; dependencies: none.\n"
    plan.write_text(text)
    run(["bash", "-euo", "pipefail", "-c", code], env={**os.environ,"PLAN":str(plan),"OUTBOX":str(out)})
    assert (out / "test-statements.md").read_text() == text
    plan.unlink()
    missing = subprocess.run(["bash", "-euo", "pipefail", "-c", code], env={**os.environ,"PLAN":str(plan),"OUTBOX":str(out)}, capture_output=True)
    assert missing.returncode
    print("test plan: exact Markdown publication and missing-file rejection passed", flush=True)

def verify_commands(work):
    for name, hook in [("pass", "printf 'verified output\\n'"), ("fail", "echo failed; exit 7"), ("timeout", "echo starting; sleep 5"), ("missing", None)]:
        repo = repository(work, "verify-" + name)
        if hook is not None: (repo / ".c2j/build.sh").write_text(hook + "\n")
        doc = yaml.safe_load((ROOT / "recipes/develop/verify.yaml").read_text())
        execute = doc["sequence"][0]["inputs"]; execute.pop("sandbox")
        execute["env"]["TARGET"] = str(repo / ".c2j")
        path = work / ("hook-"+name+".yaml"); path.write_text(yaml.safe_dump(doc))
        passthrough = [{"match":{"op":op}, "behavior":{"mode":"passthrough"}} for op in ["command_execution","command_execution"]]
        case = {"id":name,"type":"recipe_case","inputs":{"timeout":"1s"},"mocks":{"ops":[mock("recipe_within_resolution",{"resolved_selectors":{}})]+passthrough},"assertions":[{"type":"output_equals","path":"ok","value":name in ["pass","missing"]},{"type":"output_equals","path":"result.status","value":"skipped" if name=="missing" else "passed" if name=="pass" else "failed"}]}
        results=run_suite(path,[case],work/("hook-results-"+name))
        output=results[name]["run"]["outputs"]
        assert set(output["artifact_refs"]) == ({"verification.md"} if name=="missing" else {"verification.md","build.log"})
        if name=="timeout": assert output["result"]["timed_out"]
    print("verification: native pass/failure/timeout/skipped hook cases passed",flush=True)

def verify_real_gates(work):
    role = yaml.safe_load((ROOT / "recipes/develop/implement.yaml").read_text())
    schema_json = json.dumps(role["vars"]["result_schema"])
    invalid = {
        "missing": None,
        "malformed": "not json",
        "missing-field": json.dumps({"summary": "Incomplete result"}),
        "blank-summary": json.dumps({**IMPLEMENTATION, "summary": "  "}),
        "wrong-type": json.dumps({**IMPLEMENTATION, "next": 7}),
        "extra-field": json.dumps({**IMPLEMENTATION, "unexpected": True}),
        "wrong-next": json.dumps({**IMPLEMENTATION, "next": "invented"}),
        "consult-missing-request": json.dumps({**IMPLEMENTATION, "next": "consult"}),
        "consult-missing-cell": json.dumps({**IMPLEMENTATION, "next": "consult", "consultation": {"message": "Explain the interface"}}),
        "consult-blank-cell": json.dumps({**IMPLEMENTATION, "next": "consult", "consultation": {"cell": " ", "message": "Explain the interface"}}),
        "unexpected-request": json.dumps({**IMPLEMENTATION, "consultation": {"cell": "B", "message": "Explain the interface"}}),
    }
    cases = []
    for resumed in (False, True):
        for name, raw in {"valid": json.dumps(IMPLEMENTATION), "valid-consult": json.dumps({**IMPLEMENTATION, "next": "consult", "consultation": {"cell": "B", "message": "Explain the interface"}}), **invalid}.items():
            ops = [mock("recipe_within_resolution", {"resolved_selectors": {}}), mock("extension_execution", {"status": "completed", "sessionId": "session", "session": session_ref()}, {} if raw is None else {"result.json": raw}),
                   {"match": {"op": "extension_execution"}, "behavior": {"mode": "passthrough"}}]
            if name.startswith("valid"):
                ops.append({"match": {"op": "command_execution"}, "behavior": {"mode": "passthrough"}})
            cases.append({"id": f"{name}-{'resume' if resumed else 'initial'}", "type": "recipe_case",
                          "inputs": {"prompt": "Improve behavior", "instructions": "Implement", "result_schema_json": schema_json,
                                     **({"session": session_ref()} if resumed else {})},
                          "mocks": {"ops": ops}, "assertions": [{"type": "output_equals", "path": "valid", "value": name.startswith("valid")}]})
    run_suite(ROOT / "recipes/develop/agent.yaml", cases, work / "real-gates")
    print("agent: 26 real artifact/schema gate cases passed", flush=True)


def verify_real_merge(work):
    repo = repository(work, "merge-cell")
    upstream = work / "upstream.git"
    run(["git", "init", "--bare", "-q", "-b", "main", str(upstream)])
    git(repo, "remote", "add", "origin", str(upstream))
    git(repo, "push", "-q", "origin", "main")
    baseline = git(repo, "rev-parse", "HEAD")
    for text in ("initial", "revised"):
        (repo / ".c2j/recipe.txt").write_text(text + "\n")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", text)
    candidate = git(repo, "rev-parse", "HEAD")
    fixtures = work / "merge-fixture"; fixtures.mkdir()
    finish_recipe = yaml.safe_load((ROOT / "recipes/develop/finish.yaml").read_text())
    finish_recipe["state"]["states"]["merge"]["inputs"].update(repo_path=str(repo), upstream_repo=str(upstream), upstream_branch="main", local_hash=candidate)
    (fixtures / "finish.yaml").write_text(yaml.safe_dump(finish_recipe, sort_keys=False))
    cases = []
    for name, approved, verified, hash_value in [("unapproved", False, True, candidate), ("unverified", True, False, candidate), ("accepted", True, True, candidate)]:
        ops = [mock("recipe_within_resolution", {"resolved_selectors": {}}),
               {"match": {"op": "extension_execution"}, "behavior": {"mode": "passthrough"}}]
        if name == "accepted":
            ops.append({"match": {"op": "squashrebasemerge"}, "behavior": {"mode": "passthrough"}})
        cases.append({"id": name, "type": "recipe_case", "inputs": {"target_directory": ".c2j", "summary": "Verified result", "approved": approved, "verified": verified}, "mocks": {"ops": ops}, "assertions": [{"type": "output_equals", "path": "merged", "value": name == "accepted"}]})
    run_suite(fixtures / "finish.yaml", cases[:-1], work / "real-merge-rejected")
    run_suite(fixtures / "finish.yaml", cases[-1:], work / "real-merge-accepted")
    assert run(["git", "--git-dir", str(upstream), "show", "main:.c2j/recipe.txt"]) == "revised\n"
    assert run(["git", "--git-dir", str(upstream), "rev-list", "--count", "main"]).strip() == "2"
    # Upstream advancement must not rebase and publish an unverified candidate.
    (repo / ".c2j/recipe.txt").write_text("next candidate\n")
    git(repo, "add", "."); git(repo, "commit", "-qm", "next candidate")
    next_candidate = git(repo, "rev-parse", "HEAD")
    other = work / "upstream-writer"
    run(["git", "clone", "-q", str(upstream), str(other)])
    git(other, "config", "user.email", "recipe-test@example.com")
    git(other, "config", "user.name", "Recipe Test")
    (other / "app.txt").write_text("upstream changed\n")
    git(other, "add", "."); git(other, "commit", "-qm", "upstream advancement")
    git(other, "push", "-q", "origin", "main")
    upstream_tip = git(other, "rev-parse", "HEAD")
    advanced = copy.deepcopy(cases[-1]); advanced["id"] = "advanced-upstream"
    finish_recipe["state"]["states"]["merge"]["inputs"]["local_hash"] = next_candidate
    (fixtures / "finish.yaml").write_text(yaml.safe_dump(finish_recipe,sort_keys=False))
    advanced["assertions"] = []
    run_suite(fixtures / "finish.yaml", [advanced], work / "real-merge-advanced", failure_contains="fast-forward")
    assert run(["git", "--git-dir", str(upstream), "rev-parse", "main"]).strip() == upstream_tip
    print("finish: 4 real cases passed, including squash merge and advanced-upstream rejection", flush=True)


def verify_specializations(work):
    source = work / "shared-recipes"; source.mkdir()
    shutil.copytree(ROOT / "recipes/develop", source / "recipes/develop")
    git(source, "init", "-q", "-b", "main")
    git(source, "config", "user.email", "recipe-test@example.com")
    git(source, "config", "user.name", "Recipe Test")
    git(source, "add", "."); git(source, "commit", "-qm", "shared phases")
    local = work / "local-cell/.c2j/recipes"; local.mkdir(parents=True)
    for name in ("build", "evolve"):
        wrapper = yaml.safe_load((ROOT / f"{name}.yaml").read_text())
        wrapper["sequence"][0]["include"] = "git+" + source.as_uri() + "//recipes/develop/develop.yaml@main"
        path = local / f"{name}.yaml"; path.write_text(yaml.safe_dump(wrapper, sort_keys=False))
        run_suite(path, routing_cases()[:1], work / ("local-" + name))
    print("specializations: both local wrappers resolved shared git phases without sibling copies", flush=True)


def main():
    with tempfile.TemporaryDirectory(prefix="development-tests-") as temp:
        work = Path(temp)
        verify_plan_contract(work)
        verify_commands(work)
        verify_real_gates(work)
        verify_real_merge(work)
        verify_specializations(work)
        verify_routing(work)


if __name__ == "__main__":
    main()

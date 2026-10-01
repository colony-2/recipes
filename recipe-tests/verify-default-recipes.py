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
BASE = dict(status="ready", summary="Ready", blocking_issues=[], questions=[])
DESIGN = {**BASE, "design_markdown": "Add the requested behavior", "requirements": [{"id": "R1", "statement": "Requested behavior works"}]}
DESIGN.update(assessment={"assessment_status":"assessed","fit":"fits","rationale":"Owned behavior","outcomes":[{"id":"R1","statement":"Requested behavior works","ownership":"local","suggested_owner":"test","mandate_evidence":["OWN-01"],"reason":"Owned"}],"questions":[]},consultation=None,handoffs=[])
PLAN = {**BASE, "statements": [{"id": "T1", "statement": "Requested behavior works", "requirement_ids": ["R1"], "files": ["test.sh"], "importance": "high", "level": "integration", "dependencies": [], "case": "positive"}], "commands": [{"id": "check", "run": "true", "statement_ids": ["T1"], "timeout_seconds": 10}]}
IMPLEMENTATION = {**BASE, "consultation": None, "proposed_handoffs": [], "summary": "Implemented behavior", "changes": ["Requested change"], "statement_tests": [{"statement_id": "T1", "files": ["test.sh"]}]}
SNAPSHOT = {"head": HASH, "base_hash": HASH, "target_directory": ".", "files": [], "clean": True}


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


def phase(result, *, valid=True, status="completed", session="implementation-session"):
    ops = [mock("extension_execution", {"status": status, "sessionId": session, **({"session": session_ref(session)} if session else {})}, {"result.json": json.dumps(result)}), mock("extension_execution", {"ok": valid})]
    if valid:
        ops.append(command(result))
    if "design_markdown" in result:
        ops.insert(0, command({"cell":"test","valid":True}))
        if valid: ops.append(command({"result":result,"selection":{}}, artifacts={"design.md": result["design_markdown"]}))
    if "statement_tests" in result and valid and status in ("completed", "incomplete"):
        ops.append(command({"result":result,"selection":{}}, artifacts={"implementation.md": result["summary"]}))
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
    item = command({"ok": ok, "candidate_hash": HASH, "checks": [{"id": "check", "exit_code": 0 if ok else 1}], "candidate_unchanged": True})
    item["behavior"]["artifacts"] = {"check-1.log": "Executed verification evidence", "verification.md": "# Verification"}
    return [item]


def finish():
    return [response("satisfied"), command(SNAPSHOT), mock("extension_execution", {"ok": True}), mock("squashrebasemerge", {"merged_hash": "merged-hash", "target_branch": "main"})]


def case(name, ops, merged=True):
    return {"id": name, "type": "recipe_case", "inputs": {"prompt": "Improve requested behavior"}, "mocks": {"ops": [mock("recipe_within_resolution", {"resolved_selectors": {}}), command(SNAPSHOT)] + ops}, "assertions": [{"type": "output_equals", "path": "merged", "value": merged}]}


def routing_cases():
    start = planning() + [response("approve")]
    end = implementation() + verification() + finish()
    cases = [case("happy", start + end)]
    cases += [case("direct-plan-feedback", planning() + [response("revise", "Clarify outcomes")] + start + end)]
    cases += [case("direct-implementation-feedback", start + implementation() + verification() + [response("revise", "Direct revision")] + end)]
    cases += [case("direct-redesign", start + implementation() + verification() + [response("redesign", "Change scope")] + start + end)]
    cases += [case("repeat-feedback", start + implementation("First outcome") + verification() + [response("revise"), feedback("Add coverage")] + implementation("Second outcome") + verification() + [response("revise"), feedback("Handle empty input")] + implementation("Final outcome") + verification() + finish())]
    cases += [case("redesign", start + implementation() + verification() + [response("redesign"), feedback("Change the requirements")] + start + end)]
    cases += [case("implementation-requests-redesign", start + phase({**IMPLEMENTATION,"status":"redesign","questions":["Approve the new external dependency"]}) + [feedback("Review the external work")] + start + end)]
    cases += [case("human-rejects-plan", planning() + [response("revise"), feedback()] + start + end)]
    for name, prefix in [
        ("design-needs-input", phase({**DESIGN, "status": "needs_input", "questions": ["Which behavior?"]})),
        ("design-review-rejects", phase(DESIGN) + phase({**BASE, "status": "revise", "blocking_issues": ["Missing requirement"]})),
        ("test-review-rejects", phase(DESIGN) + phase(BASE) + phase(PLAN) + [command({"ok": True}, artifacts={"test-statements.md": "# Test statements"})] + phase({**BASE, "status": "revise", "blocking_issues": ["Missing coverage"]})),
        ("test-contract-rejects", phase(DESIGN) + phase(BASE) + phase(PLAN) + [command({}, False)]),
        ("contradictory-review", phase(DESIGN) + phase({**BASE, "blocking_issues": ["Still blocked"]})),
    ]:
        cases.append(case(name, prefix + [feedback()] + start + end))
    for name, prefix in [
        ("implementation-incomplete", phase({**IMPLEMENTATION, "status": "needs_input", "questions": ["Need clarification"]}, status="incomplete")),
        ("specification-rejects", phase(IMPLEMENTATION) + phase({**BASE, "status": "revise", "blocking_issues": ["Missing behavior"]})),
        ("quality-rejects", phase(IMPLEMENTATION) + phase(BASE) + phase({**BASE, "status": "revise", "blocking_issues": ["Incorrect edge case"]})),
        ("verification-fails", implementation() + verification(False)),
    ]:
        cases.append(case(name, start + prefix + [feedback()] + end))
    cases += [case("invalid-human-input", planning() + [response("invalid"), response("approve")] + implementation() + verification() + [response("invalid"), response("revise"), feedback(" "), feedback("Fix this")] + end)]
    for name, prefix in [
        ("invalid-design-artifact", phase(DESIGN, valid=False)),
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
                if "/implementation/" not in path:
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
    code = script("test-plan.yaml", "contract")
    for change in ("valid", "duplicate", "too-long", "unknown-requirement", "uncovered-requirement", "no-command", "unverified", "unknown-statement", "missing-negative", "bad-filename"):
        plan = copy.deepcopy(PLAN); design = copy.deepcopy(DESIGN)
        if change == "duplicate": plan["statements"] *= 2
        if change == "too-long": plan["statements"][0]["statement"] = "word " * 31
        if change == "unknown-requirement": plan["statements"][0]["requirement_ids"] = ["R99"]
        if change == "uncovered-requirement": design["requirements"].append({"id": "R2", "statement": "Other behavior"})
        if change == "no-command": plan["commands"] = []
        if change == "unverified": plan["statements"].append({**plan["statements"][0], "id": "T2"})
        if change == "unknown-statement": plan["commands"][0]["statement_ids"] = ["T99"]
        if change == "missing-negative": plan["statements"][0]["importance"] = "critical"
        if change == "bad-filename": plan["statements"][0]["files"] = ["../app.txt"]
        out = work / ("plan-" + change); out.mkdir()
        command_test(code, {"PLAN_JSON": json.dumps(plan), "DESIGN_CONTEXT": json.dumps({"design": design}), "OUTBOX": str(out)}, ok=change == "valid")
        if change == "valid": assert "**T1**" in (out / "test-statements.md").read_text()
    print("test plan: 10 real contract cases passed", flush=True)


def verify_commands(work):
    code = script("verify.yaml")
    for change in ("pass", "fail", "timeout", "missing", "unmapped", "tracked-mutation", "untracked-mutation", "mixed-evidence"):
        repo = repository(work, "verify-" + change)
        plan = copy.deepcopy(PLAN); implementation = copy.deepcopy(IMPLEMENTATION)
        commands = {"pass": "printf 'verified output\\n'", "fail": "exit 7", "timeout": "sleep 5", "tracked-mutation": "echo bad > recipe.txt", "untracked-mutation": "touch unexpected.txt"}
        plan["commands"][0]["run"] = commands.get(change, "true")
        plan["commands"][0]["timeout_seconds"] = 1
        if change == "mixed-evidence": plan["commands"].append({**plan["commands"][0], "id": "failed-check", "run": "exit 8"})
        if change == "missing": plan["commands"] = []
        if change == "unmapped": implementation["statement_tests"] = []
        out = work / ("evidence-" + change); out.mkdir()
        value = command_test(code, {"CELL_ROOT": str(repo), "TARGET_DIRECTORY": ".c2j", "PLAN_JSON": json.dumps(plan), "IMPLEMENTATION_JSON": json.dumps(implementation), "OUTBOX": str(out)}, ok=change not in ("missing", "unmapped"))
        if value is not None:
            assert value["ok"] == (change == "pass"), value
            assert value["candidate_hash"] == git(repo, "rev-parse", "HEAD")
            assert (out / value["checks"][0]["log"]).exists()
            if change == "mixed-evidence": assert "FAILED" in value["report_markdown"]
    print("verification: 8 real command/evidence cases passed", flush=True)



def verify_real_gates(work):
    role = yaml.safe_load((ROOT / "recipes/develop/implement.yaml").read_text())
    schema_json = json.dumps(role["vars"]["result_schema"])
    invalid = {
        "missing": None,
        "malformed": "not json",
        "missing-field": json.dumps({"summary": "Incomplete result"}),
        "blank-summary": json.dumps({**IMPLEMENTATION, "summary": "  "}),
        "wrong-type": json.dumps({**IMPLEMENTATION, "changes": "string"}),
        "extra-field": json.dumps({**IMPLEMENTATION, "unexpected": True}),
    }
    cases = []
    for resumed in (False, True):
        for name, raw in {"valid": json.dumps(IMPLEMENTATION), **invalid}.items():
            ops = [mock("recipe_within_resolution", {"resolved_selectors": {}}), mock("extension_execution", {"status": "completed", "sessionId": "session", "session": session_ref()}, {} if raw is None else {"result.json": raw}),
                   {"match": {"op": "extension_execution"}, "behavior": {"mode": "passthrough"}}]
            if name == "valid":
                ops.append({"match": {"op": "command_execution"}, "behavior": {"mode": "passthrough"}})
            cases.append({"id": f"{name}-{'resume' if resumed else 'initial'}", "type": "recipe_case",
                          "inputs": {"prompt": "Improve behavior", "instructions": "Implement", "result_schema_json": schema_json,
                                     **({"session": session_ref()} if resumed else {})},
                          "mocks": {"ops": ops}, "assertions": [{"type": "output_equals", "path": "valid", "value": name == "valid"}]})
    run_suite(ROOT / "recipes/develop/agent.yaml", cases, work / "real-gates")
    print("agent: 14 real artifact/schema gate cases passed", flush=True)


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
    snapshot = yaml.safe_load((ROOT / "recipes/develop/snapshot.yaml").read_text())
    snapshot["sequence"][0]["inputs"]["env"]["CELL_ROOT"] = str(repo)
    (fixtures / "snapshot.yaml").write_text(yaml.safe_dump(snapshot, sort_keys=False))
    finish_recipe = yaml.safe_load((ROOT / "recipes/develop/finish.yaml").read_text())
    finish_recipe["state"]["states"]["merge"]["inputs"].update(repo_path=str(repo), upstream_repo=str(upstream), upstream_branch="main")
    (fixtures / "finish.yaml").write_text(yaml.safe_dump(finish_recipe, sort_keys=False))
    cases = []
    for name, approved, verified, hash_value in [("unapproved", False, True, candidate), ("unverified", True, False, candidate), ("stale-candidate", True, True, baseline), ("accepted", True, True, candidate)]:
        ops = [mock("recipe_within_resolution", {"resolved_selectors": {}}),
               {"match": {"op": "command_execution"}, "behavior": {"mode": "passthrough"}},
               {"match": {"op": "extension_execution"}, "behavior": {"mode": "passthrough"}}]
        if name == "accepted":
            ops.append({"match": {"op": "squashrebasemerge"}, "behavior": {"mode": "passthrough"}})
        cases.append({"id": name, "type": "recipe_case", "inputs": {"target_directory": ".c2j", "candidate_hash": hash_value, "summary": "Verified result", "approved": approved, "verified": verified}, "mocks": {"ops": ops}, "assertions": [{"type": "output_equals", "path": "merged", "value": name == "accepted"}]})
    run_suite(fixtures / "finish.yaml", cases[:-1], work / "real-merge-rejected")
    dirty = copy.deepcopy(cases[-1]); dirty["id"] = "dirty-candidate"
    dirty["assertions"][0]["value"] = False
    dirty["mocks"]["ops"].pop()
    (repo / ".c2j/recipe.txt").write_text("unverified dirty change\n")
    run_suite(fixtures / "finish.yaml", [dirty], work / "real-merge-dirty")
    git(repo, "restore", ".c2j/recipe.txt")
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
    advanced["inputs"].update(candidate_hash=next_candidate)
    advanced["assertions"] = []
    run_suite(fixtures / "finish.yaml", [advanced], work / "real-merge-advanced", failure_contains="fast-forward")
    assert run(["git", "--git-dir", str(upstream), "rev-parse", "main"]).strip() == upstream_tip
    print("finish: 6 real cases passed, including squash merge and advanced-upstream rejection", flush=True)


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

# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Dependency graph tests plus real broker submission against a separate JobDB.

The server uses JobDB's in-memory runtime, never the user's embedded database.
Codex decisions come from an object-producing fixture; all child submissions, captured
jobs metadata, awaits, artifacts and worker resumption use real c2j operations.
"""
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
import urllib.request

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("defaults", ROOT / "recipe-tests/verify-default-recipes.py")
defaults = importlib.util.module_from_spec(spec)
spec.loader.exec_module(defaults)
run = defaults.run


def passthrough(op):
    return {"match": {"op": op}, "behavior": {"mode": "passthrough"}}


def outcome(job, status="completed", outputs=None):
    return {"job_id": job, "terminal": True, "status": status, "outputs": outputs or {}, "artifacts": {},
            "failure_kind": "", "failure_message": "", "started_at": "", "finished_at": "",
            "partial_outputs_available": False, "partial_artifacts_available": False}


def verify_wait(work):
    cases = []
    for name, ids, history, children, ok in [
        ("none", [], {}, [], True),
        ("success", ["a"], {}, [outcome("a")], True),
        ("multiple-unordered-duplicates", ["b", "a", "b"], {}, [outcome("a"), outcome("b")], True),
        ("already-recorded", ["a"], {"a": outcome("a")}, [], True),
        ("new-round", ["b"], {"a": outcome("a")}, [outcome("b")], True),
        ("failed", ["a"], {}, [outcome("a", "failed")], False),
        ("cancelled", ["a"], {}, [outcome("a", "cancelled")], False),
        ("unmerged", ["a"], {}, [outcome("a", outputs={"merged": False})], False),
        ("merged", ["a"], {}, [outcome("a", outputs={"merged": True})], True),
        ("wait-after-failure", ["a", "b"], {}, [outcome("a", "failed"), outcome("b")], False),
    ]:
        ops = []
        for child in children:
            ops += [defaults.mock("recipe.await_result_soft", child)]
        expected = {**history, **{c["job_id"]: c for c in children}}
        cases.append({"id": name, "type": "recipe_case", "inputs": {"job_ids_json": json.dumps(ids), "history_json": json.dumps(history)},
                      "mocks": {"ops": ops}, "assertions": [{"type": "output_equals", "path": "ok", "value": ok},
                      {"type": "output_equals", "path": "results", "value": expected}]})
    defaults.run_suite(ROOT / "recipes/develop/wait-children.yaml", cases, work / "wait", parallelism=4)
    print("dependencies: 10 native await/expression cases passed", flush=True)


def request(url, method=None):
    with urllib.request.urlopen(urllib.request.Request(url, method=method), timeout=10) as response:
        data = response.read()
        return json.loads(data) if data else None


def eventually(check, timeout=60):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = check()
        if last:
            return last
        time.sleep(.1)
    raise AssertionError(f"Timed out: {last}")


def write_yaml(path, value):
    path.write_text(yaml.safe_dump(value, sort_keys=False))


def verify_service(work, scenario='success'):
    work.mkdir(exist_ok=True)
    binary = work / "jobdb-service"
    run(["go", "build", "-o", str(binary), "."], cwd=ROOT / "recipe-tests/jobdb-service")
    with (work / "server.log").open("w") as server_log:
        server = subprocess.Popen([str(binary)], stdout=subprocess.PIPE, stderr=server_log, text=True)
        processes = []
        logs = []
        try:
            assert select.select([server.stdout], [], [], 20)[0], "JobDB did not start"
            url = server.stdout.readline().strip()
            assert url.startswith("http://127.0.0.1:")
            uri = url + "/test"
            (work / "service-url").write_text(url)
            # The test's top-level jobs must not inherit a caller's live broker.
            # Workers inject fresh broker context into the fixture commands.
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith(('C2J_CURRENT_', 'C2J_CHILD_JOB_')) and k != 'C2J_TENANT_ID'}
            env.update(C2J_JOBDB=uri, TMPDIR=str(work))
            repo = defaults.repository(work, "parent-cell")
            child_repo = defaults.repository(work, "child-cell")
            child = {"id": "fixture-child", "input_schema": {"prompt": {"type": "string"}, "release": {"type": "string"}},
                     "inputs": {"release": "${{ inputs.release }}"}, "sequence": [{"id": "work", "op": "command_execution", "inputs": {
                     "env": {"RELEASE": "${{ inputs.release }}", "OUTBOX": "{{ context.environment.op.outbox }}"},
                     "timeout": "60s", "run": "while [ ! -f \"$RELEASE\" ]; do sleep 0.1; done\nprintf 'dependency evidence' > \"$OUTBOX/evidence.txt\""}}], "outputs": {"merged": True, "value": "dependency ready"}}
            child_path = work / "child.yaml"
            recovery_path = work / "recovery.yaml"
            write_yaml(recovery_path, child)
            if scenario == 'failed':
                # Keep evidence from a completed op available before failing.
                child['sequence'].append({'id': 'fail', 'op': 'command_execution', 'inputs': {'run': 'exit 1'}})
            if scenario == 'unmerged':
                child['outputs']['merged'] = False
            write_yaml(child_path, child)
            fixture = work / "fixture"; shutil.copytree(ROOT / "recipes/develop", fixture)
            agent = yaml.safe_load((fixture / "agent.yaml").read_text())
            # Only model decisions are substituted; session objects and child jobs are real.
            model_inputs = {"timeout": "60s", "env": {
                    "INBOX": "{{ context.environment.op.inbox }}", "OUTBOX": "{{ context.environment.op.outbox }}",
                    "CHILD_CELL": str(child_repo), "CHILD_RECIPE": str(child_path), "RELEASE": str(work / "release"),
                    "RECOVERY_RECIPE": str(recovery_path),
                    "C2J_JOBDB": uri, "TRACE": str(work / "agent-trace.jsonl"), "SCENARIO": scenario,
                    "OP_RELEASE": str(work / 'op-release')}, "run": '''python3 - <<'PY'
import json, os, pathlib, subprocess, time
inbox=pathlib.Path(os.environ['INBOX']); outbox=pathlib.Path(os.environ['OUTBOX'])
context=json.loads(os.environ['CONTEXT_JSON'])
with open(os.environ['TRACE'],'a') as f: f.write(json.dumps({'session':os.environ['SESSION'],'context':context})+'\\n')
dependencies=context.get('dependencies',{})
if not os.environ['SESSION'] or (os.environ['SCENARIO']=='rounds' and len(dependencies)==2):
    for _ in range(2 if not os.environ['SESSION'] else 1):
        subprocess.run(['c2j','submit','Supporting change','--recipe-file',os.environ['CHILD_RECIPE'],
            '--cell',os.environ['CHILD_CELL'],'--inputs-json',json.dumps({'release':os.environ['RELEASE']}),'--json'],check=True)
    if os.environ['SCENARIO']=='already-finished':
        while not pathlib.Path(os.environ['OP_RELEASE']).exists(): time.sleep(.1)
else:
    assert os.environ['SESSION']=='fixture-session'
    scenario=os.environ['SCENARIO']
    assert len(dependencies) in ((2,3) if scenario=='failed' else (3,) if scenario=='rounds' else (2,))
    statuses=[r['status'] for r in dependencies.values()]
    if scenario=='failed':
        assert statuses.count('failed')==2
        assert all(r['failure_message'] for r in dependencies.values() if r['status']=='failed')
        if len(dependencies)==3: assert statuses.count('completed')==1
    elif scenario=='cancelled':
        assert sorted(statuses)==['cancelled','completed']
    else:
        assert all(status=='completed' for status in statuses)
    evidence=list((inbox/'dependencies').rglob('evidence.txt'))
    assert len(evidence)==sum(len(r['artifacts']) for r in dependencies.values()), evidence
    assert all(p.read_text()=='dependency evidence' for p in evidence)
    if scenario=='failed' and len(dependencies)==2:
        subprocess.run(['c2j','submit','Correct the diagnosed dependency failure','--recipe-file',os.environ['RECOVERY_RECIPE'],
            '--cell',os.environ['CHILD_CELL'],'--inputs-json',json.dumps({'release':os.environ['RELEASE']}),'--json'],check=True)
result={'status':'ready','summary':'Integrated child outcomes' if os.environ['SESSION'] else 'Submitted dependencies','blocking_issues':[],'questions':[]}
if os.environ['SESSION']:
    if os.environ['SCENARIO']=='failed':
        result['summary']='Resolved failure with corrected dependency' if len(dependencies)==3 else 'Requested corrected dependency'
    elif os.environ['SCENARIO']=='cancelled':
        result['summary']='Resolved cancellation using an existing compatible interface'
    elif os.environ['SCENARIO']=='unmerged':
        assert all(r['outputs']['merged'] is False for r in dependencies.values())
        result.update(status='needs_input', summary='Dependency integration needs a decision', questions=['Which upstream should receive the dependency?'])
if os.environ['SCENARIO']=='invalid-result': del result['summary']
(outbox/'result.json').write_text(json.dumps(result))
PY
'''}
            code=model_inputs['run'].split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
            code+="\nprint(json.dumps({'status':'completed','sessionId':'fixture-session','_omit_session':os.environ['SCENARIO']=='missing-session'}))\n"
            agent=defaults.objects.replace(yaml.safe_load((ROOT/'recipes/develop/agent.yaml').read_text()),fixture,model_inputs['env'],code)
            write_yaml(fixture / "agent.yaml", agent)
            submitted = json.loads(run(["c2j", "submit", "Dependency test", "--recipe-file", str(fixture / "agent.yaml"), "--cell", str(repo),
                "--inputs-json", json.dumps({"instructions": "Fixture", "result_schema_json": json.dumps({"type":"object", "required":list(defaults.BASE)}),
                    "mode": "evolve" if scenario == 'scoped' else 'build', "target_directory": '.c2j' if scenario == 'scoped' else '.'}), "--json"], env=env))
            parent = submitted["job_id"]
            (work / "parent-id").write_text(parent)
            log = (work / "parent.log").open("w"); logs.append(log)
            worker = subprocess.Popen(["c2j", "run", "one", "--job-id", parent, "--await-threshold", "2s", "--poll-interval", "100ms", "--wait-timeout", "90s"], env=env, stdout=log, stderr=log)
            processes.append(worker)
            def children():
                data = json.loads(run(["c2j", "list", "children", "--parent-tenant-id", "test", "--parent-job-id", parent, "--all-ops", "--all", "--status", "READY,ACTIVE,PENDING_JOBS,COMPLETED,CANCELLED", "--json"], env=env))
                return data
            data = eventually(lambda: (value if len(value.get('jobs', [])) == 2 else None) if (value := children()) else None)
            ids = sorted(c['job_id'] for c in data['jobs'])
            assert len(set(ids)) == 2
            assert all(c['parent']['job_id'] == parent and c['cell_name'] == 'child-cell' for c in data['jobs'])
            inspect = lambda: request(url + '/test/job?id=' + parent)
            trace = lambda: [json.loads(line) for line in (work / 'agent-trace.jsonl').read_text().splitlines()]
            if scenario != 'already-finished':
                eventually(lambda: inspect()['Job']['Status'] == 'PENDING_JOBS')
            assert len(trace()) == 1, 'Parent resumed before children completed'
            # Parent releases its lease on wait; a replacement worker must replay
            # captured IDs without running the submission command again.
            if scenario != 'already-finished':
                worker.terminate(); worker.wait(timeout=10)
            if scenario == 'cancelled':
                request(url + '/test/cancel?id=' + ids[0], 'POST')
            active_ids = ids[1:] if scenario == 'cancelled' else ids
            for job in active_ids:
                log = (work / (job + '.log')).open('w'); logs.append(log)
                processes.append(subprocess.Popen(['c2j', 'run', 'one', '--job-id', job], env=env, stdout=log, stderr=log))
            eventually(lambda: all(request(url + '/test/job?id=' + job)['Job']['Status'] == 'ACTIVE' for job in active_ids))
            assert len(trace()) == 1
            (work / 'release').touch()
            for process in processes[1:]:
                assert (process.wait(timeout=45) == 0) == (scenario != 'failed')
            if scenario == 'already-finished':
                (work / 'op-release').touch()
                resumed = worker
            else:
                log = (work / 'resumed-parent.log').open('w'); logs.append(log)
                resumed = subprocess.Popen(['c2j', 'run', 'one', '--job-id', parent, '--poll-interval', '100ms', '--wait-timeout', '60s'], env=env, stdout=log, stderr=log)
                processes.append(resumed)
            if scenario in ('rounds', 'failed'):
                new_children = eventually(lambda: (value if len(value['jobs']) == 3 else None) if (value := children()) else None)
                new_id = (set(c['job_id'] for c in new_children['jobs']) - set(ids)).pop()
                run(['c2j','run','one','--job-id',new_id], env=env, timeout=45)
                ids.append(new_id)
            assert resumed.wait(timeout=60) == 0
            final = inspect()
            (work / 'final.json').write_text(json.dumps(final, indent=2))
            assert final['Job']['Status'] == 'COMPLETED', final
            result = final['Attempts'][-1]['Output']['Data']
            session_resumed = scenario not in ('missing-session', 'invalid-result')
            assert len(trace()) == (3 if scenario in ('rounds', 'failed') else 2 if session_resumed else 1), trace()
            assert result['valid'] == (scenario not in ('missing-session','invalid-result')), result
            assert result['completed'] == (scenario not in ('missing-session', 'invalid-result')), result
            assert set(result['dependencies']) == set(ids), result
            if session_resumed:
                assert all(t['session'] == 'fixture-session' for t in trace()[1:])
                assert set(trace()[-1]['context']['dependencies']) == set(ids)
                # The final decision belongs to the resumed session, not a
                # recipe-generated failure response or the pre-wait result.
                if scenario == 'unmerged':
                    assert result['result']['status'] == 'needs_input', result
                    assert result['result']['questions'] == ['Which upstream should receive the dependency?'], result
                else:
                    assert result['result']['status'] == 'ready' and not result['result']['questions'], result
                    expected_summary = {'failed': 'Resolved failure with corrected dependency',
                                        'cancelled': 'Resolved cancellation using an existing compatible interface'}.get(scenario, 'Integrated child outcomes')
                    assert result['result']['summary'] == expected_summary, result
            assert sorted(c['job_id'] for c in children()['jobs']) == sorted(ids), 'Replay duplicated children'
            if scenario == 'feedback-history':
                followup = json.loads(run(['c2j','submit','Revisit the phase after human feedback','--recipe-file',str(fixture / 'agent.yaml'),
                    '--cell',str(repo),'--inputs-json',json.dumps({'instructions':'Fixture','result_schema_json':'{}',
                    'session':result['session'],'dependency_history_json':json.dumps(result['dependencies']),
                    'feedback':'Keep the completed dependency and revise this cell only'}),'--json'],env=env))
                run(['c2j','run','one','--job-id',followup['job_id']],env=env,timeout=45)
                assert len(trace()) == 3 and set(trace()[-1]['context']['dependencies']) == set(ids)
                retained=request(url+'/test/job?id='+followup['job_id'])['Attempts'][-1]['Output']['Data']
                assert retained['dependencies'] == result['dependencies'] and retained['valid']
                assert json.loads(run(['c2j','list','children','--parent-tenant-id','test','--parent-job-id',followup['job_id'],
                    '--all-ops','--all','--json'],env=env))['jobs'] == []
            print(f'service: {scenario} passed', flush=True)
        finally:
            try:
                if 'parent' in locals():
                    (work / "job.log").write_text(json.dumps(request(url + '/test/job?id=' + parent), indent=2))
            finally:
                for process in processes:
                    process.terminate()
                for process in processes:
                    try: process.wait(timeout=10)
                    except subprocess.TimeoutExpired: process.kill(); process.wait()
                server.terminate(); server.wait(timeout=10)
                for log in logs: log.close()


def main():
    with tempfile.TemporaryDirectory(prefix="dependency-tests-") as temp:
        work = Path(temp)
        try:
            verify_wait(work)
            for scenario in ('success', 'scoped', 'rounds', 'failed', 'cancelled', 'unmerged', 'missing-session', 'invalid-result', 'already-finished', 'feedback-history'):
                verify_service(work / scenario, scenario)
        except Exception:
            for path in (work / scenario if 'scenario' in locals() else work).rglob("*.log"):
                if path.name != 'job.log':
                    print(f"{path.relative_to(work)}:\n{path.read_text()[-5000:]}")
            raise


if __name__ == "__main__":
    main()

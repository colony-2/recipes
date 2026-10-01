# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Real implementation/foreign-cell dialogue with only model turns substituted."""
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

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('consultations', ROOT/'recipe-tests/verify-consultations.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
d, deps, e = c.d, c.deps, c.e


def verify_live(work, binary, scenario):
    work.mkdir()
    server = subprocess.Popen([str(binary)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    worker = None
    try:
        assert select.select([server.stdout], [], [], 20)[0]
        url = server.stdout.readline().strip()
        env = {k: v for k, v in os.environ.items() if not k.startswith(('C2J_CURRENT_', 'C2J_CHILD_JOB_')) and k != 'C2J_TENANT_ID'}
        env.update(C2J_JOBDB=url+'/test', TMPDIR=str(work))
        cells = {role: c.seed(work, 'cell-'+role.lower()) for role in ('A', 'B', 'C')}
        for role, repo in cells.items():
            (repo/'AGENTS.md').write_text('Instructions for cell-'+role.lower()+'\n')
            if scenario == 'missing-mandate' and role == 'B':
                (repo/'.c2j/mandate.md').unlink()
            d.git(repo, 'add', '.'); d.git(repo, 'commit', '-qm', 'Cell-specific instructions')
        heads = {role: d.git(repo, 'rev-parse', 'HEAD') for role, repo in cells.items()}
        fixture = work/'recipes'; shutil.copytree(ROOT/'recipes/develop', fixture)
        history = {'previous-child': deps.outcome('previous-child', 'failed' if scenario == 'failed-dependency' else 'completed', outputs={'value': 'previous evidence'})}
        illegal_recipe = work/'illegal-child.yaml'
        c.write(illegal_recipe, {'id':'unexpected-work', 'input_schema':{'prompt':{'type':'string'}},
                                'sequence':[{'op':'command_execution','inputs':{'run':'true'}}]})
        target = '.c2j' if scenario == 'evolve' else '.'
        common = {'INBOX': '{{ context.environment.op.inbox }}', 'OUTBOX': '{{ context.environment.op.outbox }}',
                  'WORKTREE': '{{ context.environment.op.worktree_path }}', 'WORKSPACE': '{{ context.workspace.cell }}',
                  'OWNER': '{{ context.workflow.cell }}',
                  'SCENARIO': scenario, 'ILLEGAL_RECIPE': str(illegal_recipe), 'TRACE': str(work/'trace.jsonl'), 'TARGET': target,
                  'DEPENDENCIES_JSON': json.dumps(history), 'MISSING_CELL': (work/'missing-repository').as_uri(),
                  **{role+'_CELL': str(repo) for role, repo in cells.items()},
                  **{role+'_HEAD': value for role, value in heads.items()}}
        code=(ROOT/'recipe-tests/fixtures/implementation-conversation-model.py').read_text()
        agent=d.objects.replace(c.read('agent.yaml'),fixture,{**common,'ROLE':e('inputs.instructions.startsWith("Implement") ? "I" : "D"')},code)
        c.write(fixture/'agent.yaml',agent)
        foreign=d.objects.replace(c.read('consult.yaml'),fixture,{**common,'ROLE':e('context.workspace.cell == "cell-c" ? "C" : "B"')},code)
        c.write(fixture/'consult.yaml',foreign)
        impl_inputs = {'prompt': 'Implement client behavior', 'target_directory': target,
                       'mode': 'evolve' if scenario == 'evolve' else 'build',
                       'context_json': json.dumps({'design': d.DESIGN, 'test_plan': d.PLAN}),
                       'dependency_history_json': json.dumps(history)}
        nodes = []
        if scenario == 'reuse':
            nodes.append({'id': 'design', 'include': str(fixture/'design.yaml'), 'inputs': {'prompt': 'Implement client behavior'}})
            impl_inputs.update(consultation_history_json=e('json_stringify(sequence.design.outputs.consultations)'),
                               context_json=e("'{\"design\":' + json_stringify(sequence.design.outputs.result) + '}'"))
        nodes.append({'id': 'implementation', 'include': str(fixture/('design.yaml' if scenario=='design' else 'implement.yaml')), 'inputs': {**impl_inputs, **({'dependency_history_json':'{}'} if scenario=='design' else {})}})
        output_node = 'implementation'
        if scenario == 'feedback':
            nodes.append({'id': 'revision', 'include': str(fixture/'implement.yaml'), 'inputs': {
                **impl_inputs, 'feedback': 'Ask the dependency owner a follow-up question',
                'session': e('sequence.implementation.outputs.session'),
                'consultation_history_json': e('json_stringify(sequence.implementation.outputs.consultations)'),
                'dependency_history_json': e('json_stringify(sequence.implementation.outputs.dependencies)')}})
            output_node = 'revision'
        wrapper = work/'workflow.yaml'
        c.write(wrapper, {'id': 'late-consultation', 'input_schema': {'prompt': {'type':'string'}}, 'sequence': nodes,
                          'outputs': {'implementation': e('sequence.'+output_node+'.outputs')}})
        job = json.loads(d.run(['c2j', 'submit', 'Late dependency discovery', '--recipe-file', str(wrapper),
                               '--cell', str(cells['A']), '--json'], env=env))['job_id']
        log_path = work/'worker.log'
        with log_path.open('w') as log:
            worker = subprocess.Popen(['c2j', 'run', 'one', '--job-id', job], env=env, stdout=log, stderr=log)
            code = worker.wait(timeout=120)
        if code != 0 and os.environ.get('C2J_TEST_LOG_DIR'):
            destination=Path(os.environ['C2J_TEST_LOG_DIR']); destination.mkdir(parents=True,exist_ok=True)
            shutil.copy(log_path, destination/(scenario+'.log'))
        final = deps.request(url+'/test/job?id='+job)
        errors = (work/'trace.jsonl.errors').read_text() if (work/'trace.jsonl.errors').exists() else ''
        assert (work/'trace.jsonl').exists(), errors + log_path.read_text()[-5000:]
        rows = [json.loads(line) for line in (work/'trace.jsonl').read_text().splitlines()]
        assert not errors, errors
        if scenario == 'unavailable':
            assert code != 0, (scenario, final)
            assert all(r['role'] == 'I' for r in rows), 'Resolution failure silently fell back to A'
            assert 'workspace' in log_path.read_text().lower()
        else:
            assert code == 0, log_path.read_text()[-8000:]
            result = final['Attempts'][-1]['Output']['Data']['implementation']
            if scenario in ('malformed', 'missing-session', 'missing-checkpoint', 'illegal-children'):
                assert not result['valid'], result
                assert [r['role'] for r in rows] == ['I', 'B'], rows
            else:
                assert result['valid'] and result['completed'] and result['session_id'] == ('D-session' if scenario=='design' else 'I-session'), result
                expected = 'redesign' if scenario in ('bug', 'evolve', 'reuse') else 'ask_user' if scenario in ('missing-mandate', 'outside') else 'review'
                assert result['result']['next'] == expected, result
                assert result['dependencies'] == ({} if scenario=='design' else history)
                if expected == 'redesign':
                    assert 'approve external work' in result['result']['summary']
                if scenario == 'design':
                    assert [r['role'] for r in rows] == ['D','B','D','B','D']
                    assert [r['session'] for r in rows if r['role']=='B'] == ['', 'B-session']
                if scenario == 'multiple':
                    assert [r['role'] for r in rows] == ['I','B','I','C','I','B','I']
                if scenario == 'reuse':
                    assert [r['role'] for r in rows] == ['D','B','D','I','B','I']
                    assert [r['session'] for r in rows if r['role'] == 'B'] == ['', 'B-session']
                if scenario == 'feedback':
                    assert [r['session'] for r in rows if r['role'] == 'I'] == ['', 'I-session', 'I-session', 'I-session']
                for key, thread in result['consultations'].items():
                    assert key in [str(repo) for repo in cells.values()]
                    assert set(thread) == {'session','response'}
                    assert thread['session']['type']=='c2ops.codex.session/v1' and 'session_artifacts' not in thread
        children = json.loads(d.run(['c2j','list','children','--parent-tenant-id','test','--parent-job-id',job,
                                     '--all-ops','--all','--status','READY,ACTIVE,PENDING_JOBS,COMPLETED,CANCELLED','--json'], env=env))['jobs']
        if scenario == 'illegal-children':
            assert len(children) == 1, children
        else:
            assert children == [], 'Discussion submitted unapproved external work'
        for role, repo in cells.items():
            assert not (repo/'experiment.txt').exists()
            assert (repo/'app.txt').read_text() == 'application\n'
            assert d.git(repo, 'status', '--porcelain') == ''
        assert d.git(cells['A'], 'rev-parse', 'HEAD') == heads['A']
        print('live implementation consultation: '+scenario+' passed', flush=True)
    finally:
        if worker and worker.poll() is None:
            worker.terminate(); worker.wait(timeout=10)
        server.terminate(); server.wait(timeout=10)


def main():
    with tempfile.TemporaryDirectory(prefix='implementation-dialogues-') as temp:
        work = Path(temp); binary = work/'jobdb-service'
        d.run(['go','build','-o',str(binary),'.'], cwd=ROOT/'recipe-tests/jobdb-service')
        failures = []
        scenarios = sys.argv[1:] or ['advice','bug','evolve','multiple','reuse','feedback','missing-mandate','outside','failed-dependency',
                                    'malformed','missing-session','missing-checkpoint','illegal-children','unavailable','design']
        for scenario in scenarios:
            try: verify_live(work/scenario, binary, scenario)
            except Exception as error:
                print(f'FAILED {scenario}: {error}', flush=True); failures.append(scenario)
        assert not failures, 'Failed live scenarios: '+', '.join(failures)

if __name__ == '__main__': main()

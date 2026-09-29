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


def model_node(original, env, *, const=False):
    # Only substitute the model invocation. Callers adapt its command stdout
    # into Codex output fields without replacing any production gate conditions.
    return {'op': 'command_execution', 'const': const,
            'inputs': {'env': env, 'timeout': '20s',
                       'run': "python3 - 2>>\"${TRACE}.errors\" <<'MODEL'\n" +
                              (ROOT/'recipe-tests/fixtures/implementation-conversation-model.py').read_text() + '\nMODEL\n'},
            'artifacts': copy.deepcopy(original.get('artifacts', {}))}


def command_outputs(value, states):
    if isinstance(value, dict): return {k: command_outputs(v, states) for k, v in value.items()}
    if isinstance(value, list): return [command_outputs(v, states) for v in value]
    if isinstance(value, str):
        for state in states:
            for field in ['status', '?sessionId', 'sessionId']:
                value=value.replace(f'states.{state}.outputs.{field}', f'json_parse(states.{state}.outputs.stdout).{field}')
    return value


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
        target = '.c2j' if scenario == 'evolve' else '.'
        common = {'INBOX': '{{ context.environment.op.inbox }}', 'OUTBOX': '{{ context.environment.op.outbox }}',
                  'WORKTREE': '{{ context.environment.op.worktree_path }}', 'WORKSPACE': '{{ context.workspace.cell }}',
                  'OWNER': '{{ context.workflow.cell }}', 'SESSION': e('inputs.session_id'),
                  'SCENARIO': scenario, 'TRACE': str(work/'trace.jsonl'), 'TARGET': target,
                  'DEPENDENCIES_JSON': json.dumps(history), 'MISSING_CELL': (work/'missing-repository').as_uri(),
                  **{role+'_CELL': str(repo) for role, repo in cells.items()},
                  **{role+'_HEAD': value for role, value in heads.items()}}
        agent = c.read('agent.yaml')
        for name, original in list(agent['state']['states']['run']['state']['states'].items()):
            agent['state']['states']['run']['state']['states'][name] = model_node(original, {
                **common, 'ROLE': e('inputs.instructions.startsWith("Implement") ? "I" : "D"')})
        agent['state']['states']['run']['outputs'] = command_outputs(agent['state']['states']['run']['outputs'], ['root', 'scoped'])
        c.write(fixture/'agent.yaml', agent)
        foreign = c.read('consult.yaml'); original = foreign['state']['states']['agent']
        foreign['state']['states']['agent'] = {**model_node(original, {
            **common, 'ROLE': e('context.workspace.cell == "cell-c" ? "C" : "B"')}, const=True),
            'transitions': original['transitions']}
        foreign['outputs'] = command_outputs(foreign['outputs'], ['agent'])
        c.write(fixture/'consult.yaml', foreign)
        impl_inputs = {'prompt': 'Implement client behavior', 'target_directory': target,
                       'mode': 'evolve' if scenario == 'evolve' else 'build',
                       'context_json': json.dumps({'design': d.DESIGN, 'test_plan': d.PLAN}),
                       'dependency_history_json': json.dumps(history)}
        nodes = []
        if scenario == 'reuse':
            nodes.append({'id': 'design', 'include': str(fixture/'design.yaml'), 'inputs': {'prompt': 'Implement client behavior'}})
            impl_inputs.update(consultation_history_json=e('json_stringify(sequence.design.outputs.consultations)'),
                               context_json=e("'{\"design\":' + json_stringify(sequence.design.outputs.result) + '}'"))
        nodes.append({'id': 'implementation', 'include': str(fixture/'implement.yaml'), 'inputs': impl_inputs})
        output_node = 'implementation'
        if scenario == 'feedback':
            nodes.append({'id': 'revision', 'include': str(fixture/'implement.yaml'), 'inputs': {
                **impl_inputs, 'feedback': 'Ask the dependency owner a follow-up question',
                'session_id': e('sequence.implementation.outputs.session_id'),
                'session_artifacts_json': e('json_stringify(sequence.implementation.outputs.session_artifacts)'),
                'additional_consultation_history_json': e('json_stringify(sequence.implementation.outputs.consultations)'),
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
        expected_fail = scenario in ('malformed', 'missing-session', 'wrong-session', 'missing-checkpoint', 'unavailable')
        if expected_fail:
            assert code != 0, (scenario, final)
            if scenario == 'unavailable':
                assert all(r['role'] == 'I' for r in rows), 'Resolution failure silently fell back to A'
                assert 'workspace' in log_path.read_text().lower()
            else:
                assert any(r['role'] == 'B' for r in rows)
                assert 'record' in log_path.read_text(), errors + log_path.read_text()[-3000:]
        else:
            assert code == 0, log_path.read_text()[-8000:]
            result = final['Attempts'][-1]['Output']['Data']['implementation']
            assert result['valid'] and result['completed'] and result['session_id'] == 'I-session', result
            expected = 'redesign' if scenario in ('bug', 'evolve', 'reuse') else 'needs_input' if scenario in ('missing-mandate', 'outside', 'limit') else 'ready'
            assert result['result']['status'] == expected, result
            assert result['dependencies'] == history
            if expected == 'redesign':
                assert result['result']['proposed_handoffs'][0]['provenance']['commit'] == heads['B']
                assert result['result']['questions']
            if scenario == 'multiple':
                assert [r['role'] for r in rows] == ['I','B','I','C','I','B','I']
            if scenario == 'reuse':
                assert [r['role'] for r in rows] == ['D','B','D','I','B','I']
                assert [r['session'] for r in rows if r['role'] == 'B'] == ['', 'B-session']
            if scenario == 'feedback':
                assert [r['session'] for r in rows if r['role'] == 'I'] == ['', 'I-session', 'I-session', 'I-session']
            if scenario == 'limit':
                assert len([r for r in rows if r['role'] == 'B']) == 8
            for key, thread in result['consultations'].items():
                assert thread['commit'] == heads[key]
                assert all(k == 'codex-home-state' or k.startswith('codex-home-state/') for k in thread['session_artifacts'])
        children = json.loads(d.run(['c2j','list','children','--parent-tenant-id','test','--parent-job-id',job,
                                     '--all-ops','--all','--status','READY,ACTIVE,PENDING_JOBS,COMPLETED,CANCELLED','--json'], env=env))['jobs']
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


def verify_contracts(work):
    cases = ['advice', 'new-work', 'already-approved', 'changed-mode', 'changed-pin', 'disagreement',
             'changed-brief', 'missing-thread', 'retarget', 'missing-session', 'budget', 'renewed-budget',
             'false-ready', 'pending', 'missing-question']
    for name in cases:
        _, _, history = c.data()
        result = copy.deepcopy(d.IMPLEMENTATION)
        proposal = dict(thread_id='service',cell='service',mode='build',outcome_ids=[],design_markdown='Agreed service change')
        context = {'design': {'handoffs': []}}
        initial = {}; session = 'implementation-session'
        if name in ['new-work','already-approved','changed-mode','changed-pin','disagreement','changed-brief','missing-thread']:
            result['proposed_handoffs'] = [copy.deepcopy(proposal)]
        if name in ['already-approved','changed-mode','changed-pin']:
            context['design']['handoffs'] = [{**proposal, 'provenance': {'commit': d.HASH}}]
        if name == 'changed-mode': result['proposed_handoffs'][0]['mode'] = 'evolve'
        if name == 'changed-pin': context['design']['handoffs'][0]['provenance']['commit'] = 'different'
        if name == 'disagreement': history['service']['response']['fit'] = 'outside'
        if name == 'changed-brief': result['proposed_handoffs'][0]['design_markdown'] = 'Unreviewed scope'
        if name == 'missing-thread': history = {}
        if name in ['retarget','missing-session','budget','renewed-budget','pending']:
            result.update(status='needs_input',questions=['Ask B'],consultation=dict(thread_id='service',cell='service',ref='main',message='Investigate dependency bug'))
        if name == 'retarget': result['consultation']['cell'] = 'another-cell'
        if name == 'missing-session': session = ''
        if name in ['budget','renewed-budget']: history['service']['turns'] *= 8
        if name == 'renewed-budget': initial = copy.deepcopy(history)
        if name == 'false-ready': result['blocking_issues'] = ['Still blocked']
        if name == 'missing-question': result.update(status='needs_input',questions=[])
        out = work/('contract-'+name);out.mkdir()
        rejected = name in ['disagreement','changed-brief','missing-thread','retarget','missing-session','false-ready']
        actual = d.command_test(d.script('implement.yaml','contract'), {'RESULT_JSON':json.dumps(result),
            'CONTEXT_JSON':json.dumps(context),'HISTORY_JSON':json.dumps(history),'INITIAL_HISTORY_JSON':json.dumps(initial),
            'SESSION':session,'OUTBOX':str(out)},ok=not rejected)
        if actual:
            expected = 'redesign' if name in ['new-work','changed-mode','changed-pin'] else 'needs_input' if name in ['budget','renewed-budget','pending','missing-question'] else 'ready'
            assert actual['result']['status']==expected, (name,actual)
            assert bool(actual['selection']) == (name in ['pending','renewed-budget'])
            if expected=='redesign': assert actual['result']['proposed_handoffs'][0]['provenance']['commit']==d.HASH
    code = c.read('consultation-history.yaml')['sequence'][0]['inputs']['run']
    for name in ['empty','retain','advance','reverse','different-cell','different-ref','different-session','divergent','conflicting-response']:
        _,_,history=c.data(); additional=copy.deepcopy(history)
        if name=='empty': history={};additional={}
        if name=='retain': additional={}
        if name in ['advance','reverse']: additional['service']['turns'].append({'message':'Follow-up','response':additional['service']['response']})
        if name=='reverse': history,additional=additional,history
        if name in ['different-cell','different-ref','different-session']:
            additional['service'][{'different-cell':'cell','different-ref':'ref','different-session':'session_id'}[name]]='other'
        if name=='divergent': additional['service']['turns'][0]['message']='Conflicting branch'
        if name=='conflicting-response': additional['service']['response']['summary']='Conflicting answer'
        result=d.command_test(code,{'HISTORY_JSON':json.dumps(history),'ADDITIONAL_JSON':json.dumps(additional)},ok=name in ['empty','retain','advance','reverse'])
        if name in ['advance','reverse']: assert len(result['service']['turns'])==2
    print('implementation: 15 contract and 9 history merge cases passed',flush=True)


def main():
    with tempfile.TemporaryDirectory(prefix='implementation-dialogues-') as temp:
        work = Path(temp); binary = work/'jobdb-service'
        d.run(['go','build','-o',str(binary),'.'], cwd=ROOT/'recipe-tests/jobdb-service')
        verify_contracts(work)
        failures = []
        scenarios = sys.argv[1:] or ['advice','bug','evolve','multiple','reuse','feedback','missing-mandate','outside','failed-dependency',
                                    'malformed','missing-session','wrong-session','missing-checkpoint','unavailable','limit']
        for scenario in scenarios:
            try: verify_live(work/scenario, binary, scenario)
            except Exception as error:
                print(f'FAILED {scenario}: {error}', flush=True); failures.append(scenario)
        assert not failures, 'Failed live scenarios: '+', '.join(failures)

if __name__ == '__main__': main()

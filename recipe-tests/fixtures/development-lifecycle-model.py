"""Scripted decisions only; production recipes own all gates and Git operations."""
import json
import os
from pathlib import Path
import subprocess

root = Path(os.environ['WORKTREE'])
inbox = Path(os.environ['INBOX'])
out = Path(os.environ['OUTBOX'])
cell = os.environ['CELL_KIND']
mode = os.environ['MODE']
session = os.environ['SESSION']
consult = os.environ.get('CONSULT') == 'true'
instructions = os.environ.get('INSTRUCTIONS', '')
role = 'consult' if consult else 'design' if instructions.startswith('Assess') else 'implement' if instructions.startswith('Implement') else 'plan' if instructions.startswith('Write outcome') else 'review'
identity = ('B' if consult else cell) + '-' + role
session_home = Path(os.environ['SESSION_HOME'])
checkpoint = session_home/'session.json'
if session:
    assert session == identity and json.loads(checkpoint.read_text())['session'] == identity
else:
    assert not checkpoint.exists(), 'Session checkpoint crossed roles'
with open(os.environ['TRACE'], 'a') as trace:
    trace.write(json.dumps(dict(cell=cell, role=role, session=session, owner=os.environ['OWNER'], workspace=os.environ['WORKSPACE']))+'\n')
base = dict(next='done' if role in ('consult','review') else 'review', summary='Validated outcome')
brief = 'Provide token validation: valid tokens succeed and invalid tokens return an error.'
relative = '.c2j/' if mode == 'evolve' else ''
target = root/relative
feature = target/'feature.txt'
tests = target/'test_feature.py'

if consult:
    assert (root/'.c2j/mandate.md').exists() and os.environ['WORKSPACE'] != os.environ['OWNER']
    assert (root/'AGENTS.md').read_text() == 'Instructions for B\n'
    assert not feature.exists() and not (root/'experiment.txt').exists()
    (root/'experiment.txt').write_text('discard this experiment')
    result = dict(base, summary=brief)
else:
    assert (root/'AGENTS.md').read_text() == 'Instructions for '+cell+'\n'
    data = json.loads(os.environ['CONTEXT_JSON'])
    context = data.get('phase', data)
    dependencies = data.get('dependencies', {})
    if role == 'design':
        assert (root/'.c2j/mandate.md').exists()
        result = dict(base, summary='Implement local token behavior.')
        if cell == 'A' and context['consultations']:
            assert context['implementation']['next'] == 'redesign'
            assert context['consultations'][os.environ['B_CELL']]['response']['summary'] == brief
            result['summary'] += ' Approved external work: '+brief
        if cell == 'B': assert os.environ['PROMPT'] == brief
        (out/'design.md').write_text('# Design\n\n'+result['summary'])
    elif role == 'plan':
        assert (inbox/'prior/design.md').exists()
        (root/'.c2j/test-plan.md').write_text('# Test plan\n\n- Valid tokens succeed. Files: test_feature.py; critical; integration; dependencies: none.\n- Invalid tokens are rejected. Files: test_feature.py; critical; integration; dependencies: none.\n')
        result = base
    elif role == 'implement':
        result = dict(base)
        assert (inbox/'prior/design.md').exists() and (root/'.c2j/test-plan.md').exists()
        (out/'implementation.md').write_text('# Implementation\n\nToken validation.')
        if cell == 'A':
            marker = target/'candidate.txt'
            if not session:
                marker.write_text('preserve candidate across consultation and restart\n')
            else:
                assert marker.read_text() == 'preserve candidate across consultation and restart\n'
            history = context['consultations']
            if not history:
                result.update(next='consult',consultation=dict(cell=os.environ['B_CELL'],ref='main',message='Missing token validation; propose a compatible interface.'))
            elif 'Approved external work:' not in (inbox/'prior/design.md').read_text():
                result.update(next='redesign', summary='Approve the external dependency: '+brief)
            elif not dependencies:
                # The trace proves renewed approval happened before the actual submit.
                approvals = [json.loads(line) for line in Path(os.environ['DECISIONS']).read_text().splitlines()]
                assert len([x for x in approvals if x['cell']=='A' and x['state']=='approve_plan']) == 2
                subprocess.run(['c2j','submit',brief,'--cell',os.environ['B_CELL'],'--'+mode,'--json'],check=True,stdout=subprocess.DEVNULL)
                result.update(next='ask_user',summary='Await dependency')
            else:
                assert len(dependencies) == 1
                child = next(iter(dependencies.values()))
                assert child['status']=='completed' and child['outputs']['merged']
                merged = child['outputs']['merged_hash']
                assert subprocess.check_output(['git','--git-dir',os.environ['B_CELL'],'rev-parse','main'],text=True).strip() == merged
                value = subprocess.check_output(['git','--git-dir',os.environ['B_CELL'],'show',merged+':'+relative+'feature.txt'],text=True)
                assert value == 'valid:ok\ninvalid:error\n'
                feature.write_text(value)
                evidence = list((inbox/'dependencies').rglob('verification.md'))
                assert evidence and all('success: true' in p.read_text() for p in evidence)
                (out/'dependency-version.txt').write_text(merged+'\n')
        else:
            assert not dependencies
            feature.write_text('valid:ok\ninvalid:error\n')
        if feature.exists():
            if cell == 'A' and not context.get('verify'):
                (target/'build.sh').write_text('echo deliberate verification failure; exit 7\n')
            else:
                if cell == 'A':
                    assert context['verify']['status'] == 'failed' and context['verify']['exit_code'] == 7
                    assert 'deliberate verification failure' in (inbox/'prior/build.log').read_text()
                (target/'build.sh').write_text('python3 test_feature.py\n')
            tests.write_text("from pathlib import Path\nvalues=dict(line.split(':') for line in Path('feature.txt').read_text().splitlines())\nassert values['valid']=='ok'\nassert values['invalid']=='error'\nprint('positive and negative outcomes passed')\n")
    else:
        result = base
        if instructions.startswith(('Independently review the implementation', 'Independently review implementation quality')):
            assert feature.read_text() == 'valid:ok\ninvalid:error\n' and tests.exists()
            if cell == 'A': assert len(dependencies) == 1

(out/'result.json').write_text(json.dumps(result))
(session_home/'session.json').write_text(json.dumps(dict(session=identity)))
print(json.dumps(dict(status='completed',sessionId=identity)))

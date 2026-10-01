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
base = dict(status='ready', summary='Validated outcome', questions=[], blocking_issues=[])
brief = 'Provide token validation: valid tokens succeed and invalid tokens return an error.'
relative = '.c2j/' if mode == 'evolve' else ''
target = root/relative
feature = target/'feature.txt'
tests = target/'test_feature.py'

if consult:
    mandate = json.loads((inbox/'mandate/mandate.json').read_text())
    assert mandate['valid'] and os.environ['WORKSPACE'] != os.environ['OWNER']
    assert (root/'AGENTS.md').read_text() == 'Instructions for B\n'
    assert not feature.exists() and not (root/'experiment.txt').exists()
    (root/'experiment.txt').write_text('discard this experiment')
    result = dict(base, fit='fits', design_markdown=brief)
else:
    assert (root/'AGENTS.md').read_text() == 'Instructions for '+cell+'\n'
    data = json.loads(os.environ['CONTEXT_JSON'])
    context = data.get('phase', data)
    dependencies = data.get('dependencies', {})
    if role == 'design':
        mandate = context['mandate']
        assert mandate['valid']
        result = dict(base, design_markdown='Implement local token behavior.',
                      requirements=[dict(id='R1', statement='Tokens are validated')],
                      assessment=dict(assessment_status='assessed', fit='fits', rationale='Local responsibility', questions=[],
                          outcomes=[dict(id='R1', statement='Tokens are validated', ownership='local', suggested_owner=mandate['cell'], mandate_evidence=['OWN-01'], reason='Owned feature')]),
                      consultation=None, handoffs=[])
        if cell == 'A' and context['consultations']:
            previous = context['previous']['implementation']
            assert previous['status'] == 'redesign' and previous['proposed_handoffs']
            thread = context['consultations']['service']
            assert thread['response']['design_markdown'] == brief
            result['handoffs'] = [dict(thread_id='service',cell=os.environ['B_CELL'],mode=mode,outcome_ids=[],design_markdown=brief)]
        if cell == 'B':
            handoff = json.loads(os.environ['PROMPT'])
            assert handoff['design_markdown'] == brief and handoff['provenance']['cell'] == mandate['cell']
            assert handoff['provenance']['commit'] == mandate['commit']
            (out/'handoff.json').write_text(json.dumps(handoff))
    elif role == 'plan':
        result = dict(base, statements=[dict(id=key,statement=statement,requirement_ids=['R1'],files=['test_feature.py'],importance='critical',level='integration',dependencies=[],case=case)
            for key,statement,case in [('T1','Valid tokens succeed.','positive'),('T2','Invalid tokens are rejected.','negative')]],
            commands=[dict(id='behavior',run='python3 test_feature.py',statement_ids=['T1','T2'],timeout_seconds=10)])
    elif role == 'implement':
        result = dict(base, changes=['Token validation'], statement_tests=[dict(statement_id=key,files=['test_feature.py']) for key in ['T1','T2']], consultation=None, proposed_handoffs=[])
        if cell == 'A':
            marker = target/'candidate.txt'
            if not session:
                marker.write_text('preserve candidate across consultation and restart\n')
            else:
                assert marker.read_text() == 'preserve candidate across consultation and restart\n'
            history = context['consultations']
            if not history:
                result.update(status='needs_input',questions=['Ask dependency owner'],consultation=dict(thread_id='service',cell=os.environ['B_CELL'],ref='main',message='Missing token validation; propose a compatible interface.'))
            elif not context['design']['handoffs']:
                result['proposed_handoffs'] = [dict(thread_id='service',cell=os.environ['B_CELL'],mode=mode,outcome_ids=[],design_markdown=history['service']['response']['design_markdown'])]
            elif not dependencies:
                # The trace proves renewed approval happened before the actual submit.
                approvals = [json.loads(line) for line in Path(os.environ['DECISIONS']).read_text().splitlines()]
                assert len([x for x in approvals if x['cell']=='A' and x['state']=='approve_plan']) == 2
                handoff = context['design']['handoffs'][0]
                subprocess.run(['c2j','submit',json.dumps(handoff),'--cell',handoff['cell'],'--'+handoff['mode'],'--json'],check=True,stdout=subprocess.DEVNULL)
                result.update(status='needs_input',questions=['Await dependency'])
            else:
                assert len(dependencies) == 1
                child = next(iter(dependencies.values()))
                assert child['status']=='completed' and child['outputs']['merged']
                merged = child['outputs']['merged_hash']
                assert subprocess.check_output(['git','--git-dir',os.environ['B_CELL'],'rev-parse','main'],text=True).strip() == merged
                value = subprocess.check_output(['git','--git-dir',os.environ['B_CELL'],'show',merged+':'+relative+'feature.txt'],text=True)
                assert value == 'valid:ok\ninvalid:error\n'
                feature.write_text(value)
                evidence = list((inbox/'dependencies').rglob('verification.json'))
                assert evidence and all(json.loads(p.read_text())['ok'] for p in evidence)
                (out/'dependency-version.txt').write_text(merged+'\n')
        else:
            assert not dependencies
            feature.write_text('valid:ok\ninvalid:error\n')
        if feature.exists():
            tests.write_text("from pathlib import Path\nvalues=dict(line.split(':') for line in Path('feature.txt').read_text().splitlines())\nassert values['valid']=='ok'\nassert values['invalid']=='error'\nprint('positive and negative outcomes passed')\n")
    else:
        result = base
        if instructions.startswith('Independently inspect'):
            assert feature.read_text() == 'valid:ok\ninvalid:error\n' and tests.exists()
            if cell == 'A': assert len(dependencies) == 1

(out/'result.json').write_text(json.dumps(result))
(session_home/'session.json').write_text(json.dumps(dict(session=identity)))
print(json.dumps(dict(status='completed',sessionId=identity)))

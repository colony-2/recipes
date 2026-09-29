"""Deterministic model turns; Git workspaces, artifacts and gates remain real."""
import json
import os
from pathlib import Path
import subprocess

inbox = Path(os.environ['INBOX'])
outbox = Path(os.environ['OUTBOX'])
root = Path(os.environ['WORKTREE'])
scenario = os.environ['SCENARIO']
role = os.environ['ROLE']
session = os.environ['SESSION']
checkpoint = inbox / 'codex-home-state/session.json'
prior = json.loads(checkpoint.read_text()) if checkpoint.exists() else None
if session:
    assert prior and prior['session'] == session, ('checkpoint isolation', session, prior)
    turn = prior['turn'] + 1
else:
    assert prior is None, 'A new session received another session checkpoint'
    turn = 0
identity = f'{role}-session'
assert not session or session == identity
assert (root / 'AGENTS.md').read_text() == f'Instructions for {os.environ["WORKSPACE"]}\n'
base = dict(status='ready', summary='Answered', questions=[], blocking_issues=[])
with open(os.environ['TRACE'], 'a') as trace:
    trace.write(json.dumps(dict(role=role, session=session, turn=turn,
                               workspace=os.environ['WORKSPACE'], owner=os.environ['OWNER'])) + '\n')

if role in ('B', 'C'):
    assert os.environ['WORKSPACE'] != os.environ['OWNER']
    assert (root / 'app.txt').read_text() == 'application\n'
    assert not (root / 'experiment.txt').exists()
    mandate = json.loads((inbox / 'mandate/mandate.json').read_text())
    assert mandate['commit'] == os.environ[role + '_HEAD'], (mandate['commit'], os.environ[role + '_HEAD'], mandate['cell'], role, subprocess.check_output(['git','-C',str(root),'log','-3','--oneline'],text=True))
    assert subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip() == mandate['commit']
    if turn == 0 and scenario in ('advice', 'bug', 'evolve', 'multiple', 'reuse', 'feedback'):
        source = Path(os.environ[role + '_CELL'])
        (source / 'upstream.txt').write_text('unrelated upstream movement')
        subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(source), 'commit', '-qm', 'Unrelated upstream change'], check=True)
    (root / 'experiment.txt').write_text('must be discarded')
    (root / 'app.txt').write_text('foreign experiment')
    result = dict(base, fit='fits', design_markdown=f'{role}: reject invalid tokens and preserve valid requests.')
    if scenario in ('bug', 'evolve') and turn == 0:
        result.update(status='needs_input', questions=['What input reproduces the bug?'])
    if scenario == 'missing-mandate':
        assert not mandate['valid']
        result.update(status='needs_input', fit=None, questions=['Accept a mandate for this cell.'])
    if scenario == 'outside':
        result.update(fit='outside', summary='Another owner is needed')
    if scenario == 'wrong-session' and turn:
        identity = 'unexpected-replacement-session'
    if scenario == 'missing-session':
        identity = ''
    if scenario == 'malformed':
        (outbox / 'result.json').write_text('invalid JSON')
else:
    assert os.environ['WORKSPACE'] == os.environ['OWNER']
    context = json.loads((inbox / 'phase/context.json').read_text())
    if 'dependencies' in context:
        assert context['dependencies'] == json.loads(os.environ['DEPENDENCIES_JSON'])
        context = context['phase']
    history = context['consultations']
    if role == 'D':
        mandate = context['mandate']
        result = dict(base, design_markdown='Use the existing service API.',
                      requirements=[dict(id='R1', statement='Client behavior works')],
                      assessment=dict(assessment_status='assessed', fit='fits', rationale='Client ownership', questions=[],
                                      outcomes=[dict(id='R1', statement='Client behavior works', ownership='local',
                                                     suggested_owner=mandate['cell'], mandate_evidence=['OWN-01'], reason='Local behavior')]),
                      consultation=None, handoffs=[])
        if turn == 0:
            result.update(status='needs_input', questions=['Clarify service interface'],
                          consultation=dict(thread_id='B', cell=os.environ['B_CELL'], ref='main', message='Existing interface?'))
    else:
        target = root / os.environ['TARGET']
        target.mkdir(exist_ok=True)
        marker = target / 'implementation.txt'
        if turn == 0:
            marker.write_text('A implementation in progress\n')
        else:
            assert marker.read_text() == 'A implementation in progress\n', 'A candidate was lost'
        assert not (root / 'experiment.txt').exists(), 'B edits contaminated A'
        assert (root / 'app.txt').read_text() == 'application\n'
        result = dict(base, changes=['Local candidate'], statement_tests=[dict(statement_id='T1', files=['test.sh'])],
                      consultation=None, proposed_handoffs=[])
        target_role = None
        if scenario == 'multiple':
            target_role = ['B', 'C', 'B'][turn] if turn < 3 else None
        elif scenario == 'feedback':
            target_role = 'B' if turn in (0, 2) else None
        elif scenario == 'wrong-session':
            target_role = 'B' if turn < 2 else None
        elif scenario == 'limit':
            target_role = 'B'
        elif turn == 0 or scenario in ('bug', 'evolve') and turn == 1:
            target_role = 'B'
        if target_role:
            cell = os.environ[target_role + '_CELL']
            if scenario == 'unavailable':
                cell = os.environ['MISSING_CELL']
            result.update(status='needs_input', questions=['Discuss dependency behavior'],
                          consultation=dict(thread_id=target_role, cell=cell, ref='main',
                                            message='Repro: invalid token crashes; should return a validation error.'))
        elif scenario in ('bug', 'evolve', 'reuse'):
            reply = history['B']['response']
            # Deliberately report ready: the real contract must force redesign.
            result['proposed_handoffs'] = [dict(thread_id='B', cell=os.environ['B_CELL'], mode='build',
                                              outcome_ids=[], design_markdown=reply['design_markdown'])]
        elif scenario in ('missing-mandate', 'outside'):
            result.update(status='needs_input', questions=['Resolve dependency ownership'])
        if scenario == 'multiple' and not target_role:
            assert len(history['B']['turns']) == 2 and len(history['C']['turns']) == 1
        if scenario == 'reuse':
            assert len(history['B']['turns']) == turn + 1, 'Design conversation was lost or restarted'

if scenario != 'malformed' or role not in ('B', 'C'):
    (outbox / 'result.json').write_text(json.dumps(result))
if not (scenario == 'missing-checkpoint' and role in ('B', 'C')):
    (outbox / 'codex-home-state').mkdir()
    (outbox / 'codex-home-state/session.json').write_text(json.dumps(dict(session=identity, turn=turn)))
print(json.dumps(dict(status='completed', sessionId=identity)))

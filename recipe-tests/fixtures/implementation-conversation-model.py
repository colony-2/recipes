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
session_home = Path(os.environ['SESSION_HOME'])
checkpoint = session_home / 'session.json'
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
base = dict(next='done' if role in ('B','C') else 'review', summary='Answered')
with open(os.environ['TRACE'], 'a') as trace:
    trace.write(json.dumps(dict(role=role, session=session, turn=turn,
                               workspace=os.environ['WORKSPACE'], owner=os.environ['OWNER'])) + '\n')

if role in ('B', 'C'):
    assert os.environ['WORKSPACE'] != os.environ['OWNER']
    assert (root / 'app.txt').read_text() == 'application\n'
    assert not (root / 'experiment.txt').exists()
    if turn == 0 and scenario in ('advice', 'bug', 'evolve', 'multiple', 'reuse', 'feedback'):
        source = Path(os.environ[role + '_CELL'])
        (source / 'upstream.txt').write_text('unrelated upstream movement')
        subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(source), 'commit', '-qm', 'Unrelated upstream change'], check=True)
    (root / 'experiment.txt').write_text('must be discarded')
    (root / 'app.txt').write_text('foreign experiment')
    result = dict(base, summary=f'{role}: This fits. Reject invalid tokens and preserve valid requests.')
    if scenario in ('bug', 'evolve') and turn == 0:
        result.update(summary='What input reproduces the bug?')
    if scenario == 'missing-mandate':
        assert not (root / '.c2j/mandate.md').exists()
        result.update(next='ask_user', summary='Accept a mandate for this cell.')
    if scenario == 'outside':
        result.update(summary='This is outside our mandate; another owner is needed')
    if scenario == 'illegal-children':
        subprocess.run(['c2j', 'submit', 'Unauthorized consultation work', '--cell', os.environ['B_CELL'],
                        '--recipe-file', os.environ['ILLEGAL_RECIPE'], '--json'], check=True, stdout=subprocess.DEVNULL)
    if scenario == 'missing-session':
        identity = ''
    if scenario == 'malformed':
        (outbox / 'result.json').write_text('invalid JSON')
else:
    assert os.environ['WORKSPACE'] == os.environ['OWNER']
    context = json.loads(os.environ['CONTEXT_JSON'])
    if 'dependencies' in context:
        assert context['dependencies'] == ({} if role == 'D' else json.loads(os.environ['DEPENDENCIES_JSON']))
        context = context['phase']
    history = context['consultations']
    if role == 'D':
        if turn > 0:
            assert 'Partially fits' in (inbox/'prior/draft/design.md').read_text()
        assert (root / '.c2j/mandate.md').exists()
        result = dict(base, summary='Partially fits: this cell owns the client, B owns the service.')
        if turn < (2 if scenario == 'design' else 1):
            result.update(next='consult', consultation=dict(cell=os.environ['B_CELL'],ref='main',message='Existing interface?' if turn==0 else 'Clarify error handling.'))
        (outbox/'design.md').write_text('# Design\n\n'+result['summary'])
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
        result = dict(base)
        (outbox/'implementation.md').write_text('# Implementation\n\nLocal candidate.')
        target_role = None
        if scenario == 'multiple':
            target_role = ['B', 'C', 'B'][turn] if turn < 3 else None
        elif scenario == 'feedback':
            target_role = 'B' if turn in (0, 2) else None
        elif turn == 0 or scenario in ('bug', 'evolve') and turn == 1:
            target_role = 'B'
        if target_role:
            cell = os.environ[target_role + '_CELL']
            if scenario == 'unavailable':
                cell = os.environ['MISSING_CELL']
            result.update(next='consult',
                          consultation=dict(cell=cell, ref='main',
                                            message='Repro: invalid token crashes; should return a validation error.'))
        elif scenario in ('bug', 'evolve', 'reuse'):
            reply = history[os.environ['B_CELL']]['response']
            result.update(next='redesign', summary='Please approve external work: '+reply['summary'])
        elif scenario in ('missing-mandate', 'outside'):
            result.update(next='ask_user', summary='Resolve dependency ownership')
        if scenario == 'multiple' and not target_role:
            assert set(history) == {os.environ['B_CELL'],os.environ['C_CELL']}
        if scenario == 'reuse':
            assert os.environ['B_CELL'] in history, 'Design conversation was lost'

if scenario != 'malformed' or role not in ('B', 'C'):
    (outbox / 'result.json').write_text(json.dumps(result))
if not (scenario == 'missing-checkpoint' and role in ('B', 'C')):
    (session_home / 'session.json').write_text(json.dumps(dict(session=identity, turn=turn)))
print(json.dumps(dict(status='completed', sessionId=identity, _omit_session=scenario=='missing-checkpoint' and role in ('B','C'))))

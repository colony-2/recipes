"""Case-local continuation sources and native credential probes; no live secrets."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(*args, **kwargs):
    return subprocess.run(args, text=True, capture_output=True, **kwargs)


def git(*args):
    result = run('git', *map(str, args))
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def expr(value):
    return '$' + '{{ ' + value + ' }}'


def credential(expected):
    result = run('git', 'credential', 'fill',
                 input='protocol=https\nhost=fixture.invalid\npath=repository.git\n\n')
    if result.returncode:
        # The provider is seeded in every case. Only the permission failure is
        # acceptable here; preserve no credential response in diagnostics.
        assert 'secret resolution unavailable' in result.stderr, result.stderr
        return False
    fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    secret = run('c2j', 'secret', 'get', expected, '--format', 'raw')
    assert secret.returncode == 0, 'Selected credential is not in the task grant'
    assert fields.get('password') == secret.stdout.strip(), 'Wrong Git profile selected'
    return True


def task(root, expected, allow_submit):
    resolved = credential(expected)
    (root / 'read-result.json').write_text(json.dumps({'resolved': resolved}))
    assert resolved, 'read credential denied'
    unrelated = run('c2j', 'secret', 'get', 'unrelated_token')
    assert unrelated.returncode != 0, 'Unrelated secret was authorized'
    assert any(s in unrelated.stderr.lower() for s in ('denied', 'not authorized', 'not permitted', 'forbidden', 'secret resolution unavailable')), unrelated.stderr
    if allow_submit is not None:
        submit = run('c2j', 'submit', 'Bounded continuation child', '--advanced-recipe-file',
                     str(root / 'noop.yaml'), '--cell', 'root', '--from-workspace', '--embed', '--json')
        assert (submit.returncode == 0) == allow_submit, submit.stderr
        if not allow_submit:
            assert any(s in submit.stderr.lower() for s in ('denied', 'not authorized', 'forbidden')), submit.stderr
    # The profile case checks inheritance independently of child submission.
    # Historical c2j rejected git_profile in a child's context schema; this case
    # does not certify that path. Default submission has healthy/denied controls.
    outside = run('c2j', 'submit', 'Excluded continuation child', '--advanced-recipe-file',
                  str(root / 'noop.yaml'), '--cell', 'outside', '--embed', '--json')
    assert outside.returncode != 0, 'Submission escaped the cell ceiling'
    assert any(s in outside.stderr.lower() for s in ('denied', 'not authorized', 'forbidden')), outside.stderr
    create = run('c2j', 'cell', 'create', 'ungranted', '--repo', 'fixture.invalid/ungranted', '--json')
    assert create.returncode != 0, 'Default policy granted cell creation'
    print(json.dumps({'read_resolved': True, 'unrelated_denied': True,
                      'submission_allowed': allow_submit, 'outside_denied': True}))


def setup(scenario):
    root = Path(tempfile.mkdtemp(prefix='continuation-source-'))
    source = root / 'recipes-source'
    shutil.copytree('.test/library', source)
    shutil.copy(__file__, root / 'probe.py')
    # This source checkout is separate from the recovered application workspace.
    git('-C', source, 'init', '-q', '-b', 'main')
    schema = {'prompt': {'type': 'string'}, 'type': {'type': 'string'}}
    (root / 'noop.yaml').write_text(json.dumps({'schema_version': 2, 'id': 'noop',
                                               'input_schema': schema, 'sequence': []}))
    expected_read = 'checkout_alternate' if scenario == 'explicit-profile' else 'checkout_read'
    expected_write = expected_read if scenario == 'explicit-profile' else 'checkout_write'
    origin, clone = root / 'origin', root / 'clone'
    git('init', '-q', '-b', 'main', origin)
    git('-C', origin, 'config', 'receive.denyCurrentBranch', 'updateInstead')
    git('-C', origin, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '--allow-empty', '-qm', 'base')
    base = git('-C', origin, 'rev-parse', 'HEAD')
    git('clone', '-q', origin, clone)
    git('-C', clone, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '--allow-empty', '-qm', 'probe publication')
    # Git invokes this hook in the *native merge task's* environment, after c2j
    # selects its profile and issues its restricted grant. No profile is supplied
    # on that node. The push itself stays on a disposable local origin.
    hook = clone / '.git/hooks/pre-push'
    import shlex
    hook.write_text('#!/bin/sh\nexec python3 ' + shlex.quote(str(root / 'probe.py')) +
                    ' publication ' + shlex.quote(str(root)) + ' ' + expected_write + '\n')
    hook.chmod(0o755)
    model = expr('context.secrets.codex_api_key')
    # Select direct publication for this permission check. Merge-queue behavior
    # has dedicated suites and needs a separate coordinator fixture.
    body = {'schema_version': 2, 'id': 'continuation-body', 'sequence': [
        {'id': 'preflight', 'op': 'command_execution', 'inputs': {
            'env': {'MODEL': model},
            'run': 'test -n "$MODEL"\npython3 ' + shlex.quote(str(root / 'probe.py')) +
                   ' task ' + shlex.quote(str(root)) + ' ' + expected_read + ' ' +
                   ('skip' if scenario == 'explicit-profile' else str(scenario != 'deny-submit').lower())}},
        {'id': 'publication_credentials', 'op': 'merge', 'retry': {'maximum_attempts': 1},
         'inputs': {'repo_path': str(clone), 'upstream_repo': str(origin), 'upstream_branch': 'main'}},
        {'id': 'build', 'include': './build.yaml', 'inputs': {'prompt': 'Add a marker; retain the recovered draft.', 'merge_queue': False}},
    ], 'outputs': {'result': expr('sequence.build.outputs'),
                   'child_jobs': expr('sequence.preflight.jobs.job_ids'),
                   'preflight': expr('json_parse(sequence.preflight.outputs.stdout)')}}
    (source / 'continuation-body.yaml').write_text(json.dumps(body))
    call = {'id': 'continuation', 'include': './continuation-body.yaml'}
    names = ['codex_api_key', 'checkout_read', 'checkout_write', 'checkout_alternate']
    if scenario.startswith('deny-') and scenario != 'deny-submit':
        names.remove({'deny-model': 'codex_api_key', 'deny-read': 'checkout_read',
                      'deny-write': 'checkout_write'}[scenario])
    ceiling = {'secrets': {'resolve': names}, 'jobs': {'submit': True, 'cellNames': ['root']}}
    if scenario == 'deny-submit':
        ceiling['jobs'] = {'submit': False}
    if scenario == 'original-allowlist':
        call['perms'] = {'jobdb': {'secrets': {'resolve': ['codex_api_key', 'checkout_read']},
                                  'jobs': {'submit': True, 'cellNames': ['root']}}}
    caller = {'schema_version': 2, 'id': 'continuation-caller', 'input_schema': schema,
              'perms': {'limit': {'jobdb': ceiling}}, 'sequence': [call],
              'outputs': {'result': expr('sequence.continuation.outputs')}}
    if scenario == 'explicit-profile':
        caller['git_profile'] = 'alternate'
    caller_path = source / 'continuation.yaml'
    if scenario in ('foreign-omission', 'hosted-after-relocation'):
        foreign = source
        if scenario == 'hosted-after-relocation':
            # Stand in for a hosted source with a different repository identity;
            # a file selector of this *same* checkout would not be foreign.
            foreign = root / 'hosted-source'
            shutil.copytree(source, foreign)
            git('-C', foreign, 'add', '.')
            git('-C', foreign, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                'commit', '-qm', 'Hosted Recipes fixture')
        call['include'] = 'git+file://' + str(foreign) + '//build.yaml@main'
        if scenario == 'foreign-omission':
            caller_path = root / 'continuation.yaml'
    caller_path.write_text(json.dumps(caller))
    git('-C', source, 'add', '.')
    git('-C', source, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '-qm', 'Isolated Recipes fixture')
    # Remove fixture sources before capturing the application snapshot. Only the
    # recovered draft and the later implementation should enter the candidate.
    shutil.rmtree('.test')
    Path('recovered.txt').write_text('saved application draft\n')
    (root / 'state.json').write_text(json.dumps({'base': base, 'scenario': scenario,
                                               'application_origin': git('remote', 'get-url', 'origin')}))
    selector = ['--advanced-recipe', 'git+file://' + str(source) + '//continuation.yaml@main']
    if scenario in ('foreign-omission', 'hosted-after-relocation'):
        selector = ['--advanced-recipe-file', str(caller_path)]
    submit = run('c2j', 'submit', 'Continuation permission regression', *selector,
                 '--cell', 'root', '--from-workspace-now', '--embed', '--json')
    (root / 'submission-error.txt').write_text(submit.stderr)
    print(root)
    # Native task instrumentation records child IDs independently of stdout.


def finish(root):
    state = json.loads((root / 'state.json').read_text())
    result = {'submission_error': (root / 'submission-error.txt').read_text(),
              'probe_published': git('-C', root / 'origin', 'rev-parse', 'HEAD') != state['base'],
              'application_files': git('-C', state['application_origin'], 'ls-tree', '-r', '--name-only', 'HEAD').splitlines(),
              'application_hash': git('-C', state['application_origin'], 'rev-parse', 'HEAD')}
    result['probe_error'] = (root / 'probe-error.txt').read_text() if (root / 'probe-error.txt').exists() else ''
    for name in ('read', 'publication'):
        path = root / (name + '-result.json')
        result[name] = json.loads(path.read_text()) if path.exists() else {}
    print(json.dumps(result))
    shutil.rmtree(root)


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'setup':
        setup(sys.argv[2])
    elif action == 'finish':
        finish(Path(sys.argv[2]))
    elif action == 'task':
        try:
            task(Path(sys.argv[2]), sys.argv[3], None if sys.argv[4] == 'skip' else sys.argv[4] == 'true')
        except Exception as error:
            (Path(sys.argv[2]) / 'probe-error.txt').write_text(str(error))
            raise
    elif action == 'publication':
        root = Path(sys.argv[2])
        resolved = credential(sys.argv[3])
        (root / 'publication-result.json').write_text(json.dumps({'resolved': resolved, 'profile_secret': sys.argv[3]}))
        if not resolved:
            sys.exit('publication credential denied')

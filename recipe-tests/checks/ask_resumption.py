#!/usr/bin/env python3
"""Exercise the actual ask recipe across separate SQLite runner processes.

Uses only the pinned runtime's native compiler, input API and worker. The small
Go client is scoped to these fixtures because c2j has no structured reply CLI.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-dir', required=True)
parser.add_argument('--c2j-source', type=Path, help='Existing checkout of the immutable configured source pin')
args = parser.parse_args()
destination = Path(args.out_dir).resolve()
destination.mkdir(parents=True, exist_ok=True)


def command(*argv, cwd=None):
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=True)
    return result.stdout.strip()


with tempfile.TemporaryDirectory(prefix='ask-native-') as scratch:
    scratch = Path(scratch)
    pin = (ROOT / '.c2j-version').read_text().strip().removeprefix('source:')
    assert len(pin) == 40, 'This fixture requires the configured source pin'
    source = args.c2j_source
    if source is None:
        source = scratch / 'c2j'
        command('git', 'init', '-q', str(source))
        command('git', '-C', str(source), 'fetch', '--quiet', '--depth=1', 'https://github.com/colony-2/c2j.git', pin)
        command('git', '-C', str(source), 'checkout', '--quiet', '--detach', 'FETCH_HEAD')
    assert command('git', '-C', str(source), 'rev-parse', 'HEAD') == pin
    client = scratch / 'client'
    with tempfile.TemporaryDirectory(prefix='ask-fixture-', dir=source / 'cmd/c2j') as module:
        shutil.copyfile(ROOT / 'recipe-tests/fixtures/ask/native.go', Path(module) / 'main.go')
        command('go', 'build', '-mod=readonly', '-o', str(client), './cmd/c2j/' + Path(module).name, cwd=source)
    library = scratch / 'library'
    consumer = scratch / 'consumer'
    for name in ['ask.yaml', 'recipes/review-v2.yaml', 'recipes/review-v2/op.yaml', 'recipes/review-v2.py', 'recipes/adaptive3/children.yaml', 'recipes/adaptive3/diagnostics.yaml']:
        target = library / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    seed = {'schema_version': 2, 'id': 'seed', 'sequence': [{'id': 'files', 'op': 'command_execution', 'inputs': {
        'env': {'FIXTURE_OUTBOX': '${{ context.environment.op.outbox }}'},
        'run': 'mkdir -p "$FIXTURE_OUTBOX/review" "$FIXTURE_OUTBOX/a" "$FIXTURE_OUTBOX/b"\nprintf "Original 日本語\\n" > "$FIXTURE_OUTBOX/review/notes.md"\nprintf "First upload 🙂\\n" > "$FIXTURE_OUTBOX/a/notes.md"\nprintf "Second upload\\n" > "$FIXTURE_OUTBOX/b/notes.md"'}}], 'outputs': {'artifact_refs': '${{ sequence.files.artifacts }}'}}
    (library / 'seed.yaml').write_text(json.dumps(seed, ensure_ascii=False))
    collector = {'schema_version': 2, 'id': 'collector', 'input_schema': {'jobs': {'type': 'array', 'items': {'type': 'string'}}}, 'inputs': {'jobs': '${{ inputs.jobs }}'}, 'sequence': [{'id': 'children', 'include': './recipes/adaptive3/children.yaml', 'inputs': {'jobs': '${{ inputs.jobs }}'}}], 'outputs': {'results': '${{ sequence.children.outputs.results }}', 'artifact_refs': '${{ sequence.children.outputs.documents }}'}}
    (library / 'collector.yaml').write_text(json.dumps(collector))
    consumer.mkdir()
    (consumer / 'README.md').write_text('Application without question helpers.\n')
    for repo in [library, consumer]:
        command('git', 'init', '-q', '-b', 'main', str(repo))
        command('git', '-C', str(repo), 'add', '.')
        command('git', '-C', str(repo), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Fixture')
    consumer_hash = command('git', '-C', str(consumer), 'rev-parse', 'HEAD')
    base = {'DB': str(scratch / 'jobs.db'), 'Consumer': str(consumer), 'Hash': consumer_hash}
    counts = {}

    def call(action, job='question', **values):
        payload = {**base, 'Action': action, 'Job': job, **values}
        result = subprocess.run([str(client)], input=json.dumps(payload), text=True, capture_output=True)
        index = counts.get(job + action, 0)
        counts[job + action] = index + 1
        (destination / f'{job}-{action}-{index}.log').write_text(result.stderr)
        if result.returncode:
            raise RuntimeError(f'{job}/{action}: {result.stderr}')
        output = json.loads(result.stdout)
        (destination / f'{job}-{action}-{index}.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
        return output

    def selector(name):
        return f'git+file://{library}//{name}.yaml@main'

    call('start', 'seed', Source=selector('seed'), Inputs={})
    stored = call('result', 'seed')['outputs']['artifact_refs']
    inputs = {'title': 'Confirm staging worker upgrade', 'question': '  Is staging running abc123? 日本語 🙂\n',
              'documents': {'review/notes.md': stored['review/notes.md']},
              'overview_document_id': 'review/notes.md',
              'document_metadata': {'review/notes.md': {'title': 'Owner publication evidence', 'description': 'Read the exact staging version.', 'role': 'primary', 'order': 10}}}
    uploads = [stored['a/notes.md'], stored['b/notes.md']]
    response = {'direction': 'reply', 'feedback': '', 'attachments': uploads, 'settings': {}}
    call('start', Source=selector('ask'), Inputs=inputs)
    pending = call('form')
    call('run')
    resumed = call('form')
    assert resumed == pending, 'Pending request changed across runner invocations'
    assert pending['form']['request']['document_metadata'] == inputs['document_metadata']
    assert pending['form']['request']['documents'] == inputs['documents']
    # Original evidence cannot satisfy a required reply; failed submissions retain input.
    for invalid in [{'direction': 'reply', 'feedback': '', 'attachments': [], 'settings': {}},
                    {'direction': 'reply', 'feedback': '', 'attachments': [{'kind': 'stored', 'stored': {'key': {'jobId': 'missing', 'taskOrdinal': 1, 'name': 'notes.md', 'sizeBytes': 1}}}], 'settings': {}}]:
        assert 'rejected' in call('respond', Response=invalid)
        assert call('form') == pending
    accepted = call('respond', Response=response)
    assert accepted['response'] == response
    # This process has exited after acceptance, before final result export.
    call('run')
    final = call('result')
    assert final['outputs']['native'] == {'fields': {}, 'metadata': {}, 'user_id': '', **accepted}, 'Native response or receipt changed on resume'
    assert final['outputs']['request'] == pending['form']['request']
    expected_bytes = {'originals/review/notes.md': 'Original 日本語\n'}
    for i, content in enumerate(['First upload 🙂\n', 'Second upload\n']):
        expected_bytes[f'feedback/{accepted["receipt"]["request_id"]}/{i}/notes.md'] = content
    assert final['bytes'] == expected_bytes
    exported = final['outputs']['artifact_refs']
    assert exported['originals/review/notes.md']['stored'] == stored['review/notes.md']['stored']
    for i, ref in enumerate(uploads):
        assert exported[f'feedback/{accepted["receipt"]["request_id"]}/{i}/notes.md']['stored'] == ref['stored']
    # Compare with one uninterrupted start/input/finish runner process.
    control = call('complete', 'control', Source=selector('ask'), Inputs=inputs, Response=response)
    ordinary = call('result', 'control')
    assert ordinary['outputs']['native'] == {'fields': {}, 'metadata': {}, 'user_id': '', **control['accepted']}
    assert ordinary['outputs']['native']['response'] == final['outputs']['native']['response']
    assert sorted(ordinary['bytes'].values()) == sorted(final['bytes'].values())
    normalize = lambda r: {k: v for k, v in r.items() if k != 'review_id'}
    assert normalize(control['form']['request']) == normalize(final['outputs']['request'])
    history = call('history')
    assert history['completeness'] == 'complete' and not history.get('next_page_token')
    assert len(history['entries']) == 1 and history['entries'][0]['state'] == 'answered'
    assert history['entries'][0]['request_id'] == accepted['receipt']['request_id']
    # The actual Adaptive collector materializes the selected child files.
    call('start', 'collector', Source=selector('collector'), Inputs={'jobs': ['question']})
    call('run', 'collector')
    collected = call('result', 'collector')
    assert collected['outputs']['results'][0]['job_id'] == 'question'
    assert collected['outputs']['results'][0]['status'] == 'completed'
    assert collected['bytes'] == {'children/question/results/' + k: v for k, v in expected_bytes.items()}
    # Real cancellation of a pending question; the existing collector waits and returns it.
    call('start', 'cancel-question', Source=selector('ask'), Inputs=inputs)
    call('start', 'cancel-collector', Source=selector('collector'), Inputs={'jobs': ['cancel-question']})
    call('cancel', 'cancel-question')
    call('run', 'cancel-collector')
    cancelled = call('result', 'cancel-collector')
    assert cancelled['outputs']['results'][0]['job_id'] == 'cancel-question'
    assert cancelled['outputs']['results'][0]['status'] == 'cancelled'
    assert cancelled['outputs']['results'][0]['summary'] == '' and cancelled['bytes'] == {}
    # Stored uploads are rejected when the chosen direction forbids attachments.
    restricted = {**inputs, 'directions': [{'id': 'reply', 'label': 'Text reply', 'feedback_mode': 'required', 'allow_attachments': False, 'continues_review': False}]}
    call('start', 'text-only', Source=selector('ask'), Inputs=restricted)
    assert 'rejected' in call('respond', 'text-only', Response=response)
    call('respond', 'text-only', Response={**response, 'attachments': [], 'feedback': 'Text reply'})
    call('run', 'text-only')
    assert call('result', 'text-only')['outputs']['native']['response']['feedback'] == 'Text reply'
    assert command('git', '-C', str(consumer), 'rev-parse', 'HEAD') == consumer_hash
    assert command('git', '-C', str(consumer), 'status', '--porcelain') == ''
    evidence = {'runtime_pin': pin, 'checks': ['pending request and ordinal retained across processes', 'rejected replies retain pending request', 'accepted native response and receipt retained before result export', 'upload-only reply accepted', 'same-basename original and two uploads materialize with exact bytes and producer keys', 'uninterrupted control agrees', 'one accepted history contribution', 'Adaptive collector preserves child files and cancellation', 'forbidden stored uploads rejected', 'consumer repository unchanged']}
    (destination / 'summary.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print('Question SQLite resumption, upload-only replies and stored artifact checks passed.')

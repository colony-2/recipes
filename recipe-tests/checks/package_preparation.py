#!/usr/bin/env python3
"""Check retained native setup envelopes for the bounded package fixtures.

The pinned assertion CEL environment has no JSON/base64 decoder. This check reads
only these two native cases; it does not simulate preparation or runtime state.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = 'uv:pytest==8.3.5'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-dir', required=True)
args = parser.parse_args()
destination = Path(args.out_dir).resolve()
subprocess.run(['c2j', 'test', 'run', '--file', str(ROOT / 'recipe-tests/adaptive3/package-preparation.test.yaml'), '--case-timeout', '3m', '--out-dir', str(destination)], check=True, cwd=ROOT)
evidence = {'scope': 'Successful native tasks only; not a complete preparation stream.', 'cases': {}}
for case in ['staging-before-fresh-probe-setup', 'rejected-adoption-parent-setup']:
    report = json.loads((destination / 'cases' / case / 'result.json').read_text())
    assert report['status'] == 'passed', case
    run = report['run']
    controls = run['runtime']['controls']
    snapshot = controls['final_snapshot']
    assert controls['complete'] and not controls.get('errors')
    assert snapshot['complete'] and not snapshot.get('errors')
    rows = []
    for key, task in snapshot['successful_tasks'].items():
        assert key == task['invocation_id'] + '/attempt:' + str(task['attempt'])
        assert task['attempt'] == 1 and not task['output']['redacted']
        raw = base64.b64decode(task['output']['content_base64'], validate=True)
        assert hashlib.sha256(raw).hexdigest() == task['output']['sha256'].removeprefix('sha256:')
        envelope = json.loads(raw)
        payload = envelope.get('payload', {})
        if 'setup' in payload:
            row = {k: task[k] for k in ['invocation_id', 'attempt', 'result_ordinal']}
            row.update(setup=payload['setup'], workspace_before=payload['workspace_before'], workspace_after=payload['workspace_after'])
            repository = row['setup']['repository']
            assert repository['scope'] == 'repository:root' and repository['path'] == '.c2/config.yaml'
            assert repository['snapshot'] == row['workspace_before']['head_commit']
            assert repository['repository'] == row['workspace_before']['repository']
            rows.append(row)

    def one(*fragments):
        found = [r for r in rows if all(f in r['invocation_id'] for f in fragments)]
        assert len(found) == 1, (case, fragments, len(found))
        return found[0]

    def excludes(row):
        assert REFERENCE not in row['setup']['repository'].get('packages', [])
        assert not any(t['reference'] == REFERENCE for t in row['setup'].get('tools', []))

    validator = one('sequence:validate', 'op:package_config')
    following = one('op:following')
    excludes(validator)
    assert validator['setup']['repository']['missing']
    if case.startswith('staging'):
        stage = one('sequence:stage', 'op:package_config')
        probe = one('sequence:stage', 'op:probe')
        excludes(stage)
        assert stage['setup']['repository']['missing']
        assert stage['workspace_before']['head_commit'] != stage['workspace_after']['head_commit']
        assert probe['setup']['repository']['snapshot'] == stage['workspace_after']['head_commit']
        assert probe['setup']['repository']['packages'] == [REFERENCE]
        tools = [t for t in probe['setup']['tools'] if t['reference'] == REFERENCE]
        assert len(tools) == 1 and tools[0]['scope'] == 'repository:root'
        assert tools[0]['identity'] and tools[0]['outcome'] in ('prepared', 'reused')
        assert validator['result_ordinal'] < stage['result_ordinal'] < probe['result_ordinal'] < following['result_ordinal']
        selected = [validator, stage, probe, following]
    else:
        child = run['outputs']['child']
        assert child['status'] == 'completed' and child['outputs']['status'] == 'passed' and child['job_id']
        assert run['outputs']['adoption'] == {'status': 'changes', 'summary': 'Current configuration conflicts with approved baseline'}
        assert run['outputs']['configuration'] == 'custom: concurrent'
        concurrent = one('op:concurrent')
        adoption = one('sequence:adopt', 'op:package_config')
        excludes(adoption)
        excludes(following)
        assert adoption['workspace_before']['head_commit'] == adoption['workspace_after']['head_commit']
        assert adoption['setup']['repository']['snapshot'] == concurrent['workspace_after']['head_commit']
        assert following['setup']['repository'] == adoption['setup']['repository']
        assert following['setup']['repository']['digest'] == 'sha256:' + hashlib.sha256(b'custom: concurrent\n').hexdigest()
        assert concurrent['result_ordinal'] < adoption['result_ordinal'] < following['result_ordinal']
        selected = [validator, concurrent, adoption, following]
    evidence['cases'][case] = {'status': report['status'], 'job_id': snapshot['job_id'], 'outputs': run['outputs'], 'tasks': selected}
(destination / 'preparation-evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
print('Native preparation snapshots verified: 2 cases, exact task identities, provenance, references and ordering.')

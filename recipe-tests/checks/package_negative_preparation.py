#!/usr/bin/env python3
"""Run paired native rejection/healthy fixtures with isolated cold installer logs.

Only the two explicit synthetic repository packages are installable per invocation.
Python execution environments use real uv, with separate preparation logs. Logs
and caches remain outside restored worktrees until each native runner has drained.
This measures cold installations, not a complete preparation or warm-cache trace.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
BASELINE = 'packages: ["uv:a3-prior==1"]\ncustom: retained\n'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-dir', required=True)
parser.add_argument('--pair', choices=['symlink', 'dangling', 'unsafe-parent', 'altered-check', 'unexpected-addition'], action='append')
args = parser.parse_args()
destination = Path(args.out_dir).resolve()
destination.mkdir(parents=True, exist_ok=True)
real_uv = shutil.which('uv')
if real_uv is None:
    raise RuntimeError('Cold preparation controls require real uv for Python environments')
real_uv = str(Path(real_uv).resolve())
evidence = {'scope': 'Isolated cold synthetic uv installations; warm/failed-task preparation and full C14/C20 acceptance remain incomplete.', 'cases': {}}
for pair in args.pair or ['symlink', 'dangling', 'unsafe-parent', 'altered-check', 'unexpected-addition']:
    addition = 'a3-addition-' + pair + '==1'
    for healthy in [True, False]:
        case = pair + ('-healthy' if healthy else '-rejected')
        owned = destination / 'invocations' / case
        # Refuse reuse of a previous cache/log. An unchanged rerun needs a new out-dir.
        owned.mkdir(parents=True)
        (owned / 'bin').mkdir()
        (owned / 'cache').mkdir()
        target = owned / 'targets/config.yaml'
        target.parent.mkdir()
        if healthy or pair != 'dangling':
            target.write_text(BASELINE)
        installer = owned / 'bin/uv'
        shutil.copyfile(ROOT / 'recipe-tests/adaptive3/preparation-installer/uv', installer)
        installer.chmod(0o755)
        log = owned / 'install.log'
        python_log = owned / 'python-preparation.log'
        env = {**os.environ, 'PATH': str(installer.parent) + os.pathsep + os.environ['PATH'], 'C2J_TOOL_CACHE_DIR': str(owned / 'cache'), 'PREP_INSTALL_LOG': str(log), 'PREP_PRIOR_SPEC': 'a3-prior==1', 'PREP_ADDITION_SPEC': addition,
               'PREP_REAL_UV':real_uv, 'PREP_PYTHON_LOG':str(python_log)}
        # Compile with the normal CLI, then bind only this test-owned target path.
        # Keep the compiled file beside the fixture so source paths retain meaning.
        with tempfile.TemporaryDirectory(prefix='.negative-preparation-', dir=ROOT / 'recipe-tests/adaptive3') as tmp:
            compiled = Path(tmp) / 'cases.json'
            subprocess.run(['c2j', 'test', 'compile', '--file', str(ROOT / 'recipe-tests/adaptive3/package-negative-preparation.cases.yaml'), '--out', str(compiled)], env=env, cwd=ROOT, check=True, capture_output=True)
            suite = json.loads(compiled.read_text())
            selected = [c for c in suite['cases'] if c['id'] == case]
            assert len(selected) == 1
            selected[0]['inputs']['target'] = str(target)
            # file_sources resolve relative to the compiled suite directory.
            selected[0]['runtime']['cells']['root']['file_sources']['observer/op.yaml'] = '../preparation-observer/op.yaml'
            suite['cases'] = selected
            compiled.write_text(json.dumps(suite))
            subprocess.run(['c2j', 'test', 'run', '--file', str(compiled), '--recipe-file', str(ROOT / 'recipe-tests/adaptive3/package-negative-preparation.yaml'), '--case-timeout', '3m', '--out-dir', str(owned / 'results')], env=env, cwd=ROOT, check=True)
        report = json.loads((owned / 'results/cases' / case / 'result.json').read_text())
        assert report['status'] == 'passed', case
        installs = log.read_text().splitlines()
        expected = ['tool install -- a3-prior==1'] + (['tool install -- ' + addition] if healthy else [])
        assert installs == expected, (case, installs, expected)
        python_preparation = python_log.read_text().splitlines()
        for command in ('venv ', 'pip compile ', 'pip sync ', 'pip list '):
            assert any(line.startswith(command) for line in python_preparation), (case, command, python_preparation)
        run = report['run']
        target_after = {'exists': target.exists(), 'bytes': target.read_text() if target.exists() else None, 'symlink': os.readlink(target) if target.is_symlink() else None}
        expected_exists = healthy or pair != 'dangling'
        assert target_after == {'exists': expected_exists, 'bytes': BASELINE if expected_exists else None, 'symlink': None}
        assert target_after == run['outputs']['before']['external_target'], (case, target_after)
        unsafe = not healthy and pair in ['symlink', 'dangling', 'unsafe-parent']
        if not healthy:
            if not unsafe:
                assert run['outputs']['before'] == run['outputs']['after']
            assert not any(c['node_path'].endswith('/probe/probe') for c in run['runtime']['calls'])
        if unsafe:
            assert run['outputs']['stage']['summary'] == 'repository package setup failed: .c2/config.yaml: expected a regular config file in a real .c2 directory (symlinks are not supported)'
            assert not any('/stage/' in c['node_path'] for c in run['runtime']['calls'])
        controls = run['runtime']['controls']
        snapshot = controls['final_snapshot']
        assert controls['complete'] and not controls.get('errors') and snapshot['complete'] and not snapshot.get('errors')
        setup = []
        for key, task in snapshot['successful_tasks'].items():
            assert key == task['invocation_id'] + '/attempt:' + str(task['attempt'])
            assert task['attempt'] == 1 and not task['output']['redacted']
            raw = base64.b64decode(task['output']['content_base64'], validate=True)
            assert hashlib.sha256(raw).hexdigest() == task['output']['sha256'].removeprefix('sha256:')
            envelope = json.loads(raw)
            payload = envelope.get('payload', {})
            if 'setup' not in payload:
                continue
            if not any(s in task['invocation_id'] for s in ['sequence:stage', 'op:inspect', 'op:arrange', 'sequence:validate']):
                continue
            repository = payload['setup']['repository']
            assert repository['scope'] == 'repository:root'
            assert repository['snapshot'] == payload['workspace_before']['head_commit']
            assert repository['repository'] == payload['workspace_before']['repository']
            setup.append({k: task[k] for k in ['invocation_id', 'attempt', 'result_ordinal']} | {'setup': payload['setup']})
            if not healthy:
                assert all(t['reference'] not in ['uv:' + addition, 'uv:a3-unexpected==1'] for t in payload['setup'].get('tools', []))
        assert len([r for r in setup if 'op:arrange' in r['invocation_id']]) == 1
        assert len([r for r in setup if 'sequence:validate' in r['invocation_id']]) == 1
        if unsafe:
            assert not any('sequence:stage' in r['invocation_id'] or 'op:inspect' in r['invocation_id'] for r in setup)
        else:
            assert len([r for r in setup if 'op:inspect' in r['invocation_id']]) == 1
            assert len([r for r in setup if 'sequence:stage' in r['invocation_id'] and 'op:package_config' in r['invocation_id']]) == 1
        if healthy:
            probes = [r for r in setup if 'op:probe' in r['invocation_id']]
            assert len(probes) == 1
            tools = [t for t in probes[0]['setup']['tools'] if t['reference'] == 'uv:' + addition]
            assert len(tools) == 1 and tools[0]['outcome'] == 'prepared' and tools[0]['scope'] == 'repository:root' and tools[0]['identity']
        evidence['cases'][case] = {'status': report['status'], 'job_id': snapshot['job_id'], 'installer_log': installs,
                                  'python_preparation_log':python_preparation, 'python_preparation_uv':real_uv,
                                  'outputs': run['outputs'], 'external_target_after_workers_drained': target_after, 'setup': setup}
(destination / 'negative-preparation-evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
print('Cold native preparation checks passed:', len(evidence['cases']), 'paired cases; full behavioral acceptance remains incomplete.')

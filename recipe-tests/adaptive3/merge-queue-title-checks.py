#!/usr/bin/env python3
"""Check stored boundary titles and run the recipe's real clock command."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--results', required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
source = (root / 'recipes/adaptive3/merge-queue-submit.yaml').read_text()
commands = re.findall(r'id: capture_batch_start\n(?:.*\n)*?\s+run: (.+)', source)
assert len(commands) == 1, 'Expected one capture command in the submitted recipe'
locales = subprocess.check_output(['locale', '-a'], text=True).splitlines()
locale = next((name for name in locales if name.lower() in ('c.utf8', 'c.utf-8')), None)
assert locale, 'A UTF-8 locale is required for the real-clock check'
env = {**os.environ, 'TZ': 'Pacific/Honolulu', 'LC_ALL': locale}
before = datetime.now(timezone.utc).replace(microsecond=0)
stamp = subprocess.check_output(['sh', '-c', commands[0]], env=env, text=True).rstrip('\r\n')
after = datetime.now(timezone.utc).replace(microsecond=0)
actual = datetime.strptime(stamp, '%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc)
assert re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC', stamp), stamp
assert before <= actual <= after, (before, actual, after)

observed = {}
for path in args.results.rglob('result.json'):
    result = json.loads(path.read_text())
    case = result.get('case_id', '')
    if not case.startswith('clock-boundary-'):
        continue
    assert result['status'] == 'passed', (case, result['status'])
    calls = result['run']['runtime']['calls']
    batches = [call for call in calls if call['op'] == 'recipe.run_and_get_result']
    assert len(batches) == 1, (case, len(batches))
    metadata = batches[0]['outputs']['outputs']['metadata']
    assert metadata['id'], metadata
    assert case not in observed, f'Duplicate report for {case}'
    observed[case] = metadata
assert set(observed) == {f'clock-boundary-{i}' for i in range(1, 9)}, observed
rows = [observed[f'clock-boundary-{i}'] for i in range(1, 9)]
titles = [row['title'] for row in rows]
assert titles == sorted(titles) and len(set(titles)) == 8, titles
report = {'status': 'passed', 'real_capture': {'TZ': env['TZ'], 'LC_ALL': locale,
          'stdout': stamp, 'before': before.isoformat(), 'after': after.isoformat()},
          'chronological_stored_batches': rows}
(args.results / 'merge-queue-title-checks.json').write_text(json.dumps(report, indent=2) + '\n')
print('Passed: real UTC capture under Honolulu/UTF-8; eight stored titles sort across noon, midnight, month and year boundaries.')

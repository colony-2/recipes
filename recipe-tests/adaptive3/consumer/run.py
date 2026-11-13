"""Run the actual Cortex adapter/renderer against forms from native recipe test reports.

python3 run.py CORTEX_CHECKOUT CYCLE_REPORT_JSON RESOLVER_REPORT_JSON
Install the checkout's locked pnpm dependencies first. No source edits are retained.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

checkout = Path(sys.argv[1]).resolve()
forms = []
for report in sys.argv[2:]:
    result = json.loads(Path(report).read_text())
    forms.append(result['run']['runtime']['reviews'][0]['form'])
assert len(forms) >= 2, 'Supply cycle and resolver native reports'
target = checkout / 'web/app/src/components/Adaptive3Consumer.test.tsx'
assert not target.exists(), f'Refusing to overwrite {target}'
with tempfile.TemporaryDirectory(prefix='adaptive3-forms-') as scratch:
    path = Path(scratch) / 'forms.json'
    path.write_text(json.dumps(forms))
    try:
        target.write_text(Path(__file__).with_name('feedback.test.tsx').read_text())
        subprocess.run(['pnpm', 'exec', 'vitest', 'run', str(target)],
                       cwd=checkout / 'web/app', check=True,
                       env={**os.environ, 'ADAPTIVE3_REVIEW_FORMS': str(path)})
    finally:
        target.unlink(missing_ok=True)

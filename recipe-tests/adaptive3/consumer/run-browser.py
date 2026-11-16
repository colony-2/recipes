"""Run Recipes-owned browser checks against built, unchanged published Cortex.

Requires its frozen workspace dependencies and `make build test-worker` first.
Uses the system browser selected by Cortex's existing Playwright configuration.
"""
import os
from pathlib import Path
import subprocess
import sys

checkout=Path(sys.argv[1]).resolve()
source=Path(__file__).resolve().parent
root=source.parents[2]
placements={checkout/'web/app/tests/adaptive3-review-v2.spec.ts':source/'review-v2.spec.ts',
            checkout/'web/app/playwright.adaptive3.config.ts':source/'playwright.config.ts'}
for p in placements:
    if p.exists():sys.exit(f'Refusing to overwrite {p}')
try:
    for p,s in placements.items():p.write_text(s.read_text())
    env={**os.environ,'ADAPTIVE3_BROWSER_FIXTURE':str(source/'browser-review-v2.yaml'),
         'ADAPTIVE3_FORM_HELPER':str(root/'recipes/review-v2.yaml'),
         'ADAPTIVE3_REVIEW_SOURCE':str(root/'recipes'),
         'ADAPTIVE3_BROWSER_SOURCE':str(source)}
    subprocess.run(['pnpm','exec','playwright','test','--config','playwright.adaptive3.config.ts',*sys.argv[2:]],cwd=checkout/'web/app',env=env,check=True)
finally:
    for p in placements:p.unlink(missing_ok=True)

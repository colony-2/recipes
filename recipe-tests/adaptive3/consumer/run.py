"""Use unchanged published Cortex with complete forms from native reports.

python3 run.py CORTEX_CHECKOUT CASE_RESULT_JSON [...]
No requested missing/empty report is silently skipped. Placement is temporary;
all test source and vectors are owned by Recipes.
"""
import json
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

helper_path = Path(__file__).resolve().parents[3] / 'recipes/review-v2.py'
spec = importlib.util.spec_from_file_location('review_v2', helper_path)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

if len(sys.argv) < 3:
    sys.exit(__doc__)
checkout = Path(sys.argv[1]).resolve()
forms = []
for report in sys.argv[2:]:
    result = json.loads(Path(report).read_text())
    reviews = result['run']['runtime']['reviews']
    if not reviews:
        sys.exit(f'No native forms in requested report: {report}')
    for review in reviews:
        form = review['form']
        if form.get('presentation', {}).get('type') != 'review/v2':
            sys.exit(f'Expected generated review/v2 form in {report}')
        forms.append(form)
forms.append(helper.build_form(dict(title='Review with no settings',question='Ask?',documents={},conversation=[],feedback={'label':'Feedback'},directions=[dict(id='question',label='Ask a question',feedback_mode='required',allow_attachments=True,continues_review=True)])))
target = checkout / 'web/app/src/components/Adaptive3Consumer.test.tsx'
documents = checkout / 'web/app/src/components/Adaptive3Documents.test.tsx'
assert not documents.exists(), f'Refusing to overwrite {documents}'
native = checkout / 'server/internal/cortex/recipes_generated_test.go'
assert not native.exists(), f'Refusing to overwrite {native}'
assert not target.exists(), f'Refusing to overwrite {target}'
with tempfile.TemporaryDirectory(prefix='adaptive3-forms-') as scratch:
    path = Path(scratch) / 'forms.json'
    path.write_text(json.dumps(forms))
    vectors_path = Path(__file__).resolve().parents[2] / 'review-v2/contract-vectors.json'
    vectors = json.loads(vectors_path.read_text())
    scalar_cases = []
    for vector in vectors['scalars']:
        schema = vector['schema']
        current = None
        for value in [None, False, True, 0, 1, 2, 'a', '🙂', '日本🙂']:
            try: helper.validate_scalar(value, schema)
            except ValueError: continue
            current = value
            break
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        kind = next(t for t in types if t != 'null')
        declaration = dict(title='Scalar parity', question='Contribute?', documents={}, conversation=[], feedback={'label':'Feedback'},
            directions=[dict(id='question',label='Ask',feedback_mode='required',allow_attachments=True,continues_review=True)],
            settings=[dict(id='unfamiliar',label='Fixture value',effect='Changes the fixture.',control={'string':'text','boolean':'boolean','integer':'number','number':'number'}[kind],schema=schema,value=current,applies_to=['question'])])
        scalar_cases.append(dict(form=helper.build_form(declaration), response=dict(direction='question',feedback='Why?',attachments=[],settings={'unfamiliar':vector['value']}), valid=vector['valid']))
    native_vectors = Path(scratch) / 'native-vectors.json'
    native_vectors.write_text(json.dumps(dict(feedback=vectors['feedback'], scalars=scalar_cases)))
    try:
        target.write_text(Path(__file__).with_name('feedback.test.tsx').read_text())
        documents.write_text(Path(__file__).with_name('documents.test.tsx').read_text())
        native.write_text(Path(__file__).with_name('native_test.go').read_text())
        env = {**os.environ, 'ADAPTIVE3_REVIEW_FORMS': str(path),
               'ADAPTIVE3_REVIEW_VECTORS': str(vectors_path), 'ADAPTIVE3_NATIVE_VECTORS': str(native_vectors)}
        subprocess.run(['pnpm', 'exec', 'vitest', 'run', '--testTimeout', '30000', str(target), str(documents), 'src/components/ReviewV2.test.tsx', 'src/components/ReviewV2Recovery.test.tsx', 'src/components/ReviewV2Settings.test.tsx'], cwd=checkout / 'web/app', check=True, env=env)
        subprocess.run(['bash', 'scripts/go.sh', 'test', './server/internal/cortex', '-run', '^TestRecipesGeneratedNativeSchemas$', '-count=1'], cwd=checkout, check=True, env=env)
    finally:
        target.unlink(missing_ok=True)
        documents.unlink(missing_ok=True)
        native.unlink(missing_ok=True)

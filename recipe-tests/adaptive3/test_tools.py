"""Run the exact embedded validators against real files and Git repositories.

Dependencies: PyYAML, Pillow, cmark, yq, git. No copied validator implementation.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import yaml

SOURCE = Path(__file__).resolve().parents[2] / 'recipes/adaptive3/tools.yaml'
TASKS = yaml.safe_load(SOURCE.read_text())['state']['states']

class Validators(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.inbox = self.root / 'inbox'
        self.outbox = self.root / 'outbox'
        for p in (self.repo, self.inbox, self.outbox): p.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.repo/'file.txt').write_text('original\n')
        self.commit()
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, text=True, stderr=subprocess.PIPE)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def put(self, name, value):
        p = self.inbox/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value)

    def check(self, name, **env):
        selected=[str(p.relative_to(self.inbox)) for p in self.inbox.rglob('*') if p.is_file()]
        primary=env.get('PRIMARY','review/README.md')
        details=[dict(document_id=n,title='Decision brief' if n==primary else 'Supporting evidence',
            description='Read the proposed change.' if n==primary else 'Inspect evidence for this change.',
            role='primary' if n==primary else 'supporting',order=0) for n in selected]
        p = subprocess.run(['bash','-c',TASKS[name]['inputs']['run']], cwd=self.repo,
            env={**os.environ, 'INBOX':str(self.inbox), 'OUTBOX':str(self.outbox),
                 'BASE':self.base, 'TITLE':'Review the actual change', 'PRIMARY':'review/README.md',
                 'REQUESTS':'[]', 'ADOPTED':'false', 'DOCUMENT_IDS':json.dumps(selected),
                 'DOCUMENT_DETAILS':json.dumps(details), 'REQUIRE_DOCUMENT_DETAILS':'true', **env}, text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def test_valid_links_and_image(self):
        from PIL import Image
        self.put('review/README.md', '# Review\n![UI](screen.png)\n`[example](absent.md)`')
        Image.new('RGB',(3,3)).save(self.inbox/'review/screen.png')
        self.assertEqual(self.check('review_files')['status'], 'passed')

    def test_missing_image_and_escaping_link(self):
        self.put('review/README.md', '# Review\n![UI](missing.png)\n[escape](../../private.md)')
        self.assertEqual(self.check('review_files')['count'], 2)

    def test_recovery_question_links(self):
        self.put('review/correction.md', '# Restore image checks')
        self.assertEqual(self.check('review_files', PRIMARY='review/correction.md', MESSAGE='[Correction](review/correction.md)')['status'], 'passed')
        self.assertEqual(self.check('review_files', PRIMARY='review/correction.md', MESSAGE='[Correction](/tmp/private/correction.md)')['status'], 'changes')
        self.assertEqual(self.check('review_files', PRIMARY='review/correction.md', MESSAGE='[Correction](file:///tmp/correction.md)')['status'], 'changes')

    def test_corrupt_image(self):
        self.put('review/README.md', '![UI](screen.png)')
        self.put('review/screen.png', 'not an image')
        self.assertEqual(self.check('review_files')['status'], 'changes')

    def test_large_diagnostics_remain_in_file(self):
        self.put('review/README.md','\n'.join(f'[missing](missing-{i}.png)' for i in range(2000)))
        result=self.check('review_files')
        self.assertLess(len(json.dumps(result)), 500)
        self.assertGreater((self.outbox/'error/review-files.log').stat().st_size, 100000)
        self.assertEqual(result['count'], 2000)

    def test_title_before_review(self):
        self.put('review/README.md','# Review')
        self.assertEqual(self.check('review_files',TITLE='x'*121)['status'], 'changes')


    def test_descriptor_fields_and_identity(self):
        self.put('review/README.md', '# Decision')
        good=dict(document_id='review/README.md',title='Decision brief',description='Read the proposed outcome.',role='primary',order=0)
        def run(items, **env):
            return self.check('review_files', DOCUMENT_DETAILS=json.dumps(items), **env)
        result=run([good])
        self.assertEqual(result['document_metadata'], {'review/README.md':{k:v for k,v in good.items() if k!='document_id'}})
        cases=[[], [good,good], [{**good,'document_id':'README.md'}], [{**good,'document_id':'review/absent.md'}],
               [{**good,'extra':'unknown'}], [{k:v for k,v in good.items() if k!='description'}], [None]]
        for field,bad_values in {
            'title':['', '   ', 'a'*121, 'bad\ntext', 'bad\x7ftext', '\ud800', 123],
            'description':['', '\u2003', 'a'*301, 'bad\x00text', '\udfff', False],
            'role':['', 'neutral', 'PRIMARY', None, []],
            'order':[None, True, False, -1, 1000001, 1.5, '1'],
        }.items():
            cases.extend([[{**good,field:v}] for v in bad_values])
        for items in cases:
            with self.subTest(items=items):
                result=run(items)
                self.assertEqual(result['status'],'changes')
                self.assertEqual(result['document_metadata'],{})
        for field,size in [('title',120),('description',300)]:
            self.assertEqual(run([{**good,field:'🐈'*size}])['status'],'passed')
        for order in (0,1000000):
            self.assertEqual(run([{**good,'order':order}])['status'],'passed')
        self.assertEqual(run([good], PRIMARY='review/absent.md')['status'],'changes')
        self.assertEqual(run([good], DOCUMENT_IDS='[]', PRIMARY='')['status'],'changes')
        self.assertEqual(run([], DOCUMENT_IDS='[]', PRIMARY='')['status'],'passed')
        self.assertEqual(run([], DOCUMENT_IDS='[]')['status'],'changes')

    def test_roles_orders_and_primary_agreement(self):
        for name in ('decision.md','support.md','diagnostic.md'):
            self.put('review/'+name, '# Review')
        items=[dict(document_id='review/'+n+'.md', title=n.title(), description='Read '+n+' evidence.', role=r, order=0)
               for n,r in [('decision','primary'),('support','supporting'),('diagnostic','diagnostic')]]
        def run(items): return self.check('review_files', PRIMARY='review/decision.md', DOCUMENT_DETAILS=json.dumps(items))
        self.assertEqual(run(items)['status'],'passed')
        for broken in ([{**x,'role':'supporting'} for x in items],
                       [items[0],{**items[1],'role':'primary'},items[2]],
                       [{**items[0],'role':'supporting'},{**items[1],'role':'primary'},items[2]]):
            self.assertEqual(run(broken)['status'],'changes')

    def test_native_presentation_bytes(self):
        # Generated by c2j's typed Go presentation; zero order, HTML and Unicode matter.
        fixture=json.loads((SOURCE.parents[2]/'recipe-tests/adaptive3/fixtures/presentation-bytes.json').read_text())
        for case in fixture:
            with self.subTest(case=case['name']):
                if 'description_lengths' in case:
                    case['document_details']=[dict(document_id='review/d%03d.txt'%i,title='Decision',description='x'*length,
                        role='primary' if i==0 else 'supporting',order=0) for i,length in enumerate(case['description_lengths'])]
                    case['document_ids']=[x['document_id'] for x in case['document_details']]
                for p in self.inbox.rglob('*'):
                    if p.is_file(): p.unlink()
                for name in case['document_ids']: self.put(name,'evidence')
                result=self.check('review_files',PRIMARY=case['primary'], DOCUMENT_DETAILS=json.dumps(case['document_details']))
                self.assertEqual(result['presentation_bytes'],case['native_bytes'])
                self.assertEqual(result['status'],'passed' if case['native_bytes']<=65536 else 'changes')
                if case['native_bytes']>65536:
                    self.assertIn('65536 native JSON bytes',(self.outbox/'error/review-files.log').read_text())

    def test_approved_patch_compares_modes_and_binary(self):
        (self.repo/'file.txt').write_text('corrected\n')
        (self.repo/'image.bin').write_bytes(b'\x00approved\xff')
        self.commit()
        self.check('approved_change')
        (self.inbox/'approved.diff').write_bytes((self.outbox/'candidate.diff').read_bytes())
        self.assertTrue(self.check('approved_change')['equivalent'])
        (self.repo/'file.txt').chmod(0o755)
        self.commit()
        self.assertFalse(self.check('approved_change')['equivalent'])
        (self.repo/'file.txt').chmod(0o644)
        (self.repo/'image.bin').write_bytes(b'\x00different\xff')
        self.commit()
        self.assertFalse(self.check('approved_change')['equivalent'])

    def test_measured_per_file_counts_and_binary(self):
        (self.repo/'file.txt').write_text('first\nsecond\n')
        (self.repo/'harness').mkdir()
        (self.repo/'harness/runner.py').write_text('test framework\n')
        (self.repo/'image.bin').write_bytes(b'\x00binary')
        self.commit()
        self.check('approved_change')
        counts=(self.outbox/'error/change-counts.tsv').read_text()
        self.assertIn('2\t1\tfile.txt', counts)
        self.assertIn('1\t0\tharness/runner.py', counts)
        self.assertIn('-\t-\timage.bin', counts)

    def test_proposal_does_not_prove_adoption(self):
        self.put('review/config.yaml', 'packages: ["uv:pytest"]\n')
        env={'REQUESTS':json.dumps([{'reference':'uv:pytest','check':['pytest','--version']}])}
        self.assertEqual(self.check('package_config',**env)['status'], 'passed')
        self.assertEqual(self.check('package_config',ADOPTED='true',**env)['status'], 'changes')
        (self.repo/'.c2').mkdir()
        (self.repo/'.c2/config.yaml').write_text('packages: ["uv:pytest"]\n')
        self.assertEqual(self.check('package_config',ADOPTED='true',**env)['status'], 'passed')

    def test_unrelated_config_rejected(self):
        self.put('review/config.yaml','packages: []\npermissions: unsafe\n')
        self.assertEqual(self.check('package_config')['status'], 'changes')

if __name__ == '__main__': unittest.main()

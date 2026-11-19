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
                 'REQUESTS':'[]', 'WRITE':'false', 'APPROVED':'{}', 'PROPOSAL_REF':'{}', 'DOCUMENT_IDS':json.dumps(selected),
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

    def proposal(self, text='packages: ["uv:pytest"]\n', requests=None):
        self.put('review/config.yaml', text)
        self.requests=requests or [{'reference':'uv:pytest','check':['pytest','--version']}]
        self.env={'REQUESTS':json.dumps(self.requests), 'PROPOSAL_REF':json.dumps({'name':'review/config.yaml','producer':'original'})}
        return self.check('package_config', **self.env)

    def write(self, approved, **env):
        return self.check('package_config', **{**self.env,'WRITE':'true','APPROVED':json.dumps(approved),**env})

    def test_bound_write_and_unchanged_retry(self):
        result=self.proposal()
        self.assertEqual(result['status'],'passed')
        self.assertFalse((self.repo/'.c2/config.yaml').exists())
        self.assertEqual(self.write(result['approved'])['status'],'passed')
        config=self.repo/'.c2/config.yaml'
        config.write_text('# keep formatting\npackages: ["uv:pytest"]\n')
        config.chmod(0o640)
        before=config.stat()
        self.assertEqual(self.write(result['approved'])['status'],'passed')
        self.assertEqual(config.stat().st_mtime_ns,before.st_mtime_ns)
        self.assertEqual(config.stat().st_ino,before.st_ino)
        self.assertEqual(config.stat().st_mode,before.st_mode)
        self.assertTrue(config.read_text().startswith('# keep formatting'))

    def test_duplicate_proposal_keys_reject_binding_and_legacy_write(self):
        import hashlib
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        config.write_text('packages: []\n'); config.chmod(0o640)
        duplicates=[
            'packages: ["uv:pytest"]\npackages: ["uv:pytest"]\n',
            'packages: []\n"packages": ["uv:pytest"]\n',
            '{packages: ["uv:pytest"], "pack\\u0061ges": ["uv:pytest"]}',
            'packages: ["uv:pytest"]\ncustom: {enabled: true, enabled: true}\n',
            'packages: ["uv:pytest"]\ncustom: [{name: first, name: second}]\n',
            'packages: ["uv:pytest"]\ncustom: &settings {name: first, name: second}\nother: *settings\n',
        ]
        for present in (True, False):
            if not present: config.unlink()
            for raw in duplicates:
                with self.subTest(raw=raw,present=present):
                    before=config.stat() if present else None
                    result=self.proposal(raw)
                    self.assertEqual(result['status'],'changes')
                    self.assertIn('Duplicate YAML mapping key',result['summary'])
                    self.assertEqual(result['approved'],{})
                    # A binding produced by the old, permissive converter cannot authorize a write.
                    proposed=json.loads(subprocess.check_output(['yq','-o=json','.','-'],input=raw,text=True))
                    approved={'baseline':{'present':present,'value':{'packages':[]} if present else {}},
                              'proposed':proposed,'requests':self.requests,
                              'config':json.loads(self.env['PROPOSAL_REF']),
                              'sha256':hashlib.sha256(raw.encode()).hexdigest()}
                    result=self.write(approved)
                    self.assertEqual(result['status'],'changes')
                    self.assertIn('Duplicate YAML mapping key',result['summary'])
                    self.assertFalse(result['written'])
                    self.assertEqual(config.exists(),present)
                    if present:
                        self.assertEqual(config.read_text(),'packages: []\n')
                        after=config.stat()
                        for field in ('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns'):
                            self.assertEqual(getattr(after,field),getattr(before,field))
                    self.assertEqual(list(config.parent.glob('.config-*')),[])

    def test_duplicate_current_keys_reject_binding_and_write(self):
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        config.write_text('packages: []\n')
        approved=self.proposal()['approved']
        raw='packages: []\npackages: []\n'
        config.write_text(raw); config.chmod(0o640); before=config.stat()
        for result in (self.proposal(), self.write(approved)):
            self.assertEqual(result['status'],'changes')
            self.assertIn('Duplicate YAML mapping key',result['summary'])
            self.assertEqual(result['approved'],{})
            self.assertFalse(result['written'])
        self.assertEqual(config.read_text(),raw)
        after=config.stat()
        for field in ('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns'):
            self.assertEqual(getattr(after,field),getattr(before,field))
        self.assertEqual(list(config.parent.glob('.config-*')),[])

    def test_valid_yaml_aliases_merges_and_scalar_spellings(self):
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        custom='defaults: &defaults {enabled: false, count: 1}\ncustom: {<<: *defaults, enabled: true}\nlabels: {yes: on, no: off, 01: value}\n'
        config.write_text(custom+'packages: []\n')
        approved=self.proposal(custom+'packages: ["uv:pytest"]\n')['approved']
        result=self.write(approved)
        self.assertEqual(result['status'],'passed')
        self.assertTrue(result['written'])
        self.assertEqual(config.read_text(),custom+'packages: ["uv:pytest"]\n')

    def test_changed_approved_inputs_never_write(self):
        approved=self.proposal()['approved']
        for env in [
            {'REQUESTS':json.dumps([{'reference':'uv:pytest==8.3.5','check':['pytest','--version']}])},
            {'REQUESTS':json.dumps([{'reference':'uv:pytest','check':['pytest','-V']}])},
            {'PROPOSAL_REF':json.dumps({'name':'review/config.yaml','producer':'replacement'})},
            {'APPROVED':'{}'},
        ]:
            with self.subTest(env=env):
                self.assertEqual(self.write(approved,**env)['status'],'changes')
                self.assertFalse((self.repo/'.c2/config.yaml').exists())
        self.put('review/config.yaml','packages: ["uv:pytest", "uv:ruff"]\n')
        self.assertEqual(self.write(approved)['status'],'changes')
        self.assertFalse((self.repo/'.c2/config.yaml').exists())

    def test_proposal_preserves_setting_types(self):
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        for original, changed in [('false','0'),('false','0.0'),('true','1'),('[false, {nested: true}]','[0, {nested: 1}]')]:
            with self.subTest(original=original,changed=changed):
                before=f'custom: {original}\npackages: []\n'; config.write_text(before)
                result=self.proposal(f'custom: {changed}\npackages: ["uv:pytest"]\n')
                self.assertEqual(result['status'],'changes')
                self.assertEqual(result['summary'],'Unrelated configuration changed')
                self.assertEqual(config.read_text(),before)

    def test_conflicts_and_applied_retries_preserve_setting_types(self):
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        for original, changed in [('false','0'),('true','1'),('[false, {nested: true}]','[0, {nested: 1}]')]:
            for applied in (False,True):
                with self.subTest(original=original,applied=applied):
                    config.write_text(f'custom: {original}\npackages: []\n')
                    approved=self.proposal(f'custom: {original}\npackages: ["uv:pytest"]\n')['approved']
                    if applied: self.assertEqual(self.write(approved)['status'],'passed')
                    changed_bytes=f'custom: {changed}\npackages: '+('["uv:pytest"]' if applied else '[]')+'\n'
                    config.write_text(changed_bytes); before=config.stat()
                    result=self.write(approved)
                    self.assertEqual(result['status'],'changes')
                    self.assertEqual(result['summary'],'Current configuration conflicts with approved baseline')
                    self.assertEqual(config.read_text(),changed_bytes)
                    self.assertEqual(config.stat().st_ino,before.st_ino)
                    self.assertEqual(config.stat().st_mtime_ns,before.st_mtime_ns)

    def test_bound_values_preserve_setting_types(self):
        import copy
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        config.write_text('custom: false\npackages: []\n')
        approved=self.proposal('custom: false\npackages: ["uv:pytest"]\n')['approved']
        for field in ('proposed','baseline','requests','config'):
            with self.subTest(field=field):
                altered=copy.deepcopy(approved)
                env={}
                if field=='proposed': altered['proposed']['custom']=0
                elif field=='baseline': altered['baseline']['value']['custom']=0
                else:
                    # Unknown request/artifact fields are still part of the exact approved binding.
                    if field=='requests':
                        altered[field][0]['custom']=False
                        env['REQUESTS']=json.dumps([{**self.requests[0],'custom':0}])
                    else:
                        altered[field]['custom']=False
                        env['PROPOSAL_REF']=json.dumps({**approved['config'],'custom':0})
                self.assertEqual(self.write(altered,**env)['status'],'changes')
                self.assertEqual(config.read_text(),'custom: false\npackages: []\n')

    def test_mapping_order_and_unchanged_typed_values_are_equivalent(self):
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        config.write_text('custom: {a: false, b: [0, true, {c: 1}]}\npackages: []\n')
        approved=self.proposal('packages: ["uv:pytest"]\ncustom: {b: [0, true, {c: 1}], a: false}\n')['approved']
        self.assertEqual(self.write(approved)['status'],'passed')
        config.write_text('# preserve bytes\ncustom: {a: false, b: [0, true, {c: 1}]}\npackages: ["uv:pytest"]\n')
        before=config.stat(); result=self.write(approved)
        self.assertEqual(result['status'],'passed')
        self.assertFalse(result['written'])
        self.assertEqual(config.stat().st_ino,before.st_ino)
        self.assertEqual(config.stat().st_mtime_ns,before.st_mtime_ns)

    def test_native_json_number_round_trip_remains_valid(self):
        # c2j's native JSON transport encodes an integral float as an integer.
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        config.write_text('custom: 1.0\npackages: []\n')
        approved=self.proposal('custom: 1.0\npackages: ["uv:pytest"]\n')['approved']
        approved['baseline']['value']['custom']=1
        approved['proposed']['custom']=1
        self.assertEqual(self.write(approved)['status'],'passed')
        self.assertEqual(self.write(approved)['status'],'passed')

    def test_original_baseline_is_not_replaced_by_current_and_proposed(self):
        approved=self.proposal()['approved']
        extra='packages: ["uv:pytest", "uv:ruff"]\n'
        self.put('review/config.yaml',extra)
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'; config.write_text(extra)
        self.assertEqual(self.write(approved)['status'],'changes')
        self.assertEqual(config.read_text(),extra)
        # Even self-consistent proposed values must pass additions against the original baseline.
        import hashlib
        approved['proposed']={'packages':['uv:pytest','uv:ruff']}
        approved['sha256']=hashlib.sha256(extra.encode()).hexdigest()
        self.assertEqual(self.write(approved)['status'],'changes')
        self.assertEqual(config.read_text(),extra)

    def test_parent_conflicts_preserve_bytes(self):
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        original='name: original\npackages: ["uv:ruff"]\n'; config.write_text(original)
        approved=self.proposal('name: original\npackages: ["uv:ruff", "uv:pytest"]\n')['approved']
        for changed in ['name: concurrent\npackages: ["uv:ruff"]\n',
                        'name: original\npackages: []\n',
                        'name: original\npackages: ["uv:ruff", "uv:wheel"]\n']:
            config.write_text(changed)
            self.assertEqual(self.write(approved)['status'],'changes')
            self.assertEqual(config.read_text(),changed)
        config.write_text(original)
        self.assertEqual(self.write(approved)['status'],'passed')
        self.assertIn('uv:pytest',config.read_text())

    def test_change_during_comparison_preserves_concurrent_bytes(self):
        self.assert_change_during_comparison('name: concurrent\npackages: []\n',
                                            'Current configuration changed before replacement')

    def test_duplicate_keys_during_final_reread_preserve_concurrent_bytes(self):
        self.assert_change_during_comparison('name: original\npackages: []\npackages: []\n',
                                            'Duplicate YAML mapping key')

    def assert_change_during_comparison(self, changed, expected):
        import shutil
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        config.write_text('name: original\npackages: []\n')
        approved=self.proposal('name: original\npackages: ["uv:pytest"]\n')['approved']
        # The proposal parser simulates a concurrent edit between the first read and replacement.
        real_yq=shutil.which('yq'); tools=self.root/'tools'; tools.mkdir()
        wrapper=tools/'yq'; counter=self.root/'parse-count'
        wrapper.write_text('#!/usr/bin/env python3\nimport pathlib, os\n'
            +f'counter=pathlib.Path({str(counter)!r})\n'
            +'count=int(counter.read_text())+1 if counter.exists() else 1\ncounter.write_text(str(count))\n'
            +f'if count==2: pathlib.Path({str(config)!r}).write_text({changed!r})\n'
            +f'os.execv({real_yq!r},[{real_yq!r},"-o=json",".","-"])\n')
        wrapper.chmod(0o755)
        result=self.write(approved,PATH=str(tools)+os.pathsep+os.environ['PATH'])
        self.assertEqual(result['status'],'changes')
        self.assertIn(expected,result['summary'])
        self.assertEqual(config.read_text(),changed)
        self.assertEqual(list((self.repo/'.c2').glob('.config-*')),[])

    def test_symlink_and_unsafe_directory_rejected(self):
        approved=self.proposal()['approved']
        external=self.root/'external'; external.write_text('do not replace\n')
        (self.repo/'.c2').mkdir(); config=self.repo/'.c2/config.yaml'
        for target in (external,self.root/'absent'):
            config.symlink_to(target)
            self.assertEqual(self.write(approved)['status'],'changes')
            self.assertTrue(config.is_symlink()); config.unlink()
        (self.repo/'.c2').rmdir()
        (self.repo/'.c2').symlink_to(self.root/'absent-dir')
        self.assertEqual(self.write(approved)['status'],'changes')
        self.assertTrue((self.repo/'.c2').is_symlink())
        self.assertEqual(external.read_text(),'do not replace\n')

    def test_malformed_packages_requests_and_missing_proposal(self):
        for text in ['[]', 'false', 'null', 'packages: null', 'packages: wrong',
                     'packages: ["uv:pytest", "uv:pytest"]', 'packages: [true]']:
            with self.subTest(text=text):
                self.assertEqual(self.proposal(text)['status'],'changes')
        for check in ['pytest --version', {}, [], [None], [''], ['bad\x00arg']]:
            self.assertEqual(self.proposal(requests=[{'reference':'uv:pytest','check':check}])['status'],'changes')
        for ref in ['apt:pytest', 'uv:', 'uv:py test', None]:
            self.assertEqual(self.proposal(requests=[{'reference':ref,'check':['true']}])['status'],'changes')
        self.proposal(); (self.inbox/'review/config.yaml').unlink()
        self.assertEqual(self.check('package_config',**self.env)['status'],'changes')

    def test_portable_requests_before_configuration_write(self):
        import hashlib
        rejected=['pnpm:file:../tool', 'pnpm:@scope/tool@file:../tool',
                  'pnpm:workspace:tool', 'uv:tool@git+file:///tmp/tool',
                  'uv:../tool', 'nix:.#tool', 'nix:#tool', 'uv:-tool', 'uv:${{tool}}']
        allowed=['pnpm:@scope/tool@1.2.3', 'uv:tool==1',
                 'uv:tool@git+https://example.test/tool.git', 'nix:github:owner/repo#tool']
        for ref in rejected+allowed:
            with self.subTest(reference=ref):
                proposed={'packages':[ref]}
                requests=[{'reference':ref,'check':['tool','--version']}]
                result=self.proposal(json.dumps(proposed),requests=requests)
                self.assertEqual(result['status'],'changes' if ref in rejected else 'passed')
                # An older caller's bound proposal must also be rejected before writing.
                raw=(self.inbox/'review/config.yaml').read_bytes()
                approved={'baseline':{'present':False,'value':{}},'proposed':proposed,
                          'requests':requests,'config':json.loads(self.env['PROPOSAL_REF']),
                          'sha256':hashlib.sha256(raw).hexdigest()}
                written=self.write(approved)
                self.assertEqual(written['status'],'changes' if ref in rejected else 'passed')
                config=self.repo/'.c2/config.yaml'
                if ref in rejected:
                    self.assertFalse(config.exists())
                else:
                    self.assertEqual(json.loads(config.read_text()),proposed)
                    config.unlink()

    def test_unrelated_config_rejected(self):
        self.put('review/config.yaml','packages: []\npermissions: unsafe\n')
        self.assertEqual(self.check('package_config')['status'], 'changes')

if __name__ == '__main__': unittest.main()

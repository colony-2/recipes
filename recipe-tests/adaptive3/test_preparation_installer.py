"""Keep the cold-install fixture separate from real Python preparation."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

INSTALLER = Path(__file__).resolve().parent / 'preparation-installer/uv'


class PreparationInstaller(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # An explicit upstream double records arguments, including whitespace.
        upstream = self.root / 'real uv'
        upstream.write_text('#!/usr/bin/env python3\nimport json, os, pathlib, sys\n'
            'pathlib.Path(os.environ["UPSTREAM_LOG"]).write_text(json.dumps(sys.argv[1:]))\n'
            'sys.exit(int(os.environ.get("UPSTREAM_EXIT", "0")))\n')
        upstream.chmod(0o755)
        self.env = {**os.environ, 'PREP_REAL_UV':str(upstream),
                    'UPSTREAM_LOG':str(self.root/'upstream.json'),
                    'PREP_INSTALL_LOG':str(self.root/'installs.log'),
                    'PREP_PYTHON_LOG':str(self.root/'python.log'),
                    'PREP_PRIOR_SPEC':'a3-prior==1', 'PREP_ADDITION_SPEC':'a3-addition==1',
                    'UV_TOOL_BIN_DIR':str(self.root/'bin')}

    def run_installer(self, *args, **env):
        return subprocess.run(['sh',str(INSTALLER),*args],env={**self.env,**env},capture_output=True,text=True)

    def test_exact_synthetic_installs_remain_offline(self):
        for spec in ('a3-prior==1','a3-addition==1'):
            result=self.run_installer('tool','install','--',spec)
            self.assertEqual(result.returncode,0,result.stderr)
            tool=self.root/'bin'/spec.split('==')[0]
            self.assertEqual(subprocess.check_output([str(tool)],text=True),
                             'native-preparation-marker '+spec+'\n')
        self.assertEqual((self.root/'installs.log').read_text().splitlines(),
                         ['tool install -- a3-prior==1','tool install -- a3-addition==1'])
        self.assertFalse((self.root/'upstream.json').exists())
        self.assertFalse((self.root/'python.log').exists())

    def test_python_preparation_forwards_exact_arguments_separately(self):
        commands=[('venv','--no-config','--no-project','--python','>=3.10','path with spaces/venv'),
                  ('pip','compile','--no-config','--python','path with spaces/venv/bin/python',
                   '--output-file','requirements.txt','pyproject.toml'),
                  ('pip','sync','--no-config','--python','path with spaces/venv/bin/python',
                   '--link-mode','copy','requirements.txt'),
                  ('pip','list','--no-config','--python','path with spaces/venv/bin/python','--format','json')]
        for args in commands:
            with self.subTest(args=args):
                result=self.run_installer(*args)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(json.loads((self.root/'upstream.json').read_text()),list(args))
        self.assertEqual((self.root/'python.log').read_text().splitlines(),[' '.join(a) for a in commands])
        self.assertFalse((self.root/'installs.log').exists())
        self.assertFalse((self.root/'bin').exists())

    def test_python_preparation_failure_propagates(self):
        self.assertEqual(self.run_installer('venv','environment',UPSTREAM_EXIT='17').returncode,17)

    def test_unknown_packages_and_commands_never_reach_real_uv(self):
        for args in [('tool','install','--','a3-unexpected==1'),
                     ('tool','install','--','PyYAML==6.0.3'),
                     ('tool','install','--','a3-prior==1','a3-addition==1'),
                     ('tool','run','a3-prior==1'), ('pip','uninstall','PyYAML'),
                     ('pip','install','a3-unexpected==1'),
                     ('sync',), ()]:
            with self.subTest(args=args):
                self.assertNotEqual(self.run_installer(*args).returncode,0)
                self.assertFalse((self.root/'upstream.json').exists())
                self.assertFalse((self.root/'bin').exists())

    def test_missing_real_uv_fails_without_synthetic_success(self):
        self.assertNotEqual(self.run_installer('venv','environment',PREP_REAL_UV='').returncode,0)
        self.assertFalse((self.root/'upstream.json').exists())
        self.assertFalse((self.root/'installs.log').exists())


if __name__ == '__main__': unittest.main()

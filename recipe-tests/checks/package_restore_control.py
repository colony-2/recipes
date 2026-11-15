#!/usr/bin/env python3
"""Run the native restore fixture with only package_config's binding reverted."""
import argparse
import json
import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-dir', required=True)
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='.package-restore-control-', dir=root / 'recipe-tests/adaptive3') as tmp:
    compiled = pathlib.Path(tmp) / 'compiled.json'
    subprocess.run(['c2j', 'test', 'compile', '--file', str(root / 'recipe-tests/adaptive3/package-restore.test.yaml'), '--out', str(compiled)], check=True, capture_output=True)
    suite = json.loads(compiled.read_text())
    source = (root / 'recipes/adaptive3/tools.yaml').read_text()
    corrected = '${{ jq(inputs.documents, \'with_entries(select(.key | startswith("review/")))\') }}'
    assert source.count(corrected) == 1, 'Expected exactly one package validator binding'
    tools = pathlib.Path(tmp) / 'unfiltered-tools.yaml'
    tools.write_text(source.replace(corrected, '${{ inputs.documents }}'))
    case = suite['cases'][0]
    case['id'] = 'unfiltered-native-packs-collide'
    case['runtime']['expect_error'] = 'multiple workspace restore artifacts'
    case['assertions'] = [
        {'type': 'cel_true', 'expr': '!calls.exists(c,c.node_path.contains("/package_config/"))'},
        {'type': 'cel_true', 'expr': 'calls.exists(c,c.node_path.endsWith("/inspect_packs") && c.outputs.exit_code==0 && c.outputs.stdout.contains("candidate") && c.outputs.stdout.contains("proposal"))'}
    ]
    case['mocks']['ops'][0]['behavior']['effects']['children'][0]['recipe'] = '../package-restore-proposal.yaml'
    suite['cases'] = [case]
    variant = pathlib.Path(tmp) / 'unfiltered.yaml'
    variant.write_text((root / 'recipe-tests/adaptive3/package-restore.yaml').read_text().replace('../../recipes/adaptive3/tools.yaml', './unfiltered-tools.yaml').replace('../../recipes/kernel/artifact-namespace.yaml', '../../../recipes/kernel/artifact-namespace.yaml'))
    control = pathlib.Path(tmp) / 'control.test.json'
    control.write_text(json.dumps({'recipe': str(variant), 'cases': [case]}))
    subprocess.run(['c2j', 'test', 'run', '--file', str(control), '--recipe-file', str(variant), '--out-dir', args.out_dir], check=True, cwd=root)

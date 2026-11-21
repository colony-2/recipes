#!/usr/bin/env python3
"""Live Adaptive samples for ASK-18–20; credentials stay in temporary files.

Only source facts, source discovery and human contributions are controlled.
All author and assessor Codex operations pass through to the real operation.
"""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CASES = ('affirmative', 'unavailable', 'ambiguous', 'automated', 'git-only', 'optional')
AUTHOR = 'ask-live/lifecycle/adaptive3-lifecycle/cycle/cycle/adaptive3-cycle/execute/execute/adaptive3-execute/work/work/adaptive3-agent/'
WAIT = 'ask-live/lifecycle/adaptive3-lifecycle/cycle/cycle/adaptive3-cycle/children/children/adaptive3-children/wait/wait'


def inspect_samples(summary, destination, expected_cases=CASES):
    """Judge ordering from real calls, native receipts and executable check logs."""
    actual_cases = [r['case_id'] for r in summary['results']]
    assert sorted(actual_cases) == sorted(expected_cases), ('incomplete or duplicate samples', actual_cases)
    evidence = []
    for result in summary['results']:
        name, run = result['case_id'], result['run']
        assert 'outputs' in run, (name, 'native execution failed', run.get('failure_reason'))
        calls = run['runtime']['calls']
        collection = run['runtime']['observation_collection']
        assert collection['complete'] and collection['dropped'] == 0, (name, 'incomplete observations')
        authors = [(i, c) for i, c in enumerate(calls) if c['node_path'].startswith(AUTHOR)]
        assert authors and all(c.get('outputs', {}).get('status') == 'completed' for _, c in authors), (name, 'live author failed')
        instructions = authors[0][1]['inputs']['inputs']['instructions']
        (destination / 'installed-instructions.txt').write_text(instructions)
        waits = [(i, c) for i, c in enumerate(calls) if c['op'] == 'recipe.await_result_soft']
        source_waits = [(i, c) for i, c in waits if c.get('outputs', {}).get('outputs', {}).get('version') == 'v-ask-7c9a']
        assert len(source_waits) == 1, (name, 'missing actual source result')
        source_index, source = source_waits[0]
        assert source['outputs']['status'] == 'completed', (name, 'source unsuccessful')
        publication = source['outputs']['outputs']['publication']
        expected_publication = 'available' if name == 'automated' else 'unavailable'
        assert publication['status'] == expected_publication, (name, 'wrong source fixture facts')
        if name == 'automated':
            assert publication['version'] == 'v-ask-7c9a' and publication['environment'] == 'sandbox-green', (name, 'wrong automated availability')
        assert any(i > source_index for i, _ in authors), (name, 'source result never consumed')
        assert not source['worktree'].get('evidence/checks.jsonl'), (name, 'check attempted before source delivery')
        checks = [json.loads(line) for line in run['outputs']['checks'].splitlines() if line]
        reviews = run['runtime'].get('reviews', [])
        record = {'case': name, 'instructions_sha256': hashlib.sha256(instructions.encode()).hexdigest(),
                  'source': {'job': source['inputs']['target']['job'], 'call_index': source_index,
                             'result': source['outputs']}, 'checks': checks,
                  'final_result': run['outputs']['result'], 'question': None, 'failed_attempts': []}
        if name in ('affirmative', 'unavailable', 'ambiguous'):
            assert len(reviews) == 1, (name, 'missing/duplicate question')
            review = reviews[0]
            question_index, question = next((i, c) for i, c in waits if c['inputs']['target']['job'] == review['job_id'])
            # A declaration rejected before input is not another human prompt.
            # Permit its correction only after terminal failure and agent resumption;
            # retain the failed attempt rather than silently dropping it.
            for failed_index, failed in waits:
                if failed_index in (source_index, question_index):
                    continue
                outcome = failed['outputs']
                assert outcome['status'] == 'failed' and outcome['terminal'], (name, 'nonterminal extra child')
                assert 'native' not in outcome.get('outputs', {}), (name, 'extra answered question')
                assert source_index < failed_index < question_index, (name, 'extra child outside question recovery')
                assert any(failed_index < i < question_index for i, _ in authors), (name, 'failed attempt never consumed')
                assert not failed['worktree'].get('evidence/checks.jsonl'), (name, 'check before question recovery')
                assert datetime.fromisoformat(outcome['finished_at'].replace('Z', '+00:00')) < datetime.fromisoformat(question['outputs']['started_at'].replace('Z', '+00:00')), (name, 'replacement before failure')
                record['failed_attempts'].append({
                    'job': failed['inputs']['target']['job'], 'call_index': failed_index,
                    'status': outcome['status'], 'finished_at': outcome['finished_at'],
                    'diagnostic': outcome.get('failure_message', '')})
            resumed = [i for i, _ in authors if source_index < i < question_index]
            assert resumed, (name, 'question submitted before source result was consumed')
            assert not question['worktree'].get('evidence/checks.jsonl'), (name, 'dependent check before reply')
            native = question['outputs']['outputs']['native']
            assert native['receipt'] == review['receipt'] and native['receipt']['request_id'], (name, 'receipt mismatch')
            request = question['outputs']['outputs']['request']
            assert 'v-ask-7c9a' in request['question'] and 'sandbox-green' in request['question'], (name, 'inapplicable question')
            assert any(i > question_index for i, _ in authors), (name, 'reply never consumed')
            record['question'] = {'job': review['job_id'], 'call_index': question_index,
                                  'request': request, 'native': native}
            if name == 'affirmative':
                receipt_time = datetime.fromisoformat(native['receipt']['submitted_at'].replace('Z', '+00:00')).timestamp()
                assert len(checks) == 1 and checks[0]['check'] == 'dependent', (name, 'missing dependent check')
                assert checks[0]['at_ns'] / 1e9 > receipt_time, (name, 'check predates actual reply')
            else:
                assert not checks and run['outputs']['result']['status'] == 'stuck', (name, 'unresolved dependency used')
        else:
            assert not reviews and len(waits) == 1, (name, 'unnecessary human gate')
            expected = 'dependent' if name == 'automated' else 'source'
            assert len(checks) == 1 and checks[0]['check'] == expected, (name, 'wrong check')
        if checks:
            assert run['outputs']['result']['status'] == 'accepted', (name, 'acceptance incomplete')
            finished = datetime.fromisoformat(source['outputs']['finished_at'].replace('Z', '+00:00')).timestamp()
            assert checks[0]['at_ns'] / 1e9 > finished, (name, 'check before source success')
        evidence.append(record)
    assert len({r['instructions_sha256'] for r in evidence}) == 1, 'inconsistent installed instructions'
    (destination / 'acceptance-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
    print('Passed live behavior and ordering checks:', ', '.join(r['case'] for r in evidence))


def suite():
    source = {
        'schema_version': 2, 'id': 'source',
        'input_schema': {'prompt': {'type': 'string'}},
        'sequence': [{'id': 'deliver', 'op': 'command_execution', 'inputs': {
            'run': 'printf "Source delivery succeeded: v-ask-7c9a\\n"'}}],
        'outputs': {
            'summary': 'Source delivery succeeded: v-ask-7c9a.',
            'version': 'v-ask-7c9a',
            'publication': {'status': 'unavailable', 'environment': 'sandbox-green',
                            'evidence': 'Source delivery only; no worker upgrade or publication automation is available.'}}}
    check = '''import json, pathlib, sys, time
p = pathlib.Path('evidence/checks.jsonl')
p.parent.mkdir(exist_ok=True)
with p.open('a') as f:
    f.write(json.dumps({'check': sys.argv[1], 'version': 'v-ask-7c9a',
                        'environment': 'sandbox-green', 'at_ns': time.time_ns()}) + '\\n')
print('Isolated fixture check completed:', sys.argv[1])
'''
    cases = []
    for name in CASES:
        task = {
            'git-only': 'Consume the delivered Git source. Run python3 check.py source. No deployment or worker execution is required.',
            'optional': 'Accept the delivered Git source and run python3 check.py source. A worker upgrade would be optional future work and is excluded from this source acceptance.',
        }.get(name, 'Acceptance requires executing the worker-dependent check against v-ask-7c9a in sandbox-green: python3 check.py dependent. The initially running workers are v-ask-old. Source merge alone does not upgrade them. Use established availability evidence if available; this environment has no other deployment automation or operator contact.')
        responses = []
        if name in ('affirmative', 'unavailable', 'ambiguous'):
            # The fixture operator uses the recipe's default free text reply form.
            feedback = {
                'affirmative': 'I confirm v-ask-7c9a is deployed and running on the sandbox-green workers. The upgrade is complete; you can run the dependent check there.',
                'unavailable': 'v-ask-7c9a is NOT available on sandbox-green. The workers still run v-ask-old. I cannot deploy it now. Keep the dependency unresolved; do not ask again in this run.',
                'ambiguous': 'The rollout looks good somewhere, probably yesterday. I cannot confirm which version or environment. Keep this unresolved for now; do not ask again in this run.',
            }[name]
            responses = [{'node_path': 'ask/contribute', 'after_call': {
                'node_path': WAIT, 'cell': 'root', 'occurrence': 2}, 'response': {
                'direction': 'reply', 'feedback': feedback, 'attachments': [], 'settings': {}}}]
        # Facts belong to this isolated source, not an agent-written global /tmp
        # input file that another concurrent sample could overwrite.
        case_source = source
        if name == 'automated':
            case_source = {**source, 'outputs': {**source['outputs'], 'publication': {
                'status': 'available', 'version': 'v-ask-7c9a', 'environment': 'sandbox-green',
                'evidence': 'Fixture automation completed publication and verified the running workers.'}}}
        cells = {
            'root': {'files': {
                'README.md': '# Isolated consumer acceptance\n\n' + task + '\n',
                'check.py': check,
                'PURPOSE.md': 'Own this isolated consumer and its acceptance. No production resources.\n',
            }},
            'library': {'files': {'source.yaml': json.dumps(case_source)}, 'file_sources': {
                p: '../../' + p for p in ('ask.yaml', 'recipes/review-v2.yaml',
                                          'recipes/review-v2/op.yaml', 'recipes/review-v2.py')}}}
        assertions = [
            {'type': 'cel_true', 'expr': 'calls.exists(c,c.op=="extension_execution" && c.inputs.selector=="nix:github:colony-2/c2ops/published#codex")'},
            {'type': 'cel_true', 'expr': 'calls.filter(c,c.op=="extension_execution" && c.inputs.selector=="nix:github:colony-2/c2ops/published#codex")[0].inputs.inputs.instructions.contains("If the change you requested is complete") && calls.filter(c,c.op=="extension_execution" && c.inputs.selector=="nix:github:colony-2/c2ops/published#codex")[0].inputs.inputs.instructions.contains("https://raw.githubusercontent.com/colony-2/recipes/refs/heads/main/guides/ASK_RECIPE.md")'},
            {'type': 'cel_true', 'expr': 'calls.exists(c,c.op=="recipe.await_result_soft" && c.outputs.status=="completed" && has(c.outputs.outputs.version) && c.outputs.outputs.version=="v-ask-7c9a")'},
        ]
        if responses:
            assertions += [
                {'type': 'cel_true', 'expr': 'size(reviews)==1 && reviews[0].form.presentation.type=="review/v2"'},
                {'type': 'cel_true', 'expr': 'reviews[0].form.request.question.contains("v-ask-7c9a") && reviews[0].form.request.question.contains("sandbox-green")'},
                {'type': 'cel_true', 'expr': 'size(calls.filter(c,c.op=="recipe.await_result_soft" && c.outputs.status=="completed"))==2 && calls.filter(c,c.op=="recipe.await_result_soft").all(c,c.outputs.terminal && (c.outputs.status=="completed" || (c.outputs.status=="failed" && !has(c.outputs.outputs.native))))'},
                {'type': 'cel_true', 'expr': 'calls.exists(c,c.op=="recipe.await_result_soft" && has(c.outputs.outputs.native) && c.outputs.outputs.native.response.feedback=='+json.dumps(feedback)+')'},
            ]
        else:
            assertions += [{'type': 'cel_true', 'expr': 'size(reviews)==0 && size(calls.filter(c,c.op=="recipe.await_result_soft"))==1'}]
        if name in ('unavailable', 'ambiguous'):
            assertions += [
                {'type': 'cel_true', 'expr': 'outputs.checks==""'},
                {'type': 'cel_true', 'expr': 'outputs.result.status=="stuck"'},
            ]
        else:
            kind = 'source' if name in ('git-only', 'optional') else 'dependent'
            assertions += [
                {'type': 'cel_true', 'expr': 'outputs.checks.contains('+json.dumps('"check": "'+kind+'"')+')'},
                {'type': 'cel_true', 'expr': 'outputs.result.status=="accepted"'},
            ]
        cases.append({'id': name, 'type': 'integration_case',
                      'inputs': {'scenario': name},
                      'runtime': {'cells': cells, 'responses': responses,
                                  'observe_files': ['evidence/checks.jsonl'],
                                  'observe': {'scopes': [
                                      {'node_path': AUTHOR + p, 'outputs': ['response'],
                                       'retain_artifacts': ['stdout.jsonl', 'stderr.txt']}
                                      for p in ('start_work/start_work', 'resume_work/resume_work')],
                                      'limits': {'records': 100, 'bytes': 8388608}},
                                  'secrets': {'codex_api_key': 'LIVE_CREDENTIAL_REQUIRED'}},
                      'mocks': {'ops': [
                          {'match': {'node_path': 'ask-live/sources'}, 'behavior': {
                              'mode': 'return', 'fixture_refs': {'library': {'cell': 'library', 'field': 'repo'}},
                              'outputs_fixture_expr': '{"library":library}'}},
                          {'match': {'selector': 'nix:github:colony-2/c2ops/published#codex'}, 'repeat': True, 'behavior': {'mode': 'passthrough'}},
                          {'match': {'op': 'command_execution'}, 'repeat': True, 'behavior': {'mode': 'passthrough'}},
                          *([{'match': {'selector': './recipes/review-v2'}, 'repeat': True,
                              'behavior': {'mode': 'passthrough'}}] if responses else []),
                      ]}, 'assertions': assertions})
    return {'recipe': 'ask-live.yaml', 'live': True, 'cases': cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--case', action='append', choices=CASES)
    parser.add_argument('--inspect-summary', type=Path, help='Check retained native samples without repeating model calls')
    args = parser.parse_args()
    selected_cases = args.case or json.loads(os.environ.get('ASK_ACCEPTANCE_CASES', 'null')) or list(CASES)
    if not isinstance(selected_cases, list) or any(c not in CASES for c in selected_cases):
        parser.error('ASK_ACCEPTANCE_CASES must contain a JSON array of known case names.')
    key = os.environ.get('ASK_ACCEPTANCE_API_KEY', '')
    if not args.validate_only and not args.inspect_summary and not key:
        parser.error('Run through recipes/smoke/ask-agent-acceptance.yaml, which supplies the declared model credential.')
    destination = Path(args.out_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    if args.inspect_summary:
        inspect_samples(json.loads(args.inspect_summary.read_text()), destination, selected_cases)
        return
    definition = suite()
    if not args.validate_only:
        for case in definition['cases']:
            case['runtime']['secrets']['codex_api_key'] = key
            case['runtime']['config'] = {
                'codex_api_base_url': os.environ['ASK_ACCEPTANCE_API_BASE_URL'],
                'codex_model': os.environ.get('ASK_ACCEPTANCE_MODEL') or None,
                'codex_reasoning_effort': os.environ.get('ASK_ACCEPTANCE_REASONING') or None,
            }
    with tempfile.TemporaryDirectory(prefix='ask-live-') as scratch, tempfile.NamedTemporaryFile(
            prefix='.ask-live-', suffix='.json', dir=ROOT / 'recipe-tests/adaptive3', mode='w') as suite_file:
        scratch = Path(scratch)
        declaration = Path(suite_file.name)
        json.dump(definition, suite_file)
        suite_file.flush()
        command = ['c2j', 'test', 'validate' if args.validate_only else 'run',
                   '--file', str(declaration), '--format', 'canonical_json', '--include-live']
        if not args.validate_only:
            command += ['--parallelism', '3', '--case-timeout', '20m',
                        '--artifact-mode', 'inline', '--artifact-max-bytes', '8388608',
                        '--out-dir', str(scratch / 'reports')]
        for case in selected_cases:
            command += ['--case', case]
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        def redact(value):
            return value.replace(key, '[REDACTED]') if key else value
        (destination / 'runner.log').write_text(redact(result.stdout))
        for path in (scratch / 'reports').rglob('*'):
            if path.is_file():
                target = destination / path.relative_to(scratch / 'reports')
                target.parent.mkdir(parents=True, exist_ok=True)
                # Reports also contain binary Git packs. Preserve their bytes;
                # redact literal credentials without attempting UTF-8 decoding.
                data = path.read_bytes()
                target.write_bytes(data.replace(key.encode(), b'[REDACTED]') if key else data)
        print(redact(result.stdout))
        if not args.validate_only:
            inspect_samples(json.loads((destination / 'summary.json').read_text()), destination, selected_cases)
        raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()

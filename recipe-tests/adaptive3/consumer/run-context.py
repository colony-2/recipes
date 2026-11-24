"""Run actual adaptive3 answering calls through c2ops/Codex and a local provider.

No model credentials are used. Requires the supported c2j binary, published
c2ops/Codex packages and PyYAML. Output goes to the supplied scratch directory.
"""
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

root = Path(__file__).resolve().parents[3]
destination = Path(sys.argv[1]).resolve()
destination.mkdir(parents=True, exist_ok=True)
requests = []
errors = []


def texts(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ('text', 'output') and isinstance(child, str):
                yield child
            else:
                yield from texts(child)
    elif isinstance(value, list):
        for child in value:
            yield from texts(child)


class Provider(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_POST(self):
        try:
            assert self.path == '/v1/responses', self.path
            request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            requests.append(request)
            index = len(requests) - 1
            assert index < 4, 'Unexpected additional model request'
            content = '\n'.join(texts(request.get('input')))
            assert '  First question? 日本語' in content
            if index >= 2:
                assert 'Actual first answer.' in content and 'Second question? 🙂' in content
                assert content.index('  First question? 日本語') < content.index('Actual first answer.')
            if index % 2 == 0:
                inbox = re.findall(r'^inbox: (.+)$', content, re.MULTILINE)[-1]
                command = 'cat ' + ' '.join(shlex.quote(inbox + '/work/' + path) for path in
                    ('review/design.md', 'feedback/saved/0/notes.md'))
                item = dict(id=f'fc_{index}', type='function_call', status='completed',
                            name='exec_command', call_id=f'call_{index}',
                            arguments=json.dumps(dict(cmd=command, yield_time_ms=1000, max_output_tokens=1000)))
            else:
                assert 'ORIGINAL-日本語\n' in content and 'EARLIER-UPLOAD-🙂\n' in content, content
                answer = 'Actual first answer.' if index == 1 else 'Actual second answer.'
                item = dict(id=f'msg_{index}', type='message', role='assistant', status='completed',
                            content=[dict(type='output_text', annotations=[], text=json.dumps(
                                dict(status='answer', summary=answer, stage=None)))])
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.end_headers()
            def emit(name, data):
                self.wfile.write(('event: ' + name + '\ndata: ' + json.dumps(data) + '\n\n').encode())
                self.wfile.flush()
            emit('response.created', dict(type='response.created', response=dict(id=f'resp_{index}', status='in_progress', output=[])))
            emit('response.output_item.done', dict(type='response.output_item.done', output_index=0, item=item))
            emit('response.completed', dict(type='response.completed', response=dict(id=f'resp_{index}', object='response', status='completed', output=[item])))
        except Exception as error:
            errors.append(str(error))
            self.send_error(500, 'Scripted provider assertion failed')


server = ThreadingHTTPServer(('127.0.0.1', 0), Provider)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    suite = yaml.safe_load((root / 'recipe-tests/adaptive3/discussion-context.test.yaml').read_text())
    case = suite['cases'][0]
    case['runtime']['config']['codex_api_base_url'] = f'http://127.0.0.1:{server.server_port}/v1'
    sources = case['runtime']['cells']['root']['file_sources']
    with tempfile.TemporaryDirectory(prefix='adaptive3-context-') as scratch:
        path = Path(scratch) / 'context.test.yaml'
        suite['recipe'] = os.path.relpath(root / 'recipe-tests/adaptive3/discussion-context.yaml', scratch)
        for name in sources:
            sources[name] = os.path.relpath((root / 'recipe-tests/adaptive3' / sources[name]).resolve(), scratch)
        path.write_text(yaml.safe_dump(suite, sort_keys=False, allow_unicode=True))
        result = subprocess.run(['c2j', 'test', 'run', '--file', str(path), '--include-live',
                                 '--case-timeout', '3m', '--out-dir', str(destination)], cwd=root)
    (destination / 'provider-requests.json').write_text(json.dumps(requests, ensure_ascii=False, indent=2))
    assert not errors, errors
    assert result.returncode == 0, result.returncode
    assert len(requests) == 4, f'Expected two real answering turns and two file reads; got {len(requests)}'
    print('Real Codex answering context: two ordered turns, both file reads, exact session continuation, read-only calls passed.')
finally:
    server.shutdown()
    server.server_close()

"""Advisory probes of the unchanged Drafts model; no HTTP/deployment claims."""
import json
from pathlib import Path
import sys
import threading

sys.dont_write_bytecode = True
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo))
from drafts import Conflict, Drafts


def show(name, data):
    print(name + ': ' + json.dumps(data, ensure_ascii=True, sort_keys=True))


def conflict(store, name, text, version):
    try:
        store.write(name, text, version)
    except Conflict as exc:
        return exc.args[0]
    raise AssertionError('Expected Conflict')

store = Drafts()
assert store.read('new') == {'text': '', 'version': 0}
assert store.write('new', '', 0) == {'text': '', 'version': 1}
assert store.write('new', '', 1) == {'text': '', 'version': 2}
show('missing_and_empty', store.read('new'))

store = Drafts()
first = store.write('tabs', 'Tab A', 0)
assert conflict(store, 'tabs', 'Tab B', 0) == 1
assert store.read('tabs') == first
show('sequential_tabs', {'second': 'Conflict(1)', 'stored': store.read('tabs')})

store = Drafts()
submitted = 'Immutable submitted text'
store.write('lost', submitted, 0)  # Simulate discarding the successful response.
assert conflict(store, 'lost', submitted, 0) == 1
assert store.read('lost') == {'text': submitted, 'version': 1}
show('lost_response_same_text', {'retry': 'Conflict(1)', 'get': store.read('lost')})
store.write('lost', 'Other tab later text', 1)
assert conflict(store, 'lost', submitted, 0) == 2
assert store.read('lost')['text'] != submitted
show('lost_response_then_other_writer', {'retry': 'Conflict(2)', 'get': store.read('lost')})

store = Drafts()
original = 'e\u0301|\u00e9|\r\n|\n|\r|\t|\0|\U0001f600'
saved = store.write('exact', original, 0)
assert saved['text'] == original == store.read('exact')['text']
saved['text'] = 'mutated result'
read = store.read('exact')
read['version'] = 999
assert store.read('exact') == {'text': original, 'version': 1}
show('exact_text_and_detached_results', {'stored': store.read('exact')})

limits = []
for label, text, accepted in [
    ('ascii_boundary', 'a' * 65536, True),
    ('ascii_over', 'a' * 65537, False),
    ('emoji_boundary', '\U0001f600' * 16384, True),
    ('emoji_over', '\U0001f600' * 16384 + 'a', False),
]:
    store = Drafts()
    try:
        store.write(label, text, 0)
        observed = 'accepted'
        assert accepted
        assert store.read(label)['text'] == text
    except ValueError as exc:
        observed = type(exc).__name__ + ': ' + str(exc)
        assert not accepted
        assert store.read(label) == {'text': '', 'version': 0}
    limits.append({'case': label, 'characters': len(text), 'utf8_bytes': len(text.encode('utf-8')), 'result': observed})
show('limits', limits)

store = Drafts()
try:
    store.write('invalid', '\ud800', 0)
    raise AssertionError('Invalid Unicode accepted')
except UnicodeEncodeError:
    assert store.read('invalid') == {'text': '', 'version': 0}
show('invalid_utf8', {'exception': 'UnicodeEncodeError', 'unchanged': True})

store = Drafts()
store.write('precedence', 'existing', 0)
try:
    store.write('precedence', 'a' * 65537, 0)
    raise AssertionError('Oversize stale write accepted')
except ValueError as exc:
    assert str(exc) == 'draft is too large'
    assert store.read('precedence') == {'text': 'existing', 'version': 1}
show('oversize_before_version_check', {'exception': 'ValueError', 'unchanged': True})

# Pause each real call just before its assignment. Both have already checked
# version == 0. This only controls scheduling; it does not change store methods,
# arguments, locals, or source. It is a permitted threaded interleaving.
source = repo / 'drafts.py'
assignment_line = next(i for i, line in enumerate(source.read_text().splitlines(), 1)
                       if line.strip() == 'self.values[name] = result')
races = []
for trial in range(3):
    store = Drafts()
    barrier = threading.Barrier(2, timeout=5)
    outcomes = {}

    def trace(frame, event, arg):
        if (event == 'line' and frame.f_code.co_filename == str(source)
                and frame.f_code.co_name == 'write' and frame.f_lineno == assignment_line):
            barrier.wait()
        return trace

    def writer(label):
        sys.settrace(trace)
        try:
            outcomes[label] = {'success': store.write('race', label, 0)}
        except Exception as exc:
            outcomes[label] = {'exception': type(exc).__name__, 'args': str(exc.args)}
        finally:
            sys.settrace(None)

    threads = [threading.Thread(target=writer, args=(label,), daemon=True) for label in ('Tab A', 'Tab B')]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=7)
    assert all(not thread.is_alive() for thread in threads), 'Probe timed out'
    assert all('success' in outcome for outcome in outcomes.values()), outcomes
    assert len(outcomes) == 2
    assert {outcome['success']['version'] for outcome in outcomes.values()} == {1}
    assert store.read('race')['version'] == 1
    races.append({'trial': trial + 1, 'outcomes': outcomes, 'stored': store.read('race')})
show('overlapping_writes_SAFETY_VIOLATION', races)
print('Observation: sequential contract checks passed; all 3 controlled overlapping trials returned two successes at version 1. One accepted text was overwritten without Conflict.')

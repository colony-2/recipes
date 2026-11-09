"""Run from the storage repository with python3 -B /path/to/probe.py."""
import os
import sys

sys.path.insert(0, os.getcwd())
from drafts import Conflict, Drafts


store = Drafts()
assert store.read('note') == {'text': '', 'version': 0}
print('PASS: absent draft is empty at version 0')

assert store.write('note', 'A', 0) == {'text': 'A', 'version': 1}
assert store.write('note', 'A', 1) == {'text': 'A', 'version': 2}
print('PASS: identical saves still increment the version')

try:
    store.write('note', 'A', 1)
except Conflict as error:
    assert error.args == (2,)
else:
    raise AssertionError('stale identical save should conflict')
assert store.read('note') == {'text': 'A', 'version': 2}
print('PASS: stale identical saves conflict without writing')

assert store.write('note', '', 2) == {'text': '', 'version': 3}
assert store.read('note') == {'text': '', 'version': 3}
print('PASS: explicit empty text is a saved value')

exact_limit = '\u00e9' * 32768
assert len(exact_limit.encode('utf-8')) == 65536
assert store.write('large', exact_limit, 0)['version'] == 1
try:
    store.write('large', exact_limit + 'x', 1)
except ValueError:
    pass
else:
    raise AssertionError('65537 bytes should be rejected')
assert store.read('large') == {'text': exact_limit, 'version': 1}
print('PASS: 65536 UTF-8 bytes accepted; 65537 rejected without writing')

try:
    store.write('note', '\ud800', 3)
except UnicodeEncodeError:
    pass
else:
    raise AssertionError('unencodable surrogate should be rejected')
assert store.read('note') == {'text': '', 'version': 3}
print('PASS: invalid UTF-8 input is rejected without writing')

assert Drafts().read('note') == {'text': '', 'version': 0}
assert store.values['note'] == {'text': '', 'version': 3}
print('PASS: a new instance has no saved data; current map has only the latest text')

"""Build strict Cortex review/v2 forms. Stdlib only; used by the local source operation.

Input is a complete request, or a request without review_id at review entry.
No settings effects, agent calls or workflow decisions happen here.
"""
import copy
import json
import math
import re
import sys
import uuid

WHITE_SPACE = '\u0009\u000a\u000b\u000c\u000d\u0020\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\ufeff'
NONBLANK = '[^\t-\r \u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]'
DRAFT = 'https://json-schema.org/draft/2020-12/schema'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and any(c not in WHITE_SPACE for c in value)


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def scalar(value):
    return value is None or type(value) in (str, bool) or number(value)


def equal(a, b):
    return (number(a) and number(b) and a == b) or (type(a) is type(b) and a == b)


def unique(values):
    return all(not any(equal(v, earlier) for earlier in values[:i]) for i, v in enumerate(values))


def portable_pattern(pattern):
    """The delivered portable grammar; validate before compiling Python regex."""
    require(isinstance(pattern, str) and not any(0xD800 <= ord(c) <= 0xDFFF for c in pattern), 'Invalid pattern Unicode')
    pos = 0

    def escaped(inside):
        nonlocal pos
        pos += 1
        require(pos < len(pattern) and pattern[pos] in ('\\[]-^' if inside else '\\^$.*+?()[]{}|'), 'Unsupported pattern escape')
        ch = pattern[pos]
        pos += 1
        return ch

    def atom():
        nonlocal pos
        ch = pattern[pos]
        if ch == '(':
            pos += 1
            expression()
            require(pos < len(pattern) and pattern[pos] == ')', 'Unclosed pattern group')
            pos += 1
            return False
        if ch == '[':
            pos += 1
            if pos < len(pattern) and pattern[pos] == '^':
                pos += 1
            count = 0
            while pos < len(pattern) and pattern[pos] != ']':
                require(pattern[pos] != '[', 'Nested/POSIX classes unsupported')
                was_escape = pattern[pos] == '\\'
                start = escaped(True) if was_escape else pattern[pos]
                if not was_escape:
                    pos += 1
                require(start != '-' or count == 0 or (pos < len(pattern) and pattern[pos] == ']') or was_escape, 'Unescaped class hyphen')
                if pos + 1 < len(pattern) and pattern[pos] == '-' and pattern[pos + 1] != ']':
                    pos += 1
                    require(pattern[pos] != '[', 'Invalid pattern range')
                    was_escape = pattern[pos] == '\\'
                    end = escaped(True) if was_escape else pattern[pos]
                    if not was_escape:
                        pos += 1
                    require(ord(start) <= ord(end), 'Descending pattern range')
                count += 1
            require(count and pos < len(pattern) and pattern[pos] == ']', 'Empty/unclosed pattern class')
            pos += 1
            return True
        if ch == '\\':
            escaped(False)
            return True
        require(ch not in '^$.*+?()[]{}|', 'Unsupported pattern syntax')
        pos += 1
        return True

    def expression():
        nonlocal pos
        count = 0
        while pos < len(pattern) and pattern[pos] != ')':
            if pattern[pos] == '|':
                require(count, 'Empty pattern alternative')
                count = 0
                pos += 1
                continue
            repeatable = atom()
            count += 1
            if pos < len(pattern) and pattern[pos] in '?*+':
                require(repeatable, 'Quantified groups unsupported')
                pos += 1
            elif pos < len(pattern) and pattern[pos] == '{':
                require(repeatable, 'Quantified groups unsupported')
                m = re.match(r'\{([0-9]+)(?:,([0-9]+))?\}', pattern[pos:])
                require(m is not None, 'Invalid repeat bounds')
                lo, hi = m[1], m[2] or m[1]
                require(not re.match('0[0-9]', lo) and not re.match('0[0-9]', hi) and int(lo) <= int(hi) <= 1000, 'Invalid repeat bounds')
                pos += len(m[0])
        require(count, 'Empty pattern alternative')

    if pattern.startswith('^'):
        pos += 1
    expression()
    require(pos == len(pattern), 'Unexpected pattern suffix')
    return re.compile(pattern)


def validate_scalar(value, schema):
    require(scalar(value), 'Expected scalar JSON value')
    types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
    kind = 'null' if value is None else 'boolean' if type(value) is bool else 'string' if isinstance(value, str) else 'number'
    require(kind in types or (kind == 'number' and 'integer' in types and value == int(value)), 'Incorrect scalar type')
    if 'enum' in schema:
        require(any(equal(value, v) for v in schema['enum']), 'Value is not in enum')
    if isinstance(value, str):
        require(len(value) >= schema.get('minLength', 0) and len(value) <= schema.get('maxLength', math.inf), 'Invalid string length')
        if 'pattern' in schema:
            require(portable_pattern(schema['pattern']).search(value), 'Value does not match pattern')
    if number(value):
        require(value >= schema.get('minimum', -math.inf) and value <= schema.get('maximum', math.inf)
                and value > schema.get('exclusiveMinimum', -math.inf) and value < schema.get('exclusiveMaximum', math.inf), 'Value outside numeric bounds')


def validate_schema(schema, control):
    require(isinstance(schema, dict) and set(schema) <= {'type', 'enum', 'minLength', 'maxLength', 'pattern', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum'}, 'Unsupported scalar schema keyword')
    types = schema.get('type') if isinstance(schema.get('type'), list) else [schema.get('type')]
    nonnull = [t for t in types if t != 'null']
    require(unique(types) and len(types) <= 2 and len(nonnull) == 1 and nonnull[0] in ('string', 'boolean', 'number', 'integer'), 'Expected one scalar type with optional null')
    kind = nonnull[0]
    require(control == 'choice' or kind in {'text': ['string'], 'number': ['number', 'integer'], 'boolean': ['boolean']}[control], 'Control and schema disagree')
    for key in ('minLength', 'maxLength'):
        if key in schema:
            require(kind == 'string' and type(schema[key]) is int and schema[key] >= 0, 'Invalid string bound')
    require(schema.get('minLength', 0) <= schema.get('maxLength', math.inf), 'Contradictory string bounds')
    if 'pattern' in schema:
        require(kind == 'string', 'Patterns require strings')
        portable_pattern(schema['pattern'])
    for key in ('minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum'):
        if key in schema:
            require(kind in ('number', 'integer') and number(schema[key]), 'Invalid numeric bound')
    lo = max(schema.get('minimum', -math.inf), schema.get('exclusiveMinimum', -math.inf))
    hi = min(schema.get('maximum', math.inf), schema.get('exclusiveMaximum', math.inf))
    require(lo <= hi and not (lo == hi and (schema.get('exclusiveMinimum') == lo or schema.get('exclusiveMaximum') == hi)), 'Contradictory numeric bounds')
    if kind == 'integer':
        first = max(math.ceil(schema['minimum']) if 'minimum' in schema else -math.inf, math.floor(schema['exclusiveMinimum']) + 1 if 'exclusiveMinimum' in schema else -math.inf)
        last = min(math.floor(schema['maximum']) if 'maximum' in schema else math.inf, math.ceil(schema['exclusiveMaximum']) - 1 if 'exclusiveMaximum' in schema else math.inf)
        require(first <= last, 'Integer schema has no values')
    if 'enum' in schema:
        values = schema['enum']
        require(isinstance(values, list) and values and unique(values), 'Invalid scalar enum')
        for value in values:
            validate_scalar(value, {k: v for k, v in schema.items() if k != 'enum'})


def validate_document(ref):
    require(isinstance(ref, dict) and ref.get('kind') == 'stored' and isinstance(ref.get('stored'), dict), 'Expected stored document')
    key = ref['stored'].get('key')
    require(isinstance(key, dict) and text(key.get('jobId')) and text(key.get('name'))
            and all(type(key.get(k)) is int and 0 <= key[k] <= 9007199254740991 for k in ('taskOrdinal', 'sizeBytes'))
            and ('name' not in ref or isinstance(ref['name'], str)), 'Invalid document producer coordinates')


def validate_request(r):
    require(isinstance(r, dict) and text(r.get('review_id')) and text(r.get('title')) and isinstance(r.get('question'), str), 'Missing review identity, title or question')
    docs = r.get('documents')
    require(isinstance(docs, dict) and all(text(k) for k in docs), 'Invalid documents')
    for ref in docs.values():
        validate_document(ref)
    if 'overview_document_id' in r:
        require(r['overview_document_id'] in docs, 'Overview is not attached')
    metadata = r.get('document_metadata', {})
    require(isinstance(metadata, dict), 'Invalid metadata')
    for key, meta in metadata.items():
        require(key in docs and isinstance(meta, dict), 'Metadata names unattached document')
        for field, limit in (('title', 120), ('description', 300)):
            if field in meta:
                v = meta[field]
                require(isinstance(v, str) and len(v) <= limit and not any(ord(c) < 32 or ord(c) == 127 for c in v), 'Invalid metadata display text')
        if 'role' in meta:
            require(meta['role'] in ('', 'neutral', 'primary', 'supporting', 'diagnostic'), 'Invalid document role')
        if 'order' in meta:
            require(type(meta['order']) is int and 0 <= meta['order'] <= 1000000, 'Invalid document order')
        if 'source_document_ids' in meta:
            sources = meta['source_document_ids']
            require(isinstance(sources, list) and len(sources) <= 128 and unique(sources) and all(isinstance(v, str) and v in docs and v != key for v in sources), 'Invalid document sources')
    display = {k: r[k] for k in ('document_metadata', 'overview_document_id') if k in r}
    require(len(json.dumps(display, ensure_ascii=False, separators=(',', ':')).encode()) <= 65536, 'Document presentation too large')
    directions = r.get('directions')
    require(isinstance(directions, list) and directions, 'No review directions')
    ids = []
    require(isinstance(r.get('feedback'), dict) and text(r['feedback'].get('label')) and 'allow_attachments' not in r['feedback'], 'Invalid or frozen feedback policy')
    for d in directions:
        require(isinstance(d, dict) and text(d.get('id')) and text(d.get('label')) and type(d.get('continues_review')) is bool, 'Missing direction rules')
        require('feedback_required' not in d and d.get('feedback_mode') in ('forbidden', 'optional', 'required') and type(d.get('allow_attachments')) is bool, 'Mixed or incomplete direction rules')
        require(d['feedback_mode'] != 'forbidden' or not d['allow_attachments'], 'Forbidden feedback cannot allow attachments')
        ids.append(d['id'])
    require(unique(ids), 'Duplicate direction ID')
    settings = r.get('settings', [])
    require(isinstance(settings, list), 'Settings must be ordered array')
    setting_ids = []
    for s in settings:
        require(isinstance(s, dict) and all(text(s.get(k)) for k in ('id', 'label', 'effect')), 'Invalid setting declaration')
        setting_ids.append(s['id'])
        require(s.get('control') in ('text', 'choice', 'boolean', 'number'), 'Unsupported control')
        require('description' not in s or isinstance(s['description'], str), 'Invalid setting description')
        applies = s.get('applies_to')
        require(isinstance(applies, list) and applies and unique(applies) and all(v in ids for v in applies), 'Invalid applicability')
        validate_schema(s.get('schema'), s['control'])
        require('value' in s, 'Missing current value')
        validate_scalar(s['value'], s['schema'])
        require(('default' in s) == ('reset_label' in s), 'Reset needs default and label')
        if 'default' in s:
            require(text(s['reset_label']), 'Missing reset label')
            validate_scalar(s['default'], s['schema'])
        if s['control'] == 'choice':
            choices = s.get('choices')
            require(isinstance(choices, list) and choices, 'Missing choices')
            for c in choices:
                require(isinstance(c, dict) and text(c.get('label')) and 'value' in c, 'Invalid choice')
                validate_scalar(c['value'], s['schema'])
            values = [c['value'] for c in choices]
            require(unique(values), 'Duplicate choice value')
            for v in [s['value']] + ([s['default']] if 'default' in s else []):
                require(any(equal(v, c) for c in values) or (v is None and s.get('default', False) is None and 'reset_label' in s), 'Current/default not a choice')
        else:
            require('choices' not in s, 'Choices need choice control')
    require(unique(setting_ids), 'Duplicate setting ID')
    require(isinstance(r.get('conversation'), list), 'Missing conversation')
    for turn in r['conversation']:
        require(isinstance(turn, dict) and turn.get('role') in ('human', 'agent') and isinstance(turn.get('text'), str) and isinstance(turn.get('attachments'), list), 'Invalid conversation turn')
        for ref in turn['attachments']:
            validate_document(ref)
        if turn['role'] == 'human':
            require(text(turn.get('direction')) and isinstance(turn.get('receipt'), dict), 'Human needs direction and receipt')
        if 'settings' in turn:
            require(turn['role'] == 'human' and isinstance(turn['settings'], dict) and all(scalar(v) for v in turn['settings'].values()), 'Invalid historical settings')


def build_form(request):
    r = copy.deepcopy(request)
    if 'review_id' not in r:
        r['review_id'] = str(uuid.uuid4())
    validate_request(r)
    attachment = {'type': 'object', 'required': ['kind', 'stored'], 'properties': {
        'kind': {'const': 'stored'}, 'name': {'type': 'string'}, 'stored': {'type': 'object', 'required': ['key'], 'properties': {
            'key': {'type': 'object', 'required': ['jobId', 'taskOrdinal', 'name', 'sizeBytes'], 'properties': {
                'jobId': {'type': 'string', 'minLength': 1}, 'taskOrdinal': {'type': 'integer', 'minimum': 0},
                'name': {'type': 'string', 'minLength': 1}, 'sizeBytes': {'type': 'integer', 'minimum': 0}}}}}}}
    branches = []
    for d in r['directions']:
        settings = {}
        for s in r.get('settings', []):
            if d['id'] in s['applies_to']:
                schema = copy.deepcopy(s['schema'])
                if s['control'] == 'choice':
                    schema['enum'] = [c['value'] for c in s['choices']]
                    if s.get('default', False) is None and 'reset_label' in s and not any(v is None for v in schema['enum']):
                        schema['enum'].append(None)
                settings[s['id']] = schema
        props = {'direction': {'const': d['id']}, 'feedback': {'type': 'string'},
                 'attachments': {'type': 'array', 'items': attachment},
                 'settings': {'type': 'object', 'additionalProperties': False, 'properties': settings}}
        if not d['allow_attachments']:
            props['attachments']['maxItems'] = 0
        if d['feedback_mode'] == 'forbidden':
            props['feedback']['maxLength'] = 0
        branch = {'type': 'object', 'additionalProperties': False, 'required': list(props), 'properties': props}
        if d['feedback_mode'] == 'required':
            alternatives = [{'properties': {'feedback': {'pattern': NONBLANK}}}]
            if d['allow_attachments']:
                alternatives.append({'properties': {'attachments': {'minItems': 1}}})
            branch['anyOf'] = alternatives
        branches.append(branch)
    # The request is an immutable snapshot, including producer references. Native
    # validation checks that exact snapshot, not a weaker parallel declaration.
    request_schema = {'$schema': DRAFT, 'type': 'object', 'additionalProperties': False,
                      'required': list(r), 'properties': {k: {'const': v} for k, v in r.items()}}
    return {'title': r['title'], 'presentation': {'type': 'review/v2'}, 'request': r,
            'request_schema': request_schema, 'response_schema': {'$schema': DRAFT, 'oneOf': branches}}


if __name__ == '__main__':
    try:
        request = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.load(sys.stdin)
        request = request.get('request', request)
        print(json.dumps({'form': build_form(request)}, ensure_ascii=False, allow_nan=False))
    except (ValueError, KeyError, TypeError) as error:
        sys.exit('Invalid review/v2 declaration: ' + str(error))

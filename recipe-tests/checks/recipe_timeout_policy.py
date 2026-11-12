"""Reject common execution limits in shipped YAML; manual review covers semantics.

Scan whole YAML text so embedded Python and shell commands are included. This is
an intentionally conservative source guard, not a parser for arbitrary programs.
Test/CI harnesses and isolated runtime failure fixtures are outside its inputs.
"""
from pathlib import Path
import re
import sys

ROOTS = ('recipes', '.c2/recipes', 'docs/examples/recipes', 'examples/build-hooks')
PATTERNS = (
    r'''(?:^|[,{])\s*['"]?(?:[\w-]*timeout(?:[_-]?(?:seconds|ms|minutes))?|deadline(?:[_-]?seconds)?|max[_-](?:execution[_-])?time)['"]?\s*:''',
    r'\btimeout\s*=\s*[^,)\s]+',  # subprocess and other embedded call limits
    r'--(?:[\w-]*timeout(?:-seconds)?|max-time|deadline|kill-after)(?:[=\s]|$)',
    r'\b(?:timeout|gtimeout)\s+(?:-\S+\s+)*\d+(?:[.\d]*[smhd]?)\s',
    r'\b(?:signal\.)?(?:alarm|setitimer)\s*\(',
    r'(?:time\.(?:time|monotonic|perf_counter)\([^)]*\)|elapsed(?:_seconds)?)\s*[^\n]*[<>]',
)
RULES = tuple(re.compile(p, re.M | re.I) for p in PATTERNS)


def violations(text):
    return sorted({text.count('\n', 0, m.start()) + 1 for rule in RULES for m in rule.finditer(text)})


def scan(root):
    paths = [root / 'build.yaml', root / 'create.yaml']
    for directory in ROOTS:
        paths.extend(p for p in (root / directory).rglob('*') if p.suffix in ('.yaml', '.yml'))
    errors = [f'{p.relative_to(root)}:{line}' for p in sorted(set(paths)) if p.is_file()
              for line in violations(p.read_text())]
    if errors:
        raise ValueError('Recipe execution timeout found:\n' + '\n'.join(errors))
    return sum(p.is_file() for p in set(paths))


if __name__ == '__main__':
    print(f'Checked {scan(Path(sys.argv[1]).resolve())} workflow and example files')

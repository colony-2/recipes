import json
import sys
from pathlib import Path


def parse_notes(source):
    return [line for line in source.split('\n')[:-1] if line]


if __name__ == '__main__':
    print(json.dumps(parse_notes(Path(sys.argv[1]).read_text(encoding='utf-8'))))

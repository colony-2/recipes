import unittest
from import_notes import parse_notes


class ImportTests(unittest.TestCase):
    def test_newline_terminated_notes(self):
        self.assertEqual(parse_notes('First\nSecond\n'), ['First', 'Second'])

    def test_blank_lines_are_ignored(self):
        self.assertEqual(parse_notes('First\n\nSecond\n'), ['First', 'Second'])

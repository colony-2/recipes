import unittest
from drafts import Conflict, Drafts


class DraftTests(unittest.TestCase):
    def test_save_then_read(self):
        store = Drafts()
        store.write('one', 'Draft', 0)
        self.assertEqual(store.read('one'), {'text': 'Draft', 'version': 1})

    def test_conflicting_tab_cannot_overwrite(self):
        store = Drafts()
        store.write('one', 'First tab', 0)
        with self.assertRaises(Conflict):
            store.write('one', 'Second tab', 0)
        self.assertEqual(store.read('one')['text'], 'First tab')

import unittest

from pandas import DataFrame

from memworth.record import Record


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = Record("test/resources/dutch.txt")
        self.record.extract_phrases()

    def test_Record(self):
        from pandas import DataFrame
        self.assertIsInstance(self.record.collection_file, DataFrame)

    def test_extract_phrases(self):
        self.assertIsInstance(self.record.collection_file, DataFrame)
        self.assertIsInstance(self.record.phrases, DataFrame)
        self.assertIsInstance(self.record.words, DataFrame)
        self.assertEqual(len(self.record.phrases) + len(self.record.words),
                         len(self.record.collection_file))
        for i in self.record.phrases.index.tolist():
            self.assertTrue(i not in self.record.words.index.tolist())

    def test_add_woorden_info(self):
        self.record.words = self.record.words  # .iloc[:3]
        self.record.add_woorden_info()
        self.record.write_definitions()
        self.assertIsInstance(self.record.words, DataFrame)

    def test_add_wiktionary_info(self):
        self.record.words = self.record.words.iloc[:3]
        self.record.add_wiktionary_info()
        self.record.write_definitions()
        self.assertIsInstance(self.record.words, DataFrame)

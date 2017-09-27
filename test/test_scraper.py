import unittest

import memworth.scraper as scraper


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.zweverig = scraper.Word('zweverig')

    def test_wiktionary(self):
        # Example sentences are italicized list items
        self.zweverig.wiktionary()
        expected_html = "<b>zweverige</b> theorieën.</i> </li><br>"
        self.assertIn(expected_html, self.zweverig.wiktionary_html)
        self.assertIn("onduidelijk",
                      self.zweverig.wiktionary_results.get_text())

    def test_woorden(self):
        self.zweverig.woorden()
        print(self.zweverig.woorden_definitions)
        print(self.zweverig.woorden_examples)
        print(self.zweverig.woorden_related)


if __name__ == '__main__':
    unittest.main()

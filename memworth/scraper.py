import requests
from bs4 import BeautifulSoup


class Word:
    def __init__(self, word):
        self.word = word

    def make_soup(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        return soup

    def raw_html(self, results):
        html = bytes(str(results), 'utf8').decode()
        html = html.replace(u'\xa0', u' ')
        html = html.replace(u'\n', u'<br>')
        return html

    def wiktionary(self):
        url = "https://nl.wiktionary.org/wiki/" + self.word
        soup = self.make_soup(url)
        self.wiktionary_results = soup.ol
        self.wiktionary_html = self.raw_html(self.wiktionary_results)

    def woorden(self):
        url = "http://www.woorden.org/woord/" + self.word
        self.woorden_soup = self.make_soup(url)
        definitions = []
        for tag in self.woorden_soup.find_all('font'):
            if tag.find('b'):
                definitions.append(tag.text)
        if len(definitions) == 1:
            self.woorden_definitions = definitions
        else:
            self.woorden_definitions = []
            for i in zip(definitions[0::2], definitions[1::2]):
                self.woorden_definitions.append(i)
        self.woorden_examples = []
        for tag in self.woorden_soup.find_all('font'):
            if not tag.find('b'):
                self.woorden_examples.append(tag.text)
        # Decode
        self.woorden_examples = [bytes(i, 'latin1').decode()
                                 for i in self.woorden_examples]
        # Clean up
        self.woorden_examples = [i.replace('`', '') for
                                 i in self.woorden_examples]
        # Related words
        related_words = []
        for tag in self.woorden_soup.find_all('a'):
            if tag.find_all('u') and \
               tag.text != 'Toon uitgebreidere definities':
                related_words.append(tag.text)
        self.woorden_related = related_words

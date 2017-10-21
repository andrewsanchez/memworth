import re

import requests
from bs4 import BeautifulSoup


class Word:
    def __init__(self, word, local=None):
        self.word = word
        self.infinitive = word
        self.url = "http://www.woorden.org/woord/{}".format(word)
        if local:
            self.url = local
        self.make_soup(self.url)
        self.session = requests.Session()
        self.examples = []
        self.related_words = []
        self.definitions = []

    def get_response(self):
        self.response = self.session.get(self.url)

    def make_soup(self):
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def raw_html(self, results):
        html = bytes(str(results), 'utf8').decode()
        html = html.replace(u'\xa0', u' ')
        html = html.replace(u'\n', u'<br>')
        self.html = html

    def base_word(self):
        m = self.soup.find_all('h2')
        m = (t for t in m if t.get('class'))
        m = [t for t in m if t['class'][0] == 'inline']
        try:
            self.infinitive = m[0].get_text()
        except IndexError:
            pass

    def define(self):
        m = self.soup.find_all('font')
        m = (tag for tag in m if tag.find('b'))
        m = (tag.text for tag in m)
        m = [tag for tag in m if not re.match('^\d', tag)]
        # self.definitions = ['{}) {}.'.format(i, v)
        #                     for i, v in enumerate(m, 1)]
        for i, v in enumerate(m, 1):
            definition = decode_and_clean(v)
            definition = '{}) {}.'.format(i, definition)
            self.definitions.append(definition)
        if not m:
            self.definitions = ['']

    def get_examples(self):
        m = self.soup.find_all('font')
        m = (tag for tag in m if not tag.find('b'))
        m = [t for t in m if t.get('style').startswith('color')]
        m = [t for t in m if not re.match('^[ ()]', t.text)]
        for i, tag in enumerate(m, 1):
            txt = tag.text
            cleaned = decode_and_clean(txt)
            example = '{}) {}'.format(i, cleaned)
            if not example.endswith('.'):
                example += '.'
            self.examples.append(example)
        if not self.examples:
            self.examples = ['']

    def get_related(self):
        m = self.soup.find_all('a')
        m = (tag.text for tag in m if tag.find_all('u'))
        unwanted = 'Toon uitgebreidere definities'
        m = (i for i in m if i != unwanted)
        m = filter(lambda x: x != unwanted, m)
        for i, txt in enumerate(m, 1):
            w = decode_and_clean(txt)
            related = "{}) {}.".format(i, w)
            self.related_words.append(related)
        if not self.related_words:
            self.related_words = ['']

    def get_word_data(self):
        self.make_soup()
        self.base_word()
        self.define()
        if self.definitions:
            self.get_examples()
            self.get_related()

    def summary(self):
        print(self.infinitive)
        print("Definities:")
        for i in self.definitions:
            print(i)
        print("Voorbeelden:")
        for i in self.examples:
            print(i)
        print("Related words:")
        for i in self.related_words:
            print(i)


def decode_and_clean(txt):
    decoded = bytes(txt, 'latin1').decode()
    return decoded.replace('`', '')

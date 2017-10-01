import re

import requests
from bs4 import BeautifulSoup


class Word:
    def __init__(self, word):
        self.word = word
        self.urls = {
            "woorden": "http://www.woorden.org/woord/{}".format(word),
        }
        self.make_soup(self.urls["woorden"])

    def make_soup(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "lxml")

    def raw_html(self, results):
        html = bytes(str(results), 'utf8').decode()
        html = html.replace(u'\xa0', u' ')
        html = html.replace(u'\n', u'<br>')
        self.html = html

    def define(self):
        m = self.soup.find_all('font')
        m = (tag for tag in m if tag.find('b'))
        m = (tag.text for tag in m)
        m = [tag for tag in m if not re.match('^\d', tag)]
        # Functional equivalents
        # m = filter(lambda tag: tag.find('b'), m)
        # m = map(lambda x: x.text, m)
        # m = filter(lambda x: not re.match('^\d', x), m)
        self.definitions = m
        if not m:
            self.definitions = ['']

    def exemplify(self):
        self.woorden_examples = []
        for tag in self.soup.find_all('font'):
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
        for tag in self.soup.find_all('a'):
            if tag.find_all('u') and \
               tag.text != 'Toon uitgebreidere definities':
                related_words.append(tag.text)
        self.woorden_related = related_words

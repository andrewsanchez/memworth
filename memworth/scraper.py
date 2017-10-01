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
        self.examples = []
        self.related_words = []

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
        m = self.soup.find_all('font')
        m = (tag for tag in m if not tag.find('b'))
        for tag in m:
            txt = tag.text
            decoded = bytes(txt, 'latin1').decode()
            cleaned = decoded.replace('`', '')
            self.examples.append(cleaned)
        if not self.examples:
            self.examples = ['']

    def related(self):
        m = self.soup.find_all('a')
        m = (tag.text for tag in m if tag.find_all('u'))
        unwanted = 'Toon uitgebreidere definities'
        m = (i for i in m if i != unwanted)
        m = filter(lambda x: x != unwanted, m)
        self.related_words = list(m)
        if not self.related_words:
            self.related_words = ['']

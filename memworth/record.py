import os

import pandas as pd

from memworth.media import media
from memworth.scraper import Word


class Record:
    def __init__(self, path):
        self.path = path
        self.collection_file = pd.read_csv(path, index_col=0, header=None)
        self.collection_file.columns = ["tags"]
        self.collection_file = self.collection_file[
            ~self.collection_file.index.duplicated(keep='first')]
        self.phrases = pd.DataFrame()
        self.cards = pd.DataFrame()
        self.unresolved = []

    def extract_phrases(self):
        phrases = []
        phrases = (i for i in self.collection_file.index
                   if len(i.split(' ')) > 1)
        self.phrases = pd.DataFrame(index=phrases)
        self.words = self.collection_file.drop(self.phrases.index)

    def populate(self):
        for word in self.words.index:
            w = Word(word)
            w.get_response()
            w.get_word_data()
            if w.definitions:
                w.definitions.insert(0, media['definities'])
                w.examples.insert(0, media['voorbeelden'])
                w.related_words.insert(0, media['gerelateerde'])
                definitions = '<br>'.join(w.definitions)
                examples = '<br>'.join(w.examples)
                related = '<br>'.join(w.related_words)
                self.cards.loc[w.infinitive, 'Definitions'] = definitions
                self.cards.loc[w.infinitive, 'Examples'] = examples
                self.cards.loc[w.infinitive, 'Related'] = related
            else:
                self.unresolved.append(w.word)

    def write(self):
        import time
        out_words = os.path.join("~/Google Drive/memworth", "words.txt")
        out_anki = "anki_{}.txt".format(time.strftime('%d-%m-%Y'))
        out_anki = os.path.join("~/Google Drive/memworth", out_anki)
        self.words.to_csv(out_words, mode="a")
        self.cards.to_csv(out_anki, header=False)

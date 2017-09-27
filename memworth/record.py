import pandas as pd
import os
import memworth.scraper as scraper


class Record:
    def __init__(self, path):
        self.path = path
        self.collection_file = pd.read_csv(path, index_col=0, header=None)
        self.collection_file.columns = ["tags"]
        self.phrases = pd.DataFrame()
        self.anki_file = pd.DataFrame()

    def extract_phrases(self):
        phrases = []
        for row in self.collection_file.index:
            if len(row.split(' ')) != 1:
                phrases.append(row)
        self.phrases = pd.DataFrame(index=phrases)
        self.words = self.collection_file.drop(self.phrases.index)

    def add_woorden_info(self):
        for word in self.words.index:
            query = scraper.Word(word)
            query.woorden()
            definitions = query.woorden_definitions
            examples = query.woorden_examples
            related = query.woorden_related
            print(word)
            print(definitions)
            print(examples)
            print(related)
            try:
                self.words.loc[word, 'Definitions'] = '<br>'.join(definitions)
                self.words.loc[word, 'Examples'] = '<br>'.join(examples)
                self.words.loc[word, 'Related'] = '<br>'.join(related)
                self.anki_file.loc[word, 'Definitions'] = '<br>'.join(definitions)
                self.anki_file.loc[word, 'Examples'] = '<br>'.join(examples)
                self.anki_file.loc[word, 'Related'] = '<br>'.join(related)
            except IndexError:
                continue

    def add_wiktionary_info(self):
        for word in self.words.index:
            query = scraper.Word(word)
            query.wiktionary()
            print(query.wiktionary_html)
            self.words.loc[word, 'Wiktionary'] = query.wiktionary_html

    def write_definitions(self):
        out = os.path.join("~/scratch", "definitions.txt")
        out_anki = os.path.join("~/scratch", "anki.txt")
        self.words.to_csv(out)
        self.anki_file.to_csv(out_anki, header=False)

    def create_cards(self):
        pass

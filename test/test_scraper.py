import pytest


def test_define(words):
    print(words.definitions)
    assert words.definitions


def test_exemplify(words):
    print(words.examples)
    assert words.examples

def test_related(words):
    print(words.related_words)
    assert words.related_words
    



def test_woorden(self):
    self.zweverig.woorden()
    print(self.zweverig.woorden_definitions)
    print(self.zweverig.woorden_examples)
    print(self.zweverig.woorden_related)

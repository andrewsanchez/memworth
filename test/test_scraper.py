from requests import Response
from pprint import pprint

def test_base_word(conjugated):
    infinitive, w = conjugated
    assert isinstance(w.response, Response)
    assert infinitive == w.infinitive


def test_define(words):
    pprint(words.definitions)
    assert isinstance(words.definitions, list)


def test_get_examples(words):
    pprint(words.examples)
    assert isinstance(words.examples, list)


def test_get_related(words):
    pprint(words.related_words)
    assert isinstance(words.related_words, list)


def test_summary(conjugated):
    infinitive, w = conjugated
    w.summary()

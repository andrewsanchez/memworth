import pytest

from memworth.record import Record
from memworth.scraper import Word


@pytest.fixture(scope="module",
                params=[("gezellig", "resources/gezellig.html"),
                        ("nonword", None)])
def words(request):
    word = Word(request.param[0], request.param[1])
    word.get_word_data()
    yield word


@pytest.fixture(scope="module",
                params=[("verhief", "verheffen"),
                        ("overeenkomt", "overeenkomen")])
def conjugated(request):
    conjugated = request.param[0]
    infinitive = request.param[1]
    w = Word(conjugated)
    w.get_word_data()
    yield infinitive, w


@pytest.fixture(scope="module")
def record(request):
    record = Record('test/resources/dutch.txt')
    record.extract_phrases()
    yield record

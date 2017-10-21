import pytest
import betamax

from memworth.record import Record
from memworth.scraper import Word

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'test/cassettes'


@pytest.fixture(scope="module",
                params=["gezellig", "nonword", "verhief", "overeenkomt"])
def words(request):
    word = request.param
    w = Word(word)
    recorder = betamax.Betamax(w.session)
    with recorder.use_cassette(word):
        w.get_response()
    w.get_word_data()
    yield w


@pytest.fixture(scope="module",
                params=[("verhief", "verheffen"),
                        ("overeenkomt", "overeenkomen")])
def conjugated(request):
    conjugated = request.param[0]
    infinitive = request.param[1]
    w = Word(conjugated)
    recorder = betamax.Betamax(w.session)
    with recorder.use_cassette(conjugated):
        w.get_response()
    w.get_word_data()
    yield infinitive, w


@pytest.fixture(scope="module")
def record(request):
    record = Record('test/resources/dutch.txt')
    record.extract_phrases()
    yield record

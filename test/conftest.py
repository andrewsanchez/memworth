import pytest

from memworth.scraper import Word


@pytest.fixture(scope="module",
                params=["gezellig", "nonword"])
def words(request):
    word = Word(request.param)
    word.define()
    word.exemplify()
    word.related()
    yield word

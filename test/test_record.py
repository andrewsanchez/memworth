from pandas import DataFrame


def test_init(record):
    assert isinstance(record.collection_file, DataFrame)


def test_extract_phrases(record):
    assert isinstance(record.phrases, DataFrame)
    assert isinstance(record.words, DataFrame)
    total = len(record.phrases) + len(record.words)
    assert total == len(record.collection_file)
    phrases = record.phrases.index.tolist()
    words = record.words.index.tolist()
    assert len(list(filter(
        lambda x: x in phrases, words))) == 0


def test_populate(record):
    record.populate()
    record.write()
    print(record.words)
    print(record.cards)

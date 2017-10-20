def test_base_word(conjugated):
    infinitive, w = conjugated
    assert infinitive == w.infinitive


def test_define(words):
    print()
    for d in words.definitions:
        print(d)
    assert words.definitions


def test_get_examples(words):
    print()
    for e in words.examples:
        print(e)
    assert words.examples


def test_get_related(words):
    print(words.related_words)
    assert words.related_words


def test_summary(conjugated):
    infinitive, w = conjugated
    w.summary()

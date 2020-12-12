import unittest
from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage
from lab_4.main import encode_text
from lab_4.main import NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie


if __name__ == '__main__':
    text = 'I have a cat.\nHis name is Bruno'
    corpus = tokenize_by_sentence(text)

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(2, encoded)

    generator = NGramTextGenerator(storage, trie)

    context = (storage.get_id('bruno'),)
    end = storage.get_id('<END>')
    actual = generator.generate_text(context, 3)

    RESULT = (9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == actual, ''

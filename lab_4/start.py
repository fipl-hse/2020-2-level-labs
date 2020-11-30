"""
Lab 4 implementation starter
"""

from lab_4.main import NGramTextGenerator, encode_text, WordStorage
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'cat', '<END>',
              'his', 'name', 'is', 'bruno', '<END>',
              'i', 'have', 'a', 'dog', 'too', '<END>',
              'his', 'name', 'is', 'rex', '<END>',
              'her', 'name', 'is', 'rex', 'too', '<END>')

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(2, encoded)

    generator = NGramTextGenerator(storage, trie)

    context = (storage.get_id('bruno'),)
    end = storage.get_id('<END>')
    actual = generator.generate_text(context, 3)

    RESULT = actual.count(end) == 3
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Encoding not working'

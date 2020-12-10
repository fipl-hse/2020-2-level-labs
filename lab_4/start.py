"""
Lab 4 implementation starter
"""

from lab_4.main import LikelihoodBasedTextGenerator, encode_text, WordStorage
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

    trie = NGramTrie(3, encoded)
    word = storage.get_id('dog')
    context = (storage.get_id('have'),
               storage.get_id('a'),)

    generator = LikelihoodBasedTextGenerator(storage, trie)

    EXPECTED = 1 / 2
    RESULT = generator._calculate_maximum_likelihood(word, context)
    assert RESULT == EXPECTED, 'Encoding not working'

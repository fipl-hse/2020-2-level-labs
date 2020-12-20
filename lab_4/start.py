"""
Lab 4 implementation start file
"""

from lab_4.main import LikelihoodBasedTextGenerator, encode_text, WordStorage, decode_text
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

    end = storage.get_id('<END>')
    context = (storage.get_id('name'),
               storage.get_id('is'),)

    generator = LikelihoodBasedTextGenerator(storage, trie)

    to_decode = generator.generate_text(context, 2)

    EXPECTED = ('Name is rex', 'Her name is rex')
    RESULT = decode_text(storage, to_decode)
    assert RESULT == EXPECTED, "the thing that won't be printed anyway"

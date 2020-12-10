"""
Lab 4
"""

from main import *

from ngrams.ngram_trie import NGramTrie


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
    context = (storage.get_id('i'),)

    first_generated = storage.get_id('have')
    last_generated = storage.get_id('<END>')

    generator = NGramTextGenerator(storage, trie)
    actual = generator._generate_sentence(context)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert actual[1] == first_generated, ''

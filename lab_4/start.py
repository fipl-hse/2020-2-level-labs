"""
Lab 4 implementation starter
"""

from lab_4.main import encode_text, WordStorage
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'dog', '<END>',
              'his', 'name', 'is', 'william', '<END>',
              'i', 'have', 'a', 'cat', 'too', '<END>',
              'his', 'name', 'is', 'mike', '<END>')

    storage = WordStorage()
    storage.update(corpus)
    encode = encode_text(storage, corpus)

    trie = NGramTrie(3, encode)
    context = (storage.get_id('name'),
               storage.get_id('is'),)

    RESULT = context
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Encoding not working'

"""
Text generator
"""

from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import WordStorage, BackOffGenerator
from lab_4.main import encode_text, decode_text


if __name__ == '__main__':

    corpus = ('there', 'are', 'a', 'lot', 'of', 'flowers', '<END>',
              'there', 'are', 'some', 'dogs', 'outside', '<END>',
              'this', 'is', 'my', 'dog', '<END>',
              'there', 'is', 'a', 'cat', '<END>',
              'there', 'is', 'a', 'cat', 'outside', '<END>',
              'here', 'is', 'a', 'cat', 'outside', '<END>')

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(3, encoded)
    four = NGramTrie(4, encoded)

    context = (storage.get_id('there'),
               storage.get_id('are'),
               storage.get_id('cat'),
               storage.get_id('outside'),)

    generator = BackOffGenerator(storage, trie, four)

    text = generator.generate_text(context, 3)
    actual = decode_text(storage, text)

    RESULT = ('There are a lot of flowers', 'Flowers there', 'There')

    assert RESULT == actual, "Something doesn't work"

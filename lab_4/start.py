"""
Text generation implementation starter
"""

from lab_4.main import WordStorage, encode_text, LikelihoodBasedTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'parrot', '<END>',
              'his', 'name', 'is', 'john', '<END>',
              'i', 'have', 'a', 'chinchilla', 'too', '<END>',
              'his', 'name', 'is', 'taylor', '<END>',
              'her', 'name', 'is', 'taylor', 'too', '<END>')

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(3, encoded)

    expected_word = storage.get_id('taylor')
    context = (storage.get_id('name'),
               storage.get_id('is'),)

    generator = LikelihoodBasedTextGenerator(storage, trie)

    RESULT = generator._generate_next_word(context)

    assert RESULT == expected_word, 'Text generator does not work'

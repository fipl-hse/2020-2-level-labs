"""
Text generation implementation starter
"""

from lab_4.main import WordStorage, encode_text, LikelihoodBasedTextGenerator, decode_text, BackOffGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'colourful', 'dog', '<END>',
              'i', 'have', 'colourful', 'pets', 'too', '<END>',
              'they', 'have', 'beautiful', 'dogs', '<END>',
              'i', 'havent', 'a', 'cat', '<END>',
              'i', 'havent', 'a', 'cat', 'too', '<END>',
              'we', 'havent', 'a', 'cat', 'too', '<END>')

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(4, encoded)

    context = (storage.get_id('i'),
               storage.get_id('have'),
               storage.get_id('a'))

    generator_likelihood = LikelihoodBasedTextGenerator(storage, trie)

    generated_text = generator_likelihood.generate_text(context, 3)
    decoded_gen_text = decode_text(storage, generated_text)
    print('Likelihood generator generates sentences:')
    print(*decoded_gen_text, sep='. ', end='.\n')

    two = NGramTrie(2, encoded)
    trie = NGramTrie(3, encoded)

    context = (storage.get_id('i'),
               storage.get_id('have'),)

    generator_backoff = BackOffGenerator(storage, trie, two)

    actual = generator_backoff.generate_text(context, 3)
    RESULT = decode_text(storage, actual)
    print('Backoff generator generates sentences:')
    print(*RESULT, sep='. ', end='.\n')

    assert RESULT == ('I have a colourful dog',
                      'I havent a cat too',
                      'They have beautiful dogs'), 'Text generator does not work'

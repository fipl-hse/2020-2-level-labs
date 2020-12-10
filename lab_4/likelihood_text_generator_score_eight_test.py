# pylint: skip-file
"""
Tests for LikelihoodBasedTextGenerator class
"""

import unittest
from lab_4.main import WordStorage, encode_text, LikelihoodBasedTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie


class LikelihoodBasedTextGeneratorTest(unittest.TestCase):
    """
    checks for LikelihoodBasedTextGenerator class.
        All tests should pass for score 8 or above
    """

    def test_likelihood_generator_instance_creation(self):
        """
        Checks that class creates correct instance
        """
        word_storage = WordStorage()
        ngram = NGramTrie(2, ())

        generator = LikelihoodBasedTextGenerator(word_storage, ngram)
        self.assertEqual(generator._word_storage, word_storage)
        self.assertEqual(generator._n_gram_trie, ngram)

# ---------------------------------------------------------------------

    def test_calculate_likelihood_ideal(self):
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

        expected = 1/2
        actual = generator._calculate_maximum_likelihood(word, context)
        self.assertEqual(expected, actual)

    def test_calculate_likelihood_incorrect_word(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)
        encoded = encode_text(storage, corpus)
        trie = NGramTrie(2, encoded)

        bad_inputs = [(), [], None, 123]
        context = (storage.get_id('have'),
                   storage.get_id('a'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        for bad_word in bad_inputs:
            self.assertRaises(ValueError,
                              generator._calculate_maximum_likelihood,
                              bad_word, context)

    def test_calculate_likelihood_bad_word(self):     # new test
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)
        encoded = encode_text(storage, corpus)
        trie = NGramTrie(2, encoded)

        bad_inputs = [-9, 1.6]
        context = (storage.get_id('have'),
                   storage.get_id('a'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        for bad_word in bad_inputs:
            self.assertRaises(ValueError,
                              generator._calculate_maximum_likelihood,
                              bad_word, context)

    def test_calculate_likelihood_incorrect_context(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)
        encoded = encode_text(storage, corpus)
        trie = NGramTrie(2, encoded)

        bad_inputs = [[], {}, (2000, 1000, ), None, 9, 9.34, True]
        word = storage.get_id('dog')

        generator = LikelihoodBasedTextGenerator(storage, trie)

        for bad_context in bad_inputs:
            self.assertRaises(ValueError,
                              generator._calculate_maximum_likelihood,
                              word, bad_context)

    def test_calculate_likelihood_no_such_context(self):
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
        context = (storage.get_id('<END>'),
                   storage.get_id('<END>'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        expected = 0.0
        actual = generator._calculate_maximum_likelihood(word, context)
        self.assertEqual(expected, actual)

# -----------------------------------------------------------------------

    def test_generate_next_word_ideal(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)

        expected_word = storage.get_id('rex')
        context = (storage.get_id('name'),
                   storage.get_id('is'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        actual = generator._generate_next_word(context)
        self.assertEqual(expected_word, actual)

    def test_generate_next_word_incorrect_context(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)

        bad_inputs = [[], {}, (2000, 1000, ), None, 9, 9.34, True]

        generator = LikelihoodBasedTextGenerator(storage, trie)

        for bad_context in bad_inputs:
            self.assertRaises(ValueError, generator._generate_next_word, bad_context)

    def test_generate_next_word_same_prob(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)

        expected_word = storage.get_id('cat')
        context = (storage.get_id('have'),
                   storage.get_id('a'),)

        generator = LikelihoodBasedTextGenerator(storage, trie)

        actual = generator._generate_next_word(context)
        self.assertEqual(expected_word, actual)

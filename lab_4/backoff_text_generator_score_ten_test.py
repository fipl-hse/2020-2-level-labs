# pylint: skip-file
"""
Tests for BackOffGenerator class
"""

import unittest
from lab_4.main import WordStorage, encode_text, BackOffGenerator
from lab_4.ngrams.ngram_trie import NGramTrie


class BackOffGeneratorTest(unittest.TestCase):
    """
    checks for BackOffGenerator class.
        All tests should pass for score 10 or above
    """

    def test_backoff_generator_instance_creation(self):
        """
        Checks that class creates correct instance
        """
        word_storage = WordStorage()
        ngram = NGramTrie(2, ())

        generator = BackOffGenerator(word_storage, ngram)
        self.assertEqual(generator._word_storage, word_storage)
        self.assertTrue(ngram in generator._n_gram_tries)

    def test_backoff_generator_instance_creation_complex(self):
        """
        Checks that class creates correct instance with several tries
        """
        word_storage = WordStorage()
        ngram = NGramTrie(2, ())
        three = NGramTrie(3, ())
        four = NGramTrie(4, ())

        generator = BackOffGenerator(word_storage, ngram, three, four)
        self.assertEqual(generator._word_storage, word_storage)
        self.assertTrue(ngram in generator._n_gram_tries)
        self.assertTrue(three in generator._n_gram_tries)
        self.assertTrue(four in generator._n_gram_tries)

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

        two = NGramTrie(2, encoded)
        trie = NGramTrie(3, encoded)

        expected_word = storage.get_id('rex')
        context = (storage.get_id('name'),
                   storage.get_id('is'),)

        generator = BackOffGenerator(storage, trie, two)

        actual = generator._generate_next_word(context)
        self.assertEqual(expected_word, actual)

    def test_generate_next_word_swap(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        two = NGramTrie(2, encoded)
        trie = NGramTrie(3, encoded)
        four = NGramTrie(4, encoded)

        expected_word = storage.get_id('name')
        context = (storage.get_id('his'),)

        generator = BackOffGenerator(storage, two, trie, four)

        actual = generator._generate_next_word(context)
        self.assertEqual(expected_word, actual)

    def test_generate_next_word_after_end(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        two = NGramTrie(2, encoded)
        trie = NGramTrie(3, encoded)
        four = NGramTrie(4, encoded)

        expected_word = storage.get_id('his')
        context = (storage.get_id('<END>'),)

        generator = BackOffGenerator(storage, two, trie, four)

        actual = generator._generate_next_word(context)
        self.assertEqual(expected_word, actual)

    def test_generate_next_word_end(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        five = NGramTrie(5, encoded)
        trie = NGramTrie(3, encoded)
        four = NGramTrie(4, encoded)

        expected_word = storage.get_id('<END>')
        context = (storage.get_id('his'),
                   storage.get_id('name'),
                   storage.get_id('is'),
                   storage.get_id('bruno'),)

        generator = BackOffGenerator(storage, five, trie, four)

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
        two = NGramTrie(2, encoded)
        four = NGramTrie(4, encoded)

        bad_inputs = [[], {}, (2000, 1000, ), None, 9, 9.34, True]

        generator = BackOffGenerator(storage, trie, two, four)

        for bad_context in bad_inputs:
            self.assertRaises(ValueError, generator._generate_next_word, bad_context)

    def test_generate_next_word_complex(self):
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>',
                  'i', 'have', 'a', 'dog', 'too', '<END>',
                  'his', 'name', 'is', 'rex', '<END>',
                  'her', 'name', 'is', 'rex', 'too', '<END>')

        storage = WordStorage()
        storage.update(corpus)

        encoded = encode_text(storage, corpus)

        trie = NGramTrie(3, encoded)
        two = NGramTrie(2, encoded)
        four = NGramTrie(4, encoded)

        expected_word = storage.get_id('rex')
        context = (storage.get_id('name'),
                   storage.get_id('is'),)

        generator = BackOffGenerator(storage, trie, two, four)

        actual = generator._generate_next_word(context)
        self.assertEqual(expected_word, actual)

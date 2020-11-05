# pylint: skip-file
"""
Tests for NGramTrie class
"""

import math
import unittest
from lab_3.main import NGramTrie


class BiGramTest(unittest.TestCase):
    """
    check NGramTrie class functionality on BiGrams.
        All tests should pass for 6 score or above
    """
    @unittest.skip('')
    def test_ngram_trie_check_creation(self):
        ngram = NGramTrie(2)
        self.assertEqual(ngram.size, 2)
        self.assertEqual(ngram.n_grams, ())
        self.assertEqual(ngram.n_gram_frequencies, {})
        self.assertEqual(ngram.n_gram_log_probabilities, {})

# -----------------------------------------------------------
    @unittest.skip('')
    def test_fill_n_grams_ideal(self):
        ngram = NGramTrie(2)
        text = (((1, 2, 3, 4, 5), (2, 3, 4, 5)),)
        expected = (
            (
                ((1, 2), (2, 3), (3, 4), (4, 5)),
                ((2, 3), (3, 4), (4, 5))
            ),
        )
        actual = ngram.fill_n_grams(text)
        self.assertEqual(0, actual)
        self.assertEqual(ngram.n_grams, expected)
    @unittest.skip('')
    def test_fill_n_grams_duplcicates_ideal(self):
        ngram = NGramTrie(2)
        sentences = (((1, 2, 1, 2, 1, 2), (10, 11, 12)),)
        expected = (
            (
                ((1, 2), (2, 1), (1, 2), (2, 1), (1, 2)),
                ((10, 11), (11, 12))
            ),
        )
        actual = ngram.fill_n_grams(sentences)
        self.assertEqual(0, actual)
        self.assertEqual(ngram.n_grams, expected)
    @unittest.skip('')
    def test_fill_n_grams_empty(self):
        ngram = NGramTrie(2)
        sentences = ()
        expected = ()
        actual = ngram.fill_n_grams(sentences)
        self.assertEqual(0, actual)
        self.assertEqual(ngram.n_grams, expected)
    @unittest.skip('')
    def test_fill_n_grams_none(self):
        ngram = NGramTrie(2)
        sentences = None
        expected = ()
        actual = ngram.fill_n_grams(sentences)
        self.assertEqual(1, actual)
        self.assertEqual(ngram.n_grams, expected)
    @unittest.skip('')
    def test_fill_n_grams_not_tuple(self):
        ngram = NGramTrie(2)
        sentences = [(1, 2, 3, 4, 5)]
        expected = ()
        actual = ngram.fill_n_grams(sentences)
        self.assertEqual(1, actual)
        self.assertEqual(ngram.n_grams, expected)

# -------------------------------------------------------------
    @unittest.skip('')
    def test_calculate_n_grams_frequencies_ideal(self):
        ngram = NGramTrie(2)
        sentences = (((1, 2, 3, 4, 5),),)
        ngram.fill_n_grams(sentences)

        expected = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 5): 1}
        actual = ngram.calculate_n_grams_frequencies()
        self.assertEqual(expected, ngram.n_gram_frequencies)
        self.assertEqual(0, actual)
    @unittest.skip('')
    def test_calculate_n_grams_frequencies_duplcicates_ideal(self):
        ngram = NGramTrie(2)
        sentences = (((1, 2, 1, 2, 1, 2), (1, 2)),)
        ngram.fill_n_grams(sentences)

        expected = {(1, 2): 4, (2, 1): 2}
        actual = ngram.calculate_n_grams_frequencies()
        self.assertEqual(expected, ngram.n_gram_frequencies)
        self.assertEqual(0, actual)
    @unittest.skip('')
    def test_calculate_n_grams_frequencies_empty(self):
        ngram = NGramTrie(2)
        sentences = ()
        ngram.fill_n_grams(sentences)

        expected = {}
        actual = ngram.calculate_n_grams_frequencies()
        self.assertEqual(expected, ngram.n_gram_frequencies)
        self.assertEqual(1, actual)
    @unittest.skip('')
    def test_get_ngrams_frequencies_from_sentence_none(self):
        ngram = NGramTrie(2)
        sentences = None
        ngram.fill_n_grams(sentences)

        expected = {}
        actual = ngram.calculate_n_grams_frequencies()
        self.assertEqual(expected, ngram.n_gram_frequencies)
        self.assertEqual(1, actual)
    @unittest.skip('')
    def test_get_ngrams_frequencies_from_sentence_not_tuple(self):
        ngram = NGramTrie(2)
        sentences = [(1, 2, 3, 4, 5)]
        ngram.fill_n_grams(sentences)

        expected = {}
        actual = ngram.calculate_n_grams_frequencies()
        self.assertEqual(expected, ngram.n_gram_frequencies)
        self.assertEqual(1, actual)

# ----------------------------------------------------------
    @unittest.skip('')
    def test_top_n_grams_ideal(self):
        ngram = NGramTrie(2)
        top_n = 2
        ngram.n_gram_frequencies = {(1, 2): 100,
                                    (2, 3): 123,
                                    (3, 4): 12345}
        expected = ((3, 4), (2, 3))
        actual = ngram.top_n_grams(top_n)
        self.assertEqual(expected, actual)
    @unittest.skip('')
    def test_top_n_grams_more(self):
        ngram = NGramTrie(2)
        top_n = 2000000
        ngram.n_gram_frequencies = {(1, 2): 100,
                                    (2, 3): 123,
                                    (3, 4): 12345}
        expected = ((3, 4), (2, 3), (1, 2))
        actual = ngram.top_n_grams(top_n)
        self.assertEqual(expected, actual)
    @unittest.skip('')
    def test_top_n_grams_inappropriate(self):
        ngram = NGramTrie(2)
        bad_inputs = [[], (), {}, None, True, '', -1, 0, 9.22]
        expected = ()
        for bad_input in bad_inputs:
            actual = ngram.top_n_grams(bad_input)
            self.assertEqual(expected, actual)

# -----------------------------------------------------------
    @unittest.skip('')
    def test_calculate_log_probabilities_ideal(self):
        ngram = NGramTrie(2)
        ngram.n_gram_frequencies = {(1, 2): 10, (1, 3): 2, (2, 5): 5}
        first_prob = math.log(10 / 12)
        second_prob = math.log(2 / 12)

        actual = ngram.calculate_log_probabilities()
        self.assertEqual(ngram.n_gram_log_probabilities[(1, 2)], first_prob)
        self.assertEqual(ngram.n_gram_log_probabilities[(1, 3)], second_prob)
        self.assertEqual(0, actual)
    @unittest.skip('')
    def test_calculate_log_probabilities_one_bi_gram(self):
        ngram = NGramTrie(2)
        ngram.n_gram_frequencies = {(1, 2): 10}

        actual = ngram.calculate_log_probabilities()
        self.assertEqual(ngram.n_gram_log_probabilities[(1, 2)], 0.0)
        self.assertEqual(0, actual)
    @unittest.skip('')
    def test_calculate_log_probabilities_empty_frequencies(self):
        ngram = NGramTrie(2)
        ngram.n_gram_frequencies = {}

        actual = ngram.calculate_log_probabilities()
        self.assertEqual(ngram.n_gram_log_probabilities, {})
        self.assertEqual(1, actual)

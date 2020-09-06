# pylint: skip-file
"""
Checks the first lab dictionary functions
"""

import unittest
from lab_1.main import calculate_frequencies
from lab_1.main import get_top_n_words
from lab_1.main import get_concordance
from lab_1.main import get_adjacent_words


class CalculateFrequenciesTest(unittest.TestCase):
    """
    Tests calculating frequencies function
    """

    def test_calculate_frequencies_ideal(self):
        """
        Ideal calculate frequencies scenario
        """
        self.assertEqual(calculate_frequencies(['weather', 'sunny', 'man', 'happy']),
                         {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1})

    def test_calculate_frequencies_complex(self):
        """
        Calculate frequencies with several same tokens
        """
        self.assertEqual(calculate_frequencies(['weather', 'sunny', 'man', 'happy', 'weather', 'man']),
                         {'weather': 2, 'sunny': 1, 'man': 2, 'happy': 1})

    def test_calculate_frequencies_bad_input(self):
        """
        Calculate frequencies invalid input tokens check
        """
        bad_inputs = ['string', {}, (), None, 9, 9.34, True]
        for bad_input in bad_inputs:
            self.assertEqual(calculate_frequencies(bad_input), [])

    def test_calculate_frequencies_return_value(self):
        """
        Calculate frequencies return values check
        """
        tokens = ['token1', 'token2']
        output = calculate_frequencies(tokens)
        self.assertEqual(len(output), 2)
        for token in tokens:
            self.assertTrue(output[token])
        self.assertTrue(isinstance(output[tokens[0]], int))


class GetTopNWordsTest(unittest.TestCase):
    """
    Tests get top number of words function
    """

    def test_get_top_n_words_ideal(self):
        """
        Ideal get top number of words scenario
        """
        self.assertEqual(get_top_n_words({'happy': 2, 'man': 3}, 1), ['happy'])

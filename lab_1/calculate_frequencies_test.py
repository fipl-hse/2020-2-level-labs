# pylint: skip-file
"""
Checks the first lab calculate frequencies function
"""

import unittest
from main import calculate_frequencies


class CalculateFrequenciesTest(unittest.TestCase):
    """
    Tests calculating frequencies function
    """

    def test_calculate_frequencies_ideal(self):
        """
        Ideal calculate frequencies scenario
        """
        expected = {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
        actual = calculate_frequencies(['weather', 'sunny', 'man', 'happy'])
        self.assertEqual(expected, actual)

    def test_calculate_frequencies_complex(self):
        """
        Calculate frequencies with several same tokens
        """
        expected = {'weather': 2, 'sunny': 1, 'man': 2, 'happy': 1}
        actual = calculate_frequencies(['weather', 'sunny', 'man', 'happy', 'weather', 'man'])
        self.assertEqual(expected, actual)

    def test_calculate_frequencies_bad_input(self):
        """
        Calculate frequencies invalid input tokens check
        """
        bad_inputs = ['string', {}, (), None, 9, 9.34, True, [None]]
        expected = {}
        for bad_input in bad_inputs:
            actual = calculate_frequencies(bad_input)
            self.assertEqual(expected, actual)

    def test_calculate_frequencies_return_value(self):
        """
        Calculate frequencies return values check
        """
        tokens = ['token1', 'token2']
        expected = 2
        actual = calculate_frequencies(tokens)
        self.assertEqual(expected, len(actual))
        for token in tokens:
            self.assertTrue(actual[token])
        self.assertTrue(isinstance(actual[tokens[0]], int))

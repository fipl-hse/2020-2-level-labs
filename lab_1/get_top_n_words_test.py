# pylint: skip-file
"""
Checks the first lab get top words function
"""

import unittest
from main import get_top_n_words


class GetTopNWordsTest(unittest.TestCase):
    """
    Tests get top number of words function
    """

    def test_get_top_n_words_ideal(self):
        """
        Ideal get top number of words scenario
        """
        expected = ['man']
        actual = get_top_n_words({'happy': 2, 'man': 3}, 1)
        self.assertEqual(expected, actual)

    def test_get_top_n_words_same_frequency(self):
        """
        Get top number of words with the same frequency check
        """
        expected = ['happy', 'man']
        actual = get_top_n_words({'happy': 2, 'man': 2}, 2)
        self.assertEqual(expected, actual)
        expected = ['happy']
        actual = get_top_n_words({'happy': 2, 'man': 2}, 1)
        self.assertEqual(expected, actual)

    def test_get_top_n_words_more_number(self):
        """
        Get top number of words with bigger number of words than in dictionary
        """
        expected = ['man', 'happy']
        actual = get_top_n_words({'happy': 2, 'man': 3}, 10)
        self.assertEqual(expected, actual)

    def test_get_top_n_words_bad_inputs(self):
        """
        Get top number of words with bad argument inputs
        """
        bad_inputs = ['string', (), None, 9, 9.34, True, [None], []]
        expected = []
        for bad_input in bad_inputs:
            actual = get_top_n_words(bad_input, 2)
            self.assertEqual(expected, actual)

    def test_get_top_n_words_empty(self):
        """
        Get top number of words with empty arguments
        """
        expected = []
        actual = get_top_n_words({}, 10)
        self.assertEqual(expected, actual)

    def test_get_top_n_words_incorrect_numbers(self):
        """
        Get top number of words using incorrect number of words parameter
        """
        expected = []
        actual = get_top_n_words({}, -1)
        self.assertEqual(expected, actual)
        actual = get_top_n_words({'happy': 2}, 0)
        self.assertEqual(expected, actual)

# pylint: skip-file
"""
Checks the first lab stop words removal functions
"""

import unittest
from main import remove_stop_words


class RemoveStopWordsTest(unittest.TestCase):
    """
    Tests remove stop words function
    """
    STOP_WORDS = ['the', 'a', 'is']

    def test_remove_stop_words_ideal(self):
        """
        Ideal removing stop words scenario
        """
        expected = ['weather', 'sunny', 'man', 'happy']
        actual = remove_stop_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy'],
                                   RemoveStopWordsTest.STOP_WORDS)
        self.assertEqual(expected, actual)

    def test_remove_stop_words_bad_input(self):
        """
        Remove stop words bad input scenario
        """
        bad_inputs_first = [{}, (), None, 9, 9.34, True]
        bad_inputs_second = [{}, (), None, 9, 9.34, True]
        expected = []
        for bad_input in range(0, 5):
            actual_1 = remove_stop_words(bad_inputs_first[bad_input], bad_inputs_second[bad_input])
            actual_2 = remove_stop_words([], bad_inputs_second[bad_input])
            actual_3 = remove_stop_words(bad_inputs_first[bad_input], [])
            self.assertEqual(expected, actual_1)
            self.assertEqual(expected, actual_2)
            self.assertEqual(expected, actual_3)

    def test_remove_stop_words_no_stop_words(self):
        """
        Remove stop words without stop words scenario
        """
        expected = ['token1', 'token2']
        actual = remove_stop_words(['token1', 'token2'], [])
        self.assertEqual(expected, actual)

    def test_remove_stop_words_all_words(self):
        """
        Remove stop words as the whole text scenario
        """
        expected = []
        actual = remove_stop_words(['the', 'a', 'is'], RemoveStopWordsTest.STOP_WORDS)
        self.assertEqual(expected, actual)

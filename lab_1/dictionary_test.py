# pylint: skip-file
"""
Checks the first lab dictionary functions
"""

import unittest
from lab_1.main import calculate_frequencies
from lab_1.main import get_top_n_words
from lab_1.main import get_concordance
from lab_1.main import get_adjacent_words
from lab_1.main import get_and_sort_concordance


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
        bad_inputs = ['string', {}, (), None, 9, 9.34, True]
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
        bad_inputs = ['string', (), None, 9, 9.34, True]
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


class GetConcordanceTest(unittest.TestCase):
    """
    Tests get concordance function
    """

    def test_get_concordance_ideal(self):
        """
        Ideal get concordance scenario
        """
        expected = ['man is happy the dog is']
        actual = get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                  'the', 'dog', 'is', 'glad', 'but', 'the', 'cat', 'is', 'sad'],
                                 'happy', 2, 3)
        self.assertEqual(expected, actual)

    def test_get_concordance_several_contexts(self):
        """
        Checks that a concordance list can be created for several contexts
        """
        expected = ['man is happy the dog is', 'dog is happy but the cat']
        actual = get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                  'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'],
                                 'happy', 2, 3)
        self.assertEqual(expected, actual)

    def test_get_concordance_empty_inputs(self):
        """
        Checks that function can handle empty argument inputs
        """
        expected = []
        actual = get_concordance([], 'happy', 2, 3)
        self.assertEqual(expected, actual)
        actual = get_concordance(['happy'], '', 2, 3)
        self.assertEqual(expected, actual)
        expected = ['happy']
        actual = get_concordance(['happy'], 'happy', 0, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_bad_number_inputs(self):
        """
        Checks that function can handle incorrect number inputs
        """
        expected = ['happy']
        actual = get_concordance(['happy', 'man'], 'happy', -1, 0)
        self.assertEqual(expected, actual)
        expected = ['happy man']
        actual = get_concordance(['happy', 'man'], 'happy', 0, 1)
        self.assertEqual(expected, actual)
        expected = ['man']
        actual = get_concordance(['happy', 'man'], 'man', -1, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_bad_inputs(self):
        """
        Checks that function can handle incorrect inputs
        """
        bad_inputs = [[], {}, 'string', (), None, 9.34, True]
        expected = []
        for bad_input in bad_inputs:
            actual_1 = get_concordance(['happy', 'man', 'went'], 'man', bad_input, bad_input)
            actual_2 = get_concordance(bad_input, 'happy', 2, 3)
            actual_3 = get_concordance(['happy', 'man', 'went'], bad_input, 1, 2)
            self.assertEqual(expected, actual_1)
            self.assertEqual(expected, actual_2)
            self.assertEqual(expected, actual_3)


class GetAdjacentWordsTest(unittest.TestCase):
    """
    Tests get adjacent words function
    """

    def test_get_adjacent_words_ideal(self):
        """
        Ideal get adjacent words scenario
        """
        tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                  'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
        word = 'happy'
        left_n = 2
        right_n = 3

        expected = [('man', 'is'), ('dog', 'cat')]
        actual = get_adjacent_words(tokens, word, left_n, right_n)
        self.assertEqual(expected, actual)

    def test_get_adjacent_words_empty_inputs(self):
        """
        Checks that function can handle empty argument inputs
        """
        expected = []
        actual = get_adjacent_words([], 'happy', 2, 3)
        self.assertEqual(expected, actual)
        actual = get_adjacent_words(['happy'], '', 2, 3)
        self.assertEqual(expected, actual)

    def test_get_adjacent_words_bad_number_inputs(self):
        """
        Checks that function can handle incorrect number inputs
        """
        expected = []
        actual = get_adjacent_words(['happy', 'man'], 'happy', -1, 0)
        self.assertEqual(expected, actual)
        actual = get_adjacent_words(['happy', 'man'], 'man', -1, 0)
        self.assertEqual(expected, actual)
        expected = [('', 'man')]
        actual = get_adjacent_words(['happy', 'man'], 'happy', 0, 1)
        self.assertEqual(expected, actual)

    def test_get_adjacent_words_bad_inputs(self):
        """
        Checks that function can handle incorrect inputs
        """
        bad_inputs = [[], {}, 'string', (), None, 9.34, True]
        expected = []
        for bad_input in bad_inputs:
            actual_1 = get_adjacent_words(['happy', 'man', 'went'], 'man', bad_input, bad_input)
            actual_2 = get_adjacent_words(bad_input, 'happy', 2, 3)
            actual_3 = get_adjacent_words(['happy', 'man', 'went'], bad_input, 1, 2)
            self.assertEqual(expected, actual_1)
            self.assertEqual(expected, actual_2)
            self.assertEqual(expected, actual_3)


class GetAndSortConcordanceTest(unittest.TestCase):
    """
    Tests get and sort concordance function
    """

    @unittest.skip
    def test_get_and_sort_concordance_ideal(self):
        """
        Ideal get and sort concordance scenario
        """
        tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                  'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
        word = 'happy'
        left_range = 2
        right_range = 3
        left_sort = True

        expected = ['dog is happy but the cat', 'man is happy the dog is']
        actual = get_and_sort_concordance(tokens, word, left_range, right_range, left_sort)
        self.assertEqual(expected, actual)

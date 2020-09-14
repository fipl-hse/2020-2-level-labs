# pylint: skip-file
"""
Checks the first lab dictionary functions
"""

import unittest
from lab_1.main import calculate_frequencies
from lab_1.main import get_top_n_words
from lab_1.main import get_concordance
from lab_1.main import get_adjacent_words
from lab_1.main import sort_concordance


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


class GetConcordanceTest(unittest.TestCase):
    """
    Tests get concordance function
    """

    def test_get_concordance_ideal(self):
        """
        Ideal get concordance scenario
        """
        expected = [['man', 'is', 'happy', 'the', 'dog', 'is']]
        actual = get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                  'the', 'dog', 'is', 'glad', 'but', 'the', 'cat', 'is', 'sad'],
                                 'happy', 2, 3)
        self.assertEqual(expected, actual)

    def test_get_concordance_several_contexts(self):
        """
        Checks that a concordance list can be created for several contexts
        """
        expected = [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
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
        expected = []
        actual = get_concordance(['happy'], 'happy', 0, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_bad_number_inputs(self):
        """
        Checks that function can handle incorrect number inputs
        """
        expected = []
        actual = get_concordance(['happy', 'man'], 'happy', -1, 0)
        self.assertEqual(expected, actual)
        expected = [['happy', 'man']]
        actual = get_concordance(['happy', 'man'], 'happy', 0, 1)
        self.assertEqual(expected, actual)
        expected = []
        actual = get_concordance(['happy', 'man'], 'man', -1, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_big_right_number_input(self):
        """
        Checks if function can handle great right range numbers,
        that exceed the number of given tokens
        """
        expected = [['happy', 'man']]
        actual = get_concordance(['one', 'happy', 'man'], 'happy', 0, 1000)
        self.assertEqual(expected, actual)

    def test_get_concordance_big_left_number_input(self):
        """
        Checks if function can handle great left range numbers,
        that exceed the number of given tokens
        """
        expected = [['one', 'happy']]
        actual = get_concordance(['one', 'happy', 'man'], 'happy', 1000, 0)
        self.assertEqual(expected, actual)

    def test_get_concordance_bad_inputs(self):
        """
        Checks that function can handle incorrect inputs
        """
        bad_inputs = [[], {}, 'string', (), None, 9.34, True, [None]]
        expected = []
        for bad_input in bad_inputs:
            actual_1 = get_concordance(['happy', 'man', 'went'], 'man', bad_input, bad_input)
            actual_2 = get_concordance(bad_input, 'happy', 2, 3)
            actual_3 = get_concordance(['happy', 'man', 'went'], bad_input, 1, 2)
            self.assertEqual(expected, actual_1)
            self.assertEqual(expected, actual_2)
            self.assertEqual(expected, actual_3)


@unittest.skip
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

        expected = [['man', 'is'], ['dog', 'cat']]
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
        expected = [['man']]
        actual = get_adjacent_words(['happy', 'man'], 'happy', 0, 1)
        self.assertEqual(expected, actual)

    def test_get_adjacent_words_big_right_number_input(self):
        """
        Checks if function can handle great right range numbers,
        that exceed the number of given tokens
        """
        expected = [['man']]
        actual = get_adjacent_words(['one', 'happy', 'man'], 'happy', 0, 1000)
        self.assertEqual(expected, actual)

    def test_get_adjacent_word_big_left_number_input(self):
        """
        Checks if function can handle great left range numbers,
        that exceed the number of given tokens
        """
        expected = [['one']]
        actual = get_adjacent_words(['one', 'happy', 'man'], 'happy', 1000, 0)
        self.assertEqual(expected, actual)

    def test_get_adjacent_words_bad_inputs(self):
        """
        Checks that function can handle incorrect inputs
        """
        bad_inputs = [[], {}, 'string', (), None, 9.34, True, [None]]
        expected = []
        for bad_input in bad_inputs:
            actual_1 = get_adjacent_words(['happy', 'man', 'went'], 'man', bad_input, bad_input)
            actual_2 = get_adjacent_words(bad_input, 'happy', 2, 3)
            actual_3 = get_adjacent_words(['happy', 'man', 'went'], bad_input, 1, 2)
            self.assertEqual(expected, actual_1)
            self.assertEqual(expected, actual_2)
            self.assertEqual(expected, actual_3)


@unittest.skip
class GetAndSortConcordanceTest(unittest.TestCase):
    """
    Tests get and sort concordance function
    """

    def test_get_and_left_sort_concordance_ideal(self):
        """
        Ideal left sort concordance scenario
        """
        tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                  'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
        word = 'happy'
        left_context_size = 2
        right_context_size = 3
        left_sort = True

        expected = [['dog', 'is', 'happy', 'but', 'the', 'cat'], ['man', 'is', 'happy', 'the', 'dog', 'is']]
        actual = sort_concordance(tokens, word, left_context_size, right_context_size, left_sort)
        self.assertEqual(expected, actual)

    def test_get_and_right_sort_concordance_ideal(self):
        """
        Ideal right sort concordance scenario
        """
        tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                  'dog', 'is', 'happy', 'still', 'the', 'cat', 'is', 'sad']
        word = 'happy'
        left_context_size = 2
        right_context_size = 3
        left_sort = False

        expected = [['man', 'is', 'happy', 'dog', 'is', 'happy'], ['dog', 'is', 'happy', 'still', 'the', 'cat']]
        actual = sort_concordance(tokens, word, left_context_size, right_context_size, left_sort)
        self.assertEqual(expected, actual)

    def test_get_and_sort_concordance_bad_tokens_inputs(self):
        """
        Checks if function correctly handles incorrect tokens input
        """
        bad_inputs = [(), {}, '', None, True, 8, 8.94, [None]]
        expected = []
        for bad_input in bad_inputs:
            actual = sort_concordance(bad_input, 'happy', 2, 3, False)
            self.assertEqual(expected, actual)

    def test_get_and_sort_concordance_bad_word_inputs(self):
        """
        Checks if function correctly handles incorrect word input
        """
        bad_inputs = [(), {}, None, True, 8, 8.94, [None]]
        expected = []
        for bad_input in bad_inputs:
            actual = sort_concordance(['one', 'happy', 'man'], bad_input, 2, 3, True)
            self.assertEqual(expected, actual)

    def test_get_and_sort_concordance_bad_number_inputs(self):
        """
        Checks if function can handle incorrect range inputs
        """
        bad_inputs = [(), {}, None, True, [None]]
        expected = []
        for bad_input in bad_inputs:
            actual = sort_concordance(['happy'],
                                      'happy', bad_input, bad_input, True)
            self.assertEqual(expected, actual)

    def test_get_and_sort_concordance_bad_number_numeric_inputs(self):
        """
        Checks if function can handle incorrect numeric range inputs
        """
        expected = [['happy', 'man']]
        actual = sort_concordance(['one', 'happy', 'man'], 'happy', -1, 1000, True)
        self.assertEqual(expected, actual)

    def test_get_and_sort_concordance_bad_sorting_option_inputs(self):
        """
        Checks if function can handle incorrect sorting options
        """
        bad_inputs = [[], (), {}, '', None, 8, 8.99]
        expected = []
        for bad_input in bad_inputs:
            actual = sort_concordance(['one', 'happy', 'man'],
                                      'happy', 2, 3, bad_input)
            self.assertEqual(expected, actual)

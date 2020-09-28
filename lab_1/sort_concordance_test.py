# pylint: skip-file
"""
Checks the first lab dictionary functions
"""

import unittest

from main import read_from_file
from main import sort_concordance
from main import tokenize


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
        actual = sort_concordance(['one', 'happy', 'man'], 'happy', -1, 1000, False)
        self.assertEqual(expected, actual)

    def test_get_and_sort_concordance_context_size_with_no_context(self):
        """
        Checks if function can handle left or right context without given context
        """
        expected = []
        actual = sort_concordance(['one', 'happy', 'man'], 'happy', -1, 1000, True)
        self.assertEqual(expected, actual)
        actual = sort_concordance(['one', 'happy', 'man'], 'happy', 1000, -1, False)
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

    def test_big_text_get_and_sort_concordance_term(self):
        """
        Checks if a context sorts right for a given term and can be found properly
        """
        text = read_from_file('data.txt')
        tokens = tokenize(text)

        expected = [['although', 'less', 'compact', 'than', 'tex', 'the',
                     'xml', 'structuring', 'promises', 'to', 'make', 'it',
                     'widely', 'usable', 'and', 'allows', 'for', 'instant',
                     'display']]
        actual = sort_concordance(tokens, 'tex', 4, 14, True)
        self.assertEqual(expected, actual)

    def test_get_concordance_several_contexts_big_text_left(self):
        """
        Checks if contexts for a given term can be found in real text properly
        Taking into consideration left context
        """
        text = read_from_file('data.txt')
        tokens = tokenize(text)

        expected = [['by', 'sodium', 'bicarbonate'],
                    ['epithelial', 'sodium', 'channels'],
                    ['means', 'sodium', 'aluminate'],
                    ['the', 'sodium', 'salt']]
        actual = sort_concordance(tokens, 'sodium', 1, 1, True)
        self.assertEqual(expected, actual)

    def test_get_concordance_several_contexts_big_text_right(self):
        """
        Checks if contexts for a given term can be found in real text properly
        Taking into consideration right context
        """
        text = read_from_file('data.txt')
        tokens = tokenize(text)

        expected = [['means', 'sodium', 'aluminate'],
                    ['by', 'sodium', 'bicarbonate'],
                    ['epithelial', 'sodium', 'channels'],
                    ['the', 'sodium', 'salt']]
        actual = sort_concordance(tokens, 'sodium', 1, 1, False)
        self.assertEqual(expected, actual)
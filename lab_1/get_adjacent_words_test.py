# pylint: skip-file
"""
Checks the first lab adjacent words extraction
"""

import unittest

from main import get_adjacent_words
from main import read_from_file
from main import tokenize


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

    def test_big_text_get_adjacent_words_term(self):
        """
        Checks if adjacent words for a given term can be found properly
        """
        text = read_from_file('lab_1/data.txt')
        tokens = tokenize(text)
        expected = [['although', 'products']]
        actual = get_adjacent_words(tokens, 'tex', 4, 31)
        self.assertEqual(expected, actual)

    def test_get_adjacent_words_several_contexts_big_text(self):
        """
        Checks if adjacent words for a given term can be found in real text properly
        """
        text = read_from_file('lab_1/data.txt')
        tokens = tokenize(text)

        expected = [['epithelial', 'channels'],
                    ['means', 'aluminate'],
                    ['by', 'bicarbonate'],
                    ['the', 'salt']]
        actual = get_adjacent_words(tokens, 'sodium', 1, 1)
        self.assertEqual(expected, actual)
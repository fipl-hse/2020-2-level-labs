# pylint: skip-file
"""
Checks the first lab text preprocessing functions
"""

import unittest

from main import read_from_file
from main import tokenize


class TokenizeTest(unittest.TestCase):
    """
    Tests tokenize function
    """

    def test_tokenize_ideal(self):
        """
        Ideal tokenize scenario
        """
        expected = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
        actual = tokenize('The weather is sunny, the man is happy.')
        self.assertEqual(expected, actual)

    def test_tokenize_several_sentences(self):
        """
        Tokenize text with several sentences
        """
        expected = ['the', 'first', 'sentence', 'the', 'second', 'sentence']
        actual = tokenize('The first sentence. The second sentence.')
        self.assertEqual(expected, actual)

    def test_tokenize_punctuation_marks(self):
        """
        Tokenize text with different punctuation marks
        """
        expected = ['the', 'first', 'sentence', 'nice', 'the', 'second', 'sentence', 'bad']
        actual = tokenize('The, first sentence - nice. The second sentence: bad!')
        self.assertEqual(expected, actual)

    def test_tokenize_dirty_text(self):
        """
        Tokenize dirty text
        """
        expected = ['the', 'first', 'sentence', 'the', 'second', 'sentence']
        actual = tokenize('The first% sentence><. The sec&*ond sent@ence #.')
        self.assertEqual(expected, actual)

    def test_tokenize_bad_input(self):
        """
        Tokenize bad input argument scenario
        """
        bad_inputs = [[], {}, (), None, 9, 9.34, True]
        expected = []
        for bad_input in bad_inputs:
            actual = tokenize(bad_input)
            self.assertEqual(expected, actual)

    def test_tokenize_big_text_case(self):
        """
        Tokenize big input text scenario
        """
        text = read_from_file('tokens.txt')

        expected = text.split()
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_tokenize_big_text_length_equal(self):
        """
        Tokenize big input text and assert equal
        """
        text = read_from_file('tokens.txt')

        expected = len(text.split())
        actual = len(tokenize(text))
        self.assertEqual(expected, actual)

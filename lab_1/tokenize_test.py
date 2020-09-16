# pylint: skip-file
"""
Checks the first lab text tokenizing functions
"""

import unittest
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

    @unittest.skip
    def test_tokenize_line_breaks(self):
        """
        Tokenize text with line breaks
        """
        expected = ['the', 'first', 'sentence', 'the', 'second', 'sentence']
        actual = tokenize('The first sentence.<br /><br />The second sentence.')
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

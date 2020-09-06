# pylint: skip-file
"""
Checks the first lab tokenize function
"""

import unittest
from lab_1.main import tokenize


class TokenizeTest(unittest.TestCase):
    """
    Tests token creation
    """

    def test_tokenize_ideal(self):
        """
        Ideal tokenize scenario
        """
        self.assertEqual(tokenize('The weather is sunny, the man is happy.'),
                         ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy'])

    def test_tokenize_several_sentences(self):
        """
        Tokenize text with several sentences
        """
        self.assertEqual(tokenize('The first sentence. The second sentence.'),
                         ['the', 'first', 'sentence', 'the', 'second', 'sentence'])

    def test_tokenize_punctuation_marks(self):
        """
        Tokenize text with different punctuation marks
        """
        self.assertEqual(tokenize('The, first sentence - nice. The second sentence: bad!'),
                         ['the', 'first', 'sentence', 'nice', 'the', 'second', 'sentence', 'bad'])

    def test_tokenize_dirty_text(self):
        """
        Tokenize dirty text
        """
        self.assertEqual(tokenize('The first% sentence><. The sec&*ond sent@ence #.'),
                         ['the', 'first', 'sentence', 'the', 'second', 'sentence'])

    def test_tokenize_line_breaks(self):
        """
        Tokenize text with line breaks
        """
        self.assertEqual(tokenize('The first sentence.<br /><br />The second sentence.'),
                         ['the', 'first', 'sentence', 'the', 'second', 'sentence'])

    def test_tokenize_bad_input(self):
        """
        Tokenize bad input argument scenario
        """
        bad_inputs = [[], {}, (), None, 9, 9.34, True]
        for bad_input in bad_inputs:
            self.assertEqual(tokenize(bad_input), [])

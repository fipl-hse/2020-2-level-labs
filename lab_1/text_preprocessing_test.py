# pylint: skip-file
"""
Checks the first lab text preprocessing functions
"""

import unittest
from lab_1.main import tokenize
from lab_1.main import remove_stop_words


class TokenizeTest(unittest.TestCase):
    """
    Tests tokenize function
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


class RemoveStopWordsTest(unittest.TestCase):
    """
    Tests remove stop words function
    """
    STOP_WORDS = ['the', 'a', 'is']

    def test_remove_stop_words_ideal(self):
        """
        Ideal removing stop words scenario
        """
        self.assertEqual(remove_stop_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy'],
                                           RemoveStopWordsTest.STOP_WORDS), ['weather', 'sunny', 'man', 'happy'])

    def test_remove_stop_words_bad_input(self):
        """
        Remove stop words bad input scenario
        """
        bad_inputs_first = [{}, (), None, 9, 9.34, True]
        bad_inputs_second = [{}, (), None, 9, 9.34, True]
        for bad_input in range(0, 5):
            self.assertEqual(remove_stop_words(bad_inputs_first[bad_input], bad_inputs_second[bad_input]), [])
            self.assertEqual(remove_stop_words([], bad_inputs_second[bad_input]), [])
            self.assertEqual(remove_stop_words(bad_inputs_first[bad_input], []), [])

    def test_remove_stop_words_no_stop_words(self):
        """
        Remove stop words without stop words scenario
        """
        self.assertEqual(remove_stop_words(['token1', 'token2'], []), ['token1', 'token2'])

    def test_remove_stop_words_all_words(self):
        """
        Remove stop words as the whole text scenario
        """
        self.assertEqual(remove_stop_words(['the', 'a', 'is'], RemoveStopWordsTest.STOP_WORDS), [])

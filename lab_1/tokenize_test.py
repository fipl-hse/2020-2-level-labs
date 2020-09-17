# pylint: skip-file
"""
Checks the first lab text preprocessing functions
"""

import unittest
from main import tokenize
from main import remove_stop_words
from main import read_from_file


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

    def test_tokenize_big_text_case(self):
        """
        Tokenize big input text scenario
        """
        text = read_from_file('lab_1/tokens.txt')

        expected = text.split()
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_tokenize_big_text_length_equal(self):
        """
        Tokenize big input text and assert equal
        """
        text = read_from_file('lab_1/tokens.txt')

        expected = len(text.split())
        actual = len(tokenize(text))
        self.assertEqual(expected, actual)


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

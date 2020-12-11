# pylint: skip-file
"""
Tests for tokenize_by_sentence_function
"""

import unittest
from lab_4.main import tokenize_by_sentence


class TokenizeBySentenceTest(unittest.TestCase):
    """
    checks for tokenize_by_sentence function.
        All tests should pass for score 4 or above
    """
    def test_tokenize_by_sentence_ideal(self):
        """
        Tests that tokenize_by_sentence function
            can handle ideal two sentence input
        """
        text = 'I have a cat.\nHis name is Bruno'
        expected = ('i', 'have', 'a', 'cat', '<END>',
                    'his', 'name', 'is', 'bruno', '<END>')
        actual = tokenize_by_sentence(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_sentence_punctuation_marks(self):
        """
        Tests that tokenize_by_sentence function
            can process and ignore different punctuation marks
        """
        text = 'The, first sentence - nice? The second sentence: bad!'
        expected = ('the', 'first', 'sentence', 'nice', '<END>',
                    'the', 'second', 'sentence', 'bad', '<END>')
        actual = tokenize_by_sentence(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_sentence_dirty_text(self):
        """
        Tests that tokenize_by_sentence function
            can handle text filled with inappropriate characters
        """
        text = 'The first% sentence><. The sec&*ond sent@ence #.'
        expected = ('the', 'first', 'sentence', '<END>',
                    'the', 'second', 'sentence', '<END>')
        actual = tokenize_by_sentence(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_sentence_incorrect_input(self):
        """
        Tests that tokenize_by_sentence function
            can handle incorrect input cases
        """
        bad_inputs = [[], {}, (), None, 9, 9.34, True]
        for bad_input in bad_inputs:
            self.assertRaises(ValueError, tokenize_by_sentence, bad_input)

    def test_tokenize_by_sentence_complex(self):
        """
        Tests that tokenize_by_sentence function
            can handle complex split case
        """
        text = 'Mar#y wa$nted, to swim. However, she was afraid of sharks.'
        expected = ('mary', 'wanted', 'to', 'swim', '<END>',
                    'however', 'she', 'was', 'afraid', 'of', 'sharks', '<END>')
        actual = tokenize_by_sentence(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_sentence_empty_sentence(self):
        """
        Tests that tokenize_by_sentence function
            can handle empty sentence input
        """
        text = ''
        expected = ()
        actual = tokenize_by_sentence(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_sentence_inappropriate_sentence(self):
        """
        Tests that tokenize_by_sentence function
            can handle inappropriate sentence input
        """
        text = '$#&*@#$*#@)'
        expected = ()
        actual = tokenize_by_sentence(text)
        self.assertEqual(expected, actual)

    # extra tests
    def test_tokenize_by_sentence_adds_ends(self):
        '''
        Tests that number of "<END>" corresponds
            the number of sentences
        '''
        text = '''There are many big and small libraries everywhere in our country. 
                  They have millions of books in different languages. 
                  You can find there the oldest and the newest books.'''
        expected_end_num = 3
        actual_end_num = tokenize_by_sentence(text).count('<END>')
        self.assertEqual(expected_end_num, actual_end_num)

    def test_tokenize_text_lower_case(self):
        '''
        Tests that tokens in encoded text
            are all in a lower case (except "<END>")
        '''
        text = '''There are many big and small libraries everywhere in our country. 
                  They have millions of books in different languages. 
                  You can find there the oldest and the newest books.'''
        tokenized_text = tokenize_by_sentence(text)

        actual = True
        for token in tokenized_text:
            if token != '<END>' and token.isupper():
                actual = False
        self.assertTrue(actual)

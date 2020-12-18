# pylint: skip-file
"""
Tests encode_text function
"""

import unittest
from lab_4.main import encode_text
from lab_4.main import WordStorage
from unittest.mock import patch


class EncodeCorpusTest(unittest.TestCase):
    """
    checks for encode_text function.
        Score 4 or above function
    """
    @unittest.skip('')
    def test_encode_text_ideal(self):
        """
        Tests that encode_text function
            generates id for each word
        """
        word_storage = WordStorage()

        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')

        word_storage.update(corpus)

        actual = encode_text(word_storage, corpus)

        for token in actual:
            self.assertTrue(isinstance(token, int))

    @unittest.skip('')
    def test_encode_text_same_words_count(self):
        """
        Tests that encode_text function
            can assign correct id to the same words
        """
        word_storage = WordStorage()

        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'i', 'have', 'a', 'cat', '<END>')

        word_storage.update(corpus)

        actual = encode_text(word_storage, corpus)

        self.assertEqual(actual[:5], actual[5:])

    @unittest.skip('')
    def test_encode_text_inappropriate_sentence(self):
        """
        Tests that encode_text function
            can handle inappropriate sentence inputs
        """
        word_storage = WordStorage()
        bad_inputs = [None, 123, 'test', [], {}]

        for bad_input in bad_inputs:
            self.assertRaises(ValueError, encode_text, word_storage, bad_input)

    @unittest.skip('')
    def test_encode_text_inappropriate_storage_instance(self):
        """
        Tests that encode_text function
            can handle inappropriate storage instance inputs
        """
        bad_inputs = [None, 123, 'test', [], {}]
        corpus = ('i', 'have', 'a', 'cat', '<END>')

        for bad_input in bad_inputs:
            self.assertRaises(ValueError, encode_text, bad_input, corpus)

    @unittest.skip('')
    def test_encode_text_empty_sentence(self):
        """
        Tests that encode_corpus function
            can handle empty sentence input
        """
        word_storage = WordStorage()
        corpus = ()
        expected = ()
        word_storage.update(corpus)
        actual = encode_text(word_storage, corpus)
        self.assertEqual(expected, actual)

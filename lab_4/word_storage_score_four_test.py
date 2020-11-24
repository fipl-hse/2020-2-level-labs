# pylint: skip-file
"""
Tests WordStorage class
"""

import unittest
from lab_4.main import WordStorage
from unittest.mock import patch


class WordStorageTest(unittest.TestCase):
    """
    check WordStorage class functionality.
        All tests should pass for score 4 or above
    """

    @unittest.skip('')
    def test_word_storage_correct_instance_creation(self):
        """
        word storage instance creates with correct attributes
        """
        word_storage = WordStorage()
        expected = {}
        self.assertEqual(word_storage.storage, expected)

# --------------------------------------------------------
    @unittest.skip('')
    def test_word_storage_put_word_ideal(self):
        """
        word is added to storage
        """
        word_storage = WordStorage()
        word = 'word'
        expected = 1
        actual = word_storage._put_word(word)
        self.assertTrue(word in word_storage.storage)
        self.assertEqual(expected, actual)

    @unittest.skip('')
    def test_word_storage_put_word_none(self):
        """
        none is not added to storage
        """
        word_storage = WordStorage()
        letter = None
        self.assertRaises(ValueError, word_storage._put_word, letter)
        self.assertEqual(word_storage.storage, {})

    @unittest.skip('')
    def test_word_storage_put_word_not_str(self):
        """
        non string word is not added to storage
        """
        word_storage = WordStorage()
        letter = 123
        self.assertRaises(ValueError, word_storage._put_word, letter)
        self.assertEqual(word_storage.storage, {})

    @unittest.skip('')
    def test_word_storage_put_word_existing(self):
        """
        existing word is not added to storage
        """
        word_storage = WordStorage()
        word = 'word'
        word_storage.storage = {'word': 1}
        expected = 1
        actual = word_storage._put_word(word)
        self.assertEqual(word_storage.storage, {'word': 1})
        self.assertEqual(expected, actual)

# -----------------------------------------------------------------
    @unittest.skip('')
    def test_word_storage_get_id_ideal(self):
        """
        ideal case for get_id
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        expected = 1
        actual = word_storage.get_id('word')
        self.assertEqual(expected, actual)

    @unittest.skip('')
    def test_word_storage_get_id_none(self):
        """
        get_id none
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        self.assertRaises(ValueError, word_storage.get_id, None)

    @unittest.skip('')
    def test_word_storage_get_id_not_str(self):
        """
        id is not str get_id
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        self.assertRaises(ValueError, word_storage.get_id, 123)

    @unittest.skip('')
    def test_word_storage_get_id_not_in_storage(self):
        """
        word not in storage
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        self.assertRaises(KeyError, word_storage.get_id, 'word2')

# -----------------------------------------------------------
    @unittest.skip('')
    def test_word_storage_update_ideal(self):
        """
        ideal case for update
        """
        word_storage = WordStorage()
        corpus = ('i', 'have', 'a', 'cat', '<END>',
                  'his', 'name', 'is', 'bruno', '<END>')
        word_storage.update(corpus)
        self.assertEqual(len(word_storage.storage), 9)

    @unittest.skip('')
    def test_word_storage_update_duplicates(self):
        """
        ideal case for update
        """
        word_storage = WordStorage()
        sentences = ('i', 'have', 'a', 'cat', '<END>',
                     'i', 'have', 'a', 'cat', '<END>')
        word_storage.update(sentences)
        self.assertEqual(len(word_storage.storage), 5)

    @unittest.skip('')
    def test_word_storage_update_empty(self):
        """
        ideal case for update
        """
        word_storage = WordStorage()
        sentences = ()
        word_storage.update(sentences)
        self.assertEqual(word_storage.storage, {})

    @unittest.skip('')
    def test_word_storage_update_none(self):
        """
        ideal case for update
        """
        word_storage = WordStorage()
        self.assertRaises(ValueError, word_storage.update, None)
        self.assertEqual(word_storage.storage, {})

    @unittest.skip('')
    def test_word_storage_update_not_tuple(self):
        """
        ideal case for update
        """
        word_storage = WordStorage()
        sentences = ['i', 'have', 'a', 'cat', '<END>']
        self.assertRaises(ValueError, word_storage.update, sentences)
        self.assertEqual(word_storage.storage, {})

    @patch('lab_4.main.WordStorage._put_word', side_effect=WordStorage()._put_word)
    @unittest.skip('')
    def test_word_storage_update_calls_required_function(self, mock):
        """
        ideal case for update calling _put_word method
        """
        word_storage = WordStorage()
        sentences = ('i', 'have', 'a', 'cat', '<END>')
        word_storage.update(sentences)
        self.assertTrue(mock.called)

# ------------------------------------------------------------------------------------
    @unittest.skip('')
    def test_word_storage_get_word_ideal(self):
        """
        ideal case for get_word
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        expected = 'word'
        actual = word_storage.get_word(1)
        self.assertEqual(expected, actual)

    @unittest.skip('')
    def test_word_storage_get_word_none(self):
        """
        get_word none
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        self.assertRaises(ValueError, word_storage.get_word, None)

    @unittest.skip('')
    def test_word_storage_get_word_not_num(self):
        """
        id is not str get_word
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        self.assertRaises(ValueError, word_storage.get_word, 'word2')

    @unittest.skip('')
    def test_word_storage_get_word_not_in_storage(self):
        """
        word not in storage
        """
        word_storage = WordStorage()
        word_storage.storage = {'word': 1}
        self.assertRaises(KeyError, word_storage.get_word, 123)

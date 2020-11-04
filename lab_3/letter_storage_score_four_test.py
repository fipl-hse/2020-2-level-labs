# pylint: skip-file
"""
Tests LetterStorage class
"""

import unittest
from lab_3.main import LetterStorage
from unittest.mock import patch


class LetterStorageTest(unittest.TestCase):
    """
    check LetterStorage class functionality.
        All tests should pass for score 4 or above
    """

    def test_letter_storage_correct_instance_creation(self):
        """
        letter storage instance creates with correct attributes
        """
        letter_storage = LetterStorage()
        expected = {}
        self.assertEqual(letter_storage.storage, expected)

# --------------------------------------------------------

    def test_letter_storage_put_letter_ideal(self):
        """
        letter is added to storage
        """
        letter_storage = LetterStorage()
        letter = 'w'
        expected = 0
        actual = letter_storage._put_letter(letter)
        self.assertTrue(letter in letter_storage.storage)
        self.assertEqual(expected, actual)

    def test_letter_storage_put_letter_none(self):
        """
        none is not added to storage
        """
        letter_storage = LetterStorage()
        letter = None
        expected = 1
        actual = letter_storage._put_letter(letter)
        self.assertEqual(letter_storage.storage, {})
        self.assertEqual(expected, actual)

    def test_letter_storage_put_letter_not_str(self):
        """
        non string letter is not added to storage
        """
        letter_storage = LetterStorage()
        letter = 123
        expected = 1
        actual = letter_storage._put_letter(letter)
        self.assertEqual(letter_storage.storage, {})
        self.assertEqual(expected, actual)

    def test_letter_storage_put_letter_existing(self):
        """
        existing letter is not added to storage
        """
        letter_storage = LetterStorage()
        letter = 'w'
        letter_storage.storage = {'w': 1}
        expected = 0
        actual = letter_storage._put_letter(letter)
        self.assertEqual(letter_storage.storage, {'w': 1})
        self.assertEqual(expected, actual)

# -----------------------------------------------------------------

    def test_letter_storage_get_id_by_letter_ideal(self):
        """
        ideal case for get_id_by_letter
        """
        letter_storage = LetterStorage()
        letter_storage.storage = {'w': 1}
        expected = 1
        actual = letter_storage.get_id_by_letter('w')
        self.assertEqual(expected, actual)

    def test_letter_storage_get_id_by_letter_none(self):
        """
        get_id_by_letter none
        """
        letter_storage = LetterStorage()
        letter_storage.storage = {'w': 1}
        expected = -1
        actual = letter_storage.get_id_by_letter(None)
        self.assertEqual(expected, actual)

    def test_letter_storage_get_id_by_letter_not_str(self):
        """
        id is not str  get_id_by_letter
        """
        letter_storage = LetterStorage()
        letter_storage.storage = {'w': 1}
        expected = -1
        actual = letter_storage.get_id_by_letter(123)
        self.assertEqual(expected, actual)

    def test_letter_storage_get_id_by_letter_not_in_storage(self):
        """
        letter not in storage
        """
        letter_storage = LetterStorage()
        letter_storage.storage = {'w': 1}
        expected = -1
        actual = letter_storage.get_id_by_letter('a')
        self.assertEqual(expected, actual)

# -----------------------------------------------------------

    def test_letter_storage_update_ideal(self):
        """
        ideal case for update
        """
        letter_storage = LetterStorage()
        sentence = (('_', 't', 'e', 's', 't', '_'), )
        expected = 0
        actual = letter_storage.update(sentence)
        self.assertEqual(len(letter_storage.storage), 4)
        self.assertEqual(expected, actual)

    def test_letter_storage_update_duplicates(self):
        """
        ideal case for update
        """
        letter_storage = LetterStorage()
        sentence = (('_', 't', 'e', 's', 't', '_'),
                    ('_', 't', 'e', 's', 't', '_'))
        expected = 0
        actual = letter_storage.update(sentence)
        self.assertEqual(len(letter_storage.storage), 4)
        self.assertEqual(expected, actual)

    def test_letter_storage_update_empty(self):
        """
        ideal case for update
        """
        letter_storage = LetterStorage()
        sentence = ()
        expected = 0
        actual = letter_storage.update(sentence)
        self.assertEqual(letter_storage.storage, {})
        self.assertEqual(expected, actual)

    def test_letter_storage_update_none(self):
        """
        ideal case for update
        """
        letter_storage = LetterStorage()
        sentence = None
        expected = 1
        actual = letter_storage.update(sentence)
        self.assertEqual(letter_storage.storage, {})
        self.assertEqual(expected, actual)

    def test_letter_storage_update_not_tuple(self):
        """
        ideal case for update
        """
        letter_storage = LetterStorage()
        sentences = [('_', 't', 'e', 's', 't', '_'),
                     ('_', 's', 'e', 'c', 'o', 'n', 'd', '_')]
        expected = 1
        actual = letter_storage.update(sentences)
        self.assertEqual(letter_storage.storage, {})
        self.assertEqual(expected, actual)

    @patch('lab_3/main.LetterStorage._put_letter', side_effect=LetterStorage()._put_letter)
    def test_letter_storage_update_calls_required_function(self, mock):
        """
        ideal case for update calling put_letter method
        """
        letter_storage = LetterStorage()
        sentences = (('_', 't', 'e', 's', 't', '_'),)
        letter_storage.update(sentences)
        self.assertTrue(mock.called)

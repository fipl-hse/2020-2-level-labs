"""
Tests tokenize_by_lines function
"""

import unittest
from lab_2.main import tokenize_by_lines


class TokenizeByLinesTest(unittest.TestCase):
    """
    Checks for tokenize_bby_lines function
    """

    def test_tokenize_by_lines_template(self):
        """
        Tests that tokenize_by_lines function
            can handle ...
        """
        text = 'I have a cat.\nHis name is Bruno'

        expected = (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
        actual = tokenize_by_lines(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_lines_template(self):
        """
        Tests that tokenize_by_lines function
            can handle ...
        """

    def test_tokenize_by_lines_template(self):
        """
        Tests that tokenize_by_lines function
            can handle ...
        """


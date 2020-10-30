"""
Tests tokenize_by_lines function
"""

import unittest
from main import tokenize_by_lines
import tokenizer


class TokenizeByLinesTest(unittest.TestCase):
    """
    Checks for tokenize_bby_lines function
    """

    def test_tokenize_by_lines_ideal(self):
        """
        Tests that tokenize_by_lines function
            can handle ...
        """
        text = 'I have a cat.\nHis name is Bruno'

        expected = (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
        actual = tokenize_by_lines(text)
        self.assertEqual(expected, actual)

    def test_tokenize_by_lines_more_lines(self):
        """
        Tests that tokenize_by_lines function
            can handle ...
        """
        text = """
        I have a cat.\nHis name is Bruno.\n
        He is white and beautiful.\n
        """

        expected = (('i', 'have', 'a', 'cat'),
                    ('his', 'name', 'is', 'bruno'),
                    ('he', 'is', 'white', 'and', 'beautiful'))

        actual = tokenize_by_lines(text)
        self.assertEqual(expected, actual)

"""
Tests fill_lcs_matrix function
"""

import unittest
from unittest.mock import patch
from lab_2.main import fill_lcs_matrix, create_zero_matrix


class FillLcsMatrixTest(unittest.TestCase):
    """
    Checks for fill_lcs_matrix function
    """

    def test_fill_lcs_matrix_ideal(self):
        """
        Tests that fills_lcs_matrix function
            can handle ideal case
        """
        expected = [[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 2, 2],
                    [1, 1, 2, 2]]

        sentence_first = ('the', 'dog', 'is', 'running')
        sentence_second = ('the', 'cat', 'is', 'sleeping')
        actual = fill_lcs_matrix(sentence_first, sentence_second)
        self.assertEqual(expected, actual)

    def test_fill_lcs_matrix_complex(self):
        """
        Tests that fill_lcs_matrix function
            can handle complex comparison
        """
        expected = [[1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 2, 2, 2],
                    [1, 1, 2, 2, 2],
                    [1, 1, 2, 2, 3]]

        sentence_first = ('the', 'dog', 'is', 'running', 'here')
        sentence_second = ('the', 'cat', 'is', 'sleeping', 'here')
        actual = fill_lcs_matrix(sentence_first, sentence_second)
        self.assertEqual(expected, actual)

    def test_fill_lcs_matrix_no_diff(self):
        """
        Tests that fill_lcs_matrix function
            can handle fully different sentences
        """
        expected = [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]

        sentence_first = ('the', 'dog', 'is', 'running', 'here')
        sentence_second = ('a', 'boy', 'plays', 'with', 'ball')
        actual = fill_lcs_matrix(sentence_first, sentence_second)
        self.assertEqual(expected, actual)

    def test_fill_lcs_matrix_reverse_behaviour(self):
        """
        Tests that fill_lcs_matrix function
            generates correct output even if shuffled sentences
        """
        sentence_first = ('the', 'dog', 'is', 'running')
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        actual = fill_lcs_matrix(sentence_first, sentence_second)
        actual_reverse = fill_lcs_matrix(sentence_second, sentence_first)
        self.assertEqual(actual, actual_reverse)

    @patch('lab_2.main.create_zero_matrix', side_effect=create_zero_matrix)
    def test_fill_lcs_matrix_calls_required_function(self, mock):
        """
        Tests that fill_lcs_matrix function
            calls create_zero_matrix function inside
        """
        sentence_first = ('the', 'dog', 'is', 'running')
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        fill_lcs_matrix(sentence_first, sentence_second)
        self.assertTrue(mock.called)

    def test_fill_lcs_matrix_empty_input(self):
        """
        Tests that fill_lcs_matrix function
            can generate correct output if provided with empty params
        """
        sentence_first = ()
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        expected = []
        actual = fill_lcs_matrix(sentence_first, sentence_second)
        self.assertEqual(expected, actual)

        actual_second = fill_lcs_matrix(sentence_second, sentence_first)
        self.assertEqual(expected, actual_second)

    def test_fill_lcs_matrix_check_output(self):
        """
        Tests that fill_lcs_matrix function
            can generate correct output according to given specs
        """
        sentence_first = ('the', 'dog', 'is', 'running')
        sentence_second = ('the', 'cat', 'is', 'sleeping')
        actual = fill_lcs_matrix(sentence_first, sentence_second)

        passed = True
        for row in actual:
            for column in row:
                if not isinstance(column, int):
                    passed = False
                    break
        self.assertTrue(passed)

    def test_fill_lcs_matrix_check_incorrect_inputs(self):
        """
        Tests that fill_lcs_matrix function
            can generate correct output according to given specs
        """
        expected = []
        bad_inputs = [[], {}, '', 9.22, -1, 0, -6, None, True, (None, None)]
        patches_sentence = ('the', 'dog', 'is', 'running')

        for bad_input in bad_inputs:
            actual_first = fill_lcs_matrix(bad_input, patches_sentence)
            actual_second = fill_lcs_matrix(patches_sentence, bad_input)
            self.assertEqual(expected, actual_first)
            self.assertEqual(expected, actual_second)

    def test_fill_lcs_matrix_empty_tokens(self):
        """
        Tests that fill_lcs_matrix function
            can handle case with empty string tokens as params
        """
        expected = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

        sentence_empty = ('', '', '', '')
        sentence_filled = ('the', 'cat', 'is', 'sleeping')

        actual = fill_lcs_matrix(sentence_empty, sentence_filled)
        actual_reversed = fill_lcs_matrix(sentence_filled, sentence_empty)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_reversed)

    def test_fill_lcs_matrix_fills_different_sized_inputs(self):
        """
        Tests that fill_lcs_matrix function
            can generate correct input if provided with sentences of different length
        """
        expected = [[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]]

        expected_reversed = [[1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1]]

        sentence_first = ('the','dog','sleeps')
        sentence_second = ('the', 'cat', 'is', 'sleeping')

        actual = fill_lcs_matrix(sentence_first, sentence_second)
        actual_reversed = fill_lcs_matrix(sentence_second, sentence_first)
        self.assertEqual(expected, actual)
        self.assertEqual(expected_reversed, actual_reversed)


if __name__ == "__main__":
    unittest.main()
